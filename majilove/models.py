# -*- coding: utf-8 -*-
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings as django_settings
from magi.models import User, uploadItem
from magi.item_model import MagiModel, i_choices, getInfoFromChoices
from magi.abstract_models import BaseAccount
from magi.utils import templateVariables


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

    image = models.ImageField(_('Image'), upload_to=uploadItem('idol'), null=True)

    small_image = models.ImageField('Small image (for map)', upload_to=uploadItem('idol/small'))

    def __unicode__(self):
        return unicode(self.t_name)

############################################################
# Photos

class Photo(MagiModel):
    collection_name = 'photo'

    owner = models.ForeignKey(User, related_name='added_photos')
    id = models.PositiveIntegerField(_('Album ID'), unique=True, primary_key=True, db_index=True)

    name = models.CharField(_('Photo name'), max_length=100)
    NAMES_CHOICES = ALL_ALT_LANGUAGES
    d_names = models.TextField(_('Photo name'), null=True)

    release_date = models.DateField(_('Release date'), null=True, db_index=True)
    idol = models.ForeignKey(Idol, verbose_name=_('Idol'), related_name='photos', db_index=True)

    # Images

    # The square icon
    image = models.ImageField(_('Icon'), upload_to=uploadItem('photo'), null=True)
    image_special_shot = models.ImageField(string_concat(_('Icon'), ' (', _('Special shot'), ')'), upload_to=uploadItem('photo/specialshot'), null=True)

    # Full photo
    full_photo = models.ImageField(_('Photo image'), upload_to=uploadItem('photo/image'))
    full_photo_special_shot = models.ImageField(string_concat(_('Photo image'), ' (', _('Special shot'), ')'), upload_to=uploadItem('photo/image/specialshot'), null=True)

    transparent = models.ImageField(_('Transparent'), upload_to=uploadItem('photo/transparent'), null=True)
    transparent_special_shot = models.ImageField(string_concat(_('Transparent'), ' (', _('Special shot'), ')'), upload_to=uploadItem('photo/transparent/specialshot'), null=True)

    # Poster
    art = models.ImageField(_('Poster'), upload_to=uploadItem('photo/poster'), null=True)
    art_special_shot = models.ImageField(string_concat(_('Poster'), ' (', _('Special shot'), ')'), upload_to=uploadItem('photo/poster/specialshot'), null=True)

    message = models.ImageField(_('Message'), upload_to=uploadItem('photo/message'), null=True)
    autograph = models.ImageField(_('Autograph'), upload_to=uploadItem('photo/autograph'), null=True)

    message_text = models.TextField(string_concat(_('Message text'), ' (', _('Japanese') + ')'), max_length=500, null=True)
    message_translation = models.TextField(_('Message translation'), max_length=500, null=True)
    MESSAGE_TRANSLATIONS_CHOICES = ALL_ALT_LANGUAGES
    d_message_translations = models.TextField(_('Message translation'), null=True)
    @property
    def t_message_translation(self):
        if get_language() == 'ja': return None
        return self.message_translations.get(get_language(), self.message_translation)

    # Photo statistics

    RARITIES = OrderedDict([
        ('N', {
            'translation': 'N',
            'special_shot_percentage': None,
            'outfit_unlock_percentage': 0,
            'squares_in_moments' : 4,
            'max_levels': 20,
            }),
        ('R', {
            'translation': 'R',
            'special_shot_percentage': 100,
            'outfit_unlock_percentage': 50,
            'squares_in_moments' : 16,
            'max_levels': (30, 50),
            }),
        ('SR', {
            'translation': 'SR',
            'special_shot_percentage': 83,
            'outfit_unlock_percentage': 33,
            'squares_in_moments' : 24,
            'max_levels': (40, 60),
            }),
        ('UR', {
            'translation': 'UR',
            'special_shot_percentage': 87,
            'outfit_unlock_percentage': 25,
            'squares_in_moments': 32,
            'max_levels': (50, 70),
        }),
    ])

    RARITY_CHOICES = [(_name, _info['translation']) for _name, _info in RARITIES.items()]
    i_rarity = models.PositiveIntegerField(_('Rarity'), choices=i_choices(RARITY_CHOICES), db_index=True)
    rarity_max_levels = property(getInfoFromChoices('rarity', RARITIES, 'max_levels'))
    rarity_special_shot_percentage = property(getInfoFromChoices('rarity', RARITIES, 'special_shot_percentage'))
    rarity_squares_in_moments = property(getInfoFromChoices('rarity', RARITIES, 'squares_in_moments'))

    COMBINABLE_RARITIES = ['R', 'SR', 'UR']

    @property
    def combinable(self):
        return self.rarity in self.COMBINABLE_RARITIES

    @property
    def single_max_level(self):
        return self.rarity_max_levels[0] if self.combinable else self.rarity_max_levels

    @property
    def max_max_level(self):
        return self.rarity_max_levels[1] if self.combinable else self.rarity_max_levels

    COLOR_CHOICES = [
        ('star', _('Star')), # Yellow
        ('shine', _('Shine')), # Red
        ('dream', _('Dream')), # Blue
    ]

    i_color = models.PositiveIntegerField(_('Color'), choices=i_choices(COLOR_CHOICES), db_index=True)

    dance_min = models.PositiveIntegerField(string_concat(_('Dance'), ' (', _('Minimum'), ')'), default=0)
    dance_single_copy_max = models.PositiveIntegerField(string_concat(_('Dance'), ' (', _('Single copy maximum'), ')'), default=0)
    dance_max_copy_max = models.PositiveIntegerField(string_concat(_('Dance'), ' (', _('Maxed copy maximum'), ')'), default=0)

    vocal_min = models.PositiveIntegerField(string_concat(_('Vocal'), ' (', _('Minimum'), ')'), default=0)
    vocal_single_copy_max = models.PositiveIntegerField(string_concat(_('Vocal'), ' (', _('Single copy maximum'), ')'), default=0)
    vocal_max_copy_max = models.PositiveIntegerField(string_concat(_('Vocal'), ' (', _('Maxed copy maximum'), ')'), default=0)

    charm_min = models.PositiveIntegerField(string_concat(_('Charm'), ' (', _('Minimum'), ')'), default=0)
    charm_single_copy_max = models.PositiveIntegerField(string_concat(_('Charm'), ' (', _('Single copy maximum'), ')'), default=0)
    charm_max_copy_max = models.PositiveIntegerField(string_concat(_('Charm'), ' (', _('Maxed copy maximum'), ')'), default=0)

    @property
    def dance_single_copy_increment(self):
        return float(self.dance_single_copy_max - self.dance_min)/(self.single_max_level - 1)
    @property
    def dance_combined_increment(self):
        return float(self.dance_max_copy_max - self.dance_single_copy_max)/(self.max_max_level - self.single_max_level)
    @property
    def vocal_single_copy_increment(self):
        return float(self.vocal_single_copy_max - self.vocal_min)/(self.single_max_level - 1)
    @property
    def vocal_combined_increment(self):
        return float(self.vocal_max_copy_max - self.vocal_single_copy_max)/(self.max_max_level - self.single_max_level)
    @property
    def charm_single_copy_increment(self):
        return float(self.charm_single_copy_max - self.charm_min)/(self.single_max_level - 1)
    @property
    def charm_combined_increment(self):
        return float(self.charm_max_copy_max - self.charm_single_copy_max)/(self.max_max_level - self.single_max_level)

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
        'template': _(u'{t_leader_skill_color} {t_leader_skill_stat} +{leader_skill_percentage}%'),
        'japanese_template': u'{t_leader_skill_color} の{t_leader_skill_stat}パフォーマンス{leader_skill_percentage}%上昇',
    }

    # Currently leader skill color is always the same as card color
    LEADER_SKILL_COLOR_CHOICES = COLOR_CHOICES
    i_leader_skill_color = property(lambda _a: _a.i_color)

    STATISTICS = OrderedDict([
        ('dance', {
            'translation': _('Dance'),
            'english': u'Dance',
            'japanese_translation': u'DANCE'
        }),
        ('vocal', {
            'translation': _('Vocal'),
            'english': u'Vocal',
            'japanese_translation': u'VOCAL'
        }),
        ('charm', {
            'translation': _('Charm'),
            'english': u'Charm',
            'japanese_translation': u'ACT'
        })
    ])

    LEADER_SKILL_STAT_CHOICES = [(_name, _info['translation']) for _name, _info in STATISTICS.items()]
    i_leader_skill_stat = models.PositiveIntegerField('{t_leader_skill_stat}', choices=i_choices(LEADER_SKILL_STAT_CHOICES), null=True)
    leader_skill_percentage = models.PositiveIntegerField('{leader_skill_percentage}', null=True)

    @property
    def leader_skill(self):
        if self.leader_skill_stat is None: return None
        return self.LEADER_SKILL_INFO['template'].format(**{
            k: getattr(self, k, '')
            for k in templateVariables(self.LEADER_SKILL_INFO['template'])
        })

    @property
    def japanese_leader_skill(self):
        if self.leader_skill_color is None: return None
        return self.LEADER_SKILL_INFO['japanese_template'].format(**{
            k: getattr(self, k, '')
            for k in templateVariables(self.LEADER_SKILL_INFO['template'])
        })

    # Skills
    SKILL_TYPES = OrderedDict([
        ('score_notes', {
            'translation': _(u'Score notes'),
            'english': 'Score notes',
            'japanese_translation': u'スコアノーツ',
            'icon': 'scoreup',
            'increment': 1,

            'template': _(u'Score Notes +{skill_note_count}'),
            'japanese_template': u'スコアノーツを{skill_note_count}個追加',
        }),
        ('perfect_score', {
            'translation': _(u'Perfect score up'),
            'english': 'Perfect score up',
            'japanese_translation': u'JUST PERFECTのスコア',
            'icon': 'scoreup',
            'increment': 0.3,

            'template': _(u'Perfect Score +{skill_percentage}%'),
            'japanese_template': u'JUST PERFECTのスコア{skill_percentage}%上昇',
        }),
        ('cutin', {
            'translation': _(u'Cut-in'),
            'english': 'Cut-in',
            'japanese_translation': u'カットイン',
            'icon': 'scoreup',
            'increment': 10,

            'template': _(u'Cut-in Bonus Score +{skill_percentage_int}%'),
            'japanese_template': u'カットインボーナスのスコア{skill_percentage_int}%上昇',
        }),
        ('good_lock', {
            'translation': _(u'Good lock'),
            'english': 'Good lock',
            # need someone to check this, feels too long
            'japanese_translation': u'BADをGREATに',
            'icon': 'perfectlock',
            'increment': 1,

            'template': _(u'Bad > Good ({skill_note_count} Times)'),
            'japanese_template': u'BADを{skill_note_count}回GREATにする',
        }),
        ('great_lock', {
            'translation': _(u'Great lock'),
            'english': 'Great lock',
            # also seems long, need to check which comma to use
            'japanese_translation': u'BAD,GREATをPERFECTに',
            'icon': 'perfectlock',
            'increment': 1,

            'template': _(u'Bad/Good > Great ({skill_note_count} Times)'),
            'japanese_template': u'BAD,GREATを{skill_note_count}回PERFECTにする',
        }),
        ('healer', {
            'translation': _(u'Healer'),
            'english': 'Healer',
            'japanese_translation': u'ライフ回復ノーツ',
            'icon': 'healer',
            'increment': 1,

            'template': _(u'Stamina Recovery Notes +{skill_note_count}'),
            'japanese_template': u'ライフ回復ノーツを{skill_note_count}個追加',
        }),
    ])

    SKILL_VARIABLES = ['skill_note_count', 'skill_percentage']

    SKILL_TYPE_CHOICES = [(_name, _info['translation']) for _name, _info in SKILL_TYPES.items()]

    i_skill_type = models.PositiveIntegerField(_('Skill'), choices=i_choices(SKILL_TYPE_CHOICES), null=True, db_index=True)
    japanese_skill_type = property(getInfoFromChoices('skill_type', SKILL_TYPES, 'japanese_translation'))
    skill_icon = property(getInfoFromChoices('skill_type', SKILL_TYPES, 'icon'))
    skill_template = property(getInfoFromChoices('skill_type', SKILL_TYPES, 'template'))
    japanese_skill_template = property(getInfoFromChoices('skill_type', SKILL_TYPES, 'japanese_template'))
    skill_increment = property(getInfoFromChoices('skill_type', SKILL_TYPES, 'increment'))

    @property
    def skill(self):
        if self.i_skill_type is None: return None
        return self.skill_template.format(**{
            k: getattr(self, k, '')
            for k in templateVariables(self.skill_template)
        })

    @property
    def japanese_skill(self):
        if self.i_skill_type is None: return None
        return self.japanese_skill_template.format(**{
            k: getattr(self, k, '')
            for k in templateVariables(self.japanese_skill_template)
        })

    skill_note_count = models.PositiveIntegerField('{skill_note_count}', null=True)
    # should percentage be split into different variales for perfect score and cutin?
    skill_percentage = models.FloatField('{skill_percentage}', null=True)
    skill_percentage_int = property(lambda _a: int(_a.skill_percentage))

    # Subskills
    SUB_SKILL_TYPES = OrderedDict([
        ('full_combo', {
            'translation': _(u'Full combo'),
            'english': 'Full combo',
            'japanese_translation': u'フルコンボ',

            'template': _(u'+{sub_skill_amount} score when clearing a song with a Full Combo'),
            'japanese_template': u'フルコンボクリア時+{sub_skill_amount}スコア',
        }),
        ('stamina', {
            'translation': _(u'Stamina based'),
            'english': 'Stamina based',
            # unsure about this one too
            'japanese_translation': u'LIFEでクリア時',

            'template': _(u'+{sub_skill_amount} score when clearing a song with {sub_skill_percentage}% Stamina'),
            'japanese_template': u'LIFE{sub_skill_percentage}%以上でクリア時+{sub_skill_amount}スコア',
        }),
    ])

    SUB_SKILL_VARIABLES = ['sub_skill_percentage', 'sub_skill_amount']

    SUB_SKILL_TYPE_CHOICES = [(_name, _info['translation']) for _name, _info in SUB_SKILL_TYPES.items()]
    i_sub_skill_type = models.PositiveIntegerField(_('Sub skill'), choices=i_choices(SUB_SKILL_TYPE_CHOICES), null=True)
    japanese_sub_skill_type = property(getInfoFromChoices('sub_skill_type', SUB_SKILL_TYPES, 'japanese_translation'))

    sub_skill_template = property(getInfoFromChoices('sub_skill_type', SUB_SKILL_TYPES, 'template'))
    japanese_sub_skill_template = property(getInfoFromChoices('sub_skill_type', SUB_SKILL_TYPES, 'japanese_template'))

    @property
    def sub_skill(self):
        if self.i_sub_skill_type is None: return None
        return self.sub_skill_template.format(**{
            k: getattr(self, k, '')
            for k in templateVariables(self.sub_skill_template)
        })

    @property
    def japanese_sub_skill(self):
        if self.i_sub_skill_type is None: return None
        return self.japanese_sub_skill_template.format(**{
            k: getattr(self, k, '')
            for k in templateVariables(self.japanese_sub_skill_template)
        })

    sub_skill_amount = models.PositiveIntegerField('{sub_skill_amount}', null=True)
    sub_skill_percentage = models.FloatField('{sub_skill_percentage}', null=True)
    # Currently either 3k (gacha URs) or 2k (All other cards)
    sub_skill_increment = models.PositiveIntegerField(_('Sub skill level up increment'), null=True)

    # Cache idol

    _cache_idol_days = 20
    _cache_idol_last_update = models.DateTimeField(null=True)
    _cache_j_idol = models.TextField(null=True)

    @classmethod
    def cached_idol_pre(self, d):
        d['name'] = d['names'].get('en', None)
        d['t_name'] = d['unicode'] = d['names'].get(get_language(), d['name'])

    def to_cache_idol(self):
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
                rarity=self.rarity,
                idol_name=self.cached_idol.t_name if self.cached_idol else '',
                name=self.t_name,
            )
        return u''

############################################################
# Songs

class Song(MagiModel):
    collection_name = 'song'

    owner = models.ForeignKey(User, related_name='added_songs')

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

    COLOR_CHOICES = Photo.COLOR_CHOICES
    i_color = models.PositiveIntegerField(_('Color'), choices=i_choices(COLOR_CHOICES))

    DIFFICULTY_VALIDATORS = [
        MinValueValidator(1),
        MaxValueValidator(13),
    ]

    easy_notes = models.PositiveIntegerField(string_concat(_('Easy'), ' - ', _('Notes')), null=True)
    easy_difficulty = models.PositiveIntegerField(string_concat(_('Easy'), ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    normal_notes = models.PositiveIntegerField(string_concat(_('Normal'), ' - ', _('Notes')), null=True)
    normal_difficulty = models.PositiveIntegerField(string_concat(_('Normal'), ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    hard_notes = models.PositiveIntegerField(string_concat(_('Hard'), ' - ', _('Notes')), null=True)
    hard_difficulty = models.PositiveIntegerField(string_concat(_('Hard'), ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)
    pro_notes = models.PositiveIntegerField(string_concat(_('Pro'), ' - ', _('Notes')), null=True)
    pro_difficulty = models.PositiveIntegerField(string_concat(_('Pro'), ' - ', _('Difficulty')), validators=DIFFICULTY_VALIDATORS, null=True)

    length = models.PositiveIntegerField(_('Length'), null=True)

    # just going to have unlock method for regular permanent songs for now
    unlock_chapter = models.CharField(_('Unlock Chapter'), max_length=100, null=True)
    UNLOCK_CHAPTERS_CHOICES = ALL_ALT_LANGUAGES
    d_unlock_chapters = models.TextField(_('Unlock Chapter'), null=True)

    #TODO: other unlock methods

    def __unicode__(self):
        return unicode(self.t_name)
