Двойная загрузка виртуальных машин VMWare под Linux. Часть 1.
#############################################################
:date: 2009-04-13 15:18
:author: Goletsa
:category: \*nix
:tags: debian, linux, vmware, виртуализация
:slug: dualboot-vmware-vm-linux-part-1

В нынешнем IT сообществе все чаще звучит слово "виртуализация". Как
крупные компании типа Microsoft, так и небольшие представили свои
решения по работе с виртуальными компьютерами. Одним из таких решений
является линейка программ от компании VMWare. Среди интересных
возможностей этих продуктов нельзя не отметить возможность работать
напрямую с жестким диском вашего компьютера в виртуальной среде, что
может использоваться, к примеру, для запуска второй операционной системы
с вашего компьютера.

Все дальнейшее относится к Debian 5.0 "Lenny"

Но, так как большинство дистрибутивов вполне похоже, то это должно
подходить как к потомкам Debian (Ubuntu, Runtu , Mephis), так и к другим
(типа Gentoo, Fedora). Вопросы установки на физический диск, равно и как
вопрос установки самих ОС оставим на усмотрение читателя. Это в принципе
не представляет сложности и доступно пользователю. К тому же все
современные дистрибутивы уже обзавелись красивыми графическими
установщиками, которые еще сильнее упрощают жизнь неподготовленным
пользователям.

После установки ОС следует поставить некоторые пакеты, улучшающие
производительность при запуске в виртуализированной среде VMWare. Нам
требуются open-vm-tools, open-vm-source, open-vm-toolbox . Последнее
ставим только если вам нужна графическая утилита для управления гостевой
ОС.

.. code-block:: bash

    aptitude install open-vm-tools open-vm-source

В комплекте с этими утилитами есть небольшая программа , которая
проверяет, запущена ли ОС внутри VMWARE или на реальном железе. Например
ее вывод может быть таким:

.. code-block:: bash

    vmware-checkvm

VMware software version 6 (good)

Но при попытке запуска самих утилит ловим ошибку:

.. code-block:: bash

    /etc/init.d/open-vm-tools start

    Loading open-vm-tools modules: vmhgfsFATAL: Module vmhgfs not found.

    vmmemctlFATAL: Module vmmemctl not found.

    vmsyncFATAL: Module vmsync not found.

    .
    Starting open-vm guest daemon: vmware-guestd.


Чтобы собрать модули ядра, необходимые для работы, требуется поставить
пакет module-assistant .

.. code-block:: bash

    aptitude install module-assistant

И соберем с помощью него необходимые модули ядра:

.. code-block:: bash

    m-a a-i open-vm

На вопросы о установке необходимых пакетов, отвечаем утвердительно "Y"

Перезапустим демон утилит и порадуемся загруженным модулям:

.. code-block:: bash

    /etc/init.d/open-vm-tools restart

    Stopping open-vm guest daemon: vmware-guestd.
    Removing open-vm-tools modules: vmhgfs vmmemctl vmsync.
    Loading open-vm-tools modules: vmhgfs vmmemctl vmsync.
    Starting open-vm guest daemon: vmware-guestd.

Теперь у нас настроены основные драйвера для гостевой OS.

При просмотре стартового скрипта VM Tools видно, что перед запуском
драйверов и утилит от VMWARE идет проверка запущено ли все на реальном
или виртуальном железе. Соответственно при запуске вне виртуальной
машины (при нормальном запуске) скрипты не отработают и не будут мешать
нормальной работе.

Остается проблема смены имени сетевого интерфейса, которая решается
небольшой правкой конфигурационых файлов демона udev.

Для начала следует узнать мак адреса сетевых карт (реальной и
виртуальной) с помощью ifconfig (или другим удобным вам способом).

.. code-block:: bash

    ifconfig
    eth0 Link encap:Ethernet HWaddr 00:0c:29:40:10:d5
    inet addr:192.168.136.128 Bcast:192.168.136.255 Mask:255.255.255.0
    inet6 addr: fe80::20c:29ff:fe40:10d5/64 Scope:Link
    UP BROADCAST RUNNING MULTICAST MTU:1500 Metric:1
    RX packets:26188 errors:0 dropped:0 overruns:0 frame:0
    TX packets:12926 errors:0 dropped:0 overruns:0 carrier:0
    collisions:0 txqueuelen:1000
    RX bytes:34105677 (32.5 MiB) TX bytes:1144113 (1.0 MiB)
    Interrupt:19 Base address:0x2000

В данном случае имя интерфейса eth0 и он имеет MAC адрес
00:0c:29:40:10:d5.
При запуске в другом окружении естественно адрес будет другим ( и имя
интерфейса тоже). После того как мы получили список нужных нам адресов самое время
заглянуть в папку /etc/udev/rules.d/ :

.. code-block:: bash

    ls /etc/udev/rules.d/
    50-udev.rules 75-cd-aliases-generator.rules
    60-persistent-input.rules 75-persistent-net-generator.rules
    60-persistent-storage.rules 80-drivers.rules
    60-persistent-storage-tape.rules 91-permissions.rules
    60-persistent-v4l.rules 95-late.rules
    70-persistent-cd.rules z60_xserver-xorg-input-wacom.rules
    70-persistent-net.rules

Самое интересное для нас хранится в файле 70-persistent-net.rules.
Это строки вида:

.. code-block:: bash

    SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="00:0c:29:40:10:d5", ATTR{type}=="1", KERNEL=="eth*", NAME="eth0"

Соответственно указав две строки с одинаковыми именами интерфейсов и
разными MAC адресами, соответвующие определеным устройствам вашей
реальнойвиртуальной сети мы вне зависимости от того как запущена ОС
будет получать одни и теже адреса. Трудности могут возникнуть в связи с
тем что в правилах в файле 75-persistent-net-generator.rules зачемто
указано игнорировать интерфейсы VMWARE. Это можно обойти двумя методами
на мой взгляд:

1. Комментирование строки ENV{MATCHADDR}=="00:0c:29:\*\|00:50:56:\*",
ENV{MATCHADDR}="" чтобы для виртуальных карт создавались правила (
обычно этого не происходит).
2. Изменение в конфигурационном файле \*.vmx к примеру строк с

.. code-block:: bash

    ethernet0.addressType = "generated"
    ethernet0.generatedAddress = "00:0c:29:ee:30:5a"
    ethernet0.generatedAddressOffset = "0"

на

.. code-block:: bash

    ethernet0.addressType="static"
    ethernet0.Address = "00:0c:29:40:10:d5"

При этом первые три числа вероятно надо будет сделать отличными от
00:0c:29:\*\|00:50:56:\*. (Не знаю правда к чему может привести смена
стандартных мак адресов для виртуальной сетевухи).
Или можно комбинировать оба метода. Закомментировав строчку не
создающую строчку в конфиге udev и вписав статический мак адрес для
сетевой карты ( тогда адрес желательно начинать с 00:50:56:).

Заключение
----------

Как видно настроить ваше операционную систему на работу в двух разных
окружениях не составляет большого труда. И к тому же можно не
использовать стандартные vmware-tools идущие в комплекте с программой, а
полностью перейти на открытую версию, что упрощает дальнейшие обновления
системы, т.к. не приходится следить за совместимоситью вручную, за вас
это сделали мейнтейнеры ОС.
