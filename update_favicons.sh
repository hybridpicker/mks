#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Aktualisiere Favicons und statische Dateien...${NC}"

# Projekt-Verzeichnis
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Aktiviere virtuelle Umgebung (wenn vorhanden)
if [ -d "env" ]; then
    source env/bin/activate
elif command -v conda &> /dev/null && conda env list | grep -q "mks"; then
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate mks
fi

# Statische Dateien sammeln und mit dem ManifestStaticFilesStorage verarbeiten
echo -e "${YELLOW}Sammle statische Dateien...${NC}"
python manage.py collectstatic --noinput

# Cache-Löschen in Produktion (wenn Redis verfügbar ist)
if command -v redis-cli &> /dev/null; then
    echo -e "${YELLOW}Lösche Redis-Cache...${NC}"
    redis-cli flushall
fi

# Cache-Manifest erstellen
echo -e "${YELLOW}Erstelle Cache-Manifest für Favicons...${NC}"
python manage.py shell -c "from django.contrib.staticfiles.storage import staticfiles_storage; staticfiles_storage.hashed_name('favicon/favicon.ico')"

echo -e "${GREEN}Favicons und statische Dateien wurden erfolgreich aktualisiert!${NC}"
echo -e "${GREEN}Bitte starte den Server neu, um die Änderungen zu übernehmen.${NC}"
