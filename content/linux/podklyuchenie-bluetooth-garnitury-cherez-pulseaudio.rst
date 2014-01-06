Подключение Bluetooth гарнитуры через PulseAudio
################################################
:date: 2009-08-06 22:09
:author: gigimon
:category: \*nix
:tags: a2dp, bluetooth, linux, гарнитура
:slug: podklyuchenie-bluetooth-garnitury-cherez-pulseaudio

Решил все-таки написать статейку, после долгого летнего перерыва :)

После обновления ядра с 24 на 30, перестала работать bluetooth гарнитура
:( из-за того, что убрали mod\_bt\_sco, начал искать решение,
рекомендовали через PulseAudio (который не стоял из-за ненадобности).
Итак начнем, для начала обновим портежи и пересоберем мир с pulseaudio.

Добавляем в

.. code-block:: bash

    /etc/make.conf в секцию USE "pulseaudio avahi"

Обновляем мир

.. code-block:: bash

    emerge -avDNt world

Теперь установим компоненты PulseAudio

.. code-block:: bash

    emerge -av pulseaudio paprefs pavucontrol paman padevchooser pavumeter alsa-plugins

media-sound/pulseaudio - сам сервер
media-sound/paprefs - Графическая утилита для настройки параметров
сервера
media-sound/pavumeter - Графическая утилита, которая отображает
уровни звука (типа alsamixer)
media-sound/padevchooser - Утилита для настройки звуковых устройств и
потоков, создает иконку в трее, позволяет на лету переключать устройства
звука и многое другое
media-sound/paman - Утилита для тонкой настройки модулей
media-sound/pavucontrol - Утилита позволяющая переключать каналы ипотоки.

После этого, меняем профиль esd

.. code-block:: bash

    eselect esd set 2

Добавляем в автозагрузку avahi-daemon и pulseaudio

.. code-block:: bash

    rc-update add avahi-daemon default

    rc-update add pulseaudio default

Добавим нужного пользователя в группу PulseAudio

.. code-block:: bash

    gpasswd -a USER pulse
    gpasswd -a USER pulse-access

Теперь, настроим PulseAudio, редактируем /etc/conf.d/pulseaudio к такому
виду:

.. code-block:: bash

    PA_OPTS="--log-target=syslog"
    PULSEAUDIO_SHOULD_NOT_GO_SYSTEMWIDE=YES

Затем в /etc/init.d/pulseaudio в секции start(), изменяем строчку на:

.. code-block:: bash

    PA_ALL_OPTS="${PA_OPTS} --fail=1 --daemonize=1"

Настроим ALSA. В .asoundrc (в папке пользователя) добавляем:

.. code-block:: bash

    pcm.pulse {
    type pulse
    }

    ctl.pulse {
    type pulse
    }

    pcm.!default {
    type pulse
    }
    ctl.!default {
    type pulse
    }

Эти строки говорят, что для всего по дефолту будет использоваться
PulseAudio.

Теперь стартуем PulseAudio и рестартим ALSA

.. code-block:: bash

    /etc/init.d/alsasound restart

    /etc/init.d/pulseaudio start

Теперь запускаем pavucontrol и запускаем какой-нибудь аудио плеер, и
првоеряем, что звук играет и в pavucontrol появился этот поток. Если
появился, приступим к подключению гарнитуры.

Устанавливаем bluez версии 4.38 (4.39 почему-то не работает с
PulseAudio) и гуи к нему blueman

.. code-block:: bash

    emerge -va bluez blueman

Запускаем blueman-manager и спариваем свою гарнитуру с компьютером.
Затем подключаемся к ней ко службе A2DP. После этого, в pavucontrol во
вкладке Configuration должна появится наша гарнитура. Теперь на нее
можно направлять поток. Для этого на первой влкадке, напротив названия
потока жмем на галочку->Move stream и выбираем гарнитуру.

Надеюсь после этого, у вас гарнитура заработает :)

P.S. все сказаное относится к Gentoo Linux
