from django.core.management.base import BaseCommand
import json
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Aktualisiert die Kategorien in der dance_fixture.json-Datei'

    def handle(self, *args, **options):
        # Pfad zur Fixture-Datei
        fixture_path = os.path.join(settings.BASE_DIR, 'dance_fixture.json')
        
        if not os.path.exists(fixture_path):
            self.stdout.write(self.style.ERROR(f'Fixture-Datei nicht gefunden: {fixture_path}'))
            return
        
        try:
            # Lade die Fixture-Datei
            with open(fixture_path, 'r', encoding='utf-8') as f:
                fixture_data = json.load(f)
            
            self.stdout.write(f'Geladen: {len(fixture_data)} Einträge aus {fixture_path}')
            
            # Zähle die Einträge nach Modell
            course_count = 0
            
            # Durchsuche alle Kurse
            for entry in fixture_data:
                # Wir suchen nur nach Kursen, da wir die Beschreibungen aktualisieren müssen
                if entry['model'] == 'dance.course':
                    course_count += 1
                    fields = entry.get('fields', {})
                    
                    # Prüfe, ob der Kurs "Zeitgenössischer Tanz - Fokus Improvisation & Tanztheater" ist
                    if 'name' in fields and 'Zeitgenössischer Tanz' in fields['name'] and 'Improvisation' in fields['name']:
                        self.stdout.write(f"Kurs gefunden: {fields['name']}")
                        # Hier könnten wir den Kurs bei Bedarf direkt umbenennen oder die Beschreibung ändern
                        # Da die Kategorien dynamisch berechnet werden, ist das nicht zwingend erforderlich
            
            self.stdout.write(f'Gefunden: {course_count} Kurse in der Fixture')
            
            # Da keine direkten Änderungen an der Fixture notwendig sind (die Kategorien werden durch die
            # aktualisierte get_course_category()-Funktion bestimmt), speichern wir die Datei unverändert zurück
            
            # Alternativ könnten wir hier die Datei neu exportieren, nachdem wir die Datenbank aktualisiert haben
            self.stdout.write(self.style.SUCCESS('Fixture bleibt unverändert, da die Kategorien durch Code-Anpassung aktualisiert wurden.'))
            self.stdout.write(self.style.SUCCESS('- "Klassisches Ballett" -> "Klassischer Tanz"'))
            self.stdout.write(self.style.SUCCESS('- "Zeitgenössischer Tanz..." mit "Improvisation" oder "Tanztheater" -> "Moderner Tanz"'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Fehler beim Aktualisieren der Fixture: {str(e)}'))
