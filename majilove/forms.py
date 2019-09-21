from django import forms
from django.conf import settings as django_settings
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.translation import ugettext_lazy as _
from magi.forms import AutoForm, MagiFiltersForm
from majilove import models

class IdolForm(AutoForm):

    def save(self, commit=False):
        instance = super(IdolForm, self).save(commit=False)

        # Set fake year for birthday so filters work
        if instance.birthday:
            instance.birthday = instance.birthday.replace(year=2019)

        if commit:
            instance.save()
        return instance

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

    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)

        for stat, name in models.Photo.ALL_LEADER_STAT_CHOICES:
            setattr(self.instance, 'previous_{}_max_copy_max'.format(stat),
                None if self.is_creating else getattr(self.instance, '{}_max_copy_max'.format(stat))
            )

    def clean_dance_max_copy_max(self):
        _field = self.cleaned_data.get('dance_max_copy_max')
        if self.cleaned_data.get('i_rarity') != 0 and _field is None:
            raise forms.ValidationError(u'This field is required for non-N Photos')
        return _field

    def clean_vocal_max_copy_max(self):
        _field = self.cleaned_data.get('vocal_max_copy_max')
        if self.cleaned_data.get('i_rarity') != 0 and _field is None:
            raise forms.ValidationError(u'This field is required for non-N Photos')
        return _field

    def clean_charm_max_copy_max(self):
        _field = self.cleaned_data.get('charm_max_copy_max')
        if self.cleaned_data.get('i_rarity') != 0 and _field is None:
            raise forms.ValidationError(u'This field is required for non-N Photos')
        return _field

    def save(self, commit=False):
        instance = super(PhotoForm, self).save(commit=False)

        # Set Photo release times to 1AM EST
        for field in ['release_date', 'ww_release_date']:
            date = getattr(instance, field)
            if date:
                setattr(instance, field, date.replace(hour=6, minute=00))

        # Set Photo max copy stat fields if Photo is N
        if instance.i_rarity == 0:
            for stat, name in models.Photo.LEADER_STAT_CHOICES:
                setattr(instance, '{}_max_copy_max'.format(stat), getattr(instance, '{}_max'.format(stat), 0))
                
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
        ('release_date', _('Release date')),
    ] + [
        ('_cache_{}_rank'.format(stat), name) for stat, name in models.Photo.get_leader_stat_choices()
    ] + [
        ('_cache_total_rank', _('Total')),
    ]

    def __init__(self, *args, **kwargs):
        super(PhotoFilterForm, self).__init__(*args, **kwargs)
        
        # Make sure Charm->ACT when lang is Japanese
        if 'i_leader_stat' in self.fields:
            self.fields['i_leader_stat'].choices = BLANK_CHOICE_DASH + models.Photo.get_i_leader_stat_choices() 

        if 'ordering' in self.fields:
            self.fields['ordering'].choices = [
                ('id', _('Album ID')), ('name', _('Name')), ('release_date', _('Release date')),
            ] + [
                ('_cache_{}_rank'.format(stat), name) for stat, name in models.Photo.get_leader_stat_choices()
            ] + [
                ('_cache_total_rank', _('Total')),
            ]

    idol = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(id, full_name) for (id, full_name, image) in getattr(django_settings, 'FAVORITE_CHARACTERS', [])], initial=None, label=_('Idol'))

    class Meta(MagiFiltersForm.Meta):
        model = models.Photo
        fields = ('search', 'idol', 'i_rarity', 'i_attribute', 'i_leader_stat', 'i_skill_type', 'i_sub_skill_type')

