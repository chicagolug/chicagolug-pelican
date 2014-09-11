#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import sys
from docutils.parsers.rst import directives, Directive
sys.path.append('./')

#Initial Settings
DATE_FORMATS = {
        u'en': u'%A %B %d, %Y, at %I:%M %p',
    }
DEFAULT_DATE = ('fs')
DEFAULT_LANG = u'en'
DEFAULT_PAGINATION = 6
SUMMARY_MAX_LENGTH = (2000)
DISPLAY_PAGES_ON_MENU = (False)
FILENAME_METADATA = u'.*(?P<date>\d{4}-\d{2}-\d{2}).*'
SITENAME = u'The Chicago GNU/Linux User Group'
SITEURL  = 'http://chicagolug.org'
THEME = './korgi'
TIMEZONE = 'America/Chicago'
DELETE_OUTPUT_DIRECTORY = (True)

#Path Configs
RELATIVE_URLS = (True)
RESPONSIVE_IMAGES = (True)
STATIC_PATHS = (['images', 'static', 'source'])
MENUITEMS = (('Media', 'http://media.chicagolug.org'),)

FEED_DOMAIN = ('http://chicagolug.org')
TAG_FEED_ATOM = (None)
FEED_MAX_ITEMS = 100

#Tag Cloud
TAG_CLOUD_STEPS = (4)
TAG_CLOUD_MAX_ITEMS = (100)

#Plugin Configs
PLUGIN_PATH = 'plugins'
PLUGINS = ['html_rst_directive', 'better_figures_and_images', 'pin_to_top']

# Blogroll
LINKS =  (
    ('Discussion List', 'http://lists.chicagolug.org/cgi-bin/mailman/listinfo/discuss'),
    ('Announcement List', 'http://lists.chicagolug.org/cgi-bin/mailman/listinfo/announce'),
    ('Identi.ca', 'https://identi.ca/chicagolug'),
    ('Twitter', 'https://twitter.com/chicagolug'),
    ('Meetup.com', 'http://www.meetup.com/Windy-City-Linux-Users-Group/'),
    ('Google+', 'https://plus.google.com/b/110920643277848720575/110920643277848720575/posts'),
)
