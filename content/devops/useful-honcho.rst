Полезная утилита для разработчиков - honcho
-------------------------------------------
:date: 2014-04-18 00:04
:author: gigimon
:category: Devops
:tags: devops, heroku, полезности
:slug: useful-honcho

Бороздя просторы интернета, наткнулся на клевую штуковину от heroku - `Procfile <https://devcenter.heroku.com/articles/procfile>`_
Это небольшая идеология (наверно), заключающаяся в быстром запуске каких-либо процессов используя специальный файл с именем Procfile, в котором описываются в формате "название команды: команда" команды для запуска процессов. Обычно это требуется для быстрого деплоя либо запуска чего-то постоянно. Я это использую при разработке и запуске dev окружения (поднятия вагранта, запуск базы, запуск воркеров), чтобы запустить сразу кучу процессов и разом их по Ctrl-C убить. 

Для работы с этими Procfile существует целая куча программ написаных на разных языках, но обычно полностью совместимые между собой, как по командному интерфейсу, так и по выводу, можно отметить следующие:

- `Foreman <https://github.com/ddollar/foreman>`_ на Ruby
- `Honcho <https://github.com/nickstenning/honcho>`_ на православном Python
- `Shoreman <https://github.com/hecticjeff/shoreman>`_ на shell
- `Norman <https://github.com/josh/norman>`_ node.js имплементация О_о
- `Forego <https://github.com/ddollar/forego>`_ на модном Go

Я же использую python реализацию - honcho.

Устанавливается он очень просто:

.. code-block:: bash

    pip install honcho


Все, после этого в системе доступен как honcho.

Затем, в любой директории где находимся создаем Procfile и наполняем его согласно своей нужде, для примера мой:

.. code-block:: bash

    celery: vagrant ssh -c "cd /vagrant && celery worker -n worker.base -A workers -l DEBUG"
    meteor: bash -c "cd front && exec meteor"


Теперь, находясь в директории с этим Procfile мы можем запускать либо сразу все процессы, либо какой-то отдельный, используя следующие команды соответственно:

.. code-block:: bash

    honcho run

    honcho start meteor


После этого, будет запущен honcho, который запустит эти процессы и красиво выведет их stdout:

.. code-block:: bash

    $ honcho start meteor
    16:03:40 meteor.1 | started with pid 89989
    16:03:40 meteor.1 | [[[[[ ~/workspace/python/src/meteor/front ]]]]]

    16:03:40 meteor.1 | => Started proxy.
    => Started your app.   Starting your app...


А если нажать Ctrl-C, то всем пошлется SIGINT и все должны будут завершиться.

Помимо этого, можно задать единые переменные окружения для всех процессов, для этого надо в этой же папке создать .env файл, куда перечислить все свои переменные окружения.

В целом, очень полезная утилита для разработчиков и хорошо показавшая себя в автоматизации ежедневной рутины
