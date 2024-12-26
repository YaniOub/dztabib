from django.apps import AppConfig


class MedAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MedApp'

    def ready(self):
        import MedApp.signals
