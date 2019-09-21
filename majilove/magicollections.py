from django.db.models import Prefetch, Q
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _, get_language, string_concat
from magi.magicollections import (
    ActivityCollection as _ActivityCollection,
    BadgeCollection as _BadgeCollection,
    StaffConfigurationCollection as _StaffConfigurationCollection,
    DonateCollection as _DonateCollection,
    MagiCollection,
)
from magi.default_settings import RAW_CONTEXT
from magi.item_model import i_choices
from magi.utils import custom_item_template, CuteFormType, FAVORITE_CHARACTERS_IMAGES, jsv, setSubField, staticImageURL
from majilove import forms, models

############################################################
# Activities

class ActivityCollection(_ActivityCollection):
    enabled = False

############################################################
# Badge Collection

class BadgeCollection(_BadgeCollection):
    enabled = True

############################################################
# Staff Configuration Collection

class StaffConfigurationCollection(_StaffConfigurationCollection):
    enabled = True

############################################################
# Donate Collection

class DonateCollection(_DonateCollection):
    enabled = True

############################################################
# Idol Collection

IDOLS_ICONS = {
    'name': 'id', 'cv_name': 'voice-actor',
    'group': 'users', 'description': 'author',
    'height': 'measurements', 'weight': 'measurements',
    'blood_type': 'hp', 'birthday': 'birthday',
    'astrological_sign': 'star',
    'instrument': 'guitar', 'hometown': 'town',
    'hobby': 'hobbies', 'color': 'palette',
    'photos': 'cards',
}

class IdolCollection(MagiCollection):
    queryset = models.Idol.objects.all()
    title = _('Idol')
    plural_title = _('Idols')
    image = 'mic'
    translated_fields = ('name', 'cv_name', 'description', 'instrument', 'hometown', 'hobby')
    form_class = forms.IdolForm
    reportable = False
    blockable = False
  
    filter_cuteform = {
        'i_blood_type': {'type': CuteFormType.HTML},
        'i_group': {'type': CuteFormType.HTML},
    }
    fields_icons = IDOLS_ICONS
    fields_exclude = ['japanese_name', 'japanese_cv_name']

    def to_fields(self, view, item, *args, **kwargs):
        fields = super(IdolCollection, self).to_fields(view, item, *args, **kwargs)

        setSubField(fields, 'name', key='type', value='text_annotation')
        setSubField(fields, 'name', key='annotation', value=item.name if get_language() == 'ja' else item.japanese_name)
        setSubField(fields, 'cv_name', key='type', value='text_annotation')
        setSubField(fields, 'cv_name', key='annotation', value=item.cv_name if get_language() == 'ja' else item.japanese_cv_name)
        setSubField(fields, 'color', key='type', value='color')

        return fields

    class ItemView(MagiCollection.ItemView):
        fields_prefetched_together = ['photos'] 
   
    class ListView(MagiCollection.ListView):
        filter_form = forms.IdolFilterForm
        per_line = 6
        page_size = 20
        default_ordering = 'i_group'

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']
        allow_delete = True

############################################################
# Photo Collection

PHOTO_ADD_EDIT_CUTEFORM = {
    'idol': {
        'to_cuteform': lambda k, v: v.image_url,
        'title': _('Idol'),
        'extra_settings': {
            'modal': 'true',
            'modal-text': 'true',
        },
    },
    'i_rarity': {},
    'i_attribute': {},
    'i_leader_stat': {
        'type': CuteFormType.HTML,
        'to_cuteform': lambda k, v: format_html(u'<span data-toggle="tooltip" title="{}">{}</div>', unicode(v), v[0]),
    },
}
PHOTO_CUTEFORM = PHOTO_ADD_EDIT_CUTEFORM.copy()
PHOTO_CUTEFORM['idol'] = {
    'to_cuteform': lambda k, v: FAVORITE_CHARACTERS_IMAGES[k],
    'title': _('Idol'),
    'extra_settings': {
        'modal': 'true',
        'modal-text': 'true',
    },
}

PHOTO_STATS_FIELDS = [
    u'{}_{}'.format(_st, _sf) for _sf in [
        'min', 'max', 'max_copy_max',
    ] for _st in [
        'dance', 'vocal', 'charm', 'total'
    ]
]

PHOTO_ICONS = {
    'name': 'id',
    'release_date': 'date',
    'ww_release_date': 'world',
    'message_image': 'love-letter',
    'message': 'love-letter',
    'autograph': 'author',
}

PHOTO_IMAGES = {
    'idol': 'mic.png',
    'attribute': lambda _i: staticImageURL(_i.i_attribute, folder='i_attribute', extension='png'),
    'rarity': lambda _i: staticImageURL(_i.i_rarity, folder='i_rarity', extension='png'),
}

PHOTO_EXCLUDE = [
    'i_skill_type', 'i_leader_stat', 'leader_skill_percentage',
    'skill_note_count', 'skill_percentage', 'i_sub_skill_type',
    'sub_skill_amount', 'sub_skill_percentage', 'sub_skill_increment',
    'image', 'image_special_shot', 'art', 'art_special_shot',
    'transparent', 'transparent_special_shot', 'photo', 'photo_special_shot',
    'japanese_name',
] + PHOTO_STATS_FIELDS


PHOTO_ORDER = [
    'id', 'name', 'idol', 'rarity', 'attribute', 'release_date',
    'ww_release_date', 'skill', 'sub_skill', 'leader_skill',
    'images', 'photos', 'arts', 'transparents', 'autograph',
    'message_image', 'message', 
]

class PhotoCollection(MagiCollection):
    queryset = models.Photo.objects.all()
    title = _('Photo')
    plural_title = _('Photos')
    icon = 'cards'
    multipart = True
    form_class = forms.PhotoForm
    reportable = False
    blockable = False
    translated_fields = ('name', 'message')

    filter_cuteform = PHOTO_CUTEFORM
    fields_icons = PHOTO_ICONS
    fields_images = PHOTO_IMAGES

    def to_fields(self, view, item, *args, **kwargs):
        fields = super(PhotoCollection, self).to_fields(view, item, *args, **kwargs)

        # Name
        setSubField(fields, 'name', key='type', value='text_annotation')
        setSubField(fields, 'name', key='annotation', value=item.japanese_name if item.japanese_name is not None else '')
        if item.t_name != item.name:
            setSubField(fields, 'name', key='annotation', value=item.name or '')

        # Release Date
        if item.ww_release_date:
            setSubField(fields, 'release_date', key='icon', value='jp')
            setSubField(fields, 'release_date', key='verbose_name_subtitle', value=_('Japanese version'))
        setSubField(fields, 'ww_release_date', key='verbose_name', value= _('Release date'))
        setSubField(fields, 'ww_release_date', key='verbose_name_subtitle', value=_('Worldwide version'))
        return fields

    def after_save(self, request, instance, type=None):
        super(PhotoCollection, self).after_save(request, instance, type=type)
        previous = None
        for stat, name in models.Photo.ALL_LEADER_STAT_CHOICES:
            previous = getattr(instance, 'previous_{}_max_copy_max'.format(stat), None)
            if previous != getattr(instance, '{}_max_copy_max'.format(stat), None):
                for photo in models.Photo.objects.distinct():
                    photo.force_update_cache('{}_rank'.format(stat))
        return instance

    class ItemView(MagiCollection.ItemView):
        top_illustration='items/photoItem'
        ajax_callback = 'loadPhoto'
        fields_exclude = PHOTO_EXCLUDE
        fields_order = PHOTO_ORDER

        def to_fields(self, item, extra_fields=None, *args, **kwargs):
            if extra_fields == None: extra_fields = []
            extra_fields.append(('id', {
                'verbose_name': _('Album ID'),
                'icon': 'id',
                'type': 'text',
                'value': item.id,
            }))
            if item.skill:
                extra_fields.append(('skill', {
                    'verbose_name': _('Skill'),
                    'icon': item.skill_icon,
                    'type': 'text',
                    'value': item.japanese_skill if get_language() == 'ja' else item.skill,
                }))
            if item.sub_skill:
                extra_fields.append(('sub_skill', {
                    'verbose_name': _('Sub skill'),
                    'icon': 'category',
                    'type': 'text',
                    'value': item.japanese_sub_skill if get_language() == 'ja' else item.sub_skill,
                }))
            if item.leader_skill:
                extra_fields.append(('leader_skill', {
                    'verbose_name': _('Leader skill'),
                    'icon': 'statistics',
                    'type': 'text',
                    'value': item.japanese_leader_skill if get_language() == 'ja' else item.leader_skill,
                }))
            # Add images fields
            for image, verbose_name in [('image', _('Icon')), ('art', _('Poster')), ('transparent', _('Transparent')), ('photo', (_('Photo')))]:
                if getattr(item, image, None):
                    print 'adding the thing'
                    extra_fields.append((u'{}s'.format(image), {
                        'verbose_name': verbose_name,
                        'type': 'images',
                        'images': [{
                            'value': image_url,
                            'verbose_name': verbose_name,
                        } for image_url in [
                            getattr(item, u'{}_url'.format(image)),
                            getattr(item, u'{}_special_shot_url'.format(image)),
                        ] if image_url],
                        'icon': 'pictures',
                    }))
            extra_fields.append((u'ranking', {
                'verbose_name': _('Ranking'),
                'type': 'list',
                'value': [string_concat(name + ': #' + unicode(getattr(item, 'cached_{}_rank'.format(stat), '???')))
                    for stat, name in models.Photo.LEADER_STAT_CHOICES],
                'icon': 'leaderboard',
            }))
                
            fields = super(PhotoCollection.ItemView, self).to_fields(item, extra_fields=extra_fields, *args, **kwargs)
            return fields

    class ListView(MagiCollection.ListView):
        item_template = custom_item_template
        filter_form = forms.PhotoFilterForm
        per_line = 3
        page_size = 12
        default_ordering = '-id'

        def ordering_fields(self, item, only_fields=None, *args, **kwargs):
            fields = super(PhotoCollection.ListView, self).ordering_fields(item, *args, only_fields=only_fields, **kwargs)
            for stat, name in models.Photo.get_leader_stat_choices():
                if '_cache_{}_rank'.format(stat) in only_fields:
                    fields['{}_max_copy_max'.format(stat)] = {
                        'verbose_name': name,
                        'verbose_name_subtitle': _('Ranking'),
                        'icon': 'leaderboard',
                        'type': 'text_annotation',
                        'value': getattr(item, '{}_max_copy_max'.format(stat), '???'),
                        'annotation': string_concat('#', getattr(item, 'cached_{}_rank'.format(stat), '???')),
                    }
            if '_cache_total_rank'.format(stat) in only_fields:
                fields['total_max_copy_max'] = {
                    'verbose_name': _('Total'),
                    'verbose_name_subtitle': _('Ranking'),
                    'icon': 'leaderboard',
                    'type': 'text_annotation',
                    'value': getattr(item, 'total_max_copy_max', '???'),
                    'annotation': string_concat('#', getattr(item, 'cached_total_rank', '???')),
                }
            return fields

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']
        ajax_callback = 'loadPhotoForm'
        filter_cuteform = PHOTO_ADD_EDIT_CUTEFORM

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']
        allow_delete = True
        ajax_callback = 'loadPhotoForm'
        filter_cuteform = PHOTO_ADD_EDIT_CUTEFORM

############################################################
