Библиотека для работы с облаками libcloud
##########################################
:date: 2014-01-21 00:17
:author: admin
:category: Python
:tags: http, Python, libcloud, clouds, облака
:slug: libcloud-basic

Так как последние 2 года моя работа связана с новомодными облаками,
то хотелось бы рассказать про хорошую библиотеку для питона,
которая позволяет имея один интерфейс работать с облаками разных провайдеров.
Эта библиотека называется `libcloud`_, поддерживает она большой список облачных провайдеров
от самых популярных `Amazon EC2`_ и до Ninefold (в том числе умеет новый `DigitalOcean`_ и `GCE`_).
Она дает интерфейс как к compute части облака (управление виртуальными машинами),
так и к дополнительным сервисам (S3, Load Balancer и т.д.)

==========
Установка
==========
Ставится она очень просто, как любой пакет питона.

.. code-block:: python

   pip install apache-libcloud
   pip install git+https://github.com/apache/libcloud.git


Я рекомендую ставить ее из гитхаба, если не в продакшен, т.к. очень много багфиксов
коммитится прямо в мастер.

==============
Использование
==============
Для примера использования, подключимся к Amazon EC2 и посмотрим, что оно отдаст нам:

.. code-block:: python

   from libcloud.compute.types import Provider
   from libcloud.compute.providers import get_driver

   driver = get_driver(Provider.EC2) #выбрали провайдера

   conn = driver('key', 'secret') #подключились с нашими ключами
   conn.list_sizes() #получили список размеров для инстансов

   [<NodeSize: id=t1.micro, name=Micro Instance, 
   ram=613 disk=15 bandwidth=None price=0.02 driver=Amazon EC2 ...>,
 	 <NodeSize: id=m1.small, name=Small Instance, 
   ram=1740 disk=160 bandwidth=None price=0.065 driver=Amazon EC2 ...>,
 	 <NodeSize: id=m1.medium, name=Medium Instance, 
   ram=3700 disk=410 bandwidth=None price=0.13 driver=Amazon EC2 ...>,
 	 <NodeSize: id=m1.large, name=Large Instance, 
   ram=7680 disk=850 bandwidth=None price=0.26 driver=Amazon EC2 ...>,
 	 ...]


Аналогично этому, мы можем смотреть список запущеных серверов, запускать/создавать инстансы,
управлять ключами, группами безопасности (security groups) и т.п.

На платформах, где поддерживается авторизация по ключам на серверах, можно делать так называемый deploy сервера.
Под деплоем понимается, что сервер выведется в состояние Running, дождемся SSH соединения и выполним указаные скрипты,
которые описываются на python.

.. code-block:: python

 	 from libcloud.compute.deployment import ScriptDeployment
   from libcloud.compute.deployment import MultiStepDeployment

   script = ScriptDeployment("yum -y install emacs strace tcpdump")
   msd = MultiStepDeployment([script])

   node = conn.deploy_node(deploy=msd)


В целом, данная библиотека очень хорошо подходит для поддержки многих облачных платформ, обладает понятным
и неплохо документированным API, а также ее авторы очень легко идут на контакт.
Чтобы сообщить о баге или что-то спросить, можно открыть тикет на гитхабе и втечение пары дней будет дан ответ.
А pull request обрабатываются почти всегда в 1 рабочий день, сам реквестил пяток новых фич/заплаток.


.. _libcloud: http://libcloud.org
.. _Amazon EC2: http://aws.amazon.com/ec2/
.. _DigitalOcean: http://digitalocean.com
.. _GCE: http://cloud.google.com/products/compute-engine‎