# forms.py

from django import forms
from .models import Invitation
from events.models import Event
from datetime import datetime
from django.db.models import Sum, F, Value, IntegerField, ExpressionWrapper

class InvitationForm(forms.ModelForm):
    event = forms.ChoiceField(
        choices=[],  # Choices werden in __init__ gesetzt
        label='Event wählen*',
        widget=forms.RadioSelect(),
    )

    number_of_guests = forms.IntegerField(
        min_value=0,
        max_value=5,
        initial=0,
        label='Anzahl der Begleitpersonen',
        required=False,
        help_text='Wie viele Personen begleiten Sie? (Maximal 5)'
    )

    def __init__(self, *args, **kwargs):
        available_events = kwargs.pop('available_events', [])
        super().__init__(*args, **kwargs)
        
        # Erstelle Choices für verfügbare Events
        event_choices = []
        for event_info in available_events:
            event = event_info['event']
            remaining = event_info['remaining_spots']
            date_str = event.date.strftime('%d.%m.%Y')
            time_str = event.time.strftime('%H:%M') if event.time else '18:00'
            
            choice_label = f"{event.name} - {date_str} um {time_str} ({remaining} Plätze frei)"
            event_choices.append((event.id, choice_label))
        
        self.fields['event'].choices = event_choices
        
        # Wenn keine Events verfügbar sind
        if not event_choices:
            self.fields['event'].choices = [('', 'Keine Events verfügbar')]
            self.fields['event'].widget.attrs['disabled'] = True

    class Meta:
        model = Invitation
        fields = ['name', 'email', 'event', 'number_of_guests']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ihr vollständiger Name',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Ihre E-Mail-Adresse',
                'class': 'form-control'
            }),
        }
        
    def clean_event(self):
        event_id = self.cleaned_data['event']
        if not event_id:
            raise forms.ValidationError("Bitte wählen Sie ein Event aus.")
        
        try:
            event = Event.objects.get(id=event_id)
            return event_id
        except Event.DoesNotExist:
            raise forms.ValidationError("Das gewählte Event existiert nicht.")
    
    def clean_number_of_guests(self):
        number_of_guests = self.cleaned_data.get('number_of_guests', 0)
        if number_of_guests is None:
            number_of_guests = 0
        
        if number_of_guests < 0:
            raise forms.ValidationError("Die Anzahl der Begleitpersonen kann nicht negativ sein.")
        
        return number_of_guests
    
    def clean(self):
        cleaned_data = super().clean()
        event_id = cleaned_data.get('event')
        number_of_guests = cleaned_data.get('number_of_guests', 0)
        
        if event_id:
            try:
                event = Event.objects.get(id=event_id)
                # Prüfe aktuelle Belegung
                current_registrations = Invitation.objects.filter(event=event).aggregate(
                    total=Sum(ExpressionWrapper(F('number_of_guests') + Value(1), output_field=IntegerField()))
                )['total'] or 0
                
                new_total = current_registrations + 1 + number_of_guests
                if new_total > 50:
                    raise forms.ValidationError(
                        f"Für dieses Event sind nur noch {50 - current_registrations} Plätze verfügbar. "
                        f"Sie können maximal {max(0, 50 - current_registrations - 1)} Begleitpersonen anmelden."
                    )
            except Event.DoesNotExist:
                pass  # Error bereits in clean_event behandelt
        
        return cleaned_data
