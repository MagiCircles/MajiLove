from magi import forms
from magi.forms import AutoForm
from majilove import models

class IdolForm(AutoForm):
    class Meta(AutoForm.Meta):
        model = models.Idol
        fields = '__all__'
        save_owner_on_creation = True

class PhotoForm(AutoForm):
    class Meta(AutoForm.Meta):
        model = models.Photo
        fields = '__all__'
        save_owner_on_creation = True

