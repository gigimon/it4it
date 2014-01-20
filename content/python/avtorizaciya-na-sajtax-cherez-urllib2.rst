Авторизация на сайтах через urllib2
###################################
:date: 2012-06-11 23:17
:author: admin
:category: Python
:tags: http, Python, urllib2, авторизация
:slug: avtorizaciya-na-sajtax-cherez-urllib2

Стандартная библиотека питона для работы с вебом - urllib2, позволяет
с помощью использования различных хэндлеров добавлять различный
функционал. Будь то обработка ssl, работа с cookies либо какие-то
расширения http протокола. А если есть работа с cookies, то значит можно
авторизироваться на различных сайтах и ходить по "закрытой" их части :)

Для примера, залогинимся на `лоре`_

Сначала нам требуется создать объект, который будет хранить наши куки,
этот объект создается из библиотеки cookielib

.. code-block:: python

    import cookielib

    cookie = cookielib.CookieJar()

После этого, создаем объект opener из urllib2, собственно, для общения
по протоколу http с добавлением cookie хэндлера

.. code-block:: python

    import urllib2

    req = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

Чтобы не было проблем с некоторыми веб-серверами, добавим юзер агент,
пораспространеннее

.. code-block:: python

    req.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.11) Gecko/20101012 Firefox/3.6.11'), ]

и установим наш opener как глобальный (необязательно)

.. code-block:: python

    urllib2.install_opener(self.req)

После этого, надо открыть страницу по определенному адресу и передать
туда параметры соответственно формы авторизации.

Чтобы определить адрес, на который отправлять данные, а также, как поля
формы называется, надо открыть исходники html страницы и найти форму
авторизации. Для примера, на lor она выглядит так:

.. code-block:: python

    Имя:
    Пароль:


Из формы нам требуется адрес из тэга <form> и его аттрибут action, здесь
он login.jsp, что значит адрес для отправки будет
http://linux.org.ru/login.jsp

Данные, которые надо отправлять смотрим в тэгах <input> и аттрибут name,
здесь нам потребуются nick и passwd.

Итак, теперь попробуем залогиниться:

.. code-block:: python

    resp = req.open('http://linux.org.ru/index.jsp', urllib.urlencode({'nick':'username', 'passwd':'password'}))

В объекте resp лежит код, который нам отправил веб-сервер, если это 200,
то значит все прошло хорошо (обычно это так :)

Также, можем проверить объект cookies и увидеть, что там появился номер
сессии

.. code-block:: python

    print cookie

    cookielib.CookieJar[Cookie(version=0, name='JSESSIONID', value='01626E21D72D336E302F5702AFE208A',

Чтобы прочитать содержимое страницы, используем resp.read()

Все, теперь используя объект resp мы можем ходить по сайту с куками и
авторизованными

.. _лоре: http://linux.org.ru
