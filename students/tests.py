from django.test import TestCase
from teaching.models import Teacher
from students.models import Student
from students.gender import Gender
from location.models import Country, Location


class GenderModelTest(TestCase):
    """Tests for the Gender model."""
    @classmethod
    def setUpTestData(cls):
        cls.gender = Gender.objects.create(gender='Male')

    def test_gender_creation(self):
        """Test if a Gender object is created successfully."""
        gender = Gender.objects.get(id=self.gender.id)
        self.assertEqual(gender.gender, 'Male')

    def test_gender_str(self):
        """Test the string representation of the Gender model."""
        gender = Gender.objects.get(id=self.gender.id)
        self.assertEqual(str(gender), 'Male')


class CountryModelTest(TestCase):
    """Tests for the Country model."""
    @classmethod
    def setUpTestData(cls):
        cls.country = Country.objects.create(country_name="Austria")

    def test_country_creation(self):
        """Test if a Country object is created successfully."""
        country = Country.objects.get(id=self.country.id)
        self.assertEqual(country.country_name, 'Austria')

    def test_country_str(self):
        """Test the string representation of the Country model."""
        country = Country.objects.get(id=self.country.id)
        self.assertEqual(str(country), 'Austria')


class LocationModelTest(TestCase):
    """Tests for the Location model."""
    @classmethod
    def setUpTestData(cls):
        cls.country = Country.objects.create(country_name="Austria")
        cls.location = Location.objects.create(location_name="Vienna", country=cls.country)

    def test_location_creation(self):
        """Test if a Location object is created successfully."""
        location = Location.objects.get(id=self.location.id)
        self.assertEqual(location.location_name, 'Vienna')
        self.assertEqual(location.country.country_name, 'Austria')

    def test_location_str(self):
        """Test the string representation of the Location model."""
        location = Location.objects.get(id=self.location.id)
        self.assertEqual(str(location), 'Vienna')

from django.core.exceptions import ValidationError

class TeacherModelTest(TestCase):
    """Tests for the Teacher model."""
    @classmethod
    def setUpTestData(cls):
        cls.gender = Gender.objects.create(gender='Female')
        cls.country = Country.objects.create(country_name="Austria")
        cls.location = Location.objects.create(location_name="Vienna", country=cls.country)
        cls.teacher = Teacher.objects.create(
            gender=cls.gender,
            country=cls.country,
            location=cls.location,
            first_name="Anna",
            last_name="Schmidt",
            email="anna.schmidt@example.com",
            phone="+43123456789",
            adress_line="Mariahilfer Straße",
            house_number="10",
            postal_code="1070",
            bic="BKAUATWWXXX",  # Valider österreichischer BIC
            iban="AT611904300234573201",  # Valide österreichische IBAN
            city="Vienna",
        )

    def test_teacher_creation(self):
        """Test if a Teacher object is created successfully."""
        teacher = Teacher.objects.get(id=self.teacher.id)
        self.assertEqual(teacher.first_name, "Anna")
        self.assertEqual(teacher.last_name, "Schmidt")
        self.assertEqual(teacher.bic, "BKAUATWWXXX")
        self.assertEqual(teacher.iban, "AT611904300234573201")
        self.assertEqual(str(teacher), "Anna Schmidt")

    def test_invalid_bic(self):
        """Test that invalid BIC raises a validation error."""
        teacher = Teacher(
            gender=self.gender,
            country=self.country,
            location=self.location,
            first_name="Invalid",
            last_name="BIC",
            email="invalid@example.com",
            phone="+43123456789",
            adress_line="Invalid Street",
            house_number="1",
            postal_code="1070",
            bic="INVALID",  # Ungültiger BIC
            iban="AT611904300234573201",
            city="Vienna",
        )
        with self.assertRaises(ValidationError):
            teacher.full_clean()  # Validierung explizit auslösen

    def test_invalid_iban(self):
        """Test that invalid IBAN raises a validation error."""
        teacher = Teacher(
            gender=self.gender,
            country=self.country,
            location=self.location,
            first_name="Invalid",
            last_name="IBAN",
            email="invalid@example.com",
            phone="+43123456789",
            adress_line="Invalid Street",
            house_number="1",
            postal_code="1070",
            bic="BKAUATWWXXX",
            iban="INVALIDIBAN",  # Ungültiger IBAN
            city="Vienna",
        )
        with self.assertRaises(ValidationError):
            teacher.full_clean()  # Validierung explizit auslösen

class StudentModelTest(TestCase):
    """Tests for the Student model."""
    @classmethod
    def setUpTestData(cls):
        cls.gender = Gender.objects.create(gender='Male')
        cls.country = Country.objects.create(country_name="Austria")
        cls.location = Location.objects.create(location_name="Vienna", country=cls.country)
        cls.teacher = Teacher.objects.create(
            gender=cls.gender,
            country=cls.country,
            location=cls.location,
            first_name='Maria',
            last_name='Musterfrau',
            email='teacher@teacher.at',
            phone='+43 664 750 44 533',
            adress_line='Wiener Straße',
            house_number="28/5/5",
            postal_code="1100",
            city="Mattighofen",
        )
        cls.student = Student.objects.create(
            gender=cls.gender,
            first_name='Maria',
            last_name='Musterfrau',
            email='student@student.at',
            adress_line='Wiener Straße',
            house_number="28/5/5",
            postal_code="1100",
            city="Mattighofen",
            country=cls.country,
            location=cls.location,
            teacher=cls.teacher,
        )

    def test_student_creation(self):
        """Test if a Student object is created successfully."""
        student = Student.objects.get(id=self.student.id)
        self.assertIsInstance(student, Student)
        self.assertEqual(student.first_name, 'Maria')
        self.assertEqual(student.last_name, 'Musterfrau')
        self.assertEqual(str(student), 'Maria Musterfrau')

    def test_student_relationships(self):
        """Test relationships between Student and related models."""
        student = Student.objects.get(id=self.student.id)
        self.assertEqual(student.gender.gender, 'Male')
        self.assertEqual(student.country.country_name, 'Austria')
        self.assertEqual(student.location.location_name, 'Vienna')
        self.assertEqual(student.teacher.first_name, 'Maria')
        self.assertEqual(student.teacher.last_name, 'Musterfrau')

    def test_student_address(self):
        """Test if the address fields of the Student model are correct."""
        student = Student.objects.get(id=self.student.id)
        self.assertEqual(student.adress_line, 'Wiener Straße')
        self.assertEqual(student.house_number, "28/5/5")
        self.assertEqual(student.postal_code, "1100")
        self.assertEqual(student.city, "Mattighofen")