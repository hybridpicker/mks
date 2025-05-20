from django.test import TestCase
from .models import MusicSchool
from location.models import Location, Country
# Create your tests here.

class MusicSchoolMetaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        country = Country.objects.create(country_name="Austria")
        country_id = country.id
        cls.music_school = MusicSchool.objects.create(
            school_name="Ludwig Ritter von Köchel Musikschule",
            country_id=country_id,
            contact_email="muikschule@krems.gv.at",
            adress_line="Hafnerplatz ",
            house_number=2, postal_code="3500",
            city="Krems",
        )

    def test_music_school_object_creation(self):
        # Use the object created in setUpTestData instead of assuming id=1
        x = self.music_school
        self.assertTrue(isinstance(x, MusicSchool))
        self.assertEqual(x.__str__(), (x.school_name) + ', ' + (x.city))

    def test_name_in_index_page(self):
        # Use the object created in setUpTestData instead of assuming id=1
        x = self.music_school
        # Add assertion here since the original test was incomplete
        self.assertIn(x.school_name, str(x))
