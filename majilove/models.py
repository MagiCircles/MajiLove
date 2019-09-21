# -*- coding: utf-8 -*-
from collections import OrderedDict
from math import ceil
from django.conf import settings as django_settings
from django.db import models
from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _, get_language, string_concat
from magi.abstract_models import AccountAsOwnerModel, BaseAccount
from magi.item_model import getInfoFromChoices, i_choices, MagiModel
from magi.models import uploadItem, User
from magi.utils import staticImageURL, templateVariables

############################################################
# Utility stuff

LANGUAGES_NEED_OWN_NAME = [ l for l in django_settings.LANGUAGES if l[0] in ['zh-hans', 'zh-hant'] ]
ALL_ALT_LANGUAGES = [ l for l in django_settings.LANGUAGES if l[0] != 'en' ]
ALT_LANGUAGES_EXCEPT_JP = [ l for l in django_settings.LANGUAGES if l[0] not in ['en', 'ja'] ]

class Account(BaseAccount):
    class Meta:
        pass

############################################################
# Idols

class Idol(MagiModel):
    collection_name = 'idol'
    owner = models.ForeignKey(User, related_name='added_idols')

    name = models.CharField(_('Name'), help_text='in romaji', max_length=100, unique=True)
    japanese_name = models.CharField(string_concat(_('Name'), ' (', _('Japanese'), ')'), max_length=100, unique=True)
    NAMES_CHOICES = LANGUAGES_NEED_OWN_NAME
    NAME_SOURCE_LANGUAGES = ['ja']
    d_names = models.TextField(_('Name'), null=True)

    GROUP_CHOICES = (u'ST☆RISH', 'QUARTET NIGHT')
    i_group = models.PositiveIntegerField(_('Group'), choices=i_choices(GROUP_CHOICES), null=True)

    cv_name = models.CharField(_('Voice actor'), help_text='in romaji', max_length=100, null=True)
    japanese_cv_name = models.CharField(string_concat(_('Voice actor'), ' (', _('Japanese'), ')'), max_length=100, null=True)
    CV_NAMES_CHOICES = LANGUAGES_NEED_OWN_NAME
    CV_NAME_SOURCE_LANGUAGES = ['ja']
    d_cv_names = models.TextField(_('Name'), null=True)

    description = models.TextField(_('Description'), max_length=1000, null=True)
    DESCRIPTIONS_CHOICES = ALL_ALT_LANGUAGES
    d_descriptions = models.TextField(_('Description'), null=True)

    height = models.PositiveIntegerField(_('Height'), help_text='in cm', null=True)
    weight = models.PositiveIntegerField(_('Weight'), help_text='in kg (0 = ?)', null=True)

    BLOOD_TYPE_CHOICES = ('O', 'A', 'B', 'AB', '?')
    i_blood_type = models.PositiveIntegerField(_('Blood Type'), choices=i_choices(BLOOD_TYPE_CHOICES), null=True)

    birthday = models.DateField(_('Birthday'), null=True)

    ASTROLOGICAL_SIGN_CHOICES = (
        ('Leo', _('Leo')), ('Aries', _('Aries')), ('Libra', _('Libra')),
        ('Virgo', _('Virgo')), ('Scorpio', _('Scorpio')), ('Capricorn', _('Capricorn')),
        ('Pisces', _('Pisces')), ('Gemini', _('Gemini')), ('Cancer', _('Cancer')),
        ('Sagittarius', _('Sagittarius')), ('Aquarius', _('Aquarius')), ('Taurus', _('Taurus')),
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

    color = models.CharField('Color', help_text='Format: #XXXXXX', max_length=7)
    image = models.ImageField(_('Image'), upload_to=uploadItem('idol'))

    def __unicode__(self):
        return unicode(self.t_name)

    ############################################################
    # Display Fields

    display_birthday = property(lambda f: date_format(f.birthday, format='MONTH_DAY_FORMAT', use_l10n=True))
    display_height = property(lambda f: u'{} cm'.format(f.height))
    display_weight = property(lambda f: u'{} kg'.format('?' if f.weight == 0 else f.weight))

    ############################################################
    # Reverse relations

    reverse_related = (
        { 'field_name': 'photos', 'verbose_name': _('Photos') },
    )

############################################################
# Photos

class Photo(MagiModel):
    collection_name = 'photo'
    owner = models.ForeignKey(User, related_name='added_photos')

    id = models.PositiveIntegerField(_('Album ID'), unique=True, primary_key=True, db_index=True)

    name = models.CharField(_('Name'), max_length=100, null=True)
    japanese_name = models.CharField(string_concat(_('Name'), ' (', _('Japanese'), ')'), max_length=100, null=True)
    NAME_SOURCE_LANGUAGES = ['ja']
    NAMES_CHOICES = ALT_LANGUAGES_EXCEPT_JP
    d_names = models.TextField(_('Name'), null=True)

    # Note: JST and EST (1AM)
    release_date = models.DateTimeField(_('Release date'), null=True, db_index=True)
    ww_release_date = models.DateTimeField(string_concat(_('Release date'), ' (', _('English version'), ')'), null=True)

    idol = models.ForeignKey(Idol, verbose_name=_('Idol'), related_name='photos', db_index=True)

    RARITIES = OrderedDict([
        ('N', {
            'special_shot_percentage': None,
            'outfit_unlock_percentage': 0,
            'squares_in_moments' : 4,
            'max_levels': [20],
            }),
        ('R', {
            'special_shot_percentage': 100,
            'outfit_unlock_percentage': 50,
            'squares_in_moments' : 16,
            'max_levels': [30, 50],
            }),
        ('SR', {
            'special_shot_percentage': 83,
            'outfit_unlock_percentage': 33,
            'squares_in_moments' : 24,
            'max_levels': [40, 60],
            }),
        ('UR', {
            'special_shot_percentage': 87,
            'outfit_unlock_percentage': 25,
            'squares_in_moments': 32,
            'max_levels': [50, 70],
        }),
    ])
    RARITY_CHOICES = [(_name, _name) for _name, _info in RARITIES.items()]
    i_rarity = models.PositiveIntegerField(_('Rarity'), choices=i_choices(RARITY_CHOICES), db_index=True)

    ATTRIBUTE_CHOICES = [('star', _('Star')), ('shine', _('Shine')), ('dream', _('Dream'))]
    i_attribute = models.PositiveIntegerField(_('Attribute'), choices=i_choices(ATTRIBUTE_CHOICES), db_index=True)

    ############################################################
    # Images

    # Icon
    image = models.ImageField(_('Icon'), upload_to=uploadItem('photo/icon'), null=True)
    image_special_shot = models.ImageField(string_concat(_('Icon'), ' (', _('Special shot'), ')'), upload_to=uploadItem('photo/icon/specialshot'), null=True)

    # Photo
    photo = models.ImageField(_('Photo'), upload_to=uploadItem('photo'))
    photo_special_shot = models.ImageField(string_concat(_('Photo'), ' (', _('Special shot'), ')'), upload_to=uploadItem('photo/specialshot'), null=True)

    # Transparent
    transparent = models.ImageField(_('Transparent'), upload_to=uploadItem('photo/transparent'), null=True)
    transparent_special_shot = models.ImageField(string_concat(_('Transparent'), ' (', _('Special shot'), ')'), upload_to=uploadItem('photo/transparent/specialshot'), null=True)

    # Poster
    art = models.ImageField(_('Poster'), upload_to=uploadItem('photo/poster'), null=True)
    art_special_shot = models.ImageField(string_concat(_('Poster'), ' (', _('Special shot'), ')'), upload_to=uploadItem('photo/poster/specialshot'), null=True)

    # Other
    autograph = models.ImageField(_('Autograph'), upload_to=uploadItem('photo/autograph'), null=True)
    message_image = models.ImageField(_('Message'), upload_to=uploadItem('photo/message'), null=True)

    message = models.TextField(_('Message'), max_length=500, null=True)
    japanese_message = models.TextField(string_concat(_('Message'), ' (', _('Japanese'),  ')'), max_length=500, null=True)
    MESSAGE_SOURCE_LANGUAGES = ['ja']
    MESSAGES_CHOICES = ALT_LANGUAGES_EXCEPT_JP
    d_messages = models.TextField(_('Message'), null=True)

    ############################################################
    # Photo Stats

    dance_min = models.PositiveIntegerField(string_concat(_('Dance'), ' (', _('Minimum'), ')'))
    dance_max = models.PositiveIntegerField(string_concat(_('Dance'), ' (', _('Single copy maximum'), ')'))
    dance_max_copy_max = models.PositiveIntegerField(string_concat(_('Dance'), ' (', _('Maxed copy maximum'), ')'), null=True)

    vocal_min = models.PositiveIntegerField(string_concat(_('Vocal'), ' (', _('Minimum'), ')'))
    vocal_max = models.PositiveIntegerField(string_concat(_('Vocal'), ' (', _('Single copy maximum'), ')'))
    vocal_max_copy_max = models.PositiveIntegerField(string_concat(_('Vocal'), ' (', _('Maxed copy maximum'), ')'), null=True)

    charm_min = models.PositiveIntegerField(string_concat(_('Charm'), ' (', _('Minimum'), ')'))
    charm_max = models.PositiveIntegerField(string_concat(_('Charm'), ' (', _('Single copy maximum'), ')'))
    charm_max_copy_max = models.PositiveIntegerField(string_concat(_('Charm'), ' (', _('Maxed copy maximum'), ')'), null=True)

    total_min = property(lambda f: f.dance_min + f.vocal_min + f.charm_min)
    total_max = property(lambda f: f.dance_max + f.vocal_max + f.charm_max)
    total_max_copy_max = property(lambda f: f.dance_max_copy_max + f.vocal_max_copy_max + f.charm_max_copy_max)
        
    ############################################################
    # Skills

    # Leader Skill
    LEADER_STATS = OrderedDict([
        ('dance', {
            'translation': _('Dance'),
            'japanese_translation': u'DANCE'
        }),
        ('vocal', {
            'translation': _('Vocal'),
            'japanese_translation': u'VOCAL'
        }),
        ('charm', {
            'translation': _('Charm'),
            'japanese_translation': u'ACT'
        })
    ])
    LEADER_STAT_CHOICES = [(_name, _info['translation']) for _name, _info in LEADER_STATS.items()]
    JAPANESE_LEADER_STAT_CHOICES = [(_name, _info['japanese_translation']) for _name, _info in LEADER_STATS.items()]
    ALL_LEADER_STAT_CHOICES = LEADER_STAT_CHOICES + [('total', _('Total'))]

    i_leader_stat = models.PositiveIntegerField(_('Leader Skill'), choices=i_choices(LEADER_STAT_CHOICES), null=True)
    japanese_leader_stat = property(getInfoFromChoices('stat', LEADER_STATS, 'japanese_translation'))
    t_leader_stat = property(lambda f: f.japanese_stat if get_language() == 'ja' else MagiModel.t_stat.fget(f))

    # Fetches the correct translation of stats for forms
    @classmethod
    def get_leader_stat_choices(self):
        return self.JAPANESE_LEADER_STAT_CHOICES if get_language() == 'ja' else self.LEADER_STAT_CHOICES
    @classmethod
    def get_i_leader_stat_choices(self):
        return i_choices(self.JAPANESE_LEADER_STAT_CHOICES if get_language() == 'ja' else self.LEADER_STAT_CHOICES)

    LEADER_SKILL_INFO = {
        'template': _(u'{t_attribute} {t_leader_stat} +{leader_skill_percentage}%'),
        'japanese_template': u'{t_attribute}の{t_leader_stat}パフォーマンス{leader_skill_percentage}%上昇',
    }   
    leader_skill_percentage = models.PositiveIntegerField(string_concat(_('Leader Skill'), ' %'), null=True)

    @property
    def leader_skill(self):
        if self.leader_stat is None: return None
        return self.LEADER_SKILL_INFO['template'].format(**{
            k: getattr(self, k, '')
            for k in templateVariables(self.LEADER_SKILL_INFO['template'])
        })

    @property
    def japanese_leader_skill(self):
        if self.leader_stat is None: return None
        return self.LEADER_SKILL_INFO['japanese_template'].format(**{
            k: getattr(self, k, '')
            for k in templateVariables(self.LEADER_SKILL_INFO['template'])
        })

    # Main Skill
    SKILL_TYPES = OrderedDict([
        ('score_notes', {
            'translation': _(u'Score notes'),
            'japanese_translation': u'スコアノーツ',
            'icon': 'scoreup',
            'increment': 1,
            'template': _(u'Score Notes +{skill_note_count}'),
            'japanese_template': u'スコアノーツを{skill_note_count}個追加',
        }),
        ('perfect_score', {
            'translation': _(u'Perfect score up'),
            'japanese_translation': u'JUST PERFECTのスコア',
            'icon': 'scoreup',
            'increment': 0.3,
            'template': _(u'Perfect Score +{skill_percentage}%'),
            'japanese_template': u'JUST PERFECTのスコア{skill_percentage}%上昇',
        }),
        ('cutin', {
            'translation': _(u'Cut-in'),
            'japanese_translation': u'カットイン',
            'icon': 'scoreup',
            'increment': 10,
            'template': _(u'Cut-in Bonus Score +{skill_percentage_int}%'),
            'japanese_template': u'カットインボーナスのスコア{skill_percentage_int}%上昇',
        }),
        ('good_lock', {
            'translation': _('{note_type} lock').format(note_type=string_concat(_('Good'), '(WW)/', _('Great'), '(JP)')),
            'japanese_translation': u'BADをGREATに',
            'icon': 'perfectlock',
            'increment': 1,
            'template': _(u'Bad > Good ({skill_note_count} Times)'),
            'japanese_template': u'BADを{skill_note_count}回GREATにする',
        }),
        ('great_lock', {
            'translation': _('{note_type} lock').format(note_type=string_concat(_('Great'), '(WW)/', _('Perfect'), '(JP)')),
            'japanese_translation': u'BAD、GREATをPERFECTに',
            'icon': 'perfectlock',
            'increment': 1,
            'template': _(u'Bad/Good > Great ({skill_note_count} Times)'),
            'japanese_template': u'BAD,GREATを{skill_note_count}回PERFECTにする',
        }),
        ('healer', {
            'translation': _(u'Healer'),
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

    skill_note_count = models.PositiveIntegerField('Skill Note Count', null=True)
    skill_percentage = models.FloatField('Skill %', null=True)
    skill_percentage_int = property(lambda _a: int(_a.skill_percentage))

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

    # Sub Skill
    SUB_SKILL_TYPES = OrderedDict([
        ('full_combo', {
            'translation': _(u'Full combo'),
            'japanese_translation': u'フルコンボ',
            'template': _(u'+{sub_skill_amount} score when clearing a song with a Full Combo'),
            'japanese_template': u'フルコンボクリア時+{sub_skill_amount}スコア',
        }),
        ('stamina', {
            'translation': _(u'Stamina based'),
            'japanese_translation': u'LIFEでクリア時',
            'template': _(u'+{sub_skill_amount} score when clearing a song with {sub_skill_percentage}% Stamina'),
            'japanese_template': u'LIFE{sub_skill_percentage}%以上でクリア時+{sub_skill_amount}スコア',
        }),
    ])
    SUB_SKILL_VARIABLES = ['sub_skill_percentage', 'sub_skill_amount']

    SUB_SKILL_TYPE_CHOICES = [(_name, _info['translation']) for _name, _info in SUB_SKILL_TYPES.items()]
    i_sub_skill_type = models.PositiveIntegerField(_('Sub skill'), choices=i_choices(SUB_SKILL_TYPE_CHOICES), null=True)
    japanese_sub_skill_type = property(getInfoFromChoices('sub_skill_type', SUB_SKILL_TYPES, 'japanese_translation'))

    sub_skill_amount = models.PositiveIntegerField('Sub Skill Amount', null=True)
    sub_skill_percentage = models.FloatField('Sub Skill %', null=True)
    sub_skill_increment = models.PositiveIntegerField('Sub Skill Level Up Increment', null=True)

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

    ############################################################
    # Caches

    # Idol
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

    # Stats
    _cache_dance_rank = models.PositiveIntegerField(null=True)
    _cache_vocal_rank = models.PositiveIntegerField(null=True)
    _cache_charm_rank = models.PositiveIntegerField(null=True)
    _cache_total_rank = models.PositiveIntegerField(null=True)

    _cache_dance_rank_update_on_none = True
    _cache_vocal_rank_update_on_none = True
    _cache_charm_rank_update_on_none = True
    _cache_total_rank_update_on_none = True

    def to_cache_dance_rank(self):
        return type(self).objects.filter(dance_max_copy_max__gt=self.dance_max_copy_max).values('dance_max_copy_max').distinct().count() + 1

    def to_cache_vocal_rank(self):
        return type(self).objects.filter(vocal_max_copy_max__gt=self.vocal_max_copy_max).values('vocal_max_copy_max').distinct().count() + 1

    def to_cache_charm_rank(self):
        return type(self).objects.filter(charm_max_copy_max__gt=self.charm_max_copy_max).values('charm_max_copy_max').distinct().count() + 1

    def to_cache_total_rank(self):
        rank = 1
        for obj in type(self).objects.distinct():
            if self.total_max_copy_max < obj.total_max_copy_max:
                rank += 1
        return rank

    ############################################################
    # Miscellaneous

    rarity_max_levels = property(getInfoFromChoices('rarity', RARITIES, 'max_levels'))
    rarity_special_shot_percentage = property(getInfoFromChoices('rarity', RARITIES, 'special_shot_percentage'))
    rarity_squares_in_moments = property(getInfoFromChoices('rarity', RARITIES, 'squares_in_moments'))

    COMBINABLE_RARITIES = ['R', 'SR', 'UR']
    combinable = property(lambda f: f.rarity in f.COMBINABLE_RARITIES)
    single_max_level = property(lambda f: f.rarity_max_levels[0] if self.combinable else self.rarity_max_levels)
    max_max_level = property(lambda f: f.rarity_max_levels[1] if self.combinable else f.rarity_max_levels)

    dance_single_copy_increment = property(lambda f: float(f.dance_max - f.dance_min)/(f.single_max_level - 1))
    vocal_single_copy_increment = property(lambda f: float(f.vocal_max - f.dance_min)/(f.vocal_max_level - 1))
    charm_single_copy_increment = property(lambda f: float(f.charm_max - f.charm_min)/(f.charm_max_level - 1))

    dance_combined_increment = property(lambda f: float(f.dance_max_copy_max - f.dance_max)/(f.max_max_level - f.single_max_level))
    vocal_combined_increment = property(lambda f: float(f.vocal_max_copy_max - f.vocal_max)/(f.max_max_level - f.single_max_level))
    charm_combined_increment = property(lambda f: float(f.charm_max_copy_max - f.charm_max)/(f.max_max_level - f.single_max_level))

    def __unicode__(self):
        if self.id:
            return u'{rarity} {idol_name} {name}'.format(
                rarity=self.rarity,
                idol_name=self.cached_idol.t_name if self.cached_idol else '',
                name=string_concat('- ', self.t_name) if self.t_name is not None else '',
            )
        return u''

############################################################
# Collectible Photos
# Model not recently tested

''' class CollectiblePhoto(AccountAsOwnerModel):
    collection_name = 'collectiblephoto'

    account = models.ForeignKey(Account, verbose_name=_('Account'), related_name='photoscollectors')
    photo = models.ForeignKey(Photo, verbose_name=_('Photo'), related_name='collectedphotos')
    level = models.PositiveIntegerField(_('Level'), default=1)
    leader_bonus = models.PositiveIntegerField(_('Leader skill percentage'), null=True)
    skill_level = models.PositiveIntegerField(_('Skill level'), default=1)

    @property
    def skill_percentage(self):
        return self.photo.skill_percentage + (self.skill_level - 1) * self.photo.skill_increment
    @property
    def skill_note_count(self):
        return self.photo.skill_note_count + (self.skill_level - 1) * self.photo.skill_increment

    @property
    def skill(self):
        return self.photo.skill_template.format({
            k: getattr(self, k)
            for k in templateVariables(self.photo.skill_template)
        })

    sub_skill_level = models.PositiveIntegerField(_('Sub skill level'), null=True)
    @property
    def sub_skill_amount(self):
        return self.photo.sub_skill_amount + (self.sub_skill_level - 1) * self.photo.sub_skill_increment

    @property
    def sub_skill(self):
        _sub_skill_variables = {k: getattr(self.photo, k)
        for k in templateVariables(self.photo.sub_skill_template
        )}
        _sub_skill_variables['sub_skill_amount'] = self.sub_skill_amount
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

    CROWN_OPTIONS = [150, 200] #Now only 200; change this to a variable
    CROWN_TYPES = [
        'silver',
        'gold',
        'rainbow',
    ]
    CROWN_TEMPLATE = '+{crown_amount} {crown_attribute}'
    SILVER_CROWN_AMOUNT_CHOICES = CROWN_OPTIONS
    i_silver_crown_amount = models.PositiveIntegerField(_('Silver crown bonus'), choices=i_choices(SILVER_CROWN_AMOUNT_CHOICES), null=True)
    SILVER_CROWN_ATTRIBUTE_CHOICES = Photo.LEADER_STAT_CHOICES
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
    GOLD_CROWN_ATTRIBUTE_CHOICES = Photo.LEADER_STAT_CHOICES
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
    RAINBOW_CROWN_ATTRIBUTE_CHOICES = Photo.LEADER_STAT_CHOICES
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
        if self.level == self.photo.single_max_level: return self.photo.dance_max
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

 '''