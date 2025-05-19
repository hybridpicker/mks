# user_management_views.py - User Role Management System

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from users.models import CustomUser
from teaching.models import Teacher
from teaching.models import SubjectCategory


def is_admin(user):
    """Check if user is superuser"""
    return user.is_superuser


@login_required(login_url='/team/login/')
@user_passes_test(is_admin)
def user_role_dashboard(request):
    """Dashboard für User Role Management"""
    
    # Statistiken
    total_users = CustomUser.objects.count()
    admin_count = CustomUser.objects.filter(is_superuser=True).count()
    staff_count = CustomUser.objects.filter(is_staff=True, is_superuser=False).count()
    coordinator_count = CustomUser.objects.filter(coordinator=True).count()
    teacher_count = Teacher.objects.exclude(user__isnull=True).count()
    regular_users = total_users - admin_count - staff_count - coordinator_count
    
    # Letzte Aktivitäten (neue Benutzer)
    recent_users = CustomUser.objects.order_by('-date_joined')[:5]
    
    context = {
        'total_users': total_users,
        'admin_count': admin_count,
        'staff_count': staff_count,
        'coordinator_count': coordinator_count,
        'teacher_count': teacher_count,
        'regular_users': regular_users,
        'recent_users': recent_users,
    }
    
    return render(request, 'users/admin/dashboard.html', context)


@login_required(login_url='/team/login/')
@user_passes_test(is_admin)
def user_role_list(request):
    """Liste aller Benutzer mit Rollenverwaltung"""
    
    # Filter
    role_filter = request.GET.get('role', 'all')
    search_query = request.GET.get('search', '')
    
    users = CustomUser.objects.all().order_by('last_name', 'first_name')
    
    # Role filtering
    if role_filter == 'admin':
        users = users.filter(is_superuser=True)
    elif role_filter == 'staff':
        users = users.filter(is_staff=True, is_superuser=False)
    elif role_filter == 'coordinator':
        users = users.filter(coordinator=True)
    elif role_filter == 'teacher':
        users = users.filter(teacher__isnull=False)
    elif role_filter == 'regular':
        users = users.filter(is_staff=False, is_superuser=False, coordinator=False, teacher__isnull=True)
    
    # Search functionality
    if search_query:
        users = users.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Add role information to users
    users_with_roles = []
    for user in users:
        roles = []
        if user.is_superuser:
            roles.append('Administrator')
        if user.is_staff and not user.is_superuser:
            roles.append('Staff')
        if user.coordinator:
            roles.append('Koordinator')
        if hasattr(user, 'teacher'):
            roles.append('Lehrer')
        if not roles:
            roles.append('Benutzer')
        
        users_with_roles.append({
            'user': user,
            'roles': roles,
            'primary_role': roles[0] if roles else 'Benutzer'
        })
    
    # Pagination
    paginator = Paginator(users_with_roles, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
        'role_filter': role_filter,
        'search_query': search_query,
        'total_users': users.count(),
    }
    
    return render(request, 'users/admin/user_list.html', context)


@login_required(login_url='/team/login/')
@user_passes_test(is_admin)
def user_role_edit(request, user_id):
    """Einzelnen Benutzer bearbeiten"""
    
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        # Admin Role
        if 'admin' in request.POST:
            user.is_superuser = True
            user.is_staff = True  # Admins should also be staff
        else:
            user.is_superuser = False
        
        # Staff Role
        if 'staff' in request.POST and not user.is_superuser:
            user.is_staff = True
        elif not user.is_superuser:
            user.is_staff = False
        
        # Coordinator Role
        user.coordinator = 'coordinator' in request.POST
        
        # Basic user info
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.is_active = 'is_active' in request.POST
        
        # Teacher Role handling
        if 'teacher' in request.POST:
            # Check if user already has teacher profile
            if not hasattr(user, 'teacher'):
                # Create teacher profile
                Teacher.objects.create(
                    user=user,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    gender=1  # Default value
                )
        else:
            # Remove teacher profile if exists
            if hasattr(user, 'teacher'):
                user.teacher.delete()
        
        user.save()
        messages.success(request, f'Benutzer {user.get_full_name()} wurde aktualisiert')
        return redirect('users:role_list')
    
    # Get available subject categories for coordinators
    subject_categories = SubjectCategory.objects.all()
    
    # Check if user is a teacher
    is_teacher = hasattr(user, 'teacher')
    
    context = {
        'edit_user': user,
        'subject_categories': subject_categories,
        'is_teacher': is_teacher,
    }
    
    return render(request, 'users/admin/user_edit.html', context)


@login_required(login_url='/team/login/')
@user_passes_test(is_admin)
def user_role_create(request):
    """Neuen Benutzer erstellen"""
    
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Benutzername bereits vergeben')
            return render(request, 'users/admin/user_create.html')
        
        # Create user
        user = CustomUser.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        
        # Set roles
        user.is_superuser = 'admin' in request.POST
        if user.is_superuser:
            user.is_staff = True
        else:
            user.is_staff = 'staff' in request.POST
        user.coordinator = 'coordinator' in request.POST
        user.save()
        
        # Create teacher profile if needed
        if 'teacher' in request.POST:
            Teacher.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                gender=1  # Default value
            )
        
        messages.success(request, f'Benutzer {user.get_full_name()} wurde erstellt')
        return redirect('users:role_list')
    
    return render(request, 'users/admin/user_create.html')


@login_required(login_url='/team/login/')
@user_passes_test(is_admin)
def user_role_delete(request, user_id):
    """Benutzer löschen"""
    
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Prevent deletion of current user
    if user == request.user:
        messages.error(request, 'Sie können sich nicht selbst löschen')
        return redirect('users:role_list')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'Benutzer {username} wurde gelöscht')
        return redirect('users:role_list')
    
    context = {
        'delete_user': user,
    }
    
    return render(request, 'users/admin/user_delete.html', context)
