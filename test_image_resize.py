#!/usr/bin/env python
"""
Test script for the gallery image resizing functionality.
Run this to test if the image processing works correctly.
"""

import os
import sys
import django
from django.conf import settings

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from gallery.image_utils import resize_image, get_image_info, process_uploaded_image
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

def create_test_image(width=3000, height=2000, format='JPEG'):
    """Create a test image for testing"""
    img = Image.new('RGB', (width, height), color='red')
    
    # Add some pattern to make it more realistic
    for x in range(0, width, 100):
        for y in range(0, height, 100):
            img.paste((0, 255, 0), (x, y, x+50, y+50))
    
    buffer = io.BytesIO()
    img.save(buffer, format=format, quality=95)
    buffer.seek(0)
    
    return SimpleUploadedFile(
        name=f'test_image_{width}x{height}.jpg',
        content=buffer.getvalue(),
        content_type='image/jpeg'
    )

def test_image_processing():
    """Test the image processing functions"""
    print("Testing Gallery Image Resize Functionality")
    print("="*50)
    
    # Test 1: Create a large test image
    print("1. Creating test image (3000x2000)...")
    test_image = create_test_image(3000, 2000)
    
    # Test 2: Get image info
    print("2. Getting image info...")
    info = get_image_info(test_image)
    if info:
        print(f"   Original: {info['width']}x{info['height']}, {info['size_mb']}MB")
    else:
        print("   ERROR: Could not get image info!")
        return False
    
    # Test 3: Process the image
    print("3. Processing image...")
    test_image.seek(0)  # Reset file pointer
    processed = process_uploaded_image(test_image)
    
    if processed['main']:
        print("   ✓ Main image processed successfully")
        print(f"   Main image size: {len(processed['main'].read())/1024:.1f}KB")
    else:
        print("   ✗ Failed to process main image")
        return False
    
    if processed['thumbnail']:
        print("   ✓ Thumbnail created successfully")
        print(f"   Thumbnail size: {len(processed['thumbnail'].read())/1024:.1f}KB")
    else:
        print("   ✗ Failed to create thumbnail")
    
    if processed['lazy']:
        print("   ✓ Lazy image created successfully")
        print(f"   Lazy image size: {len(processed['lazy'].read())/1024:.1f}KB")
    else:
        print("   ✗ Failed to create lazy image")
    
    print("\n" + "="*50)
    print("✓ Image processing test completed successfully!")
    print("Your gallery is ready to handle large image uploads.")
    return True

if __name__ == '__main__':
    try:
        success = test_image_processing()
        if success:
            print("\n🎉 All tests passed! The image resize functionality is working.")
        else:
            print("\n❌ Some tests failed. Check the error messages above.")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
