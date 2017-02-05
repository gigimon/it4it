Title: [Перевод] Поиск утечек памяти в тестах с py.test
Date: 2017-01-06 01:20
Category: Python, py.test, тестирование, memory leak
Slug: pytest-memory
Summary: [Перевод] Поиск утечек памяти в тестах с py.test

*Данная заметка это перевод статьи [https://nvbn.github.io/2017/02/02/pytest-leaking/](https://nvbn.github.io/2017/02/02/pytest-leaking/) посвященной поиску утечек памяти в тестах.*

На одном из наших проектов у нас была проблема с утечкой памяти в тестах, проблема была очень велика, т.к. каждый раз какой-то из тестов утекал на несколько Гб. Мы пробовали [https://github.com/abalkin/pytest-leaks](pytest-leaks), но он оказался избыточен и не работал с нашей версией python. Поэтому мы написали свой небольшой детектор утечек.

В первую очередь мы получаем используемую RAM с помощью [psutil](https://github.com/giampaolo/psutil):

```python
import os
from psutil import Process

_proc = Process(os.getpid())


def get_consumed_ram():
    return _proc.memory_info().rss
```

Затем мы создали лог использования RAM памяти, где *nodeid* это специальная репрезентация теста в pytest, например *tests/test_service.py::TestRemoteService::test_connection*:

```python
from collections import namedtuple

START = 'START'
END = 'END'
ConsumedRamLogEntry = namedtuple('ConsumedRamLogEntry', ('nodeid', 'on', 'consumed_ram'))
consumed_ram_log = []
```

И логгируем использование памяти с помощью pytest хуков, просто добавив код в *conftest.py*:

```python
def pytest_runtest_setup(item):
    log_entry = ConsumedRamLogEntry(item.nodeid, START, get_consumed_ram())
    consumed_ram_log.append(log_entry)

def pytest_runtest_teardown(item):
    log_entry = ConsumedRamLogEntry(item.nodeid, END, get_consumed_ram())
    consumed_ram_log.append(log_entry)
```

Pytest вызывает *pytest\_runtest\_setup* до запуска каждого теста, а *pytest\_runtest\_teardown* после.

И после всех тестов мы выводим всю информацию об утечках в тестах превышающих допустимую границу (10Мб в нашем случае) через *pytest\_terminal\_summary* хук:

```python
from itertools import groupby

LEAK_LIMIT = 10 * 1024 * 1024


def pytest_terminal_summary(terminalreporter):
    grouped = groupby(consumed_ram_log, lambda entry: entry.nodeid)
    for nodeid, (start_entry, end_entry) in grouped:
        leaked = end_entry.consumed_ram - start_entry.consumed_ram
        if leaked > LEAK_LIMIT:
            terminalreporter.write('LEAKED {}MB in {}\n'.format(
                leaked / 1024 / 1024, nodeid))
```

И после запуска всех тестов, получаем список текучих тестов:

```
LEAKED 712MB in tests/test_service.py::TestRemoteService::test_connection
```
