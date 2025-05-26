#!/usr/bin/env python
"""
Final Blog Test - Test the actual blog creation functionality
"""

import os
import sys

project_root = '/Users/lukasschonsgibl/Coding/Django/mks'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from blog.models import BlogPost
from blog.forms import ArticleForm
from django.db import transaction

def test_blog_creation():
    """Test creating a blog post"""
    print("Testing blog post creation...")
    
    # Test data
    test_data = {
        'title': 'Test Blog Post für Fix',
        'content': '<p>Dies ist ein Testinhalt für den Blog-Fix. Dieser Text ist lang genug um die Validierung zu bestehen.</p>',
        'lead_paragraph': 'Dies ist ein Test-Lead-Paragraph für den Blog-Fix.',
        'published': False
    }
    
    try:
        # Test form validation
        form = ArticleForm(data=test_data)
        if form.is_valid():
            print("✓ Form validation passed")
            
            # Test saving
            with transaction.atomic():
                blog_post = form.save()
                print(f"✓ Blog post created successfully with ID: {blog_post.id}")
                print(f"  - Title: {blog_post.title}")
                print(f"  - Slug: {blog_post.slug}")
                print(f"  - Meta Title: {blog_post.meta_title}")
                print(f"  - Meta Description: {blog_post.meta_description[:50]}...")
                
                # Clean up - delete test post
                blog_post.delete()
                print("✓ Test post cleaned up")
                
            return True
        else:
            print(f"✗ Form validation failed: {form.errors}")
            return False
            
    except Exception as e:
        print(f"✗ Blog creation test failed: {e}")
        return False

def test_edge_cases():
    """Test edge cases that previously caused issues"""
    print("\nTesting edge cases...")
    
    edge_cases = [
        {
            'title': 'Äöü ßß Spezialzeichen Test',
            'content': '<p>Test mit deutschen Sonderzeichen.</p>',
            'lead_paragraph': 'Test mit Umlauten und ß',
        },
        {
            'title': 'A' * 120,  # Max length title
            'content': '<p>' + 'X' * 500 + '</p>',  # Long content
            'lead_paragraph': 'Y' * 200,  # Long lead paragraph
        },
        {
            'title': 'Duplicate Test',  # We'll create this twice to test uniqueness
            'content': '<p>Testing duplicate handling.</p>',
            'lead_paragraph': 'Duplicate test',
        }
    ]
    
    created_posts = []
    
    for i, test_case in enumerate(edge_cases):
        try:
            form = ArticleForm(data=test_case)
            if form.is_valid():
                blog_post = form.save()
                created_posts.append(blog_post)
                print(f"✓ Edge case {i+1} passed: '{blog_post.title[:30]}...' -> '{blog_post.slug}'")
            else:
                print(f"✗ Edge case {i+1} failed: {form.errors}")
                
        except Exception as e:
            print(f"✗ Edge case {i+1} exception: {e}")
    
    # Test duplicate handling by creating the same title again
    try:
        duplicate_data = {
            'title': 'Duplicate Test',
            'content': '<p>Another duplicate test.</p>',
            'lead_paragraph': 'Another duplicate',
        }
        form = ArticleForm(data=duplicate_data)
        if form.is_valid():
            blog_post = form.save()
            created_posts.append(blog_post)
            print(f"✓ Duplicate handling test passed: slug = '{blog_post.slug}'")
        else:
            print(f"✗ Duplicate handling failed: {form.errors}")
    except Exception as e:
        print(f"✗ Duplicate handling exception: {e}")
    
    # Clean up test posts
    for post in created_posts:
        try:
            post.delete()
        except:
            pass
    
    if created_posts:
        print(f"✓ Cleaned up {len(created_posts)} test posts")

def main():
    print("FINAL BLOG FUNCTIONALITY TEST")
    print("=" * 40)
    
    # Test basic creation
    creation_success = test_blog_creation()
    
    # Test edge cases
    test_edge_cases()
    
    print("\n" + "=" * 40)
    if creation_success:
        print("✓ BLOG FIX SUCCESSFUL!")
        print("Your blog should now work correctly.")
        print("\nNext steps:")
        print("1. Go to /blogedit/new")
        print("2. Create a new blog post")
        print("3. Try both 'Save Draft' and 'Save & Publish'")
    else:
        print("✗ BLOG FIX INCOMPLETE")
        print("There are still issues that need to be resolved.")

if __name__ == "__main__":
    main()
