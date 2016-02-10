#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'gigimon'
SITENAME = u"Блог gigimon'а"

TIMEZONE = 'Europe/Simferopol'
LOCALE = ('ru_RU')
DEFAULT_LANG = u'ru'

DATE_FORMATS = {u'ru': '%d %B %Y'}
DEFAULT_DATE_FORMAT = '%d %B %Y'

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
# PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

THEME = 'theme/'

DISQUS_SITENAME = 'it4it'
GOOGLE_ANALYTICS = 'UA-5586227-1'

TWITTER_USERNAME = 'gigimon'

WITH_FUTURE_DATES = True

LINKEDIN_URL = 'http://ua.linkedin.com/pub/oleg-suharev/44/936/411'
GITHUB_URL = 'https://github.com/gigimon'

PLUGIN_PATHS = ['plugins']

PLUGINS = [
    'youtube',
    'vimeo',
    'extended_sitemap'
]

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.8,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}
