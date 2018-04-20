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

    image = models.ImageField(_('Image'), upload_to=uploadItem('i'))

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
# Accounts

class Account(BaseAccount):
    class Meta:
        pass
