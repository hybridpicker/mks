# Umgestaltung der Fachgruppen-Seiten

## Übersicht
Die Musikschul-Fachgruppen wurden von einer einzigen Übersichtsseite auf individuelle Seiten pro Fachgruppe umgestellt.

## Durchgeführte Änderungen

### 1. Template-Struktur
- Neues Basis-Template: `templates/teaching/fachgruppen/base_fachgruppe.html`
- Spezielles Template für EME: `templates/teaching/fachgruppen/eme.html`

### 2. Views
- Neue generische Funktion `get_fachgruppe_context()` erstellt
- Alle Fachgruppen-Views verwenden jetzt das Basis-Template
- Views holen Daten dynamisch aus der Datenbank

### 3. URLs
- Neue URL für Tanz und Bewegung: `/bildungsangebot-musikschule/tanz-und-bewegung`
- Bestehende URLs bleiben unverändert

### 4. Datenbank
- Management Command `create_fachgruppen` erstellt
- Erstellt alle benötigten SubjectCategory-Einträge

## Verwendung

### Kategorien anlegen
```bash
python manage.py create_fachgruppen
```

### Neue Fachgruppe hinzufügen
1. SubjectCategory in der Datenbank anlegen
2. Neue View-Funktion erstellen
3. URL hinzufügen
4. Link auf Übersichtsseite ergänzen

### Templates anpassen
- Basis-Template für allgemeine Anpassungen: `base_fachgruppe.html`
- Spezielle Templates für einzelne Fachgruppen erstellen (wie `eme.html`)

## Features
- Breadcrumb-Navigation
- Dynamische Lehrerübersicht mit Bildern
- Auflistung aller Instrumente/Fächer
- Responsive Design
- Lazy Loading für Bilder

## Offene Punkte
- Testen aller Seiten
- Prüfen ob alle Kategorien korrekt angelegt sind
- ggf. weitere spezielle Templates erstellen
