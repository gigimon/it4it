Защита ssh от ботов с помощью sshguard
######################################
:date: 2008-11-17 19:30
:author: gigimon
:category: \*nix
:slug: zashhita-ssh-ot-botov-s-pomoshhyu-sshguard

После установки сервера и вывешивании его в интернет, практически
мгновенно на порт ssh (tcp-22) стали ломиться боты, пытаясь подобрать
юзера и пароль. Это подтверждают такие строчки в логах auth.log:

.. code-block:: bash

    Nov 16 09:34:27 solaria sshd[3343]: Failed password for root from 221.132.118.11 port 43083 ssh2
    Nov 16 09:34:29 solaria sshd[3345]: reverse mapping checking getaddrinfo for tw118-static11.tw1.com failed - POSSIBLE BREAK-IN ATTEMPT!
    Nov 16 09:34:29 solaria sshd[3345]: (pam_unix) authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=221.132.118.11  user=root
    Nov 16 09:34:31 solaria sshd[3345]: Failed password for root from 221.132.118.11 port 43354 ssh2
    Nov 16 09:34:34 solaria sshd[3347]: reverse mapping checking getaddrinfo for tw118-static11.tw1.com failed - POSSIBLE BREAK-IN ATTEMPT!
    Nov 16 09:34:34 solaria sshd[3347]: (pam_unix) authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=221.132.118.11  user=root
    Nov 16 09:34:37 solaria sshd[3347]: Failed password for root from 221.132.118.11 port 43623 ssh2
    Nov 16 09:34:38 solaria sshd[3349]: reverse mapping checking getaddrinfo for tw118-static11.tw1.com failed - POSSIBLE BREAK-IN ATTEMPT!
    Nov 16 09:34:38 solaria sshd[3349]: (pam_unix) authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=221.132.118.11  user=root
    Решил поставить пакет sshguard, который банит по IP адресу, с помощью iptables ботов пытающихся подобрать пароль (если больше n попыток за m секунд).

Итак, приступим к установке. Для начала установим пакет sshguard из
репозитария, либо скачаем с официального сайта и скомпилируем. После
этого надо: 1. Добавить правила в начало iptables:

.. code-block:: bash

    iptables -N sshguard
    iptables -A INPUT -p tcp --dport 22 -j sshguard

2. Сделать так, чтобы sshguard читал логи об авторизацци на 22 порт:

.. code-block:: bash

    tail -n0 -F /var/log/auth.log | /usr/sbin/sshguard;

И добавим это правило в автозагрузку 3. Дать права рута sshguard, чтобы
он мог динамически менять правила iptables:

.. code-block:: bash

    chmod +s /usr/sbin/sshguard

После этого, в списке процессов должен появится sshguard

.. code-block:: bash

    root      2299  0.0  0.6   9984   784 ?        Sl   Nov15   0:00 /usr/sbin/sshguard

Теперь, в конфиге можем видет ьследующее:

.. code-block:: bash

    Nov 17 10:35:12 solaria sshd[4614]: Invalid user aaron from 221.130.184.137
    Nov 17 10:35:12 solaria sshd[4614]: (pam_unix) check pass; user unknown
    Nov 17 10:35:12 solaria sshd[4614]: (pam_unix) authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=221.130.184.137
    Nov 17 10:35:12 solaria sshguard[2299]: Matched IP address 221.130.184.137
    Nov 17 10:35:12 solaria sshguard[2299]: Blocking 221.130.184.137: 4 failures over 23 seconds.
    Nov 17 10:35:12 solaria sshguard[2299]: Setting environment: SSHG_ADDR=221.130.184.137;SSHG_ADDRKIND=4;SSHG_SERVICE=10.
    Nov 17 10:35:12 solaria sshguard[2299]: Run command "case $SSHG_ADDRKIND in 4) exec /sbin/iptables -A sshguard -s $SSHG_ADDR -j DROP ;; 6) exec /sbin/ip6tables -A sshguard -s $SSHG_ADDR -j DROP ;; *) exit -2 ;; esac": exited 0.

Вот и все ;)
