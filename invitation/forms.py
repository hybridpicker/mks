# forms.py

from django import forms
from .models import Invitation
from datetime import datetime
from django.db.models import Sum, F, Value, IntegerField, ExpressionWrapper

class InvitationForm(forms.ModelForm):
    event_date = forms.ChoiceField(
        choices=[],  # Choices werden in __init__ gesetzt
        label='Wunschtermin*',
        widget=forms.RadioSelect(),
    )

    number_of_guests = forms.IntegerField(
        min_value=0,
        max_value=5,
        initial=0,
        label='Anzahl der Begleitpersonen',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        available_dates = kwargs.pop('available_dates', None)
        super().__init__(*args, **kwargs)
        if available_dates is not None:
            self.fields['event_date'].choices = available_dates
        else:
            self.fields['event_date'].choices = [
                ('2024-12-18 18:00', '18. Dezember 2024 um 18:00 Uhr'),
                ('2024-12-19 18:00', '19. Dezember 2024 um 18:00 Uhr'),
            ]

    class Meta:
        model = Invitation
        fields = ['name', 'email', 'event_date', 'number_of_guests']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ihr Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ihre E-Mail'}),
            # 'event_date' Widget wird im Feld selbst definiert
        }

    def clean_event_date(self):
        event_date_str = self.cleaned_data['event_date']
        # Optional: Validierung der Datumsformatierung
        try:
            datetime.strptime(event_date_str, '%Y-%m-%d %H:%M')
        except ValueError:
            raise forms.ValidationError("Ungültiges Datum.")
        return event_date_str  # Rückgabe als String
    
    def clean_number_of_guests(self):
        number_of_guests = self.cleaned_data.get('number_of_guests', 0)
        if number_of_guests is None:
            number_of_guests = 0
        return number_of_guests
