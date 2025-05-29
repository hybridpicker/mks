"""
Middleware für automatische Lazy Image Generierung
Diese Middleware kann in settings.py aktiviert werden
"""
import logging
from django.utils.deprecation import MiddlewareMixin
from gallery.models import Photo
from gallery.lazy_image_generator import generate_missing_images_async
import os
from django.conf import settings

logger = logging.getLogger(__name__)

class LazyImageGeneratorMiddleware(MiddlewareMixin):
    """
    Middleware die periodisch prüft ob Lazy Images fehlen und diese generiert
    """
    
    # Counter um nicht bei jedem Request zu prüfen
    request_counter = 0
    CHECK_INTERVAL = 100  # Prüfe alle 100 Requests
    
    def process_request(self, request):
        # Nur auf Gallery-Seiten aktiv
        if '/gallery' not in request.path:
            return None
            
        self.request_counter += 1
        
        # Prüfe nur periodisch
        if self.request_counter % self.CHECK_INTERVAL != 0:
            return None
            
        try:
            # Finde Photos ohne Lazy Images
            photos_needing_lazy = []
            
            photos = Photo.objects.filter(
                image_lazy__isnull=True
            ).exclude(image__isnull=True)[:10]  # Limitiere auf 10 pro Durchgang
            
            for photo in photos:
                image_path = os.path.join(settings.MEDIA_ROOT, photo.image.name)
                if os.path.exists(image_path):
                    photos_needing_lazy.append(photo.id)
            
            if photos_needing_lazy:
                logger.info(f"Middleware: Generiere Lazy Images für {len(photos_needing_lazy)} Fotos")
                generate_missing_images_async(photos_needing_lazy)
                
        except Exception as e:
            logger.error(f"Fehler in LazyImageGeneratorMiddleware: {str(e)}")
        
        return None