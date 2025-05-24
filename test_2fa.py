#!/usr/bin/env python3
"""
Quick test script to verify 2FA functionality
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from users.models import CustomUser
import pyotp

def test_2fa_functionality():
    print("🧪 Testing 2FA Functionality")
    print("=" * 40)
    
    try:
        # Test 1: Check if CustomUser has 2FA fields
        print("✅ Test 1: CustomUser model has 2FA fields")
        user_fields = [field.name for field in CustomUser._meta.fields]
        required_fields = ['totp_secret', 'is_2fa_enabled', 'backup_codes']
        
        for field in required_fields:
            if field in user_fields:
                print(f"   ✅ {field} field exists")
            else:
                print(f"   ❌ {field} field missing")
                return False
        
        # Test 2: Test TOTP secret generation
        print("\n✅ Test 2: TOTP secret generation")
        test_user = CustomUser(email="test@example.com", username="testuser")
        secret = test_user.generate_totp_secret()
        if secret and len(secret) == 32:
            print(f"   ✅ Generated secret: {secret[:8]}...")
        else:
            print(f"   ❌ Invalid secret generated: {secret}")
            return False
        
        # Test 3: Test TOTP verification
        print("\n✅ Test 3: TOTP verification")
        totp = pyotp.TOTP(secret)
        current_token = totp.now()
        print(f"   ℹ️  Current token: {current_token}")
        
        if test_user.verify_totp(current_token):
            print("   ✅ TOTP verification working")
        else:
            print("   ❌ TOTP verification failed")
            return False
        
        # Test 4: Test QR code generation
        print("\n✅ Test 4: QR code generation")
        qr_code = test_user.get_qr_code()
        if qr_code and qr_code.startswith('data:image/png;base64,'):
            print("   ✅ QR code generated successfully")
        else:
            print("   ❌ QR code generation failed")
            return False
        
        # Test 5: Test backup codes
        print("\n✅ Test 5: Backup codes generation")
        backup_codes = test_user.generate_backup_codes()
        if len(backup_codes) == 10:
            print(f"   ✅ Generated {len(backup_codes)} backup codes")
            print(f"   ℹ️  Sample code: {backup_codes[0]}")
        else:
            print(f"   ❌ Expected 10 backup codes, got {len(backup_codes)}")
            return False
        
        print("\n" + "=" * 40)
        print("🎉 All tests passed! 2FA is ready to use.")
        print("\nYou can now:")
        print("1. Start your server: python3 manage.py runserver")
        print("2. Login and go to /team/2fa/settings/")
        print("3. Enable 2FA for your account")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_2fa_functionality()
    sys.exit(0 if success else 1)
