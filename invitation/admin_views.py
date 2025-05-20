# admin_views.py - Admin-spezifische Views für Anmeldungen

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, F, Value, IntegerField, ExpressionWrapper
from collections import defaultdict
from datetime import datetime

from .models import Invitation
from .forms import InvitationForm

# Try to import Event model, create a simple fallback if not available
try:
    from events.models import Event
except ImportError:
    # Fallback: create a simple Event class
    class Event:
        @classmethod
        def objects(cls):
            return cls
        
        @classmethod
        def filter(cls, **kwargs):
            return []
        
        @classmethod
        def all(cls):
            return []


def is_admin_or_office(user):
    """Check if user is admin or has office role"""
    return (user.is_superuser or 
            user.is_staff or 
            hasattr(user, 'role') and user.role in ['admin', 'office'])


@login_required(login_url='/team/login/')
@user_passes_test(is_admin_or_office)
def invitation_admin_dashboard(request):
    """Admin Dashboard für alle Event-Anmeldungen"""
    
    try:
        # Versuche mit Event-Beziehung zu arbeiten (neue Implementation)
        events_with_invitations = Event.objects.filter(
            invitation__isnull=False
        ).distinct().order_by('-date')
        
        # Statistiken für jedes Event
        event_stats = []
        for event in events_with_invitations:
            invitations = Invitation.objects.filter(event=event)
            total_persons = invitations.aggregate(
                total=Sum(ExpressionWrapper(F('number_of_guests') + Value(1), output_field=IntegerField()))
            )['total'] or 0
            
            event_stats.append({
                'event': event,
                'invitation_count': invitations.count(),
                'total_persons': total_persons,
            })
    
    except Exception:
        # Fallback für Legacy-System (alte Implementation)
        # Alle einzigartigen Event-Daten aus Invitations
        unique_event_dates = Invitation.objects.values('event_date', 'event_name').distinct().order_by('-event_date')
        
        # Statistiken für jedes Event
        event_stats = []
        for event_info in unique_event_dates:
            if event_info['event_date']:
                invitations = Invitation.objects.filter(
                    event_date=event_info['event_date'],
                    event_name=event_info['event_name']
                )
                total_persons = invitations.aggregate(
                    total=Sum(ExpressionWrapper(F('number_of_guests') + Value(1), output_field=IntegerField()))
                )['total'] or 0
                
                # Create a pseudo-event object for template compatibility
                pseudo_event = type('Event', (), {
                    'id': hash(str(event_info['event_date']) + event_info['event_name']),
                    'name': event_info['event_name'],
                    'title': event_info['event_name'],
                    'date': event_info['event_date'],
                    'venue': 'Siehe Anmeldungsdetails'
                })()
                
                event_stats.append({
                    'event': pseudo_event,
                    'invitation_count': invitations.count(),
                    'total_persons': total_persons,
                })
    
    # Alle verfügbaren Events (für Event-Erstellung Link)
    try:
        all_events = Event.objects.filter(date__gte=datetime.now().date()).order_by('date')[:10]
    except:
        all_events = []
    
    # Zusammenfassung
    total_invitations = Invitation.objects.count()
    total_all_persons = Invitation.objects.aggregate(
        total=Sum(ExpressionWrapper(F('number_of_guests') + Value(1), output_field=IntegerField()))
    )['total'] or 0
    
    context = {
        'event_stats': event_stats,
        'all_events': all_events,
        'total_invitations': total_invitations,
        'total_all_persons': total_all_persons,
    }
    
    return render(request, 'invitation/admin/dashboard.html', context)


@login_required(login_url='/team/login/')
@user_passes_test(is_admin_or_office)
def invitation_event_edit(request):
    """Edit-View für alle Anmeldungen mit optionaler Filterung"""
    
    # Optional: Filter by event_date from GET parameter
    event_date_filter = request.GET.get('event_date')
    
    invitations = Invitation.objects.all().order_by('-timestamp')
    
    if event_date_filter:
        try:
            filter_date = datetime.strptime(event_date_filter, '%Y-%m-%d').date()
            # Versuche beide Methoden: event_date und event-Beziehung
            try:
                invitations = invitations.filter(event__date=filter_date)
            except:
                invitations = invitations.filter(event_date__date=filter_date)
        except ValueError:
            pass
    
    # Suchfunktion
    search_query = request.GET.get('search', '')
    if search_query:
        try:
            # Versuche mit Event-Name zu suchen (neue Implementation)
            invitations = invitations.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(event__name__icontains=search_query)
            )
        except:
            # Fallback ohne Event-Beziehung (Legacy)
            invitations = invitations.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(event_name__icontains=search_query)
            )
    
    # Pagination
    paginator = Paginator(invitations, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistiken
    total_persons = invitations.aggregate(
        total=Sum(ExpressionWrapper(F('number_of_guests') + Value(1), output_field=IntegerField()))
    )['total'] or 0
    
    context = {
        'event': None,  # No specific event
        'invitations': page_obj,
        'total_invitations': invitations.count(),
        'total_persons': total_persons,
        'search_query': search_query,
        'event_date_filter': event_date_filter,
    }
    
    return render(request, 'invitation/admin/event_edit.html', context)


@login_required(login_url='/team/login/')
@user_passes_test(is_admin_or_office)
def invitation_detail_edit(request, invitation_id):
    """Einzelne Anmeldung bearbeiten"""
    
    invitation = get_object_or_404(Invitation, id=invitation_id)
    
    if request.method == 'POST':
        # Manual form handling da wir keine ModelForm verwenden
        if 'delete' in request.POST:
            invitation.delete()
            messages.success(request, 'Anmeldung wurde gelöscht')
            return redirect('invitation:admin_dashboard')
        else:
            # Update fields
            invitation.name = request.POST.get('name', invitation.name)
            invitation.email = request.POST.get('email', invitation.email)
            invitation.number_of_guests = int(request.POST.get('number_of_guests', 0))
            invitation.save()
            messages.success(request, 'Anmeldung wurde aktualisiert')
            return redirect('invitation:admin_dashboard')
    
    context = {
        'invitation': invitation,
    }
    
    return render(request, 'invitation/admin/detail_edit.html', context)


@login_required(login_url='/team/login/')
@user_passes_test(is_admin_or_office)
def invitation_create(request):
    """Neue Anmeldung erstellen"""
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        event_date_str = request.POST.get('event_date')
        event_name = request.POST.get('event_name', 'Die Hexe Rabaukel bekommt Weihnachtspost')
        number_of_guests = int(request.POST.get('number_of_guests', 0))
        
        # Parse event date
        event_date = datetime.strptime(event_date_str, '%Y-%m-%d %H:%M')
        
        # Create invitation
        invitation = Invitation.objects.create(
            name=name,
            email=email,
            event_date=event_date,
            event_name=event_name,
            number_of_guests=number_of_guests
        )
        
        messages.success(request, 'Anmeldung wurde erstellt')
        return redirect('invitation:admin_dashboard')
    
    # Predefined event dates (same as in original views.py)
    EVENT_CHOICES = [
        ('2024-12-18 18:00', '18. Dezember 2024 um 18:00 Uhr'),
        ('2024-12-19 18:00', '19. Dezember 2024 um 18:00 Uhr'),
    ]
    
    # Convert to format expected by template
    events = []
    for date_str, label in EVENT_CHOICES:
        events.append({
            'date_str': date_str,
            'title': f"Die Hexe Rabaukel - {label}",
            'date': datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        })
    
    context = {
        'events': events,
        'event_choices': EVENT_CHOICES,
    }
    
    return render(request, 'invitation/admin/create.html', context)
