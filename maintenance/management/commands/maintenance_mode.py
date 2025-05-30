from django.core.management.base import BaseCommand
from maintenance.models import MaintenanceMode

class Command(BaseCommand):
    help = 'Aktiviert oder deaktiviert den Wartungsmodus'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            type=str,
            choices=['on', 'off', 'status'],
            help='Aktion: on (aktivieren), off (deaktivieren), status (Status anzeigen)'
        )
        parser.add_argument(
            '--message',
            type=str,
            help='Nachricht für die Wartungsseite'
        )
        parser.add_argument(
            '--duration',
            type=str,
            help='Erwartete Dauer der Wartung'
        )

    def handle(self, *args, **options):
        maintenance = MaintenanceMode.load()
        action = options['action']
        
        if action == 'status':
            status = 'AKTIV' if maintenance.is_active else 'INAKTIV'
            self.stdout.write(f'Wartungsmodus ist: {status}')
            if maintenance.is_active:
                self.stdout.write(f'Nachricht: {maintenance.message}')
                if maintenance.expected_downtime:
                    self.stdout.write(f'Erwartete Dauer: {maintenance.expected_downtime}')
        
        elif action == 'on':
            maintenance.is_active = True
            if options['message']:
                maintenance.message = options['message']
            if options['duration']:
                maintenance.expected_downtime = options['duration']
            maintenance.save()
            self.stdout.write(self.style.SUCCESS('Wartungsmodus aktiviert'))
        
        elif action == 'off':
            maintenance.is_active = False
            maintenance.save()
            self.stdout.write(self.style.SUCCESS('Wartungsmodus deaktiviert'))