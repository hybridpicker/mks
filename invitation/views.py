from django.shortcuts import render, redirect
from .forms import InvitationForm
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from .models import Invitation


def invitation_view(request):
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save()
            event_date = invitation.event_date  # Zugriff auf das Feld aus der Modellinstanz
            return render(request, 'invitation/thank_you.html', {'event_date': event_date})
    else:
        form = InvitationForm()
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
        print(f"Name: {invitation.name}, Event Date: {invitation.event_date}, Timestamp: {invitation.timestamp}")

    # Gruppierung nach `event_date`
    invitations_by_date = defaultdict(list)

    for invitation in invitations:
        if invitation.event_date:  # Nur Einträge mit gültigem Datum
            event_date = invitation.event_date.date()
            invitations_by_date[event_date].append(invitation)

    # Debugging: Gruppierte Einladungen anzeigen
    print("Grouped Invitations:", dict(invitations_by_date))

    context = {
        'invitations_by_date': dict(invitations_by_date),
        'total_count': invitations.count(),
    }
    return render(request, 'invitation/invitation_list.html', context)