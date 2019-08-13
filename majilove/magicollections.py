from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _, get_language
from magi.magicollections import (
    MagiCollection,
    ActivityCollection as _ActivityCollection,
    BadgeCollection as _BadgeCollection,
    StaffConfigurationCollection as _StaffConfigurationCollection,
    DonateCollection as _DonateCollection,
)
from magi.default_settings import RAW_CONTEXT
from majilove import models, forms
from magi.utils import CuteFormType, staticImageURL, setSubField

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
        'i_astrological_sign': {},
        'i_blood_type': {
            'type': CuteFormType.HTML,
        },
        'i_group': {
            'type': CuteFormType.HTML,
        },
    }

    def to_fields(self, view, item, extra_fields=None, exclude_fields=None, *args, **kwargs):
        if exclude_fields is None: exclude_fields = ['japanese_name', 'japanese_cv_name'] 
        if extra_fields is None: extra_fields = []
        # Make sure weight appears if it is ?
        if item.weight is None:
            item.weight = item.display_weight
        fields = super(IdolCollection, self).to_fields(view, item, *args, icons=IDOLS_ICONS, images={},
            extra_fields=extra_fields, exclude_fields=exclude_fields, **kwargs)

        # Idol Name
        setSubField(fields, 'name', key='type', value='text_annotation')
        setSubField(fields, 'name', key='annotation', value=item.japanese_name)
        if get_language() == 'ja':
            setSubField(fields, 'name', key='value', value=item.japanese_name)
            setSubField(fields, 'name', key='annotation', value=item.name)

        # Idol Voice Actor
        setSubField(fields, 'cv_name', key='type', value='text_annotation')
        setSubField(fields, 'cv_name', key='annotation', value=item.japanese_cv_name)
        if get_language() == 'ja':
            setSubField(fields, 'cv_name', key='value', value=item.japanese_cv_name)
            setSubField(fields, 'cv_name', key='annotation', value=item.cv_name)

        # Other
        setSubField(fields, 'birthday', key='type', value='text')
        setSubField(fields, 'birthday', key='value', value=lambda f: date_format(item.birthday, format='MONTH_DAY_FORMAT', use_l10n=True))
        setSubField(fields, 'height', key='value', value=u'{} cm'.format(item.height))
        setSubField(fields, 'weight', key='value', value=u'{} kg'.format(item.display_weight))
        setSubField(fields, 'description', key='type', value='long_text')
        setSubField(fields, 'color', key='type', value='color')

        return fields
   
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

PHOTO_STATS_FIELDS = [
    u'{}{}'.format(_st, _sf) for _sf in [
        '_min', '_single_copy_max', '_max_copy_max',
    ] for _st in [
        'dance', 'vocal', 'charm', 'overall',
    ]
]

PHOTO_ICONS = {
    'name': 'id',
    'release_date': 'date',
}

PHOTO_IMAGES = {
    'idol': 'mic',
}

PHOTOS_EXCLUDE = [
    'i_skill_type', 'i_leader_skill_stat', 'leader_skill_percentage', 'skill_note_count', 'skill_percentage', 'i_sub_skill_type', 'sub_skill_amount', 'sub_skill_percentage',
] + [
    'image', 'image_special_shot', 'art', 'art_special_shot', 'transparent', 'transparent_special_shot', 'full_photo', 'full_photo_special_shot',
]


PHOTOS_ORDER = [
    'id', 'name', 'idol', 'rarity', 'color', 'release_date', 'skill', 'sub_skill', 'images', 'full_photos', 'arts', 'transparents',
] + PHOTO_STATS_FIELDS

class PhotoCollection(MagiCollection):
    queryset = models.Photo.objects.all()
    title = _('Photo')
    plural_title = _('Photos')
    icon = 'cards'
    navbar_title = _('Photos')
    multipart = True
    form_class = forms.PhotoForm

    reportable = False
    blockable = False
    translated_fields = ('name', 'message_translation')

    def to_fields(self, view, item, *args, **kwargs):
        _photo_images = PHOTO_IMAGES.copy()
        _photo_images.update({
            'color': staticImageURL(item.color, folder='color', extension='png'),
            'rarity': staticImageURL(item.rarity, folder='rarity', extension='png'),
        })
        fields = super(PhotoCollection, self).to_fields(view, item, *args, icons=PHOTO_ICONS, images=_photo_images, **kwargs)
        return fields

    class ItemView(MagiCollection.ItemView):
        def to_fields(self, item, extra_fields=None, exclude_fields=None, order=None, *args, **kwargs):
            if extra_fields is None: extra_fields = []
            if exclude_fields is None: exclude_fields = []
            if order is None: order = PHOTOS_ORDER
            exclude_fields += PHOTOS_EXCLUDE
            extra_fields.append(('skill', {
                'verbose_name': _('Skill'),
                'icon': item.skill_icon,
                'type': 'text',
                'value': item.skill,
            }))
            extra_fields.append(('sub_skill', {
                'verbose_name': _('Sub skill'),
                'type': 'text',
                'value': item.sub_skill,
            }))
            # Add images fields
            for image, verbose_name in [('image', _('Icon')), ('art', _('Poster')), ('transparent', _('Transparent')), ('full_photo', (_('Photo')))]:
                if getattr(item, image):
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
            return super(PhotoCollection.ItemView, self).to_fields(item, *args, extra_fields=extra_fields, exclude_fields=exclude_fields, order=order, **kwargs)


############################################################
