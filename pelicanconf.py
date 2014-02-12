#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import sys
from docutils.parsers.rst import directives, Directive
sys.path.append('./')

#Initial Settings
DATE_FORMATS = {
        u'en': u'%Y-%m-%d',
    }
DEFAULT_DATE = ('fs')
DEFAULT_LANG = u'en'
DEFAULT_PAGINATION = 10
DISPLAY_PAGES_ON_MENU = (False)
FILENAME_METADATA = u'.*(?P<date>\d{4}-\d{2}-\d{2}).*'
SITENAME = u'Chicago GNU/Linux User Group'
# SITEURL  = u'http://localhost:8000'
SITEURL  = u'http://chicagolug.org'
THEME = './korgi'
TIMEZONE = 'America/Chicago'

#Path Configs
RELATIVE_URLS = (True)
#RELATIVE_URLS = (False)
RESPONSIVE_IMAGES = (True)
STATIC_PATHS = (['corporate', 'images', 'static'])

#Plugin Configs
PLUGIN_PATH = 'plugins'
PLUGINS = ['html_rst_directive', 'better_figures_and_images']

# Blogroll
LINKS =  (
    ('Cgit', 'https://git.kernel.org/'),
    ('Wikis', 'https://www.wiki.kernel.org/'),
    ('Bugzilla', 'https://bugzilla.kernel.org/'),
    ('Patchwork', 'https://patchwork.kernel.org/'),
    ('Kernel Mailing Lists', 'http://vger.kernel.org/'),
    ('Mirrors', 'http://mirrors.kernel.org/'),
    ('Linux.com', 'http://www.linux.com/'),
    ('Linux Foundation', 'http://www.linuxfoundation.org/'),
    ('Kernel Planet', 'http://planet.kernel.org/'),
)

# Social widget
SOCIAL = (
    ('ChicagoLUG on Google+', 'https://plus.google.com/110920643277848720575/posts'),
)

# Commented config options
#ARTICLE_URL = u'posts/{date:%Y}-{date:%m}-{date:%d}/{slug}.html'
#ARTICLE_SAVE_AS = u'posts/{date:%Y}-{date:%m}-{date:%d}/{slug}.html'
