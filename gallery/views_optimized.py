import json
from django.shortcuts import render
from django.core.paginator import Paginator
from gallery.models import Photo
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_GET

logger = logging.getLogger(__name__)

def gallery_view_optimized(request):
    # Basis-Queryset mit select_related für bessere Performance
    photos_queryset = Photo.objects.exclude(
        category__title="E-Learning"
    ).select_related('category').order_by('-ordering')
    
    # Nur die ersten 24 Bilder für initiales Laden
    initial_photos = photos_queryset[:24]
    
    # JSON Daten nur für die initialen Bilder
    json_photo = {}
    for photo in initial_photos:
        if photo.image:
            photo_dict = {
                "title": photo.title,
                "description": photo.description,
                "image": photo.image.url,
            }
            if photo.copyright_by:
                photo_dict["copyright_by"] = photo.copyright_by
            json_photo[photo.id] = photo_dict
    
    gallery_json_data = json.dumps(json_photo)
    
    context = {
        'gallery_json_data': gallery_json_data,
        'photos': initial_photos,
        'total_count': photos_queryset.count(),
        'show_all_mode': True,
    }
    return render(request, 'gallery/gallery_optimized.html', context)

@require_GET
def load_more_photos(request):
    """AJAX Endpoint für das Nachladen weiterer Bilder"""
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 24))
    
    photos = Photo.objects.exclude(
        category__title="E-Learning"
    ).select_related('category').order_by('-ordering')[offset:offset+limit]
    
    photos_data = []
    json_photo = {}
    
    for photo in photos:
        if photo.image:
            photo_data = {
                'id': photo.id,
                'title': photo.title,
                'description': photo.description,
                'image_url': photo.image.url,
                'lazy_url': photo.image_lazy.url if photo.image_lazy else None,
                'is_portrait': photo.image.height > photo.image.width,
                'is_landscape': photo.image.width > photo.image.height,
                'is_square': photo.image.width == photo.image.height,
            }
            if photo.copyright_by:
                photo_data['copyright_by'] = photo.copyright_by
            
            photos_data.append(photo_data)
            
            # Für showImg Funktion
            json_photo[photo.id] = {
                "title": photo.title,
                "description": photo.description,
                "image": photo.image.url,
                "copyright_by": photo.copyright_by if photo.copyright_by else None
            }
    
    return JsonResponse({
        'photos': photos_data,
        'photo_data': json_photo,
        'has_more': offset + limit < Photo.objects.exclude(category__title="E-Learning").count()
    })
