from django import forms
from .models import Invitation
from datetime import datetime

class InvitationForm(forms.ModelForm):
    EVENT_CHOICES = [
        ('2024-12-17 18:00', '17. Dezember 2024 um 18:00 Uhr'),
        ('2024-12-18 18:00', '18. Dezember 2024 um 18:00 Uhr'),
    ]
    event_date = forms.ChoiceField(
        choices=EVENT_CHOICES,
        label='Wunschtermin*',
        widget=forms.RadioSelect
    )

    class Meta:
        model = Invitation
        fields = ['name', 'email', 'event_date']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ihr Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ihre E-Mail'}),
        }

    def clean_event_date(self):
        event_date_str = self.cleaned_data['event_date']
        # Den ausgewählten String in ein datetime-Objekt umwandeln
        event_date = datetime.strptime(event_date_str, '%Y-%m-%d %H:%M')
        return event_date