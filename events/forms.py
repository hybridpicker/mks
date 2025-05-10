import datetime
from datetime import timedelta
from django import forms
from django.forms import ModelChoiceField
from django.forms import DateTimeField
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import AdminDateWidget
from .models import Event

class EventForm(forms.Form):
    INPUT_FORMATS = ['%Y-%m-%d %H:%M']
    INPUT_FORMATS_DAY = ['%Y-%m-%d']
    INPUT_FORMATS_TIME = ['%H:%M']
    name = forms.CharField(max_length=100, required=True)
    venue = forms.CharField(max_length=80, required=False)
    date = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
    time = forms.TimeField(input_formats=INPUT_FORMATS_TIME, widget=forms.DateTimeInput())
    image = forms.ImageField(
        required=True,
        help_text="Bild für die Veranstaltung. Optimal: 800x600px, max. 2MB."
    )
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if not image:
            raise ValidationError("Ein Bild ist erforderlich.")
            
        # Check image size (max 2MB)
        if image and image.size > 2 * 1024 * 1024:
            raise ValidationError("Das Bild ist zu groß. Die maximale Dateigröße beträgt 2MB.")
            
        return image

class EventModelForm(forms.ModelForm):
    """
    Alternative ModelForm für erweiterte Event-Erstellung
    """
    class Meta:
        model = Event
        fields = ['name', 'venue', 'date', 'time', 'image', 'link']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'timepicker'}),
        }
        help_texts = {
            'image': 'Bild für die Veranstaltung. Optimal: 800x600px, max. 2MB.',
            'link': 'Optional: Link zu weiteren Informationen über die Veranstaltung.',
        }
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if not image:
            raise ValidationError("Ein Bild ist erforderlich.")
            
        # Check image size (max 2MB)
        if image and image.size > 2 * 1024 * 1024:
            raise ValidationError("Das Bild ist zu groß. Die maximale Dateigröße beträgt 2MB.")
            
        return image
