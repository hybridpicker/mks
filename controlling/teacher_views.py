"""
Erweiterte Teacher-Verwaltungsansichten für das MKS Admin Interface
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from teaching.models import Teacher
from teaching.subject import Subject, SubjectCategory
from students.models import Gender, AcademicTitle
from location.models import Country


@login_required
def get_all_teachers(request):
    """
    Alle Lehrer anzeigen mit erweiterten Such- und Filterfunktionen
    """
    search_query = request.GET.get('search', '').strip()
    subject_filter = request.GET.get('subject', '')
    sort_by = request.GET.get('sort', 'last_name')
    
    # Base queryset with optimizations
    teachers = Teacher.objects.select_related(
        'gender', 
        'academic_title', 
        'country'
    ).prefetch_related(
        'subject', 
        'subject_coordinator'
    )
    
    # Search functionality
    if search_query:
        teachers = teachers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(subject__subject__icontains=search_query)  # Fixed: subject.subject instead of subject.name
        ).distinct()
    
    # Subject filter
    if subject_filter:
        teachers = teachers.filter(subject__id=subject_filter)
    
    # Sorting
    sort_options = {
        'last_name': 'last_name',
        'first_name': 'first_name',
        'email': 'email',
        'recent': '-id',
    }
    
    if sort_by in sort_options:
        teachers = teachers.order_by(sort_options[sort_by], 'first_name')
    else:
        teachers = teachers.order_by('last_name', 'first_name')
    
    # Get all subjects for filter - Fixed: order by 'subject' instead of 'name'
    all_subjects = Subject.objects.all().order_by('subject')
    
    # Statistics
    total_count = teachers.count()
    
    context = {
        'teachers': teachers,
        'search_query': search_query,
        'subject_filter': subject_filter,
        'sort_by': sort_by,
        'total_count': total_count,
        'all_subjects': all_subjects,
        'coordinators_count': teachers.filter(subject_coordinator__isnull=False).distinct().count(),
        'teachers_with_email': teachers.exclude(email='').count(),
        'teachers_with_phone': teachers.exclude(phone='').count(),
    }
    
    return render(request, 'controlling/teachers_list.html', context)


@login_required
def teacher_create(request):
    """
    Neuen Lehrer erstellen
    """
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        gender_id = request.POST.get('gender')
        
        # Validation
        errors = []
        
        if not first_name:
            errors.append('Vorname ist erforderlich.')
        
        if not last_name:
            errors.append('Nachname ist erforderlich.')
        
        if not gender_id:
            errors.append('Geschlecht ist erforderlich.')
        
        if email and '@' not in email:
            errors.append('Bitte geben Sie eine gültige E-Mail-Adresse ein.')
        
        # Check for duplicate email
        if email and Teacher.objects.filter(email=email).exists():
            errors.append('Diese E-Mail-Adresse wird bereits verwendet.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            try:
                # Create new teacher
                teacher = Teacher(
                    first_name=first_name,
                    last_name=last_name,
                    email=email if email else '',
                    phone=phone if phone else '',
                    gender_id=gender_id
                )
                
                # Optional fields
                academic_title_id = request.POST.get('academic_title')
                if academic_title_id:
                    teacher.academic_title_id = academic_title_id
                    
                bio = request.POST.get('bio', '').strip()
                if bio:
                    teacher.bio = bio
                    
                homepage = request.POST.get('homepage', '').strip()
                if homepage:
                    teacher.homepage = homepage
                
                teacher.save()
                
                # Handle subjects (many-to-many) - can only be set after saving
                subject_ids = request.POST.getlist('subjects')
                if subject_ids:
                    subjects = Subject.objects.filter(id__in=subject_ids)
                    teacher.subject.set(subjects)
                
                # Handle subject coordinators - nur wenn aktiv
                subject_coordinator_active = request.POST.get('subject_coordinator_active') == '1'
                teacher.subject_coordinator_active = subject_coordinator_active
                
                if subject_coordinator_active:
                    coordinator_ids = request.POST.getlist('subject_coordinators')
                    if coordinator_ids:
                        coordinators = SubjectCategory.objects.filter(id__in=coordinator_ids)
                        teacher.subject_coordinator.set(coordinators)
                
                messages.success(
                    request, 
                    f'Lehrer {teacher.first_name} {teacher.last_name} wurde erfolgreich erstellt.'
                )
                return redirect('controlling:teacher_detail', teacher_id=teacher.id)
                
            except Exception as e:
                messages.error(request, f'Fehler beim Erstellen: {str(e)}')
    
    # Get form choices
    context = {
        'academic_titles': AcademicTitle.objects.all(),
        'genders': Gender.objects.all(),
        'countries': Country.objects.all(),
        'all_subjects': Subject.objects.all().order_by('subject'),
        'subject_categories': SubjectCategory.objects.all().order_by('name'),
    }
    
    return render(request, 'controlling/teacher_create.html', context)


@login_required
def get_teacher_detail(request, teacher_id):
    """
    Einzelnen Lehrer anzeigen mit erweiterten Informationen
    """
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    context = {
        'teacher': teacher,
        'subjects': teacher.subject.all(),
        'coordinator_subjects': teacher.subject_coordinator.all(),
        'total_subjects': teacher.subject.count(),
        'is_coordinator': teacher.subject_coordinator.exists() and teacher.subject_coordinator_active,
        'is_coordinator_inactive': teacher.subject_coordinator.exists() and not teacher.subject_coordinator_active,
        'has_contact_info': bool(teacher.email or teacher.phone or teacher.homepage),
        'has_address': bool(teacher.adress_line or teacher.city),
        'has_media': bool(teacher.youtube_id_one or teacher.youtube_id_two),
    }
    
    return render(request, 'controlling/teacher_detail.html', context)


@login_required
def teacher_quick_edit(request, teacher_id):
    """
    Schnelle Bearbeitung wichtiger Lehrer-Daten
    """
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        bio = request.POST.get('bio', '').strip()
        
        # Validation
        errors = []
        
        if not first_name:
            errors.append('Vorname ist erforderlich.')
        
        if not last_name:
            errors.append('Nachname ist erforderlich.')
        
        if email and '@' not in email:
            errors.append('Bitte geben Sie eine gültige E-Mail-Adresse ein.')
        
        # Check for duplicate email
        if email and Teacher.objects.filter(email=email).exclude(id=teacher.id).exists():
            errors.append('Diese E-Mail-Adresse wird bereits verwendet.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            try:
                teacher.first_name = first_name
                teacher.last_name = last_name
                teacher.email = email if email else ''
                teacher.phone = phone if phone else ''
                teacher.bio = bio if bio else ''
                
                # Handle subject coordinators - nur wenn aktiv
                subject_coordinator_active = request.POST.get('subject_coordinator_active') == '1'
                teacher.subject_coordinator_active = subject_coordinator_active
                
                if subject_coordinator_active:
                    coordinator_ids = request.POST.getlist('subject_coordinators')
                    if coordinator_ids:
                        coordinators = SubjectCategory.objects.filter(id__in=coordinator_ids)
                        teacher.subject_coordinator.set(coordinators)
                    else:
                        teacher.subject_coordinator.clear()
                else:
                    # Wenn inaktiv, alle Zuweisungen entfernen
                    teacher.subject_coordinator.clear()
                
                teacher.save()
                
                messages.success(
                    request, 
                    f'Lehrer {teacher.first_name} {teacher.last_name} wurde erfolgreich aktualisiert.'
                )
                return redirect('controlling:teacher_detail', teacher_id=teacher.id)
                
            except Exception as e:
                messages.error(request, f'Fehler beim Speichern: {str(e)}')
    
    context = {
        'teacher': teacher,
        'subject_categories': SubjectCategory.objects.all().order_by('name'),
    }
    
    return render(request, 'controlling/teacher_quick_edit.html', context)


@login_required
def teacher_full_edit(request, teacher_id):
    """
    Vollständige Bearbeitung aller Lehrer-Daten einschließlich Subjects
    """
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        try:
            # Basic information
            teacher.first_name = request.POST.get('first_name', '').strip()
            teacher.last_name = request.POST.get('last_name', '').strip()
            teacher.email = request.POST.get('email', '').strip()
            teacher.phone = request.POST.get('phone', '').strip()
            teacher.homepage = request.POST.get('homepage', '').strip()
            
            # Address
            teacher.adress_line = request.POST.get('adress_line', '').strip()
            teacher.house_number = request.POST.get('house_number', '').strip()
            teacher.postal_code = request.POST.get('postal_code', '').strip()
            teacher.city = request.POST.get('city', '').strip()
            
            # Banking - REMOVED
            # teacher.iban = request.POST.get('iban', '').strip()
            # teacher.bic = request.POST.get('bic', '').strip()
            # teacher.socialSecurityField = request.POST.get('social_security', '').strip()
            
            # Biography and media
            teacher.bio = request.POST.get('bio', '').strip()
            teacher.youtube_id_one = request.POST.get('youtube_id_one', '').strip()
            teacher.youtube_id_two = request.POST.get('youtube_id_two', '').strip()
            
            # Foreign keys
            academic_title_id = request.POST.get('academic_title')
            if academic_title_id:
                teacher.academic_title_id = academic_title_id
            else:
                teacher.academic_title = None
                
            gender_id = request.POST.get('gender')
            if gender_id:
                teacher.gender_id = gender_id
                
            country_id = request.POST.get('country')
            if country_id:
                teacher.country_id = country_id
            else:
                teacher.country = None
            
            teacher.save()
            
            # Handle subjects (many-to-many)
            subject_ids = request.POST.getlist('subjects')
            if subject_ids:
                subjects = Subject.objects.filter(id__in=subject_ids)
                teacher.subject.set(subjects)
            else:
                teacher.subject.clear()
            
            # Handle subject coordinators - nur wenn aktiv
            subject_coordinator_active = request.POST.get('subject_coordinator_active') == '1'
            teacher.subject_coordinator_active = subject_coordinator_active
            
            if subject_coordinator_active:
                coordinator_ids = request.POST.getlist('subject_coordinators')
                if coordinator_ids:
                    coordinators = SubjectCategory.objects.filter(id__in=coordinator_ids)
                    teacher.subject_coordinator.set(coordinators)
                else:
                    teacher.subject_coordinator.clear()
            else:
                # Wenn inaktiv, alle Zuweisungen entfernen
                teacher.subject_coordinator.clear()
            
            messages.success(request, f'Lehrer {teacher.first_name} {teacher.last_name} wurde vollständig aktualisiert.')
            return redirect('controlling:teacher_detail', teacher_id=teacher.id)
            
        except Exception as e:
            messages.error(request, f'Fehler beim Speichern: {str(e)}')
    
    # Get form data
    context = {
        'teacher': teacher,
        'academic_titles': AcademicTitle.objects.all(),
        'genders': Gender.objects.all(),
        'countries': Country.objects.all(),
        'all_subjects': Subject.objects.all().order_by('subject'),  # Fixed: order by 'subject'
        'subject_categories': SubjectCategory.objects.all().order_by('name'),
    }
    
    return render(request, 'controlling/teacher_full_edit.html', context)


@login_required
def teacher_delete(request, teacher_id):
    """
    Lehrer löschen (nur POST-Requests)
    """
    if request.method == 'POST':
        teacher = get_object_or_404(Teacher, id=teacher_id)
        teacher_name = f"{teacher.first_name} {teacher.last_name}"
        
        try:
            teacher.delete()
            messages.success(request, f'Lehrer {teacher_name} wurde erfolgreich gelöscht.')
        except Exception as e:
            messages.error(request, f'Fehler beim Löschen: {str(e)}')
    
    return redirect('controlling:get_controlling_teachers')


@login_required
@require_http_methods(["GET"])
def teacher_api_search(request):
    """
    API endpoint for AJAX teacher search
    """
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'teachers': []})
    
    teachers = Teacher.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query)
    ).select_related('academic_title')[:10]
    
    teacher_list = []
    for teacher in teachers:
        teacher_list.append({
            'id': teacher.id,
            'name': f"{teacher.academic_title} {teacher.first_name} {teacher.last_name}".strip(),
            'email': teacher.email,
            'subjects': [subject.subject for subject in teacher.subject.all()[:3]]  # Fixed: subject.subject
        })
    
    return JsonResponse({'teachers': teacher_list})


@login_required
@require_http_methods(["GET"])
def teacher_stats_api(request):
    """
    API endpoint for teacher statistics
    """
    total_teachers = Teacher.objects.count()
    coordinators = Teacher.objects.filter(subject_coordinator__isnull=False).distinct().count()
    with_email = Teacher.objects.exclude(email='').count()
    with_phone = Teacher.objects.exclude(phone='').count()
    
    # Subject distribution
    subject_stats = []
    subjects = Subject.objects.annotate(
        teacher_count=Count('teacher')
    ).filter(teacher_count__gt=0).order_by('-teacher_count')
    
    for subject in subjects[:10]:
        subject_stats.append({
            'name': subject.subject,  # Fixed: subject.subject instead of subject.name
            'teacher_count': subject.teacher_count
        })
    
    return JsonResponse({
        'total_teachers': total_teachers,
        'coordinators': coordinators,
        'with_email': with_email,
        'with_phone': with_phone,
        'subject_distribution': subject_stats,
        'completion_rate': {
            'email': round((with_email / total_teachers) * 100, 1) if total_teachers > 0 else 0,
            'phone': round((with_phone / total_teachers) * 100, 1) if total_teachers > 0 else 0,
        }
    })
