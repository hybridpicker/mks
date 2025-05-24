#!/usr/bin/env python3
"""
Setup script for Two-Factor Authentication in Django MKS project
Run this after creating all the 2FA files
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e.stderr.strip() if e.stderr else str(e)}")
        return False

def main():
    print("🚀 Django MKS - Two-Factor Authentication Setup")
    print("=" * 50)
    
    # Check if we're in the right directory 
    if not os.path.exists('manage.py'):
        print("❌ Error: Please run this script from the Django project root directory")
        print("   Expected to find manage.py in current directory")
        sys.exit(1)
    
    # Check if 2FA files exist
    required_files = [
        'users/twofa_forms.py',
        'users/twofa_views.py', 
        'templates/users/2fa_setup.html',
        'templates/users/2fa_verify.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Error: Missing required 2FA files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\n   Please ensure all 2FA files have been created first.")
        sys.exit(1)
    
    # Step 1: Apply migrations
    success = run_command('python3 manage.py migrate users', 'Applying database migrations')
    if not success:
        print("\n⚠️  Migration failed. Please check your database connection and try again.")
        return
    
    # Step 2: Collect static files (if needed)
    run_command('python3 manage.py collectstatic --noinput', 'Collecting static files')
    
    # Step 3: Check system
    success = run_command('python3 manage.py check', 'Running system checks')
    if not success:
        print("\n⚠️  System check failed. Please review the errors above.")
        return
    
    # Step 4: Create superuser if needed
    print("\n🔄 Checking for superuser account...")
    try:
        from django.contrib.auth import get_user_model
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
        django.setup()
        
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            print("   No superuser found. You may want to create one:")
            print("   python3 manage.py createsuperuser")
        else:
            print("✅ Superuser account exists")
    except Exception as e:
        print(f"   Warning: Could not check superuser status: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 2FA Setup Complete!")
    print("\nNext Steps:")
    print("1. Start your development server: python3 manage.py runserver")
    print("2. Login to your account")
    print("3. Navigate to: http://localhost:8000/team/2fa/settings/")
    print("4. Click 'Enable 2FA' to set up your authenticator app")
    print("\nRecommended Authenticator Apps:")
    print("• Google Authenticator (recommended)")
    print("• Authy")  
    print("• Microsoft Authenticator")
    print("\n📚 Full documentation available in the setup guide")

if __name__ == '__main__':
    main()
