Подключение VPN с помощью pptp
##############################
:date: 2008-11-13 01:59
:author: gigimon
:category: \*nix
:tags: linux, ppp, pptp, vpn, интернет, провайдер
:slug: podklyuchenie-vpn-s-pomoshhyu-pptp

Недавно потребовалось подключиться к провайдеру с помощью VPN соединения
с Linux машины. Как всем известно, кроме как использовать пакет PPTP
способов подключиться нет.

Итак, устанавливаем пакет PPTP

Для Debian:

.. code-block:: bash
   
   apt-get install pptp

Он автоматчиески вытянет все нужные зависимости. После этого надо
настроить конфиг соединения:

#. Идем в папку /etc/ppp/peers
#. Создаем файл с любым названием, у меня sevstar (название првоайдера ;)
#. Вносим туда настройки для него:

.. code-block:: bash

    lock
    noauth

    #не используем компресию и шифрование

    nobsdcomp
    nodeflate
    refuse-eap
    refuse-pap
    refuse-chap
    nomppe

    #максимальное число попыток установления связи, если 0 - будут попытки пока не подключимя

    maxfail 0
    #использовать как шлюз по умолчанию
    defaultroute

    #установки MTU и MRU
    mru 1500
    mtu 1500

    persist

4. Открываем файл /etc/ppp/chap-secrets и добавляем туда логин и пароль
в таком виде:

.. code-block:: bash

    login  PPTP password *     

    Собственно все. После этого, запускаем командой

    pppd call sev2 pty "pptp 10.10.0.1 --nolaunchpppd"

И контроллируем, чтобы появился интерфейс ppp0
