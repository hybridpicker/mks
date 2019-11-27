from django.core.management.base import BaseCommand
import datetime

class Command(BaseCommand):

    help = 'Expires event objects which are out-of-date'

    def handle(self, *args, **options):
        from events.models import Event
        event = Event.objects.filter(date__lt=datetime.datetime.now())
        event.delete()
        return 'Deleted events'
