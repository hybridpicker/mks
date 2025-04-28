from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from django.apps import apps

@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
    """
    Lädt die initialen Tanzdaten, wenn die Tabellen leer sind.
    Diese Funktion wird nach jeder Migration ausgeführt.
    """
    # Nur ausführen, wenn es sich um die dance-App handelt
    if sender.name == 'dance':
        # Überprüfe, ob die Modelle existieren und leer sind
        dance_app = apps.get_app_config('dance')
        
        # Wenn die App fertig migriert ist und alle Modelle existieren
        if all(model.__name__ in ['Teacher', 'Course', 'TimeSlot'] 
              for model in dance_app.get_models()):
            # Führe das Management-Kommando aus
            call_command('setup_dance_data')
