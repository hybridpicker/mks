import json
from django.shortcuts import render, redirect
from gallery.models import Photo, PhotoCategory
import logging
import os
from django.conf import settings
from gallery.image_utils import create_lazy_image, create_thumbnail
from django.core.files.base import ContentFile

# Logger einrichten
logger = logging.getLogger(__name__)

# Create your views here.
def gallery_view(request):
    # Alle Fotos aus allen Kategorien laden (außer von E-Learning)
    all_photos = Photo.objects.exclude(category__title="E-Learning").order_by('-ordering')
    
    # Filterung der Fotos, um sicherzustellen, dass die Bilddateien existieren
    photos = []
    for photo in all_photos:
        # Prüfen, ob Bilddatei existiert
        image_path = os.path.join(settings.MEDIA_ROOT, photo.image.name)
        if os.path.exists(image_path):
            photos.append(photo)
            
            # Automatische Generierung von Lazy Images wenn nicht vorhanden
            try:
                # Prüfe ob Lazy Image generiert werden muss
                if photo.image and not photo.image_lazy:
                    logger.info(f"Generiere Lazy Image für Photo ID: {photo.id}")
                    
                    # Öffne das Originalbild
                    photo.image.open()
                    
                    # Erstelle Lazy Image
                    lazy_image = create_lazy_image(photo.image)
                    if lazy_image:
                        # Speichere das Lazy Image
                        photo.image_lazy.save(lazy_image.name, lazy_image, save=True)
                        logger.info(f"Lazy Image erfolgreich erstellt für Photo ID: {photo.id}")
                    else:
                        logger.warning(f"Konnte kein Lazy Image erstellen für Photo ID: {photo.id}")
                
                # Optional: Auch Thumbnail generieren wenn nicht vorhanden
                if photo.image and not photo.image_thumbnail:
                    logger.info(f"Generiere Thumbnail für Photo ID: {photo.id}")
                    
                    # Reset file pointer
                    photo.image.seek(0)
                    
                    # Erstelle Thumbnail
                    thumbnail = create_thumbnail(photo.image)
                    if thumbnail:
                        # Speichere das Thumbnail
                        photo.image_thumbnail.save(thumbnail.name, thumbnail, save=True)
                        logger.info(f"Thumbnail erfolgreich erstellt für Photo ID: {photo.id}")
                    else:
                        logger.warning(f"Konnte kein Thumbnail erstellen für Photo ID: {photo.id}")
                        
            except Exception as e:
                logger.error(f"Fehler beim Generieren von Lazy/Thumbnail Images für Photo ID {photo.id}: {str(e)}")
                # Trotzdem das Foto zur Liste hinzufügen, auch wenn Lazy Image fehlt
                pass
        else:
            logger.warning(f"Bild nicht gefunden: {photo.image.name} (ID: {photo.id})")
    
    # Prepare photo data for JavaScript
    json_photo = {}
    for photo in photos:
        photo_dict = {}
        photo_dict["title"] = photo.title
        photo_dict["description"] = photo.description
        photo_dict["image"] = photo.image.url
        if photo.copyright_by:
            photo_dict["copyright_by"] = photo.copyright_by
        json_photo[photo.id] = photo_dict

    gallery_json_data = json.dumps(json_photo)

    context = {
        'gallery_json_data': gallery_json_data,
        'photos': photos,
        'show_all_mode': True,  # Neue Flag für "Alle Bilder" Modus
    }
    return render(request, 'gallery/gallery.html', context)
