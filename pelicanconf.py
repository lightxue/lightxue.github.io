#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Light Xue'
SITENAME = '0xFEE1C001'
SITESUBTITLE = 'Where there is a shell, there is a way'
SITEURL = 'http://www.lightxue.com'
DESCRIPTION = '这是个兴趣使然的技术博客。0xFEE1C001是feel cool的hexspeak。主题包括但不限于操作系统、编程语言、数据库、算法、工具。心血来潮才会动手写一篇。渴望能和更多的人交流，欢迎留言、邮件分享你的见解。'

PATH = 'content'
STATIC_PATHS = [
    'images',
    'extra/robots.txt',
    'extra/favicon.png',
    'extra/CNAME',
    'extra/google-search-console.txt',
]
EXTRA_PATH_METADATA = {
    'extra/robots.txt':  {'path': 'robots.txt'},
    'extra/favicon.png': {'path': 'favicon.png'},
    'extra/CNAME': {'path': 'CNAME'},
    'extra/google-search-console.txt': {'path': 'google17d8cb936a6462eb.html'},
}

DEFAULT_DATE_FORMAT = '%Y-%m-%d'
TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh'

SEARCH_BOX = False
SEARCH_SITE = 'lightxue.com'

MENUITEMS = (
    ('首页', '/'),
    ('程序员工具', 'http://tools.lightxue.com'),
    ('关于', '/about-me'),
)
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

ARTICLE_URL      = '{slug}'
ARTICLE_SAVE_AS  = '{slug}.html'
DRAFT_URL        = 'drafts/{slug}'
DRAFT_SAVE_AS    = 'drafts/{slug}.html'
PAGE_URL         = '{slug}'
PAGE_SAVE_AS     = '{slug}.html'
CATEGORY_URL     = 'category/{slug}'
CATEGORY_SAVE_AS = 'category/{slug}.html'
TAG_URL          = 'tag/{slug}'
TAG_SAVE_AS      = 'tag/{slug}.html'
AUTHOR_URL       = 'author/{slug}'
AUTHOR_SAVE_AS   = 'author/{slug}.html'

# Feed generation is usually not desired when developing
FEED_DOMAIN = ''
FEED_ATOM = 'feeds/atom.xml'
#CATEGORY_FEED_ATOM = None
#TRANSLATION_FEED_ATOM = None
#AUTHOR_FEED_ATOM = None
#AUTHOR_FEED_RSS = None

THEME = 'themes/octopress'

DEFAULT_CATEGORY = 'Other'

# Blogroll
LINKS = ()
#LINKS = (('Pelican', 'http://getpelican.com/'),
         #('Python.org', 'http://python.org/'),
         #('Jinja2', 'http://jinja.pocoo.org/'),
         #('You can modify those links in your config file', '#'),)

SOCIAL = ()
# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
          #('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
#DISQUS_SITENAME = '0xfee1c00l'

PLUGIN_PATHS = ['plugins']
PLUGINS = [
    'summary',
    #'render_math',
    'jsmath',
    'better_codeblock_line_numbering',
]

SUMMARY_END_MARKER = '<!-- more -->'

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'linenums': False,
        },
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}

MATH_JAX = {
    'source': '"//cdn.bootcss.com/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML"'
}

BAIDU_ANALYTICS = '8a9edae11717cd734925510200712026'
GOOGLE_ANALYTICS = 'UA-42436465-3'

GITHUB_ID = 'lightxue'
GITMENT_REPO = 'lightxue.github.io'
GITMENT_ID = 'cfbdea1160f74d535db2'
GITMENT_SECRET = '5616e795360075c1d526671e6b272f3da57ac501'
