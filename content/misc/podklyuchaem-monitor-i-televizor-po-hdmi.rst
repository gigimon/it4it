Подключаем монитор и телевизор по hdmi
######################################
:date: 2009-01-03 20:47
:author: gigimon
:category: \*nix
:tags: gentoo, nvidia, xinerama, мониторы, телевизор, экраны
:slug: podklyuchaem-monitor-i-televizor-po-hdmi

Последние 3 месяца заместо плохого по качеству кабельного ТВ использую
ресурс `ZomboBox`_ Множество каналов, возможность просмотра любой
программы в любое время и другие плюсы современного мира. Поэтому
используя вывод по hdmi на телевизор, показывал домашним ТВ :) Но есть 1
минус, при полноэкранном режиме, Flash плеер не дает убрать фокус с окна
и вылетает в небольшое окошко. Решил я эту задачу в любимом Linux :) с
помощью создания двух X серверов, и запуске на втором этого плеера в
полный экран :)

Сразу оговорю, видеокарта у меня NVIDIA 9600GT с драйверами 180.18,
монитор подключен к DVI1 Samsung 753DF, а телевизор подключен к HDMI к
телевизору Phillips.

Итак,  после всех моих проверок и читания, какой же режим нужен для
такой работы в драйверах NVIDIA (по выборам всяких режимах в
nvidia-settings), нам требуется режим Separate X screen с выключеным
Xinerama.

После включения этого режима, можем получить такой xorg.conf:

.. code-block:: bash

    Section "ServerLayout"
    Identifier     "Layout0"
    Screen      0  "Screen0" 0 0
    Screen      1  "Screen1" 1024 0
    EndSection

    Section "Files"
    EndSection

    Section "Module"
    Load           "dbe"
    Load           "extmod"
    Load           "type1"
    Load           "freetype"
    Load           "glx"
    EndSection

    Section "ServerFlags"
    Option         "Xinerama" "0"
    EndSection

    Section "Monitor"

    # HorizSync source: builtin, VertRefresh source: builtin
    Identifier     "Monitor0"
    VendorName     "Unknown"
    ModelName      "CRT-0"
    HorizSync       28.0 - 55.0
    VertRefresh     43.0 - 72.0
    Option         "DPI" "96 x 96"
    Option         "DPMS"
    EndSection

    Section "Monitor"

    # HorizSync source: edid, VertRefresh source: edid
    Identifier     "Monitor1"
    VendorName     "Unknown"
    ModelName      "Philips 1080p TV (3)"
    HorizSync       31.0 - 80.0
    VertRefresh     47.0 - 85.0
    Option       "DPI" "96 x 96"
    Option         "DPMS"
    EndSection

    Section "Device"
    Identifier     "Device0"
    Driver         "nvidia"
    VendorName     "NVIDIA Corporation"
    BoardName      "GeForce 9600 GT"
    BusID          "PCI:1:0:0"
    Screen          0
    EndSection

Мышь и клавиатура работают через HAL, поэтому их упоминаний тут нету.

Также, помимом стандартных опций сгенерированных nvidia-settings,
добавил

.. code-block:: bash

    Option       "DPI" "96 x 96"

чтобы все нормально смотрелось :)

С таким конфигом, разрешение экрана на телевизоре меняется без
перезагрузки иксов.

Чтобы запустить чт-либо на втором Х сервере (телевизоре), используйте
комманду:

.. code-block:: bash

    DISPLAY=:<номер_экрана> <программа>

Удачи в работе на двух экранах :)

.. _ZomboBox: http://zombobox.com
