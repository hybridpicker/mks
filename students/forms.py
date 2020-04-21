from django.utils.translation import gettext as _
from django import forms
from django.forms import ModelChoiceField
from teaching.subject import Subject
from datetime import datetime

def get_years_signinform():
    year_now = datetime.now().year
    max_birthyear = year_now - 24
    BIRTH_YEAR_CHOICES = []
    for x in range(max_birthyear, year_now - 1):
        BIRTH_YEAR_CHOICES.append(x)
    return BIRTH_YEAR_CHOICES

class SignInForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    parent_first_name = forms.CharField(max_length=30, required=True)
    parent_last_name = forms.CharField(max_length=30, required=True)
    birthdate = forms.DateField(label='Wie lautet das Geburtsdatum?',
                                widget=forms.SelectDateWidget(years=get_years_signinform()))
    from_email = forms.EmailField(label="E-Mailadresse",
                                  max_length=100,
                                  required=True)
    subject = forms.ModelChoiceField(queryset=Subject.objects.all().order_by('subject').exclude(
                                     subject='Direktor').exclude(
                                     subject="Sekretariat"))
    adress_line = forms.CharField(label="street", max_length=80, required=True)
    house_number = forms.CharField(label="house_number", max_length=80, required=True)
    postal_code = forms.CharField(label="postal_code", max_length=30, required=True)
    city = forms.CharField(label="city", max_length=30, required=True)
