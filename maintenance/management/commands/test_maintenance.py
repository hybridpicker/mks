from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Run maintenance mode tests'

    def handle(self, *args, **options):
        self.stdout.write('Running maintenance mode tests...')
        call_command('test', 'maintenance', '--verbosity=2')
