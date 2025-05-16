import json
from django.shortcuts import render, redirect
from gallery.models import Photo, PhotoCategory
import logging
import os
from django.conf import settings

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
