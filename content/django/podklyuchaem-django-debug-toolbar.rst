Подключаем django-debug-toolbar
###############################
:date: 2009-08-19 12:43
:author: gigimon
:category: Django
:tags: debug, Django, Python
:slug: podklyuchaem-django-debug-toolbar

Очень полезным дополнением для Django является django-debug-toolbar.
Это своего рода отладочная панель, которая легко подключается, позволяет
просматривать множество данных (в том числе настройки, SQL запросы,
время выполнения, traceback). Приступим собственно к его установке :)

1. Установим собственно django-debug-toolbar. Можно из `git'a`_ или же
стабильную версию с помощью easy\_install

.. code-block:: python

    easy_install django-debug-toolbar

2. Добавляем в наш проект. В секцию MIDDLEWARE\_CLASSES добавим в конец
'debug\_toolbar.middleware.DebugToolbarMiddleware',

3. В settings.py добавим секцию INTERNAL\_IPS = ('127.0.0.1',) (если вы
работаете на локальной машине)

4. Добавим путь в TEMPLATE\_DIRS до папки с темплейтами
django-debug-toolbar. У меня в Gentoo этот путь
 '/usr/lib/python2.5/site-packages/django\_debug\_toolbar-0.7.0-py2.5.egg/debug\_toolbar/templates/',

5. Подключим к нашему проекту, в секции INSTALLED\_APPS  добавить
'debug\_toolbar',

6. После этого, можно опционально добавить секцию
DEBUG\_TOOLBAR\_PANELS, в которой задаются активные панели.

.. code-block:: python

    DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    )

Все, после этого, на каждой странице вверху, будет отображаться
тулбарчик с панелькой :)

P.S. панель отображается только если в темплейте есть открывающийся и
закрывающийся тег <body></body>

.. _git'a: git://github.com/robhudson/django-debug-toolbar.git

.. |Общий вид| image:: {filename}/images/2009/08/debug1-450x16.png
   :target: {filename}/images/2009/08/debug1.png
.. |Вид запросов| image:: {filename}/images/2009/08/debug2-450x152.png
   :target: {filename}/images/2009/08/debug2.png
