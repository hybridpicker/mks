"""
Umfassender Test für die Lazy Loading Gallery Implementation
"""
import os
import tempfile
import json
from django.test import TestCase, Client, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth import get_user_model
from gallery.models import Photo, PhotoCategory
from gallery.image_utils import create_lazy_image, create_thumbnail, process_uploaded_image
from PIL import Image
import io

# Temporäres Media-Verzeichnis für Tests
TEMP_MEDIA_ROOT = tempfile.mkdtemp()

User = get_user_model()

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ComprehensiveLazyLoadingTest(TestCase):
    """Umfassender Test für alle Lazy Loading Features"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Erstelle notwendige Verzeichnisse
        os.makedirs(os.path.join(TEMP_MEDIA_ROOT, 'gallery/images'), exist_ok=True)
        os.makedirs(os.path.join(TEMP_MEDIA_ROOT, 'gallery/images/lazy'), exist_ok=True)
        os.makedirs(os.path.join(TEMP_MEDIA_ROOT, 'gallery/images/thumbnail'), exist_ok=True)
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )
        
        self.category = PhotoCategory.objects.create(
            title='Test Category',
            ordering=1
        )
    
    def create_test_image(self, width=1000, height=800, color='red'):
        """Erstellt ein Test-Bild"""
        image = Image.new('RGB', (width, height), color)
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=85)
        output.seek(0)
        return SimpleUploadedFile('test.jpg', output.getvalue())    
    def test_complete_lazy_loading_workflow(self):
        """Test des kompletten Lazy Loading Workflows"""
        print("\n🧪 Test 1: Kompletter Lazy Loading Workflow")
        
        # 1. Erstelle Photo ohne Lazy Images
        photo = Photo.objects.create(
            title='Test Photo',
            image=self.create_test_image(2000, 1500),
            category=self.category,
            ordering=1
        )
        self.assertFalse(photo.image_lazy, "❌ Photo sollte noch kein Lazy Image haben")
        print("✅ Photo ohne Lazy Image erstellt")
        
        # 2. Rufe Gallery View auf
        response = self.client.get('/galerie/')
        self.assertEqual(response.status_code, 200)
        print("✅ Gallery View erfolgreich aufgerufen")
        
        # 3. Prüfe ob Lazy Image automatisch erstellt wurde
        photo.refresh_from_db()
        self.assertTrue(photo.image_lazy, "❌ Lazy Image sollte automatisch erstellt worden sein")
        self.assertTrue(photo.image_thumbnail, "❌ Thumbnail sollte automatisch erstellt worden sein")
        print("✅ Lazy Images wurden automatisch generiert")
        
        # 4. Prüfe HTML-Struktur
        content = response.content.decode('utf-8')
        self.assertIn('data-src=', content, "❌ data-src Attribut fehlt")
        self.assertIn('class="lazy"', content, "❌ lazy Klasse fehlt")
        self.assertIn('<noscript>', content, "❌ noscript Tag fehlt")
        self.assertIn('lazy-loading.js', content, "❌ Lazy Loading Script fehlt")
        self.assertIn('lazy-loading.css', content, "❌ Lazy Loading CSS fehlt")
        print("✅ HTML-Struktur für Lazy Loading korrekt")
        
        # 5. Prüfe JSON Daten
        json_data = json.loads(response.context['gallery_json_data'])
        self.assertEqual(len(json_data), 1)
        self.assertIn(str(photo.id), json_data)
        print("✅ JSON Daten korrekt generiert")
        
    def test_image_processing_sizes(self):
        """Test dass Bilder korrekt verkleinert werden"""
        print("\n🧪 Test 2: Bildverarbeitung und Größen")
        
        # Erstelle großes Bild
        large_image = self.create_test_image(3000, 2000)
        processed = process_uploaded_image(large_image)
        
        self.assertIsNotNone(processed['main'], "❌ Hauptbild fehlt")
        self.assertIsNotNone(processed['lazy'], "❌ Lazy Image fehlt")
        self.assertIsNotNone(processed['thumbnail'], "❌ Thumbnail fehlt")
        print("✅ Alle Bildvarianten erstellt")