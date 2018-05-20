from django.utils.translation import ugettext_lazy as _
from magi.magicollections import MagiCollection, ActivityCollection as _ActivityCollection, BadgeCollection as _BadgeCollection, StaffConfigurationCollection as _StaffConfigurationCollection, DonateCollection as _DonateCollection
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
    # these fields are all for after views are added
    #navbar_title = _('Characters')
    # want the following as 'microphone' https://www.flaticon.com/free-icon/karaoke-microphone-icon_69364
    #icon = 'microphone'
    #navbar_link_list = 'utapri'
    translated_fields = ('name', 'description', 'instrument', 'hometown', 'hobby')

    form_class = forms.IdolForm

    reportable = False
    blockable = False

############################################################
