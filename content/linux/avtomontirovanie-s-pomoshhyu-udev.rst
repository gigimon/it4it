Автомонтирование с помощью udev
###############################
:date: 2009-06-07 13:05
:author: gigimon
:category: \*nix
:tags: flash, linux, udev, usb
:slug: avtomontirovanie-s-pomoshhyu-udev

После перехода с kde на openbox, стал вопрос автомонтирования
устройств (особенно флэшек). Погуглив, нашел несколько способов:

1. с помощью инструментов kde
2. с помощью gnome-mount
3. xfce4-mount
4. ivman
5. udev

Первые два не подходили, слишком много зависимостей. При третьем,
всегда пришлось бы держать в памяти апплет xfce и панель его, что тоже
не хотелось.
ivman я не смог заставить работать :( он тупо не монтировал, незнаю
почему.
А вот с udev немного разобрался, нагуглил готовое и теперь использую
его.

Итак, автомонтирование устрйоств с помощью udev является простым,
требуется всего лишь написать 1 файл с правилами.
Создаем файл для правил:

.. code-block:: bash

    touch /etc/udev/rules.d/10-udev-automount.rules

И вписываем в него следующие правила:

.. code-block:: bash

    KERNEL=="sd[b-z]", DRIVER=="usb-storage", GROUP="storage"ACTION=="add"
    KERNEL=="sd[b-z][0-9]", GROUP="storage", RUN+="/bin/mkdir -p /media/$env{ID_FS_LABEL_ENC}"ACTION=="add"
    KERNEL=="sd[b-z][0-9]", PROGRAM=="/lib/udev/vol_id -t %N", RESULT=="vfat", RUN+="/bin/mount -t vfat -o rw,flush,quiet,nodev,noauto,noexec,nosuid,noatime,dmask=000,fmask=111,iocharset=utf8 /dev/%k /media/$env{ID_FS_LABEL_ENC}"ACTION=="add"
    KERNEL=="sd[b-z][0-9]", PROGRAM=="/lib/udev/vol_id -t %N", RESULT=="ntfs", RUN+="/bin/mount -t ntfs-3g -o rw,flush,quiet,nodev,noauto,noexec,nosuid,noatime,dmask=000,fmask=111,iocharset=utf8 /dev/%k /media/$env{ID_FS_LABEL_ENC}"ACTION=="add"
    KERNEL=="sd[b-z][0-9]", RUN+="/bin/mount -o rw,noauto,noexec,nodev,noatime,dmask=000,fmask=111 /dev/%k /media/$env{ID_FS_LABEL_ENC}"
    ACTION=="remove", KERNEL=="sd[b-z][0-9]", RUN+="/bin/umount /dev/%k"
    ACTION=="remove", KERNEL=="sd[b-z][0-9]", RUN+="/bin/rmdir /media/$env{ID_FS_LABEL_ENC}"

Перегружаем службу udev.
После этого, при установке usb флэшки, она будет монтироваться в
/media в папку с названием флэшки (название тома), с полным доступом
пользователям, а также нормальной кодировкой

Из известных багов, есть два:

1. Если у флэшки нет названия тома, то она монтируется прямо в /media
2. Если флэшка определяется как /dev/sdb без цифр, она не монтируется
