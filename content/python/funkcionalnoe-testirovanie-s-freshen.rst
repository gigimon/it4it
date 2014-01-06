Функциональное тестирование с freshen
#####################################
:date: 2011-09-28 22:05
:author: gigimon
:category: Python
:tags: freshen, Python
:slug: funkcionalnoe-testirovanie-s-freshen

Некоторое время назад, набрел в сети на пакет cucumber, который помогает
создавать различные тесты. Все действия в тесте описываюстя с помощью
файла  сценария, который пишется на языке `Grekhin`_ представляющий из
себя обычный, понятный для человека текст на любом языке. К сожалению
cucumber это разработка для Ruby, но у него есть практически полная
копия переписаная под Python с поддержкой nose и  зовется `freshen`_

Теперь, расскажу про создание теста на freshen

Файл сценарий содержит в себе:

#. Путь к файлу с шагами теста (steps файл)
#. Описание данного теста
#. Сценарии

Для привязки шагов в коде с шагами в .feature файле используются
декораторы.

Для примера, стандартный .feature файл с описанием сценария выглядит так
(пример из документации):

.. code-block:: python

    Using step definitions from: 'steps', 'step/page_steps'

    Feature: Destroy a document
      In order to take out one's anger on a document
      As an unsatisfied reader
      I want to be able to rip off the pages of the document

      Scenario: Rip off a page
        Given a document of 5 pages
        And the page is 3
        When I rip off the current page
        Then the page is 3
        But the document has 4 pages

Файл с шагами будет выглядеть примерно так:

 

.. code-block:: python

    @Given('a document of 5 pages')
    def step1():
        pass
    @Given('the page is 3')
    def step2():
        pass
    @When('I rip off the current page')
    def step3():
        pass
    @Then('the page is 3')
    def step4():
        pass
    @Then('the document has 4 pages')
    def step5():
        pass

Основные ключевые слова при использовании английского языка для
написания сценариев:

Given, When, Then, But, And

Также, для описания шага можно использовать регулярные выражения:

.. code-block:: python

    @Given('the page is ([d]+)')
    def step2(page):
        pass

 

Т.к. freshen поддерживает работу с nose, то для его запуска через nose
можно использовать такую команду:

nosetests --with-freshen test.feature

После выполнения тестов, если не было неудачно закончившихся шагов,
покажет что все хорошо, иначе покажет на каком степе остановился. Также,
freshen поддерживает тэги, которые можно повесить на сценарии и
запускать только по тэгам.

.. _Grekhin: https://github.com/cucumber/cucumber/wiki/Gherkin
.. _freshen: https://github.com/rlisagor/freshen
