Социальные штуки в Django с Redis часть 2
#########################################
:date: 2011-06-04 15:15
:author: gigimon
:category: Django
:tags: Django, Python, redis, комментари
:slug: socialnye-shtuki-v-django-s-redis-chast-2

В прошлой части я рассказал, как использую Redis в Django для показа
онлайн пользователей. Во второй же части я расскажу, как сделать показ
новых комментариев для постов (количество у каждого поста и подсветка
новых в посте).

Разберемся сначала, из каких частей будет состоять вся "индикация":

1. Тэг, показывающий сколько новых комментариев в топике у данного
пользователя

2. Функция, возвращающая номера новых комментариев в посте и удаляющая
их из базы

3. Функция добавляющая новый комментарий в список 'новых' для всех
пользователей

Для понимания работы этих функций, рассмотрим ключи в базе:

'users:%username%:posts' - содержит номера новых постов

'users:%username%:%post.id%' - содержит id комментариев для поста

'users:%username%' - общее количество новых комментариев

Теперь, рассмотрим функции по работе с базой и их применение для каждого
случая.

Все начинается с того, что при сохранении комментария его id
записывается в базу для каждого юзера:

.. code-block:: python

    def add_comment(sender, **kwargs):
        comment = kwargs['instance']
        if redis_db.exists('users'):
            users = redis_db.smembers('users')
            if comment.author.username not in users:
                redis_db.sadd('users', comment.author.username)
                users.add(comment.author.username)
        else:
            redis_db.sadd('users', comment.author.username)
            users = redis_db.smembers('users')
        for user in users:
            if user == comment.author.username:
                continue
            if redis_db.exists('users:%s' % user):
                if int(redis_db.get('users:%s' % user)) < getattr(settings, 'UNREAD_LIMIT', 100):
                    redis_db.incr('users:%s' % user)
                    redis_db.sadd('users:%s:%s' % (user, comment.post.id), comment.id)
                    redis_db.sadd('users:%s:posts' % user, comment.post.id)
                else:
                    continue
            else:
                redis_db.set('users:%s' % user, 0)

Работает код просто, сначала достаем список со всеми пользователями
(ключ 'users'), а потом проходимся по каждому и добавляем номер
комментария в ключ с номером поста ('users:%username%:%post.id%') и
увеличиваем количество новых комментариев.

Данная функция сделана как сигнал и используется при сохранении
комментария:

.. code-block:: python

    post_save.connect(add_comment, sender=Comment)

Для отображения количества новых комментариев у каждого поста,
используется такой тэг:

.. code-block:: python

    register = template.Library()

    @register.tag(name='newcom_count')
    def get_count_newcom(parser, token):
        bits = token.split_contents()
        if len(bits) == 3:
            return NewcomCountNode(bits[1], bits[2])
        elif len(bits) == 5 and bits[3] == 'as':
            return NewcomCountNode(bits[1], bits[2], bits[4])
        else:
            raise template.TemplateSyntaxError, "%r tag requires a two argument, username and post_id" % token.contents.split()[0]

    class NewcomCountNode(template.Node):
        def __init__(self, username, count, varname=None):
            self.username = template.Variable(username)
            self.count = template.Variable(count)
            self.varname = varname
        def render(self, context):
            try:
                username = self.username.resolve(context)
            except template.VariableDoesNotExist:
                username = ''
            try:
                count = self.count.resolve(context)
            except template.VariableDoesNotExist:
                count = 1
            if self.varname:
                context[self.varname] = get_post_newcom(username, count)
                return ''
            return get_post_newcom(username, count)

Он используется в темплейтах, как

.. code-block:: python

    {% newcom_count user.username post.id as newcom %}

.. code-block:: python

    Функция для работы с базой:

.. code-block:: python

    def get_post_newcom(username, post_id):
        try:
            count = redis_db.scard('users:%s:%s' % (username, post_id))
        except:
            count = 0
        return int(count)

Она всего-лишь достает количество новых комментариев, если таких нет, то
вернет 0.

В самом посте, чтобы узнать какой комментарий является новым, используем
такую функцию:

.. code-block:: python

    def del_comment(post, username):
        if redis_db.srem('users:%s:posts' % username, post.id):
            comments = redis_db.smembers('users:%s:%s' % (username, post.id))
            redis_db.delete('users:%s:%s' % (username, post.id))
            count = int(redis_db.get('users:%s' % username))
            redis_db.set('users:%s' % username, count - len(comments))
        else:
            comments = []
        return [int(x) for x in comments]

На вход она принимает instance post и имя пользователя, а на выход
отдает список с id комментариев. В своей работе, она также удаляет из
ключа новые посты. Передача его в шаблон, позволяет простой проверкой
узнавать, новый или нет комментарий.

Я использую во вьюхе вывода поста:

.. code-block:: python

    newcomments = del_comment(post, request.user.username)

А в шаблоне делаю проверку:

.. code-block:: python

    {% if comment.id in newcom %}

На этом все и заканчивается. Как видно из кода, все достаточно просто,
по сравнению с использованием реляционных баз.
