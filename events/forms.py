from django import forms

class EventForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    venue = forms.CharField(max_length=30, required=False)
    date = forms.DateField(input_formats=['%Y-%m-%d'], help_text="JJJJ-MM-DD")
    time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), help_text="hh:mm")
