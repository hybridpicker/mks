# CSS Version Management Scripts

Diese Skripte helfen dabei, alle CSS-Dateien im Django-Projekt auf eine bestimmte Version zu aktualisieren.

## Verfügbare Skripte

### 1. Python-Skript (Empfohlen)
`update_css_version.py` - Vollständiges Python-Skript mit Django-Integration

**Features:**
- Automatische Django-Version-Erkennung
- Backup-Erstellung
- Template-Referenzen-Update
- Dry-run Modus
- Ausführliche Logging
- JSON-Versionsinformationen

**Usage:**
```bash
# Dry-run (zeigt was gemacht würde, ohne Änderungen)
python3 update_css_version.py --version 3.0.0 --dry-run

# Mit Backup
python3 update_css_version.py --version 3.0.0 --backup

# Normale Ausführung
python3 update_css_version.py --version 3.0.0
```

**Parameter:**
- `--version`: Ziel-Version (z.B. 3.0.0)
- `--dry-run`: Simulation ohne Änderungen
- `--backup`: Backup vor Änderungen erstellen
- `--force`: Update auch bei Django-Version-Mismatch
- `--project-root`: Django-Projekt-Pfad (Standard: aktuelles Verzeichnis)

### 2. Bash-Skript (Einfach)
`update_css_simple.sh` - Einfaches Bash-Skript für schnelle Updates

**Usage:**
```bash
./update_css_simple.sh 3.0.0
```

## Funktionsweise

### Was passiert beim Update:

1. **CSS-Dateien umbenennen:**
   - `mks.css` → `mks.3.0.0.css`
   - `admin.css` → `admin.3.0.0.css`
   - Bestehende Versionen werden ersetzt

2. **Template-Referenzen aktualisieren:**
   - HTML-Templates durchsuchen
   - CSS-Referenzen ersetzen
   - Django-Template-Syntax berücksichtigen

3. **Backup erstellen:**
   - Originaldateien sichern
   - Struktur beibehalten

## Beispiel-Workflow

```bash
# 1. Aktuellen Stand prüfen
python3 update_css_version.py --version 3.0.0 --dry-run

# 2. Mit Backup ausführen
python3 update_css_version.py --version 3.0.0 --backup

# 3. Änderungen überprüfen
git status
git diff

# 4. Bei Problemen: Backup wiederherstellen
# Backup-Ordner wird angezeigt, z.B.:
# cp -r css_backup_20250524_153022/* .
```

## Unterstützte Dateitypen

### CSS-Dateien:
- `.css` in `/static/`
- `.css` in App-spezifischen `/static/` Ordnern
- `.css` in `/staticfiles/` und `/static_cdn/`

### Template-Dateien:
- `.html`
- `.htm`
- `.django`
- `.jinja2`

### Erkannte Referenz-Patterns:
- `<link href="style.css">`
- `{% static 'css/style.css' %}`
- `{% load static %}`
- Direkte CSS-Pfade

## Versionierung

### Django-Version-Alignment:
Das Skript prüft die Django-Version und warnt bei Mismatch:
- Django 3.0.0 → CSS-Version 3.0.0 ✅
- Django 3.0.0 → CSS-Version 2.5.0 ⚠️ (Warnung)

### Versionsformat:
- Muss `X.Y.Z` Format folgen (z.B. 3.0.0, 2.1.5)
- Semantic Versioning wird empfohlen

## Sicherheit

### Backup-System:
- Automatische Backups mit Zeitstempel
- Vollständige Ordnerstruktur erhalten
- Backup-Pfad wird angezeigt

### Dry-Run:
- Zeigt alle geplanten Änderungen
- Keine Dateien werden verändert
- Sicher zum Testen

## Troubleshooting

### Häufige Probleme:

1. **"No CSS files found"**
   - Prüfen Sie den Projektpfad
   - Stellen Sie sicher, dass CSS-Dateien in `/static/` liegen

2. **Django-Setup-Fehler**
   - `DJANGO_SETTINGS_MODULE` prüfen
   - Virtual Environment aktiviert?
   - Dependencies installiert?

3. **Permission Denied**
   - Skript ausführbar machen: `chmod +x script.sh`
   - Schreibrechte im Projektordner prüfen

4. **Template-Updates fehlgeschlagen**
   - Encoding-Probleme (UTF-8 verwenden)
   - Backup wiederherstellen und manuell prüfen

### Debug-Tipps:
```bash
# Gefundene CSS-Dateien anzeigen
find . -name "*.css" -type f

# Template-Dateien anzeigen
find . -name "*.html" -type f

# Django-Version prüfen
python3 -c "import django; print(django.VERSION)"
```

## Integration in CI/CD

### GitHub Actions Beispiel:
```yaml
- name: Update CSS Version
  run: |
    python3 update_css_version.py --version ${{ github.event.release.tag_name }} --backup
    git add .
    git commit -m "Update CSS to version ${{ github.event.release.tag_name }}"
```

### Pre-commit Hook:
```bash
#!/bin/sh
# In .git/hooks/pre-commit
python3 update_css_version.py --version $(cat VERSION) --dry-run
```

## Entwicklung

### Skript erweitern:
- Neue Dateitypen in `find_template_files()` hinzufügen
- Zusätzliche Referenz-Patterns in `update_template_references()` einfügen
- Logging-Level anpassen

### Testing:
```bash
# Test mit kleinem Projekt
mkdir test_project
cd test_project
echo "body { color: red; }" > style.css
echo '<link href="style.css">' > index.html
python3 ../update_css_version.py --version 1.0.0 --dry-run
```
