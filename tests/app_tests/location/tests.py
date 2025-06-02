from django.test import TestCase
from location.models import Country, Location

# Create your tests here.

class CountryTestCase(TestCase):
    def create_country(self, country_name="Austria"):
        return Country.objects.create(country_name=country_name)

    def test_country_creation(self):
        x = self.create_country()
        self.assertTrue(isinstance(x, Country))
        self.assertEqual(x.__str__(), x.country_name)


class LocationTestCase(TestCase):
    def create_country(self, country_name="Austria"):
        return Country.objects.create(country_name=country_name)

    def create_location(self, location_name="Vienna"):
        country = Country.objects.create(country_name="Vienna")
        country_name = Country.objects.get(country_name=country).id
        return Location.objects.create(location_name=location_name, country_id=country_name)

    def test_location_creation(self):
        x = self.create_location()
        self.assertTrue(isinstance(x, Location))
        self.assertEqual(x.__str__(), x.location_name)
