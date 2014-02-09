#!/usr/bin/env python
# -*- coding: utf-8 -*- #
SITENAME = u'The Chicago GNU/Linux User Group'
SITEURL  = u'https://chicagolug.org'
RELATIVE_URLS = (True)
THEME = './korgi'
DEFAULT_PAGINATION = 10

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = u'en'

DATE_FORMATS = {
        u'en': u'%Y-%m-%d',
    }

DEFAULT_DATE = ('fs')
FILENAME_METADATA = u'.*(?P<date>\d{4}-\d{2}-\d{2}).*'

#ARTICLE_URL = u'posts/{date:%Y}-{date:%m}-{date:%d}/{slug}.html'
#ARTICLE_SAVE_AS = u'posts/{date:%Y}-{date:%m}-{date:%d}/{slug}.html'

# Dirs to always push to site
STATIC_PATHS = (['corporate', 'images'])

import sys
sys.path.append('./')

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


