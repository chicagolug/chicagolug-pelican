#!/usr/bin/env python
# -*- coding: utf-8 -*- #
SITENAME = u'The Linux Kernel Archives'
SITEURL  = u'https://www.kernel.org'

TIMEZONE = 'UTC'

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
from plugins import releases

LONGTERM_KERNELS = ('3.4', '3.2', '3.0', '2.6.34', '2.6.32')
EOL_KERNELS = ('3.5', '3.6', '3.7', '3.8', '3.9')

GIT_MAINLINE = '/mnt/pub/scm/linux/kernel/git/torvalds/linux.git'
GIT_STABLE   = '/mnt/pub/scm/linux/kernel/git/stable/linux-stable.git'
GIT_NEXT     = '/mnt/pub/scm/linux/kernel/git/next/linux-next.git'

PUB_MOUNT = '/mnt'

PLUGINS = [releases]

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
    ('Linux on Google+', 'https://plus.google.com/+Linux/posts'),
)

THEME = './korgi'
DEFAULT_PAGINATION = 10
