Написание GUI для Python с помощью EasyGUI
##########################################
:date: 2008-09-11 20:05
:author: gigimon
:category: Python
:tags: easygui, Python, перевод
:slug: napisanie-gui-dlya-python-s-pomoshhyu-easygui

Хочу начать по-тихоньку переводить некоторые полезные статьи относящиеся
к компьютерах. Как проба пера, хочу перевести небольшую инструкцию по
использованию EasyGui. Объективная, не грубая критика принимается в
комментариях.

В большинстве случаев, для создания графического интерфейса используют
библиотеку Tkinter, либо аналогичную другую. Чаще всего, это делают люди
обладающие достаточным опытом программирования на Python, т.к. требуется
достаточно много сложного кода. К счастью, модуль EasyGUI добавляет
возможность быстро и легко написать качественный GUI для вашего скрипта.
Используя EasyGUI, требуется всего лишь несколько строк, для создания
визуальных элементов.

Лучший путь изучения EasyGUI раскрывается при использовании его с уже
существующим скриптом. Данный пример будет строиться на создании GUI
интерфейса к программе Pygmynote - простой менеджер информации,
созданный для личного использования, записи заметок, ссылок. Хотя
Pygmynote и не сложен в использовании, добавим к нему несколько строчек
ввода, сделающие его более легким для управления записями.

Перед началом работы, надо установить EasyGUI. Скачайте последнюю версию
с официального сайта, распакуйте полученный архив и перенесите файл
easygui.py в директорию /usr/lib/python2.5/site-packages. Для
импортирования модуля EasyGUI используйте в своем скрипте строчку (в
начале скрипта)

.. code-block:: python

    from easygui import

Теперь можно приступать к изучению.

Для начала создадим окно приветствия программы Pygmynote, которое будет
встречать пользователей при запуске с помощью всплывающего окна
MessageBox. Функция msgbox требует всего-лишь один обязательный
параметр, текст сообщения:

.. code-block:: python

    msgbox("Pygmynote is ready.")

Помимо этого, у нее есть еще три параметра, которые можно использовать
для задания различных функций сообщения: заголовок (box title), подпись
кнопки (the button label) и картинку. Вы можете использовать последний
параметр для выделения окна с помощью .gif рисунка. Пример окна со всеми
тремя параметрами:

.. code-block:: python

    image = "pygmynote.gif"
    msgbox("Pygmynote is ready.", "Pygmynote", ok_button="Pile up!", image=image)

Для более легкого использования Pygmynote, можно создать меню со
списком, содержащее все команды. Пользователь сможет выполнить эту
команду выбрав ее из списка и нажав на кнопку "Ok", или с помощью
двойного клика по выбранной команде. Чтобы это сделать, можно
использовать EasyGui's choicebox функции. Также как и msgbox, checkbox
имеет три параметра: сообщение (the choicebox's message), заголовок (the
window title), и список опций (a list of options):

.. code-block:: python

    msg ="What's your favorite fruit?"
    title = "Fruity"
    choices = ["Apple", "Apricot", "Pineapple"]
    choice = choicebox(msg, title, choices)

Когда пользователь выберет один из параметров и нажмет на кнопку "Ok"
(или двойной клик на выбраном), то функция вернет имя выбранного
элемента. Чтобы создать choicebox для Pygmenot, надо в список добавить
параметры программы:

.. code-block:: python

    msg ="Select command and press OK"
    title = "Pygmynote"
    choices = ["Help", "Insert new record", "Show all records", "Quit"]
    command = choicebox(msg, title, choices)

Если вы сейчас запустите скрипт, то увидите окно choicebox с
отсортированным по алфавиту содержимым. Почему EasyGUI не соблюдает
порядок установки параметров? Чтобы этого избежать, надо использовать
такую запись: "1 - Insert new record" или "X - Quit".

Следующая часть разработки нашего скрипта, это отображение найденых
результатов.  Следующий код, показывает все полученные значения:

.. code-block:: python

    elif command=="a":
      cursor.execute ("SELECT * FROM notes ORDER BY id ASC")
      rows = cursor.fetchall ()
      for row in rows:
          print "n   %s %s [%s]" % (row[0], row[1], row[2])
      print "n   Number of records: %d" % cursor.rowcount

Используя функцию textblock можно отобразить множество строк в приятном
text box. Чтобы это создать, вам надо немного изменить код возвращающий
каждую найденую запись в виде строки. Используйте result\_list = [] для
создания пустого списка, и метод .append для добавления в него записей:

.. code-block:: python

    elif command=="Show all records":
      cursor.execute ("SELECT * FROM notes ORDER BY id ASC")
      rows = cursor.fetchall ()
      result_list = []
      for row in rows:
          record_str = "n%s %s [%s]" % (row[0], row[1], row[2])
          result_list.append (record_str)
      textbox ("Found records:", "Pygmynote", result_list)

EasyGui's boolbox функция позволяет вручную контролировать потоки
скрипта. Для примера, когда вы обновляете запись в Pygmynote, скрипт
спрашивает, уверены ли вы в обновлении записи или тэга. Оригинальный код
выполняющий данную функцию таков:

.. code-block:: python

    elif command=="u":
      input_id=raw_input("Record id: ")
      input_type=raw_input("Update note (n) or tags (t): ")
      if input_type=="n":
          input_update=raw_input("Note: ")
          sqlstr=escapechar(input_update)
          cursor.execute ("UPDATE notes SET note='" + sqlstr + "' WHERE id='" + input_id + "'""")
      else:
          input_update=raw_input("Tags: ")
          sqlstr=escapechar(input_update)
          cursor.execute ("UPDATE notes SET tags='" + sqlstr + "' WHERE id='" + input_id + "'""")
      print "nRecord has been updated."

Функция boolbox позволяет вам показать диалоговое окно с двумя кнопками.
Функция возвратит 1, если нажата первая кнопка, и 0 - если вторая. Вот
простой пример:

.. code-block:: python

    if boolbox("What do monkeys like most?", "Pygmynote", ["Bread", "Bananas"]):
        msgbox ("Well, not really.")
    else:
        msgbox ("Yep, that's what they like most.")

В нашем случае, вы можете использовать функцию boolbox для показа
диалогового окна с двумя кнопками выбора "Note" или "Tag", и
перенаправления на обработку этого выбора:

.. code-block:: python

    elif command=="Update record":
      input_id=enterbox(msg='Record ID: ', title='Pygmynote', default='', strip=True)
      if boolbox("What do you want to update?", "Pygmynote", ["Note", "Tags"]):
        input_update=enterbox(msg='Enter note: ', title='Pygmynote', default='', strip=True)
        sqlstr=escapechar(input_update)
        cursor.execute ("UPDATE notes SET note='" + sqlstr + "' WHERE id='" + input_id + "'""")
      else:
        input_update=enterbox(msg='Enter tags: ', title='Pygmynote', default='', strip=True)
        sqlstr=escapechar(input_update)
        cursor.execute ("UPDATE notes SET tags='" + sqlstr + "' WHERE id='" + input_id + "'""")
      msgbox ("Record has been updated.", "Pygmynote", ok_button="Close")

Для создания imput box только с числовыми вариантами, можно использовать
функцию integerbox. В параметры функции можно задать верхний и нижний
диапазон. Для примера, можно модифицировать часть скрипта Pygmynote
отображающего календарь с месяцами от 1 до 12:

.. code-block:: python

    inputmonth=integerbox(msg='"Month (1-12): "', title='Pygmynotes', default='', argLowerBound=1, argUpperBound=12)

Также, EasuGUI предлагает функцию diropenbox, которая показывает dialog
box выбора директории. Вы можете добавить эту функцию в часть скрипта
Pygmynote для выбора пути сохранения всех записей pygmynote.txt..
Оригинальная часть кода сохраняющая все записи в исходную папку, но
используя diropenbox для указания пользователем папки сохранения:

.. code-block:: python

    elif command=="Save all records as pygmynote.txt":
      cursor.execute ("SELECT * FROM notes ORDER BY id ASC")
      rows = cursor.fetchall ()
      filedir = diropenbox(msg="Select directory", title="Pygmynote", default=None)
      filename = filedir + os.sep + "pygmynote.txt"
      if os.path.exists(filename):
          os.remove(filename)
      for row in rows:
         file = open(filename, 'a')
         file.write("%st%st[%s]n" % (row[0], row[1], row[2]))
         file.close()
      msgbox ("Records have been saved in the pygmynote.txt file.", "Pygmynote", ok_button="Close")

EasyGui не может заменить полнофункциональные библиотеки для создания
интерфейсов, такие как TKinter, WxPython, GTK+, QT, но является
замечательным средством для создания интерфейсов простых скриптов
новичками.

Ссылки: `первоисточник`_

Официальный сайт `EasyGUI`_

Скрипт `Pygmynote`_

`EasyGui tutorial`_

.. _первоисточник: http://www.linux.com/feature/145949
.. _EasyGUI: http://easygui.sourceforge.net/
.. _Pygmynote: http://code.google.com/p/pygmynote/
.. _EasyGui tutorial: http://www.ferg.org/easygui/tutorial.html
