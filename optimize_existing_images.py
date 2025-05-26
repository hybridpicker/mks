#!/usr/bin/env python3
"""
Script zur Optimierung bestehender Blog-Banner-Bilder
Führt die neue Bildoptimierung für alle existierenden Blog-Posts aus.
"""

import os
import django
from django.conf import settings

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from blog.models import BlogPost
from PIL import Image

def optimize_existing_images():
    """Optimiert alle bestehenden Blog-Banner-Bilder"""
    posts_with_images = BlogPost.objects.filter(image__isnull=False).exclude(image='')
    
    print(f"📸 Gefunden: {posts_with_images.count()} Blog-Posts mit Bildern")
    
    for i, post in enumerate(posts_with_images, 1):
        print(f"\n🔄 [{i}/{posts_with_images.count()}] Optimiere: {post.title}")
        
        try:
            if post.image and hasattr(post.image, 'path'):
                # Bildinfos vor Optimierung
                with Image.open(post.image.path) as img:
                    old_width, old_height = img.size
                    old_ratio = old_width / old_height if old_height > 0 else 1
                
                print(f"   📏 Original: {old_width}x{old_height} (ratio: {old_ratio:.2f})")
                
                # Optimierung ausführen
                post.optimize_banner_image()
                
                # Neue Info anzeigen
                if post.image_width and post.image_height:
                    new_ratio = post.image_width / post.image_height
                    print(f"   ✅ Optimiert: {post.image_width}x{post.image_height} (ratio: {new_ratio:.2f})")
                    
                    # Focus-Point setzen wenn nicht vorhanden
                    if post.image_focus_x is None or post.image_focus_y is None:
                        post.image_focus_x = 0.5  # Zentral
                        post.image_focus_y = 0.5  # Zentral
                        print(f"   🎯 Focus-Point gesetzt: 50%, 50%")
                
                # Speichern ohne erneute Optimierung
                post.save()
                print(f"   💾 Gespeichert")
                
        except Exception as e:
            print(f"   ❌ Fehler bei {post.title}: {e}")
    
    print(f"\n🎉 Optimierung abgeschlossen!")
    print(f"📊 Statistik:")
    
    # Statistiken
    landscape_count = BlogPost.objects.filter(image__isnull=False).exclude(image='').filter(image_width__gt=0, image_height__gt=0).extra(where=["image_width::float / image_height::float > 1.2"]).count()
    portrait_count = BlogPost.objects.filter(image__isnull=False).exclude(image='').filter(image_width__gt=0, image_height__gt=0).extra(where=["image_width::float / image_height::float < 0.8"]).count()
    square_count = BlogPost.objects.filter(image__isnull=False).exclude(image='').filter(image_width__gt=0, image_height__gt=0).extra(where=["image_width::float / image_height::float BETWEEN 0.8 AND 1.2"]).count()
    
    print(f"   🖼️  Querformat: {landscape_count}")
    print(f"   📱 Hochformat: {portrait_count}")
    print(f"   ⬜ Quadratisch: {square_count}")

if __name__ == "__main__":
    print("🚀 Blog-Banner Bildoptimierung gestartet...\n")
    optimize_existing_images()
