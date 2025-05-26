#!/usr/bin/env python3
"""
Test Script für die save() Methode - prüft ob Duplikate entstehen
"""

import os
import django
from django.conf import settings

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from blog.models import BlogPost
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

def test_save_method():
    print("🧪 Teste die save() Methode auf Duplikatserstellung...")
    
    initial_count = BlogPost.objects.count()
    print(f"📊 Initial: {initial_count} Blog-Posts")
    
    # Create a test post
    test_post = BlogPost(
        title="Test Save Method",
        lead_paragraph="Test für die save() Methode",
        content="<p>Das ist ein Test-Post um zu prüfen ob die save() Methode Duplikate erstellt.</p>",
        published=False
    )
    
    print("💾 Speichere Test-Post...")
    test_post.save()
    
    after_save_count = BlogPost.objects.count()
    print(f"📊 Nach save(): {after_save_count} Blog-Posts")
    
    if after_save_count == initial_count + 1:
        print("✅ ERFOLGREICH: Genau 1 neuer Post erstellt")
    else:
        print(f"❌ PROBLEM: {after_save_count - initial_count} Posts erstellt!")
    
    # Test mit Bild-Update
    print("\n🖼️  Teste mit Bild-Upload...")
    
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    
    # Add image to post
    test_post.image.save(
        'test_image.jpg',
        ContentFile(img_io.read()),
        save=True  # This should trigger our save method
    )
    
    after_image_count = BlogPost.objects.count()
    print(f"📊 Nach Bild-Upload: {after_image_count} Blog-Posts")
    
    if after_image_count == after_save_count:
        print("✅ ERFOLGREICH: Keine zusätzlichen Posts durch Bild-Upload")
    else:
        print(f"❌ PROBLEM: {after_image_count - after_save_count} zusätzliche Posts durch Bild!")
    
    # Cleanup
    print(f"\n🧹 Lösche Test-Post (ID: {test_post.id})...")
    test_post.delete()
    
    final_count = BlogPost.objects.count()
    print(f"📊 Final: {final_count} Blog-Posts")
    
    if final_count == initial_count:
        print("✅ Cleanup erfolgreich")
    else:
        print(f"⚠️  Cleanup Problem: {final_count - initial_count} Posts übrig")

if __name__ == "__main__":
    test_save_method()
