#!/bin/bash

# CSS Analysis Script
# ===================
# Analyzing CSS files and references in MKS Django project

echo "=== CSS FILES & REFERENCES ANALYSIS ==="
echo "========================================"
echo

PROJECT_ROOT="/Users/lukasschonsgibl/Coding/Django/mks"

echo "📁 MAIN CSS FILES FOUND:"
echo "========================"

# Main CSS files (excluding animate library)
echo "MKS Core CSS Files:"
find "$PROJECT_ROOT/static/css" -name "*.css" -not -path "*/animate/*" | sort
echo

echo "Gallery CSS Files:"
find "$PROJECT_ROOT/static/gallery" -name "*.css" | sort
echo

echo "🔍 CHECKING MAIN CSS REFERENCES:"
echo "================================"

echo "1. Base Template (templates/templates/base.html):"
grep -n "\.css" "$PROJECT_ROOT/templates/templates/base.html" | head -5
echo

echo "2. User Navbar Template:"
grep -n "\.css" "$PROJECT_ROOT/templates/templates/user_navbar.html" | head -3
echo

echo "3. Gallery Template:"
grep -n "\.css" "$PROJECT_ROOT/templates/gallery/gallery.html" | head -3
echo

echo "🎯 VERSIONIERTE CSS FILES:"
echo "========================="
echo "Files with version numbers in name:"
find "$PROJECT_ROOT" -name "*.css" | grep -E '\.[0-9]+\.[0-9]+\.[0-9]+\.css$'
echo

echo "📊 CSS REFERENCE VALIDATION:"
echo "============================"

# Check if referenced CSS files exist
echo "Checking main referenced files:"

CSS_FILES=(
    "css/mks/mks_v2.5.0.css"
    "css/mks/logout_fix.css"
    "css/admin_nav.css"
    "css/navigation/mks_overlay_menu.css"
    "css/mobile-enhancements.css"
    "gallery/css/modern/gallery.3.0.0.css"
)

for css_file in "${CSS_FILES[@]}"; do
    if [ -f "$PROJECT_ROOT/static/$css_file" ]; then
        echo "✅ $css_file - EXISTS"
    else
        echo "❌ $css_file - MISSING"
    fi
done

echo
echo "🔗 BROKEN REFERENCES CHECK:"
echo "==========================="

# Search for common broken reference patterns
echo "Searching for incomplete CSS references..."
grep -r "\.css'" "$PROJECT_ROOT/templates" | grep -v "{% static" | head -5
echo

echo "✨ ANALYSIS COMPLETE"
echo "==================="
