#!/usr/bin/env python
"""
Test the gallery upload functionality directly
"""

import os
import sys
import django
import json
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from django.contrib.auth import get_user_model
from gallery.models import Photo, PhotoCategory
from PIL import Image
import io

User = get_user_model()

# Create test client
client = Client()

# Create or get test user
try:
    user = User.objects.get(username='admin')
except User.DoesNotExist:
    print("Please run this test with an existing admin user")
    sys.exit(1)

# Login
client.force_login(user)

# Get first category
category = PhotoCategory.objects.first()
if not category:
    print("No categories found!")
    sys.exit(1)

print(f"Using category: {category.title} (ID: {category.id})")

# Create a test image
def create_test_image():
    img = Image.new('RGB', (800, 600), color='blue')
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return SimpleUploadedFile("test_image.jpg", buffer.getvalue(), content_type="image/jpeg")

# Test upload
print("\nTesting image upload...")
test_image = create_test_image()

response = client.post('/galerie/admin/upload/', {
    'is_multiple': 'true',
    'category_id': category.id,
    'images': [test_image]
})

print(f"Response status: {response.status_code}")
print(f"Response content: {response.content.decode()}")

if response.status_code == 200:
    data = json.loads(response.content)
    if data.get('status') == 'success':
        print("\n✅ Upload successful!")
        print(f"Message: {data.get('message')}")
    else:
        print("\n❌ Upload failed!")
        print(f"Error: {data.get('message')}")
        if data.get('errors'):
            for error in data['errors']:
                print(f"  - {error}")
else:
    print(f"\n❌ HTTP Error: {response.status_code}")
