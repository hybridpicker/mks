from django.test import TestCase
from teaching.models import Teacher
from students.models import Student
from students.gender import Gender
from students.academic_title import AcademicTitle
from users.models import CustomUser
from location.models import Country, Location
from teaching.get_students import request_teacher_id, get_alibi_pic

def create_teacher(self, first_name='Maria', last_name='Musterfrau',
                   image='teacher_imageDefault', email='teacher@teacher.at',
                   phone='+43 664 750 44 533', socialSecurityField='4586',
                   iban="AT52 5200 3222 2555", bic="ATXXXSPDA",
                   adress_line='Wiener Straße', house_number="28/5/5",
                   postal_code="1100", city="Mattighofen"):
    gender = Gender.objects.create(gender='Male').id
    academic = AcademicTitle.objects.create(academic_title='Dr.').id
    user = CustomUser.objects.create(first_name=first_name, last_name=last_name).id
    country = Country.objects.create(country_name="Austria").id
    location = Location.objects.create(location_name="Vienna", country_id=country).id
    teacher = Teacher.objects.create(gender_id=gender, academic_title_id=academic,
                                     first_name=first_name, last_name=last_name,
                                     user_id=user, image=image, email=email,
                                     phone=phone, socialSecurityField=socialSecurityField,
                                     iban=iban, bic=bic, adress_line=adress_line,
                                     house_number=house_number, postal_code=postal_code,
                                     city=city, country_id=country,
                                     location_id=location)
    return teacher

class TeacherMetaTest(TestCase):
    def create_teacher(self, first_name='Maria', last_name='Musterfrau',
                       image='teacher_imageDefault', email='teacher@teacher.at',
                       phone='+43 664 750 44 533', socialSecurityField='4586',
                       iban="AT52 5200 3222 2555", bic="ATXXXSPDA",
                       adress_line='Wiener Straße', house_number="28/5/5",
                       postal_code="1100", city="Mattighofen"):
        gender = Gender.objects.create(gender='Male').id
        academic = AcademicTitle.objects.create(academic_title='Dr.').id
        user = CustomUser.objects.create(first_name=first_name, last_name=last_name).id
        country = Country.objects.create(country_name="Austria").id
        location = Location.objects.create(location_name="Vienna", country_id=country).id
        teacher = Teacher.objects.create(gender_id=gender, academic_title_id=academic,
                                         first_name=first_name, last_name=last_name,
                                         user_id=user, image=image, email=email,
                                         phone=phone, adress_line=adress_line,
                                         house_number=house_number, postal_code=postal_code,
                                         city=city, country_id=country,
                                         location_id=location)
        return teacher

    def test_teacher_creation(self):
        x = self.create_teacher()
        self.assertTrue(isinstance(x, Teacher))
        self.assertEqual(x.__str__(), (x.first_name) + ' ' + x.last_name)

class RequestTeacherIdTest(TestCase):
    def create_teacher(self, first_name='Maria', last_name='Musterfrau',
                       image='teacher_imageDefault', email='teacher@teacher.at',
                       phone='+43 664 750 44 533', socialSecurityField='4586',
                       iban="AT52 5200 3222 2555", bic="ATXXXSPDA",
                       adress_line='Wiener Straße', house_number="28/5/5",
                       postal_code="1100", city="Mattighofen"):
        gender = Gender.objects.create(gender='Male').id
        academic = AcademicTitle.objects.create(academic_title='Dr.').id
        user = CustomUser.objects.create(first_name=first_name, last_name=last_name).id
        country = Country.objects.create(country_name="Austria").id
        location = Location.objects.create(location_name="Vienna", country_id=country).id
        return Teacher.objects.create(id=4, gender_id=gender, academic_title_id=academic,
                                      first_name=first_name, last_name=last_name,
                                      user_id=user, image=image, email=email,
                                      phone=phone, adress_line=adress_line,
                                      house_number=house_number, postal_code=postal_code,
                                      city=city, country_id=country,
                                      location_id=location).user

    def test_request_if_user_id_is_four(self):
        x = self.create_teacher()
        self.assertEqual(request_teacher_id(x), 4)
