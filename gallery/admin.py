from django.contrib import admin
from .models import Photo, PhotoCategory
from gallery.image_utils import process_uploaded_image
import logging

logger = logging.getLogger(__name__)

# Register your models here.

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'ordering', 'has_lazy_image', 'has_thumbnail']
    list_filter = ['category']
    search_fields = ['title', 'description']
    
    def has_lazy_image(self, obj):
        return bool(obj.image_lazy)
    has_lazy_image.boolean = True
    has_lazy_image.short_description = 'Lazy Image'
    
    def has_thumbnail(self, obj):
        return bool(obj.image_thumbnail)
    has_thumbnail.boolean = True
    has_thumbnail.short_description = 'Thumbnail'
    
    def save_model(self, request, obj, form, change):
        # Automatische Bildverarbeitung bei neuen Uploads
        if 'image' in form.changed_data and obj.image:
            try:
                logger.info(f"Verarbeite Upload für Photo: {obj.title}")
                
                # Verarbeite das hochgeladene Bild
                processed = process_uploaded_image(obj.image)
                
                if processed['main']:
                    obj.image = processed['main']
                    logger.info("Hauptbild verarbeitet")
                
                if processed['thumbnail']:
                    obj.image_thumbnail = processed['thumbnail']
                    logger.info("Thumbnail erstellt")
                
                if processed['lazy']:
                    obj.image_lazy = processed['lazy']
                    logger.info("Lazy Image erstellt")
                    
            except Exception as e:
                logger.error(f"Fehler bei Bildverarbeitung: {str(e)}")
                # Trotzdem speichern, aber ohne optimierte Versionen
        
        super().save_model(request, obj, form, change)

admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoCategory)