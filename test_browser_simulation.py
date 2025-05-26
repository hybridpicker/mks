#!/usr/bin/env python
"""
Simulate Browser Blog Post Creation with Image
"""

import os
import sys
from PIL import Image
import io

project_root = '/Users/lukasschonsgibl/Coding/Django/mks'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

def create_test_image(width=800, height=600, format='JPEG'):
    """Create a test image"""
    img = Image.new('RGB', (width, height), color='blue')
    img_io = io.BytesIO()
    img.save(img_io, format=format)
    img_io.seek(0)
    return img_io.getvalue()

def test_blog_creation_with_image():
    """Test blog creation through Django test client"""
    print("Testing blog creation with image via Django test client...")
    
    # Create test client
    client = Client()
    
    # Get or create a test user
    User = get_user_model()
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"Created test user: {user.username}")
    
    # Login
    login_success = client.login(username='testuser', password='testpass123')
    print(f"Login successful: {login_success}")
    
    if not login_success:
        print("Cannot login - check if user exists and has correct password")
        return False
    
    # Create test image
    image_data = create_test_image()
    test_image = SimpleUploadedFile(
        name='test_blog_image.jpg',
        content=image_data,
        content_type='image/jpeg'
    )
    
    # Prepare form data
    form_data = {
        'title': 'Test Blog Post with Image via Client',
        'content': '<p>This is a test blog post created via Django test client with an image.</p>',
        'lead_paragraph': 'This is the lead paragraph for the test post.',
        'meta_title': 'Test Blog Post SEO Title',
        'meta_description': 'This is the meta description for the test blog post.',
        'published': False,
        'save-draft': 'Save Draft',
        
        # Gallery formset management form
        'gallery_images-TOTAL_FORMS': '0',
        'gallery_images-INITIAL_FORMS': '0',
        'gallery_images-MIN_NUM_FORMS': '0',
        'gallery_images-MAX_NUM_FORMS': '10',
    }
    
    files_data = {
        'image': test_image
    }
    
    print("Sending POST request to /blogedit/new")
    
    # Make POST request
    response = client.post('/blogedit/new', data=form_data, files=files_data, follow=True)
    
    print(f"Response status code: {response.status_code}")
    print(f"Response redirect chain: {response.redirect_chain}")
    print(f"Final URL: {response.wsgi_request.path}")
    
    # Check if we were redirected to success page
    if response.status_code == 200:
        if 'thanks' in response.wsgi_request.path:
            print("✓ Successfully redirected to thanks page")
            return True
        else:
            print("✗ Not redirected to thanks page")
            print("Response content preview:")
            content = response.content.decode('utf-8')
            # Look for form errors
            if 'error-message' in content:
                print("Found form errors in response")
                start = content.find('error-message')
                end = content.find('</div>', start)
                if end > start:
                    error_section = content[start:end+6]
                    print(f"Error section: {error_section}")
            return False
    else:
        print(f"✗ Unexpected status code: {response.status_code}")
        return False

def check_logs():
    """Check Django logs for errors"""
    print("\nChecking logs for errors...")
    
    log_file = os.path.join(project_root, 'logs', 'django.log')
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                log_content = f.read()
                if log_content:
                    lines = log_content.split('\n')
                    recent_lines = lines[-50:]  # Last 50 lines
                    
                    error_lines = [line for line in recent_lines if 'ERROR' in line or 'CRITICAL' in line]
                    
                    if error_lines:
                        print("Recent errors found in logs:")
                        for line in error_lines[-10:]:  # Last 10 errors
                            print(f"  {line}")
                    else:
                        print("No recent errors found in logs")
                else:
                    print("Log file is empty")
        except Exception as e:
            print(f"Cannot read log file: {e}")
    else:
        print("Log file does not exist")

def main():
    print("BLOG IMAGE UPLOAD BROWSER SIMULATION")
    print("=" * 50)
    
    try:
        success = test_blog_creation_with_image()
        check_logs()
        
        if success:
            print("\n✅ BLOG CREATION WITH IMAGE SUCCESSFUL!")
            print("The image upload functionality is working correctly.")
        else:
            print("\n❌ BLOG CREATION FAILED!")
            print("There are issues with the image upload functionality.")
            print("\nTroubleshooting steps:")
            print("1. Check Django logs above for errors")
            print("2. Verify media directory permissions")
            print("3. Check form validation in the browser")
            print("4. Test with different image sizes/formats")
            
    except Exception as e:
        print(f"\n❌ TEST FAILED WITH EXCEPTION: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
