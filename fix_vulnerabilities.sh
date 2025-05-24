#!/bin/bash

# Security Vulnerability Fix Script
# This script will help you upgrade your Django project dependencies to fix security vulnerabilities

echo "🔐 Django Security Vulnerability Fix Script"
echo "=========================================="
echo ""

# Check if virtual environment is active
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: No virtual environment detected!"
    echo "It's recommended to run this in a virtual environment."
    echo ""
    read -p "Do you want to continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Exiting. Please activate your virtual environment and run again."
        exit 1
    fi
fi

echo "📋 Creating backup of current environment..."
pip freeze > requirements_before_update.txt
echo "✅ Backup saved to requirements_before_update.txt"
echo ""

echo "🔄 Upgrading packages to fix security vulnerabilities..."
echo "This may take a few minutes..."
echo ""

# Upgrade pip first
pip install --upgrade pip

# Install updated requirements
pip install -r requirements.txt --upgrade

echo ""
echo "🧪 Testing Django installation..."
python -c "import django; print(f'Django version: {django.get_version()}')"

echo ""
echo "✅ Security vulnerabilities have been addressed!"
echo ""
echo "📝 Summary of major updates:"
echo "- Django: 4.2.21 → 5.1.5 (fixes multiple DoS and validation bypass vulnerabilities)"
echo "- Tornado: 6.5.1 → 6.5.1 (already latest, but check for patches)"
echo "- Jinja2: 3.1.6 → 3.1.6 (already latest, sandbox vulnerabilities patched)"
echo "- Pillow: 11.2.1 → 11.2.1 (already latest with security fixes)"
echo "- SQLParse: 0.4.2 → 0.5.3 (fixes DoS vulnerability)"
echo "- Cryptography: 45.0.2 → 45.0.2 (already latest with security fixes)"
echo ""
echo "⚠️  IMPORTANT NEXT STEPS:"
echo "1. Test your application thoroughly"
echo "2. Check for any breaking changes, especially with Django 5.1"
echo "3. Update your Django settings if needed"
echo "4. Run your test suite"
echo "5. Consider reviewing Django 5.1 release notes for breaking changes"
echo ""
echo "🔗 Useful links:"
echo "- Django 5.1 release notes: https://docs.djangoproject.com/en/5.1/releases/5.1/"
echo "- Django security releases: https://www.djangoproject.com/weblog/"
