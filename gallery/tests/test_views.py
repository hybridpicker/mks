from django.test import TestCase, Client
from django.urls import reverse
from gallery.models import Photo, PhotoCategory
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

class GalleryViewTestCase(TestCase):
    """Test cases für Gallery Views"""
    
    def setUp(self):
        self.client = Client()
        self.category = PhotoCategory.objects.create(
            title="Test Category",
            ordering=1
        )
        
    def create_test_photo(self):
        """Erstelle ein Test-Foto mit Bild"""
        img = Image.new('RGB', (800, 600), color='blue')
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        image_file = SimpleUploadedFile(
            name='test_photo.jpg',
            content=img_io.getvalue(),
            content_type='image/jpeg'
        )
        
        photo = Photo.objects.create(
            title="Test Photo",
            image=image_file,
            category=self.category,
            ordering=1
        )
        return photo
    
    def test_gallery_view_loads(self):
        """Test ob Gallery View lädt"""
        response = self.client.get(reverse('gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gallery/gallery.html')
    
    def test_gallery_with_lazy_loading(self):
        """Test Gallery mit Lazy Loading Features"""
        photo = self.create_test_photo()
        response = self.client.get(reverse('gallery'))
        
        # Prüfe ob Lazy Loading HTML vorhanden ist
        self.assertContains(response, 'data-src=')
        self.assertContains(response, 'class="lazy"')