from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect

from django.template import RequestContext
from school.models import MusicSchool
from events.models import Event
from events.forms import EventForm
from .forms import CustomUserCreationForm
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/team/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password_success')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {
        'form': form
    })

@login_required(login_url='/team/login/')
def change_password_success(request):
    return render(request, 'registration/password_change_success.html',)

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class HomePageView(TemplateView):
    template_name = 'users/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Echte Statistiken aus der Datenbank laden
        from teaching.models import Teacher
        from teaching.subject import Subject, SubjectCategory
        
        # Lehrer-Anzahl
        total_teachers = Teacher.objects.count()
        
        # Aktive Instrumente/Fächer
        total_subjects = Subject.objects.filter(hidden_subject=False).count()
        
        # Versuche Schüler-Anzahl zu laden (falls vorhanden)
        try:
            from students.models import Student
            total_students = Student.objects.count()
        except ImportError:
            total_students = "250+"  # Fallback
        
        # Events-Anzahl
        try:
            total_events = Event.objects.count()
        except:
            total_events = 0
        
        context.update({
            'stats': {
                'teachers': total_teachers,
                'subjects': total_subjects,
                'students': total_students,
                'events': total_events,
            }
        })
        
        return context

# Create your views here.

@login_required(login_url='/team/login/')
def eventView(request):
    events = Event.objects.all().order_by('-date')
    edit_event = None
    
    # Löschen einer Veranstaltung
    try:
        if 'delete_id' in request.GET:
            event_id = request.GET['delete_id']
            Event.objects.filter(id=event_id).delete()
            messages.success(request, 'Veranstaltung erfolgreich gelöscht!')
            return redirect('event_managing_view')
    except Exception as e:
        messages.error(request, f'Fehler beim Löschen der Veranstaltung: {str(e)}')
    
    # Bearbeiten einer Veranstaltung - Event zum Bearbeiten laden
    if 'edit_id' in request.GET:
        try:
            edit_id = request.GET['edit_id']
            edit_event = Event.objects.get(id=edit_id)
        except Event.DoesNotExist:
            messages.error(request, 'Die gewählte Veranstaltung existiert nicht.')
            return redirect('event_managing_view')
    
    # Formular verarbeiten (entweder neues Event erstellen oder bestehendes aktualisieren)
    if request.method == 'POST':
        # Event aktualisieren
        if 'event_id' in request.POST and request.POST['event_id']:
            try:
                event_id = request.POST['event_id']
                event = Event.objects.get(id=event_id)
                
                # Formularfelder aktualisieren
                event.name = request.POST['name']
                event.venue = request.POST['venue']
                event.date = request.POST['date']
                event.time = request.POST['time']
                event.link = request.POST.get('link', '')
                
                # Projekt-Zuordnung
                project_id = request.POST.get('project')
                if project_id:
                    event.project_id = project_id
                else:
                    event.project = None
                
                # Prüfen, ob ein neues Bild hochgeladen wurde
                if 'image' in request.FILES:
                    event.image = request.FILES['image']
                
                event.save()
                messages.success(request, 'Veranstaltung erfolgreich aktualisiert!')
                return redirect('event_managing_view')
            except Exception as e:
                messages.error(request, f'Fehler beim Aktualisieren der Veranstaltung: {str(e)}')
        
        # Neues Event erstellen
        else:
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                name = request.POST['name']
                venue = request.POST['venue']
                date = request.POST['date']
                time = request.POST['time']
                link = request.POST.get('link', '')
                
                # Projekt-Zuordnung
                project_id = request.POST.get('project')
                project = None
                if project_id:
                    try:
                        from projects.models import Project
                        project = Project.objects.get(id=project_id)
                    except Project.DoesNotExist:
                        pass
                
                # Prüfen, ob ein Bild hochgeladen wurde
                if 'image' not in request.FILES:
                    messages.error(request, 'Bitte laden Sie ein Bild für diese Veranstaltung hoch.')
                    context = {
                        'events': events,
                        'form': form,
                        'edit_event': edit_event,
                    }
                    return render(request, 'users/events.html', context)
                    
                image = request.FILES['image']
                
                new_event = Event(
                    name=name,
                    venue=venue,
                    date=date,
                    time=time,
                    link=link,
                    project=project,
                    image=image
                )
                new_event.save()
                messages.success(request, 'Veranstaltung erfolgreich erstellt!')
                return redirect('event_managing_view')
    else:
        form = EventForm()
    
    # Projekte für Dropdown laden
    try:
        from projects.models import Project
        projects = Project.objects.all()
    except:
        projects = []
    
    context = {
        'events': events,
        'form': form,
        'edit_event': edit_event,
        'projects': projects,
    }
    return render(request, 'users/events.html', context)

# Team View - Updated to use real database data
@login_required(login_url='/team/login/')
def team_view(request):
    """Modern Team View for Musikschule St. Pölten - Using real database data"""
    from teaching.models import Teacher
    from teaching.subject import Subject, SubjectCategory
    
    # Echte Lehrer aus der Datenbank laden
    teachers = Teacher.objects.select_related('gender', 'academic_title').prefetch_related('subject', 'subject_coordinator').all()
    
    # Team-Mitglieder für das Template vorbereiten
    team_members = []
    for teacher in teachers:
        # Vollständiger Name mit akademischem Titel
        full_name = ""
        if teacher.academic_title:
            full_name += f"{teacher.academic_title} "
        full_name += f"{teacher.first_name} {teacher.last_name}"
        
        # Initialen erstellen
        initials = f"{teacher.first_name[0] if teacher.first_name else ''}{teacher.last_name[0] if teacher.last_name else ''}"
        
        # Fächer sammeln
        subjects = [subject.subject for subject in teacher.subject.all()]
        coordinator_subjects = [cat.name for cat in teacher.subject_coordinator.all()]
        all_skills = subjects + coordinator_subjects
        
        # Rolle bestimmen (basierend auf Koordinatorfunktion oder erstem Fach)
        role = "Lehrkraft"
        if coordinator_subjects:
            role = f"{coordinator_subjects[0]}-Koordination"
        elif subjects:
            role = f"{subjects[0]}-Lehrer"
        
        # Bio oder Standard-Beschreibung
        description = teacher.bio if teacher.bio else f"Qualifizierte Lehrkraft für {', '.join(subjects[:2])}."
        
        # Team-Mitglied-Dictionary erstellen
        team_member = {
            'name': full_name,
            'role': role,
            'description': description,
            'skills': all_skills[:6],  # Max 6 Skills für bessere Darstellung
            'email': teacher.email if teacher.email else 'info@musikschule-stpoelten.at',
            'initials': initials,
            'image': teacher.image.url if teacher.image else None,
            'phone': str(teacher.phone) if teacher.phone else None,
            'homepage': teacher.homepage if teacher.homepage else None,
        }
        team_members.append(team_member)
    
    # Statistiken basierend auf echten Daten
    total_teachers = teachers.count()
    total_subjects = Subject.objects.filter(hidden_subject=False).count()
    # Student-Count - falls Sie ein Student-Model haben
    try:
        from students.models import Student
        total_students = Student.objects.count()
    except ImportError:
        total_students = "250+"  # Fallback
    
    stats = {
        'teachers': total_teachers,
        'instruments': total_subjects,
        'students': total_students,
    }
    
    context = {
        'team_members': team_members,
        'stats': stats,
        'user': request.user,
    }
    
    return render(request, 'users/team.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import CustomUser, UserRole
from .forms import UserRoleForm, UserEditForm
import json

def superuser_required(user):
    return user.is_superuser

@login_required(login_url='/team/login/')
@user_passes_test(superuser_required)
def user_management(request):
    """User management dashboard for superusers"""
    users = CustomUser.objects.all().select_related('user_role').order_by('last_name', 'first_name')
    roles = UserRole.objects.filter(is_active=True).order_by('name')
    
    context = {
        'users': users,
        'roles': roles,
        'total_users': users.count(),
        'total_roles': roles.count(),
        'active_users': users.filter(is_active=True).count(),
    }
    
    return render(request, 'users/user_management.html', context)

@login_required(login_url='/team/login/')
@user_passes_test(superuser_required)
def role_management(request):
    """Role management dashboard for superusers"""
    roles = UserRole.objects.all().order_by('name')
    
    context = {
        'roles': roles,
        'total_roles': roles.count(),
        'active_roles': roles.filter(is_active=True).count(),
    }
    
    return render(request, 'users/role_management.html', context)

@login_required(login_url='/team/login/')
@user_passes_test(superuser_required)
def create_role(request):
    """Create a new user role"""
    if request.method == 'POST':
        form = UserRoleForm(request.POST)
        if form.is_valid():
            role = form.save()
            messages.success(request, f'Rolle "{role.name}" wurde erfolgreich erstellt.')
            return redirect('users:role_management')
    else:
        form = UserRoleForm()
    
    context = {'form': form, 'action': 'Erstellen'}
    return render(request, 'users/role_form.html', context)

@login_required(login_url='/team/login/')
@user_passes_test(superuser_required)
def edit_role(request, role_id):
    """Edit an existing user role"""
    role = get_object_or_404(UserRole, id=role_id)
    
    if request.method == 'POST':
        form = UserRoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, f'Rolle "{role.name}" wurde erfolgreich aktualisiert.')
            return redirect('users:role_management')
    else:
        form = UserRoleForm(instance=role)
    
    context = {'form': form, 'role': role, 'action': 'Bearbeiten'}
    return render(request, 'users/role_form.html', context)

@login_required(login_url='/team/login/')
@user_passes_test(superuser_required)
def delete_role(request, role_id):
    """Delete a user role"""
    role = get_object_or_404(UserRole, id=role_id)
    
    if request.method == 'POST':
        # Check if role is in use
        users_with_role = CustomUser.objects.filter(user_role=role).count()
        if users_with_role > 0:
            messages.error(request, f'Rolle "{role.name}" kann nicht gelöscht werden, da sie von {users_with_role} Benutzer(n) verwendet wird.')
        else:
            role_name = role.name
            role.delete()
            messages.success(request, f'Rolle "{role_name}" wurde erfolgreich gelöscht.')
        return redirect('users:role_management')
    
    context = {'role': role}
    return render(request, 'users/role_confirm_delete.html', context)

@login_required(login_url='/team/login/')
@user_passes_test(superuser_required)
def edit_user(request, user_id):
    """Edit user details and role assignment"""
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Benutzer "{user.get_full_name()}" wurde erfolgreich aktualisiert.')
            return redirect('users:user_management')
    else:
        form = UserEditForm(instance=user)
    
    context = {'form': form, 'user': user}
    return render(request, 'users/user_edit.html', context)

@login_required(login_url='/team/login/')
@user_passes_test(superuser_required)
@require_http_methods(["POST"])
def toggle_user_status(request, user_id):
    """Toggle user active/inactive status"""
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Prevent deactivating yourself
    if user == request.user:
        return JsonResponse({'error': 'Sie können sich nicht selbst deaktivieren.'}, status=400)
    
    user.is_active = not user.is_active
    user.save()
    
    status = 'aktiviert' if user.is_active else 'deaktiviert'
    messages.success(request, f'Benutzer "{user.get_full_name()}" wurde {status}.')
    
    return JsonResponse({'success': True, 'is_active': user.is_active})

@login_required(login_url='/team/login/')
@user_passes_test(superuser_required)
@require_http_methods(["POST"])
def toggle_role_status(request, role_id):
    """Toggle role active/inactive status"""
    role = get_object_or_404(UserRole, id=role_id)
    
    role.is_active = not role.is_active
    role.save()
    
    status = 'aktiviert' if role.is_active else 'deaktiviert'
    messages.success(request, f'Rolle "{role.name}" wurde {status}.')
    
    return JsonResponse({'success': True, 'is_active': role.is_active})

@login_required(login_url='/team/login/')
@user_passes_test(superuser_required)
def role_permissions(request, role_id):
    """View detailed permissions for a role"""
    role = get_object_or_404(UserRole, id=role_id)
    users_with_role = CustomUser.objects.filter(user_role=role).count()
    
    # Group permissions by category
    permissions = {
        'Schüler-Verwaltung': [
            ('can_view_students', 'Schüler anzeigen', role.can_view_students),
            ('can_edit_students', 'Schüler bearbeiten', role.can_edit_students),
            ('can_delete_students', 'Schüler löschen', role.can_delete_students),
        ],
        'Lehrkräfte-Verwaltung': [
            ('can_view_teachers', 'Lehrkräfte anzeigen', role.can_view_teachers),
            ('can_edit_teachers', 'Lehrkräfte bearbeiten', role.can_edit_teachers),
            ('can_delete_teachers', 'Lehrkräfte löschen', role.can_delete_teachers),
        ],
        'Veranstaltungen': [
            ('can_view_events', 'Veranstaltungen anzeigen', role.can_view_events),
            ('can_edit_events', 'Veranstaltungen bearbeiten', role.can_edit_events),
            ('can_delete_events', 'Veranstaltungen löschen', role.can_delete_events),
        ],
        'Galerie': [
            ('can_view_gallery', 'Galerie anzeigen', role.can_view_gallery),
            ('can_edit_gallery', 'Galerie bearbeiten', role.can_edit_gallery),
            ('can_delete_gallery', 'Galerie löschen', role.can_delete_gallery),
        ],
        'System': [
            ('can_view_controlling', 'Controlling anzeigen', role.can_view_controlling),
            ('can_export_data', 'Daten exportieren', role.can_export_data),
            ('can_manage_users', 'Benutzer verwalten', role.can_manage_users),
            ('can_manage_roles', 'Rollen verwalten', role.can_manage_roles),
        ],
    }
    
    context = {
        'role': role,
        'permissions': permissions,
        'users_with_role': users_with_role,
    }
    
    return render(request, 'users/role_permissions.html', context)



@login_required
def user_profile(request):
    """User profile page with optional 2FA settings"""
    from django.utils.translation import gettext as _
    
    user = request.user
    
    # Ensure user has all necessary attributes
    backup_codes_count = 0
    try:
        if hasattr(user, 'backup_codes') and user.backup_codes:
            backup_codes_count = len(user.backup_codes)
    except:
        pass
    
    # Check 2FA status safely
    is_2fa_enabled = False
    try:
        is_2fa_enabled = getattr(user, 'is_2fa_enabled', False)
    except:
        pass
    
    context = {
        'user': user,
        'is_2fa_enabled': is_2fa_enabled,
        'backup_codes_count': backup_codes_count,
        'show_2fa_info': True,  # Show 2FA as optional feature
    }
    
    return render(request, 'users/profile.html', context)


@login_required  
def user_security_settings(request):
    """Security settings page with optional 2FA"""
    from django.utils.translation import gettext as _
    
    user = request.user
    
    # Ensure user has all necessary attributes
    backup_codes_count = 0
    try:
        if hasattr(user, 'backup_codes') and user.backup_codes:
            backup_codes_count = len(user.backup_codes)
    except:
        pass
    
    # Check 2FA status safely
    is_2fa_enabled = False
    try:
        is_2fa_enabled = getattr(user, 'is_2fa_enabled', False)
    except:
        pass
    
    context = {
        'user': user,
        'is_2fa_enabled': is_2fa_enabled,
        'backup_codes_count': backup_codes_count,
        'show_2fa_benefits': not is_2fa_enabled,  # Show benefits if not enabled
        'optional_feature': True,  # Mark as optional, not required
    }
    
    # Use team_security template for team security URL
    if request.path.startswith('/team/security/'):
        return render(request, 'users/team_security.html', context)
    else:
        return render(request, 'users/security_settings.html', context)
