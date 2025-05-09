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
    # Try to get category from URL parameter
    category_id = request.GET.get('category')
    
    # Check if categories exist
    categories = PhotoCategory.objects.all().exclude(title="E-Learning")
    
    if not categories.exists():
        # No categories exist, show empty gallery
        return render(request, 'gallery/gallery.html', {
            'gallery_json_data': json.dumps({}),
            'category': [],
            'photos': [],
            'category_id': None,
            'no_categories': True
        })
    
    if category_id:
        # Use provided category ID
        try:
            category_id = int(category_id)
            # Verify this category exists
            if not PhotoCategory.objects.filter(id=category_id).exists():
                category_id = None
        except (ValueError, TypeError):
            category_id = None
    
    if not category_id:
        # If no valid category ID is provided, try to use category with ID 1 first
        if PhotoCategory.objects.filter(id=1).exists():
            category_id = 1
        else:
            # Otherwise use the first category ordered by 'ordering'
            category_id = categories.order_by('ordering').first().id
    
    # Get photos for the selected category
    all_photos = Photo.objects.filter(category_id=category_id)
    
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
        'category': categories,
        'photos': photos,
        'category_id': category_id,
    }
    return render(request, 'gallery/gallery.html', context)
