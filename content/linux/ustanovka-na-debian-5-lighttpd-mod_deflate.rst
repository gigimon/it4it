Установка на Debian 5 - lighttpd + mod_deflate
##############################################
:date: 2009-10-06 23:41
:author: gigimon
:category: \*nix
:tags: apache, bzip, lighttpd, web, веб сервер, сжатие
:slug: ustanovka-na-debian-5-lighttpd-mod_deflate

После переезда с 1 хостера к другому, решил сменить apache2 на Lighttpd.
Т.к. VPS мой на Debian 5 и там есть только Lighttpd версии 1.4.19, в
которой нету такого нужного модуля, как mod\_deflate, для сжатия
передаваемых данных. Данный модуль появился только с версии 1.5, в 1.4
есть лишь mod\_compress, который умеет только статчиеские файлы сжимать.
К счастью, патч, реализующий mod\_deflate,  доступен практически ко всей
ветке 1.4. В этой статье рассмотрим, как доабвить mod\_deflate модуль.

Для начала, установим пакет build-essential для сборки lighttpd в .deb
пакет

.. code-block:: bash

    apt-get install build-essential

Затем надо скачать сорцы lighttpd и патча:

.. code-block:: bash

    cd /usr/src
    apt-get source lighttpd

    wget http://redmine.lighttpd.net/attachments/download/632/lighttpd-1.4.19.mod_deflate.patch

Патчим:

.. code-block:: bash

    cd lighttpd-1.4.19
    patch -p1 < ../lighttpd-1.4.19.mod_deflate.patch

Теперь соберем в .deb пакет:

.. code-block:: bash

    dpkg-buildpackage

После выполнения команды, у вас наверняка появится ошибка подобно этой:

.. code-block:: bash

    dpkg-checkbuilddeps: Unmet build dependencies: debhelper (>= 5.0.0) cdbs libssl-dev zlib1g-dev libbz2-dev libattr1-dev libpcre3-dev libmysqlclient15-dev libldap2-dev libfcgi-dev libgdbm-dev libmemcache-dev liblua5.1-0-dev dpatch patchutils pkg-config uuid-dev libsqlite3-dev libxml2-dev

Это означает, что нехватает этих пакетов для сборки. Надо их установить:

.. code-block:: bash

    apt-get install  cdbs libssl-dev zlib1g-dev libbz2-dev libattr1-dev libpcre3-dev

После их установки, еще раз выполняем команду

.. code-block:: bash

    build-essential

Если по окончанию программы никаких ошибок не выявится, вы должны будете
увидеть в папке на 1 уровень выше множество .deb пакет (примерно такого
вида)

.. code-block:: bash

    cd ..
    ls -l
    rwxr-xr-x 8 root root   4096 2007-08-08 19:09 lighttpd-1.4.19
    -rw-r--r-- 1 root src     861 2007-08-08 19:07 lighttpd_1.4.19-5.dsc
    -rw-r--r-- 1 root src    2000 2007-08-08 19:12 lighttpd_1.4.19-5e_amd64.changes
    -rw-r--r-- 1 root src  287998 2007-08-08 19:12 lighttpd_1.4.19-5_amd64.deb

Теперь установим Lighttpd:

.. code-block:: bash

    dpkg -i lighttpd_1.4.19-5_amd64.deb

Теперь скопируем сам модуль mod\_deflate, в папку модулей Lighttpd (патч
не патчит make файл, поэтому надо ручками)

.. code-block:: bash

    cp /usr/src/lighttpd-1.4.19/debian/tmp/usr/lib/lighttpd/mod_deflate.so /usr/lib/lighttpd

Проверим, установился ли модуль и видит его lighttpd:

.. code-block:: bash

    lighttpd -V
    lighttpd-1.4.19 (ssl) - a light and fast webserver
    Build-Date: Oct  5 2009 01:35:25

    Event Handlers:

    + select (generic)
    + poll (Unix)
    + rt-signals (Linux 2.4+)
    + epoll (Linux 2.6)
    - /dev/poll (Solaris)
    - kqueue (FreeBSD)

    Network handler:

    + sendfile

    Features:

    + IPv6 support
    + zlib support
    + bzip2 support
    + crypt support
    + SSL Support
    + PCRE support
    + mySQL support
    + LDAP support
    + memcached support
    + FAM support
    + LUA support
    + xml support
    + SQLite support
    + GDBM support

Следует обратить внимание на наличие строки bzip2, если она
присутствует, то mod\_deflate установился.

После этих манипуляций, надо настроить сам модуль. Для этого создаем
конфиг и впишем в него нужные опции (они будут действовать для всех
хостов) и включим:

.. code-block:: bash

    nano -w /etc/lighttpd/conf-available/10-deflate.conf

    #включением

    deflate.enabled = "enable"

    #степень компрессии

    deflate.compression-level = 9
    deflate.mem-level = 9
    deflate.window-size = 15
    deflate.bzip2 = "enable"
    deflate.min-compress-size = 200
    deflate.output-buffer-size = 4096
    deflate.work-block-size = 512

    #типы файлов, которые сжимать

    deflate.mimetypes = ("text/html", "text/plain", "text/css", "text/javascript", "text/xml")

    ln -s /etc/lighttpd/conf-available/10-deflate.conf /etc/lighttpd/conf-enabled/10-deflate.conf

После этого рестартим Lighttpd и проверяем с помощью Opera DragonFly или
FF FireBug (ну или чем вам удобно смотреть HTTP заголовки) на предмет
сжатия.

.. code-block:: bash

    /etc/init.d/lighttpd restart

Все, после этого должно все работать :) Надеюсь это вам помогло
