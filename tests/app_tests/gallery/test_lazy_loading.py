import os
import tempfile
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()
from gallery.models import Photo, PhotoCategory
from gallery.image_utils import create_lazy_image, create_thumbnail, process_uploaded_image
from PIL import Image
import io
import json

class LazyLoadingTestCase(TestCase):
    """Test cases für Lazy Loading Funktionalität"""
    
    def setUp(self):
        """Setup für alle Tests"""
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        
        # Erstelle Test-Kategorie
        self.category = PhotoCategory.objects.create(
            title='Test Category',
            ordering=1
        )
        
        # Erstelle ein Test-Bild
        self.test_image = self.create_test_image()
        
    def create_test_image(self, width=1000, height=800, color='red', format='JPEG'):
        """Erstellt ein Test-Bild"""
        image = Image.new('RGB', (width, height), color)
        output = io.BytesIO()
        image.save(output, format=format)
        output.seek(0)
        return SimpleUploadedFile(
            name='test_image.jpg',
            content=output.getvalue(),
            content_type='image/jpeg'
        )    
    def test_lazy_image_creation(self):
        """Test ob Lazy Images korrekt erstellt werden"""
        # Erstelle ein Photo ohne Lazy Image
        photo = Photo.objects.create(
            title='Test Photo',
            image=self.test_image,
            category=self.category,
            ordering=1
        )
        
        # Prüfe dass noch kein echtes Lazy Image existiert (nur default)
        self.assertEqual(photo.image_lazy.name, 'gallery_lazy_imageDefault.jpg')
        
        # Erstelle Lazy Image
        photo.image.open()
        lazy_image = create_lazy_image(photo.image)
        
        # Prüfe dass Lazy Image erstellt wurde
        self.assertIsNotNone(lazy_image)
        
        # Speichere Lazy Image
        photo.image_lazy.save(lazy_image.name, lazy_image)
        photo.refresh_from_db()
        
        # Prüfe dass Lazy Image gespeichert wurde (nicht mehr default)
        self.assertTrue(photo.image_lazy)
        self.assertNotEqual(photo.image_lazy.name, 'gallery_lazy_imageDefault.jpg')
        self.assertIn('_lazy.jpg', photo.image_lazy.name)
    
    def test_thumbnail_creation(self):
        """Test ob Thumbnails korrekt erstellt werden"""
        # Erstelle ein Photo ohne Thumbnail
        photo = Photo.objects.create(
            title='Test Photo Thumbnail',
            image=self.create_test_image(),
            category=self.category,
            ordering=2
        )
        
        # Erstelle Thumbnail
        photo.image.seek(0)
        thumbnail = create_thumbnail(photo.image)
        
        # Prüfe dass Thumbnail erstellt wurde
        self.assertIsNotNone(thumbnail)
        
        # Speichere Thumbnail
        photo.image_thumbnail.save(thumbnail.name, thumbnail)
        photo.refresh_from_db()
        
        # Prüfe dass Thumbnail gespeichert wurde
        self.assertTrue(photo.image_thumbnail)
        self.assertIn('_thumb.jpg', photo.image_thumbnail.name)    
    def test_process_uploaded_image(self):
        """Test die komplette Bildverarbeitung"""
        # Erstelle großes Test-Bild
        large_image = self.create_test_image(width=3000, height=2000)
        
        # Verarbeite das Bild
        processed = process_uploaded_image(large_image)
        
        # Prüfe dass alle Varianten erstellt wurden
        self.assertIsNotNone(processed['main'])
        self.assertIsNotNone(processed['thumbnail'])
        self.assertIsNotNone(processed['lazy'])
        
        # Prüfe die Namen
        self.assertIn('.jpg', processed['main'].name)
        self.assertIn('_thumb.jpg', processed['thumbnail'].name)
        self.assertIn('_lazy.jpg', processed['lazy'].name)
    
    def test_gallery_view_with_lazy_loading(self):
        """Test der Gallery View mit Lazy Loading"""
        # Erstelle mehrere Test-Photos
        for i in range(5):
            Photo.objects.create(
                title=f'Test Photo {i}',
                image=self.create_test_image(),
                category=self.category,
                ordering=i
            )
        
        # Rufe Gallery View auf
        response = self.client.get(reverse('gallery_view'))
        
        # Prüfe Response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-src')
        self.assertContains(response, 'lazy-loading.js')
        self.assertContains(response, 'lazy-loading.css')
        
        # Prüfe dass alle Photos im Context sind
        self.assertEqual(len(response.context['photos']), 5)
        
        # Prüfe JSON Daten
        gallery_json = json.loads(response.context['gallery_json_data'])
        self.assertEqual(len(gallery_json), 5)    
    def test_automatic_lazy_generation_in_view(self):
        """Test dass Lazy Images automatisch in der View generiert werden"""
        # Erstelle Photo ohne Lazy Image
        photo = Photo.objects.create(
            title='Photo without Lazy',
            image=self.create_test_image(),
            category=self.category,
            ordering=1
        )
        
        # Prüfe dass kein echtes Lazy Image existiert (nur default)
        self.assertEqual(photo.image_lazy.name, 'gallery_lazy_imageDefault.jpg')
        
        # Rufe Gallery View auf
        response = self.client.get(reverse('gallery_view'))
        self.assertEqual(response.status_code, 200)
        
        # Photo neu laden und prüfen ob Lazy Image erstellt wurde
        photo.refresh_from_db()
        self.assertNotEqual(photo.image_lazy.name, 'gallery_lazy_imageDefault.jpg', "Lazy Image sollte automatisch erstellt worden sein")
        self.assertNotEqual(photo.image_thumbnail.name, 'gallery_thumbnail_imageDefault.jpg', "Thumbnail sollte automatisch erstellt worden sein")
    
    def test_admin_automatic_processing(self):
        """Test dass der Admin automatisch Bilder verarbeitet"""
        self.client.login(username='admin', password='testpass123')
        
        # Erstelle neues Bild über Admin
        test_image = self.create_test_image(width=2500, height=2000)
        
        response = self.client.post(
            reverse('admin:gallery_photo_add'),
            {
                'title': 'Admin Test Photo',
                'image': test_image,
                'category': self.category.id,
                'ordering': 1,
            }
        )
        
        # Prüfe ob erfolgreich erstellt
        self.assertEqual(response.status_code, 302)  # Redirect nach Erfolg
        
        # Hole das erstellte Photo
        photo = Photo.objects.get(title='Admin Test Photo')
        
        # Prüfe dass alle Bildvarianten erstellt wurden
        self.assertTrue(photo.image)
        self.assertTrue(photo.image_lazy)
        self.assertTrue(photo.image_thumbnail)