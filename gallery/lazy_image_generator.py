"""
Utility functions for automatic lazy image generation in gallery views
"""
import logging
import threading
from django.conf import settings
from gallery.models import Photo
from gallery.image_utils import create_lazy_image, create_thumbnail
import os

logger = logging.getLogger(__name__)

# Cache für bereits verarbeitete Photos in dieser Session
_processed_photos = set()

def process_images_sync(photo_ids):
    """
    Synchrone Version der Bildverarbeitung (für Tests)
    
    Args:
        photo_ids: Liste von Photo IDs die verarbeitet werden sollen
    """
    for photo_id in photo_ids:
        if photo_id in _processed_photos:
            continue
            
        try:
            photo = Photo.objects.get(id=photo_id)
            
            # Prüfe ob das Hauptbild existiert
            if not photo.image:
                continue
                
            image_path = os.path.join(settings.MEDIA_ROOT, photo.image.name)
            if not os.path.exists(image_path):
                logger.warning(f"Sync: Bilddatei nicht gefunden: {image_path}")
                continue
            
            # Generiere Lazy Image wenn nötig
            if not photo.image_lazy or photo.image_lazy.name == 'gallery_lazy_imageDefault.jpg':
                logger.info(f"Sync: Generiere Lazy Image für Photo ID: {photo_id}")
                lazy_image = create_lazy_image(photo.image)
                if lazy_image:
                    photo.image_lazy.save(lazy_image.name, lazy_image, save=True)
                    logger.info(f"Sync: Lazy Image erstellt für Photo ID: {photo_id}")
            
            # Generiere Thumbnail wenn nötig
            if not photo.image_thumbnail or photo.image_thumbnail.name == 'gallery_thumbnail_imageDefault.jpg':
                logger.info(f"Sync: Generiere Thumbnail für Photo ID: {photo_id}")
                photo.image.seek(0)
                thumbnail = create_thumbnail(photo.image)
                if thumbnail:
                    photo.image_thumbnail.save(thumbnail.name, thumbnail, save=True)
                    logger.info(f"Sync: Thumbnail erstellt für Photo ID: {photo_id}")
            
            _processed_photos.add(photo_id)
            
        except Photo.DoesNotExist:
            logger.warning(f"Sync: Photo mit ID {photo_id} nicht gefunden")
        except Exception as e:
            logger.error(f"Sync: Fehler bei Verarbeitung von Photo ID {photo_id}: {str(e)}")

def generate_missing_images_async(photo_ids):
    """
    Generiert fehlende Lazy Images und Thumbnails im Hintergrund
    
    Args:
        photo_ids: Liste von Photo IDs die verarbeitet werden sollen
    """
    def process_images():
        for photo_id in photo_ids:
            if photo_id in _processed_photos:
                continue
                
            try:
                photo = Photo.objects.get(id=photo_id)
                
                # Prüfe ob das Hauptbild existiert
                if not photo.image:
                    continue
                    
                image_path = os.path.join(settings.MEDIA_ROOT, photo.image.name)
                if not os.path.exists(image_path):
                    continue
                
                # Generiere Lazy Image wenn nötig
                if not photo.image_lazy or photo.image_lazy.name == 'gallery_lazy_imageDefault.jpg':
                    logger.info(f"Background: Generiere Lazy Image für Photo ID: {photo_id}")
                    photo.image.open()
                    lazy_image = create_lazy_image(photo.image)
                    if lazy_image:
                        photo.image_lazy.save(lazy_image.name, lazy_image, save=True)
                        logger.info(f"Background: Lazy Image erstellt für Photo ID: {photo_id}")
                
                # Generiere Thumbnail wenn nötig
                if not photo.image_thumbnail or photo.image_thumbnail.name == 'gallery_thumbnail_imageDefault.jpg':
                    logger.info(f"Background: Generiere Thumbnail für Photo ID: {photo_id}")
                    photo.image.seek(0)
                    thumbnail = create_thumbnail(photo.image)
                    if thumbnail:
                        photo.image_thumbnail.save(thumbnail.name, thumbnail, save=True)
                        logger.info(f"Background: Thumbnail erstellt für Photo ID: {photo_id}")
                
                _processed_photos.add(photo_id)
                
            except Exception as e:
                logger.error(f"Background: Fehler bei Photo ID {photo_id}: {str(e)}")
    
    # Starte Verarbeitung im Hintergrund
    thread = threading.Thread(target=process_images)
    thread.daemon = True
    thread.start()

def check_and_generate_lazy_image(photo):
    """
    Prüft und generiert Lazy Image für ein einzelnes Photo synchron
    
    Args:
        photo: Photo Objekt
        
    Returns:
        bool: True wenn erfolgreich oder bereits vorhanden
    """
    try:
        if photo.image_lazy:
            return True
            
        if not photo.image:
            return False
            
        logger.info(f"Generiere Lazy Image für Photo ID: {photo.id}")
        photo.image.open()
        lazy_image = create_lazy_image(photo.image)
        
        if lazy_image:
            photo.image_lazy.save(lazy_image.name, lazy_image, save=True)
            logger.info(f"Lazy Image erstellt für Photo ID: {photo.id}")
            return True
        else:
            logger.warning(f"Konnte kein Lazy Image erstellen für Photo ID: {photo.id}")
            return False
            
    except Exception as e:
        logger.error(f"Fehler beim Generieren von Lazy Image für Photo ID {photo.id}: {str(e)}")
        return False