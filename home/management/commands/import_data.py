from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.management import call_command
import json

class Command(BaseCommand):
    args = ''
    help = 'Loads the initial data in to database'

    def handle(self, *args, **options):
        # Your Code
        call_command('loaddata', 'fretboard/fixtures/databasedump.json')
        call_command('loaddata', 'location/fixtures/location_dump.json')
        call_command('loaddata', 'students/fixtures/students_dump.json')
        call_command('loaddata', 'teaching/fixtures/subject_dump.json')
        call_command('loaddata', 'teaching/fixtures/calendar_dump.json')
        call_command('loaddata', 'teaching/fixtures/lessonform_dump.json')
        call_command('loaddata', 'blog/fixtures/blogdata_dump.json')
        call_command('loaddata', 'teachingmaterial/fixtures/teachingmaterial_dump.json')
        result = {'message': "Successfully Loading initial data"}
        return json.dumps(result)
