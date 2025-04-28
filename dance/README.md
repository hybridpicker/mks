# Tanz & Bewegung App

Diese Django-App verwaltet den Tanzunterricht der Musikschule St. Pölten mit Kursen, Lehrkräften und Stundenplänen.

## Features

- Öffentlicher Stundenplan mit Filterung nach Tanzstil und Altersgruppe
- Detailansicht für Kurse mit Beschreibungen
- Administrationsbereich für berechtigte Benutzer zum Verwalten von:
  - Lehrkräften
  - Kursen
  - Zeitfenstern

## Installation und Einrichtung

### Automatische Einrichtung

Für eine einfache Einrichtung der App verwenden Sie das bereitgestellte Setup-Skript:

```bash
./setup_dance_app.sh
```

Das Skript führt folgende Schritte aus:
1. Prüft und repariert die dance_fixture.json-Datei
2. Führt Migrationen aus
3. Lädt die Tanzdaten in die Datenbank
4. Sammelt statische Dateien

### Manuelle Einrichtung

Alternativ können Sie die App auch manuell einrichten:

1. Migrationen ausführen:
   ```bash
   python manage.py migrate
   ```

2. Fixture-Datei prüfen und reparieren:
   ```bash
   python manage.py fix_dance_fixture
   ```

3. Tanzdaten laden:
   ```bash
   python manage.py load_dance_fixture
   ```

4. Statische Dateien sammeln:
   ```bash
   python manage.py collectstatic
   ```

## Datenmodell

Die App verwendet folgende Modelle:

- **Teacher (Lehrkraft)**: Name und E-Mail-Kontakt
- **Course (Kurs)**: Name, Beschreibung, Altersgruppe und zugeordnete Lehrkraft
- **TimeSlot (Zeitfenster)**: Tag, Start- und Endzeit, Studio und zugeordneter Kurs

## Management-Kommandos

Die App stellt folgende Management-Kommandos bereit:

- `setup_dance_data`: Lädt die Standarddaten aus dem Fixture
- `load_dance_fixture`: Lädt Daten aus der dance_fixture.json
- `update_dance_fixture`: Exportiert aktuelle Daten in die Fixture-Datei
- `fix_dance_fixture`: Repariert und validiert die Fixture-Datei
- `import_dance_csv`: Importiert Kursdaten aus einer CSV-Datei

## URLs

- `/tanz-und-bewegung/`: Öffentlicher Stundenplan
- `/tanz-und-bewegung/wartung/`: Administrationsbereich (Login erforderlich)
- `/tanz-und-bewegung/kurs/<id>/`: API-Endpunkt für Kursdetails

## Wartung und Updates

### Aktualisieren der Fixture-Datei

Wenn Sie Änderungen an den Daten vorgenommen haben und diese in die Fixture-Datei übernehmen möchten:

```bash
python manage.py update_dance_fixture
```

### Neue Daten aus CSV importieren

```bash
python manage.py import_dance_csv path/to/your/csv/file.csv
```

## Entwicklung

### CSS-Styling

Die Stylesheets befinden sich im Verzeichnis `dance/static/dance/css/`.

### Templates

Die Templates befinden sich im Verzeichnis `templates/dance/`:
- `schedule.html`: Öffentlicher Stundenplan
- `maintenance.html`: Administrationsbereich
- `slider.html`: Bildslider für die Kopfzeile

## Fehlerbehandlung

Falls Probleme mit der Fixture-Datei auftreten:

```bash
python manage.py fix_dance_fixture
```

Bei Problemen mit der Datenbank:

```bash
python manage.py migrate --fake dance zero
python manage.py migrate dance
```
