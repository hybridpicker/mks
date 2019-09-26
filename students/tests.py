import datetime

from django.test import TestCase
from teaching.models import Teacher
from students.models import Student
from students.gender import Gender
from students.academic_title import AcademicTitle
from users.models import CustomUser
from location.models import Country, Location
from teaching.subject import Subject
from teaching.lesson_form import LessonForm
from schedule.models.calendars import Calendar

# Create your tests here.
class StudentMetaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        gender = Gender.objects.create(gender='Male')
        gender_id = gender.id
        country = Country.objects.create(country_name="Austria")
        country_id = country.id
        location = Location.objects.create(location_name="Vienna", country_id=country_id)
        location_id = location.id
        calendar = Calendar.objects.create(name='maria-musterfrau', slug='maria-musterfrau')
        teacher = Teacher.objects.create(
            gender_id=gender.id, country_id=country.id, calendar_id=calendar.id,
            location_id=location.id,
            first_name='Maria', last_name='Musterfrau',
            image='teacher_imageDefault', email='teacher@teacher.at',
            phone='+43 664 750 44 533', socialSecurityField='4586',
            iban="AT52 5200 3222 2555", bic="ATXXXSPDA",
            adress_line='Wiener Straße', house_number="28/5/5",
            postal_code="1100", city="Mattighofen",
        )
        Student.objects.create(
            id=15,
            gender_id=gender_id,
            first_name='Maria',
            last_name='Musterfrau',
            email='student@student.at',
            adress_line='Wiener Straße',
            house_number="28/5/5",
            postal_code="1100",
            city="Mattighofen",
            country_id=country_id,
            location_id=location_id,
            teacher_id=teacher.id
            )

    def test_student_creation(self):
        x = Student.objects.get(id=15)
        self.assertTrue(isinstance(x, Student))
        self.assertEqual(x.__str__(), (x.first_name) + ' ' + x.last_name)
