from django.apps import AppConfig


class BeaconmgmtConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'beaconmgmt'
    verbose_name = 'Beacon Academy Management'

    def ready(self):
        pass  # Add any app initialization code here if needed
