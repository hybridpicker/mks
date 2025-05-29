#!/usr/bin/env python
"""
Debug script to test gallery upload functionality
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from gallery.models import Photo, PhotoCategory

# Check if categories exist
categories = PhotoCategory.objects.all()
print(f"Found {categories.count()} categories:")
for cat in categories:
    print(f"  - {cat.id}: {cat.title}")

# Check if photos exist
photos = Photo.objects.all()
print(f"\nFound {photos.count()} photos total")

# Check media directory
media_path = "/Users/lukasschonsgibl/Coding/Django/mks/media/gallery/images"
if os.path.exists(media_path):
    files = os.listdir(media_path)
    print(f"\nFound {len(files)} files in media/gallery/images/")
else:
    print(f"\nMedia directory does not exist: {media_path}")

# Create a test category if none exist
if categories.count() == 0:
    print("\nNo categories found. Creating test category...")
    test_cat = PhotoCategory.objects.create(
        title="Test Gallery",
        ordering=1
    )
    print(f"Created category: {test_cat.title} (ID: {test_cat.id})")
