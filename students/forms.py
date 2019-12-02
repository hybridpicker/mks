from django.utils.translation import gettext as _
from django import forms
from django.forms import ModelChoiceField
from teaching.subject import Subject

class SignInForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    parent_first_name = forms.CharField(max_length=30, required=True)
    parent_last_name = forms.CharField(max_length=30, required=True)
    from_email = forms.EmailField(label="E-Mailadresse", max_length=100, required=True)
    subject = forms.ModelChoiceField(queryset=Subject.objects.all().exclude(
                                     subject='Direktor').exclude(
                                     subject="Sekretariat"))
    adress_line = forms.CharField(label="street", max_length=80, required=True)
    house_number = forms.CharField(label="house_number", max_length=80, required=True)
    postal_code = forms.CharField(label="postal_code", max_length=30, required=True)
    city = forms.CharField(label="city", max_length=30, required=True)
