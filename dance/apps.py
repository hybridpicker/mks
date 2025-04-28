from django.apps import AppConfig


class DanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dance'
    
    def ready(self):
        """
        Importiert die Signals, wenn die App geladen wird.
        """
        import dance.signals
