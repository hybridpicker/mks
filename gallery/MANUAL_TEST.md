# 🧪 Manueller Test für Lazy Loading

## Schnelltest im Browser (2 Minuten)

### 1. Server starten
```bash
conda activate mks
cd /Users/lukasschonsgibl/Coding/Django/mks
python manage.py runserver
```

### 2. Browser-Test durchführen

1. **Öffnen Sie:** http://localhost:8000/gallery/

2. **Öffnen Sie die Entwicklertools** (F12 oder Rechtsklick → "Element untersuchen")

3. **Gehen Sie zum "Network" Tab** und aktivieren Sie "Disable cache"

4. **Laden Sie die Seite neu** (F5)

5. **Prüfen Sie:**
   - [ ] Werden `lazy-loading.js` und `lazy-loading.css` geladen?
   - [ ] Scrollen Sie langsam nach unten
   - [ ] Werden neue Bilder im Network Tab nachgeladen?
   - [ ] Erscheinen Bilder mit einem sanften Fade-in?

### 3. HTML-Struktur prüfen (Elements Tab)

Suchen Sie nach einem Bild-Element und prüfen Sie:
```html
<img class="lazy loaded" 
     src="/media/gallery/images/lazy/bild_lazy.jpg"
     data-src="/media/gallery/images/bild.jpg"
     alt="...">
```

## ✅ Erfolgskriterien

- **Lazy Loading funktioniert wenn:**
  - Bilder haben `class="lazy"` und `data-src` Attribute
  - Beim Scrollen werden neue Bilder geladen
  - In der Console steht: "Lazy Loading für Galerie initialisiert"

## 🔧 Wenn etwas nicht funktioniert:

1. **Prüfen Sie die Browser Console auf Fehler**
2. **Prüfen Sie ob die Dateien existieren:**
   ```bash
   ls -la static/gallery/js/lazy-loading.js
   ls -la static/gallery/css/lazy-loading.css
   ```

3. **Sammeln Sie statische Dateien:**
   ```bash
   python manage.py collectstatic --noinput
   ```

## 📊 Performance-Vergleich

**Ohne Lazy Loading:**
- Alle Bilder werden sofort geladen
- Lange initiale Ladezeit
- Hoher Speicherverbrauch

**Mit Lazy Loading:**
- Nur sichtbare Bilder werden geladen
- Schnellere initiale Ladezeit
- Bilder werden beim Scrollen nachgeladen