from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings as django_settings
from magi.models import User, uploadItem
from magi.item_model import MagiModel, i_choices
from magi.abstract_models import BaseAccount


############################################################
# Utility stuff

LANGUAGES_NEED_OWN_NAME = [ l for l in django_settings.LANGUAGES if l[0] in ['ru', 'zh-hans', 'zh-hant', 'kr'] ]
ALL_ALT_LANGUAGES = [ l for l in django_settings.LANGUAGES if l[0] != 'en' ]



class Account(BaseAccount):
    class Meta:
        pass

############################################################
# Idols

class Idol(MagiModel):
    collection_name = 'idol'

    owner = models.ForeignKey(User, related_name='added_idols')

    name = models.CharField(string_concat(_('Name'), ' (', _('Romaji'), ')'), max_length=100, unique=True)

    japanese_name = models.CharField(string_concat(_('Name'), ' (', _('Japanese'), ')'), max_length=100, unique=True)

    NAMES_CHOICES = LANGUAGES_NEED_OWN_NAME
    d_names = models.TextField(_('Name'), null=True)

    @property
    def t_name(self):
        if get_language() == 'ja':
            return self.japanese_name
        return self.names.get(get_language(), self.name)

    romaji_voice_actor_name = models.CharField(_('Voice actor'), help_text='In romaji', max_length=100, null=True)

    voice_actor_name = models.CharField(string_concat(_('Voice actor'), ' (', _('Japanese'), ')'), help_text='In Japanese characters.', max_length=100, null=True)

    description = models.TextField(_('Description'), max_length=1000, null=True)
    DESCRIPTIONS_CHOICES = ALL_ALT_LANGUAGES
    d_descriptions = models.TextField(_('Description'), null=True)

    # in cm
    height = models.PositiveIntegerField(_('Height'), null=True)

    weight = models.PositiveIntegerField(_('Weight'), null=True)

    @property
    def display_weight(self):
        return self.weight or '?'

    BLOOD_TYPE_CHOICES = (
        'O',
        'A',
        'B',
        'AB',
    )

    i_blood_type = models.PositiveIntegerField(_('Blood Type'), choices=i_choices(BLOOD_TYPE_CHOICES), null=True)

    @property
    def display_blood_type(self):
        return self.blood_type or '?'

    birthday = models.DateField(_('Birthday'), null=True, help_text='The year is not used, so write whatever')

    ASTROLOGICAL_SIGN_CHOICES = (
        ('Leo', _('Leo')),
        ('Aries', _('Aries')),
        ('Libra', _('Libra')),
        ('Virgo', _('Virgo')),
        ('Scorpio', _('Scorpio')),
        ('Capricorn', _('Capricorn')),
        ('Pisces', _('Pisces')),
        ('Gemini', _('Gemini')),
        ('Cancer', _('Cancer')),
        ('Sagittarius', _('Sagittarius')),
        ('Aquarius', _('Aquarius')),
        ('Taurus', _('Taurus')),
    )

    i_astrological_sign = models.PositiveIntegerField(_('Astrological Sign'), choices=i_choices(ASTROLOGICAL_SIGN_CHOICES), null=True)

    instrument = models.CharField(_('Instrument'), max_length=100, null=True)
    INSTRUMENTS_CHOICES = ALL_ALT_LANGUAGES
    d_instruments = models.TextField(_('Instrument'), null=True)

    hometown = models.CharField(_('Hometown'), max_length=100, null=True)
    HOMETOWNS_CHOICES = LANGUAGES_NEED_OWN_NAME
    d_hometowns = models.TextField(_('Hometown'), null=True)

    hobby = models.CharField(_('Hobby'), max_length=100, null=True)
    HOBBYS_CHOICES = ALL_ALT_LANGUAGES
    d_hobbys = models.TextField(_('Hobby'), null=True)

    image = models.ImageField(_('Image'), upload_to=uploadItem('idol'))

    small_image = models.ImageField(_('Image'), upload_to=uploadItem('idol/small'))

    def __unicode__(self):
        return unicode(self.t_name)


############################################################
# Songs

class Song(MagiModel):
    collection_name = 'song'
    owner = models.ForeignKey(User, related_name='added_songs')

    DIFFICULTY_VALIDATORS = [
        MinValueValidator(1),
        MaxValueValidator(13),
    ]

    name = models.CharField(string_concat(_('Title'), ' (', _('Translation'), ')'), max_length=100, null=True)
    japanese_name = models.CharField(_('Title'), max_length=100, null=True)
    NAMES_CHOICES = ALL_ALT_LANGUAGES
    d_names = models.TextField(_('Title'), null=True)
    @property
    def t_name(self):
        if get_language() == 'ja': return self.japanese_name
        return self.names.get(get_language(), self.name)

    image = models.ImageField('Album cover', upload_to=uploadItem('song'), null=True)

    composer = models.CharField(_('Composer'), max_length=100, null=True)
    COMPOSERS_CHOICES = LANGUAGES_NEED_OWN_NAME
    d_composers = models.TextField(_('Composer'), null=True)
    lyricist = models.CharField(_('Lyricist'), max_length=100, null=True)
    LYRICISTS_CHOICES = LANGUAGES_NEED_OWN_NAME
    d_lyricists = models.TextField(_('Lyricist'), null=True)
    arranger = models.CharField(_('Arranger'), max_length=100, null=True)
    ARRANGERS_CHOICES = LANGUAGES_NEED_OWN_NAME
    d_arrangers = models.TextField(_('Arranger'), null=True)

    singers = models.ManyToManyField(Idol, related_name="sung_songs", verbose_name=_('Singers'))

    # TODO: whichever of photo or song goes in second should take this from the other
    COLORS= OrderedDict([
        (1, { # yellow
            'translation': _('Star'),
            'english': u'Star'
        }),
        (2, { # red
            'translation': _('Shine'),
            'english': u'Shine'
        }),
        (3, { # blue
            'translation': _('Dream'),
            'english': u'Dream'
        })
    ])

    COLOR_CHOICES = [(_name, _info['translation']) for _name, _info in COLORS.items()]
    COLOR_WITHOUT_I_CHOICES=True
    i_color = models.PositiveIntegerField(_('Color'), choices=i_choices(COLOR_CHOICES))

    easy_notes = models.PositiveIntegerField(string_concat(_('Easy'), ' - ', _('Notes')), null=True)
    easy_difficulty = models.PositiveIntegerField(string_concat(_('Easy'), ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    normal_notes = models.PositiveIntegerField(string_concat(_('Normal'), ' - ', _('Notes')), null=True)
    normal_difficulty = models.PositiveIntegerField(string_concat(_('Normal'), ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    hard_notes = models.PositiveIntegerField(string_concat(_('Hard'), ' - ', _('Notes')), null=True)
    hard_difficulty = models.PositiveIntegerField(string_concat(_('Hard'), ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    pro_notes = models.PositiveIntegerField(string_concat(_('Pro'), ' - ', _('Notes')), null=True)
    pro_difficulty = models.PositiveIntegerField(string_concat(_('Pro'), ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)

    length = models.PositiveIntegerField(_('Length'), null=True)

    #TODO: unlock method

    def __unicode__(self):
        return unicode(self.t_name)