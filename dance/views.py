from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .models import TimeSlot, Course, Teacher
from collections import defaultdict
import locale

# Set locale to German for correct day sorting if needed
try:
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'German_Germany.1252') # Windows fallback
    except locale.Error:
        print("Warning: German locale not found, day sorting might be alphabetical.")

def dance_schedule_view(request):
    """Displays the dance schedule grouped by day."""
    # Fetch all timeslots, efficiently grabbing related course and teacher info
    all_timeslots = TimeSlot.objects.select_related('course__teacher').order_by('day', 'start_time')

    # Group timeslots by day
    timeslots_by_day = defaultdict(list)
    for timeslot in all_timeslots:
        timeslots_by_day[timeslot.day].append(timeslot)

    # Order the days correctly (using locale if possible, otherwise default order)
    # Define the desired order of days
    day_order = {day[0]: i for i, day in enumerate(TimeSlot.DAYS_OF_WEEK)}
    # Sort the grouped dictionary by the custom day order
    sorted_timeslots_by_day = dict(sorted(timeslots_by_day.items(), key=lambda item: day_order.get(item[0], 99)))

    context = {
        'timeslots_by_day': sorted_timeslots_by_day,
        'page_title': 'Tanz & Bewegung - Stundenplan' # Example title
    }
    return render(request, 'dance/schedule.html', context)

@login_required
def maintenance_view(request):
    """Wartungsansicht für Kurse, Zeitfenster und Lehrer."""
    # Filter nach Query-Parametern
    teacher_filter = request.GET.get('teacher')
    age_group_filter = request.GET.get('age_group')
    
    # Kurse abfragen
    courses_query = Course.objects.all().prefetch_related('timeslots')
    
    if teacher_filter:
        courses_query = courses_query.filter(teacher_id=teacher_filter)
    
    if age_group_filter:
        courses_query = courses_query.filter(age_group=age_group_filter)
    
    # Paginierung einrichten
    paginator = Paginator(courses_query.order_by('name'), 10)  # 10 Kurse pro Seite
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)
    
    # Alle Lehrer abfragen
    teachers = Teacher.objects.all().order_by('name')
    
    # Eindeutige Altersgruppen für Filter
    age_groups = Course.objects.values_list('age_group', flat=True).distinct().order_by('age_group')
    
    context = {
        'courses': courses,
        'teachers': teachers,
        'age_groups': age_groups,
        'days_of_week': TimeSlot.DAYS_OF_WEEK,
    }
    
    return render(request, 'dance/maintenance.html', context)

@login_required
def teacher_action(request):
    """Hinzufügen oder Bearbeiten eines Lehrers."""
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        if teacher_id:
            # Bearbeiten eines bestehenden Lehrers
            teacher = get_object_or_404(Teacher, id=teacher_id)
            teacher.name = name
            teacher.email = email
            teacher.save()
        else:
            # Neuen Lehrer hinzufügen
            Teacher.objects.create(name=name, email=email)
        
        return redirect('dance:maintenance')
    
    return HttpResponseRedirect(reverse('dance:maintenance'))

@login_required
def course_action(request):
    """Hinzufügen oder Bearbeiten eines Kurses."""
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        name = request.POST.get('name')
        teacher_id = request.POST.get('teacher_id')
        age_group = request.POST.get('age_group')
        description = request.POST.get('description')
        
        teacher = get_object_or_404(Teacher, id=teacher_id)
        
        if course_id:
            # Bearbeiten eines bestehenden Kurses
            course = get_object_or_404(Course, id=course_id)
            course.name = name
            course.teacher = teacher
            course.age_group = age_group
            course.description = description
            course.save()
        else:
            # Neuen Kurs hinzufügen
            Course.objects.create(
                name=name,
                teacher=teacher,
                age_group=age_group,
                description=description
            )
        
        return redirect('dance:maintenance')
    
    return HttpResponseRedirect(reverse('dance:maintenance'))

@login_required
def timeslot_action(request):
    """Hinzufügen oder Bearbeiten eines Zeitfensters."""
    if request.method == 'POST':
        timeslot_id = request.POST.get('timeslot_id')
        course_id = request.POST.get('course_id')
        day = request.POST.get('day')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        studio = request.POST.get('studio')
        
        course = get_object_or_404(Course, id=course_id)
        
        if timeslot_id:
            # Bearbeiten eines bestehenden Zeitfensters
            timeslot = get_object_or_404(TimeSlot, id=timeslot_id)
            timeslot.course = course
            timeslot.day = day
            timeslot.start_time = start_time
            timeslot.end_time = end_time
            timeslot.studio = studio
            timeslot.save()
        else:
            # Neues Zeitfenster hinzufügen
            TimeSlot.objects.create(
                course=course,
                day=day,
                start_time=start_time,
                end_time=end_time,
                studio=studio
            )
        
        return redirect('dance:maintenance')
    
    return HttpResponseRedirect(reverse('dance:maintenance'))

@login_required
def delete_action(request):
    """Löschen von Objekten (Lehrer, Kurse, Zeitfenster)."""
    if request.method == 'POST':
        object_id = request.POST.get('id')
        object_type = request.POST.get('type')
        
        if object_type == 'teacher':
            # Lehrer löschen
            teacher = get_object_or_404(Teacher, id=object_id)
            teacher.delete()
        elif object_type == 'course':
            # Kurs löschen
            course = get_object_or_404(Course, id=object_id)
            course.delete()
        elif object_type == 'timeslot':
            # Zeitfenster löschen
            timeslot = get_object_or_404(TimeSlot, id=object_id)
            timeslot.delete()
        
        return redirect('dance:maintenance')
    
    return HttpResponseRedirect(reverse('dance:maintenance'))

def course_detail(request, course_id):
    """API-Endpunkt für Kursbeschreibungen."""
    course = get_object_or_404(Course, id=course_id)
    data = {
        'id': course.id,
        'name': course.name,
        'description': course.description,
        'teacher': course.teacher.name,
        'age_group': course.age_group
    }
    return JsonResponse(data)
