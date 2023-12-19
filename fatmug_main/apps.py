from django.apps import AppConfig

class FatmugMainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fatmug_main'

    def ready(self):
        import fatmug_main.signals  # Import signals inside the ready method
