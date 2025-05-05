from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from django.apps import apps
from django.db import connection
import os
from django.conf import settings

@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
    """
    Lädt die initialen Tanzdaten nach der Migration.
    Beim Git-Pull werden alle bestehenden Daten gelöscht und neu geladen.
    """
    # Nur ausführen, wenn es sich um die dance-App handelt
    if sender.name == 'dance':
        # Überprüfe, ob die Modelle existieren
        dance_app = apps.get_app_config('dance')
        
        # Wenn die App fertig migriert ist und alle Modelle existieren
        if all(model.__name__ in ['Teacher', 'Course', 'TimeSlot'] 
              for model in dance_app.get_models()):
              
            # Leere alle Tabellen der Dance-App, um doppelte Daten zu vermeiden
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM dance_timeslot")
                cursor.execute("DELETE FROM dance_course")
                cursor.execute("DELETE FROM dance_teacher")
                
            # Zurücksetzen der Sequenzen für PostgreSQL
            if connection.vendor == 'postgresql':
                with connection.cursor() as cursor:
                    cursor.execute("ALTER SEQUENCE dance_teacher_id_seq RESTART WITH 1")
                    cursor.execute("ALTER SEQUENCE dance_course_id_seq RESTART WITH 1")
                    cursor.execute("ALTER SEQUENCE dance_timeslot_id_seq RESTART WITH 1")
            
            # SQLite zurücksetzen
            elif connection.vendor == 'sqlite':
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='dance_teacher'")
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='dance_course'")
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='dance_timeslot'")
            
            # Prüfe, ob dance_data.json im fixtures Verzeichnis existiert
            fixture_path = os.path.join(settings.BASE_DIR, 'dance', 'fixtures', 'dance_data.json')
            if os.path.exists(fixture_path):
                try:
                    # Führe das Management-Kommando aus, um die Daten aus dance_data.json zu laden
                    call_command('loaddata', 'dance_data')
                    print("Tanzdaten aus dance/fixtures/dance_data.json erfolgreich geladen")
                except Exception as e:
                    print(f"Fehler beim Laden von dance_data.json: {str(e)}")
                    # Fallback auf die Standard-Daten, wenn es ein Problem mit dance_data.json gibt
                    call_command('setup_dance_data')
            else:
                # Führe das Standard-Kommando aus, wenn dance_data.json nicht existiert
                call_command('setup_dance_data')
                print("Standard-Tanzdaten wurden geladen (dance_data.json nicht gefunden)")
