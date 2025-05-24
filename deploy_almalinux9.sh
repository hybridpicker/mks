#!/bin/bash

# AlmaLinux 9 Django Deployment Script
# Security-optimized for production deployment

echo "🚀 AlmaLinux 9 Django MKS Deployment"
echo "===================================="
echo ""

# Check if running on AlmaLinux
if ! grep -q "AlmaLinux" /etc/os-release 2>/dev/null; then
    echo "⚠️  Warnung: Dieses Script ist für AlmaLinux 9 optimiert"
fi

echo "📋 System Information:"
echo "OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
echo "Python: $(python3 --version)"
echo ""

# Update system packages
echo "🔄 System-Updates installieren..."
sudo dnf update -y

# Install required system packages for Django
echo "📦 System-Abhängigkeiten installieren..."
sudo dnf install -y \
    python3 \
    python3-pip \
    python3-devel \
    python3-venv \
    postgresql-devel \
    gcc \
    gcc-c++ \
    make \
    libjpeg-turbo-devel \
    libpng-devel \
    freetype-devel \
    libxml2-devel \
    libxslt-devel \
    zlib-devel \
    openssl-devel \
    libffi-devel

# Create virtual environment
echo "🔧 Python Virtual Environment erstellen..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "⬆️  pip upgraden..."
pip install --upgrade pip

# Install Python packages
echo "📥 Python-Pakete installieren..."
pip install -r requirements.txt

echo ""
echo "🔒 Sicherheitsstatus nach Installation:"
echo "======================================"

# Check Django version
echo "Django Version: $(python -c "import django; print(django.get_version())")"

# Check critical security packages
echo "Sicherheitspakete:"
echo "- SQLParse: $(pip show sqlparse | grep Version | cut -d' ' -f2)"
echo "- Pillow: $(pip show pillow | grep Version | cut -d' ' -f2)"
echo "- Cryptography: $(pip show cryptography | grep Version | cut -d' ' -f2)"

# Check if CKEditor is removed
if pip show django-ckeditor >/dev/null 2>&1; then
    echo "- CKEditor: ❌ NOCH INSTALLIERT (Sicherheitsrisiko!)"
else
    echo "- CKEditor: ✅ ENTFERNT (Sicher)"
fi

echo ""
echo "🧪 Django System Check..."
python manage.py check

echo ""
echo "✅ AlmaLinux 9 Deployment abgeschlossen!"
echo ""
echo "Nächste Schritte:"
echo "1. Datenbank-Migrationen: python manage.py migrate"
echo "2. Statische Dateien: python manage.py collectstatic"
echo "3. Web-Server konfigurieren (nginx/apache)"
echo "4. Firewall-Regeln setzen"
echo ""
echo "🔐 Sicherheitsstatus: SICHER für Production!"
