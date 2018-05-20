from django.utils.translation import ugettext_lazy as _
from django.utils.formats import dateformat
from magi.magicollections import MagiCollection, ActivityCollection as _ActivityCollection, BadgeCollection as _BadgeCollection, StaffConfigurationCollection as _StaffConfigurationCollection, DonateCollection as _DonateCollection
from magi.utils import setSubField
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

IDOL_ICONS = {
    'name': 'id',
    'japanese_name': 'id',
    'voice_actor_name': 'profile',
    'romaji_voice_actor_name': 'profile',
    'birthday': 'event',
    'instrument': 'song',
    'description': 'id',
    'astrological_sign': 'idolized',
    'hometown': 'world',
    'height': 'scoreup',
}

IDOL_ORDER =[
    'name',
    'japanese_name',
    'romaji_voice_actor_name',
    'voice_actor_name',
    'height',
    'display_weight',
    'display_blood_type',
    'birthday',
    'astrological_sign',
    'instrument',
    'hometown',
    'description',
]

class IdolCollection(MagiCollection):
    queryset = models.Idol.objects.all()
    title = _('Idol')
    plural_title = _('Idols')
    # these fields are all for after views are added
    #navbar_title = _('Characters')
    # want the following as 'microphone' https://www.flaticon.com/free-icon/karaoke-microphone-icon_69364
    #icon = 'microphone'
    #navbar_link_list = 'utapri'
    translated_fields = ('name', 'description', 'instrument', 'hometown')

    form_class = forms.IdolForm

    reportable = False
    blockable = False

    def to_fields(self, view, item, exclude_fields=None, extra_fields=None, order=None, *args, **kwargs):
        if exclude_fields is None: exclude_fields = []
        if extra_fields is None: extra_fields = []
        if order is None: order = IDOL_ORDER
        exclude_fields += ['d_names', 'weight', 'blood_type']
        extra_fields.append(('display_weight', {
            'verbose_name': _(u'Weight'),
            'icon': 'scoreup',
            'value': item.display_weight,
            'type': 'text'
            }))
        extra_fields.append(('display_blood_type', {
            'verbose_name': _(u'Blood type'),
            'icon': 'hp',
            'value': item.display_blood_type,
            'type': 'text'
            }))
        fields = super(IdolCollection, self).to_fields(view, item, *args, icons=IDOL_ICONS,
            exclude_fields=exclude_fields, extra_fields=extra_fields, order=order, **kwargs)
        setSubField(fields, 'height', key='value', value='{} cm'.format(item.height))
        setSubField(fields, 'description', key='type', value='long_text')
        setSubField(fields, 'birthday', key='type', value='text')
        setSubField(fields, 'birthday', key='value', value=lambda f: dateformat.format(item.birthday, "F d"))
        return fields
############################################################
