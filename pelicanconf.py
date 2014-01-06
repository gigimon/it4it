#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'gigimon'
SITENAME = u"блог gigimon'а"
SITEURL = 'http://it4it.ru'

TIMEZONE = 'Europe/Simferopol'
LOCALE = ('ru_RU')
DEFAULT_LANG = u'ru'

DATE_FORMATS = {u'ru': '%H:%M %d %B %Y'}
DEFAULT_DATE_FORMAT = '%H:%M %d %B %Y'

DEFAULT_CATEGORY = "misc"
DEFAULT_PAGINATION = 10

PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'
TAGS_URL = 'tags/'
TAGS_SAVE_AS = 'tags/index.html'

CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'

AUTHOR_URL = 'author/'
AUTHOR_SAVE_AS = 'author/{slug}/index.html'

PATH = "content"
OUTPUT_PATH = "site"

STATIC_PATHS = ['images', 'files', 'extra/robots.txt']
EXTRA_PATH_METADATA = {'extra/robots.txt': {'path': 'robots.txt'},}

ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'

SUMMARY_MAX_LENGTH = 150

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/rss.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
TRANSLATION_FEED_ATOM = None

TYPOGRIFY = True
PYGMENTS_RST_OPTIONS = {'classprefix': 'pgcss', 'linenos': 'table'}

# THEME = 'tuxlite_tbs'

# Blogroll
# LINKS =  (
# 	('RSS', 'http://it4it.ru/feeds/rss.xml'),
# )

# Social widget
# SOCIAL = (
# 	(u'Почта', 'gigimon4ik@gmail.com'),
# 	('Linkedin', 'http://www.linkedin.com/pub/oleg-suharev/44/936/411')
# )

DISQUS_SITENAME = 'it4it'
GOOGLE_ANALYTICS = 'UA-5586227-1'

TWITTER_USERNAME = 'gigimon'
GITHUB_URL = 'https://github.com/gigimon'

PLUGIN_PATH = 'plugins'

PLUGINS = [
    'youtube',
    'vimeo',
    'sitemap'
]

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}
