#!/usr/bin/env python3
"""
Debug script for 2FA setup issues on deployment server
"""

import os
import django
import logging

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from django.conf import settings
from users.models import CustomUser

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_2fa_setup():
    """Debug 2FA setup functionality"""
    print("=== 2FA Setup Debug ===")
    
    # Check database connection
    try:
        user_count = CustomUser.objects.count()
        print(f"✓ Database connection OK - {user_count} users found")
    except Exception as e:
        print(f"✗ Database error: {e}")
        return
    
    # Check if we can create and verify TOTP
    try:
        # Get first user for testing
        user = CustomUser.objects.first()
        if not user:
            print("✗ No users found for testing")
            return
            
        print(f"Testing with user: {user.email}")
        
        # Generate secret
        secret = user.generate_totp_secret()
        print(f"✓ Generated TOTP secret: {secret[:8]}...")
        
        # Try to generate QR code
        try:
            qr_code = user.get_qr_code()
            print(f"✓ QR code generated (length: {len(qr_code)})")
        except Exception as e:
            print(f"✗ QR code generation failed: {e}")
        
        # Test TOTP verification with current time
        import pyotp
        totp = pyotp.TOTP(secret)
        current_token = totp.now()
        print(f"Current TOTP token: {current_token}")
        
        # Verify token
        is_valid = user.verify_totp(current_token, allow_reuse=True)
        print(f"✓ TOTP verification: {'PASS' if is_valid else 'FAIL'}")
        
    except Exception as e:
        print(f"✗ TOTP test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_2fa_setup()
