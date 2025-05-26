from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import BlogPost
from PIL import Image
import logging

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=BlogPost)
def optimize_blog_image_on_save(sender, instance, **kwargs):
    """
    Signal handler für Bildoptimierung - läuft vor dem Speichern
    Verhindert Rekursion und Duplikate
    """
    # Skip if we're already processing this instance
    if getattr(instance, '_signal_processing', False):
        return
    
    # Skip if no image
    if not instance.image:
        return
    
    # Check if this is a new image upload
    needs_optimization = False
    
    try:
        if instance.pk:
            # Existing instance - check if image changed
            old_instance = BlogPost.objects.get(pk=instance.pk)
            if old_instance.image != instance.image:
                needs_optimization = True
        else:
            # New instance with image
            needs_optimization = True
            
    except BlogPost.DoesNotExist:
        # New instance
        needs_optimization = True
    
    if needs_optimization and hasattr(instance.image, 'path'):
        try:
            # Mark as processing to prevent recursion
            instance._signal_processing = True
            
            # Get image dimensions and optimize if needed
            with Image.open(instance.image.path) as img:
                instance.image_width, instance.image_height = img.size
                
                # Set default focus points if not set
                if instance.image_focus_x is None:
                    instance.image_focus_x = 0.5
                if instance.image_focus_y is None:
                    instance.image_focus_y = 0.5
                
                logger.info(f"Optimized image for {instance.title}: {img.size}")
                
        except Exception as e:
            logger.error(f"Image optimization failed for {instance.title}: {e}")
        finally:
            # Always remove the processing flag
            instance._signal_processing = False

@receiver(post_save, sender=BlogPost)
def log_blog_post_save(sender, instance, created, **kwargs):
    """
    Signal handler zum Logging von Blog-Post Speicherungen
    """
    action = "erstellt" if created else "aktualisiert"
    logger.info(f"Blog-Post '{instance.title}' wurde {action} (ID: {instance.pk})")
