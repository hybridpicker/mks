"""
Kompakter Test für Lazy Loading Gallery
Ausführen: python manage.py test gallery.tests.test_all
"""
from django.test import TestCase, Client
from django.urls import reverse
from gallery.models import Photo, PhotoCategory
from django.core.files.uploadedfile import SimpleUploadedFile
from gallery.image_utils import create_lazy_image
from PIL import Image
import io

class TestLazyLoadingGallery(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.cat = PhotoCategory.objects.create(title="Test")
        
    def make_image(self, w=800, h=600):
        img = Image.new('RGB', (w, h), 'red')
        buf = io.BytesIO()
        img.save(buf, 'JPEG')
        buf.seek(0)
        return SimpleUploadedFile('t.jpg', buf.getvalue())
    
    def test_all_features(self):
        """Testet alle Lazy Loading Features"""
        
        # 1. Gallery lädt
        r = self.client.get(reverse('gallery_view'))
        self.assertEqual(r.status_code, 200)
        
        # 2. Photo mit Lazy HTML
        p = Photo.objects.create(
            title="Test",
            image=self.make_image(),
            category=self.cat
        )
        
        r = self.client.get(reverse('gallery_view'))
        self.assertIn(b'data-src=', r.content)
        self.assertIn(b'class="lazy"', r.content)
        
        # 3. Lazy Image Generierung
        lazy = create_lazy_image(self.make_image(2000, 1500))
        self.assertIsNotNone(lazy)
        
        img = Image.open(lazy)
        self.assertLessEqual(img.width, 800)
        
        print("✅ Lazy Loading funktioniert!")