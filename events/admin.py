from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.core.exceptions import ValidationError
from .models import Event

# Event-Formularklasse mit benutzerdefinierten Validierungen
class EventAdminForm(forms.ModelForm):
    """
    Custom form for Event model with additional validations
    """
    class Meta:
        model = Event
        fields = '__all__'
    
    def clean_image(self):
        """
        Validate that an image is provided and it's not too large
        """
        image = self.cleaned_data.get('image')
        
        # Check if image is provided
        if not image:
            raise ValidationError(
                "Ein Bild ist erforderlich. Bitte laden Sie ein Bild für diese Veranstaltung hoch."
            )
        
        # Check image size (max 2MB)
        if image and image.size > 2 * 1024 * 1024:
            raise ValidationError(
                "Das Bild ist zu groß. Die maximale Dateigröße beträgt 2MB."
            )
            
        return image

# Admin-Konfiguration für Events
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ('name', 'date', 'time', 'venue', 'show_image')
    list_filter = ('date',)
    search_fields = ('name', 'venue')
    date_hierarchy = 'date'
    
    fieldsets = (
        (None, {
            'fields': ('name', 'date', 'time', 'venue'),
        }),
        ('Medien & Links', {
            'fields': ('image', 'link', 'project'),
            'description': format_html(
                """
                <div style="padding: 10px; background-color: #f8f9fa; border-left: 4px solid #e60000; margin: 10px 0;">
                    <h3 style="margin-top: 0; color: #333;">Bildrichtlinien:</h3>
                    <ul>
                        <li><strong>Erforderlich:</strong> Jede Veranstaltung muss ein Bild haben</li>
                        <li><strong>Optimale Größe:</strong> 800 × 600 Pixel</li>
                        <li><strong>Format:</strong> JPG oder WEBP (empfohlen)</li>
                        <li><strong>Maximale Dateigröße:</strong> 2MB</li>
                        <li><strong>Seitenverhältnis:</strong> 4:3 (Querformat)</li>
                        <li><strong>Auflösung:</strong> 72 dpi ist ausreichend</li>
                    </ul>
                    <p>Bilder werden auf der Startseite und in der Veranstaltungsübersicht angezeigt.</p>
                </div>
                """
            )
        }),
    )
    
    def show_image(self, obj):
        """Display a thumbnail in the admin list view"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px;" />', 
                obj.image.url
            )
        return "Kein Bild"
    show_image.short_description = "Bild"

    def save_model(self, request, obj, form, change):
        """Custom save method to handle image validation"""
        if not obj.image:
            # This is just an extra check - the form validation should already catch this
            from django.contrib import messages
            messages.error(request, "Bitte fügen Sie ein Bild für diese Veranstaltung hinzu.")
            return
        super().save_model(request, obj, form, change)
