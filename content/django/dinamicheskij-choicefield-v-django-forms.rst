Динамический ChoiceField в Django forms
#######################################
:date: 2012-08-08 21:20
:author: gigimon
:category: Django
:tags: choicefield, Django, forms
:slug: dinamicheskij-choicefield-v-django-forms

Достаточно часто у новичков возникает вопрос, а как сделать ChoiceField
динамическим? Существует несколько способов, зависящих от того, какие
данные вы хотите туда подставлять. Стандартными средставми форм можно
подставлять данные из других моделей (из queryset). Для этого, надо
исопльзовать ModelChoiceField и параметр queryset, для примера:

.. code-block:: python

    class PostForm(forms.Form):
        month = forms.ModelChoiceField(queryset=Month.objects.all())

Более подробно про такой способ описано в документации `здесь`_

В этой же статье, я расскажу про заполнение данными, если они берутся не
из базы, а откуда либо еще, либо если требуется какие-то фильтры.

Итак, для примера, у нас есть модель Post, при добавлении которой через
форму, требуется выбрать рубрику,название которых хранится в настройках
(в settings.py).

.. code-block:: python

    class Post(models.Model):
        description = models.TextField()
        category = models.CharField(max_length=255)

Создадим для нее форму:

.. code-block:: python

    class PostForm(forms.ModelForm):
        class Meta:
            model = Post
            widgets = {'category': forms.CheckboxSelectMultiple, }

Если выведем эту форму, то увидим, что category не предоставляет
ниодного пункта выбора.

Для того, чтобы заполнить категории, нам требуется у формы
переопределить метод \_\_init\_\_ и именно в нем вставлять в поле
варианты.

.. code-block:: python

    class PostForm(forms.ModelForm):
        class Meta:
            model = Post
            widgets = {'category': forms.CheckboxSelectMultiple, }
        def __init__(self, *args, **kwargs):
            super(PostForm, self).__init__(*args, **kwargs)
            self.fields['category'].choices = (('audio','Audio'),('video','Video'))

Теперь же, если вывести форму, то увидим, что можно выбрать между Audio
и Video категориями.

.. _здесь: https://docs.djangoproject.com/en/1.4/ref/forms/fields/#django.forms.ModelChoiceField
