#!/usr/bin/env python
"""
Direct Form Test for Blog Image Upload
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

from django.core.files.uploadedfile import SimpleUploadedFile
from blog.forms import ArticleForm, GalleryImageFormSet
from blog.models import BlogPost

def create_test_image(width=800, height=600):
    """Create a test image"""
    img = Image.new('RGB', (width, height), color='red')
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    return img_io.getvalue()

def test_form_with_large_image():
    """Test form with different image sizes"""
    print("Testing form with different image sizes...")
    
    test_cases = [
        (800, 600, "Medium image"),
        (1920, 1080, "Large image"),
        (3000, 2000, "Very large image"),
        (5000, 3000, "Huge image"),
    ]
    
    for width, height, description in test_cases:
        print(f"\nTesting {description} ({width}x{height})...")
        
        # Create test image
        image_data = create_test_image(width, height)
        file_size_mb = len(image_data) / (1024 * 1024)
        print(f"  Image size: {file_size_mb:.2f} MB")
        
        test_image = SimpleUploadedFile(
            name=f'test_{width}x{height}.jpg',
            content=image_data,
            content_type='image/jpeg'
        )
        
        # Test form
        form_data = {
            'title': f'Test {description}',
            'content': f'<p>Testing with {description} of size {width}x{height}</p>',
            'lead_paragraph': f'Lead paragraph for {description}',
        }
        
        files_data = {
            'image': test_image
        }
        
        form = ArticleForm(data=form_data, files=files_data)
        
        print(f"  Form valid: {form.is_valid()}")
        
        if not form.is_valid():
            print(f"  Form errors: {form.errors}")
            continue
        
        # Try to save
        try:
            blog_post = form.save()
            print(f"  ✓ Saved successfully: ID {blog_post.id}")
            
            if blog_post.image:
                print(f"  ✓ Image saved: {blog_post.image.name}")
                print(f"  ✓ Image URL: {blog_post.image.url}")
                
                # Check if file actually exists
                if os.path.exists(blog_post.image.path):
                    actual_size = os.path.getsize(blog_post.image.path)
                    print(f"  ✓ File exists on disk: {actual_size / (1024*1024):.2f} MB")
                else:
                    print(f"  ✗ File NOT found on disk: {blog_post.image.path}")
            else:
                print(f"  ✗ No image attached to blog post")
            
            # Cleanup
            blog_post.delete()
            
        except Exception as e:
            print(f"  ✗ Save failed: {e}")
            import traceback
            traceback.print_exc()

def test_actual_post_data():
    """Simulate actual POST data from browser"""
    print("\n" + "="*50)
    print("Testing with realistic browser POST data...")
    
    # Create a realistic test image
    image_data = create_test_image(1200, 800)
    test_image = SimpleUploadedFile(
        name='blog_featured_image.jpg',
        content=image_data,
        content_type='image/jpeg'
    )
    
    # Realistic form data (similar to what browser would send)
    form_data = {
        'title': 'My New Blog Post with Image',
        'content': '''<p>This is a comprehensive blog post with rich content.</p>
                     <p>It includes multiple paragraphs and <strong>formatting</strong>.</p>
                     <p>This should work perfectly with our new form validation.</p>''',
        'lead_paragraph': 'This is an engaging lead paragraph that will appear in previews.',
        'meta_title': 'My New Blog Post - SEO Optimized Title',
        'meta_description': 'This is a meta description for search engines that describes the blog post content.',
        'published': False,  # Draft
        'category': '',  # No category selected
        'author': '',    # No author selected
        'slug': '',      # Auto-generate
        'image_alt_text': 'Featured image for my blog post',
    }
    
    files_data = {
        'image': test_image
    }
    
    # Test ArticleForm
    print("Testing ArticleForm...")
    form = ArticleForm(data=form_data, files=files_data)
    
    print(f"Form is valid: {form.is_valid()}")
    
    if not form.is_valid():
        print("Form errors:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
        return False
    
    # Test GalleryImageFormSet (empty)
    print("Testing empty GalleryImageFormSet...")
    
    gallery_data = {
        'gallery_images-TOTAL_FORMS': '0',
        'gallery_images-INITIAL_FORMS': '0',
        'gallery_images-MIN_NUM_FORMS': '0',
        'gallery_images-MAX_NUM_FORMS': '10',
    }
    
    gallery_formset = GalleryImageFormSet(data=gallery_data)
    print(f"Gallery formset is valid: {gallery_formset.is_valid()}")
    
    if not gallery_formset.is_valid():
        print("Gallery formset errors:")
        print(f"  {gallery_formset.errors}")
        print(f"  Non-form errors: {gallery_formset.non_form_errors()}")
    
    # Try to save everything
    print("Attempting to save...")
    
    try:
        blog_post = form.save(commit=False)
        
        # Apply the same logic as in the view
        if not blog_post.slug:
            from blog.views import create_slug_text
            blog_post.slug = create_slug_text(blog_post.title)
        
        if not blog_post.meta_title:
            blog_post.meta_title = blog_post.title[:60]
            
        if not blog_post.meta_description:
            blog_post.meta_description = blog_post.lead_paragraph[:160]
        
        blog_post.save()
        
        print(f"✓ Blog post saved: ID {blog_post.id}")
        print(f"  Title: {blog_post.title}")
        print(f"  Slug: {blog_post.slug}")
        print(f"  Published: {blog_post.published}")
        
        if blog_post.image:
            print(f"  ✓ Image saved: {blog_post.image.name}")
            print(f"  ✓ Image URL: {blog_post.image.url}")
            print(f"  ✓ Alt text: {blog_post.image_alt_text}")
        else:
            print("  ✗ No image was saved!")
        
        # Save gallery formset
        if gallery_formset.is_valid():
            gallery_formset.instance = blog_post
            gallery_formset.save()
            print("  ✓ Gallery formset saved")
        
        # Cleanup
        blog_post.delete()
        print("  ✓ Test post cleaned up")
        
        return True
        
    except Exception as e:
        print(f"✗ Save failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("COMPREHENSIVE IMAGE UPLOAD TEST")
    print("=" * 50)
    
    try:
        # Test with different image sizes
        test_form_with_large_image()
        
        # Test with realistic data
        success = test_actual_post_data()
        
        if success:
            print("\n✅ ALL TESTS PASSED!")
            print("Image upload functionality is working correctly.")
            print("\nIf you're still experiencing issues in the browser:")
            print("1. Check browser console for JavaScript errors")
            print("2. Check Django logs: tail -f logs/django.log")
            print("3. Check server response in browser dev tools")
            print("4. Try with different image formats/sizes")
        else:
            print("\n❌ TESTS FAILED!")
            print("There are issues with the form validation or saving process.")
            
    except Exception as e:
        print(f"\n❌ TEST FAILED WITH EXCEPTION: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
