#!/usr/bin/env python3
"""
Simple test to verify Pillow works and our image processing logic is sound.
"""

try:
    from PIL import Image, ImageOps
    import io
    import os
    
    print("Testing Pillow Image Processing")
    print("="*40)
    
    # Test 1: Create a test image
    print("1. Creating test image (3000x2000)...")
    img = Image.new('RGB', (3000, 2000), color='red')
    
    # Add some pattern
    for x in range(0, 3000, 100):
        for y in range(0, 2000, 100):
            img.paste((0, 255, 0), (x, y, x+50, y+50))
    
    # Save to buffer to simulate uploaded file
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=95)
    original_size = len(buffer.getvalue())
    print(f"   Original size: {original_size / (1024*1024):.2f}MB")
    
    # Test 2: Resize the image
    print("2. Resizing image to max 2048x2048...")
    buffer.seek(0)
    img = Image.open(buffer)
    
    # Get original dimensions
    original_width, original_height = img.size
    max_width, max_height = 2048, 2048
    
    # Calculate new dimensions maintaining aspect ratio
    ratio = min(max_width / original_width, max_height / original_height)
    
    if ratio < 1:
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        print(f"   Resized from {original_width}x{original_height} to {new_width}x{new_height}")
    
    # Test 3: Save resized image
    output_buffer = io.BytesIO()
    img.save(output_buffer, format='JPEG', quality=85, optimize=True)
    new_size = len(output_buffer.getvalue())
    print(f"   New size: {new_size / (1024*1024):.2f}MB")
    print(f"   Size reduction: {((original_size - new_size) / original_size * 100):.1f}%")
    
    # Test 4: Create thumbnail
    print("3. Creating thumbnail (400x400)...")
    output_buffer.seek(0)
    img = Image.open(output_buffer)
    img.thumbnail((400, 400), Image.Resampling.LANCZOS)
    
    thumb_buffer = io.BytesIO()
    img.save(thumb_buffer, format='JPEG', quality=80, optimize=True)
    thumb_size = len(thumb_buffer.getvalue())
    print(f"   Thumbnail size: {thumb_size / 1024:.1f}KB")
    
    print("\n" + "="*40)
    print("✅ All Pillow tests passed!")
    print("Your system is ready for image processing.")
    
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("Please install Pillow: pip install Pillow")
except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()
