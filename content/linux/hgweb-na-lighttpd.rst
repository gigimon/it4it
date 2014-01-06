hgweb на lighttpd
#################
:date: 2010-05-14 10:20
:author: gigimon
:category: Python
:tags: dvcs, hg, hgweb, lighttpd, mercurial
:slug: hgweb-na-lighttpd

Опять давно ничего не писал :) А сегодня решил напомнить, что я жив и
рассказать, как поднять свой hg репозитарий с web мордой на веб-сервере
Lighttpd.

Предположим, что mercurial и Lighttpd у вас уже установлены, а
репозитарии hg будут храниться в /var/www. Т.к. hgweb мы будем запускать
через fastcgi (единственный возможный на lighttpd, не считая прокси), то
нам потребуется .fcgi скрипт, который будет создавать wsgi сервер с
сокетом. Т.к. у меня кучка django сайтов, то я сделал папку
/var/www/fcgi, в которой все их и храню :)

1. Создадим такую папку и положим в файл hgweb.fcgi такой код:

.. code-block:: python

    from mercurial import demandimport; demandimport.enable()

    import os
    os.environ["HGENCODING"] = "UTF-8"
    from mercurial.hgweb.hgwebdir_mod import hgwebdir
    from mercurial.hgweb.request import wsgiapplication
    from flup.server.fcgi import WSGIServer

    def make_web_app():
        return hgwebdir("hgweb.conf")

    def wsgiapplication2(app_maker):
        application = app_maker()
        def run_wsgi(env, respond):
            path = env['PATH_INFO'].replace('hgweb.fcgi/','')
            env['PATH_INFO'] = path
        return application(env, respond)
    return run_wsgi

    WSGIServer(wsgiapplication2(make_web_app)).run()

2. Тамже, положим файл hgweb.conf с конфигурацией нашего сервера:

.. code-block:: bash

    [paths]
    /repo_name = /path/to/repo
    [web]
    style = gitweb
    allow_archive = bz2 gz zip
    baseurl =

В секции [paths] определяются все репозитории, которые будут видны в
hgweb.

Baseurl - устанавливает префикс в url для доступа к репозитарию. В моем
случае, ссылка будет http://example.com/repo\_name.

3. Создадим репозиторий hg, либо склонируем его с локальнйо машины по
ssh :)

.. code-block:: bash

    cd /path/to/repo

    hg init

    cd /path/to/repo

    hg clone . ssh://login@example.com//path/to/repo

При клонировании по ssh, важно не забыть именно два слэша, после адреса.

4. Конфигурируем lighttpd.

Создаем новый конфиг, я назвал его 15-hgweb.conf, имя значения не имеет
впринципе :) Кладем в папочку и включаем:

.. code-block:: bash

    /etc/lighttpd/conf-available/

    ln -s /etc/lighttpd/conf-available/15-hgweb.conf /etc/lighttpd/conv-enabled/15-hgweb.conf

Содержимое файла 15-hgweb.conf:

.. code-block:: bash

    $HTTP["host"] == "hg.example.com" {

        server.document-root = ""
        server.errorlog = "/var/log/lighttpd/hgweb.error.log"
        accesslog.filename = "/var/log/lighttpd/hgweb.access.log"
        accesslog.format = "%h %l %u %f %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i""
        server.follow-symlink = "enable"

        url.rewrite-once = (
        "^/(.*)$" => "/hgweb.fcgi/$1",
        )
        fastcgi.server = (
            "/hgweb.fcgi" => (
            "main" => (
            "socket" => "/tmp/hgweb.socket",
            "check-local" => "disable",
            "bin-path" => "/path/to/hgweb.fcgi",
            "broken-scriptfilename" => "enable",
            "min-procs" => 1,
            "max-procs" => 1,
            )
         )
       )

        alias.url = (
           "/static" => "/usr/share/mercurial/templates/static",
        )

        $HTTP["querystring"] =~ "cmd=unbundle"  {
           auth.backend = "htpasswd"
           auth.backend.htpasswd.userfile = "/path/to/passwd"
           auth.require = (   "" => (
                  "method"  => "basic",
                  "realm"   => "gigimon Repo",
                  "require" => "valid-user"
            )
           )
        }
    }

Последняя секция с авторизацией нужна для возможности делать push в
репозитории. Если хотите сделать его публичным дял просомтра, либо
убрать возможность пуша, то можете ее полностью убрать.

Также, для пуша требуется, чтобы в lighttpd был настроен SSL, в
дефолтной поставке дебиана такое есть. Проверить можно в
/etc/lighttpd/lighttpd.conf , обычно в самом низу:

.. code-block:: bash

    $SERVER["socket"] == ":443" {
        ssl.engine = "enable"
        ssl.pemfile = "/etc/lighttpd/lighttpd.pem"
    }

Файл с паролями, который указывается в auth.backend.htpasswd.userfile,
создается командой htpasswd входящей в apache2-utils

5. Теперь, если хотим разрешить пуш некоторым лицам, нам требуется
настроить сам репозиторий через файл hgrc

.. code-block:: bash

    cat /path/to/repo/.hg/hgrc

    [web]
    allow_push = user1, user2
    description = "example.com development"

Также, помимо разрешения, в этом файле задаются многие параметры для
репозитория. Я использую авто апдейт кода при пуше в него, через строку:

.. code-block:: bash

    [hooks]
    changegroup.upd = hg update

После перезагрузки lighttpd

.. code-block:: bash

    /etc/init.d/lighttpd restart

По вашему адресу, должен будет появиться и работать hgweb, надеюсь у вас
он появился :)
