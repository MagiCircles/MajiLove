import time, datetime
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings as django_settings
from magi.tools import totalDonators, getStaffConfigurations
from majilove import models

def generate_settings():

    print 'Get total donators'
    total_donators = totalDonators()

    print 'Get staff configurations'
    staff_configurations, latest_news = getStaffConfigurations()

    print 'Get the latest news'
    now = timezone.now()
    # get events, gachas, etc, then:
    # latest_news.append({
    #     'title': unicode(event.t_name),
    #     'image': image,
    #     'url': event.item_url,
    #     'hide_title': True,
    #     'ajax': event.ajax_item_url,
    # })

    print 'Get the characters'
    favorite_characters = []
    all_idols = models.Idol.objects.all().order_by('name')
    favorite_characters = [
        (idol.pk, idol.name, idol.image_url) 
    for idol in all_idols]
    
    print 'Get the colors'
    user_colors = []
    user_colors = [
        (idol.name.replace(' ', ''), idol.t_name, idol.name.replace(' ', ''), idol.color)
    for idol in all_idols]

    print 'Save generated settings'
    # STARTERS = ' + unicode(starters) + u'\n\
    s = u'\
# -*- coding: utf-8 -*-\n\
import datetime\n\
LATEST_NEWS = ' + unicode(latest_news) + u'\n\
TOTAL_DONATORS = ' + unicode(total_donators) + u'\n\
STAFF_CONFIGURATIONS = ' + unicode(staff_configurations) + u'\n\
FAVORITE_CHARACTERS = ' + unicode(favorite_characters) + u'\n\
USER_COLORS = ' + unicode(user_colors) + u'\n\
GENERATED_DATE = datetime.datetime.fromtimestamp(' + unicode(time.time()) + u')\n\
'
    print s
    with open(django_settings.BASE_DIR + '/' + django_settings.SITE + '_project/generated_settings.py', 'w') as f:
        f.write(s.encode('utf8'))
        f.close()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        generate_settings()
