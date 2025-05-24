#!/usr/bin/env python3
"""
2FA Debug Script - Identifiziert mögliche Probleme auf dem Deployment Server
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

def check_dependencies():
    """Check if all required packages are installed"""
    print("🔍 Checking Dependencies...")
    
    required_packages = {
        'pyotp': 'pyotp',
        'qrcode': 'qrcode', 
        'PIL': 'Pillow'
    }
    
    missing = []
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {package} ({pip_name}) - OK")
        except ImportError:
            print(f"❌ {package} ({pip_name}) - MISSING")
            missing.append(pip_name)
    
    if missing:
        print(f"\n🚨 Install missing packages: pip install {' '.join(missing)}")
        return False
    return True

def check_database():
    """Check if 2FA fields exist in database"""
    print("\n🔍 Checking Database Schema...")
    
    from users.models import CustomUser
    
    # Check if 2FA fields exist
    expected_fields = ['totp_secret', 'is_2fa_enabled', 'backup_codes', 'twofa_reset_code', 'twofa_reset_expires']
    
    user_fields = [f.name for f in CustomUser._meta.fields]
    
    for field in expected_fields:
        if field in user_fields:
            print(f"✅ Field '{field}' exists")
        else:
            print(f"❌ Field '{field}' MISSING - Run migrations!")
            
def check_user_model():
    """Test user model methods"""
    print("\n🔍 Testing User Model Methods...")
    
    from users.models import CustomUser
    
    # Test user creation and methods
    try:
        # Try to get or create a test user (without saving sensitive data)
        print("✅ CustomUser model imports OK")
        
        # Test if methods exist
        methods_to_check = [
            'generate_totp_secret',
            'get_totp_uri', 
            'get_qr_code',
            'verify_totp',
            'generate_backup_codes',
            'use_backup_code'
        ]
        
        for method in methods_to_check:
            if hasattr(CustomUser, method):
                print(f"✅ Method '{method}' exists")
            else:
                print(f"❌ Method '{method}' MISSING")
                
    except Exception as e:
        print(f"❌ CustomUser model error: {e}")

def check_urls():
    """Check if 2FA URLs are properly configured"""
    print("\n🔍 Checking URL Configuration...")
    
    from django.urls import reverse
    
    urls_to_check = [
        'users:2fa_setup',
        'users:2fa_verify', 
        'users:2fa_disable',
        'users:2fa_settings'
    ]
    
    for url_name in urls_to_check:
        try:
            reverse(url_name)
            print(f"✅ URL '{url_name}' - OK")
        except Exception as e:
            print(f"❌ URL '{url_name}' - ERROR: {e}")
