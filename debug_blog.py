#!/usr/bin/env python
"""
Blog Debug Script - Führe dieses Script aus, um Blog-Probleme zu diagnostizieren
"""

import os
import sys
import django

# Add the project root to the Python path
project_root = '/Users/lukasschonsgibl/Coding/Django/mks'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from django.db import connection
from django.core.exceptions import ValidationError
from blog.models import BlogPost, GalleryImage, Author
from blog.forms import ArticleForm, GalleryImageFormSet
from teaching.subject import Subject
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_connection():
    """Test database connection"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            logger.info("✓ Database connection successful")
            return True
    except Exception as e:
        logger.error(f"✗ Database connection failed: {e}")
        return False

def test_blog_model():
    """Test blog model operations"""
    try:
        # Test creating a blog post
        test_post = BlogPost(
            title="Test Blog Post",
            content="<p>Test content that is longer than 10 characters</p>",
            lead_paragraph="Test lead paragraph",
        )
        test_post.full_clean()  # Validate without saving
        logger.info("✓ Blog model validation successful")
        return True
    except ValidationError as e:
        logger.error(f"✗ Blog model validation failed: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ Blog model test failed: {e}")
        return False

def test_slug_generation():
    """Test slug generation"""
    try:
        from blog.views import create_slug_text
        
        test_cases = [
            "Test Blog Post",
            "Äöü ßß Test",
            "Special!@#$%^&*()Characters",
            "",
            "   ",
        ]
        
        for title in test_cases:
            slug = create_slug_text(title)
            logger.info(f"'{title}' -> '{slug}'")
            
        logger.info("✓ Slug generation test successful")
        return True
    except Exception as e:
        logger.error(f"✗ Slug generation test failed: {e}")
        return False

def test_form_validation():
    """Test form validation"""
    try:
        # Test valid form data
        valid_data = {
            'title': 'Test Blog Post',
            'content': '<p>This is test content that is long enough.</p>',
            'lead_paragraph': 'This is a lead paragraph',
            'published': False
        }
        
        form = ArticleForm(data=valid_data)
        if form.is_valid():
            logger.info("✓ Form validation test successful")
            return True
        else:
            logger.error(f"✗ Form validation failed: {form.errors}")
            return False
            
    except Exception as e:
        logger.error(f"✗ Form validation test failed: {e}")
        return False

def test_existing_slugs():
    """Check for duplicate slugs in database"""
    try:
        slugs = BlogPost.objects.values_list('slug', flat=True)
        slug_counts = {}
        
        for slug in slugs:
            slug_counts[slug] = slug_counts.get(slug, 0) + 1
        
        duplicates = {slug: count for slug, count in slug_counts.items() if count > 1}
        
        if duplicates:
            logger.warning(f"⚠ Found duplicate slugs: {duplicates}")
        else:
            logger.info("✓ No duplicate slugs found")
            
        return len(duplicates) == 0
        
    except Exception as e:
        logger.error(f"✗ Slug check failed: {e}")
        return False

def check_media_directory():
    """Check media directory permissions"""
    try:
        from django.conf import settings
        media_root = settings.MEDIA_ROOT
        blog_media_dir = os.path.join(media_root, 'blog', 'posts', 'images')
        
        # Check if directory exists
        if not os.path.exists(blog_media_dir):
            os.makedirs(blog_media_dir, exist_ok=True)
            logger.info(f"✓ Created media directory: {blog_media_dir}")
        else:
            logger.info(f"✓ Media directory exists: {blog_media_dir}")
        
        # Check permissions
        if os.access(blog_media_dir, os.W_OK):
            logger.info("✓ Media directory is writable")
            return True
        else:
            logger.error("✗ Media directory is not writable")
            return False
            
    except Exception as e:
        logger.error(f"✗ Media directory check failed: {e}")
        return False

def check_dependencies():
    """Check required dependencies"""
    try:
        dependencies = [
            'tinymce',
            'sorl.thumbnail',
            'slugify',
        ]
        
        for dep in dependencies:
            try:
                __import__(dep)
                logger.info(f"✓ {dep} is available")
            except ImportError:
                logger.error(f"✗ {dep} is not available")
                return False
                
        return True
        
    except Exception as e:
        logger.error(f"✗ Dependency check failed: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    logger.info("Starting blog diagnostic tests...")
    logger.info("=" * 50)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Blog Model", test_blog_model),
        ("Slug Generation", test_slug_generation),
        ("Form Validation", test_form_validation),
        ("Existing Slugs", test_existing_slugs),
        ("Media Directory", check_media_directory),
        ("Dependencies", check_dependencies),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\nRunning {test_name} test...")
        result = test_func()
        results.append((test_name, result))
    
    logger.info("\n" + "=" * 50)
    logger.info("DIAGNOSTIC RESULTS:")
    logger.info("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        logger.info(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        logger.info("\n✓ All tests passed! Blog should work correctly.")
    else:
        logger.info("\n✗ Some tests failed. Please address the issues above.")
    
    return all_passed

if __name__ == "__main__":
    main()
