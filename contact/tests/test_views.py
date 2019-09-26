from django.test import TestCase
from django.test import Client
from django.urls import reverse

from contact.models import ContactKeyword
from contact.forms import ContactForm

from location.models import Location
from location.models import Country
from students.gender import Gender
from teaching.subject import Subject

class SetupClass(TestCase):
    def setUp(self):
        country_id = Country.objects.create(country_name="Austria").id
        self.location = Location.objects.create(location_name="Wien", country_id=country_id)
        self.gender = Gender.objects.create(gender='Female')
        self.subject = Subject.objects.create(subject='Guitar')

# Create your tests here.
class Contact_Form_Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        country_id = Country.objects.create(country_name="Austria").id
        location = Location.objects.create(location_name="Wien", country_id=country_id)
        gender = Gender.objects.create(gender='Female')
        subject = Subject.objects.create(subject='Guitar')
    #Valid Form Data

    #TODO: Test with Captcha
    #
    def test_contact_form_valid(self):
        gender_id = Gender.objects.get(gender='Female').id
        subject_id = Subject.objects.get(subject='Guitar').id
        location_id = Location.objects.get(location_name="Wien").id
        form = ContactForm(data={'gender': str(gender_id), 'first_name': 'Luke',
                                 'last_name': 'Skywalker', 'from_email':'luke@starwars.com',
                                 'message': 'Holaridilio this is a Message!', 'subject': str(subject_id),
                                 'location': str(location_id), 'captcha': 'captcha'})
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid(self):
        form = ContactForm(data={'gender': '', 'first_name': '',
                                 'last_name': '', 'from_email':'',
                                 'message': '!', 'subject': '',
                                 'location': ''})
        self.assertFalse(form.is_valid())

class ContactViewsTestCase(SetupClass):
    def test_contact_view(self):
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 301)
        self.assertRedirects(response, '/contact/', status_code=301,
                            target_status_code=200, fetch_redirect_response=True)


    def test_contact_form_user_view(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/email.html')

    #Invalid data
    def test_contact_form_is_invalid(self):
        response = self.client.post('/contact/success/', {'gender': '', 'first_name': '',
                                 'last_name': '', 'from_email':'',
                                 'message': '!', 'subject': '',
                                 'location': ''})
        self.assertFalse(b'Not Found' in response.content)

    #Valid data
    def test_contact_form_view(self):
        gender_id = Gender.objects.get(gender='Female').id
        subject_id = Subject.objects.get(subject='Guitar').id
        location_id = Location.objects.get(location_name="Wien").id
        response = self.client.post('/contact/success/', {'gender': str(gender_id), 'first_name': 'Luke',
                                 'last_name': 'Skywalker', 'from_email':'luke@starwars.com',
                                 'message': 'Holaridilio this is a Message!', 'subject': str(subject_id),
                                 'location': str(location_id)})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(b'Not Found' in response.content)

    def test_view_uses_correct_template(self):
        gender_id = Gender.objects.get(gender='Female').id
        subject_id = Subject.objects.get(subject='Guitar').id
        location_id = Location.objects.get(location_name="Wien").id
        response = self.client.post(reverse('success_contact'), {'gender': str(gender_id), 'first_name': 'Luke',
                                 'last_name': 'Skywalker', 'from_email':'luke@starwars.com',
                                 'message': 'Holaridilio this is a Message!', 'subject': str(subject_id),
                                 'location': str(location_id)})
        self.assertEqual(response.status_code, 200)
        #Check actual Template
        self.assertTemplateUsed(response, 'contact/success.html')
        #Check template
        self.assertTemplateUsed(response, 'templates/base.html')

    def test_get_url_correct_contact(self):
        gender_id = Gender.objects.get(gender='Female').id
        subject_id = Subject.objects.get(subject='Guitar').id
        location_id = Location.objects.get(location_name="Wien").id
        response = self.client.post('/contact/success/',
                                    {'gender': str(gender_id), 'first_name': 'Luke',
                                     'last_name': 'Skywalker',
                                     'from_email':'luke@starwars.com',
                                     'message': 'Holaridilio this is a Message!',
                                     'subject': str(subject_id),
                                     'location': str(location_id)})
        self.assertEqual(response.status_code, 200)

    def test_form_is_valid(self):
        gender_id = Gender.objects.get(gender='Female').id
        subject_id = Subject.objects.get(subject='Guitar').id
        location_id = Location.objects.get(location_name="Wien").id
        form_data = {'gender': str(gender_id), 'first_name': 'Luke',
                     'last_name': 'Skywalker', 'from_email':'luke@starwars.com',
                     'message': 'Holaridilio this is a Message!', 'subject': str(subject_id),
                     'location': str(location_id)}
        form = ContactForm(form_data)
        self.assertTrue(form.is_valid)
# TODO: Test with Captcha
#    def test_view_form_valid(self):
#        gender_id = Gender.objects.get(gender='Female').id
#        subject_id = Subject.objects.get(subject='Guitar').id
#        location_id = Location.objects.get(location_name="Wien").id
#        form_data = {'gender': str(gender_id), 'first_name': 'Luke',
#                     'last_name': 'Skywalker', 'from_email':'luke@starwars.com',
#                     'message': 'Holaridilio this is a Message!', 'subject': str(subject_id),
#                    'location': str(location_id)}
#        form = ContactForm(form_data)
#        response = self.client.post(reverse('contact_email'), form_data)
#        self.assertRedirects(response, '/contact/success/', status_code=302,
#                             target_status_code=200)
