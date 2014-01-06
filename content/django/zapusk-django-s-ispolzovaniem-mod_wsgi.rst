Запуск Django с использованием mod_wsgi
#######################################
:date: 2009-02-24 01:03
:author: gigimon
:category: Django
:tags: apache, Django, wsgi
:slug: zapusk-django-s-ispolzovaniem-mod_wsgi

После недавнего окончания разработки первого своего сайта на Django,
пришло время его выставлять в свет :) Для этого на VPS, где крутился
Apache2, был установлен mod\_wsgi. Чтобы заставить работать Django сайт
с mod\_wsgi, надо лишь немного поправить конфиг Apache для вашего
виртуального хоста, и написать небольшой скрипт.  В моем примере, сайт
будет лежать в /var/www/domain.net/www/ . Такая вложенность получилась
не просто так,  при попытке запуска сайта из /var/www/domain.net, я
ловил ошибку о ненахождении модулей :(

Первое что сделаем, изменим запись о хосте. Открываем файл, где
прописаны настройки виртуального хоста и добавляем:

.. code-block:: bash

    ServerAdmin aliens@it4it.ru
    ServerName domain.net
    ServerAlias www.domain.net
    DocumentRoot /var/www/domain.net/www
    CustomLog /var/log/apache2/domainl-access.log combined
    ErrorLog /var/log/apache2/domain-error.log

    #вот этой стрчокой прописываем алиас до вашей статики в виде: /урл_статики /папка_статики

    Alias /static/ /var/www/domain.net/www/media/
    #настройки wsgi, от чьего имени запускать и количество запросов и потоков
    WSGIProcessGroup aliens
    WSGIDaemonProcess aliens user=aliens group=www-data threads=2 maximum-requests=1000

    #путь до скрипта, который будет запускать наш джанго проект

    WSGIScriptAlias / /var/www/domain.net/www/django.wsgi

    #алиас до статики для админки

    Alias "/media/" "/var/lib/python-support/python2.5/django/contrib/admin/media/"

            SetHandler None
        

        
            Order deny,allow
            Allow from all

После этого, создаем и редактируем
файл /var/www/domain.net/www/django.wsgi с таким содержимым:

.. code-block:: python

    import sys
    import os
    import os.path

    sys.path.insert(0, os.path.dirname(__file__))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

    from django.core.handlers.wsgi import WSGIHandler
    application = WSGIHandler()

Все, после этого проверить права на файлы, и можно перезапускать Apache
и проверять работоспособность сайта.

Хочу предупредить, после любого изменения файлов сайта, надо
перезагрузить Apache
