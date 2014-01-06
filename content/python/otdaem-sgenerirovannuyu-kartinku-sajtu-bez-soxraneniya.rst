Отдаем сгенерированную картинку сайту без сохранения
####################################################
:date: 2009-01-26 01:00
:author: gigimon
:category: Python
:tags: Django, javascript, pil, Python
:slug: otdaem-sgenerirovannuyu-kartinku-sajtu-bez-soxraneniya

Хочу рассказать немного про генерацию картинок и их отдачу на лету, с
помощью 1 примера, где надо было генерирвоать по полученым параметрам
(от js) картинку и отдавать ее - эта картинка становилась фоном. Если о
генерации ее вопросов не было, появился вопрос о том, как ее отдать. На
1 англйиском сайте нашел простео объяснение, что можно отдавать в
request. И так, пример:
В html страничке, делаем такой скрипт:

.. code-block:: javascript


          var height = innerHeight;
          var width = innerWidth;
          document.body.background = "/utils/genback/?width="+width+"&height="+height;
          document.body.style.backgroundAttachment = 'fixed';
          document.body.style.backgroundPosition = 'right center'; 

Он узнает размера окна браузера и передает их скрипту по
адресу /utils/genback/?width="+width+"&height="+height;  с помощью GET
запроса. В ответ получает картинку и устанавливает ее фоном. На стороне
сервера имеем вот такой скрипт:
/utils/genback/?width="+width+"&height="+height;

На стороне сервера у нас такой скрипт:

.. code-block:: python

    #-*-coding:utf8-*-
    from PIL import Image, ImageDraw
    from django.http import HttpResponse

    def generation_background(request):
        if request.method == 'GET':
            screen_width = int(request.GET['width'])
            screen_height = int(request.GET['height'])
        else:
            screen_width = 1024
            screen_height = 768
        COLOR = (240, 239, 239, 128)
        image = Image.new("RGBA", (screen_width, screen_height), (0,0,0,0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((100, -10, 100+screen_width, -30+screen_width), fill=COLOR, outline=COLOR)
        del draw
        response = HttpResponse(mimetype="image/png")
        image.save(response, 'PNG')
        return response

Данный скрипт, получает из GET запроса размеры, генерирует по ним фон
(круг), устанавливает тип запроса image/png:  response =
HttpResponse(mimetype="image/png"),  сохраняет картинку в request и
возвращает ее.

Конечно специалисты и так знают, а новичкам в django будет помощь :)
