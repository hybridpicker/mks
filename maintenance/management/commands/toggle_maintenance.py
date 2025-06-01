from django.core.management.base import BaseCommand
from django.core.cache import cache
import os

class Command(BaseCommand):
    help = 'Toggle maintenance mode on/off'

    def add_arguments(self, parser):
        parser.add_argument(
            '--on',
            action='store_true',
            help='Aktiviere Maintenance Mode',
        )
        parser.add_argument(
            '--off',
            action='store_true',
            help='Deaktiviere Maintenance Mode',
        )

    def handle(self, *args, **options):
        if options['on']:
            # Setze Environment Variable
            os.environ['MAINTENANCE_MODE'] = 'true'
            # Cache invalidieren
            cache.delete('maintenance_mode_status')
            self.stdout.write(self.style.SUCCESS('Maintenance Mode aktiviert'))
        elif options['off']:
            os.environ['MAINTENANCE_MODE'] = 'false'
            cache.delete('maintenance_mode_status')
            self.stdout.write(self.style.SUCCESS('Maintenance Mode deaktiviert'))
        else:
            self.stdout.write(self.style.ERROR('Bitte --on oder --off angeben'))
