#!/usr/bin/env python
"""
Gallery Formset Debug - Check if empty formset causes transaction rollback
"""

import os
import sys

project_root = '/Users/lukasschonsgibl/Coding/Django/mks'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from blog.forms import GalleryImageFormSet

def test_empty_gallery_formset():
    """Test empty gallery formset validation"""
    print("Testing empty gallery formset...")
    
    # Data that would come from an empty form
    empty_data = {
        'gallery_images-TOTAL_FORMS': '0',
        'gallery_images-INITIAL_FORMS': '0',
        'gallery_images-MIN_NUM_FORMS': '0',
        'gallery_images-MAX_NUM_FORMS': '10',
    }
    
    formset = GalleryImageFormSet(data=empty_data)
    
    print(f"Formset is valid: {formset.is_valid()}")
    print(f"Formset errors: {formset.errors}")
    print(f"Formset non-form errors: {formset.non_form_errors()}")
    
    return formset.is_valid()

def test_formset_with_extra_forms():
    """Test formset with extra empty forms"""
    print("\nTesting formset with extra empty forms...")
    
    # Data that would come from the browser with 3 extra empty forms
    data_with_extras = {
        'gallery_images-TOTAL_FORMS': '3',
        'gallery_images-INITIAL_FORMS': '0',
        'gallery_images-MIN_NUM_FORMS': '0',
        'gallery_images-MAX_NUM_FORMS': '10',
        
        # Empty form 0
        'gallery_images-0-image': '',
        'gallery_images-0-caption': '',
        'gallery_images-0-alt_text': '',
        'gallery_images-0-DELETE': '',
        
        # Empty form 1
        'gallery_images-1-image': '',
        'gallery_images-1-caption': '',
        'gallery_images-1-alt_text': '',
        'gallery_images-1-DELETE': '',
        
        # Empty form 2
        'gallery_images-2-image': '',
        'gallery_images-2-caption': '',
        'gallery_images-2-alt_text': '',
        'gallery_images-2-DELETE': '',
    }
    
    formset = GalleryImageFormSet(data=data_with_extras)
    
    print(f"Formset is valid: {formset.is_valid()}")
    print(f"Formset errors: {formset.errors}")
    print(f"Formset non-form errors: {formset.non_form_errors()}")
    
    if not formset.is_valid():
        print("Individual form errors:")
        for i, form in enumerate(formset.forms):
            if form.errors:
                print(f"  Form {i}: {form.errors}")
    
    return formset.is_valid()

def test_browser_like_data():
    """Test with data that looks like what browser would actually send"""
    print("\nTesting with browser-like data...")
    
    # This is what the browser actually sends
    browser_data = {
        'csrfmiddlewaretoken': 'dummy-token',
        'title': 'Test Blog Post',
        'content': '<p>Test content</p>',
        'lead_paragraph': 'Test lead',
        'meta_title': '',
        'meta_description': '',
        'slug': '',
        'image_alt_text': '',
        'category': '',
        'author': '',
        'published': 'off',  # Unchecked checkbox
        'save-draft': 'Save Draft',
        
        # Gallery formset management form
        'gallery_images-TOTAL_FORMS': '3',
        'gallery_images-INITIAL_FORMS': '0',
        'gallery_images-MIN_NUM_FORMS': '0',
        'gallery_images-MAX_NUM_FORMS': '10',
        
        # The browser sends these even for empty forms
        'gallery_images-0-caption': '',
        'gallery_images-0-alt_text': '',
        'gallery_images-1-caption': '',
        'gallery_images-1-alt_text': '',
        'gallery_images-2-caption': '',
        'gallery_images-2-alt_text': '',
    }
    
    # Filter out only gallery formset data
    gallery_data = {k: v for k, v in browser_data.items() if k.startswith('gallery_images-')}
    
    print("Gallery data being sent to formset:")
    for key, value in gallery_data.items():
        print(f"  {key}: '{value}'")
    
    formset = GalleryImageFormSet(data=gallery_data)
    
    print(f"\nFormset is valid: {formset.is_valid()}")
    print(f"Formset errors: {formset.errors}")
    print(f"Formset non-form errors: {formset.non_form_errors()}")
    
    if not formset.is_valid():
        print("\nDetailed form errors:")
        for i, form in enumerate(formset.forms):
            print(f"Form {i}:")
            print(f"  Has changed: {form.has_changed()}")
            print(f"  Errors: {form.errors}")
            print(f"  Cleaned data: {form.cleaned_data if form.is_bound and form.is_valid() else 'Invalid'}")
    
    return formset.is_valid()

def main():
    print("GALLERY FORMSET DEBUG")
    print("=" * 50)
    
    tests = [
        test_empty_gallery_formset,
        test_formset_with_extra_forms,
        test_browser_like_data,
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print("=" * 50)
    
    all_passed = all(results)
    
    for i, result in enumerate(results, 1):
        status = "PASS" if result else "FAIL"
        print(f"Test {i}: {status}")
    
    if all_passed:
        print("\n✅ All formset tests passed!")
        print("Gallery formset is not the issue.")
    else:
        print("\n❌ Some formset tests failed!")
        print("Gallery formset validation errors might be causing the transaction rollback.")
        
        print("\nSuggested fixes:")
        print("1. Make gallery formset non-blocking (save main post even if gallery fails)")
        print("2. Fix formset validation to handle empty forms correctly")
        print("3. Add better error handling in the view")

if __name__ == "__main__":
    main()
