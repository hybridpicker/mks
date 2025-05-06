#!/bin/bash

# Skript zum Sichern und Wiederherstellen der Dance-App-Fixture-Datei

# Farbige Ausgabe
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

FIXTURE_PATH="dance/fixtures/dance_data.json"
BACKUP_PATH="dance/fixtures/dance_data_backup.json"

# Funktion zum Sichern der Fixture-Datei
backup_fixture() {
    echo -e "${YELLOW}Sichere Fixture-Datei...${NC}"
    if [ -f "$FIXTURE_PATH" ]; then
        cp "$FIXTURE_PATH" "$BACKUP_PATH"
        echo -e "${GREEN}Fixture-Datei gesichert: $BACKUP_PATH${NC}"
    else
        echo -e "${RED}Fixture-Datei nicht gefunden: $FIXTURE_PATH${NC}"
        exit 1
    fi
}

# Funktion zum Wiederherstellen der Fixture-Datei
restore_fixture() {
    echo -e "${YELLOW}Stelle Fixture-Datei wieder her...${NC}"
    if [ -f "$BACKUP_PATH" ]; then
        cp "$BACKUP_PATH" "$FIXTURE_PATH"
        echo -e "${GREEN}Fixture-Datei wiederhergestellt: $FIXTURE_PATH${NC}"
    else
        echo -e "${RED}Backup der Fixture-Datei nicht gefunden: $BACKUP_PATH${NC}"
        exit 1
    fi
}

# Hauptskript
case "$1" in
    backup)
        backup_fixture
        ;;
    restore)
        restore_fixture
        ;;
    *)
        echo -e "${YELLOW}Verwendung: $0 {backup|restore}${NC}"
        exit 1
        ;;
esac

exit 0
