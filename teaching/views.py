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
    """
    try:
        category = SubjectCategory.objects.get(name=category_name)
    except SubjectCategory.DoesNotExist:
        return {'category_name': category_name, 'subjects': [], 'teachers': []}
    
    # Hole alle Fächer dieser Kategorie
    subjects = Subject.objects.filter(category=category, hidden_subject=False)
    
    # Hole alle Lehrer dieser Kategorie
    teachers = Teacher.objects.filter(subject__category=category).distinct()
    
    context = {
        'category': category,
        'category_name': category_name,
        'subjects': subjects,
        'teachers': teachers,
    }
    
    return context

def teaching_brass_view (request):
    context = get_fachgruppe_context('Blasinstrumente')
    context['intro_text'] = 'Die Abteilung für Blasinstrumente bietet Unterricht in Holz- und Blechblasinstrumenten. Von der Flöte bis zur Tuba können Sie bei uns alle klassischen Orchesterinstrumente erlernen.'
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_eme_view (request):
    context = get_fachgruppe_context('Elementare Musikerziehung')
    context['intro_text'] = 'Die Elementare Musikerziehung bietet einen spielerischen Zugang zur Musik für Kinder. In Gruppen werden musikalische Grundlagen vermittelt und die Freude an der Musik geweckt.'
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_theory_view (request):
    context = get_fachgruppe_context('Musikkunde')
    context['intro_text'] = 'Die Musikkunde vermittelt die theoretischen Grundlagen der Musik. Von der Notenlehre bis zur Harmonielehre werden alle wichtigen Bereiche der Musiktheorie behandelt.'
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_drums_view (request):
    context = get_fachgruppe_context('Schlaginstrumente')
    context['intro_text'] = 'Die Abteilung für Schlaginstrumente umfasst klassische Percussion, Drumset, Stabspiele und weitere rhythmische Instrumente. Der Unterricht reicht von klassischer Percussion bis zu modernen Stilrichtungen.'
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_vocal_view (request):
    context = get_fachgruppe_context('Stimmbildung')
    context['intro_text'] = 'Die Gesangsabteilung bietet Unterricht in verschiedenen Stilrichtungen an. Von klassischem Gesang über Musical bis zu Pop und Jazz können Sie Ihre Stimme professionell ausbilden lassen.'
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_strings_view (request):
    context = get_fachgruppe_context('Streichinstrumente')
    context['intro_text'] = 'Die Streicherabteilung unterrichtet alle klassischen Streichinstrumente. Vom Kontrabass bis zur Violine bieten wir professionellen Unterricht für Anfänger und Fortgeschrittene.'
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_keys_view (request):
    context = get_fachgruppe_context('Tasteninstrumente')
    context['intro_text'] = 'Die Abteilung für Tasteninstrumente ist die größte Abteilung unserer Musikschule. Neben dem beliebten Klavier unterrichten wir auch Akkordeon, Cembalo und Kirchenorgel.'
    return render (request, 'teaching/fachgruppen/base_fachgruppe.html', context)

def teaching_picked_view (request):
    context = get_fachgruppe_context('Zupfinstrumente')
    context['intro_text'] = 'Die Zupfinstrumente umfassen Gitarre, E-Gitarre, E-Bass, Harfe und Zither. Ob klassische Gitarre oder moderne E-Gitarre - bei uns finden Sie den passenden Unterricht.'
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
