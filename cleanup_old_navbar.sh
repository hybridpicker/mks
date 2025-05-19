#!/bin/bash

# MKS Overlay Menu - Cleanup und Migration Script
# Dieses Script räumt alte Navigation-Dateien auf und organisiert das Projekt

echo "🚀 MKS Overlay Menu - Cleanup wird gestartet..."

# Farben für die Ausgabe
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Projekt-Root-Verzeichnis
PROJECT_ROOT="/Users/lukasschonsgibl/Coding/Django/mks"

# Prüfen ob wir im richtigen Verzeichnis sind
if [ ! -f "$PROJECT_ROOT/manage.py" ]; then
    echo -e "${RED}❌ Error: Nicht im Django Projekt-Verzeichnis!${NC}"
    echo "Expected: $PROJECT_ROOT"
    exit 1
fi

echo -e "${BLUE}📁 Arbeite in: $PROJECT_ROOT${NC}"

# 1. Alte Navigation-Dateien organisieren
echo -e "\n${YELLOW}📂 Organisiere alte Navigation-Dateien...${NC}"

# Erstelle Backup-Ordner falls nicht vorhanden
BACKUP_DIR="$PROJECT_ROOT/templates/templates/old_navbar_backups"
mkdir -p "$BACKUP_DIR"

# Backup alte Navbar-Dateien
OLD_NAVBAR_FILES=(
    "user_navbar_backup.html"
    "user_navbar_enhanced.html"
    "user_navbar_fix.html"
)

for file in "${OLD_NAVBAR_FILES[@]}"; do
    OLD_PATH="$PROJECT_ROOT/templates/templates/$file"
    NEW_PATH="$BACKUP_DIR/$file"
    
    if [ -f "$OLD_PATH" ]; then
        mv "$OLD_PATH" "$NEW_PATH"
        echo -e "${GREEN}✅ Moved: $file → old_navbar_backups/${NC}"
    fi
done

# 2. Alte CSS-Dateien aufräumen
echo -e "\n${YELLOW}🎨 Räume alte CSS-Dateien auf...${NC}"

# Backup alte CSS-Dateien
OLD_CSS_FILES=(
    "overlay_menu.css"
)

for file in "${OLD_CSS_FILES[@]}"; do
    OLD_PATH="$PROJECT_ROOT/static/css/navigation/$file"
    
    if [ -f "$OLD_PATH" ]; then
        # Umbenennen zu .old
        mv "$OLD_PATH" "${OLD_PATH}.old"
        echo -e "${GREEN}✅ Backed up: $file → $file.old${NC}"
    fi
done

# 3. Alte JavaScript-Dateien aufräumen  
echo -e "\n${YELLOW}📜 Räume alte JavaScript-Dateien auf...${NC}"

OLD_JS_FILES=(
    "overlay_menu.js"
)

for file in "${OLD_JS_FILES[@]}"; do
    OLD_PATH="$PROJECT_ROOT/static/js/navigation/$file"
    
    if [ -f "$OLD_PATH" ]; then
        # Umbenennen zu .old
        mv "$OLD_PATH" "${OLD_PATH}.old"
        echo -e "${GREEN}✅ Backed up: $file → $file.old${NC}"
    fi
done

# 4. Prüfe neue Dateien
echo -e "\n${YELLOW}🔍 Überprüfe neue Dateien...${NC}"

NEW_FILES=(
    "static/css/navigation/mks_overlay_menu.css"
    "static/js/navigation/mks_overlay_menu.js"
    "templates/navigation/mks_overlay_menu.html"
    "templates/templates/user_navbar.html"
)

ALL_FILES_EXIST=true

for file in "${NEW_FILES[@]}"; do
    FULL_PATH="$PROJECT_ROOT/$file"
    
    if [ -f "$FULL_PATH" ]; then
        # Dateigröße prüfen
        SIZE=$(stat -f%z "$FULL_PATH" 2>/dev/null || stat -c%s "$FULL_PATH" 2>/dev/null)
        echo -e "${GREEN}✅ $file (${SIZE} bytes)${NC}"
    else
        echo -e "${RED}❌ Missing: $file${NC}"
        ALL_FILES_EXIST=false
    fi
done

# 5. Static Files sammeln
if [ "$ALL_FILES_EXIST" = true ]; then
    echo -e "\n${YELLOW}📦 Sammle Static Files...${NC}"
    cd "$PROJECT_ROOT"
    python manage.py collectstatic --noinput
    echo -e "${GREEN}✅ Static Files gesammelt${NC}"
else
    echo -e "\n${RED}⚠️ Einige Dateien fehlen. Static Files werden NICHT gesammelt.${NC}"
fi

# 6. Git Status (falls Git Repository)
if [ -d "$PROJECT_ROOT/.git" ]; then
    echo -e "\n${YELLOW}📊 Git Status:${NC}"
    cd "$PROJECT_ROOT"
    git status --porcelain | head -10
    
    if [ $(git status --porcelain | wc -l) -gt 0 ]; then
        echo -e "\n${BLUE}💭 Möchten Sie die Änderungen committen? (y/n)${NC}"
        read -r COMMIT_CHANGES
        
        if [ "$COMMIT_CHANGES" = "y" ] || [ "$COMMIT_CHANGES" = "Y" ]; then
            git add .
            git commit -m "feat: implement new MKS overlay menu v2.0

- Replace old navigation system with modern overlay menu
- Add accessibility features (WCAG 2.1 AA)
- Implement responsive design for mobile/tablet
- Add touch gesture support
- Integrate MKS brand colors and design system
- Add loading states and animations
- Include statistics dashboard
- Backup old navigation files"
            echo -e "${GREEN}✅ Änderungen committed${NC}"
        fi
    fi
fi

# 7. Zusammenfassung
echo -e "\n${GREEN}🎉 Cleanup abgeschlossen!${NC}"
echo -e "\n${BLUE}📋 Zusammenfassung:${NC}"
echo -e "• Alte Navbar-Dateien → ${BACKUP_DIR}"
echo -e "• Alte CSS/JS-Dateien → *.old backups"
echo -e "• Neue Overlay Menu Dateien überprüft"
echo -e "• Static Files gesammelt"

echo -e "\n${YELLOW}🔄 Nächste Schritte:${NC}"
echo -e "1. Django Development Server starten"
echo -e "2. Overlay Menu in Browser testen"
echo -e "3. Mobile Responsiveness prüfen"
echo -e "4. Accessibility mit Screen Reader testen"

echo -e "\n${BLUE}📖 Dokumentation: OVERLAY_MENU_DOCUMENTATION.md${NC}"

# 8. Development Server starten? (Optional)
echo -e "\n${BLUE}🚀 Development Server starten? (y/n)${NC}"
read -r START_SERVER

if [ "$START_SERVER" = "y" ] || [ "$START_SERVER" = "Y" ]; then
    echo -e "${YELLOW}🔄 Starte Django Development Server...${NC}"
    cd "$PROJECT_ROOT"
    python manage.py runserver
fi
