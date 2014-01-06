Скрипт отправки на dpaste.com
#############################
:date: 2008-04-11 23:55
:author: admin
:category: Python
:tags: dpaste.com, Python
:slug: skript-otpravki-na-dpastecom

Хочу показать свой скрипт, написанный на Python для отправки содержимого
файла на сервич публикования кода ( ну или как они называются )
`dpaste.com`_ .

Собственно вот код скрипта:

.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    #Script for send to dpaste.com
    import urllib,sys
    #Список хедеров
    header = {'content':"",
          'language':"Python",
          'title':"",
          'poster':"",
          'hold':""
          }
    url = "http://dpaste.com/"
    #првоеряем аргументы введеные при запуске
    if len( sys.argv ) < 2:
        sys.exit(1)
    parameters = iter(sys.argv)
    #првоерка на наличие аргументов
    for argument in parameters:
        if argument.startswith("-"):
            try:
                value = parameters.next();
                if value.startswith("-"):
                    print "Vvedite parametr posle klu4a "%s"" % argument
                    sys.exit(1)
            except StopIteration:
                print "ERROR"
                sys.exit(1)
            if argument == "-l":
                header['language'] = value
            if argument == "-t":
                header['title'] = value
            if argument == "-p":
                header['poster'] = value
            if argument == "-h":
                header['hold'] = value
            if argument == "-f":
                name_file = value
                files = open(name_file,"r")
                header['content'] = files.read()
                files.close()

    openurl = urllib.urlopen(url,urllib.urlencode(header))
    adress = openurl.geturl()
    print "Your script on: %s" % adress

Работает скрипт довольно просто, отправляет данные на dpaste, с помощью
их веб формы для добавления кода.

Использовать скрипт крайне легко, он имеет несколько ключей:

-l --- язык, на котором написан код ( по-умолчанию питон ;) )

-t --- заголовок

-p --- имя автора

-h --- заблокировать или нет

-f --- путь к файлу для публикации.

Обязательным является только " -f "

P.S. Написан на чистом питоне, работоспособность проверена лишь в Linux.
Закинул его в /usr/sbin и юзаю через ' dpaste -f /path/to/file '

Удачи в использовании, если что-то непонятно,пишите, на
профессиональность кода не расчитываю)

.. _dpaste.com: http://dpaste.com
