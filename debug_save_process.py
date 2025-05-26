#!/usr/bin/env python
"""
Blog Post Save Debug - Check what's happening during save
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
from django.db import connection

def check_database_posts():
    """Check what posts are actually in the database"""
    print("Checking database for blog posts...")
    
    posts = BlogPost.objects.all().order_by('-id')[:10]
    
    print(f"Total blog posts in database: {BlogPost.objects.count()}")
    print("\nLast 10 posts:")
    
    for post in posts:
        print(f"ID: {post.id}")
        print(f"  Title: {post.title}")
        print(f"  Slug: {post.slug}")
        print(f"  Published: {post.published}")
        print(f"  Created: {post.created_at}")
        print(f"  Image: {post.image.name if post.image else 'None'}")
        print(f"  Meta Title: {post.meta_title}")
        print(f"  Meta Description: {post.meta_description[:50]}..." if post.meta_description else "None")
        print()

def check_database_connection():
    """Check database connection and recent queries"""
    print("Checking database connection...")
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM blog_blogpost")
        count = cursor.fetchone()[0]
        print(f"Blog posts count via raw SQL: {count}")
        
        # Check recent inserts
        cursor.execute("""
            SELECT id, title, slug, published, created_at 
            FROM blog_blogpost 
            ORDER BY id DESC 
            LIMIT 5
        """)
        
        rows = cursor.fetchall()
        print("\nRecent posts via raw SQL:")
        for row in rows:
            print(f"  ID: {row[0]}, Title: {row[1]}, Slug: {row[2]}, Published: {row[3]}, Created: {row[4]}")

def simulate_exact_save_process():
    """Simulate the exact save process from the view"""
    print("\nSimulating exact save process...")
    
    from django.core.files.uploadedfile import SimpleUploadedFile
    from blog.forms import ArticleForm, GalleryImageFormSet
    from blog.views import create_slug_text
    from django.db import transaction
    from PIL import Image
    import io
    
    # Create test image
    img = Image.new('RGB', (100, 100), color='green')
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    
    test_image = SimpleUploadedFile(
        name='debug_test.jpg',
        content=img_io.getvalue(),
        content_type='image/jpeg'
    )
    
    # Simulate form data
    form_data = {
        'title': 'Debug Test Blog Post',
        'content': '<p>This is a debug test to see what happens during save.</p>',
        'lead_paragraph': 'Debug test lead paragraph',
        'published': False,
    }
    
    files_data = {
        'image': test_image
    }
    
    # Gallery formset data (empty)
    gallery_data = {
        'gallery_images-TOTAL_FORMS': '0',
        'gallery_images-INITIAL_FORMS': '0',
        'gallery_images-MIN_NUM_FORMS': '0',
        'gallery_images-MAX_NUM_FORMS': '10',
    }
    
    print("Creating forms...")
    form = ArticleForm(data=form_data, files=files_data)
    gallery_formset = GalleryImageFormSet(data=gallery_data)
    
    print(f"Form is valid: {form.is_valid()}")
    if not form.is_valid():
        print(f"Form errors: {form.errors}")
        return False
    
    print(f"Gallery formset is valid: {gallery_formset.is_valid()}")
    if not gallery_formset.is_valid():
        print(f"Gallery formset errors: {gallery_formset.errors}")
        print(f"Gallery formset non-form errors: {gallery_formset.non_form_errors()}")
    
    print("Attempting to save...")
    
    try:
        with transaction.atomic():
            print("  Inside transaction...")
            
            blog_post = form.save(commit=False)
            print(f"  Form saved (commit=False): {blog_post}")
            print(f"  Blog post title: {blog_post.title}")
            print(f"  Blog post has image: {bool(blog_post.image)}")
            
            # Apply view logic
            if not blog_post.slug:
                blog_post.slug = create_slug_text(blog_post.title)
                print(f"  Generated slug: {blog_post.slug}")
            
            if not blog_post.meta_title:
                blog_post.meta_title = blog_post.title[:60]
                print(f"  Generated meta_title: {blog_post.meta_title}")
            
            if not blog_post.meta_description and blog_post.lead_paragraph:
                blog_post.meta_description = blog_post.lead_paragraph[:160]
                print(f"  Generated meta_description: {blog_post.meta_description}")
            
            print("  About to save blog_post...")
            blog_post.save()
            print(f"  ✓ Blog post saved with ID: {blog_post.id}")
            
            # Check if it's actually in the database
            saved_post = BlogPost.objects.get(id=blog_post.id)
            print(f"  ✓ Verified in database: {saved_post.title}")
            
            # Process gallery formset
            if gallery_formset.is_valid():
                gallery_formset.instance = blog_post
                gallery_formset.save()
                print("  ✓ Gallery formset saved")
            
            print("  Transaction completed successfully")
            
            return blog_post.id
            
    except Exception as e:
        print(f"  ✗ Error during save: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_transaction_isolation():
    """Check if there are transaction isolation issues"""
    print("\nChecking transaction isolation...")
    
    from django.db import transaction
    
    # Check current transaction state
    print(f"In atomic block: {transaction.get_connection().in_atomic_block}")
    print(f"Autocommit: {transaction.get_autocommit()}")
    
    # Check if there are any pending transactions
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM pg_stat_activity WHERE state = 'active'")
        active_connections = cursor.fetchone()[0]
        print(f"Active database connections: {active_connections}")

def main():
    print("BLOG POST SAVE DEBUG")
    print("=" * 50)
    
    print("1. Checking existing posts in database...")
    check_database_posts()
    
    print("\n2. Checking database connection...")
    check_database_connection()
    
    print("\n3. Checking transaction state...")
    check_transaction_isolation()
    
    print("\n4. Simulating save process...")
    result = simulate_exact_save_process()
    
    if result:
        print(f"\n✅ SUCCESS! Blog post created with ID: {result}")
        
        # Check if it's still there
        print("\n5. Verifying post exists after save...")
        try:
            post = BlogPost.objects.get(id=result)
            print(f"✓ Post still exists: {post.title}")
            
            # Clean up
            post.delete()
            print("✓ Test post cleaned up")
            
        except BlogPost.DoesNotExist:
            print("✗ Post disappeared after transaction!")
            
    else:
        print("\n❌ FAILED! Could not save blog post")
    
    print("\n6. Final database check...")
    check_database_posts()

if __name__ == "__main__":
    main()
