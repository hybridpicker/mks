# Lazy Loading Test Checkliste

## 🧪 Manuelle Tests (im Browser)

### 1. Gallery Seite öffnen
- [ ] Öffne `/gallery/` im Browser
- [ ] Öffne die Entwicklertools (F12)
- [ ] Gehe zum "Network" Tab

### 2. Lazy Loading prüfen
- [ ] Scrolle langsam nach unten
- [ ] Beobachte im Network Tab: Werden Bilder nachgeladen?
- [ ] Prüfe: Erscheinen Bilder mit sanftem Fade-in?

### 3. HTML-Struktur prüfen (Elements Tab)
- [ ] Suche nach `<img class="lazy">`
- [ ] Prüfe ob `data-src` Attribute vorhanden sind
- [ ] Prüfe ob `<noscript>` Tags vorhanden sind

### 4. Console prüfen
- [ ] Suche nach "Lazy Loading für Galerie initialisiert"
- [ ] Prüfe auf Fehlermeldungen

## 🤖 Automatische Tests

### Django Tests ausführen:
```bash
# Alle Gallery Tests
python manage.py test gallery -v 2

# Nur Lazy Loading Tests
python manage.py test gallery.tests.test_lazy_loading -v 2

# Quick Test Command
python manage.py test_lazy_loading
```

### Erwartete Testergebnisse:
- ✅ test_lazy_image_creation
- ✅ test_thumbnail_creation
- ✅ test_process_uploaded_image
- ✅ test_gallery_view_with_lazy_loading
- ✅ test_automatic_lazy_generation_in_view

## 📊 Performance Test

### Vorher (ohne Lazy Loading):
1. Öffne Network Tab
2. Lade Gallery Seite
3. Notiere: Gesamte Ladezeit, Anzahl Requests, Datenmenge

### Nachher (mit Lazy Loading):
1. Gleicher Test
2. Vergleiche: Sollte schneller sein, weniger initiale Requests

## 🔍 Troubleshooting

### Bilder werden nicht geladen:
- Prüfe Browser Console auf Fehler
- Prüfe ob `lazy-loading.js` geladen wird
- Prüfe ob Intersection Observer unterstützt wird

### Lazy Images werden nicht generiert:
- Prüfe Logs: `tail -f logs/django.log`
- Prüfe Berechtigungen: `media/gallery/images/lazy/`
- Führe aus: `python manage.py generate_lazy_images`

### Performance ist nicht besser:
- Prüfe ob wirklich Lazy Images verwendet werden
- Prüfe Größe der Lazy Images (sollten ~800x600 sein)
- Cache leeren und neu testen