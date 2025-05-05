from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
from django.conf import settings
from django.db import connection
from dance.models import Teacher, Course, TimeSlot

class Command(BaseCommand):
    help = 'Lädt die Tanzdaten aus der dance_fixture.json Datei in die Datenbank'

    def add_arguments(self, parser):
        parser.add_argument(
            '--preserve',
            action='store_true',
            help='Bestehende Daten beibehalten und nicht löschen',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Lade Tanzdaten aus dance/fixtures/dance_data.json...'))
        
        # Prüfe, ob die Fixture-Datei existiert
        fixture_path = os.path.join(settings.BASE_DIR, 'dance', 'fixtures', 'dance_data.json')
        
        if not os.path.exists(fixture_path):
            self.stdout.write(self.style.ERROR(f'Fixture-Datei nicht gefunden: {fixture_path}'))
            return

        # Wenn preserve nicht gewählt wurde, lösche bestehende Daten
        if not options['preserve']:
            self.stdout.write(self.style.WARNING('Lösche bestehende Tanzdaten...'))
            
            # Lösche alle Daten aus den Tabellen
            TimeSlot.objects.all().delete()
            Course.objects.all().delete()
            Teacher.objects.all().delete()
            
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
        
        # Lade das Fixture
        try:
            call_command('loaddata', 'dance_data')
            
            # Zähle die Datensätze
            teacher_count = Teacher.objects.count()
            course_count = Course.objects.count()
            timeslot_count = TimeSlot.objects.count()
            
            self.stdout.write(self.style.SUCCESS(
                f'Tanzdaten erfolgreich geladen! '
                f'Lehrer: {teacher_count}, '
                f'Kurse: {course_count}, '
                f'Zeitfenster: {timeslot_count}'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Fehler beim Laden des Fixtures: {str(e)}'))
            
            # Versuche, die Fixture-Datei direkt zu validieren
            self.stdout.write(self.style.WARNING('Überprüfe die Fixture-Datei auf Fehler...'))
            try:
                call_command('loaddata', fixture_path, verbosity=2, dry_run=True)
                self.stdout.write(self.style.WARNING('Fixture-Datei scheint in Ordnung zu sein, aber konnte nicht geladen werden.'))
            except Exception as validation_error:
                self.stdout.write(self.style.ERROR(f'Fehler in der Fixture-Datei: {str(validation_error)}'))
