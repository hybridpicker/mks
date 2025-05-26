#!/usr/bin/env python
"""
Blog Image Upload Debug Script
"""

import os
import sys

project_root = '/Users/lukasschonsgibl/Coding/Django/mks'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from blog.forms import ArticleForm
from blog.models import BlogPost
import tempfile
from PIL import Image
import io

def check_media_directories():
    """Check if media directories exist and are writable"""
    print("Checking media directories...")
    
    media_root = settings.MEDIA_ROOT
    blog_media_dir = os.path.join(media_root, 'blog', 'posts', 'images')
    
    directories = [
        ('MEDIA_ROOT', media_root),
        ('Blog Media Dir', blog_media_dir),
    ]
    
    for name, directory in directories:
        print(f"\n{name}: {directory}")
        
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"  ✓ Created directory")
            except Exception as e:
                print(f"  ✗ Cannot create directory: {e}")
                return False
        else:
            print(f"  ✓ Directory exists")
        
        # Test write permissions
        test_file = os.path.join(directory, 'test_write.txt')
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            print(f"  ✓ Directory is writable")
        except Exception as e:
            print(f"  ✗ Directory not writable: {e}")
            return False
    
    return True

def create_test_image():
    """Create a test image file"""
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=img_io.getvalue(),
        content_type='image/jpeg'
    )

def test_form_validation():
    """Test form validation with image upload"""
    print("\nTesting form validation with image...")
    
    test_image = create_test_image()
    
    form_data = {
        'title': 'Test Blog Post with Image',
        'content': '<p>Test content for image upload</p>',
        'lead_paragraph': 'Test lead paragraph',
        'published': False
    }
    
    files_data = {
        'image': test_image
    }
    
    try:
        form = ArticleForm(data=form_data, files=files_data)
        
        print(f"Form is valid: {form.is_valid()}")
        
        if not form.is_valid():
            print("Form errors:")
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
            return False
        
        # Try to save the form
        blog_post = form.save()
        print(f"✓ Blog post created with ID: {blog_post.id}")
        
        if blog_post.image:
            print(f"✓ Image saved: {blog_post.image.url}")
            print(f"  File path: {blog_post.image.path}")
            print(f"  File exists: {os.path.exists(blog_post.image.path)}")
        else:
            print("✗ No image was saved")
            return False
        
        # Clean up test post
        blog_post.delete()
        print("✓ Test post cleaned up")
        
        return True
        
    except Exception as e:
        print(f"✗ Form test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_file_upload_settings():
    """Check Django file upload settings"""
    print("\nChecking file upload settings...")
    
    settings_to_check = [
        'MEDIA_ROOT',
        'MEDIA_URL',
        'FILE_UPLOAD_MAX_MEMORY_SIZE',
        'DATA_UPLOAD_MAX_MEMORY_SIZE',
        'DEFAULT_FILE_STORAGE',
    ]
    
    for setting_name in settings_to_check:
        if hasattr(settings, setting_name):
            value = getattr(settings, setting_name)
            print(f"  {setting_name}: {value}")
        else:
            print(f"  {setting_name}: Not set")
    
    # Check if we have any upload handlers
    print(f"  FILE_UPLOAD_HANDLERS: {getattr(settings, 'FILE_UPLOAD_HANDLERS', 'Default')}")

def test_image_validation():
    """Test different image types and sizes"""
    print("\nTesting image validation...")
    
    test_cases = [
        # (width, height, format, expected_result)
        (100, 100, 'JPEG', True),
        (1920, 1080, 'PNG', True),
        (50, 50, 'GIF', True),
        (5000, 5000, 'JPEG', False),  # Too large
    ]
    
    for width, height, format, expected in test_cases:
        print(f"\nTesting {width}x{height} {format} image...")
        
        try:
            # Create test image
            img = Image.new('RGB', (width, height), color='blue')
            img_io = io.BytesIO()
            img.save(img_io, format=format)
            img_io.seek(0)
            
            # Calculate approximate file size
            file_size = len(img_io.getvalue())
            print(f"  File size: {file_size / 1024 / 1024:.2f} MB")
            
            if file_size > 10 * 1024 * 1024:  # 10MB limit
                print(f"  Expected to fail: File too large")
                expected = False
            
            test_image = SimpleUploadedFile(
                name=f'test_{width}x{height}.{format.lower()}',
                content=img_io.getvalue(),
                content_type=f'image/{format.lower()}'
            )
            
            form_data = {
                'title': f'Test {width}x{height}',
                'content': '<p>Test content</p>',
            }
            
            form = ArticleForm(data=form_data, files={'image': test_image})
            is_valid = form.is_valid()
            
            if is_valid == expected:
                print(f"  ✓ Result as expected: {is_valid}")
            else:
                print(f"  ✗ Unexpected result: {is_valid}, expected: {expected}")
                if not is_valid:
                    print(f"    Errors: {form.errors}")
                    
        except Exception as e:
            print(f"  ✗ Error creating test image: {e}")

def main():
    print("BLOG IMAGE UPLOAD DEBUG")
    print("=" * 40)
    
    tests = [
        ("Media Directories", check_media_directories),
        ("File Upload Settings", lambda: (check_file_upload_settings(), True)[1]),
        ("Form Validation", test_form_validation),
        ("Image Validation", lambda: (test_image_validation(), True)[1]),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append((test_name, False))
    
    print(f"\n{'='*40}")
    print("SUMMARY:")
    print("=" * 40)
    
    all_passed = True
    for test_name, result in results:
        if result is not None:
            status = "PASS" if result else "FAIL"
            print(f"{test_name}: {status}")
            if not result:
                all_passed = False
    
    if all_passed:
        print("\n✅ All tests passed!")
        print("Image upload should work correctly.")
    else:
        print("\n❌ Some tests failed!")
        print("Check the errors above for image upload issues.")

if __name__ == "__main__":
    main()
