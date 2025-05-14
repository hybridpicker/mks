'''
Views for teaching
'''
import datetime
from datetime import timedelta
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.db.models import F
from django.shortcuts import render, redirect
from students.models import Student
from teaching.models import Teacher
from django.contrib.auth.forms import AuthenticationForm
from blog.models import BlogPost
from teaching.show_teacher_view import get_teachers_from_category
from school.school_year import get_current_school_year
from teaching.subject import Subject, SubjectCategory

def get_calendar(student):
    '''
    Helper function to get calendar
    '''
    student = Student.objects.get(pk=student)  # pylint: disable=no-member
    calendar = student.teacher.calendar
    return calendar

def get_date_time(date, time):
    start_time = str(date + ' ' + time)
    start = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
    return start

def get_end_time(start, student_id):
    '''
    Calculate end time
    '''
    date_and_time = start
    student = Student.objects.get(pk=student_id)
    lesson_form_minutes = student.lesson_form.minutes
    end_delta = timedelta(minutes=lesson_form_minutes)
    end_time = date_and_time + end_delta
    return end_time

def increment_counter(student_id):
    student = Student.objects.get(pk=student_id)
    student.lesson_count = F('lesson_count') + 1
    student.save()
    return student_id

def get_title(student, new_count):
    student = str(student)
    counter = str(new_count)
    title = student + ' ' + '(' + counter + ')'
    return title

def teaching_music_view (request):
    return render (request, 'teaching/teaching_music.html')

def get_fachgruppe_context(category_name):
    """
    Generische Funktion um den Context für eine Fachgruppe zu erstellen
    Nutzt die gleiche Logik wie die ueber-uns Seite
    """
    try:
        category = SubjectCategory.objects.get(name=category_name)
    except SubjectCategory.DoesNotExist:
        return {'category_name': category_name, 'subjects': [], 'teachers': []}
    
    # Hole alle Fächer dieser Kategorie
    subjects = Subject.objects.filter(category=category, hidden_subject=False)
    
    # Hole alle Lehrer dieser Kategorie mit der gleichen Funktion wie bei ueber-uns
    teachers = get_teachers_from_category(category_name)
    
    context = {
        'category': category,
        'category_name': category_name,
        'subjects': subjects,
        'teachers': teachers if teachers is not None else [],
    }
    
    return context

def teaching_brass_view (request):
    # Blasinstrumente umfasst sowohl Holz- als auch Blechblasinstrumente
    context = {}
    
    # Hole Lehrer für beide Kategorien
    teachers_brass = get_teachers_from_category("Blechblasinstrumente")
    teachers_wood = get_teachers_from_category("Holzblasinstrumente")
    
    # Kombiniere die Lehrer (beide sind jetzt immer QuerySets)
    teachers = teachers_brass | teachers_wood
    
    # Hole Subjects von beiden Kategorien
    subjects = []
    try:
        brass_cat = SubjectCategory.objects.get(name="Blechblasinstrumente")
        brass_subjects = Subject.objects.filter(category=brass_cat, hidden_subject=False)
        subjects.extend(list(brass_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    try:
        wood_cat = SubjectCategory.objects.get(name="Holzblasinstrumente")
        wood_subjects = Subject.objects.filter(category=wood_cat, hidden_subject=False)
        subjects.extend(list(wood_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    context['category_name'] = 'Blasinstrumente'
    context['subjects'] = subjects
    context['teachers'] = teachers.distinct()
    context['intro_text'] = 'Die Abteilung für Blasinstrumente bietet Unterricht in Holz- und Blechblasinstrumenten. Von der Flöte bis zur Tuba können Sie bei uns alle klassischen Orchesterinstrumente erlernen.'
    context['youtube_videos'] = ['aOCC8U4ldBI', 'HeTdrvqdkzg', 'AkXkj-1mOgg', 'GP04_HEJwvM', 'mYLesCKiU8E']
    
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_eme_view (request):
    # Elementare Musikerziehung und Musikalische Früherziehung
    context = {}
    
    # Hole Lehrer für beide Kategorien
    teachers_eme = get_teachers_from_category("Elementare Musikerziehung")
    teachers_mfe = get_teachers_from_category("Musikalische Früherziehung")
    
    # Kombiniere die Lehrer (beide sind jetzt immer QuerySets)
    teachers = teachers_eme | teachers_mfe
    
    # Hole Subjects von beiden Kategorien
    subjects = []
    try:
        eme_cat = SubjectCategory.objects.get(name="Elementare Musikerziehung")
        eme_subjects = Subject.objects.filter(category=eme_cat, hidden_subject=False)
        subjects.extend(list(eme_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    try:
        mfe_cat = SubjectCategory.objects.get(name="Musikalische Früherziehung")
        mfe_subjects = Subject.objects.filter(category=mfe_cat, hidden_subject=False)
        subjects.extend(list(mfe_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    context['category_name'] = 'Elementare Musikerziehung'
    context['subjects'] = subjects
    context['teachers'] = teachers.distinct()
    context['intro_text'] = 'Die Elementare Musikerziehung bietet einen spielerischen Zugang zur Musik für Kinder. In Gruppen werden musikalische Grundlagen vermittelt und die Freude an der Musik geweckt.'
    
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_theory_view (request):
    # Musikkunde und Theorie
    context = {}
    
    # Hole Lehrer für beide Kategorien
    teachers_musikkunde = get_teachers_from_category("Musikkunde")
    teachers_theorie = get_teachers_from_category("Theorie")
    
    # Kombiniere die Lehrer (beide sind jetzt immer QuerySets)
    teachers = teachers_musikkunde | teachers_theorie
    
    # Hole Subjects von beiden Kategorien
    subjects = []
    try:
        musikkunde_cat = SubjectCategory.objects.get(name="Musikkunde")
        musikkunde_subjects = Subject.objects.filter(category=musikkunde_cat, hidden_subject=False)
        subjects.extend(list(musikkunde_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    try:
        theorie_cat = SubjectCategory.objects.get(name="Theorie")
        theorie_subjects = Subject.objects.filter(category=theorie_cat, hidden_subject=False)
        subjects.extend(list(theorie_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    context['category_name'] = 'Musikkunde'
    context['subjects'] = subjects
    context['teachers'] = teachers.distinct()
    context['intro_text'] = 'Die Musikkunde vermittelt die theoretischen Grundlagen der Musik. Von der Notenlehre bis zur Harmonielehre werden alle wichtigen Bereiche der Musiktheorie behandelt.'
    
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_drums_view (request):
    # Schlaginstrumente und Schlagwerk
    context = {}
    
    # Hole Lehrer für beide Kategorien
    teachers_schlag = get_teachers_from_category("Schlaginstrumente")
    teachers_schlagwerk = get_teachers_from_category("Schlagwerk")
    
    # Kombiniere die Lehrer (beide sind jetzt immer QuerySets)
    teachers = teachers_schlag | teachers_schlagwerk
    
    # Hole Subjects von beiden Kategorien
    subjects = []
    try:
        schlag_cat = SubjectCategory.objects.get(name="Schlaginstrumente")
        schlag_subjects = Subject.objects.filter(category=schlag_cat, hidden_subject=False)
        subjects.extend(list(schlag_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    try:
        schlagwerk_cat = SubjectCategory.objects.get(name="Schlagwerk")
        schlagwerk_subjects = Subject.objects.filter(category=schlagwerk_cat, hidden_subject=False)
        subjects.extend(list(schlagwerk_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    context['category_name'] = 'Schlaginstrumente'
    context['subjects'] = subjects
    context['teachers'] = teachers.distinct()
    context['intro_text'] = 'Die Abteilung für Schlaginstrumente umfasst klassische Percussion, Drumset, Stabspiele und weitere rhythmische Instrumente. Der Unterricht reicht von klassischer Percussion bis zu modernen Stilrichtungen.'
    context['youtube_videos'] = ['w8yg-ZHYYAA']
    
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_vocal_view (request):
    # Stimmbildung und Gesang
    context = {}
    
    # Hole Lehrer für beide Kategorien
    teachers_stimm = get_teachers_from_category("Stimmbildung")
    teachers_gesang = get_teachers_from_category("Gesang")
    
    # Kombiniere die Lehrer (beide sind jetzt immer QuerySets)
    teachers = teachers_stimm | teachers_gesang
    
    # Hole Subjects von beiden Kategorien
    subjects = []
    try:
        stimm_cat = SubjectCategory.objects.get(name="Stimmbildung")
        stimm_subjects = Subject.objects.filter(category=stimm_cat, hidden_subject=False)
        subjects.extend(list(stimm_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    try:
        gesang_cat = SubjectCategory.objects.get(name="Gesang")
        gesang_subjects = Subject.objects.filter(category=gesang_cat, hidden_subject=False)
        subjects.extend(list(gesang_subjects))
    except SubjectCategory.DoesNotExist:
        pass
    
    context['category_name'] = 'Stimmbildung'
    context['subjects'] = subjects
    context['teachers'] = teachers.distinct()
    context['intro_text'] = 'Die Gesangsabteilung bietet Unterricht in verschiedenen Stilrichtungen an. Von klassischem Gesang über Musical bis zu Pop und Jazz können Sie Ihre Stimme professionell ausbilden lassen.'
    context['youtube_videos'] = ['ESVykNyE3tY', '64DIUyJyXeM']
    
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_strings_view (request):
    context = get_fachgruppe_context('Streichinstrumente')
    context['intro_text'] = 'Die Streicherabteilung unterrichtet alle klassischen Streichinstrumente. Vom Kontrabass bis zur Violine bieten wir professionellen Unterricht für Anfänger und Fortgeschrittene.'
    context['youtube_videos'] = ['rVTWes-vLL4', 'cI4jhzFOBoQ']
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_keys_view (request):
    context = get_fachgruppe_context('Tasteninstrumente')
    context['intro_text'] = 'Die Abteilung für Tasteninstrumente ist die größte Abteilung unserer Musikschule. Neben dem beliebten Klavier unterrichten wir auch Akkordeon, Cembalo und Kirchenorgel.'
    context['youtube_videos'] = ['fi8ZGiB-lSc', 'NaTwXuR4VwM', 'Wh-uAzNYsLU', 'XhqeetX6NFo']
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_picked_view (request):
    context = get_fachgruppe_context('Zupfinstrumente')
    context['intro_text'] = 'Die Zupfinstrumente umfassen Gitarre, E-Gitarre, E-Bass, Harfe und Zither. Ob klassische Gitarre oder moderne E-Gitarre - bei uns finden Sie den passenden Unterricht.'
    context['youtube_videos'] = ['v30Zs04SwTU', 'CO9peHPN-_Q', 'jQUk2C51T5c', '2kBBFfEORmw']
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_art_view (request):
    blog = BlogPost.objects.filter(category__category__name="Kunstschule")[0:6]
    teacher_art = get_teachers_from_category("Kunstschule")
    context = { 'blog': blog, 
                'teacher_art': teacher_art,}
    return render (request, 'teaching/teaching_art.html', context)

def teaching_prices_view (request):
    current_school_year = get_current_school_year()
    context = { 'current_school_year': current_school_year,}
    return render (request, 'teaching/prices.html', context)
