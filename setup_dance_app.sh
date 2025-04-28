#!/bin/bash

# Setup-Skript für die Tanz-App
# Dieses Skript:
# 1. Prüft, ob die dance_fixture.json existiert und repariert sie
# 2. Lädt die Fixtures in die Datenbank
# 3. Sammelt die statischen Dateien

set -e

# Farbige Ausgabe
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Setup der Tanz-App ===${NC}"

# Django-Verzeichnis
DJANGO_DIR=$(dirname "$0")
cd "$DJANGO_DIR"

# Überprüfe, ob das Verzeichnis wirklich ein Django-Projekt ist
if [ ! -f "manage.py" ]; then
    echo -e "${RED}Fehler: manage.py nicht gefunden. Sind Sie im richtigen Verzeichnis?${NC}"
    exit 1
fi

# 1. Prüfe, ob die dance_fixture.json existiert
echo -e "${YELLOW}Überprüfe die dance_fixture.json...${NC}"
if [ -f "dance_fixture.json" ]; then
    echo -e "${GREEN}Die dance_fixture.json existiert.${NC}"
    
    # Repariere die Fixture-Datei mit dem Django-Management-Kommando
    echo -e "${YELLOW}Repariere die Fixture-Datei...${NC}"
    python manage.py fix_dance_fixture --path dance_fixture.json
    
    # Aktualisiere die Standorte in der Fixture-Datei
    echo -e "${YELLOW}Aktualisiere Standorte in der Fixture-Datei...${NC}"
    python manage.py update_dance_locations --input dance_fixture.json --output dance_fixture.json
else
    echo -e "${YELLOW}Die dance_fixture.json existiert nicht, verwende die Fixture aus dem dance-App-Ordner...${NC}"
    
    # Prüfe, ob die Fixture in dance/fixtures existiert
    if [ -f "dance/fixtures/dance_data.json" ]; then
        echo -e "${YELLOW}Kopiere dance/fixtures/dance_data.json nach dance_fixture.json...${NC}"
        cp dance/fixtures/dance_data.json dance_fixture.json
        
        # Repariere die Fixture-Datei mit dem Django-Management-Kommando
        echo -e "${YELLOW}Repariere die Fixture-Datei...${NC}"
        python manage.py fix_dance_fixture --path dance_fixture.json
        
        # Aktualisiere die Standorte in der Fixture-Datei
        echo -e "${YELLOW}Aktualisiere Standorte in der Fixture-Datei...${NC}"
        python manage.py update_dance_locations --input dance_fixture.json --output dance_fixture.json
    else
        echo -e "${RED}Keine Fixture-Datei gefunden. Die Standard-Daten werden später geladen.${NC}"
    fi
fi

# 2. Lade die Daten in die Datenbank
echo -e "${YELLOW}Lade die Daten in die Datenbank...${NC}"

# Prüfe, ob wir PostgreSQL oder SQLite verwenden
if grep -q "postgresql" mks/settings.py; then
    echo -e "${YELLOW}PostgreSQL-Datenbank erkannt.${NC}"
    
    # Überprüfe, ob PostgreSQL läuft
    if ! command -v pg_isready &> /dev/null; then
        echo -e "${RED}PostgreSQL-Client nicht gefunden. Überspringe Datenbankprüfung.${NC}"
    else
        if ! pg_isready -h localhost -U postgres > /dev/null 2>&1; then
            echo -e "${RED}PostgreSQL ist nicht erreichbar. Bitte stellen Sie sicher, dass der Datenbankserver läuft.${NC}"
            exit 1
        fi
    fi
else
    echo -e "${YELLOW}SQLite-Datenbank erkannt.${NC}"
fi

# Migrationen durchführen
echo -e "${YELLOW}Führe Migrationen durch...${NC}"
python manage.py migrate

# Lade die Fixtures mit dem Management-Kommando
echo -e "${YELLOW}Lade die Tanzdaten...${NC}"
python manage.py load_dance_fixture

# 3. Sammle die statischen Dateien
echo -e "${YELLOW}Sammle statische Dateien...${NC}"
python manage.py collectstatic --noinput

echo -e "${GREEN}=== Tanz-App Setup abgeschlossen ===${NC}"
echo -e "${GREEN}Die Tanz-App ist jetzt einsatzbereit.${NC}"
echo -e "${YELLOW}Besuchen Sie die Seite unter: http://localhost:8000/tanz-und-bewegung/${NC}"
