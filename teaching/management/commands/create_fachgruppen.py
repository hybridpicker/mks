from django.core.management.base import BaseCommand
from teaching.subject import SubjectCategory

class Command(BaseCommand):
    help = 'Erstellt die Fachgruppen-Kategorien für die Musikschule'

    def handle(self, *args, **options):
        categories = [
            'Blasinstrumente',
            'Elementare Musikerziehung',
            'Musikkunde',
            'Schlaginstrumente',
            'Stimmbildung',
            'Streichinstrumente',
            'Tasteninstrumente',
            'Zupfinstrumente',
            'Tanz und Bewegung',
            'Kunstschule'
        ]
        
        for category_name in categories:
            category, created = SubjectCategory.objects.get_or_create(
                name=category_name,
                defaults={'hidden': False}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Kategorie "{category_name}" wurde erstellt.'
                    )
                )
            else:
                self.stdout.write(
                    f'Kategorie "{category_name}" existiert bereits.'
                )
