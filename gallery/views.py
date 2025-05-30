import json
from django.shortcuts import render, redirect
from gallery.models import Photo, PhotoCategory
import logging
import os
import sys
from django.conf import settings
from gallery.image_utils import create_lazy_image, create_thumbnail
from django.core.files.base import ContentFile
from gallery.lazy_image_generator import generate_missing_images_async

# Logger einrichten
logger = logging.getLogger(__name__)

# Create your views here.
def gallery_view(request):
    # Alle Fotos aus allen Kategorien laden (außer von E-Learning)
    all_photos = Photo.objects.exclude(category__title="E-Learning").order_by('-ordering')
    
    # Listen für verschiedene Verarbeitungsschritte
    photos = []
    photos_needing_lazy = []
    
    # Filterung der Fotos und Sammlung der IDs die Lazy Images brauchen
    for photo in all_photos:
        # Prüfen, ob Bilddatei existiert
        image_path = os.path.join(settings.MEDIA_ROOT, photo.image.name)
        if os.path.exists(image_path):
            photos.append(photo)
            
            # Sammle Photos die Lazy Images brauchen
            if photo.image and (
                not photo.image_lazy or photo.image_lazy.name == 'gallery_lazy_imageDefault.jpg' or
                not photo.image_thumbnail or photo.image_thumbnail.name == 'gallery_thumbnail_imageDefault.jpg'
            ):
                photos_needing_lazy.append(photo.id)
        else:
            logger.warning(f"Bild nicht gefunden: {photo.image.name} (ID: {photo.id})")
    
    # Starte asynchrone Generierung im Hintergrund wenn nötig
    if photos_needing_lazy:
        logger.info(f"Starte Hintergrund-Generierung für {len(photos_needing_lazy)} Fotos")
        # Für Tests: Synchrone Verarbeitung wenn 'test' in sys.argv
        is_testing = 'test' in sys.argv
        
        if is_testing:
            # Synchrone Verarbeitung für Tests
            from gallery.lazy_image_generator import process_images_sync
            process_images_sync(photos_needing_lazy)
        else:
            # Asynchrone Verarbeitung für Production
            generate_missing_images_async(photos_needing_lazy)
    
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