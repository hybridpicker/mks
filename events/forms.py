import datetime
from datetime import timedelta
from django import forms
from django.forms import ModelChoiceField
from django.forms import DateTimeField

from django.contrib.admin.widgets import AdminDateWidget

class EventForm(forms.Form):
    INPUT_FORMATS = ['%Y-%m-%d %H:%M']
    INPUT_FORMATS_DAY = ['%Y-%m-%d']
    INPUT_FORMATS_TIME = ['%H:%M']
    name = forms.CharField(max_length=50, required=True)
    venue = forms.CharField(max_length=30, required=False)
    date = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker'}))
    time = forms.TimeField(input_formats=INPUT_FORMATS_TIME, widget=forms.DateTimeInput())
