#!/usr/bin/env python
"""
Script zum Reparieren und Aktualisieren der dance_fixture.json-Datei.
Dieses Skript liest die Datei ein, validiert die Struktur und schreibt sie zurück.
"""

import json
import os
import sys
from datetime import time

def fix_fixture_file(fixture_path):
    """
    Liest die Fixture-Datei ein, prüft und repariert die Struktur und schreibt sie zurück.
    
    Args:
        fixture_path: Pfad zur Fixture-Datei
    
    Returns:
        bool: True, wenn die Datei erfolgreich repariert wurde, sonst False
    """
    try:
        # Lese die Fixture-Datei
        with open(fixture_path, 'r', encoding='utf-8') as f:
            fixture_data = json.load(f)
        
        print(f"Gelesen: {len(fixture_data)} Einträge aus {fixture_path}")
        
        # Validiere und repariere die Struktur
        valid_models = ["dance.teacher", "dance.course", "dance.timeslot"]
        required_fields = {
            "dance.teacher": ["name", "email"],
            "dance.course": ["name", "teacher", "age_group", "description"],
            "dance.timeslot": ["course", "day", "start_time", "end_time"]
        }
        
        # Gültige Wochentage
        valid_days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        
        # Zähle die Modelltypen
        model_counts = {model: 0 for model in valid_models}
        
        # Repariere die Einträge
        repaired_entries = []
        for entry in fixture_data:
            model = entry.get("model")
            pk = entry.get("pk")
            fields = entry.get("fields", {})
            
            # Überspringe ungültige Modelle
            if model not in valid_models:
                print(f"Überspringe ungültiges Modell: {model}")
                continue
            
            model_counts[model] += 1
            
            # Stelle sicher, dass alle erforderlichen Felder vorhanden sind
            for field in required_fields[model]:
                if field not in fields:
                    print(f"Fehlendes Feld {field} in {model} (pk={pk})")
                    
                    # Füge Standardwerte hinzu
                    if field == "description":
                        fields[field] = ""
                    elif field == "studio":
                        fields[field] = None
            
            # Repariere Wochentage für TimeSlot
            if model == "dance.timeslot" and "day" in fields:
                day = fields["day"]
                if day not in valid_days:
                    print(f"Ungültiger Wochentag {day} in TimeSlot (pk={pk})")
                    # Setze einen Standardwert
                    fields["day"] = "Montag"
            
            # TimeSlot-spezifische Validierung
            if model == "dance.timeslot":
                # Stelle sicher, dass start_time und end_time im richtigen Format sind
                for time_field in ["start_time", "end_time"]:
                    if time_field in fields:
                        time_str = fields[time_field]
                        if not isinstance(time_str, str) or not time_str.count(":") >= 1:
                            print(f"Ungültiges Zeitformat {time_str} in TimeSlot (pk={pk})")
                            # Setze einen Standardwert
                            fields[time_field] = "12:00:00" if time_field == "start_time" else "13:00:00"
                        elif len(time_str.split(":")) == 2:
                            # Füge Sekunden hinzu, wenn sie fehlen
                            fields[time_field] = time_str + ":00"
            
            # Füge den reparierten Eintrag hinzu
            repaired_entries.append({
                "model": model,
                "pk": pk,
                "fields": fields
            })
        
        # Schreibe die reparierte Datei zurück
        with open(fixture_path, 'w', encoding='utf-8') as f:
            json.dump(repaired_entries, f, ensure_ascii=False, indent=4)
        
        print(f"Reparierte Fixture-Datei gespeichert: {fixture_path}")
        print(f"Modell-Zählung: {model_counts}")
        
        return True
    
    except Exception as e:
        print(f"Fehler beim Reparieren der Fixture-Datei: {str(e)}")
        return False

if __name__ == "__main__":
    # Standardpfad oder übergebener Pfad
    fixture_path = sys.argv[1] if len(sys.argv) > 1 else "dance_fixture.json"
    if not os.path.exists(fixture_path):
        print(f"Fixture-Datei nicht gefunden: {fixture_path}")
        sys.exit(1)
    
    success = fix_fixture_file(fixture_path)
    sys.exit(0 if success else 1)
