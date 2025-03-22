from django.apps import AppConfig


class EntryExitAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'entry_exit_app'

    def ready(self):
        import entry_exit_app.signals