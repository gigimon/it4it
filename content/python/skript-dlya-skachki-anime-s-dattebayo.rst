Скрипт для скачки аниме с dattebayo
###################################
:date: 2008-04-18 17:17
:author: gigimon
:category: Python
:tags: Python, аниме
:slug: skript-dlya-skachki-anime-s-dattebayo

Решил поделиться своим скриптом для скачки аниме с `dattebayo`_ . Там
выкладываются релизы от dattebayo. Последнее время там: bleach, naruto.

Собственно, мой скрипт качает серии блича (наруто я не смотрю) с главной
страницы сайта.

Вот весь скрипт:

.. code-block:: python

    #!/bin/python
    # -*- coding: utf-8 -*-
    import urllib
    import os
    import re

    class getsBleach:
        def __init__(self, url_site="http://dattebayo.com/", file="bleach"):
            self.url_site = url_site
            self.file = file
        def find_link(self, url):
            """В этом методе, получим из страницы все ссылки на торрент с бличем"""
            try:
                site = urllib.urlopen(self.url_site)
            except URLError:
                print "Error URL"
                return 0
            site = site.read()
            razdel = re.compile(r'( Bleach d+ )') #делаем паттерн
            result = razdel.findall( site ) #находим все по паттерну в список
            for rez in reversed(result):
               episode_num = "".join(rez).split(" ")[-2] #находим нмоер эпизода
               if episode_num > self.getOldNum(): #проверка на новизну
                   link = "".join(result).split(""")[1] #ссылка
                   self.saveNewEpisode(episode_num) #передаем на обработку ссылки
        def getOldNum(self):#тут получаем из файла номер последней серии
            try:
               numfile = open( self.file, "r" )#имя файла при инициализации
            except:
               return 0
            numOldEpisode = numfile.readline()
            file.close
            return numOldEpisode
        def saveNewEpisode( self, newEpisode, tor_com="transmission-remote -a" ):
            tor_url = self.url_site + "t/b" + newEpisode + ".torrent" #создаем ссылку
            fileurl = urllib.urlretrieve(tor_url) #скачиваем торрент
            os.system("%s %s" % (tor_com, fileurl[0]))#отправляем торрент транмишиону
            file = open( self.file, "w+" )#записываем номер эпизода
            file.write( "%s" % newEpisode )
            file.close()

    starting = getsBleach()
    numep = starting.getOldNum()
    starting.find_link(numep)

Торренты скачиваются в /tmp (ну или временную папку системы), и
передаются на скачку transmission-remote.

Скрипт удобно держать в cron'e,  чтобы автоматизировать скачку аниме ;)

.. _dattebayo: http://dattebayo.com
