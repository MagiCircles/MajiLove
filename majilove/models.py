# -*- coding: utf-8 -*-
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from django.db import models
from django.conf import settings as django_settings
from magi.item_model import MagiModel, i_choices, getInfoFromChoices
from magi.abstract_models import AccountAsOwnerModel, BaseAccount
from magi.models import User, uploadItem

# Create your models here.

LANGUAGES_NEED_OWN_NAME = [ l for l in django_settings.LANGUAGES if l[0] in ['ru', 'zh-hans', 'zh-hant', 'kr'] ]
LANGUAGES_NEED_OWN_NAME_KEYS = [ l[0] for l in django_settings.LANGUAGES if l[0] in ['ru', 'zh-hans', 'zh-hant', 'kr'] ]
LANGUAGES_DIFFERENT_CHARSET = [ l for l in django_settings.LANGUAGES if l[0] in ['ja', 'ru', 'zh-hans', 'zh-hant', 'kr'] ]
LANGUAGES_DIFFERENT_CHARSET_KEYS = [ l[0] for l in django_settings.LANGUAGES if l[0] in ['ja', 'ru', 'zh-hans', 'zh-hant', 'kr'] ]
ALL_ALT_LANGUAGES = [ l for l in django_settings.LANGUAGES if l[0] != 'en' ]
ALL_ALT_LANGUAGES_KEYS = [ l[0] for l in django_settings.LANGUAGES if l[0] != 'en' ]
ALT_LANGUAGES_EXCEPT_JP = [ l for l in django_settings.LANGUAGES if l[0] not in ['en', 'ja'] ]
ALT_LANGUAGES_EXCEPT_JP_KEYS = [ l[0] for l in django_settings.LANGUAGES if l[0] not in ['en', 'ja'] ]

############################################################
# Idols

class Idol(MagiModel):
    collection_name = 'idol'

    owner = models.ForeignKey(User, related_name='added_idols')

    # mostly copying the name stuff from the bandori.party code
    name = models.CharField(string_concat(_('Name'), ' (', _('Romaji'), ')'), max_length=100, unique=True)

    japanese_name = models.CharField(string_concat(_('Name'), ' (', _('Japanese'), ')'), max_length = 100, unique=True)

    NAMES_CHOICES = LANGUAGES_NEED_OWN_NAME
    d_names = models.TextField(_('Name'), null=True)

    @property
    def t_name(self):
        if get_language() == 'ja':
            return self.japanese_name
        return self.names.get(get_language(), self.name)

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

    i_blood_type = models.PositiveIntegerField(_('Blood Type'), choices=i_choices(BLOOD_CHOICES), null=True)

    birthday = models.DateField(_('Birthday'), null=True, help_text='The year is not used, so write whatever')

    star_sign = models.CharField(_('Asrtrological Sign'), max_length=100, null=True)

    instrument = models.CharField(_('Instrument'), max_length=100, null=True)

    hometown = models.CharField(_('Hometown'), max_length=100, null=True)

    image = models.ImageField(_('Image'), upload_to=uploadItem('idol'))

############################################################
# Photos

class Photo(MagiModel):
    collection_name = 'photo'

    owner = models.ForeignKey(User, related_name='added_photos')

    id = models.PositiveIntegerField(_('ID'), unique=True, primary_key=True, db_index=True)

    name = models.CharField(_('Photo Name'), max_length=100)

    japanese_name = models.CharField(string_concat(_('Photo Name'), ' (', _('Japanese'), ')'), max_length=100)

    NAMES_CHOICES = ALT_LANGUAGES_EXCEPT_JP

    d_names = models.TextField(_('Title'), null=True)

    @property
    def t_name(Self):
        if get_language() == 'ja':
            return self.japanese_name
        return self.names.get(get_language(), self.name)

    release_date = models.DateField(_('Release date'), null=True, db_index=True)

    idol = models.ForeignKey(Idol, verbose_name=_('Idol'), related_name='photos', null=True, on_delete=models.SET_NULL, db_index=True)

    dance_min = models.PositiveIntegerField(string_concat(_('Dance'), ' (', _('Minimum'), ')'), default=0)

    dance_single_copy_max = models.PositiveIntegerField(string_concat(_('Dance'), ' (', _('Single Copy Maximum'), ')'), default=0)

    dance_max_copy_max = models.PositiveIntegerField(string_concat(_('Dance'), ' (', _('Maxed Copy Maximum'), ')'), default=0)

    vocal_min = models.PositiveIntegerField(string_concat(_('Vocal'), ' (', _('Minimum'), ')'), default=0)

    vocal_single_copy_max = models.PositiveIntegerField(string_concat(_('Vocal'), ' (', _('Single Copy Maximum'), ')'), default=0)

    vocal_max_copy_max = models.PositiveIntegerField(string_concat(_('Vocal'), ' (', _('Maxed Copy Maximum'), ')'), default=0)

    charm_min = models.PositiveIntegerField(string_concat(_('Charm'), ' (', _('Minimum'), ')'), default=0)

    charm_single_copy_max = models.PositiveIntegerField(string_concat(_('Charm'), ' (', _('Single Copy Maximum'), ')'), default=0)

    charm_max_copy_max = models.PositiveIntegerField(string_concat(_('Charm'), ' (', _('Maxed Copy Maximum'), ')'), default=0)

    @property
    def overall_min(self):
        return self.dance_min + self.vocal_min + self.charm_min

    @property
    def overall_single_copy_max(self):
        return self.dance_single_copy_max + self.vocal_single_copy_max + self.charm_single_copy_max

    @property
    def overall_max_copy_max(self):
        return self.dance_max_copy_max + self.vocal_max_copy_max + self.charm_max_copy_max

    RARITY_CHOICES = (
        'N',
        'R',
        'SR',
        'UR'
    )

    i_rarity = models.PositiveIntegerField(_('Rarity'), choices=i_choices(RARITY_CHOICES), db_index=True)

    ATTRIBUTES= OrderedDict([
        (1, {
            'translation': _('Star'),
            'english': u'Star'
        }),
        (2, {
            'translation': _('Shine'),
            'english': u'Shine'
        }),
        (3 {
            'translation': _('Dream'),
            'english': u'Dream'
        })
    ])

    ATTRIBUTE_CHOICES = [(_name, _info['translation']) for _name, _info in ATTRIBUTES.items()]
    ATTRIBUTE_WITHOUT_I_CHOICES=True
    i_attribute = models.PositiveIntegerField(_('Attribute'), choices=ATTRIBUTE_CHOICES, db_index=True)
    english_attribute = property(getInfoFromChoices('attribute', ATTRIBUTES, 'english'))

    # Images

    # The square icon
    icon = models.ImageField(_('Icon'), upload_to=uploadItem('p'), null=True)
    icon_special_shot = models.ImageField(string_concat(_('Icon'), ' (', _('Special Shot'), ')'), upload_to=uploadItem('p/a'), null=True)

    # Full photo
    image = models.ImageField(_('Photo Image'), upload_to=uploadItem('p/image'))
    image_special_shot = models.ImageField(string_concat(_('Photo Image'), ' (', _('Special Short'), ')'), upload_to=uploadItem('p/image/a'), null=True)

    # only URs have a poster for normal shot
    poster = models.ImageField(_('Poster'), upload_to=uploadItem('p/poster'), null=True)

    # SR and UR have special shot poster
    poster_special_shot = models.ImageField(string_concat(_('Poster'), ' (', _('Special Shot'), ')'), upload_to=uploadItem('p/poster/a'), null=True)

    message = models.ImageField(_('Message'), upload_to=uploadItem('p/message'), null=True)
    autograph = models.ImageField(_('Autograph'), upload_to=uploadItem('p/autograph'), null=True)

    message_japanese_text = models.TextField(string_concat(_('Message Text'), ' (', _('Japanese') + ')'), max_length=1000, null=True)
    message_text = models.TextField(_('Message Text'), max_length=1000, null=True)

    # Skill
    SKILL_TYPES = OrderedDict([
        (1, {
            'translation': _(u'Score notes'),
            'english': 'Score notes'
            'japanese_translation': u'スコアノーツ',
            'icon': 'scoreup',

            'variables': ['note_count'],
            'template': _(u'Score Notes +{note_count}'),
            'japanese_template': u'スコアノーツを{note_count}個追加'
        }),
        (2, {
            'translation': _(u'Perfect score up'),
            'english': 'Perfect score up',
            'japanese_translation': u'JUST PERFECTのスコア',
            'icon': 'scoreup',

            'variables': ['percentage'],
            'template': _(u'Perfect Score +{percentage}%'),
            'japanese_template': u'JUST PERFECTのスコア{percentage}%上昇'
        }),
        (3, {
            'translation': _(u'Cut-in'),
            'english': 'Cut-in',
            'japanese_translation': u'カットイン',
            'icon': 'scoreup',

            'variables': ['percentage'],
            'template': _(u'Cut-in Bonus Score +{percentage}%'),
            'japanese_template': u'カットインボーナスのスコア{percentage}%上昇'
        }),
        (4, {
            'translation': _(u'Good lock'),
            'english': 'Good lock',
            # need someone to check this, feels too long
            'japanese_translation': u'BADをGREATにする',
            'icon': 'perfectlock',

            'variables': ['note_count'],
            'template': _(u'Bad > Good ({note_count} Times)'),
            'japanese_template': _(u'BADを{note_count}回GREATにする')
        }),
        (5, {
            'translation': _(u'Great lock'),
            'english': 'Great lock',
            # also seems long, need to check which comma to use
            'japanese_translation': u'BAD,GREATをPERFECTにする',
            'icon': 'perfectlock',

            'variables': ['note_count'],
            'template': _(u'Bad/Good > Great ({note_count} Times)'),
            'japanese_template': u'BAD,GREATを{note_count}回PERFECTにする'
        }),
        (6, {
            'translation': _(u'Healer'),
            'english': 'Healer',
            'japanese_translation': u'ライフ回復ノーツ',
            'icon': 'healer',

            'variables': ['note_count'],
            'template': _(u'Stamina Recovery Notes +{note_count}'),
            'japanese_template': u'ライフ回復ノーツを{note_count}個追加'
        })
    ])

    ALL_VARIABLES = { item: True for sublist in [ _info['variables'] for _info in SKILL_TYPES.values() ] for item in sublist }.keys()

    SKILL_TYPE_WITHOUT_I_CHOICES = True
    SKILL_TYPE_CHOICES = [(_name, _info['translation']) for _name, _info in SKILL_TYPES.items()]

    i_skill_type = models.PositiveIntegerField(_('Skill'), choices=SKILL_TYPE_CHOICES, null=True, db_index=True)
    japanese_skill_type = property(getInfoFromChoices('skill_type', SKILL_TYPES, 'japanese_translation'))
    skill_icon = property(getInfoFromChoices('skill_type', SKILL_TYPES, 'icon'))

    @property
    def skill_template(self):
        return self.SKILL_TYPES[self.skill_type]['template']

    @property
    def japanese_skill_template(self):
        return self.SKILL_TYPES[self.skill_type]['japanese_template']

    @property
    def skill_variables(self):
        return {
            key: getattr(self, u'skill_{}'.format(key))
            for key in self.SKILL_TYPES[self.skill_type]['variables']
        }

    @property
    def skill(self):
        self.i_skill_type is None: return None
        return self.skill_template.format(**self.skill_variables)

    @property
    def japanese_skill(self):
        if self.i_skill_type is None: return None
        return self.japanese_skill_template.format(**self.skill_variables)

    skill_note_count = models.PositiveIntegerField('{note_count}', null=True)
    # should percentage be split into different variales for perfect score and cutin?
    skill_percentage = models.FloatField('{percentage}', null=True)

    STATS = OrderedDict([
        (1, {
            'translation': _('Dance'),
            'english': u'Dance',
            'japanese_translation': u'DANCE'
        }),
        (2, {
            'translation': _('Vocal'),
            'english': u'Vocal',
            'japanese_translation': u'VOCAL'
        }),
        (3, {
            'translation': _('Charm'),
            'english': u'Charm',
            'japanese_translation': u'ACT'
        })
    ])
    # Leader Skill
    LEADER_SKILL_INFO = {
        'variables': ['color', 'stat', 'percentage'],
        'template': _(u'{color} {stat} +{percentage}%'),
        'japanese_template': u'{color} の{stat}パフォーマンス{percentage}%上昇'
    }

    #currently always the same as attribute, but is this safer for future stuff?
    LEADER_SKILL_COLOR_CHOICES = ATTRIBUTE_CHOICES
    LEADER_SKILL_COLOR_WITHOUT_I_CHOICES = True
    i_leader_skill_color = models.PositiveIntegerField('{color}', choices=LEADER_SKILL_COLOR_CHOICES, null=True)

    LEADER_SKILL_STAT_CHOICES = [(_name, _info['translation']) for _name, _info in STATS.items()]
    LEADER_SKILL_STAT_WITHOUT_I_CHOICES = True
    i_leader_skill_stat = models.PositiveIntegerField('{stat}', choices=LEADER_SKILL_STAT_CHOICES, null=True)

    leader_skill_percentage = models.FloatField('{percentage}', null=True)

    @property
    def leader_skill_variables(self):
        return {
            key: getattr(self, u'leader_skill_{}'.format(key))
            for key in self.LEADER_SKILL_INFO['variables']
        }

    @property
    def leader_skill(self):
        if self.leader_skill_color is None: return None
        return self.LEADER_SKILL_INFO['template'].format(**self.leader_skill_variables)

    @property
    def japanese_leader_skill(self):
        if self.leader_skill_color is None: return None
        return self.LEADER_SKILL_INFO['japanese_template'].format(**self.leader_skill_variables)

    SUB_SKILL_TYPES = OrderedDict([
        (1, {
            'translation': _(u'Full combo'),
            'english': 'Full combo',
            'japanese_translation': u'フルコンボ',

            'variables': ['amount'],
            'template': _(u'+{amount} score when clearing a song with a Full Combo'),
            'japanese_template': u'フルコンボクリア時+{amount}スコア'
        }),
        (2, {
            'translation': _(u'Stamina based'),
            'english': 'Stamina based',
            # unsure about this one too
            'japanese_translation': u'LIFEでクリア時',

            'variables': ['percentage', 'amount'],
            'template': _(u'+{amount} score when clearing a song with {percentage}% Stamina'),
            'japanese_template': u'LIFE{percentage}%以上でクリア時+{amount}スコア'
        })
    ])

    ALL_SUB_SKILL_VARIABLES = { item: True for sublist in [ _info['variables'] for _info in SUB_SKILL_TYPES.values()] for item in sublist }.keys()

    SUB_SKILL_TYPE_CHOICES = [(_name, _info['translation']) for _name, _info in SUB_SKILL_TYPES.items()]
    SUB_SKILL_TYPE_WITHOUT_I_CHOICES = True
    i_sub_skill_type = models.PositiveIntegerField(_('Sub Skill'), choices=SUB_SKILL_TYPE_CHOICES, null=True)
    japanese_sub_skill_type = property(getInfoFromChoices('sub_skill_type', SUB_SKILL_TYPES, 'japanese_translation'))

    @property
    def sub_skill_template(self):
        return self.SUB_SKILL_TYPES[self.sub_skill_type]['template']

    @property
    def japanese_sub_skill_template(self):
        return self.SUB_SKILL_TYPES[self.sub_skill_type]['japanese_template']

    @property
    def sub_skill_variables(self):
        return {
            key: getattr(self, u'sub_skill_{}'.format(key))
            for key in self.SUB_SKILL_TYPES[self.sub_skill_type]['variables']
        }

    @property
    def sub_skill(self):
        if self.i_sub_skill_type is None: return None
        return self.sub_skill_template.format(**self.sub_skill_variables)

    @property
    def japanese_sub_skill(self):
        if self.i_sub_skill_type is None: return None
        return self.japanese_sub_skill_template.format(**self.sub_skill_variables)

    sub_skill_amount = models.PositiveIntegerField('{amount}', null=True)
    sub_skill_percentage = models.FloatField('{percentage}', null=True)


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

    owner = models.ForeignKey(User, related_name='added_songs')
    singers = models.ManyToManyField(Idol, related_name="sung_songs", verbose_name=_('Singers'))

    image = models.ImageField('Album cover', upload_to=uploadItem('song'))

    japanese_name = models.CharField(_('Title'), max_length=100, unique=True)
    romaji_name = models.CharField(string_concat(_('Title'), ' (', _('Romaji'), ')'), max_length=100, null=True)

    ATTRIBUTE_CHOICES = Photo.ATTRIBUTE_CHOICES

    ATTRIBUTE_WITHOUT_I_CHOICES=True
    i_attribute = models.PositiveIntegerField(_('Attribute'), choices=i_choices(ATTRIBUTE_CHOICES))

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

    UNLOCK = OrderedDict([
        ('complete_tutorial', {
            'translation': _('Complete prologue'),
            'template': _('Complete prologue'),
            'variables': []

        }),
        ('complete_story', {
            'translation': _('Complete story'),
            'template': _('Complete Chapter {chapter}, Story {story}, Episode {episode}'),
            'variables': ['chapter', 'story', 'episode']
        }),
        ('initial', {
            'translation': _('Initially available'),
            'template': _('Initially available'),
            'variables': []
        }),
        ('temporary_campaign', {
            'translation': _('Available in campaign temporarily'),
            'template': _('Available in campaign tab from {start_date} to {end_date}'),
            'variables': ['start_date', 'end_date']
        }),
        ('temporary_campaign_daily', {
            'translation': _('Available in campaign temporarily'),
            'template': _('Available in campaign tab from {start_date} to {end_date} on {day}'), # day should be plural in English
            'variables': ['start_date', 'end_date', 'day']
        }),
        ('temporary_campaign_daily_exp', {
            'translation': _('Available in campaign temporarily'),
            'template': _('Available in campaign tab from {start_date} to {end_date} on {day1} and {day2}'),
            'variables': ['start_date', 'end_date', 'day1', 'day2']
        }),
    ])

    UNLOCK_CHOICES = [(_name, _info['translation']) for _name, _info in UNLOCK.items()]
    i_unlock = models.PositiveIntegerField(_('How to unlock?'), choices=i_choices(UNLOCK_CHOICES), null=True)

    c_unlock_variables = models.CharField(max_length=100, null=True)
    unlock_variable_keys = property(getInfoFromChoices('unlock', UNLOCK, 'variables'))
    unlock_template = property(getInfoFromChoices('unlock', UNLOCK, 'template'))
    @property
    def unlock_sentence(self):
        if self.i_unlock is None: return None
        return unicode(self.unlock_template).format(**dict(zip(self.unlock_variable_keys, self.unlock_variables)))

    #TODO link events and create an 'is currently available' utility function

############################################################
# Accounts

class Account(BaseAccount):
    class Meta:
        pass
