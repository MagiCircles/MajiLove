# -*- coding: utf-8 -*-
from django.conf import settings as django_settings
from majilove import models

# Configure and personalize your website here.

SITE_NAME = 'Maji Love'
SITE_URL = 'http://maji.love/'
SITE_IMAGE = 'majilove.png'
SITE_STATIC_URL = '//localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else '//i.majilove.com/'
GAME_NAME = u'Utano☆Princesama Shining Live'
DISQUS_SHORTNAME = 'majilove'
ACCOUNT_MODEL = models.Account
COLOR = '#158399'
