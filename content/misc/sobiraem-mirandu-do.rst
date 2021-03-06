Собираем миранду до ...
#######################
:date: 2009-01-17 16:18
:author: gigimon
:category: Всякое
:tags: icq, miranda
:slug: sobiraem-mirandu-do

После чтения множестваспоров о том, что лучше, миранда или квип,
аргументы что миранду тяжело собрать до уровня квипа, решил написать
небольшйо мануал по сборке миранды.

Первое что надо сделать, скачать дистрибутив миранды. Все ниже описанное
будет проводиться на разрабатываемой версии 0.8 Test Build 26 Unicode,
взятая `здесь`_

После этого, распакуем куда нибудь. И уберем ненужные нам файлы
(ChangeLog.txt и в папке plugins не нужные протоколы и плагины). В папке
plugins  я удалил файлы:

chat.dll - плагин для поддержки чатов

clist\_classic.dll, clist\_mw.dll, clist\_nicer.dll - плагины для вывода
контакт листа. Это разные вариации, мы будем использовать
clist\_modern.dll

GG.dll, irc.dll, jabber.dll, msn.dll, yahoo.dll - плагины для поддержки
различных протоколов.

scriver.dll, srmm.dll -  плагины для создания окон чата

Теперь `скачаем`_ файл русификации и распакованый положим в корень папки
миранды.

После надо скачать и добавить некоторые полезные плагины:

`smileyadd`_ unicode - поддержка смайликов

`ieview`_ - окно чата с поддержкой Html тэгов, скинов, использующее
движок IE для вывода.

`history++`_ - мощная система для ведения логов

`tipper`_ - вывод всплывающего информационного окна для контакта

`fingerprint`_ - опознавание клиентов собеседников

После того как скачаете, распаковываете все, все .dll ложите в папку
plugins, а остальыне папки которые будут, в корень миранды (только
ieview и папку и .dll положить в plugins)

Теперь запустим миранду miranda32.exe. Появится окно для создания вашего
файла профиля, пишем любое имя.

|crdb|

После ввода имени, жмем Создать. Увидим контакт лист и окно добавления
учетных записей. жмем на зеленый плюсик, и в появившемся окне вписываем
название учетной записи и выбираем протокол ICQ:

|cruser|

Жмем ОК, выбираем созданую учетку, и вписываем свои ICQ номер и пароль и
жмем Ок

Увидим наш КЛ, теперь можем подключиться к сети.

После этого, будем настраивать наши плагины. заходим в настройки
(нажимаем на значок миранды, корону, настройки).

1. Настраиваем  наше окно чата:

Беседы-Журнал-Основной журнал сообщений --- выбираем IEView

Беседы-Журнал-Параметры --- Поддержка BBCode

Беседы-Журнал IEView-Общее --- Поддержка BBCode, Поддержка flash,
Включить прозрачность для PNG

Беседы-Чаты --- Включить интеграцию чата

После этого перегружаем миранду.

Потом выбираем любой контакт, чтобы открыть окно чата, жмем
Контейнер-Настройки контейнера-Окно --- ставим галочки у Скрыть меню,
Показать инфо-панель

2. Настроим плагин ICQ

Настройки-Сеть-Входящие (и исходящие) сообщения --- Поставить галочку
Порты и  вписать: 1050-1100, 2000-2900,34891, 32528, 26120

Сеть-<название вашего аккаунта ICQ, который писали в начале>
-Возможности --- Поставить галочку: только подтверждение с сервера.

3. Настроим всплывающее окно с информацией контактов

Тонкая настройка-Подсказки --- и выбираете все на свой вкус :)

4. Настройка контакт листа

Список контактов-Элементы строк-Аватар --- Значки на аватарах-Значок
контакта

Список контактов-Элементы строк-Значок --- прятать значок протокола,
Значок хСтатуса вместо пзначка протокола

Список контактов-Элементы строк-Экстра значки --- Снять галчоки с
Протокол, Телефон/SMS, Web страница.

Т.к. все по русски, поизменяйте все на свой вкус.

Последний этап, это установка скинов.

1. Установим скин на КЛ

Качаем любой стиль для Modern CList `отсюда`_

Я скачал BlackStyle. распаковываем его в корень мирандыthemesmodern

После этого, идем в

Настройки-Тонкая настройка-Скин списка --- жмем кнопку Обзор, выбираем
папку, куда скопировали скин и выбираем .msf файл, жмем Ок. Этот скин
появится в обозревателе, выберем его и нажмем применить. Вы могли
заметить, что у некоторых скинов есть свои кнопки быстрого доступа, и
получается две панели одинаковых кнопок. Чтоыб отключить кнопки миранды,
надо зайти:

Настройки-Тонкая настройка-Панель кнопок и снять галочку с Кнопки в
панели кнопок.

|clist| |image0|


2. Установка скина для окна разговора (чата)

Качаем любой скин для tabSrmm
`отсюда <http://addons.miranda-im.org/index.php?action=display&id=90>`__

Я взял скин BlackStyle. Скачаный архив распаковываем в tabsrmmskins

Потом идем в Настройки-Тонкая настройка-Скин окна беседы, жмем на "..."
и выбираем файл .tsk из распакованной папки. Ставим галочки на:
загружать этот скин при старте, загружать шрифты из скина. Жмем на
кнопку Применить скин

|chat|

3. Установка скина для списка сообщений (ieview)

Качаем
`отсюда <http://addons.miranda-im.org/index.php?action=display&id=83>`__
любой скин для ieview и распаковываем его в themesieview

Затем, идем в

Настройки-Беседы-Журнал IEView-Журнал --- выбираем Шаблон, жмем "...",
выбираем наш скин .ivt

4. Осталось последнее, поменять иконки статусов.

Качаем стандартный набор ICQ иконок, распаковывем в Icons

Настройки-Значки-Статус-ICQ, жмем кнопку Выбрать набор значков, и
выбираем распакованный .dll файл, все иконки ICQ поменяются

В итоге получил :

|all|

К сожалению, не очень удачный скин, т.к. цвет шрифтов черный и совпадает
с фоном. Но думаю, вы сможете найти хорошие скины, это самое сложное )

.. _здесь: http://files.miranda-im.org/builds/miranda-v080a26w.zip
.. _скачаем: http://addons.miranda-im.org/feed.php?dlfile=3415
.. _smileyadd: http://addons.miranda-im.org/feed.php?dlfile=2455
.. _ieview: http://addons.miranda-im.org/feed.php?dlfile=1788
.. _history++: http://addons.miranda-im.org/feed.php?dlfile=2995
.. _tipper: http://addons.miranda-im.org/feed.php?dlfile=3717
.. _fingerprint: http://addons.miranda-im.org/feed.php?dlfile=3526
.. _отсюда: http://addons.miranda-im.org/index.php?action=display&id=93

.. |image0| image:: {filename}/images/2009/01/clist.png
   :target: {filename}/images/2009/01/clist.png
.. |crdb| image:: {filename}/images/2009/01/crdb.png
   :target: {filename}/images/2009/01/crdb.png
.. |cruser| image:: {filename}/images/2009/01/cruser.png
   :target: {filename}/images/2009/01/cruser.png
.. |clist| image:: {filename}/images/2009/01/clist.png
   :target: {filename}/images/2009/01/clist.png
.. |chat| image:: {filename}/images/2009/01/chat.png
   :target: {filename}/images/2009/01/chat.png
.. |all| image:: {filename}/images/2009/01/all.png
   :target: {filename}/images/2009/01/all.png
