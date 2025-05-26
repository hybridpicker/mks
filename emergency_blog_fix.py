#!/usr/bin/env python
"""
EMERGENCY BLOG FIX - Quick fix for immediate blog problems
"""

import os
import sys

# Add the project root to the Python path
project_root = '/Users/lukasschonsgibl/Coding/Django/mks'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from django.db import transaction
from blog.models import BlogPost
from django.utils.text import slugify
import uuid

def fix_empty_meta_fields():
    """Fix posts with empty meta fields"""
    print("Fixing empty meta fields...")
    
    posts_fixed = 0
    for post in BlogPost.objects.all():
        needs_save = False
        
        if not post.meta_title:
            post.meta_title = post.title[:60] if post.title else f"Blog Post {post.pk}"
            needs_save = True
            
        if not post.meta_description:
            if post.lead_paragraph:
                post.meta_description = post.lead_paragraph[:160]
            else:
                post.meta_description = f"Blog post about {post.title}"[:160] 
            needs_save = True
            
        if needs_save:
            post.save(update_fields=['meta_title', 'meta_description'])
            posts_fixed += 1
            print(f"Fixed meta fields for: {post.title}")
    
    print(f"Fixed {posts_fixed} posts")

def fix_empty_slugs():
    """Fix posts with empty slugs"""
    print("Fixing empty slugs...")
    
    posts_fixed = 0
    for post in BlogPost.objects.filter(slug__isnull=True):
        if post.title:
            base_slug = slugify(post.title)
        else:
            base_slug = f"blog-post-{post.pk}"
            
        if not base_slug:
            base_slug = f"blog-post-{uuid.uuid4().hex[:8]}"
            
        # Make sure slug is unique
        slug = base_slug
        counter = 1
        while BlogPost.objects.filter(slug=slug).exclude(pk=post.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        post.slug = slug
        post.save(update_fields=['slug'])
        posts_fixed += 1
        print(f"Fixed slug for: {post.title} -> {slug}")
    
    print(f"Fixed {posts_fixed} posts")

def main():
    print("EMERGENCY BLOG FIX")
    print("=" * 30)
    
    try:
        with transaction.atomic():
            fix_empty_meta_fields()
            fix_empty_slugs()
            
        print("\n✓ Emergency fixes completed successfully!")
        print("Try creating a new blog post now.")
        
    except Exception as e:
        print(f"\n✗ Emergency fix failed: {e}")
        print("Please check the error and try the full diagnostic script.")

if __name__ == "__main__":
    main()
