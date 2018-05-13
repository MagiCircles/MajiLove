from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from django.db import models
from magi.item_model import MagiModel, i_choices
from magi.abstract_models import AccountAsOwnerModel, BaseAccount
from magi.models import uploadItem

# Create your models here.

############################################################
# Idols

class Idol(MagiModel):
    collection_name = 'idol'

    # mostly copying the name stuff from the bandori.party code
    name = models.CharField(string_concat(_('Name'), ' (', _('Romaji'), ')'), max_length=100, unique=True)

    japanese_name = models.CharField(string_concat(_('Name'), ' (', _('Japanese'), ')'), max_length = 100, unique=True)

    # not entirely sure what this part is for
    d_names = models.TextField(_('Name'), null=True)

    @property
    def t_name(self):
        if get_language() == 'ja':
            return self.japanese_name
        return self.name

    romaji_CV = models.CharField(_('CV'), help_text='In romaji', max_length=100)

    CV = models.CharField(string_concat(_('CV'), ' (', _('Japanese'), ')'), help_text='In Japanese characters.', max_length=100)

    bio = models.TextField(_('Bio'), max_length=1000)

    # in cm
    height = models.PositiveIntegerField(_('Height'), null=True, default=None)

    # in kg, need to figure out how to display for Ai
    weight = models.PositiveIntegerField(_('Weight'), null=True, blank=True)

    BLOOD_CHOICES = (
        'O',
        'A',
        'B',
        'AB',
        '?'
        )

    blood_type = models.PositiveIntegerField(_('Blood Type'), choices=i_choices(BLOOD_CHOICES), null=True)

    birthday = models.DateField(_('Birthday'), null=True, help_text='The year is not used, so write whatever')

    star_sign = models.CharField(_('Asrtrological Sign'), max_length=100, null=True)

    instrument = models.CharField(_('Instrument'), max_length=100, null=True)

    hometown = models.CharField(_('Hometown'), max_length=100, null=True)

    image = models.ImageField(_('Image'), upload_to=uploadItem('idol'))

############################################################
# Photos

class Photo(MagiModel):
    collection_name = 'photo'

    id = models.PositiveIntegerField(_('ID'), unique=True, primary_key=True, db_index=True)

    idol = models.ForeignKey(Idol, verbose_name=_('Idol'), related_name='photos', null=True, on_delete=models.SET_NULL, db_index=True)

    RARITY_CHOICES = (
        "N",
        "R",
        "SR",
        "UR"
    )

############################################################
# Songs

class Song(MagiModel):
    collection_name = 'song'

    DIFFICULTY_VALIDATORS = [
        MinValueValidator(1),
        MaxValueValidator(13),
    ]

    DIFFICULTIES = [
        ('easy', _('Easy')),
        ('normal', _('Normal')),
        ('hard', _('Hard')),
        ('pro', _('Pro')),
    ]

    SONGWRITERS_DETAILS = [
        ('composer', _('Composer')),
        ('lyricist', _('Lyricist')),
        ('arranger', _('Arranger')),
    ]

    singers = models.ManyToManyField(Idol, related_name="sung_songs", verbose_name=_('Singers'))

    image = models.ImageField('Album cover', upload_to=uploadItem('song'))

    japanese_name = models.CharField(_('Title'), max_length=100, unique=True)
    romaji_name = models.CharField(string_concat(_('Title'), ' (', _('Romaji'), ')'), max_length=100, null=True)

    name = models.CharField(string_concat(_('Title'), ' (', _('Translation'), ')'), max_length=100, null=True)
    NAMES_CHOICES = ALT_LANGUAGES_EXCEPT_JP
    d_names = models.TextField(_('Title'), null=True)


    easy_notes = models.PositiveIntegerField(string_concat(_('Easy'), ' - ', _('Notes')), null=True)
    easy_difficulty = models.PositiveIntegerField(string_concat(_('Easy'), ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    normal_notes = models.PositiveIntegerField(string_concat(_('Normal'), ' - ', _('Notes')), null=True)
    normal_difficulty = models.PositiveIntegerField(string_concat(_('Normal'), ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    hard_notes = models.PositiveIntegerField(string_concat(_('Hard'), ' - ', _('Notes')), null=True)
    hard_difficulty = models.PositiveIntegerField(string_concat(_('Hard'), ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    pro_notes = models.PositiveIntegerField(string_concat(_('Pro'), ' - ', _('Notes')), null=True)
    pro_difficulty = models.PositiveIntegerField(string_concat(_('Pro'), ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)

    composer = models.CharField(_('Composer'), max_length=100, null=True)
    lyricist = models.CharField(_('Lyricist'), max_length=100, null=True)
    arranger = models.CharField(_('Arranger'), max_length=100, null=True)




############################################################
# Accounts

class Account(BaseAccount):
    class Meta:
        pass
