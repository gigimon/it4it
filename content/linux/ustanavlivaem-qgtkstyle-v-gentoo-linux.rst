Устанавливаем QGtkStyle в Gentoo Linux
######################################
:date: 2008-12-23 20:35
:author: gigimon
:category: \*nix
:tags: gentoo, gtk, qt4, theme
:slug: ustanavlivaem-qgtkstyle-v-gentoo-linux

После убиения KDE и перехода на софт GTK и Qt4 захотелось видеть их в
одинаковой цветовой гамме и с одинаковой темой. Подумал сначала
использовать gtk-engines-qt, но у него есть пара минусов: зависимости от
KDE4 (чуть ли не полностью кеды) и малое количество тем для Qt4.
Наткнулся на недавнюю разработку от Qt Software для Qt версии 4.4 под
названием QGtkStyle, которая использует тему GTK для Qt приложений.
Итак, приступим:

#. QGtkStyle в портежах официальных нету, поэтому надо добавить оверлей
   voyageur.
#. Установить QGtkStyle с помощью команды emerge qgtkstyle
#. Выбрать нужную тему для GTK \ |gtk-chtheme|
#. В файл ~/.gtkrc-2.0 добавить строчку в начало файла gtk-theme-name =
   "NAME"
#. В активный профиль /etc/profile  добавить запись export
   GTK2\_RC\_FILES="\`pwd\`/.gtkrc-2.0"
#. Перезагрузить активный профиль sorce /etc/profile
#. В qtconfig (qt4config) выбрать тему GTK, после этого перезапустить X
   сервер и радоваться результату

|qtconfig|

Результат:

|smplayer|

К сожалению SMPlayer не очень информативен, но софта на Qt с кучей
кнопок нету :)

Замечания:

Следует не забывать добавлять строчку  gtk-theme-name = "NAME", т.к.
она требуется для работы QGtkStyle. Если ее не будет, то при выборе в
qtconfig темы GTK, вы будете получать ошибку: "QGtkStyle cannot be used
together with the GTK\_Qt engine." Также можно использовать патченую gtk-chtheme,  патч и ебилд можно
взять `здесь`_

.. _здесь: http://bugs.gentoo.org/show_bug.cgi?format=multiple&id=250504

.. |gtk-chtheme| image:: {filename}/images/2008/12/gtk-chtheme.png
.. |qtconfig| image:: {filename}/images/2008/12/qtconfig.png
.. |smplayer| image:: {filename}/images/2008/12/smplayer.png
