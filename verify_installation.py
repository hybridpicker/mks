#!/usr/bin/env python3
"""
Verification script to check if the gallery image resize implementation is correctly installed.
"""

import os

def check_file_exists(filepath, description):
    """Check if a file exists and show status"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✅ {description}: {filepath} ({size} bytes)")
        return True
    else:
        print(f"❌ {description}: {filepath} - NOT FOUND")
        return False

def main():
    print("Gallery Image Resize Implementation Verification")
    print("=" * 60)
    
    base_path = "/Users/lukasschonsgibl/Coding/Django/mks"
    all_good = True
    
    # Check main files
    files_to_check = [
        ("gallery/image_utils.py", "Image processing utilities"),
        ("gallery/gallery_admin_views.py", "Updated admin views"),
        ("gallery/gallery_admin_views_backup.py", "Backup of original admin views"),
        ("gallery/management/commands/resize_existing_images.py", "Management command"),
        ("test_image_resize.py", "Django integration test"),
        ("simple_test_pillow.py", "Basic Pillow test"),
    ]
    
    for filename, description in files_to_check:
        filepath = os.path.join(base_path, filename)
        if not check_file_exists(filepath, description):
            all_good = False
    
    print("\n" + "=" * 60)
    
    # Check if __init__.py files exist for management commands
    init_files = [
        "gallery/management/__init__.py",
        "gallery/management/commands/__init__.py",
    ]
    
    for init_file in init_files:
        filepath = os.path.join(base_path, init_file)
        if not check_file_exists(filepath, f"Django management init file ({init_file})"):
            all_good = False
    
    print("\n" + "=" * 60)
    
    if all_good:
        print("🎉 ALL FILES INSTALLED CORRECTLY!")
        print("\nNext steps:")
        print("1. Test basic functionality: python3 simple_test_pillow.py")
        print("2. Install Pillow if needed: pip install Pillow")
        print("3. Test in Django admin by uploading a large image")
        print("4. Check Django logs for processing details")
    else:
        print("❌ SOME FILES ARE MISSING!")
        print("Please check the installation process.")
    
    return all_good

if __name__ == "__main__":
    main()
