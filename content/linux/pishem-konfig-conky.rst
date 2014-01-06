Пишем конфиг conky
##################
:date: 2008-10-06 23:35
:author: gigimon
:category: \*nix
:tags: conky, linux
:slug: pishem-konfig-conky

Решил недавно занять свободное пространство по бокам от панельки. ничего
лучше не придумал, как показывать туда системную информацию, для этого
избрал conky.

Итак, мой конфиг коньков, будет показывать:

#. Загрузка двух ядер
#. Индикация свободной/занятой RAM и SWAP
#. Свободное пространство в / и /home/user (домашний каталог на
   отдельном разделе винта)
#. День недели и аптайм
#. Название активных сетевых интерфейсов с IP адресами, скоростью в
   данный момент (только для активных)

Приведу сразу текст конфига:

.. code-block:: bash

    override_utf8_locale yes # использование UFT-8 локаль (нужно для xft)
    use_xft yes # используем xft
    xftfont Liberation Mono:size=7 # используемый шрифтxftalpha 0.5 # коэффициент прозрачности
    update_interval 1.0 # частота обновления (на самом деле период)
    own_window yes # в отдельном окне
    own_window_type desktop # на десктопе (так же может быть normal или override)
    own_window_colour 000 # цвет фона
    double_buffer yes # двойная буферизация
    minimum_size 1274 5 # минимальный размер ширинаdraw_shades no # отключаем тенalignment bottom_left # расположение снизу слева
    gap_x 0 # начальные координаты: X
    gap_y 0 # начальные координаты: Y
    TEXT # выводимая информация
    ${voffset 2}${color grey}Core 1:${color white}${cpu cpu1}%${color red} | ${color grey}RAM: ${color white}${mem}/${memmax}${color grey}${color red} | ${color grey}ROOT: ${color white}${fs_free /}/${fs_size /} ${color grey} ${alignr}${color yellow}${time %a}${color white}${alignr}${if_up eth0} eth0 ${color gray}${addr eth0}${color red}>${color gray} ↓: ${color white}${downspeed eth0} kiB/s (${totaldown eth0}) ${color red}| ${color grey}↑: ${color white}${upspeed eth0} kiB/s (${totalup eth0})${endif} ${uptime}
    ${color grey}Core 2:${color white}${cpu cpu2}%${color red} | ${color grey}SWAP: ${color white}${swap}/${swapmax}${color grey}${color red} | ${color grey}HOME: ${color white}${fs_free /home/aliens}/${fs_size /home/aliens}${alignr}${if_up wlan0} Wlan0 ${color gray}${addr wlan0}${color red}>${color gray} ↓: ${color white}${downspeed wlan0} kiB/s (${totaldown wlan0}) ${color red}| ${color grey}↑: ${color white}${upspeed wlan0} kiB/s (${totalup wlan0})${endif}

Рассмотрим последнюю строчку, которая отвечает за выводимый текст.

Параметры (переменные) указываются в формате ${}, внутри блока пишется
команда. Текст, написаный не в блоке ${} будет просто выводиться на
панель. Основные использованные команды:

${color цвет} - указывает использующийся цвет после блока, до следующего
такого блока

${fs\_free раздел} - показывает количество свободного места на указаном
разделе

${fs\_size раздел} - размер раздела

${cpu cpuN} - показывает загрузку процессора N

${if\_up}, ${endif} - блок условие. Если условие выполняется (поднят
интерфейс или нет), то показывается весь код до ${endif}.

В конце, у меня получилась такая картина:

|image0|

Почитать про настройку можно на официальном `сайте`_

.. _сайте: http://conky.sourceforge.net/docs.html

.. |image0| image:: {filename}/images/2008/10/conky-450x8.jpg
   :target: {filename}/images/2008/10/conky.jpg
