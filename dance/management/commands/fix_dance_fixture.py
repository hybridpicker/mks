from django.core.management.base import BaseCommand
import os
import json
import sys
from django.conf import settings

class Command(BaseCommand):
    help = 'Repariert und validiert die dance_fixture.json-Datei'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            default='dance/fixtures/dance_data.json',
            help='Pfad zur Fixture-Datei (Standard: dance/fixtures/dance_data.json)',
        )

    def handle(self, *args, **options):
        fixture_path = options['path']
        
        # Wenn der Pfad relativ ist, kombiniere ihn mit BASE_DIR
        if not os.path.isabs(fixture_path):
            fixture_path = os.path.join(settings.BASE_DIR, fixture_path)
        
        self.stdout.write(self.style.WARNING(f'Überprüfe und repariere Fixture-Datei: {fixture_path}'))
        
        if not os.path.exists(fixture_path):
            self.stdout.write(self.style.ERROR(f'Fixture-Datei nicht gefunden: {fixture_path}'))
            return
        
        try:
            # Fixture-Datei einlesen
            with open(fixture_path, 'r', encoding='utf-8') as f:
                fixture_data = json.load(f)
            
            # Zähle die Einträge nach Modell
            model_counts = {}
            for entry in fixture_data:
                model = entry.get('model', 'unknown')
                model_counts[model] = model_counts.get(model, 0) + 1
            
            self.stdout.write(f'Gefundene Einträge: {len(fixture_data)}')
            for model, count in model_counts.items():
                self.stdout.write(f'  - {model}: {count} Einträge')
            
            # Validiere und repariere die Struktur
            valid_models = ["dance.teacher", "dance.course", "dance.timeslot"]
            required_fields = {
                "dance.teacher": ["name", "email"],
                "dance.course": ["name", "teacher", "age_group", "description"],
                "dance.timeslot": ["course", "day", "start_time", "end_time"]
            }
            
            # Gültige Wochentage
            valid_days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
            
            # Repariere die Einträge
            repaired_entries = []
            repairs_made = 0
            
            for entry in fixture_data:
                model = entry.get("model")
                pk = entry.get("pk")
                fields = entry.get("fields", {})
                
                # Überspringe ungültige Modelle
                if model not in valid_models:
                    self.stdout.write(self.style.WARNING(f'Überspringe ungültiges Modell: {model}'))
                    continue
                
                # Stelle sicher, dass alle erforderlichen Felder vorhanden sind
                entry_repaired = False
                for field in required_fields[model]:
                    if field not in fields:
                        self.stdout.write(self.style.WARNING(f'Fehlendes Feld {field} in {model} (pk={pk})'))
                        
                        # Füge Standardwerte hinzu
                        if field == "description":
                            fields[field] = ""
                        elif field == "studio":
                            fields[field] = None
                        
                        entry_repaired = True
                
                # Repariere Wochentage für TimeSlot
                if model == "dance.timeslot" and "day" in fields:
                    day = fields["day"]
                    if day not in valid_days:
                        self.stdout.write(self.style.WARNING(f'Ungültiger Wochentag {day} in TimeSlot (pk={pk})'))
                        # Setze einen Standardwert
                        fields["day"] = "Montag"
                        entry_repaired = True
                
                # TimeSlot-spezifische Validierung
                if model == "dance.timeslot":
                    # Stelle sicher, dass start_time und end_time im richtigen Format sind
                    for time_field in ["start_time", "end_time"]:
                        if time_field in fields:
                            time_str = fields[time_field]
                            if not isinstance(time_str, str) or not time_str.count(":") >= 1:
                                self.stdout.write(self.style.WARNING(f'Ungültiges Zeitformat {time_str} in TimeSlot (pk={pk})'))
                                # Setze einen Standardwert
                                fields[time_field] = "12:00:00" if time_field == "start_time" else "13:00:00"
                                entry_repaired = True
                            elif len(time_str.split(":")) == 2:
                                # Füge Sekunden hinzu, wenn sie fehlen
                                fields[time_field] = time_str + ":00"
                                entry_repaired = True
                
                if entry_repaired:
                    repairs_made += 1
                
                # Füge den reparierten Eintrag hinzu
                repaired_entries.append({
                    "model": model,
                    "pk": pk,
                    "fields": fields
                })
            
            # Schreibe die reparierte Datei zurück
            with open(fixture_path, 'w', encoding='utf-8') as f:
                json.dump(repaired_entries, f, ensure_ascii=False, indent=4)
            
            if repairs_made > 0:
                self.stdout.write(self.style.SUCCESS(f'Fixture-Datei repariert: {repairs_made} Änderungen vorgenommen'))
            else:
                self.stdout.write(self.style.SUCCESS('Fixture-Datei bereits korrekt, keine Reparaturen notwendig'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Fehler beim Reparieren der Fixture-Datei: {str(e)}'))
