# -*- coding: utf-8 -*-
import datetime, pytz
from django.conf import settings as django_settings
from magi.default_settings import DEFAULT_ENABLED_PAGES
from majilove import models

############################################################
# General settings

SITE_NAME = 'Maji Love'
SITE_URL = 'http://maji.love/'
SITE_IMAGE = 'majilove.png'
SITE_STATIC_URL = '//localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else '//i.majilove.com/'
GAME_NAME = u'Utano☆Princesama Shining Live'
DISQUS_SHORTNAME = 'majilove'
ACCOUNT_MODEL = models.Account
COLOR = '#158399'

############################################################
# Enabled pages

ENABLED_PAGES = DEFAULT_ENABLED_PAGES
ENABLED_PAGES['index']['enabled'] = True

############################################################
# Social

TWITTER_HANDLE = "MajiLoveCollect"

############################################################
# Prelaunch details

LAUNCH_DATE = datetime.datetime(2019, 8, 1, 12, 0, 0, tzinfo=pytz.UTC)
