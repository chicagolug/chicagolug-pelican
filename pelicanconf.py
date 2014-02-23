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
DEFAULT_PAGINATION = 6
SUMMARY_MAX_LENGTH = (2000)
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

FEED_DOMAIN = ('http://chicagolug.org')
TAG_FEED_ATOM = (None)
FEED_MAX_ITEMS = 100

#Plugin Configs
PLUGIN_PATH = 'plugins'
PLUGINS = ['html_rst_directive', 'better_figures_and_images']

# Blogroll
LINKS =  (
    ('Mailing List', 'http://groups.google.com/group/chicagolinux-discuss'),
    ('Identi.ca', 'https://identi.ca/chicagolug'),
    ('Twitter', 'https://twitter.com/chicagolug'),
    ('Meetup.com', 'http://www.meetup.com/Windy-City-Linux-Users-Group/'),
    ('Google+', 'https://plus.google.com/b/110920643277848720575/110920643277848720575/posts'),
)

# Social widget
SOCIAL = (
)

# Commented config options
#ARTICLE_URL = u'posts/{date:%Y}-{date:%m}-{date:%d}/{slug}.html'
#ARTICLE_SAVE_AS = u'posts/{date:%Y}-{date:%m}-{date:%d}/{slug}.html'
