from django.utils.translation import ugettext_lazy as _
from magi.magicollections import MagiCollection, ActivityCollection as _ActivityCollection, BadgeCollection as _BadgeCollection, StaffConfigurationCollection as _StaffConfigurationCollection, DonateCollection as _DonateCollection
from magi.default_settings import RAW_CONTEXT
from majilove import models, forms

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

class IdolCollection(MagiCollection):
    queryset = models.Idol.objects.all()
    title = _('Idol')
    plural_title = _('Idols')
    navbar_title = _('Idols')
    image = 'mic'
    translated_fields = ('name', 'description', 'instrument', 'hometown', 'hobby')

    form_class = forms.IdolForm
    multipart = True

    reportable = False
    blockable = False

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
        _photo_images.update({'color': '{static_url}img/color/{value}.png'.format(**{'value':item.color, 'static_url':RAW_CONTEXT['static_url']}),
            'rarity': '{static_url}img/rarity/{value}.png'.format(**{'value':item.rarity, 'static_url':RAW_CONTEXT['static_url']})})
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
