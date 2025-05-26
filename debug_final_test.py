#!/usr/bin/env python3
"""
Finaler Test für das Blog-System - prüft auf Duplikate
"""

import os
import django

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from blog.models import BlogPost
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

def test_no_duplicates():
    print("🔧 BLOG-SYSTEM DUPLIKAT-TEST")
    print("=" * 40)
    
    initial_count = BlogPost.objects.count()
    print(f"📊 Start: {initial_count} Posts")
    
    # Test 1: Post mit Bild
    print("\n🖼️  Test: Post mit Bild erstellen...")
    
    # Create test image
    img = Image.new('RGB', (800, 600), color='red')
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    
    post = BlogPost(
        title="Duplikat-Test Post",
        lead_paragraph="Test für Duplikate",
        content="<p>Test-Content</p>",
        published=True
    )
    
    # Add image and save
    post.image.save(
        'duplikat_test.jpg',
        ContentFile(img_io.read()),
        save=False
    )
    
    post.save()
    
    after_create = BlogPost.objects.count()
    print(f"📊 Nach Erstellung: {after_create} Posts")
    
    # Test 2: Post mehrfach speichern
    print(f"\n🔁 Test: Post mehrfach speichern...")
    
    for i in range(5):
        post.title = f"Duplikat-Test Post - Update {i+1}"
        post.save()
        count = BlogPost.objects.count()
        print(f"   Save {i+1}: {count} Posts")
    
    final_count = BlogPost.objects.count()
    
    # Results
    print(f"\n📊 ERGEBNIS:")
    print(f"   Start: {initial_count}")
    print(f"   Ende: {final_count}")
    print(f"   Erwartet: {initial_count + 1}")
    
    if final_count == initial_count + 1:
        print("✅ ERFOLG: Keine Duplikate!")
    else:
        duplicates = final_count - initial_count - 1
        print(f"❌ PROBLEM: {duplicates} Duplikate erstellt!")
    
    # Cleanup
    post.delete()
    print(f"🧹 Cleanup: {BlogPost.objects.count()} Posts übrig")

if __name__ == "__main__":
    test_no_duplicates()
