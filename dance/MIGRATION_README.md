# Migrations-Anweisungen für die Tanz-App

Diese Datei enthält Anweisungen zum Anwenden der Migrationen, die die `location`-Spalte hinzufügen und die Standorte für die Tanz-App korrekt zuweisen.

## Hintergrund

Es gab einen Fehler beim Zugriff auf die `location`-Spalte in der `dance_timeslot`-Tabelle, da diese in der Produktionsumgebung nicht existiert. Die folgenden Migrations-Dateien wurden erstellt, um dieses Problem zu beheben:

- `0004_timeslot_location_for_production.py`: Fügt die `location`-Spalte zur `dance_timeslot`-Tabelle hinzu
- `0005_assign_locations.py`: Weist Standorte basierend auf den Lehrernamen zu

## Anwendung der Migrationen

Führen Sie einfach den Standard-Migrationsbefehl aus:

```bash
python manage.py migrate
```

Dies sollte alle ausstehenden Migrationen anwenden, einschließlich der neuen Migrationen für die Standort-Funktionalität.

## Standort-Zuweisungsregeln

Die Migration `0005_assign_locations.py` weist die Standorte gemäß folgender Regeln zu:

- **Campus**: Zeisel, Bauer, und alle anderen Lehrer ohne explizite Zuweisung
- **Kulturhaus Wagram**: Usmanova
- **Kulturhaus Spratzern**: Grüssinger, Holzweber

Diese Zuweisungen basieren auf den Namen der Lehrer in der Datenbank. Wenn ein Lehrername einen der oben genannten Namen enthält, wird der entsprechende Standort zugewiesen.

## Fehlerbehebung

Wenn es Probleme bei der Anwendung der Migrationen gibt, versuchen Sie folgende Schritte:

1. Überprüfen Sie den aktuellen Migrations-Status:
   ```bash
   python manage.py showmigrations dance
   ```

2. Wenden Sie die Migrationen einzeln an:
   ```bash
   python manage.py migrate dance 0004_timeslot_location_for_production
   python manage.py migrate dance 0005_assign_locations
   ```

3. Falls die Migrationen nicht angewendet werden können, kann ein Backup der Datenbank und ein anschließendes Zurücksetzen der Migrations-Historie für die Dance-App eine Option sein:
   ```bash
   python manage.py migrate dance zero
   python manage.py migrate dance
   ```
   (Achtung: Dies löscht alle Daten in den Dance-Tabellen und setzt die Migrations-Historie zurück!)