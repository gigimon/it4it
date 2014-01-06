Скрипт получения состояния счета Djuice
#######################################
:date: 2009-04-26 23:53
:author: gigimon
:category: Python
:tags: djuice, Python, счет
:slug: skript-polucheniya-sostoyaniya-scheta-djuice

Для своих нужд написал быстренько небольшой скрипт, который выводит
состояние текущего счета оператора Djuice Украина. Скрипт просто выводит
колчиество денег на счету, я его показываю в conky :)

Вот скрипт:

.. code-block:: python

    # -*- coding: utf-8 -*-
    import urllib
    import urllib2
    import re
    TEL_NUM="8097xxxxxxx"
    PASSWORD="asfdxczcx"
    urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor))
    params = urllib.urlencode({"user":TEL_NUM,"password":PASSWORD})
    stat = urllib2.urlopen("https://my.djuice.com.ua/tbmb/login_djuice/perform.do",params)
    sta = stat.read()

    regexp = re.compile(r'([-d.]+)')
    variables = regexp.findall(sta)

    print "На счету: %s грн" % variables[0]

 
Может все-таки он и будет кому полезен
