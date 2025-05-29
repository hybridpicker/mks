#!/usr/bin/env python
"""
Test script for gallery image optimization
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from gallery.image_utils import resize_image, get_image_info, process_uploaded_image
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io


def create_test_image(width, height, format='JPEG'):
    """Create a test image with specified dimensions"""
    img = Image.new('RGB', (width, height), color='red')
    buffer = io.BytesIO()
    img.save(buffer, format=format)
    buffer.seek(0)
    return SimpleUploadedFile(f"test_{width}x{height}.jpg", buffer.getvalue(), content_type="image/jpeg")


def test_image_processing():
    """Test the image processing functions"""
    print("Testing Gallery Image Optimization")
    print("-" * 50)
    
    # Test 1: Large image
    print("\nTest 1: Large image (4000x3000)")
    large_image = create_test_image(4000, 3000)
    print(f"Original size: {large_image.size / 1024:.1f} KB")
    
    processed = process_uploaded_image(large_image)
    if processed['main']:
        info = get_image_info(processed['main'])
        print(f"Processed size: {info['size_mb']:.2f} MB")
        print(f"Dimensions: {info['width']}x{info['height']}")
    
    # Test 2: Very large image
    print("\nTest 2: Very large image (8000x6000)")
    huge_image = create_test_image(8000, 6000)
    print(f"Original size: {huge_image.size / 1024 / 1024:.1f} MB")
    
    processed = process_uploaded_image(huge_image)
    if processed['main']:
        info = get_image_info(processed['main'])
        print(f"Processed size: {info['size_mb']:.2f} MB")
        print(f"Dimensions: {info['width']}x{info['height']}")
        
    # Test 3: Check all variants
    print("\nTest 3: Check all image variants")
    test_image = create_test_image(3000, 2000)
    processed = process_uploaded_image(test_image)
    
    for variant, image in processed.items():
        if image:
            info = get_image_info(image)
            print(f"{variant.capitalize()}: {info['width']}x{info['height']}, {info['size_mb']:.2f} MB")
    
    print("\n✅ Testing complete!")


if __name__ == "__main__":
    test_image_processing()
