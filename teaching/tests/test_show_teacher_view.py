from django.test import TestCase
from django.urls import reverse
# Create your tests here.

from teaching.subject import Subject
from teaching.models import Teacher
from schedule.models.calendars import Calendar
from location.models import Country, Location
from students.gender import Gender

class ShowGuitarTeacherViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Create 13 Materials for pagination TestCase
        number_of_teachers = 13
        gender = Gender.objects.create(gender='Male')
        gender_id = gender.id
        subject = Subject.objects.create(subject='guitar', id=1)
        subject_id = subject.id
        country = Country.objects.create(country_name="Austria")
        country_id = country.id
        location = Location.objects.create(location_name="Vienna", country_id=country_id)
        location_id = location.id

        for teacher_id in range (number_of_teachers):
            calendar = Calendar.objects.create(name=f'maria-musterfrau{teacher_id}',
                                               slug=f'maria-musterfrau{teacher_id}')
            calendar_id = calendar.id
            Teacher.objects.create(
                gender_id=gender_id,
                first_name=f'Maria {teacher_id}',
                last_name=f'Musterfrau {teacher_id}',
                image='teacher_imageDefault',
                email=f'teacher{teacher_id}@teacher.at',
                subject_id=subject_id,
                bio=f'Lorem Ipsum Description',
                adress_line='Wiener Straße',
                house_number="28/5/5",
                postal_code="1100",
                city="Mattighofen",
                calendar_id=calendar_id,
                country_id=country_id,
                location_id=location_id,
                )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/gitarrenunterricht')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('guitar_lessons'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('guitar_lessons'))
        self.assertEqual(response.status_code, 200)
        #Check actual Template
        self.assertTemplateUsed(response, 'teaching/guitar_lesson.html')
        #Check template
        self.assertTemplateUsed(response, 'templates/base.html')

    def test_teacher_list_is_13(self):
        response = self.client.get('/gitarrenunterricht')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('teacher_data' in response.context)
        self.assertTrue(len(response.context['teacher_data']) == 13)

class ShowPianoTeacherViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/klavierunterricht')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('piano_lessons'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('piano_lessons'))
        self.assertEqual(response.status_code, 200)
        #Check actual Template
        self.assertTemplateUsed(response, 'teaching/piano_lesson.html')
        #Check template
        self.assertTemplateUsed(response, 'templates/base.html')

class ShowVocalTeacherViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/gesangsunterricht')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('vocal_lessons'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('vocal_lessons'))
        self.assertEqual(response.status_code, 200)
        #Check actual Template
        self.assertTemplateUsed(response, 'teaching/vocal_lesson.html')
        #Check template
        self.assertTemplateUsed(response, 'templates/base.html')
