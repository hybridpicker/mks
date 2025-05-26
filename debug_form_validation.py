#!/usr/bin/env python
"""
Test Form Validation Edge Cases
"""

import os
import sys

project_root = '/Users/lukasschonsgibl/Coding/Django/mks'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from blog.forms import ArticleForm
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

def create_test_image():
    """Create a small test image"""
    img = Image.new('RGB', (50, 50), color='red')
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    return SimpleUploadedFile(
        name='test.jpg',
        content=img_io.getvalue(),
        content_type='image/jpeg'
    )

def test_minimal_valid_form():
    """Test with minimal valid data"""
    print("Testing minimal valid form...")
    
    form_data = {
        'title': 'Test Blog Post',
        'content': '<p>This is test content that is long enough.</p>',
    }
    
    files_data = {
        'image': create_test_image()
    }
    
    form = ArticleForm(data=form_data, files=files_data)
    
    print(f"Form is valid: {form.is_valid()}")
    if not form.is_valid():
        print(f"Form errors: {form.errors}")
        return False
    
    print("Cleaned data:")
    for key, value in form.cleaned_data.items():
        if key == 'image':
            print(f"  {key}: FILE ({value.name if value else 'None'})")
        else:
            print(f"  {key}: {repr(value)}")
    
    return True

def test_empty_meta_fields():
    """Test with empty meta fields (should auto-generate)"""
    print("\nTesting with empty meta fields...")
    
    form_data = {
        'title': 'Test Blog Post With Empty Meta',
        'content': '<p>This is test content.</p>',
        'lead_paragraph': 'This is a lead paragraph',
        'meta_title': '',  # Empty
        'meta_description': '',  # Empty
        'slug': '',  # Empty
    }
    
    form = ArticleForm(data=form_data)
    
    print(f"Form is valid: {form.is_valid()}")
    if not form.is_valid():
        print(f"Form errors: {form.errors}")
        return False
    
    # Check auto-generated fields
    print("Auto-generated fields:")
    print(f"  meta_title: {repr(form.cleaned_data.get('meta_title'))}")
    print(f"  meta_description: {repr(form.cleaned_data.get('meta_description'))}")
    print(f"  slug: {repr(form.cleaned_data.get('slug'))}")
    
    return True

def test_missing_required_fields():
    """Test with missing required fields"""
    print("\nTesting with missing required fields...")
    
    test_cases = [
        ({}, "No data at all"),
        ({'title': ''}, "Empty title"),
        ({'title': 'Test', 'content': ''}, "Empty content"),
        ({'title': 'Test', 'content': '<p>Short</p>'}, "Too short content"),
        ({'title': 'A' * 150, 'content': '<p>Valid content</p>'}, "Title too long"),
    ]
    
    all_failed_as_expected = True
    
    for form_data, description in test_cases:
        print(f"\n  Testing: {description}")
        form = ArticleForm(data=form_data)
        is_valid = form.is_valid()
        
        print(f"    Valid: {is_valid}")
        if not is_valid:
            print(f"    Errors: {form.errors}")
        else:
            print("    ⚠️  This should have failed!")
            all_failed_as_expected = False
    
    return all_failed_as_expected

def test_tinymce_content_variations():
    """Test different TinyMCE content formats"""
    print("\nTesting TinyMCE content variations...")
    
    content_tests = [
        ('<p>Simple paragraph</p>', "Simple HTML"),
        ('<p>First paragraph</p><p>Second paragraph</p>', "Multiple paragraphs"),
        ('<p><strong>Bold</strong> and <em>italic</em> text</p>', "Formatted text"),
        ('<p>Text with <a href="http://example.com">link</a></p>', "With links"),
        ('Plain text without HTML tags', "Plain text"),
        ('', "Empty content"),
        ('   ', "Whitespace only"),
        ('<p></p>', "Empty HTML paragraph"),
    ]
    
    for content, description in content_tests:
        print(f"\n  Testing: {description}")
        
        form_data = {
            'title': f'Test - {description}',
            'content': content,
        }
        
        form = ArticleForm(data=form_data)
        is_valid = form.is_valid()
        
        print(f"    Content: {repr(content[:50])}")
        print(f"    Valid: {is_valid}")
        
        if not is_valid and 'content' in form.errors:
            print(f"    Content error: {form.errors['content']}")

def test_browser_checkbox_behavior():
    """Test how browser checkboxes work"""
    print("\nTesting browser checkbox behavior...")
    
    # Test cases for how browsers send checkbox data
    checkbox_tests = [
        ({'published': 'on'}, "Checked checkbox"),
        ({}, "Unchecked checkbox (no field sent)"),
        ({'published': ''}, "Unchecked checkbox (empty value)"),
        ({'published': 'false'}, "JavaScript false value"),
    ]
    
    for form_data, description in checkbox_tests:
        print(f"\n  Testing: {description}")
        
        complete_data = {
            'title': 'Checkbox Test',
            'content': '<p>Testing checkbox behavior</p>',
            **form_data
        }
        
        form = ArticleForm(data=complete_data)
        is_valid = form.is_valid()
        
        print(f"    Data: {form_data}")
        print(f"    Valid: {is_valid}")
        
        if is_valid:
            published_value = form.cleaned_data.get('published')
            print(f"    Published value: {published_value} (type: {type(published_value)})")

def main():
    print("FORM VALIDATION EDGE CASES DEBUG")
    print("=" * 50)
    
    tests = [
        ("Minimal Valid Form", test_minimal_valid_form),
        ("Empty Meta Fields", test_empty_meta_fields),  
        ("Missing Required Fields", test_missing_required_fields),
        ("TinyMCE Content Variations", lambda: (test_tinymce_content_variations(), True)[1]),
        ("Browser Checkbox Behavior", lambda: (test_browser_checkbox_behavior(), True)[1]),
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            test_func()
        except Exception as e:
            print(f"Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print("DEBUG COMPLETE")
    print("\nIf forms are validating correctly, the issue might be:")
    print("1. Transaction rollback due to database constraints")
    print("2. Redirect happening before commit")
    print("3. Exception in view logic after form.save()")
    print("4. Frontend JavaScript preventing form submission")
    
    print("\nNext steps:")
    print("1. Check Django logs during actual browser form submission")  
    print("2. Check browser Network tab for actual POST data")
    print("3. Add more detailed logging to views")

if __name__ == "__main__":
    main()
