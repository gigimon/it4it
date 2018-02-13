Установка home-assistant и подключение Xiaomi датчиков
------------------------------------------------------
:date: 2017-01-16 21:50
:author: gigimon
:category: homeassistant
:tags: xiaomi, home-assistant, iot, smart home, умный дом
:slug: home-assistant-1


Последние пару лет тема домашней автоматизации и internet of things (iot) стала очень популярной, из-за чего появилось куча как программных продуктов, таких как home-assistant, majordomo и т.п., так и аппаратных решений от различных производителей (xiaomi, apple с homekit, решения от мегафона, lg). Я для себя выбрал home-assistant + xiaomi для внутренних датчиков и самодельных в будущем. В этой статье установим home-assistant на linux машину, а также добавим в него отображение информации с xiaomi gateway + температурные датчики с настройкой внешнего вида дашборда


*************
0. Подготовка
*************

Для начала определим, что нам необходимо. Из аппаратного обеспечения:

1. Компьютер на linux
2. `Xiaomi gateway 2<http://www.mi.com/wangguan/?cfrom=list>`_
3. Подключенные датчики темепратуры к xiaomi gateway и MiHome, у меня `такие <https://youpin.mi.com/detail?gid=731>`_
   

***************************
1. Установка home-assistant
***************************

Установить home-assistant можно разными способами:

- системный пакет для вашего дистрибутива
- установка через pip
- установка через docker. Как установить docker на ваш linux читать `тут <https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-using-the-convenience-script>`_
  
Я выбрал установку через docker, т.к. это самый простой и быстрый способ установки.

Первое, что необходимо сделать, это создать папку на локальном диске, которая будет бэкапиться или которую вы не удалите, для того, чтобы хранить конфиги home-assistant и не потерять их, при работе с контейнером docker.


.. code-block:: bash

  mkdir /ваш/путь/homeassistant


Затем запускаем контейнер с последней версией home-assistant

.. code-block:: python

  docker run -d --name="home-assistant" -v /ваш/путь/homeassistant/config:/config -v /etc/localtime:/etc/localtime:ro --net=host homeassistant/home-assistant


Эта команда скачает образ для docker и запустит контейнер, пердав ему нашу папку с будущим конфигом (на хосте в папке /ваш/путь/), а также подключит веб интерфейс home-assistant на основной адрес сервера, на порт 8123. Чтобы проверить доступность home-assistant, необходимо в браузере зайти на адрес **http://адрес_сервера:8123** и увидете интерфейс home-assistant. По умолчанию home-assistant включает авто определение устройств в сети, поэтому на первой странице home-assistant вы возможно увидете какие-то устройства.


*********************************************
2. Добавление xiaomi gateway в home-assistant
*********************************************

Добавление устройств (датчиков) в home-assistant проводится через редактирование конфигурационного файла. Если посмотреть в папку 

.. code-block:: bash

    ls -la /ваш/путь/homeassistant/config/*.yaml

    /ваш/путь/homeassistant/config/automations.yaml
    /ваш/путь/homeassistant/config/configuration.yaml
    /ваш/путь/homeassistant/config/customize_glob.yaml
    /ваш/путь/homeassistant/config/customize.yaml
    /ваш/путь/homeassistant/config/groups.yaml
    /ваш/путь/homeassistant/config/scripts.yaml
    /ваш/путь/homeassistant/config/secrets.yaml

то можно увидеть различные конфиги:

1. automations.yaml - конфигурация для скриптов автоматизации
2. configuration.yaml - главный файл, в котором подключаются все остальные
3. customize_glob.yaml - настройка внешнего вида для категорий датчиков
4. customize.yaml - настройка внешнего вида отдельных датчиков
5. groups.yaml - настройка зон (комнат)
6. scripts.yaml - скрипты
7. secrets.yaml - файл для хранения секретных данных (паролей)
   
Для упрощения, добавим наш датчик в основной конфигурационный файл configuration.yaml, в конец файла

.. code-block:: bash

    xiaomi_aqara:
        discovery_retry: 5
        gateways:
            - key: <your_key>

Где вместо <your_key> необходимо добавить ваш отключ доступа к шлюзу. Взять его можно через MiHome:
1. В MiHome нажать на шлюз
2. Затем ... и выбрать пункт About
3. Нажать на версию (подержать), которая снизу, появится 2 дополнительных пункта
4. Нажать на пункт "local area network communication protocol" и в открывшемся окне необходимр включить "local area network communication protocol" и сохранить поле "password", это и будет ключ, который надо вставить в конфиг
   
Затем, надо перезагрузить home-assistant, чтобы он прочитал новый конфиг, сделать это можно либо через docker (docker stop container_id && docker start container_id), либо через меню home-assistant Settings -> Common -> Restart
