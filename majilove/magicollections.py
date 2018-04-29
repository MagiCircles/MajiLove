from magi.magicollections import MagiCollection, ActivityCollection as _ActivityCollection, BadgeCollection as _BadgeCollection, StaffConfigurationCollection as _StaffConfigurationCollection, DonateCollection as _DonateCollection

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
############################################################
