from django.core.management.base import BaseCommand
import datetime

class Command(BaseCommand):

    help = 'Expires event objects which are out-of-date'

    def handle(self, *args, **options):
        from todo.models import FinishedItems
        task = FinishedItems.objects.all()
        task.delete()
        return 'Deleted Finished_Todos'
