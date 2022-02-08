from django.utils.translation import gettext as _
from django import forms
from faq.models import FAQ

class FaqForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']