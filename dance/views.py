from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, FileResponse
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from .models import TimeSlot, Course, Teacher
from collections import defaultdict
import locale
import os
import tempfile
from .excel_utils import export_to_excel, parse_excel_file, generate_fixture_from_excel_data, update_database_from_fixture

# Set locale to German for correct day sorting if needed
try:
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'German_Germany.1252') # Windows fallback
    except locale.Error:
        print("Warning: German locale not found, day sorting might be alphabetical.")

# Importiere die aktualisierte Kategorie-Funktion
from .views_categories import get_course_category

def dance_schedule_view(request):
    """Displays the dance schedule grouped by day with filtering."""
    category_filter = request.GET.get('category')
    age_group_filter = request.GET.get('age_group')
    location_filter = request.GET.get('location')

    # Fetch all timeslots, efficiently grabbing related course and teacher info
    all_timeslots = TimeSlot.objects.select_related('course__teacher').order_by('day', 'start_time')

    # Filter timeslots based on category and age group
    filtered_timeslots = []
    for timeslot in all_timeslots:
        course = timeslot.course
        
        # Determine category based on description and age
        base_category = get_course_category(course.description or '')
        
        # If age indicates children's class, override category for children under certain age
        age_text = course.age_group.lower() if course.age_group else ""
        has_young_age = any(term in age_text for term in ['3-', '4-', '5-', '6-', '7-', '8-', 'kinder'])
        
        if has_young_age and base_category != 'Musical Dance':
            course_category = 'Kindertanz'
        else:
            course_category = base_category

        # Bestimme, zu welcher vordefinierten Altersgruppe der Kurs gehört
        actual_age_group = course.age_group.lower() if course.age_group else ""
        mapped_age_group = ""
        
        # Zuordnung der tatsächlichen Altersangaben zu den vordefinierten Filtern
        if any(x in actual_age_group for x in ["3", "4", "5"]) or "kleinkinder" in actual_age_group:
            mapped_age_group = "3-6 Jahre"
        elif any(x in actual_age_group for x in ["6", "7", "8", "9"]) or "grundschule" in actual_age_group:
            mapped_age_group = "6-9 Jahre"
        elif any(x in actual_age_group for x in ["10", "11", "12", "13", "14"]) or "jugendliche" in actual_age_group:
            mapped_age_group = "10-14 Jahre"
        elif any(x in actual_age_group for x in ["15+", "15", "16", "17", "18", "erwachsene"]):
            mapped_age_group = "15+"
        else:
            # Fallback basierend auf den ersten Zahlen im String
            import re
            age_numbers = re.findall(r'\d+', actual_age_group)
            if age_numbers:
                first_age = int(age_numbers[0])
                if first_age <= 6:
                    mapped_age_group = "3-6 Jahre"
                elif first_age <= 9:
                    mapped_age_group = "6-9 Jahre"
                elif first_age <= 14:
                    mapped_age_group = "10-14 Jahre"
                else:
                    mapped_age_group = "15+"
        
        # Speichere die zugeordnete Altersgruppe für die Anzeige
        timeslot.mapped_age_group = mapped_age_group
        
        # Apply filters
        category_match = not category_filter or course_category == category_filter
        age_group_match = not age_group_filter or mapped_age_group == age_group_filter
        location_match = not location_filter or timeslot.location == location_filter

        if category_match and age_group_match and location_match:
            filtered_timeslots.append(timeslot)
            # Store the computed category for display in template
            timeslot.computed_category = course_category

    # Group filtered timeslots by day
    timeslots_by_day = defaultdict(list)
    for timeslot in filtered_timeslots:
        timeslots_by_day[timeslot.day].append(timeslot)

    # Order the days correctly (using locale if possible, otherwise default order)
    day_order = {day[0]: i for i, day in enumerate(TimeSlot.DAYS_OF_WEEK)}
    sorted_timeslots_by_day = dict(sorted(timeslots_by_day.items(), key=lambda item: day_order.get(item[0], 99)))
    
    # Get all unique locations for the filter - ensure true uniqueness
    # Verwende ein Set, um Duplikate zu vermeiden
    unique_locations = set()
    for location in TimeSlot.objects.values_list('location', flat=True):
        if location:  # Ignoriere None/leere Werte
            unique_locations.add(location)
    # Sortiere die Liste für eine konsistente Anzeige
    unique_locations = sorted(unique_locations)

    # Verwende feste Altersgruppen statt die aus der Datenbank
    all_courses = Course.objects.all()
    unique_age_groups = ["3-6 Jahre", "6-9 Jahre", "10-14 Jahre", "15+"]
    
    # Generate available categories by actually analyzing the courses
    available_categories = []
    for course in all_courses:
        base_category = get_course_category(course.description or '')
        
        # Override for young children
        age_text = course.age_group.lower() if course.age_group else ""
        has_young_age = any(term in age_text for term in ['3-', '4-', '5-', '6-', '7-', '8-', 'kinder'])
        
        if has_young_age and base_category != 'Musical Dance':
            category = 'Kindertanz'
        else:
            category = base_category
            
        if category not in available_categories:
            available_categories.append(category)
    
    available_categories.sort()

    # Count courses per category and age group for display
    category_counts = {}
    age_group_counts = {}
    
    # Initialisiere Zähler für Altersgruppen
    for age_group in unique_age_groups:
        age_group_counts[age_group] = 0
    
    # Zähle Kurse pro Kategorie
    for category in available_categories:
        count = 0
        for course in all_courses:
            base_cat = get_course_category(course.description or '')
            age_text = course.age_group.lower() if course.age_group else ""
            has_young_age = any(term in age_text for term in ['3-', '4-', '5-', '6-', '7-', '8-', 'kinder'])
            
            if has_young_age and base_cat != 'Musical Dance':
                comp_cat = 'Kindertanz'
            else:
                comp_cat = base_cat
                
            if comp_cat == category:
                count += 1
        category_counts[category] = count
    
    # Zähle Kurse pro Altersgruppe
    for course in all_courses:
        age_text = course.age_group.lower() if course.age_group else ""
        
        # Zuordnung zu einer der vordefinierten Altersgruppen
        if any(x in age_text for x in ["3", "4", "5"]) or "kleinkinder" in age_text:
            age_group_counts["3-6 Jahre"] += 1
        elif any(x in age_text for x in ["6", "7", "8", "9"]) or "grundschule" in age_text:
            age_group_counts["6-9 Jahre"] += 1
        elif any(x in age_text for x in ["10", "11", "12", "13", "14"]) or "jugendliche" in age_text:
            age_group_counts["10-14 Jahre"] += 1
        elif any(x in age_text for x in ["15+", "15", "16", "17", "18", "erwachsene"]):
            age_group_counts["15+"] += 1
        else:
            # Fallback basierend auf den ersten Zahlen im String
            import re
            age_numbers = re.findall(r'\d+', age_text)
            if age_numbers:
                first_age = int(age_numbers[0])
                if first_age <= 6:
                    age_group_counts["3-6 Jahre"] += 1
                elif first_age <= 9:
                    age_group_counts["6-9 Jahre"] += 1
                elif first_age <= 14:
                    age_group_counts["10-14 Jahre"] += 1
                else:
                    age_group_counts["15+"] += 1
            else:
                # Falls keine Altersinformation gefunden wurde, zum Standardwert
                age_group_counts["3-6 Jahre"] += 1

    # Count timeslots per location for display
    location_counts = {}
    for location in unique_locations:
        # Count the number of timeslots at this location
        count = TimeSlot.objects.filter(location=location).count()
        location_counts[location] = count

    context = {
        'timeslots_by_day': sorted_timeslots_by_day,
        'page_title': 'Tanz & Bewegung - Stundenplan',
        'unique_age_groups': unique_age_groups,
        'available_categories': available_categories,
        'unique_locations': unique_locations,
        'category_counts': category_counts,
        'age_group_counts': age_group_counts,
        'location_counts': location_counts,
        'selected_category': category_filter,
        'selected_age_group': age_group_filter,
        'selected_location': location_filter,
        'total_courses': len(all_courses),
        'filtered_count': len(filtered_timeslots),
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
        location = request.POST.get('location')
        
        course = get_object_or_404(Course, id=course_id)
        
        if timeslot_id:
            # Bearbeiten eines bestehenden Zeitfensters
            timeslot = get_object_or_404(TimeSlot, id=timeslot_id)
            timeslot.course = course
            timeslot.day = day
            timeslot.start_time = start_time
            timeslot.end_time = end_time
            timeslot.studio = studio
            timeslot.location = location
            timeslot.save()
        else:
            # Neues Zeitfenster hinzufügen
            TimeSlot.objects.create(
                course=course,
                day=day,
                start_time=start_time,
                end_time=end_time,
                studio=studio,
                location=location
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
    
    # Sammle die Standorte aus allen Zeitfenstern des Kurses
    # Verwende set() um sicherzustellen, dass jeder Standort nur einmal vorkommt
    locations = set([loc for loc in course.timeslots.values_list('location', flat=True) if loc])
    # Konvertiere zurück zu einer sortierten Liste
    locations = sorted(list(locations))
    
    data = {
        'id': course.id,
        'name': course.name,
        'description': course.description,
        'teacher': course.teacher.name,
        'teacher_id': course.teacher.id,
        'age_group': course.age_group,
        'locations': list(locations)
    }
    return JsonResponse(data)

def teacher_detail_api(request, teacher_id):
    """API-Endpunkt für Lehrerdaten."""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    data = {
        'id': teacher.id,
        'name': teacher.name,
        'email': teacher.email
    }
    return JsonResponse(data)

def timeslot_detail_api(request, timeslot_id):
    """API-Endpunkt für Zeitfensterdaten."""
    timeslot = get_object_or_404(TimeSlot, id=timeslot_id)
    data = {
        'id': timeslot.id,
        'course_id': timeslot.course.id,
        'day': timeslot.day,
        'start_time': timeslot.start_time.strftime('%H:%M'),
        'end_time': timeslot.end_time.strftime('%H:%M'),
        'studio': timeslot.studio or '',
        'location': timeslot.location or ''
    }
    return JsonResponse(data)

@login_required
def export_excel(request):
    """Exports all dance classes data as an Excel file."""
    try:
        # Create Excel file and get relative path
        excel_path = export_to_excel()
        
        # Create absolute path for the server
        full_path = os.path.join(settings.BASE_DIR, excel_path)
        
        # Create file response for download
        response = FileResponse(
            open(full_path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(excel_path)
        )
        return response
    except Exception as e:
        messages.error(request, f"Error exporting: {str(e)}")
        return redirect('dance:maintenance')

@login_required
def import_excel(request):
    """Imports dance classes data from an Excel file."""
    if request.method == 'POST' and request.FILES.get('excel_file'):
        try:
            excel_file = request.FILES['excel_file']
            
            # Temporary file for the uploaded Excel file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
                for chunk in excel_file.chunks():
                    temp_file.write(chunk)
            
            # Parse Excel file
            excel_data = parse_excel_file(temp_file.name)
            
            # Path to fixture
            fixture_path = os.path.join(settings.BASE_DIR, 'dance', 'fixtures', 'dance_data.json')
            
            # Generate fixture from Excel data
            generate_fixture_from_excel_data(excel_data, fixture_path)
            
            # Update database from fixture
            update_database_from_fixture(fixture_path)
            
            # Delete temporary file
            os.unlink(temp_file.name)
            
            messages.success(request, "Data successfully imported and database updated.")
        except Exception as e:
            messages.error(request, f"Error importing: {str(e)}")
        
        return redirect('dance:maintenance')
    
    # Redirect to maintenance page for GET requests or errors
    return redirect('dance:maintenance')
