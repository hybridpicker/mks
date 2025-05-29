# Gallery Upload Debugging Guide

## Problem
Der Upload-Fortschrittsbalken zeigt 100%, aber die Bilder werden nicht gespeichert.

## Mögliche Ursachen

1. **Fehlende Kategorie-ID**: Prüfen Sie, ob eine Kategorie ausgewählt ist
2. **Dateien werden nicht übertragen**: Die Files könnten im FormData fehlen
3. **Server-Fehler**: Fehler bei der Bildverarbeitung

## Debug-Schritte

### 1. Browser-Konsole öffnen
Öffnen Sie die Browser-Entwicklertools (F12) und gehen Sie zur Konsole.

### 2. Upload versuchen
Laden Sie Bilder hoch und beobachten Sie die Konsole auf:
- "Files to upload: X" - Anzahl der Dateien
- "Adding file: filename.jpg" - Jede hinzugefügte Datei
- "Response status: XXX" - HTTP Status Code
- "Response data: {...}" - Server-Antwort

### 3. Server-Logs prüfen
```bash
cd /Users/lukasschonsgibl/Coding/Django/mks
tail -f logs/django.log
```

### 4. Manuelle Tests

#### Test 1: Einzelbild-Upload
1. Wechseln Sie zum "Einzelnes Bild" Tab
2. Laden Sie ein einzelnes Bild hoch
3. Funktioniert das?

#### Test 2: Kategorie prüfen
1. Stellen Sie sicher, dass eine Kategorie ausgewählt ist
2. Die URL sollte `?category=X` enthalten

#### Test 3: Kleine Dateien
1. Versuchen Sie es mit sehr kleinen Bildern (< 1MB)
2. Funktioniert es mit kleinen Dateien?

## Temporäre Lösung

Falls der Multi-Upload nicht funktioniert:
1. Verwenden Sie den Einzelbild-Upload
2. Oder laden Sie die Bilder über das Django Admin Interface hoch

## Erweiterte Fehlersuche

### Server neu starten
```bash
cd /Users/lukasschonsgibl/Coding/Django/mks
python3 manage.py runserver
```

### Berechtigungen prüfen
```bash
ls -la media/gallery/images/
```

### Test-Upload via Command Line
```bash
cd /Users/lukasschonsgibl/Coding/Django/mks
python3 manage.py shell

from gallery.models import Photo, PhotoCategory
from django.core.files.base import ContentFile

cat = PhotoCategory.objects.first()
photo = Photo.objects.create(
    title="Test",
    category=cat,
    image=ContentFile(b"test", name="test.jpg")
)
print(f"Created photo: {photo.id}")
```

## Kontaktieren Sie den Entwickler

Wenn das Problem weiterhin besteht, senden Sie bitte:
1. Screenshot der Browser-Konsole
2. Inhalt von logs/django.log
3. Genaue Schritte zur Reproduktion
