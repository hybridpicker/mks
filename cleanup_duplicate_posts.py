#!/usr/bin/env python3
"""
Script zum Entfernen von duplizierten Blog-Posts
"""

import os
import django
from django.conf import settings
from django.db.models import Count

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from blog.models import BlogPost

def remove_duplicate_posts():
    """Entfernt doppelte Blog-Posts basierend auf Titel und Slug"""
    
    print("🔍 Suche nach duplizierten Blog-Posts...")
    
    # Finde Posts mit gleichem Titel
    duplicates_by_title = BlogPost.objects.values('title').annotate(
        count=Count('id')
    ).filter(count__gt=1)
    
    # Find Posts mit gleichem Slug
    duplicates_by_slug = BlogPost.objects.values('slug').annotate(
        count=Count('id')
    ).filter(count__gt=1)
    
    print(f"📊 Gefunden:")
    print(f"   - {len(duplicates_by_title)} Titel mit Duplikaten")
    print(f"   - {len(duplicates_by_slug)} Slugs mit Duplikaten")
    
    removed_count = 0
    
    # Handle title duplicates
    for duplicate in duplicates_by_title:
        title = duplicate['title']
        posts = BlogPost.objects.filter(title=title).order_by('created_at')
        
        print(f"\n🔧 Verarbeite '{title}' ({posts.count()} Duplikate)")
        
        # Keep the first (oldest) post, remove the rest
        posts_to_keep = posts.first()
        posts_to_remove = posts.exclude(id=posts_to_keep.id)
        
        print(f"   ✅ Behalte: #{posts_to_keep.id} (erstellt: {posts_to_keep.created_at})")
        
        for post in posts_to_remove:
            print(f"   🗑️  Lösche: #{post.id} (erstellt: {post.created_at})")
            post.delete()
            removed_count += 1
    
    # Handle slug duplicates (in case there are any remaining)
    for duplicate in duplicates_by_slug:
        slug = duplicate['slug']
        posts = BlogPost.objects.filter(slug=slug).order_by('created_at')
        
        if posts.count() > 1:  # Still duplicates after title cleanup
            print(f"\n🔧 Verarbeite Slug-Duplikate '{slug}' ({posts.count()} Posts)")
            
            posts_to_keep = posts.first()
            posts_to_remove = posts.exclude(id=posts_to_keep.id)
            
            print(f"   ✅ Behalte: #{posts_to_keep.id}")
            
            for post in posts_to_remove:
                print(f"   🗑️  Lösche: #{post.id}")
                post.delete()
                removed_count += 1
    
    print(f"\n🎉 Cleanup abgeschlossen!")
    print(f"   Entfernte Duplikate: {removed_count}")
    print(f"   Verbleibende Posts: {BlogPost.objects.count()}")

def show_post_statistics():
    """Zeigt Blog-Post Statistiken"""
    print("\n📈 Blog-Post Statistiken:")
    total_posts = BlogPost.objects.count()
    published_posts = BlogPost.objects.filter(published=True).count()
    with_images = BlogPost.objects.filter(image__isnull=False).exclude(image='').count()
    
    print(f"   Total Posts: {total_posts}")
    print(f"   Veröffentlicht: {published_posts}")
    print(f"   Mit Bildern: {with_images}")
    
    # Show recent posts
    recent_posts = BlogPost.objects.order_by('-created_at')[:5]
    print(f"\n📝 Letzte 5 Posts:")
    for i, post in enumerate(recent_posts, 1):
        status = "✅" if post.published else "📝"
        print(f"   {i}. {status} {post.title} (ID: {post.id})")

if __name__ == "__main__":
    print("🧹 Blog-Post Duplikat-Cleanup gestartet...\n")
    show_post_statistics()
    
    response = input("\n❓ Duplikate wirklich entfernen? (y/N): ")
    if response.lower() in ['y', 'yes', 'ja', 'j']:
        remove_duplicate_posts()
        show_post_statistics()
    else:
        print("❌ Abgebrochen - keine Änderungen vorgenommen")
