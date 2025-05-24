#!/bin/bash

# Comprehensive Security Vulnerability Fix Script for Conda Environment
echo "🔐 Comprehensive Security Fix for MKS Django Project"
echo "=================================================="
echo ""

# Activate conda environment
source /Users/lukasschonsgibl/opt/anaconda3/etc/profile.d/conda.sh
conda activate mks

echo "📋 Current environment: $(conda info --envs | grep '*' | awk '{print $1}')"
echo ""

# Create backup
echo "📋 Creating backup of current environment..."
pip freeze > requirements_before_security_fix.txt
echo "✅ Backup saved to requirements_before_security_fix.txt"
echo ""

echo "🔄 Upgrading vulnerable packages..."
echo ""

# Upgrade critical security packages
echo "Upgrading Django to latest secure version..."
pip install --upgrade "Django>=5.1,<6.0"

echo "Upgrading Pillow to latest secure version..."
pip install --upgrade "Pillow>=10.0.0"

echo "Upgrading SQLParse to latest secure version..."
pip install --upgrade "sqlparse>=0.5.0"

echo "Upgrading Tornado to latest secure version..."
pip install --upgrade "tornado>=6.4.0"

echo "Upgrading Jinja2 to latest secure version..."
pip install --upgrade "Jinja2>=3.1.6"

echo "Upgrading Cryptography to latest secure version..."
pip install --upgrade "cryptography>=42.0.0"

echo "Upgrading urllib3 to latest secure version..."
pip install --upgrade "urllib3>=2.2.0"

echo "Upgrading certifi to latest secure version..."
pip install --upgrade "certifi>=2024.0.0"

# Remove vulnerable CKEditor if still present
echo "Removing django-ckeditor..."
pip uninstall django-ckeditor -y

# Update other packages to secure versions
echo "Updating other Django packages..."
pip install --upgrade django-allauth django-extensions django-tinymce

echo ""
echo "🧪 Testing Django installation..."
python -c "import django; print(f'Django version: {django.get_version()}')"

echo ""
echo "🔍 Running Django security check..."
python manage.py check

echo ""
echo "📝 Creating updated requirements.txt..."
pip freeze > requirements.txt

echo ""
echo "✅ Security vulnerability fix complete!"
echo ""
echo "📊 Summary of major upgrades:"
echo "- Django: 4.2.21 → Latest (5.1+)"
echo "- Pillow: 11.2.1 → Latest (security patches)"
echo "- SQLParse: 0.4.2 → 0.5+ (DoS fix)"
echo "- Tornado: 6.5.1 → Latest (multipart/cookie fixes)"
echo "- Jinja2: 3.1.6 → Latest (sandbox fixes)"
echo "- Cryptography: 45.0.2 → Latest (timing attack fix)"
echo "- Removed: django-ckeditor (security vulnerability)"
echo ""
echo "⚠️  IMPORTANT: Test your application thoroughly after this upgrade!"
