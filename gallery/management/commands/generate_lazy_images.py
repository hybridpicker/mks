from django.core.management.base import BaseCommand
from gallery.models import Photo
from gallery.image_utils import create_lazy_image, create_thumbnail
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Generiert Lazy Loading und Thumbnail Bilder für alle existierenden Fotos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Überschreibt existierende Lazy/Thumbnail Bilder',
        )
        parser.add_argument(
            '--photo-id',
            type=int,
            help='Verarbeitet nur ein spezifisches Foto mit der angegebenen ID',
        )

    def handle(self, *args, **options):
        force = options.get('force', False)
        photo_id = options.get('photo_id')
        
        if photo_id:
            photos = Photo.objects.filter(id=photo_id)
            if not photos.exists():
                self.stdout.write(
                    self.style.ERROR(f'Foto mit ID {photo_id} nicht gefunden')
                )
                return
        else:
            photos = Photo.objects.all()
        
        total_photos = photos.count()
        processed = 0
        skipped = 0
        errors = 0
        
        self.stdout.write(
            self.style.SUCCESS(f'Starte Verarbeitung von {total_photos} Fotos...')
        )        
        for photo in photos:
            try:
                # Prüfe ob das Hauptbild existiert
                if not photo.image:
                    self.stdout.write(
                        self.style.WARNING(f'Foto {photo.id} hat kein Bild')
                    )
                    skipped += 1
                    continue
                
                image_path = os.path.join(settings.MEDIA_ROOT, photo.image.name)
                if not os.path.exists(image_path):
                    self.stdout.write(
                        self.style.WARNING(f'Bilddatei nicht gefunden: {photo.image.name}')
                    )
                    skipped += 1
                    continue
                
                # Prüfe ob Lazy Image generiert werden muss
                generate_lazy = force or not photo.image_lazy
                generate_thumb = force or not photo.image_thumbnail
                
                if not generate_lazy and not generate_thumb:
                    skipped += 1
                    continue
                
                # Öffne das Bild
                photo.image.open()
                
                # Generiere Lazy Image
                if generate_lazy:
                    lazy_image = create_lazy_image(photo.image)
                    if lazy_image:
                        photo.image_lazy.save(lazy_image.name, lazy_image, save=False)
                        self.stdout.write(f'Lazy image erstellt für Foto {photo.id}')
                
                # Generiere Thumbnail
                if generate_thumb:
                    photo.image.seek(0)  # Reset file pointer
                    thumbnail = create_thumbnail(photo.image)
                    if thumbnail:
                        photo.image_thumbnail.save(thumbnail.name, thumbnail, save=False)
                        self.stdout.write(f'Thumbnail erstellt für Foto {photo.id}')
                
                # Speichere Änderungen
                photo.save()
                processed += 1
                
            except Exception as e:
                errors += 1
                self.stdout.write(
                    self.style.ERROR(f'Fehler bei Foto {photo.id}: {str(e)}')
                )
                logger.error(f'Fehler bei Verarbeitung von Foto {photo.id}: {str(e)}')
        
        # Zusammenfassung
        self.stdout.write(
            self.style.SUCCESS(
                f'\nVerarbeitung abgeschlossen:\n'
                f'- Verarbeitet: {processed}\n'
                f'- Übersprungen: {skipped}\n'
                f'- Fehler: {errors}\n'
                f'- Gesamt: {total_photos}'
            )
        )