from django.test import TestCase
from django.urls import reverse
# Create your tests here.
import datetime
from teaching.subject import Subject
from teaching.models import Teacher
from teaching.lesson_form import LessonForm
from schedule.models.calendars import Calendar
from location.models import Country, Location
from students.models import Student
from students.gender import Gender
from users.models import CustomUser
from students.academic_title import AcademicTitle

from teaching.get_students import request_teacher_id, get_alibi_pic

class CheckGetStudentViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Create 13 Materials for pagination TestCase
        Student.objects.all().delete()
        Teacher.objects.all().delete()
        gender = Gender.objects.create(gender='Male')
        gender_id = gender.id
        user = CustomUser.objects.create(first_name="username_first", last_name="username_last")
        subject = Subject.objects.create(subject='guitar')
        subject_id = subject.id
        country = Country.objects.create(country_name="Austria")
        country_id = country.id
        location = Location.objects.create(location_name="Vienna", country_id=country_id)
        location_id = location.id
        calendar = Calendar.objects.create(name='maria-musterfrau',
                                           slug='maria-musterfrau')
        calendar_id = calendar.id
        teacher = Teacher.objects.create(
            gender_id=gender_id,
            first_name='Maria',
            last_name='Musterfrau',
            image='teacher_imageDefault',
            email='teacher@teacher.at',
            subject_id=subject_id,
            bio=f'Lorem Ipsum Description',
            adress_line='Wiener Straße',
            house_number="28/5/5",
            postal_code="1100",
            city="Mattighofen",
            calendar_id=calendar_id,
            country_id=country_id,
            location_id=location_id,
            user_id=user.id,
            )
        first_name = 'Maria'
        last_name = 'Musterfrau'
        image = 'teacher_imageDefault'
        email = 'teacher@teacher.at'
        phone = '+4366475044533'
        iban = "AT52 5200 3222 2555"
        bic = "ATXXXSPDA"
        adress_line = 'Wiener Straße'
        house_number = "28"
        postal_code = "1100"
        city = "Mattighofen"
        regular_lesson_day = 3
        lesson_count = 1
        gender_male = Gender.objects.get(gender='Male').id
        gender_female = Gender.objects.create(gender='Female').id
        academic = AcademicTitle.objects.create(academic_title='Dr.').id
        country = Country.objects.create(country_name="Austria").id
        location = Location.objects.create(location_name="Vienna", country_id=country).id
        subject = Subject.objects.create(subject='Gitarre').id
        regular_lesson_time = datetime.datetime.strptime('14:00:00', '%H:%M:%S')
        start_date = datetime.datetime.strptime('2018-09-17', '%Y-%m-%d')
        lesson_form = LessonForm.objects.create(lesson_form='Einzelunterricht',
                                                billing_form='Monatlicher Betrag',
                                                minutes=25, subject_id=subject, price=250).id
        student = Student.objects.create(pk=1, gender_id=gender_male, academic_title_id=academic,
                                         first_name=first_name, phone=phone,
                                         last_name=last_name, image=image, email=email,
                                         subject_id=subject, iban=iban, bic=bic,
                                         adress_line=adress_line, house_number=house_number,
                                         postal_code=postal_code, city=city, country_id=country,
                                         teacher_id=teacher.id, lesson_form_id=lesson_form,
                                         location_id=location, lesson_count=lesson_count,
                                         regular_lesson_time=regular_lesson_time,
                                         start_date=start_date,
                                         regular_lesson_day=regular_lesson_day)
        student_female = Student.objects.create(pk=2, gender_id=gender_female, academic_title_id=academic,
                                         first_name=first_name, phone=phone,
                                         last_name=last_name, image=image, email=email,
                                         subject_id=subject, iban=iban, bic=bic,
                                         adress_line=adress_line, house_number=house_number,
                                         postal_code=postal_code, city=city, country_id=country,
                                         teacher_id=teacher.id, lesson_form_id=lesson_form,
                                         location_id=location, lesson_count=lesson_count,
                                         regular_lesson_time=regular_lesson_time,
                                         start_date=start_date,
                                         regular_lesson_day=regular_lesson_day)
        student_pic = Student.objects.create(pk=3, gender_id=gender_female, academic_title_id=academic,
                                         first_name=first_name, phone=phone,
                                         last_name=last_name, image='image.png', email=email,
                                         subject_id=subject, iban=iban, bic=bic,
                                         adress_line=adress_line, house_number=house_number,
                                         postal_code=postal_code, city=city, country_id=country,
                                         teacher_id=teacher.id, lesson_form_id=lesson_form,
                                         location_id=location, lesson_count=lesson_count,
                                         regular_lesson_time=regular_lesson_time,
                                         start_date=start_date,
                                         regular_lesson_day=regular_lesson_day)

    def get_student_args(self):
        student = Student.objects.get(pk=1)
        gender = student.gender
        first_name = student.first_name
        last_name = student.last_name
        adressline = student.adress_line
        house_number = student.house_number
        postal_code = student.postal_code
        city = student.city
        location = student.location
        email = student.email
        country = student.country
        start_date = student.start_date
        lesson_form = student.lesson_form
        image = student.image.url
        image = get_alibi_pic(image, gender, student)
            # Model data
        context = {
            'first_name': first_name,
            'last_name': last_name,
            'image': image,
            'adressline': adressline,
            'house_number': house_number,
            'postal_code': postal_code,
            'city': city,
            'postal_code': postal_code,
            'location': location,
            'email': email,
            'country': country,
            'start_date': start_date,
            'lesson_form': lesson_form,
                }
        return context

    def test_view_url_exists_at_desired_location(self):
        student_id = Student.objects.get(pk=1)
        response = self.client.get('/teaching/singlestudent?student=' + str(student_id.id), context=self.get_student_args())
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        student = Student.objects.get(pk=1)
        response = self.client.get(reverse('get_student'), {'student': student.id})
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        student = Student.objects.get(id=1)
        response = self.client.get(reverse('get_student'), {'student': student.id})
        self.assertEqual(response.status_code, 200)
        #Check actual Template
        self.assertTemplateUsed(response, 'teaching/single_student.html')
        #Check template
        self.assertTemplateUsed(response, 'templates/teaching_base.html')
#
    def test_student_is_male_pic(self):
        student = Student.objects.get(pk=1)
        response = self.client.get('/teaching/singlestudent?student=' + str(student.id), context=self.get_student_args())
        self.assertEqual(response.status_code, 200)
        self.assertTrue('image' in response.context)
        self.assertTrue(response.context['image'], '/media/students/images/signup_male.jpg')

    def test_student_is_female_pic(self):
        student = Student.objects.get(pk=2)
        response = self.client.get('/teaching/singlestudent?student=' + str(student.id), context=self.get_student_args())
        self.assertEqual(response.status_code, 200)
        self.assertTrue('image' in response.context)
        self.assertTrue(response.context['image'], '/media/students/images/signup_female.png')

    def test_student_has_already_pic(self):
        student_id = Student.objects.get(image="image.png").id
        response = self.client.get('/teaching/singlestudent?student=' + str(student_id), context=self.get_student_args())
        self.assertEqual(response.status_code, 200)
        self.assertTrue('image' in response.context)
        self.assertTrue(response.context['image'], 'image.png')
