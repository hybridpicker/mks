from django.test import TestCase
from .models import MusicSchool
from location.models import Location, Country
# Create your tests here.

class MusicSchoolMetaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        country = Country.objects.create(country_name="Austria")
        country_id = country.id
        music_school = MusicSchool.objects.create(
            school_name ="Ludwig Ritter von Köchel Musikschule",
            country_id=country_id,
            contact_email="muikschule@krems.gv.at",
            adress_line="Hafnerplatz ",
            house_number=2, postal_code="3500",
            city="Krems",
        )

    def test_music_school_object_creation(self):
        x = MusicSchool.objects.get(id=1)
        self.assertTrue(isinstance(x, MusicSchool))
        self.assertEqual(x.__str__(), (x.school_name) + ', ' + (x.city))
