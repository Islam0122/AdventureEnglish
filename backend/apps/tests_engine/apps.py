from django.apps import AppConfig


class TypingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tests_engine'
    verbose_name = 'Управления TEST '

    def ready(self):
        import apps.test.signals
