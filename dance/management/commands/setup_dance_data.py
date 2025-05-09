from django.core.management.base import BaseCommand
from django.core.management import call_command
from dance.models import Teacher, Course, TimeSlot
import json
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Überprüft, ob Tanzdaten vorhanden sind, und lädt ggf. das Fixture'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Lade Tanzdaten aus Fixture...'))
        
        # Fixture-Pfad
        fixture_path = os.path.join(settings.BASE_DIR, 'dance', 'fixtures', 'dance_data.json')
        
        # Wenn das Fixture nicht existiert, erstelle es zuerst
        if not os.path.exists(fixture_path):
            self.create_initial_fixture(fixture_path)
            self.stdout.write(self.style.SUCCESS('Initiales Fixture erstellt: {}'.format(fixture_path)))
        
        # Lade das Fixture
        try:
            call_command('loaddata', 'dance_data.json', app_label='dance')
            self.stdout.write(self.style.SUCCESS('Tanzdaten erfolgreich geladen!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Fehler beim Laden des Fixtures: {}'.format(str(e))))

    def data_exists(self):
        """Prüft, ob bereits Daten in der Datenbank vorhanden sind."""
        return Teacher.objects.exists() and Course.objects.exists() and TimeSlot.objects.exists()

    def create_initial_fixture(self, fixture_path):
        """Erstellt ein initiales Fixture mit Beispieldaten."""
        
        # Erstelle Beispieldaten-Array
        fixture_data = []
        
        # Lehrer erstellen
        teachers = [
            {"model": "dance.teacher", "pk": 1, "fields": {"name": "Petra Holzweber", "email": "petra.holzweber@example.com"}},
            {"model": "dance.teacher", "pk": 2, "fields": {"name": "Maria Grüssinger", "email": "maria.gruessinger@example.com"}},
            {"model": "dance.teacher", "pk": 3, "fields": {"name": "Anna Mayer", "email": "anna.mayer@example.com"}},
            {"model": "dance.teacher", "pk": 4, "fields": {"name": "Sophie Bauer", "email": "sophie.bauer@example.com"}},
        ]
        
        # Kurse erstellen
        courses = [
            {"model": "dance.course", "pk": 1, "fields": {"name": "Kindertanz", "teacher": 1, "age_group": "4-6 Jahre", "description": "Spielerisches Kennenlernen von Rhythmus und Bewegung"}},
            {"model": "dance.course", "pk": 2, "fields": {"name": "Ballett für Anfänger", "teacher": 2, "age_group": "6-8 Jahre", "description": "Grundlagen des klassischen Balletts"}},
            {"model": "dance.course", "pk": 3, "fields": {"name": "Jazz Dance", "teacher": 3, "age_group": "10-14 Jahre", "description": "Moderner Tanz mit Jazz-Elementen"}},
            {"model": "dance.course", "pk": 4, "fields": {"name": "Hip Hop", "teacher": 4, "age_group": "12-16 Jahre", "description": "Urbane Tanzstile und Choreografien"}},
            {"model": "dance.course", "pk": 5, "fields": {"name": "Contemporary Dance", "teacher": 3, "age_group": "14-18 Jahre", "description": "Zeitgenössischer Tanz mit Fokus auf Ausdruck"}},
        ]
        
        # Zeitfenster erstellen
        timeslots = [
            {"model": "dance.timeslot", "pk": 1, "fields": {"course": 1, "day": "Montag", "start_time": "15:00:00", "end_time": "16:00:00", "studio": "Tanzraum, Campus"}},
            {"model": "dance.timeslot", "pk": 2, "fields": {"course": 2, "day": "Dienstag", "start_time": "16:30:00", "end_time": "18:00:00", "studio": "Tanzraum, Campus"}},
            {"model": "dance.timeslot", "pk": 3, "fields": {"course": 3, "day": "Mittwoch", "start_time": "17:00:00", "end_time": "18:30:00", "studio": "Tanzraum, Campus"}},
            {"model": "dance.timeslot", "pk": 4, "fields": {"course": 4, "day": "Donnerstag", "start_time": "18:00:00", "end_time": "19:30:00", "studio": "Tanzraum, Campus"}},
            {"model": "dance.timeslot", "pk": 5, "fields": {"course": 5, "day": "Freitag", "start_time": "16:00:00", "end_time": "17:30:00", "studio": "Tanzraum, Campus"}},
            {"model": "dance.timeslot", "pk": 6, "fields": {"course": 1, "day": "Mittwoch", "start_time": "14:00:00", "end_time": "15:00:00", "studio": "Kulturheim Spratzern"}},
            {"model": "dance.timeslot", "pk": 7, "fields": {"course": 2, "day": "Donnerstag", "start_time": "15:30:00", "end_time": "17:00:00", "studio": "Kulturheim Spratzern"}},
        ]
        
        # Daten zusammenführen
        fixture_data.extend(teachers)
        fixture_data.extend(courses)
        fixture_data.extend(timeslots)
        
        # Fixture-Datei schreiben
        os.makedirs(os.path.dirname(fixture_path), exist_ok=True)
        with open(fixture_path, 'w', encoding='utf-8') as f:
            json.dump(fixture_data, f, ensure_ascii=False, indent=4)
