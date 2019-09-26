from django.test import TestCase
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.management import call_command
import json

# Create your tests here.
class ImportDataCommandTestCase(TestCase):
    def test_keyword_creation(self):
        x = call_command('import_data')
        result = '{"message": "Successfully Loading initial data"}'
        self.assertEqual(x, result)    
