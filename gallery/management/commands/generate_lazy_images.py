from django.core.management.base import BaseCommand
from django.db.models import Q
from gallery.models import Photo
from gallery.image_utils import create_lazy_image, create_thumbnail
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Generiert fehlende Lazy Images und Thumbnails für alle Gallery Photos'

    def handle(self, *args, **options):
        # Finde alle Photos die Lazy Images brauchen
        photos_needing_processing = Photo.objects.filter(
            Q(image_lazy__isnull=True) | 
            Q(image_lazy='gallery_lazy_imageDefault.jpg') |
            Q(image_thumbnail__isnull=True) |
            Q(image_thumbnail='gallery_thumbnail_imageDefault.jpg')
        )
        
        total = photos_needing_processing.count()
        self.stdout.write(f'Gefunden: {total} Photos die verarbeitet werden müssen')
        
        processed = 0
        errors = 0
        
        for photo in photos_needing_processing:
            try:
                if not photo.image:
                    continue
                    
                # Lazy Image generieren
                if not photo.image_lazy or photo.image_lazy.name == 'gallery_lazy_imageDefault.jpg':
                    lazy_image = create_lazy_image(photo.image)
                    if lazy_image:
                        photo.image_lazy.save(
                            f'lazy_{photo.id}_{photo.image.name.split("/")[-1]}',
                            ContentFile(lazy_image.read()),
                            save=False
                        )
                
                # Thumbnail generieren
                if not photo.image_thumbnail or photo.image_thumbnail.name == 'gallery_thumbnail_imageDefault.jpg':
                    thumbnail = create_thumbnail(photo.image)
                    if thumbnail:
                        photo.image_thumbnail.save(
                            f'thumb_{photo.id}_{photo.image.name.split("/")[-1]}',
                            ContentFile(thumbnail.read()),
                            save=False
                        )
                
                photo.save()
                processed += 1
                
                if processed % 10 == 0:
                    self.stdout.write(f'Verarbeitet: {processed}/{total}')
                    
            except Exception as e:
                errors += 1
                logger.error(f'Fehler bei Photo {photo.id}: {str(e)}')
                self.stdout.write(self.style.ERROR(f'Fehler bei Photo {photo.id}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'Fertig! {processed} Photos verarbeitet, {errors} Fehler'
        ))