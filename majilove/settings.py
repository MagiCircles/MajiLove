# -*- coding: utf-8 -*-
import datetime, pytz
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _
from magi.default_settings import DEFAULT_ENABLED_PAGES
from magi.utils import tourldash
from majilove import models

############################################################
# General settings

SITE_NAME = 'Maji Love'
SITE_URL = 'http://maji.love/'
SITE_IMAGE = 'majilove_collection.png'
SITE_LOGO = 'majilove.png'
EMAIL_IMAGE = 'majilove_collection_full.png'
EMPTY_IMAGE = 'emptyicon.jpg'
DONATE_IMAGE = 'donate.png'
SITE_NAV_LOGO = 'majilove_title_white.png'
SITE_STATIC_URL = '//localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else '//i.maji.love/'
ACCOUNT_MODEL = models.Account
COLOR = '#5acccd'

############################################################
# Game

GAME_NAME = u'Utano☆Princesama Shining Live'
GAME_URL = 'https://www.utapri-shining-live.com/en/'

############################################################
# Enabled pages

ENABLED_PAGES = DEFAULT_ENABLED_PAGES
ENABLED_PAGES['index']['enabled'] = True

############################################################
# Social

TWITTER_HANDLE = "MajiLoveCollect"
HASHTAGS = ['シャニライ', 'ShiningLive']
GITHUB_REPOSITORY = ('MagiCircles', 'MajiLove')

############################################################
# User preferences and profiles

FAVORITE_CHARACTER_NAME = _('Idol')
FAVORITE_CHARACTER_TO_URL = lambda link: (u'/idol/{pk}/'.format(pk=link.raw_value))

############################################################
# Donations

DONATORS_STATUS_CHOICES = (
    ('THANKS', 'Thanks'),
    ('SUPPORTER', _('Shining Student')),
    ('LOVER', _('Shining Master Course')),
    ('AMBASSADOR', _('Shining Idol')),
    ('PRODUCER', _('Shining Super Star')),
    ('DEVOTEE', _('Shining Saotome')),
)

############################################################
# Prelaunch details

LAUNCH_DATE = True

############################################################
# Technical details

GOOGLE_ANALYTICS = 'UA-118452679-1'
DISQUS_SHORTNAME = 'maji-love'

############################################################
# Generated settings

TOTAL_DONATORS = getattr(django_settings, 'TOTAL_DONATORS', None)
LATEST_NEWS = getattr(django_settings, "LATEST_NEWS", None)
STAFF_CONFIGURATIONS = getattr(django_settings, "STAFF_CONFIGURATIONS", None)
FAVORITE_CHARACTERS = getattr(django_settings, 'FAVORITE_CHARACTERS', None)
USER_COLORS = getattr(django_settings, 'USER_COLORS', None)