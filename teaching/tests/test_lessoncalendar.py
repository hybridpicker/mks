from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.test.client import RequestFactory
from django.contrib.auth.models import User

import datetime
from django.contrib.auth.decorators import login_required

from lessoncalendar.lessonevent import create_lesson_event
from students.models import Student
from students.gender import Gender
from schedule.models import Event
from schedule.models import Calendar
from teaching.models import Teacher
from teaching.subject import Subject
from location.models import Country, Location
from schedule.models.calendars import Calendar
from teaching.lesson_form import LessonForm
from lessoncalendar.models import LessonEvent
from users.models import CustomUser
from students.academic_title import AcademicTitle

from teaching.views import get_calendar, get_date_time
from teaching.views import get_end_time, increment_counter
from teaching.views import get_title

class LessonCalendarViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Create 13 Materials for pagination TestCase
        Student.objects.all().delete()
        Teacher.objects.all().delete()
        gender = Gender.objects.create(gender='Male')
        gender_id = gender.id
        user = CustomUser.objects.create(username="Captain", first_name="Captain", last_name="Marv", password="123")
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
        first_name = 'Mitch'
        last_name = 'Maisel'
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
        lesson_count = 0
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

    def test_calendar_request(self):
        user = CustomUser.objects.get(first_name="Captain", last_name="Marv")
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='Captain', password='12345')
        start = datetime.datetime.strptime('14:00', '%H:%M')
        end = datetime.datetime.strptime('15:00', '%H:%M')
        student = Student.objects.get(last_name='Maisel')
        calendar = get_calendar(student.id)
        title = str(student)
        form_data = {'start':start,'end':end, 'title':title,
                     'calendar':calendar,'student':student,}
        form = create_lesson_event(form_data)
        self.assertTrue(form.is_valid)
        response = client.get("/teaching/calendar".format(user.id), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/calendar/fullcalendar.html')

    def test_form_valid_request(self):
        user = CustomUser.objects.get(first_name="Captain", last_name="Marv")
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='Captain', password='12345')
        start = datetime.datetime.strptime('14:00', '%H:%M')
        end = datetime.datetime.strptime('15:00', '%H:%M')
        student = Student.objects.get(last_name='Maisel')
        calendar = get_calendar(student.id)
        title = str(student)
        date = '2019-04-16'
        time = '14:00'
        text_field = 'Lorem Ipsum'
        form_data = {'date':date,
                     'time':time,
                     'text_field':text_field,
                     'student':student.id}
        form = create_lesson_event(data=form_data)
        self.assertTrue(form.is_valid())
        response = client.get(reverse('teaching_calendar'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/calendar/fullcalendar.html')

    def test_form_invalid_request(self):
        user = CustomUser.objects.get(first_name="Captain", last_name="Marv")
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='Captain', password='12345')
        start = datetime.datetime.strptime('14:00', '%H:%M')
        end = datetime.datetime.strptime('15:00', '%H:%M')
        student = Student.objects.get(last_name='Maisel')
        calendar = get_calendar(student.id)
        title = str(student)
        date = '2019-04-16'
        time = '14:00'
        text_field = 'Lorem Ipsum'
        form_data = {'date':date,
                     'time':time,
                     'text_field':text_field,
                     'student':''}
        form = create_lesson_event(data=form_data)
        self.assertFalse(form.is_valid())
        response = client.get(reverse('teaching_calendar'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/calendar/fullcalendar.html')

    def test_get_date_time(self):
        start = '14:00'
        date = '2018-09-17'
        end_date = datetime.datetime.strptime('2018-09-17 14:00', '%Y-%m-%d %H:%M')
        date_time_func = get_date_time(date, start)
        self.assertEqual(date_time_func, end_date)

    def test_get_end_time(self):
        start = datetime.datetime.strptime('2018-09-17 14:00', '%Y-%m-%d %H:%M')
        student = Student.objects.get(first_name='Mitch')
        end_time_func = get_end_time(start, student.id)
        end_time = datetime.datetime.strptime('2018-09-17 14:25', '%Y-%m-%d %H:%M')
        self.assertEqual(end_time_func, end_time)

    def test_increment_count(self):
        student = Student.objects.get(first_name='Mitch')
        counter = student.lesson_count
        new_count = increment_counter(student.id)
        self.assertEqual(new_count, (counter + 1))

    def get_title_calendar(self):
        student = Student.objects.get(first_name='Mitch')
        new_count = increment_counter(student.id)
        x = get_title(student.id, new_count)
        y = str(student) + ' (' +str(new_count) + ')'
        self.assertEqual(x, y)
