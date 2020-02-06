from ckeditor.widgets import CKEditorWidget
from django.utils.translation import gettext as _
from django import forms
from .models import Author, BlogPost

class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = BlogPost
        fields = ['content', 'image', 'title', 'lead_paragraph']
