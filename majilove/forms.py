from django import forms
from django.utils.translation import ugettext_lazy as _
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
    release_date = forms.DateField(label='Release Date', required=False)
    ww_release_date = forms.DateField(label='Release Date (Worldwide)', required=False)

    def save(self, commit=False):
        instance = super(PhotoForm, self).save(commit=False)

        # Set Photo release times to 1AM EST
        for field in ['release_date', 'ww_release_date']:
            date = getattr(instance, field)
            if date:
                setattr(instance, field, date.replace(hour=6, minute=00))
                
        if commit:
            instance.save()
        return instance

    class Meta(AutoForm.Meta):
        model = models.Photo
        fields = '__all__'
        save_owner_on_creation = True

class PhotoFilterForm(MagiFiltersForm):
    search_fields = [
        'name', 'japanese_name', 'message', 'japanese_message',
        'leader_skill', 'japanese_leader_skill',
        'skill', 'japanese_skill',
        'sub_skill', 'japanese_sub_skill',
    ]
    search_fields_labels = {
        'japanese_name': '', 'japanese_message': '',
        'japanese_leader_skill': '', 'japanese_skill': '',
        'japanese_sub_skill': '',
    }

    ordering_fields = [
        ('id', _('Album ID')),
        ('name', _('Name')),  
    ]

    class Meta(MagiFiltersForm.Meta):
        model = models.Photo
        fields = ('search', 'idol', 'i_rarity', 'i_attribute')

