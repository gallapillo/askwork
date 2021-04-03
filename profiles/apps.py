from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'profiles'
    verbose_name = 'Профили'

    def ready(self):
        import profiles.signals