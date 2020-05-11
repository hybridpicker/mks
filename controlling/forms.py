from ckeditor.widgets import CKEditorWidget
from django.utils.translation import gettext as _
from django import forms
from home.models import IndexText

class IndexForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = IndexText
        fields = ['content', 'lead_paragraph']
