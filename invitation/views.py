# views.py

from django.shortcuts import render
from .forms import InvitationForm
from .models import Invitation
from collections import defaultdict
from django.db.models import Sum, F, Value, IntegerField, ExpressionWrapper  # Sum hinzugefügt
from django.contrib.auth.decorators import login_required
from datetime import datetime

def get_available_event_dates():
    # Definierte Veranstaltungstermine
    EVENT_CHOICES = [
        ('2024-12-17 18:00', '17. Dezember 2024 um 18:00 Uhr'),
        ('2024-12-18 18:00', '18. Dezember 2024 um 18:00 Uhr'),
    ]
    available_dates = []
    for event_date_str, label in EVENT_CHOICES:
        event_date = datetime.strptime(event_date_str, '%Y-%m-%d %H:%M')
        total_registered = Invitation.objects.filter(event_date=event_date).aggregate(
            total_persons=Sum(ExpressionWrapper(F('number_of_guests') + Value(1), output_field=IntegerField()))
        )['total_persons'] or 0
        if total_registered < 50:
            available_dates.append((event_date_str, label))
    return available_dates

def invitation_view(request):
    available_dates = get_available_event_dates()
    if not available_dates:
        return render(request, 'invitation/no_dates_available.html')
    if request.method == 'POST':
        form = InvitationForm(request.POST, available_dates=available_dates)
        if form.is_valid():
            event_date = form.cleaned_data['event_date']  # Bereits ein datetime-Objekt
            number_of_guests = form.cleaned_data['number_of_guests']
            # Verwenden Sie event_date direkt
            event_datetime = event_date
            total_registered = Invitation.objects.filter(event_date=event_datetime).aggregate(
                total_persons=Sum(ExpressionWrapper(F('number_of_guests') + Value(1), output_field=IntegerField()))
            )['total_persons'] or 0
            # Neue Gesamtanzahl nach der aktuellen Anmeldung
            new_total = total_registered + 1 + number_of_guests
            if new_total > 50:
                form.add_error(None, 'Für diesen Veranstaltungstag sind leider keine Plätze mehr verfügbar.')
            else:
                invitation = form.save()
                return render(request, 'invitation/thank_you.html', {'event_date': invitation.event_date})
    else:
        form = InvitationForm(available_dates=available_dates)
    context = {
        'form': form,
    }
    return render(request, 'invitation/invitation_form.html', context)

def thank_you_view(request):
    return render(request, 'invitation/thank_you.html')

@login_required(login_url='/team/login/')
def invitation_list_view(request):
    # Alle Einladungen abrufen und nach Datum sortieren
    invitations = Invitation.objects.all().order_by('event_date', 'timestamp')

    # Debugging: Rohdaten aus der Datenbank anzeigen
    print("Alle Einladungen:")
    for invitation in invitations:
        print(f"Name: {invitation.name}, Event Date: {invitation.event_date}, Timestamp: {invitation.timestamp}, Number of Guests: {invitation.number_of_guests}")

    # Gruppierung nach `event_date`
    invitations_by_date = defaultdict(list)
    total_persons_by_date = defaultdict(int)

    for invitation in invitations:
        if invitation.event_date:
            event_date = invitation.event_date.date()
            invitations_by_date[event_date].append(invitation)
            total_persons = 1 + invitation.number_of_guests
            total_persons_by_date[event_date] += total_persons

    # Gesamtanzahl aller Personen
    total_persons = sum(total_persons_by_date.values())

    context = {
        'invitations_by_date': dict(invitations_by_date),
        'total_count': total_persons,
        'total_persons_by_date': dict(total_persons_by_date),
    }
    return render(request, 'invitation/invitation_list.html', context)
