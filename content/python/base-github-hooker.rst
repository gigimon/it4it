Простой сервер для ловли GitHub webhooks на BaseHTTPServer
##########################################################
:date: 2014-08-08 15:17
:author: admin
:category: Python
:tags: http, Python, github, webhook
:slug: base-github-hooker

Пришлось недавно освоить Github webhooks, чтобы автоматически обновлять на продакшене код, после пуша в мастер :)
Итак, те кто незнает, что это, прочитайте - `Github Webhooks <https://developer.github.com/webhooks/>`_ либо в двух словах.
При получении каждого коммита, гитхаб может отправить POST запрос с данными об этом коммите по указаной вами ссылке.

Для того, чтобы настроить такие уведомления, у репозитория в Settings->Webhooks надо добавить свой URL.

Собственно, погуглив интернетик я не нашел чего-то простого для получения таких хуков и обработки их.
Либо же это было на Flask/Django, либо не на Python, из-за чего пришлось написать быстренько самому на Python.


.. code-block:: python

    #!/usr/bin/env python
    import os
    import sys
    import json
    import time
    import subprocess
    import functools
    import BaseHTTPServer

    BASE_PATH = os.path.realpath(os.path.dirname(__file__))
    UPDATE_REPO_PATH = os.path.realpath(os.path.join(BASE_PATH, 'test_repo'))

    HOST_NAME = '0.0.0.0'
    PORT_NUMBER = int(sys.argv[1]) if len(sys.argv) == 2 else 8000

    def update_repo(payload, path):
        os.chdir(path)
        if payload['ref'] == 'refs/heads/master':
            out = subprocess.check_output(['git', 'pull', 'origin', 'master'])
        else:
            print 'Skip update because push not to master: %s' % payload['ref']


    REPO_HANDLERS = {
        'Username/test_repo': functools.partial(update_repo, path=UPDATE_REPO_PATH),
    }


    class HookHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        server_version = "GitHubWebHookHandler/0.1"

        def do_GET(s):
            s.send_response(200)
            s.wfile.write('WAT!?')

        def do_POST(s):
            length = int(s.headers['Content-Length'])
            data = s.rfile.read(length).decode('utf-8')
            post_data = json.loads(data)
            repository = post_data['repository']['full_name']

            meth = REPO_HANDLERS.get(repository, None)

            if meth:
                meth(post_data)

            s.send_response(200)


    if __name__ == '__main__':
        server_class = BaseHTTPServer.HTTPServer
        httpd = server_class((HOST_NAME, PORT_NUMBER), HookHandler)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()


Итак, данный код делает следующее:

#. Висит либо на 8000 порту, либо который укажете и слушает POST запросы

#. Если получил POST запрос, то достает из него полное имя репозитория

#. Затем проверяет, может ли он такое имя обработать (проверяя REPO_HANDLERS) и если да, то вызывает ту функцию

#. А функция, всего лишь заходит в указаную папку и делает git pull origin master и все.


У меня такая система обновляет 3 репозитория. Надеюсь, кому-нибудь пригодится