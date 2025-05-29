from django.test import TestCase, Client
from gallery.models import Photo, PhotoCategory
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

class LazyLoadingFrontendTest(TestCase):
    """Frontend Tests für Lazy Loading"""
    
    def setUp(self):
        self.client = Client()
        self.category = PhotoCategory.objects.create(
            title='Test Category',
            ordering=1
        )
        
    def create_test_image(self, name='test.jpg'):
        """Erstellt ein Test-Bild"""
        image = Image.new('RGB', (800, 600), 'blue')
        output = io.BytesIO()
        image.save(output, format='JPEG')
        output.seek(0)
        return SimpleUploadedFile(
            name=name,
            content=output.getvalue(),
            content_type='image/jpeg'
        )
    
    def test_lazy_loading_html_structure(self):
        """Test dass HTML-Struktur für Lazy Loading korrekt ist"""
        # Erstelle Test Photos
        for i in range(3):
            photo = Photo.objects.create(
                title=f'Test Photo {i}',
                image=self.create_test_image(f'test{i}.jpg'),
                category=self.category,
                ordering=i
            )
            
            # Erstelle Lazy Image
            from gallery.image_utils import create_lazy_image
            photo.image.open()
            lazy_image = create_lazy_image(photo.image)
            if lazy_image:
                photo.image_lazy.save(lazy_image.name, lazy_image)
        
        # Hole Gallery Seite
        response = self.client.get('/gallery/')
        self.assertEqual(response.status_code, 200)
        
        # Prüfe HTML Struktur
        content = response.content.decode('utf-8')