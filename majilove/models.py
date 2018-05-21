# -*- coding: utf-8 -*-
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from django.db import models
from django.conf import settings as django_settings
from magi.models import User, uploadItem
from magi.item_model import MagiModel, i_choices, getInfoFromChoices
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
    def display_bloody_type(self):
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

    image = models.ImageField(_('Image'), upload_to=uploadItem('idol'))

    small_image = models.ImageField(_('Image'), upload_to=uploadItem('idol/small'))

    def __unicode__(self):
        return unicode(self.t_name)

############################################################
# Photos

class Photo(MagiModel):
    collection_name = 'photo'
    owner = models.ForeignKey(User, related_name='added_photos')
    id = models.PositiveIntegerField(_('ID'), unique=True, primary_key=True, db_index=True)

    name = models.CharField(_('Photo Name'), max_length=100)
    japanese_name = models.CharField(string_concat(_('Photo Name'), ' (', _('Japanese'), ')'), max_length=100)
    NAMES_CHOICES = LANGUAGES_NEED_OWN_NAME
    d_names = models.TextField(_('Title'), null=True)
    @property
    def t_name(Self):
        if get_language() == 'ja':
            return self.japanese_name
        return self.names.get(get_language(), self.name)

    release_date = models.DateField(_('Release date'), null=True, db_index=True)
    idol = models.ForeignKey(Idol, verbose_name=_('Idol'), related_name='photos', null=True, on_delete=models.SET_NULL, db_index=True)

    # Images

    # The square icon
    icon = models.ImageField(_('Icon'), upload_to=uploadItem('p'), null=True)
    icon_special_shot = models.ImageField(string_concat(_('Icon'), ' (', _('Special Shot'), ')'), upload_to=uploadItem('p/a'), null=True)

    # Full photo
    image = models.ImageField(_('Photo Image'), upload_to=uploadItem('p/image'))
    image_special_shot = models.ImageField(string_concat(_('Photo Image'), ' (', _('Special Short'), ')'), upload_to=uploadItem('p/image/a'), null=True)

    transparent = models.ImageField(_('Transparent'), upload_to=uploadItem('p/transparent'), null=True)
    transparent_special_shot = models.ImageField(string_concat(_('Transparent'), ' (', _('Special shot'), ')'), upload_to=uploadItem('p/transparent/a'), null=True)

    poster = models.ImageField(_('Poster'), upload_to=uploadItem('p/poster'), null=True)
    poster_special_shot = models.ImageField(string_concat(_('Poster'), ' (', _('Special Shot'), ')'), upload_to=uploadItem('p/poster/a'), null=True)

    message = models.ImageField(_('Message'), upload_to=uploadItem('p/message'), null=True)
    autograph = models.ImageField(_('Autograph'), upload_to=uploadItem('p/autograph'), null=True)

    message_text = models.TextField(string_concat(_('Message Text'), ' (', _('Japanese') + ')'), max_length=500, null=True)
    message_translation = models.TextField(_('Message translation'), max_length=500, null=True)
    MESSAGE_TRANSLATIONs_CHOICES = ALL_ALT_LANGUAGES
    d_message_translations = models.TextField(_('Message translation'), null=True)
    @property
    def t_message_translation(self):
        if get_language() == 'ja': return None
        return self.message_translations.get(get_language(), self.message_translation)

    # photo stats

    #triplets_in_moments is number of sets of +30 dance/vocal/charm sqaures before 100%
    RARITIES = OrderedDict([
        (1, {
            'short_form': 'N',
            'special_shot_percentage': None,
            'outfit_unlock_percentage': 0,
            'triplets_in_moments' : 1,
            'max_levels': 20,
            }),
        (2, {
            'short_form': 'R',
            'special_shot_percentage': 100,
            'outfit_unlock_percentage': 50,
            'triplets_in_moments' : 4,
            'max_levels': (30, 50),
            }),
        (3, {
            'short_form': 'SR',
            'special_shot_percentage': 83,
            'outfit_unlock_percentage': 33,
            'triplets_in_moments' : 6,
            'max_levels': (40, 60),
            }),
        (4, {
            'short_form': 'UR',
            'special_shot_percentage': 87,
            'outfit_unlock_percentage': 25,
            'triplets_in_moments': 8,
            'max_levels': (50, 70),
        }),
    ])

    RARITY_CHOICES = [(_name, _info['short_form']) for _name, _info in RARITIES.items()]
    RARITY_WITHOUT_I_CHOICES = True
    i_rarity = models.PositiveIntegerField(_('Rarity'), choices=i_choices(RARITY_CHOICES), db_index=True)

    COMBINABLE_RARITIES = [2, 3, 4]

    @property
    def combinable(self):
        return self.i_rarity in self.COMBINABLE_RARITIES

    @property
    def single_max_level(self):
        return RARITIES[self.i_rarity]['max_levels'][0] if self.combinable else RARITIES[self.i_rarity]['max_levels']

    @property
    def max_max_level(self):
        return RARITIES[self.i_rarity]['max_levels'][1] if self.combinable else RARITIES[self.i_rarity]['max_levels']

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
    i_color = models.PositiveIntegerField(_('Color'), choices=COLOR_CHOICES, db_index=True)
    english_color = property(getInfoFromChoices('color', COLORS, 'english'))

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

    # Leader Skill
    LEADER_SKILL_INFO = {
        'variables': ['color', 'stat', 'percentage'],
        'template': _(u'{color} {stat} +{percentage}%'),
        'japanese_template': u'{color} の{stat}パフォーマンス{percentage}%上昇'
    }

    #currently always the same as color, but this is safer
    LEADER_SKILL_COLOR_CHOICES = COLOR_CHOICES
    LEADER_SKILL_COLOR_WITHOUT_I_CHOICES = True
    i_leader_skill_color = models.PositiveIntegerField('{color}', choices=LEADER_SKILL_COLOR_CHOICES, null=True)

    LEADER_SKILL_STAT_CHOICES = [(_name, _info['translation']) for _name, _info in STATS.items()]
    LEADER_SKILL_STAT_WITHOUT_I_CHOICES = True
    i_leader_skill_stat = models.PositiveIntegerField('{stat}', choices=LEADER_SKILL_STAT_CHOICES, null=True)

    leader_skill_percentage = models.PositiveIntegerField('{percentage}', null=True)

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


    # Skills
    SKILL_TYPES = OrderedDict([
        (1, {
            'translation': _(u'Score notes'),
            'english': 'Score notes',
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
            'japanese_translation': u'BADをGREATに',
            'icon': 'perfectlock',

            'variables': ['note_count'],
            'template': _(u'Bad > Good ({note_count} Times)'),
            'japanese_template': _(u'BADを{note_count}回GREATにする')
        }),
        (5, {
            'translation': _(u'Great lock'),
            'english': 'Great lock',
            # also seems long, need to check which comma to use
            'japanese_translation': u'BAD,GREATをPERFECTに',
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
        if self.i_skill_type is None: return None
        return self.skill_template.format(**self.skill_variables)

    @property
    def japanese_skill(self):
        if self.i_skill_type is None: return None
        return self.japanese_skill_template.format(**self.skill_variables)

    skill_note_count = models.PositiveIntegerField('{note_count}', null=True)
    # should percentage be split into different variales for perfect score and cutin?
    skill_percentage = models.FloatField('{percentage}', null=True)

    # Subskills
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

    # Cache idol

    _cache_idol_days = 20
    _cache_idol_last_update = models.DateTimeField(null=True)
    _cache_j_idol = models.TextField(null=True)

    @classmethod
    def cached_idol_pre(self, d):
        d['name'] = d['names'].get('en', None)
        d['t_name'] = d['unicode'] = d['names'].get(get_language(), d['name'])

    def to_cache_member(self):
        if not self.idol:
            return {
                'id': None,
                'names': {},
                'image': None,
            }
        names = self.idol.names or {}
        names['en'] = self.idol.name
        names['ja'] = self.idol.japanese_name
        return {
            'id': self.idol.id,
            'names': names,
            'image': unicode(self.idol.image)
        }

    def __unicode__(self):
        if self.id:
            return u'{rarity} {idol_name} - {name}'.format(
                rarity = self.rarity,
                idol_name = self.cached_idol.t_name if self.cached_idol else '',
                name=(self.japanese_name
                    if (get_language() == 'ja' and self.japanese_name) or not self.name
                    else self.name or ''),
            )
        return u''
