# views.py

from django.shortcuts import render, redirect
from .forms import InvitationForm
from .models import Invitation
from events.models import Event
from collections import defaultdict
from django.db.models import Sum, F, Value, IntegerField, ExpressionWrapper  
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

def get_available_events():
    """Gibt verfügbare Events für Anmeldungen zurück"""
    available_events = []
    
    try:
        # Versuche mit Event-Model zu arbeiten (neue Implementation)
        today = datetime.now().date()
        upcoming_events = Event.objects.filter(date__gte=today).order_by('date')
        
        for event in upcoming_events:
            # Prüfe aktuelle Anmeldungen für dieses Event
            try:
                current_registrations = Invitation.objects.filter(event=event)
            except:
                # Fallback: count by event_date if event relationship doesn't exist yet
                event_datetime = datetime.combine(event.date, event.time or datetime.min.time().replace(hour=18))
                current_registrations = Invitation.objects.filter(event_date=event_datetime)
            
            total_persons = current_registrations.aggregate(
                total=Sum(ExpressionWrapper(F('number_of_guests') + Value(1), output_field=IntegerField()))
            )['total'] or 0
            
            # Maximum 50 Personen pro Event (konfigurierbar)
            if total_persons < 50:
                available_events.append({
                    'event': event,
                    'current_registrations': total_persons,
                    'remaining_spots': 50 - total_persons
                })
    
    except Exception as e:
        # Fallback zu Legacy-System
        # Hardcoded event dates for backward compatibility
        EVENT_CHOICES = [
            ('2024-12-18 18:00', '18. Dezember 2024 um 18:00 Uhr', 'Die Hexe Rabaukel bekommt Weihnachtspost'),
            ('2024-12-19 18:00', '19. Dezember 2024 um 18:00 Uhr', 'Die Hexe Rabaukel bekommt Weihnachtspost'),
        ]
        
        for event_date_str, label, event_name in EVENT_CHOICES:
            event_date = datetime.strptime(event_date_str, '%Y-%m-%d %H:%M')
            total_registered = Invitation.objects.filter(event_date=event_date).aggregate(
                total_persons=Sum(ExpressionWrapper(F('number_of_guests') + Value(1), output_field=IntegerField()))
            )['total_persons'] or 0
            
            if total_registered < 50:
                # Create pseudo-event for template compatibility
                pseudo_event = type('Event', (), {
                    'id': f"legacy_{event_date_str.replace(' ', '_').replace(':', '_')}",
                    'name': event_name,
                    'date': event_date.date(),
                    'time': event_date.time(),
                    'venue': "Grillparzercampus Orchestersaal, Grillparzerstraße 17, 3100 St. Pölten"
                })()
                
                available_events.append({
                    'event': pseudo_event,
                    'current_registrations': total_registered,
                    'remaining_spots': 50 - total_registered
                })
    
    return available_events

def invitation_view(request):
    available_events = get_available_events()
    
    if not available_events:
        return render(request, 'invitation/no_dates_available.html')
    
    if request.method == 'POST':
        form = InvitationForm(request.POST, available_events=available_events)
        if form.is_valid():
            event_id = form.cleaned_data['event']
            number_of_guests = form.cleaned_data['number_of_guests']
            
            # Get the selected event
            try:
                selected_event = Event.objects.get(id=event_id)
            except Event.DoesNotExist:
                form.add_error('event', 'Das gewählte Event existiert nicht.')
                return render(request, 'invitation/invitation_form.html', {'form': form})
            
            # Check availability again
            current_registrations = Invitation.objects.filter(event=selected_event).aggregate(
                total=Sum(ExpressionWrapper(F('number_of_guests') + Value(1), output_field=IntegerField()))
            )['total'] or 0
            
            new_total = current_registrations + 1 + number_of_guests
            if new_total > 50:
                form.add_error(None, 'Für dieses Event sind leider keine Plätze mehr verfügbar.')
            else:
                # Create invitation with Event relationship
                invitation = Invitation.objects.create(
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    event=selected_event,
                    number_of_guests=number_of_guests,
                    # Set legacy fields for compatibility
                    event_name=selected_event.name,
                    event_date=datetime.combine(selected_event.date, selected_event.time or datetime.min.time().replace(hour=18)),
                    location=selected_event.venue or "Ort wird noch bekannt gegeben"
                )
                return render(request, 'invitation/thank_you.html', {
                    'event': selected_event,
                    'invitation': invitation
                })
    else:
        form = InvitationForm(available_events=available_events)
    
    context = {
        'form': form,
        'available_events': available_events,
    }
    return render(request, 'invitation/invitation_form.html', context)

def thank_you_view(request):
    return render(request, 'invitation/thank_you.html')

@login_required(login_url='/team/login/')
def invitation_list_view(request):
    # Alle Einladungen abrufen und nach Event sortieren
    invitations = Invitation.objects.all().order_by('event__date', 'timestamp')
    
    # Gruppierung nach Event
    invitations_by_event = defaultdict(list)
    total_persons_by_event = defaultdict(int)
    
    for invitation in invitations:
        if invitation.event:
            event_key = invitation.event
            invitations_by_event[event_key].append(invitation)
            total_persons = 1 + (invitation.number_of_guests or 0)
            total_persons_by_event[event_key] += total_persons
        else:
            # Legacy invitations ohne Event-Beziehung
            legacy_key = f"Legacy: {invitation.get_event_name()}"
            invitations_by_event[legacy_key].append(invitation)
            total_persons = 1 + (invitation.number_of_guests or 0)
            total_persons_by_event[legacy_key] += total_persons
    
    # Gesamtanzahl aller Personen
    total_persons = sum(total_persons_by_event.values())
    
    context = {
        'invitations_by_event': dict(invitations_by_event),
        'total_count': total_persons,
        'total_persons_by_event': dict(total_persons_by_event),
    }
    return render(request, 'invitation/invitation_list.html', context)
