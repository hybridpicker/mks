from django.utils.translation import gettext as _
from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image', 'image_thumbnail', 'description']
