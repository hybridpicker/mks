#!/bin/bash

# Deployment-Script für die Tanz-App auf dem Produktionsserver
# Dieses Script führt folgende Schritte aus:
# 1. Erstellt ein Backup der Datenbank
# 2. Fügt die location-Spalte zur dance_timeslot-Tabelle hinzu
# 3. Weist die Standorte für die Lehrer zu
# 4. Sammelt die statischen Dateien

set -e

# Farbige Ausgabe
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Deployment der Tanz-App ===${NC}"

# Django-Verzeichnis
DJANGO_DIR=$(dirname "$0")
cd "$DJANGO_DIR"

# Überprüfe, ob das Verzeichnis wirklich ein Django-Projekt ist
if [ ! -f "manage.py" ]; then
    echo -e "${RED}Fehler: manage.py nicht gefunden. Sind Sie im richtigen Verzeichnis?${NC}"
    exit 1
fi

# 1. Erstelle ein Backup der Datenbank (nur für MySQL und PostgreSQL)
echo -e "${YELLOW}Erstelle ein Backup der Datenbank...${NC}"

DB_ENGINE=$(python -c "from django.conf import settings; print(settings.DATABASES['default']['ENGINE'])")
DB_NAME=$(python -c "from django.conf import settings; print(settings.DATABASES['default']['NAME'])")

BACKUP_DIR="backups"
mkdir -p $BACKUP_DIR

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql"

if [[ "$DB_ENGINE" == *"mysql"* ]]; then
    echo -e "${YELLOW}MySQL-Datenbank erkannt.${NC}"
    mysqldump -u $(python -c "from django.conf import settings; print(settings.DATABASES['default']['USER'])") \
              -p$(python -c "from django.conf import settings; print(settings.DATABASES['default']['PASSWORD'])") \
              $DB_NAME > $BACKUP_FILE
elif [[ "$DB_ENGINE" == *"postgresql"* ]]; then
    echo -e "${YELLOW}PostgreSQL-Datenbank erkannt.${NC}"
    PGPASSWORD=$(python -c "from django.conf import settings; print(settings.DATABASES['default']['PASSWORD'])") \
    pg_dump -U $(python -c "from django.conf import settings; print(settings.DATABASES['default']['USER'])") \
            -h $(python -c "from django.conf import settings; print(settings.DATABASES['default']['HOST'] or 'localhost')") \
            $DB_NAME > $BACKUP_FILE
else
    echo -e "${YELLOW}Andere Datenbank-Engine erkannt, überspringe Backup.${NC}"
    BACKUP_FILE="kein_backup_erstellt"
fi

echo -e "${GREEN}Datenbank-Backup erstellt: $BACKUP_FILE${NC}"

# 2. Füge die location-Spalte zur dance_timeslot-Tabelle hinzu
echo -e "${YELLOW}Füge die location-Spalte zur dance_timeslot-Tabelle hinzu...${NC}"
python manage.py fix_timeslot_location --force-sql

# 3. Weise die Standorte für die Lehrer zu
echo -e "${YELLOW}Weise die Standorte für die Lehrer zu...${NC}"
python manage.py assign_locations

# 4. Sammle die statischen Dateien
echo -e "${YELLOW}Sammle statische Dateien...${NC}"
python manage.py collectstatic --noinput

echo -e "${GREEN}=== Deployment der Tanz-App abgeschlossen ===${NC}"
echo -e "${GREEN}Die Tanz-App ist jetzt einsatzbereit.${NC}"
echo -e "${YELLOW}Besuchen Sie die Seite unter: /tanz-und-bewegung/${NC}"
