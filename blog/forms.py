from ckeditor.widgets import CKEditorWidget
from django.utils.translation import gettext as _
from django import forms
from django.utils.text import slugify  # Hinzugefügt
from .models import Author, BlogPost

class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = BlogPost
        fields = ['content', 'image', 'title', 'lead_paragraph', 'slug']

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug != slugify(slug):
            raise forms.ValidationError("Invalid slug format. Only alphanumeric characters, hyphens, and underscores are allowed.")
        return slug