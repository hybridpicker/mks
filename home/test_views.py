from django.test import TestCase
from django.test import Client
from django.urls import reverse

class HomeViewTestCase(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_home_template_render(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'home/index.html')
        #Check template
        self.assertTemplateUsed(response, 'templates/base.html')

class ImpressumViewTestCase(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('impressum'))
        self.assertEqual(response.status_code, 200)

    def test_view_templates(self):
        #Check actual Template
        response = self.client.get(reverse('impressum'))
        self.assertTemplateUsed(response, 'home/impressum.html')
        #Check template
        self.assertTemplateUsed(response, 'templates/base.html')
