#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Thomas'
AUTHOR_HOME = 'https://github.com/tym-oao'
SITENAME = 'TYM engineering notes'
SITEURL = 'http://devblog.ty-m.xyz'
RELATIVE_URLS = True

FEED_ALL_ATOM = 'feeds/all.atom.xml'

PATH = 'content'

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = 'en'
THEME = 'mfb'
# # Feed generation is usually not desired when developing
# FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


DEFAULT_PAGINATION = 7

PYGMENTS_STYLE = 'solarizeddark'
CC_LICENSE = "CC-BY-SA"
USE_PAGER = True
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
HIDE_SIDEBAR = True
# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
STATIC_PATHS = ['things']
EXTRA_PATH_METADATA = {
    'things/CNAME': {'path': 'CNAME'},
    'things/LICENSE': {'path': 'LICENSE'},
    'things/README': {'path': 'README.md'},
    'things/.gitignore': {'path': '.gitignore'},
}
PLUGINS = ['pelican_gist']
