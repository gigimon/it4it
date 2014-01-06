Восстановление загрузчика GRUB
##############################
:date: 2009-04-03 23:55
:author: gigimon
:category: \*nix
:tags: grub, linux, загрузчик
:slug: vosstanovlenie-zagruzchika-grub

Иногда бывает нужным восстановить linux загрузчик GRUB и каждый раз я
что-то забывал :) Приходилось лезть в книжку по генте и смотреть. Решил
записать.

Для начала загрузимся с livecd. В моем случае это livecd с Gentoo.

Монтируем корневой раздел

.. code-block:: bash

    mount -t ext3 /dev/sda6 /mnt/gentoo

Затем монтируем /proc и /dev в систему, которой восстанавливаем
загрузчик:

.. code-block:: bash

    mount -t  proc none /mnt/gentoo/proc

    mount -o bind /dev/ mnt/gentoo/dev

После, chroot'имся в систему:

.. code-block:: bash

    chroot /mnt/gentoo /bin/bash

Теперь делаем команду:

.. code-block:: bash

    grep -v rootf /proc/mounts > /etc/mtab

И восстанови загрузчик. Есть 2 способа, автоматчиеский и ручной.
Рассмотрим сначала первый:

Надо всего-лишь запустить 1 команду:

.. code-block:: bash

    grub-install --no-floppy /dev/sda6

ключ --no-floppy используется если нет флоповод.

Либо ручной режим:

.. code-block:: bash

    grub

В появившейся колнсоли:

.. code-block:: bash

    root (hd0,5)  --- раздел с /boot

    setup (hd0) --- установка в MBR

    quit

Все,  после этого ребутимся и видим GRUB (ну если все хорошо прошло :)
