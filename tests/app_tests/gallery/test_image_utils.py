import os
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

from gallery.image_utils import create_lazy_image, create_thumbnail, process_uploaded_image

class ImageUtilsTestCase(TestCase):
    """Test cases für image_utils.py Funktionen"""
    
    def create_test_image(self, width=1000, height=800):
        """Erstelle ein Test-Bild"""
        img = Image.new('RGB', (width, height), color='red')
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        return SimpleUploadedFile(
            name=f'test_{width}x{height}.jpg',
            content=img_io.getvalue(),
            content_type='image/jpeg'
        )
    
    def test_lazy_image_creation(self):
        """Test ob Lazy Images korrekt erstellt werden"""
        test_image = self.create_test_image()
        lazy_image = create_lazy_image(test_image)
        
        self.assertIsNotNone(lazy_image)
        self.assertTrue(lazy_image.name.endswith('_lazy.jpg'))
        
        # Prüfe Größe
        lazy_img = Image.open(lazy_image)
        self.assertLessEqual(lazy_img.width, 800)
        self.assertLessEqual(lazy_img.height, 600)
    
    def test_process_uploaded_image(self):
        """Test ob alle Varianten erstellt werden"""
        test_image = self.create_test_image(2000, 1500)
        processed = process_uploaded_image(test_image)
        
        self.assertIn('main', processed)
        self.assertIn('thumbnail', processed)
        self.assertIn('lazy', processed)
        self.assertIsNotNone(processed['main'])
        self.assertIsNotNone(processed['thumbnail'])
        self.assertIsNotNone(processed['lazy'])