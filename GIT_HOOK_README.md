[SUCCESS] Pre-push hook completed successfully
```

## Fehlerbehebung

### Häufige Probleme

#### 1. Conda Environment nicht gefunden
```bash
[ERROR] mks conda environment not found at /Users/lukasschonsgibl/opt/anaconda3/envs/mks/bin/python
```
**Lösung**: Überprüfe den Pfad zum Python-Interpreter im Hook

#### 2. CSS Update Scripts nicht gefunden
```bash
[ERROR] No CSS update scripts found
```
**Lösung**: Stelle sicher, dass `update_css_version.py` oder `update_css_simple.sh` im Projektroot vorhanden sind

#### 3. Django Tests schlagen fehl
```bash
[ERROR] Django tests failed! Push aborted
```
**Lösung**: Behebe die Tests vor dem Push. Hook verhindert Push bei Test-Fehlern

#### 4. Permission Denied
```bash
permission denied: .git/hooks/pre-push
```
**Lösung**: 
```bash
chmod +x .git/hooks/pre-push
```

### Debug-Modus

Für detaillierte Debug-Informationen, bearbeite den Hook und füge hinzu:
```bash
set -x  # Debug-Modus aktivieren
```

### Hook temporär deaktivieren

```bash
# Hook umbenennen
mv .git/hooks/pre-push .git/hooks/pre-push.disabled

# Push ohne Hook
git push

# Hook wieder aktivieren
mv .git/hooks/pre-push.disabled .git/hooks/pre-push
```

## Erweiterte Konfiguration

### Custom Version Detection

Um eine eigene Versionierungslogik zu verwenden, bearbeite die `get_project_version()` Funktion:

```bash
get_project_version() {
    # Beispiel: Version aus package.json lesen
    VERSION=$(python -c "
import json
try:
    with open('package.json') as f:
        data = json.load(f)
        print(data.get('version', '1.0.0'))
except:
    print('1.0.0')
")
    echo "$VERSION"
}
```

### CSS Detection anpassen

Um zusätzliche Dateitypen zu überwachen:

```bash
# Erweiterte Pattern
CSS_MODIFIED=$(git diff --cached --name-only --diff-filter=AM | grep -E '\.(css|scss|sass|less)$' || true)
```

### Selective CSS Updates

Um nur bestimmte CSS-Dateien zu versionieren:

```bash
# Nur main CSS-Dateien
CSS_MODIFIED=$(git diff --cached --name-only --diff-filter=AM | grep -E 'main.*\.css$|app.*\.css$' || true)
```

## Integration mit CI/CD

### GitHub Actions Beispiel

```yaml
name: Pre-Push Validation
on: [push]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Run CSS Version Check
        run: |
          python update_css_version.py --version ${{ github.ref_name }} --dry-run
```

### Pre-Commit Integration

Zusätzlich zum Pre-Push Hook kann auch ein Pre-Commit Hook erstellt werden:

```bash
# .git/hooks/pre-commit
#!/bin/bash
# Validate CSS syntax before commit
find . -name "*.css" -exec csslint {} \;
```

## Monitoring und Logging

### Log-Ausgabe anpassen

Die Log-Funktionen können erweitert werden:

```bash
log_info() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')] [INFO]${NC} $1"
}
```

### Log-Datei erstellen

```bash
# Am Anfang des Hooks hinzufügen
LOG_FILE="/tmp/mks_pre_push_$(date +%s).log"
exec > >(tee -a "$LOG_FILE")
exec 2>&1
```

## Backup und Recovery

### Automatische Backups

Der Hook erstellt automatisch Backups in:
- `css_backup_YYYYMMDD_HHMMSS/` für CSS-Dateien
- `dance/fixtures/dance_data_backup.json` für Test-Fixtures

### Backup wiederherstellen

```bash
# CSS-Dateien wiederherstellen
cp -r css_backup_20231215_143022/* .

# Fixture wiederherstellen
cp dance/fixtures/dance_data_backup.json dance/fixtures/dance_data.json
```

## Performance Optimierung

### Skip-Mechanismus

Um unnötige CSS-Updates zu vermeiden:

```bash
# Check if version file is newer than CSS files
if [ "$NEWEST_CSS" -le "$LAST_UPDATE" ]; then
    log_success "CSS files are up to date"
    return 0
fi
```

### Parallele Ausführung

Für große Projekte können Tests und CSS-Updates parallelisiert werden:

```bash
# Tests im Hintergrund starten
$PYTHON_CMD manage.py test --keepdb &
TEST_PID=$!

# CSS Update durchführen
update_css_versions

# Auf Tests warten
wait $TEST_PID
TESTS_EXIT_CODE=$?
```

## Wartung

### Hook Updates

Um den Hook zu aktualisieren:

1. Backup erstellen: `cp .git/hooks/pre-push .git/hooks/pre-push.backup`
2. Neue Version installieren
3. Testen: `./test_hook.sh`

### Regelmäßige Überprüfung

Monatliche Aufgaben:
- Hook-Performance überprüfen
- Backup-Ordner bereinigen
- Version-JSON-Dateien archivieren

```bash
# Cleanup-Script
find . -name "css_backup_*" -mtime +30 -exec rm -rf {} \;
find . -name "css_version_*.json" -mtime +90 -exec rm {} \;
```

## Support

Bei Problemen:
1. Prüfe die Log-Ausgabe des Hooks
2. Teste mit `./test_hook.sh`
3. Überprüfe die Dateiberechtigungen
4. Validiere die Python-Environment-Pfade

---

**Erstellt**: $(date)
**Version**: 1.0.0
**Autor**: MKS Development Team
