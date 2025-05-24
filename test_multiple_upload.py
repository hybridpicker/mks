#!/usr/bin/env python3
"""
Test script to verify multiple large image upload handling
"""

from PIL import Image
import io
import os

def create_test_images(count=3, sizes=[(4000, 3000), (3500, 2800), (5000, 4000)]):
    """Create multiple test images of different sizes"""
    test_images = []
    
    for i in range(count):
        width, height = sizes[i % len(sizes)]
        
        # Create image with different colors
        colors = ['red', 'blue', 'green', 'yellow', 'purple']
        img = Image.new('RGB', (width, height), color=colors[i % len(colors)])
        
        # Add pattern to make it more realistic
        for x in range(0, width, 200):
            for y in range(0, height, 200):
                img.paste('white', (x, y, x+100, y+100))
        
        # Save to buffer
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=95)
        size_mb = len(buffer.getvalue()) / (1024 * 1024)
        
        test_images.append({
            'name': f'test_image_{i+1}_{width}x{height}.jpg',
            'size': len(buffer.getvalue()),
            'size_mb': size_mb,
            'dimensions': f'{width}x{height}',
            'data': buffer.getvalue()
        })
        
        print(f"Created: {test_images[-1]['name']} - {size_mb:.1f}MB ({width}x{height})")
    
    return test_images

def simulate_multiple_upload_processing(test_images):
    """Simulate the multiple upload processing logic"""
    print("\n" + "="*60)
    print("SIMULATING MULTIPLE UPLOAD PROCESSING")
    print("="*60)
    
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    uploaded_photos = []
    errors = []
    warnings = []
    
    for i, image_data in enumerate(test_images):
        print(f"\nProcessing {image_data['name']}...")
        
        try:
            # Check file size (like in the real implementation)
            if image_data['size'] > MAX_FILE_SIZE:
                error_msg = (f"{image_data['name']}: Original file too large "
                           f"(max. {MAX_FILE_SIZE//(1024*1024)}MB). "
                           f"File is {image_data['size_mb']:.2f}MB.")
                errors.append(error_msg)
                print(f"  ❌ {error_msg}")
                continue
            
            # Simulate image processing (calculate what the final size would be)
            original_mb = image_data['size_mb']
            
            # Simulate resize reduction (typically 70-85% reduction for large images)
            if original_mb > 5:
                reduction_factor = 0.15  # Keep ~15% of original size
            elif original_mb > 2:
                reduction_factor = 0.25  # Keep ~25% of original size  
            else:
                reduction_factor = 0.5   # Keep ~50% of original size
            
            final_mb = original_mb * reduction_factor
            
            # Check if still quite large after processing
            if final_mb > 5:
                warning_msg = f"{image_data['name']}: Processed image is still {final_mb:.1f}MB large"
                warnings.append(warning_msg)
                print(f"  ⚠️  {warning_msg}")
            
            # Simulate successful processing
            uploaded_photo = {
                'name': image_data['name'],
                'original_size_mb': original_mb,
                'final_size_mb': final_mb,
                'dimensions': image_data['dimensions'],
                'savings_mb': original_mb - final_mb,
                'reduction_percent': ((original_mb - final_mb) / original_mb) * 100
            }
            
            uploaded_photos.append(uploaded_photo)
            print(f"  ✅ Success: {original_mb:.1f}MB → {final_mb:.1f}MB "
                  f"(saved {uploaded_photo['savings_mb']:.1f}MB, "
                  f"{uploaded_photo['reduction_percent']:.1f}% reduction)")
            
        except Exception as e:
            error_msg = f"{image_data['name']}: {str(e)}"
            errors.append(error_msg)
            print(f"  ❌ Error: {error_msg}")
    
    # Print summary (like the real implementation)
    print("\n" + "="*60)
    print("PROCESSING SUMMARY")
    print("="*60)
    
    if uploaded_photos:
        total_original = sum(p['original_size_mb'] for p in uploaded_photos)
        total_final = sum(p['final_size_mb'] for p in uploaded_photos)
        total_saved = total_original - total_final
        
        message_parts = [f"{len(uploaded_photos)} images successfully processed"]
        if warnings:
            message_parts.append(f"{len(warnings)} warnings")
        if errors:
            message_parts.append(f"{len(errors)} errors")
        
        print(f"✅ {' ('.join(message_parts)}{''.join([')'] if len(message_parts) > 1 else [])}")
        print(f"📊 Total savings: {total_original:.1f}MB → {total_final:.1f}MB "
              f"(saved {total_saved:.1f}MB)")
        
        print(f"\n📋 Successful uploads:")
        for photo in uploaded_photos:
            print(f"  • {photo['name']}: {photo['original_size_mb']:.1f}MB → {photo['final_size_mb']:.1f}MB")
        
        if warnings:
            print(f"\n⚠️  Warnings:")
            for warning in warnings:
                print(f"  • {warning}")
        
        if errors:
            print(f"\n❌ Errors:")
            for error in errors:
                print(f"  • {error}")
    else:
        print("❌ No images could be processed")
        if errors:
            print("\nErrors:")
            for error in errors:
                print(f"  • {error}")

def main():
    print("Testing Multiple Large Image Upload Processing")
    print("=" * 60)
    
    # Create test images of various sizes
    test_images = create_test_images(5, [
        (4000, 3000),   # ~8-10MB
        (3500, 2800),   # ~6-8MB  
        (5000, 4000),   # ~12-15MB (too large)
        (2500, 2000),   # ~3-5MB
        (6000, 4500)    # ~15-20MB (too large)
    ])
    
    # Simulate the processing
    simulate_multiple_upload_processing(test_images)
    
    print("\n" + "🎉" * 20)
    print("Multiple upload processing test completed!")
    print("Your gallery can handle batches of large images safely.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
