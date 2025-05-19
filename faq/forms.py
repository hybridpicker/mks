from tinymce.widgets import TinyMCE
from django.utils.translation import gettext as _
from django import forms
from faq.models import FAQ

class FaqForm(forms.ModelForm):
    question = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter the question'),
        }),
        label=_("Question"),
        max_length=500
    )
    
    answer = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 15}),
        label=_("Answer"),
        required=False
    )
    
    ordering = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Order (optional)'),
        }),
        label=_("Display Order"),
        required=False,
        help_text=_("Lower numbers appear first")
    )
    
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'ordering']