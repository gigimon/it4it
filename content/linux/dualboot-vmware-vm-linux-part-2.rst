Двойная загрузка виртуальных машин VMWare под Linux. Часть 2. Графика.
######################################################################
:date: 2009-04-18 23:42
:author: Goletsa
:category: \*nix
:tags: vmware, X, x-server, xorg, графика, настройка
:slug: dualboot-vmware-vm-linux-part-2

Такие вкусные возможности, как то освобождение курсора из окна
виртуальной машины без нажатия горячих клавиш или Drag and Drop требуют
установки специальных драйверов.
Они входят как и в официальные VMWARE Tools так и в их открытую
версию.

Ставим их штатными средствами:

.. code-block:: bash

    aptitude install xserver-xorg-video-vmware xserver-xorg-input-vmmouse open-vm-toolbox

Для переключения между драйверами при запуске компьютера можно
воспользоваться несложным скриптом, базирующемся частично на исходном
коде open-vm-tools:

.. code-block:: bash

    #!/bin/sh

    exit_if_not_in_vm () {
        if [ ! -x /usr/bin/vmware-checkvm ] || ! /usr/bin/vmware-checkvm > /dev/null 2>&1
        then
             echo "Not starting as we're not running in a vm."
             cp -f /etc/X11/xorg.conf.realpc /etc/X11/xorg.conf && echo “Real Videocard driver selected”
    exit 0
    fi
    }

    case "${1}" in
    start)
    # Check if we're running inside VMWare
    exit_if_not_in_vm
    cp -f /etc/X11/xorg.conf.vmware /etc/X11/xorg.conf && echo “VMWARE X Driver selected”
    ;;
    *)
    echo “VMWARE Video Driver Xorg config changer”;
    exit 1;
    ;;
    esac

Примерный вид xorg.conf.vmware:

.. code-block:: bash


    Section "InputDevice"
            Identifier    "VMware Keyboard"
            Driver        "kbd"
            Option        "XkbRules"    "xorg"
            Option        "XkbModel"    "pc105"
            Option        "XkbLayout"    "us"
    EndSection

    Section "InputDevice"
            Identifier    "VMware Mouse"
            Driver        "vmmouse"
            Option        "CorePointer"
            Option        "Device"    "/dev/input/mice"
            Option        "Emulate3Buttons"    "true"
            Option        "ZAxisMapping"    "4 5"
    EndSection

    Section "Device"
            Identifier  "VMware SVGA"
            Driver      "vmware"
    EndSection

    Section "Screen"
            Identifier    "Default Screen"
            Device      "VMware SVGA"
            Monitor     "vmware"
    # Don't specify DefaultColorDepth unless you know what you're
    # doing. It will override the driver's preferences which can
    # cause the X server not to run if the host doesn't support the
    # depth.
            Subsection "Display"
                    # VGA mode: better left untouched
                    Depth       4
                    Modes       "640x480"
                    ViewPort    0 0
            EndSubsection
            Subsection "Display"
                    Depth       15
                    Modes       "800x600"
                    ViewPort    0 0
            EndSubsection
            Subsection "Display"
                    Depth       16
                    Modes       "800x600"
                    ViewPort    0 0
            EndSubsection
            Subsection "Display"
                    Depth       24
                    Modes       "800x600"
                    ViewPort    0 0
            EndSubsection
    EndSection

    Section "ServerLayout"
            Identifier    "Default Layout"
            Screen       "Default Screen"
            InputDevice    "VMware Keyboard"    "CoreKeyboard"
            InputDevice "VMware Mouse"    "CorePointer"
    EndSection

    Section "Monitor"
            Identifier      "vmware"
            VendorName      "VMware, Inc"
            HorizSync       1-10000
            VertRefresh     1-10000
    EndSection

В нем настроен и сам адаптер чтобы можно было без нажатий на Hotkey
перемещать мышь между хостом и гостем, так и сам драйвер виртуальной
мышки, чтобы движения были не судорожными. При желании можно указать
другие разрешения и глубину цвета.

Соответственно в xorg.conf.realpc у вас должен быть конфигурационный
файл для обычной видеокарты, а в xorg.conf.vmware — для виртуальной.
Так же у вас обязательно должны стоять open-vm-tools, так как
программа для проверки реальный это компьютер или нет входит

Сам скрипт надо положить в /etc/init.d/checkvmvideo к примеру и сделать
его исполняемым:

.. code-block:: bash

    chmod +x /etc/init.d/checkvmvideo

Следующим шагом надо заставить этот скрипт стартовать при старте системы
что делается проще простого:

.. code-block:: bash

    update-rc.d checkvmvideo defaults

На что система вам ответит чемто похожим на:

.. code-block:: bash

    update-rc.d: warning: /etc/init.d/checkvmvideo missing LSB information
    update-rc.d: see
    Adding system startup for /etc/init.d/checkvmvideo ...
    /etc/rc0.d/K20checkvmvideo -> ../init.d/checkvmvideo
    /etc/rc1.d/K20checkvmvideo -> ../init.d/checkvmvideo
    /etc/rc6.d/K20checkvmvideo -> ../init.d/checkvmvideo
    /etc/rc2.d/S20checkvmvideo -> ../init.d/checkvmvideo
    /etc/rc3.d/S20checkvmvideo -> ../init.d/checkvmvideo
    /etc/rc4.d/S20checkvmvideo -> ../init.d/checkvmvideo
    /etc/rc5.d/S20checkvmvideo -> ../init.d/checkvmvideo

Все. Теперь при старте системы будет проверка на виртуальную машину и
выбираться правильный конфиг X.org
