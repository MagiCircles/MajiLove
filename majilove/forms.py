from django.utils.translation import ugettext_lazy as _
from magi import forms
from magi.forms import AutoForm, MagiFiltersForm
from majilove import models

class IdolForm(AutoForm):
    class Meta(AutoForm.Meta):
        model = models.Idol
        fields = '__all__'
        save_owner_on_creation = True

class IdolFilterForm(MagiFiltersForm):
    search_fields = [
        'name', 'japanese_name', 'cv_name', 'japanese_cv_name', 'description', 
        'i_astrological_sign', 'instrument', 'hometown', 'hobby', 'color'
    ]
    search_fields_labels = {'japanese_name': '', 'japanese_cv_name': '',}

    ordering_fields = [
        ('i_group', _('Group')),
        ('name', _('Name')),
        ('cv_name', _('Voice actor')),
        ('birthday', _('Birthday')),
        ('height', _('Height')),
        ('weight', _('Weight')),
        ('color', _('Color')),
    ]

    class Meta(MagiFiltersForm.Meta):
        model = models.Idol
        fields = ('search', 'i_group')


class PhotoForm(AutoForm):
    class Meta(AutoForm.Meta):
        model = models.Photo
        fields = '__all__'
        save_owner_on_creation = True

