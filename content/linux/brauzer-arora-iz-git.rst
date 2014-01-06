Браузер Arora - из GIT
######################
:date: 2008-09-23 20:13
:author: gigimon
:category: \*nix
:tags: acid3, arora, qt4, webkit
:slug: brauzer-arora-iz-git

Решил недавно поискать браузеры использующие движок Webkit, и написаные
на Qt4. В итоге, нашел лишь один мультиплатформенный браузер `Arora`_. В
настоящее время он имеет версию 0.3, и разрабатывается 0.4. Умеет он
пока что мало:

-  Табы
-  Закладки
-  История посещеных сайтов
-  Автоматическое дополнение запросов в строку поиска google из истории
-  Качалка файлов
-  Режим приватности (не записываются логи)

Но, хоть версия и мала, браузер достаточно стабильно работает и быстро
(благо WebKit из SVN, а Qt4.4).

Хочу рассказать, как обновить его до актуального состояния, т.е. собрать
из GIT ;)

Для этого нам требуется в системе установленое Qt4.4 и Qt4-webkit (его я
поставил для удовлетворения зависимостей, и для других приложений).
После этого:

1. Скачиваем исходные коды с помощью команды

.. code-block:: bash

   git clone git://github.com/Arora/arora.git

2.  Теперь надо взять последнюю версию WebKit:

.. code-block:: bash

   svn checkout http://svn.webkit.org/repository/webkit/trunk WebKit

3. Собираем WebKit

.. code-block:: bash

   cd WebKit
   ./WebKitTools/Scripts/build-webkit --qt --release

4. Настраиваем переменные окружения, для сборки Arora с последним
WebKit:

.. code-block:: bash

   cd /path/to/arora/source
   export QT\_WEBKIT=webkit\_trunk
   export WEBKITDIR=/pat/to/webkit/source

5. Собираем Arora:

.. code-block:: bash

   qmake "CONFIG-=debug" -r
   make clean
   make

Впринципе, пункты 2,3,4 можно пропустить, но тогда будет использована
слишком старая версия WebKit. Для сравнения производительности, приведу
цифры, сравнивая с Opera 9.60 Beta1 build 2424.

**Тест Acid3:**

Opera 9.60 Beta1 build 2424  - 85/100

Arora с Qt4-webkit из репозитария - 41/100

Arora с WebKit из SVN - 96/100

**Тест `SunSpide`_\ r (цифры за весь тест):**

Opera 9.60 Beta1 build 2424 - 14035.8ms +/- 4.3%

Arora с Qt4-webkit из репозитария - 24818.0ms +/- 5.2%

Arora с WebKit из SVN - 4695.4ms +/- 10.0%

Как не трудно догадаться, советую WebKit обновлять ;)

.. _Arora: http://code.google.com/p/arora/
.. _SunSpide: http://www2.webkit.org/perf/sunspider-0.9/
