#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Ankur Ankan'
SITENAME = 'Bayesian Learning, Python and Random Thoughts'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = './theme/'
# ABOUT_PAGE = '/pages/about.html'
TWITTER_USERNAME = 'AnkurAnkan'
GITHUB_USERNAME = 'ankurankan'
STACKOVERFLOW_ADDRESS = 'http://stackoverflow.com/users/2937831/jakevdp'
AUTHOR_BLOG = 'http://ankurankan.github.io'
SHOW_ARCHIVES = True
SHOW_FEED = True  # Need to address large feeds

ENABLE_MATHJAX = True
