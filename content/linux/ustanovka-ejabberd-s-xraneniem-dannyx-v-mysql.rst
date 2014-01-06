Установка ejabberd с хранением данных в MySQL
#############################################
:date: 2009-02-06 20:47
:author: gigimon
:category: \*nix
:tags: ejabberd, jabber, mysql, nix
:slug: ustanovka-ejabberd-s-xraneniem-dannyx-v-mysql

Установка jabber сервера на свой сервер достаточно проста и производится
минут за 20 :)

 Итак приступим:

Для начала устновим ejabberd

.. code-block:: bash

    apt-get install ejabberd

Затем идем редактировать конфиг

.. code-block:: bash

    cd /etc/ejabberd

    nano ejabberd.cfg

Редактируем строку admin:

.. code-block:: bash

    %% Admin user
    {acl, admin, {user, "admin_nick", "host_server"}}.

где, admin\_nick ник  того, кто может управлять серверов через веб и
другими средствами, host\_server - это сервер, которым он может
управлять

Потом меняем host:

.. code-block:: bash

    %% Hostname
    {hosts, ["yourhost"]}.

yourhost - ваш домен, где будет висеть жаббер сервер

Далее в секции listen, устанавливаем так:

.. code-block:: bash

    {5222, ejabberd_c2s, [
    {access, c2s},
    {shaper, c2s_shaper},
    {max_stanza_size, 65536},
    starttls, {certfile, "path_to_cert"}
    ]},

    %%
    %% To enable the old SSL connection method (deprecated) in port 5223:
    %%
    {5223, ejabberd_c2s, [
    {access, c2s},
    {shaper, c2s_shaper},
    {max_stanza_size, 65536},
    tls, {certfile, "path_to_cert"}
    ]},

    {5269, ejabberd_s2s_in, [
    {shaper, s2s_shaper},
    {max_stanza_size, 131072}
    ]},
    {5280, ejabberd_http, [
    http_poll,
    web_admin
    ]}

Для регистрации через клиент, надо изменить в секции ACCESS RULES:

.. code-block:: bash

    {access, register, [{deny, all}]}.  на {access, register, [{allow, all}]}.

Для активации прослушивания портов и поддержки ssl соединений, а также
серверов со старым SSL.

.. code-block:: bash

    {s2s_certfile, "path_to_cert"}.

path\_to\_cert - путь к сертификату 9который сделаем чуть ниже)

Дальше включаем режим аутентификации через БД

.. code-block:: bash

    {auth_method, odbc}.

В секции DATABASE SETUP раскомментируем секцию для базы которую будем
использовать (MySQL, PG и др), а также устаналиваем параметры соединения

.. code-block:: bash

    {odbc_server, {mysql, "server", 1234, "database", "username", "password"}}.

В секции modules заменяем

.. code-block:: bash

    {mod_last,     []},  на  {mod_last_odbc,     []},

    {mod_offline,  []}, на  {mod_offline_odbc,  []},

    {mod_roster,   []}, на {mod_roster_odbc,   []},

    {mod_vcard,     []}, на {mod_vcard_odbc,    [{search, true},
    {matches, infinity},
    {allow_return_all, true}]},

В mod\_register можете поменять текст сообщения, которое будет
присылается новому зарегистрированному пользователю.

После этого, установим базу данных ejabberd. для MySQL базу берем `тут`_

Импортируем ее любым доступным для вас способом, через phpmyadmin или
ручками, или еще как:

.. code-block:: bash

    mysql -D ejabberd -p -u ejabberd  < mysql.sql

Для дебиана, надо установить клиент к БД. пакет можно взять `здесь`_

Теперь сгенерируем сертификат для работы сервера:

.. code-block:: bash

    cd /etc/ejabberd/

    openssl rsa -in ssl.key -out ssl.key

    cat ssl.crt ssl.key sub.class1.xmpp.ca.crt >ejabberd.pem

    chown ejabberd.ejabberd ejabberd.pem
    chmod 400 ejabberd.pem

После этого можно запускать сервер:

.. code-block:: bash

    /etc/init.d/ejabberd start

Добавить первого пользователя можно через ejabberdctl:

.. code-block:: bash

    Первого пользователя зарегистрируйте админа :)
    Также, есть небольшая админка по адресу http://ваш_зост:5280/admin
    Куда надо ввести jid админа и его пароль, чтобы войти.
    Еще, иногда требуется добавить SRV поля для вашего домена в ДНС сервер:

    _jabber._tcp IN SRV 0 0 5269 ваш_домен_с_жаббером.
    _xmpp-server._tcp IN SRV 0 0 5269 ваш_домен_с_жаббером.
    _xmpp-client._tcp IN SRV 0 0 5222 ваш_домен_с_жаббером.

Все, после этого все должно работать :)

.. _тут: http://svn.process-one.net/ejabberd/trunk/src/odbc/mysql.sql
.. _здесь: http://blog.jwchat.org/download/ejabberd-mysql-20090114_1-2_all.deb
