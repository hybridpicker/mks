from django.test import TestCase
from django.urls import reverse
# Create your tests here.

from teaching.lesson_form import LessonForm
from teaching.subject import Subject

class ShowGuitarTeacherViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Create 13 Materials for pagination TestCase
        subject = Subject.objects.create(subject='guitar')
        lesson_form = LessonForm.objects.create(lesson_form='Einzelunterricht',
                                                billing_form='Monatlicher Betrag',
                                                minutes=50, subject_id=subject.id,
                                                price=150,)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/preisliste')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('teaching_prices_view'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('teaching_prices_view'))
        self.assertEqual(response.status_code, 200)
        #Check actual Template
        self.assertTemplateUsed(response, 'teaching/prices.html')
        #Check template
        self.assertTemplateUsed(response, 'templates/base.html')

    def test_pricelist_in_view(self):
        response = self.client.get(reverse('teaching_prices_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('prices' in response.context)
        self.assertTrue(len(response.context['prices']) == 1)
