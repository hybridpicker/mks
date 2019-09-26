from django.utils.translation import gettext as _
from django import forms
from teaching.lesson_form import LessonForm
from location.models import Location
from teaching.subject import Subject
from students.gender import Gender

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    from_email = forms.EmailField(label="E-Mailadresse", max_length=100, required=True)
    message = forms.CharField(label="Nachricht",widget=forms.Textarea, required=False)
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    location = forms.ModelChoiceField(queryset=Location.objects.all().exclude(location_name='Unterwaltersdorf'))
