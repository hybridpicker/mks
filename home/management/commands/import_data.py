from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.management import call_command
import json

class Command(BaseCommand):
    args = ''
    help = 'Loads the initial data in to database'

    def handle(self, *args, **options):
##        call_command('loaddata', 'students/fixtures/students_dump.json')
##        call_command('loaddata', 'location/fixtures/location_dump.json')
##        call_command('loaddata', 'gallery/fixtures/gallery.json')
##        call_command('loaddata', 'teaching/fixtures/teacher_dump.json')
#        call_command('loaddata', 'events/fixtures/events.json')
##        call_command('loaddata', 'downloadsection/fixtures/forms.json')
#        call_command('loaddata', 'todo/fixtures/todo.json')
##        call_command('loaddata', 'school/fixtures/dump_data.json')
        call_command('loaddata', 'positionfinder/fixtures/databasedump.json')
        result = {'message': "Successfully Loading initial data"}
        return json.dumps(result)
