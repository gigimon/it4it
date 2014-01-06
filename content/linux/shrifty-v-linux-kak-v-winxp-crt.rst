Шрифты в Linux как в WinXP (CRT)
################################
:date: 2008-12-22 00:50
:author: gigimon
:category: \*nix
:tags: crt, windows, монитор, шрифты
:slug: shrifty-v-linux-kak-v-winxp-crt

Недавно надоело смотреть на корявенькие шрифты в Linux, стал гуглить, н
онаходил только настройку для LCD монитора, а у меня CRT еще. Узнал по
форумам, дали ссылку на проект `SharpFonts`_. Воспользовался мануалом,
получил шрифты как в винде. Хочу вот перевести ман, для тех кто слабо
знает английский.

Для начала надо убедиться, что в системе установлено:

-  fontconfig (обычно идет во всех дистрибутивах)
-  freetype2 с поддержкой ByteCode Interpreter

После этого, требуется скачать шрифты от Microsoft. Но сперва прочитайте
лицензию `EULA`_, и если согласны с ней, вперед, скачивать :)

`andale32.exe`_ `arial32.exe`_ `arialb32.exe`_ `comic32.exe`_
`courie32.exe`_ `georgi32.exe`_ `impact32.exe`_ `tahoma32.exe`_
`times32.exe`_ `trebuc32.exe`_ `verdan32.exe`_ `webdin32.exe`_

После того как скачаете, надо установить пакет cabextract и распаковать
эти пакеты командой (от рута):

.. code-block:: bash

    mkdir -p /usr/share/fonts/truetype/

    cabextract -d /usr/share/fonts/truetype/ andale32.exe arial32.exe arialb32.exe comic32.exe courie32.exe georgi32.exe impact32.exe tahoma32.exe times32.exe trebuc32.exe verdan32.exe webdin32.exe

Затем,  скачать `файлы`_ конфигурации и распаковать их в /etc/fonts с
заменой старых:

.. code-block:: bash

    tar xvjpf fontconfig.tbz -C /etc/fonts/

После перезапуска иксов, у вас будут  шрифты как в WinXP

Удачи ;)

Авторство принадлежит `SharpFonts <http://sharpfonts.com/>`__

.. _SharpFonts: http://sharpfonts.com/
.. _EULA: http://sharpfonts.com/MS-EULA.txt
.. _andale32.exe: http://sharpfonts.com/fonts/andale32.exe
.. _arial32.exe: http://sharpfonts.com/fonts/arial32.exe
.. _arialb32.exe: arialb32.exe
.. _comic32.exe: comic32.exe
.. _courie32.exe: http://sharpfonts.com/fonts/courie32.exe
.. _georgi32.exe: http://sharpfonts.com/fonts/georgi32.exe
.. _impact32.exe: http://sharpfonts.com/fonts/impact32.exe
.. _tahoma32.exe: http://sharpfonts.com/fonts/tahoma32.exe
.. _times32.exe: http://sharpfonts.com/fonts/times32.exe
.. _trebuc32.exe: http://sharpfonts.com/fonts/trebuc32.exe
.. _verdan32.exe: http://sharpfonts.com/fonts/verdan32.exe
.. _webdin32.exe: http://sharpfonts.com/fonts/webdin32.exe
.. _файлы: http://sharpfonts.com/fontconfig.tbz
