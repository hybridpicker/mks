#!/bin/bash

# Skript zum Installieren der Git-Hooks für das MKS-Projekt

# Pfad zum Git-Hooks-Verzeichnis
HOOKS_DIR=".git/hooks"

# Kopieren des pre-push-Hooks
cat > $HOOKS_DIR/pre-push << 'EOF'
#!/bin/bash

echo "Running pre-push hooks..."

# Aktiviere die virtuelle Umgebung (anpassen an deine lokale Umgebung)
# Für Conda:
source ~/opt/anaconda3/envs/mks/bin/activate
# Für venv:
# source venv/bin/activate

# Generiere aktuelles Fixture für die Dance-App
echo "Generating updated fixture for Dance app..."
python manage.py dumpdata dance --indent 2 --output dance/fixtures/dance_data.json
FIXTURE_RESULT=$?

if [ $FIXTURE_RESULT -ne 0 ]; then
    echo "ERROR: Failed to generate Dance app fixture. Push aborted."
    exit 1
fi

echo "Dance app fixture successfully updated."
git add dance/fixtures/dance_data.json

# Führe die Tests aus
echo "Running tests..."
python manage.py test
TEST_RESULT=$?

# Überprüfe, ob die Tests erfolgreich waren
if [ $TEST_RESULT -ne 0 ]; then
    echo "Tests failed. Push aborted."
    exit 1
fi

echo "All pre-push checks passed. Proceeding with push..."
exit 0
EOF

# Hook ausführbar machen
chmod +x $HOOKS_DIR/pre-push

echo "Git hooks erfolgreich installiert!"
echo "Der pre-push Hook wurde eingerichtet. Er wird automatisch ein aktuelles Dance-App Fixture generieren, bevor ein Push erfolgt."
