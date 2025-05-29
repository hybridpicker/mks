"""
Django Tests für Lazy Loading Gallery Implementation
Führen Sie aus mit: python manage.py test gallery.tests
"""
from django.test import TestCase, Client
from django.urls import reverse
from gallery.models import Photo, PhotoCategory
from django.core.files.uploadedfile import SimpleUploadedFile
from gallery.image_utils import create_lazy_image, process_uploaded_image
from PIL import Image
import io

class GalleryLazyLoadingTestCase(TestCase):
    """Testet alle Aspekte der Lazy Loading Implementation"""
    
    def setUp(self):
        self.client = Client()
        self.category = PhotoCategory.objects.create(title="Test", ordering=1)
        
    def create_test_image(self, width=800, height=600):
        """Helper: Erstellt Test-Bild"""
        img = Image.new('RGB', (width, height), color='blue')
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        return SimpleUploadedFile('test.jpg', img_io.getvalue(), 'image/jpeg')
    
    def test_complete_lazy_loading_workflow(self):
        """Testet den kompletten Lazy Loading Workflow"""
        
        # 1. Test: Gallery View lädt ohne Fotos
        response = self.client.get(reverse('gallery'))
        self.assertEqual(response.status_code, 200)
        
        # 2. Test: Erstelle Foto und prüfe HTML-Struktur
        photo = Photo.objects.create(
            title="Test Photo",
            image=self.create_test_image(1200, 900),
            category=self.category
        )
        
        response = self.client.get(reverse('gallery'))
        self.assertContains(response, 'data-src=')
        self.assertContains(response, 'class="lazy"')
        self.assertContains(response, '<noscript>')
        self.assertContains(response, photo.title)
        
        # 3. Test: Bildverarbeitung funktioniert
        test_img = self.create_test_image(2000, 1500)
        processed = process_uploaded_image(test_img)
        
        self.assertIsNotNone(processed['main'])
        self.assertIsNotNone(processed['lazy'])
        self.assertIsNotNone(processed['thumbnail'])
        
        # 4. Test: Lazy Image hat korrekte Größe
        lazy_img = create_lazy_image(self.create_test_image(1500, 1000))
        self.assertIsNotNone(lazy_img)
        
        pil_img = Image.open(lazy_img)
        self.assertLessEqual(pil_img.width, 800)
        self.assertLessEqual(pil_img.height, 600)
        
        print("✅ Alle Lazy Loading Tests erfolgreich!")