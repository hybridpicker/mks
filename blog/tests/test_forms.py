from django.test import TestCase
from blog.forms import ArticleForm
from blog.models import Author
from django.core.files.uploadedfile import SimpleUploadedFile
import os


class ArticleFormTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name="Jane", last_name="Doe")
        # Pfad zum Dummy-Bild
        self.image_path = os.path.join(os.path.dirname(__file__), 'assets/test_image.png')

    def test_valid_form(self):
        """Test if the form is valid with proper data."""
        with open(self.image_path, 'rb') as image_file:
            file_data = {
                'image': SimpleUploadedFile(
                    name='test_image.png',
                    content=image_file.read(),
                    content_type='image/png'
                )
            }
        form_data = {
            'title': 'A Valid Blog Post',
            'content': 'This is some valid content.',
            'lead_paragraph': 'A short summary.',
            'slug': 'a-valid-blog-post',  # Slug hinzugefügt
        }
        form = ArticleForm(data=form_data, files=file_data)
        print(form.errors)  # Debugging: Fehler im Formular anzeigen
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_fields(self):
        """Test if the form is invalid when required fields are missing."""
        form_data = {
            'content': 'This is content without a title.',
        }
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_invalid_slug(self):
        """Test if the form catches invalid slugs."""
        with open(self.image_path, 'rb') as image_file:
            file_data = {
                'image': SimpleUploadedFile(
                    name='test_image.png',
                    content=image_file.read(),
                    content_type='image/png'
                )
            }
        form_data = {
            'title': 'A Valid Blog Post',
            'content': 'This is some valid content.',
            'slug': 'invalid slug!',  # Invalid slug format
        }
        form = ArticleForm(data=form_data, files=file_data)
        self.assertFalse(form.is_valid())  # Formular sollte ungültig sein
        self.assertIn('slug', form.errors)  # Fehler sollte im `slug`-Feld liegen