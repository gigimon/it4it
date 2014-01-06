Установка Xen в CentOS
######################
:date: 2009-09-23 23:51
:author: gigimon
:category: \*nix
:tags: centos, xen, виртуализация
:slug: ustanovka-xen-v-centos

Недавно начал пробовать систему виртуализации Xen. После быстрого чтения
мануалов, смог установить виртуальную машину с Debian, что говорит о
достаточно простой конфигурации (для начальных нужд). Итак, в качестве
хостовой машины (dom0) будет использоваться CentOS 5.2, запущенный на
компьютере с поддержкой аппаратной виртуализации (AMD-V или Intel-VT).
Поддержка аппаратной виртуализации нужна, если вы собираетесь запускать
Windows.

Первое что необходимо, установить ядро с поддержкой Xen. В стандартных
репозитариях CentOS есть такое ядро, kernel-xen версии 2.6.18-164 с Xen
3.0

.. code-block:: bash

    yum install kernel-xen

После установки, в /boot появится ядро vmlinuz-2.6.18-164.el5xen. Теперь
надо загрузиться с ним. Можео либо вручную его выбрать при загрузке
grub, либо отредактировать файл /boot/grub/menu.lst и параметр default
сделать равным 0 (по-умолчанию, kernel-xen автоматчиески прописывает
себя первым ядром в меню grub).

После загрузки с ядром Xen'а, работу его можно проверить наличием
интерфейсов xenbr и vif в выводе ifconfig:

.. code-block:: bash

    [root@gigi ~]# ifconfig
    peth1     Link encap:Ethernet  HWaddr FE:FF:FF:FF:FF:FF
    inet6 addr: fe80::fcff:ffff:feff:ffff/64 Scope:Link
    UP BROADCAST RUNNING NOARP  MTU:1500  Metric:1
    RX packets:1484845567 errors:0 dropped:848 overruns:0 frame:0
    TX packets:21318806 errors:0 dropped:0 overruns:0 carrier:0
    collisions:0 txqueuelen:1000
    RX bytes:107304750948 (99.9 GiB)  TX bytes:1495739489 (1.3 GiB)
    Memory:dc080000-dc0a0000

    vifxenv0  Link encap:Ethernet  HWaddr FE:FF:FF:FF:FF:FF
    inet6 addr: fe80::fcff:ffff:feff:ffff/64 Scope:Link
    UP BROADCAST RUNNING NOARP  MTU:1500  Metric:1
    RX packets:17643569 errors:0 dropped:0 overruns:0 frame:0
    TX packets:1467766901 errors:0 dropped:390908 overruns:0 carrier:0
    collisions:0 txqueuelen:32
    RX bytes:863953497 (823.9 MiB)  TX bytes:100008573528 (93.1 GiB)

    vif0.1    Link encap:Ethernet  HWaddr FE:FF:FF:FF:FF:FF
    inet6 addr: fe80::fcff:ffff:feff:ffff/64 Scope:Link
    UP BROADCAST RUNNING NOARP  MTU:1500  Metric:1
    RX packets:3588998 errors:0 dropped:0 overruns:0 frame:0
    TX packets:1483233162 errors:0 dropped:0 overruns:0 carrier:0
    collisions:0 txqueuelen:0
    RX bytes:370499902 (353.3 MiB)  TX bytes:107193417651 (99.8 GiB)

    xenbr1    Link encap:Ethernet  HWaddr FE:FF:FF:FF:FF:FF
    UP BROADCAST RUNNING NOARP  MTU:1500  Metric:1
    RX packets:3930114 errors:0 dropped:0 overruns:0 frame:0
    TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
    collisions:0 txqueuelen:0
    RX bytes:2361888673 (2.1 GiB)  TX bytes:0 (0.0 b)

А также, посмотреть вывод команды xm list, он должен выглядеть примерно
так:

.. code-block:: bash

    [root@gigi ~]# xm list
    Name                                      ID Mem(MiB) VCPUs State   Time(s)
    Domain-0                                   0      512     4 r-----  45273.0

Запись Domain-0 обозначает, что запущена машина с dom0 (наша хостовая)
 и значит, все работает :)

Из известных проблем, следует упомянуть, не используйте сетевые карты
Realtek на чипсетах 8169 и ему подобном, т.к. при использовании такой
сетевой карты, не сохраняются сетевые параметры (не применяются при
создании моста xenbr), а также MAC адрес становится FF:FF:FF:FF:FF:FF

В следующей заметке (очень скоро) расскажу про создание Linux и Windows
виртуальных машин.

Ссылки:

Официальный `сайт`_

Официальная `документация`_

`Документация xen`_ на русском

.. _сайт: http://www.xen.org/
.. _документация: http://tx.downloads.xensource.com/downloads/docs/user
.. _Документация xen: http://xgu.ru/wiki/Xen
