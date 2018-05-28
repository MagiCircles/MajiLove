# -*- coding: utf-8 -*-
from collections import OrderedDict
from math import ceil
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from django.db import models
from django.conf import settings as django_settings
from magi.models import User, uploadItem
from magi.item_model import MagiModel, i_choices, getInfoFromChoices
from magi.abstract_models import AccountAsOwnerModel, BaseAccount
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
    NAMES_CHOICES = ALL_ALT_LANGUAGES
    d_names = models.TextField(_('Photo Name'), null=True)

    release_date = models.DateField(_('Release date'), null=True, db_index=True)
    idol = models.ForeignKey(Idol, verbose_name=_('Idol'), related_name='photos', db_index=True)

    # Images

    # The square icon
    image = models.ImageField(_('Icon'), upload_to=uploadItem('photo'), null=True)
    image_special_shot = models.ImageField(string_concat(_('Icon'), ' (', _('Special Shot'), ')'), upload_to=uploadItem('photo/specialshot'), null=True)

    # Full photo
    full_photo = models.ImageField(_('Photo Image'), upload_to=uploadItem('photo/image'))
    full_photo_special_shot = models.ImageField(string_concat(_('Photo Image'), ' (', _('Special Shot'), ')'), upload_to=uploadItem('photo/image/specialshot'), null=True)

    transparent = models.ImageField(_('Transparent'), upload_to=uploadItem('photo/transparent'), null=True)
    transparent_special_shot = models.ImageField(string_concat(_('Transparent'), ' (', _('Special Shot'), ')'), upload_to=uploadItem('photo/transparent/specialshot'), null=True)

    # Poster
    art = models.ImageField(_('Poster'), upload_to=uploadItem('photo/poster'), null=True)
    art_special_shot = models.ImageField(string_concat(_('Poster'), ' (', _('Special Shot'), ')'), upload_to=uploadItem('photo/poster/specialshot'), null=True)

    message = models.ImageField(_('Message'), upload_to=uploadItem('photo/message'), null=True)
    autograph = models.ImageField(_('Autograph'), upload_to=uploadItem('photo/autograph'), null=True)

    message_text = models.TextField(string_concat(_('Message Text'), ' (', _('Japanese') + ')'), max_length=500, null=True)
    message_translation = models.TextField(_('Message translation'), max_length=500, null=True)
    MESSAGE_TRANSLATIONs_CHOICES = ALL_ALT_LANGUAGES
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
            'squares_in_moments' : 1,
            'max_levels': 20,
            }),
        ('R', {
            'translation': 'R',
            'special_shot_percentage': 100,
            'outfit_unlock_percentage': 50,
            'squares_in_moments' : 4,
            'max_levels': (30, 50),
            }),
        ('SR', {
            'translation': 'SR',
            'special_shot_percentage': 83,
            'outfit_unlock_percentage': 33,
            'squares_in_moments' : 6,
            'max_levels': (40, 60),
            }),
        ('UR', {
            'translation': 'UR',
            'special_shot_percentage': 87,
            'outfit_unlock_percentage': 25,
            'squares_in_moments': 8,
            'max_levels': (50, 70),
        }),
    ])

    RARITY_CHOICES = [(_name, _info['translation']) for _name, _info in RARITIES.items()]
    i_rarity = models.PositiveIntegerField(_('Rarity'), choices=i_choices(RARITY_CHOICES), db_index=True)
    rarity_max_levels = property(getInfoFromChoices('rarity', RARITIES, 'max_levels'))
    rarity_special_shot_perecentage = property(getInfoFromChoices('rarity', RARITIES, 'special_shot_percentage'))
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

    COLOR_CHOICES = OrderedDict([
        ('star', _('Star')), # Yellow
        ('shine', _('Shine')), # Red
        ('dream', _('Dream')), # Blue
    ])

    i_color = models.PositiveIntegerField(_('Color'), choices=i_choices(COLOR_CHOICES), db_index=True)

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
    def dance_single_copy_increment(self):
        return (self.dance_single_copy_max - self.dance_min)/(self.single_max_level - 1)
    @property
    def dance_combined_increment(self):
        return (self.dance_max_copy_max - self.dance_single_copy_max)/(self.max_max_level - self.single_max_level)
    @property
    def vocal_single_copy_increment(self):
        return (self.vocal_single_copy_max - self.vocal_min)/(self.single_max_level - 1)
    @property
    def vocal_combined_increment(self):
        return (self.vocal_max_copy_max - self.vocal_single_copy_max)/(self.max_max_level - self.single_max_level)
    @property
    def charm_single_copy_increment(self):
        return (self.charm_single_copy_max - self.charm_min)/(self.single_max_level - 1)
    @property
    def charm_combined_increment(self):
        return (self.charm_max_copy_max - self.charm_single_copy_max)/(self.max_max_level - self.single_max_level)


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
    LEADER_SKILL_COLOR_WITHOUT_I_CHOICES = True
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

            'template': _(u'Cut-in Bonus Score +{skill_percentage}%'),
            'japanese_template': u'カットインボーナスのスコア{skill_percentage}%上昇',
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
    i_sub_skill_type = models.PositiveIntegerField(_('Sub Skill'), choices=i_choices(SUB_SKILL_TYPE_CHOICES), null=True)
    japanese_sub_skill_type = property(getInfoFromChoices('sub_skill_type', SUB_SKILL_TYPES, 'japanese_translation'))

    sub_skill_template = property(getInfoFromChoices('sub_skill_type', SUB_SKILL_TYPES, 'template'))
    japanese_sub_skill_template = property(getInfoFromChoices('sub_skill_type', SUB_SKILL_TYPES, 'japanese_template'))

    @property
    def sub_skill(self):
        if self.i_sub_skill_type is None: return None
        return self.sub_skill_template.format({
            k: getattr(self, k, '')
            for k in templateVariables(self.sub_skill_template)
        })

    @property
    def japanese_sub_skill(self):
        if self.i_sub_skill_type is None: return None
        return self.japanese_sub_skill_template.format({
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
                rarity=self.rarity,
                idol_name=self.cached_idol.t_name if self.cached_idol else '',
                name=self.t_name,
            )
        return u''

############################################################
# Collectible Photos

class CollectiblePhoto(AccountAsOwnerModel):
    collection_name = 'collectiblephoto'

    account = models.ForeignKey(Account, verbose_name=_('Account'), related_name='photoscollectors')
    photo = models.ForeignKey(Photo, verbose_name=_('Photo'), related_name='collectedphotos')
    level = models.PositiveIntegerField(_('Level'), default=1)
    leader_bonus = models.PositiveIntegerField(_('Leader skill percentage'), null=True)
    skill_level = models.PositiveIntegerField(_('Skill level'), default=1)
    @property
    def skill(self):
        return self.photo.skill_template.format({
            k: getattr(self.photo, k) + (self.skill_level - 1) * self.photo.skill_increment
            for k in templateVariables(self.photo.skill_template)
        })

    sub_skill_level = models.PositiveIntegerField(_('Sub skill level'), null=True)
    @property
    def sub_skill(self):
        _sub_skill_variables = {k: getattr(self.photo, k)
        for k in templateVariables(self.photo.sub_skill_template
        )}
        _sub_skill_variables['sub_skill_amount'] = self.photo.sub_skill_amount + (sub_skill_level * self.photo.sub_skill_increment)
        return self.photo.sub_skill_template.format(**_sub_skill_variables)

    rank = models.PositiveIntegerField(_('Rank'), default=1)

    # TODO: moment based things are the same across, do I need an intermediate model for moment things?

    # percentage displayed on moments page for the card
    moments_unlocked = models.PositiveIntegerField(_('Percent of moments unlocked'), default = 0)
    # integer number of squares
    bonus_moment_squares_unlocked = models.PositiveIntegerField(_('Number of moment squares unlocked past 100%'), default = 0)
    @property
    def special_shot_unlocked(self):
        return self.moments_unlocked >= self.photo.special_shot_percentage

    prefer_normal_shot = models.BooleanField(_('Prefer normal shot photo image'), default=False)

    @property
    def image(self):
        return self.photo.image_special_shot if self.special_shot_unlocked and not self.prefer_normal_shot else self.photo.image

    @property
    def art(self):
        return self.photo.art_special_shot if self.special_shot_unlocked and not self.prefer_normal_shot else self.photo.art

    @property
    def final_leader_skill_percentage(self):
        if self.leader_bonus: return self.leader_bonus
        if self.photo.rarity is 'UR' and self.bonus_moment_squares_unlocked is 16: return 70
        _extra_squares = self.bonus_moment_squares_unlocked - 1
        if self.photo.rarity is 'UR': _extra_squares = (self.bonus_moment_squares_unlocked // 4) - 1
        if _extra_squares < 0: _extra_squares = 0
        return self.photo.leader_skill_percentage + (_extra_squares * 3)

    @property
    def leader_skill(self):
        _leader_skill_variables = {
            k: getattr(self.photo, k)
            for k in templateVariables(Photo.LEADER_SKILL_INFO['template'])
        }
        _leader_skill_variables['leader_skill_percentage'] = self.final_leader_skill_percentage
        return Photo.LEADER_SKILL_INFO['template'].format(**_leader_skill_variables)

    CROWN_OPTIONS = [150, 200]
    CROWN_TYPES = [
        'silver',
        'gold',
        'rainbow',
    ]
    CROWN_TEMPLATE = '+{crown_amount} {crown_attribute}'
    SILVER_CROWN_AMOUNT_CHOICES = CROWN_OPTIONS
    i_silver_crown_amount = models.PositiveIntegerField(_('Silver crown bonus'), choices=i_choices(SILVER_CROWN_AMOUNT_CHOICES), null=True)
    SILVER_CROWN_ATTRIBUTE_CHOICES = Photo.LEADER_SKILL_STAT_CHOICES
    i_silver_crown_attribute = models.PositiveIntegerField(_('Silver crown attribute'), choices=i_choices(SILVER_CROWN_ATTRIBUTE_CHOICES), null=True)
    @property
    def silver_crown(self):
        if self.silver_crown_attribute is None: return None
        return CROWN_TEMPLATE.format(**{
            k: getattr(self, 'silver_{}'.format(k))
            for k in templateVariables(CROWN_TEMPLATE)
        })

    GOLD_CROWN_AMOUNT_CHOICES = CROWN_OPTIONS
    i_gold_crown_amount = models.PositiveIntegerField(_('Gold crown bonus'), choices=i_choices(GOLD_CROWN_AMOUNT_CHOICES), null=True)
    GOLD_CROWN_ATTRIBUTE_CHOICES = Photo.LEADER_SKILL_STAT_CHOICES
    i_gold_crown_attribute = models.PositiveIntegerField(_('Gold crown attribute'), choices=i_choices(GOLD_CROWN_ATTRIBUTE_CHOICES), null=True)
    @property
    def gold_crown(self):
        if self.gold_crown_attribute is None: return None
        return CROWN_TEMPLATE.format(**{
            k: getattr(self, 'gold_{}'.format(k))
            for k in templateVariables(CROWN_TEMPLATE)
        })

    RAINBOW_CROWN_AMOUNT_CHOICES = CROWN_OPTIONS
    i_rainbow_crown_amount = models.PositiveIntegerField(_('Rainbow crown bonus'), choices=i_choices(RAINBOW_CROWN_AMOUNT_CHOICES), null=True)
    RAINBOW_CROWN_ATTRIBUTE_CHOICES = Photo.LEADER_SKILL_STAT_CHOICES
    i_rainbow_crown_attribute = models.PositiveIntegerField(_('Rainbow crown attribute'), choices=i_choices(RAINBOW_CROWN_ATTRIBUTE_CHOICES), null=True)
    @property
    def rainbow_crown(self):
        if self.rainbow_crown_attribute is None: return None
        return CROWN_TEMPLATE.format(**{
            k: getattr(self, 'rainbow_{}'.format(k))
            for k in templateVariables(CROWN_TEMPLATE)
        })

    @property
    def crown_dance_boost(self):
        return sum([getattr(self, '{}_crown_amount'.format(v)) for v in CROWN_TYPES
            if getattr(self, '{}_crown_attribute'.format(v)) is 'dance'])
    @property
    def crown_vocal_boost(self):
        return sum([getattr(self, '{}_crown_amount'.format(v)) for v in CROWN_TYPES
            if getattr(self, '{}_crown_attribute'.format(v)) is 'vocal'])
    @property
    def crown_charm_boost(self):
        return sum([getattr(self, '{}_crown_amount'.format(v)) for v in CROWN_TYPES
            if getattr(self, '{}_crown_attribute'.format(v)) is 'charm'])

    custom_dance_stat = models.PositiveIntegerField(_('Dance'), null=True)
    custom_vocal_stat = models.PositiveIntegerField(_('Vocal'), null=True)
    custom_charm_stat = models.PositiveIntegerField(_('Charm'), null=True)

    # pre moment stats
    @property
    def level_dance_stat(self):
        if self.level == 1: return self.photo.dance_min
        if self.level == self.photo.single_max_level: return self.photo.dance_single_copy_max
        if self.level == self.photo.max_max_level: return self.photo.dance_max_copy_max
        if self.level < self.photo.single_max_level:
            return self.photo.dance_min + ((self.level - 1) * self.photo.dance_single_copy_increment)
        return self.photo.dance_single_copy_max + ((self.level - self.photo.single_max_level) * self.photo.dance_combined_increment)
    @property
    def level_vocal_stat(self):
        if self.level == 1: return self.photo.vocal_min
        if self.level == self.photo.single_max_level: return self.photo.vocal_single_copy_max
        if self.level == self.photo.max_max_level: return self.photo.vocal_max_copy_max
        if self.level < self.photo.single_max_level:
            return self.photo.vocal_min + ((self.level - 1) * self.photo.vocal_single_copy_increment)
        return self.photo.vocal_single_copy_max + ((self.level - self.photo.single_max_level) * self.photo.vocal_combined_increment)
    @property
    def level_charm_stat(self):
        if self.level == 1: return self.photo.charm_min
        if self.level == self.photo.single_max_level: return self.photo.charm_single_copy_max
        if self.level == self.photo.max_max_level: return self.photo.charm_max_copy_max
        if self.level < self.photo.single_max_level:
            return self.photo.charm_min + ((self.level - 1) * self.photo.charm_single_copy_increment)
        return self.photo.charm_single_copy_max + ((self.level - self.photo.single_max_level) * self.photo.charm_combined_increment)

    @property
    def moment_squares_unlocked(self):
        return ceil((self.moments_unlocked / 100) * self.photo.rarity_squares_in_moments) + (self.bonus_moment_squares_unlocked if self.photo.rarity is 'UR' else 0)

    # squares go +30 dance->vocal->charm->big square
    @property
    def moment_dance_bonus(self):
        return ceil(self.moment_squares_unlocked / 4) * 30
    @property
    def moment_vocal_bonus(self):
        return ((self.moment_squares_unlocked // 4) + (1 if (self.moment_squares_unlocked % 4) >= 2 else 0)) * 30
    @property
    def moment_charm_bonus(self):
        return ((self.moment_squares_unlocked // 4) + (1 if (self.moment_squares_unlocked % 4) >= 3 else 0)) * 30

    @property
    def display_dance(self):
        if self.custom_dance_stat: self.custom_dance_stat
        return self.level_dance_stat + self.moment_dance_bonus + self.crown_dance_boost
    @property
    def display_vocal(self):
        if self.custom_vocal_stat: self.custom_vocal_stat
        return self.level_vocal_stat + self.moment_vocal_bonus + self.crown_vocal_boost
    @property
    def display_charm(self):
        if self.custom_charm_stat: self.custom_charm_stat
        return self.level_charm_stat + self.moment_charm_bonus + self.crown_charm_boost

    @property
    def total_stats(self):
        return self.display_dance + self.display_vocal + self.display_charm

    def __unicode__(self):
        if self.id:
            return unicode(self.photo)
        return super(CollectiblePhoto, self).__unicode__()
