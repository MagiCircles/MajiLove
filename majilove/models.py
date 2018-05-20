from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from django.db import models
from django.conf import settings as django_settings
from magi.models import User, uploadItem
from magi.item_model import MagiModel, i_choices
from magi.abstract_models import BaseAccount


############################################################
# Utility stuff

LANGUAGES_NEED_OWN_NAME = [ l for l in django_settings.LANGUAGES if l[0] in ['ru', 'zh-hans', 'zh-hant', 'kr'] ]
LANGUAGES_NEED_OWN_NAME_KEYS = [ l[0] for l in django_settings.LANGUAGES if l[0] in ['ru', 'zh-hans', 'zh-hant', 'kr'] ]
LANGUAGES_DIFFERENT_CHARSET = [ l for l in django_settings.LANGUAGES if l[0] in ['ja', 'ru', 'zh-hans', 'zh-hant', 'kr'] ]
LANGUAGES_DIFFERENT_CHARSET_KEYS = [ l[0] for l in django_settings.LANGUAGES if l[0] in ['ja', 'ru', 'zh-hans', 'zh-hant', 'kr'] ]
ALL_ALT_LANGUAGES = [ l for l in django_settings.LANGUAGES if l[0] != 'en' ]
ALL_ALT_LANGUAGES_KEYS = [ l[0] for l in django_settings.LANGUAGES if l[0] != 'en' ]
ALT_LANGUAGES_EXCEPT_JP = [ l for l in django_settings.LANGUAGES if l[0] not in ['en', 'ja'] ]
ALT_LANGUAGES_EXCEPT_JP_KEYS = [ l[0] for l in django_settings.LANGUAGES if l[0] not in ['en', 'ja'] ]



class Account(BaseAccount):
    class Meta:
        pass

############################################################
# Idols

class Idol(MagiModel):
    collection_name = 'idol'

    owner = models.ForeignKey(User, related_name='added_idols')

    name = models.CharField(string_concat(_('Name'), ' (', _('Romaji'), ')'), max_length=100, unique=True)

    japanese_name = models.CharField(string_concat(_('Name'), ' (', _('Japanese'), ')'), max_length = 100, unique=True)

    NAMES_CHOICES = LANGUAGES_NEED_OWN_NAME
    d_names = models.TextField(_('Name'), null=True)

    @property
    def t_name(self):
        if get_language() == 'ja':
            return self.japanese_name
        return self.names.get(get_language(), self.name)

    romaji_CV = models.CharField(_('CV'), help_text='In romaji', max_length=100, null=True)

    CV = models.CharField(string_concat(_('CV'), ' (', _('Japanese'), ')'), help_text='In Japanese characters.', max_length=100, null=True)

    bio = models.TextField(_('Bio'), max_length=1000)

    # in cm
    height = models.PositiveIntegerField(_('Height'), null=True)

    weight = models.PositiveIntegerField(_('Weight'), null=True)

    @property
    def display_weight(self):
        if self.weight: return self.weight
        return '?' # this is how Ai's weight is displayed in game

    BLOOD_CHOICES = (
        'O',
        'A',
        'B',
        'AB',
        '?'
    )

    i_blood_type = models.PositiveIntegerField(_('Blood Type'), choices=i_choices(BLOOD_CHOICES), null=True)

    birthday = models.DateField(_('Birthday'), null=True, help_text='The year is not used, so write whatever')

    star_sign = models.CharField(_('Astrological Sign'), max_length=100, null=True)

    instrument = models.CharField(_('Instrument'), max_length=100, null=True)

    hometown = models.CharField(_('Hometown'), max_length=100, null=True)

    image = models.ImageField(_('Image'), upload_to=uploadItem('idol'))

    small_image = models.ImageField(_('Image'), upload_to=uploadItem('idol/small'))

    def __unicode__(self):
        return unicode(self.t_name)
