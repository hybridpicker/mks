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

def teaching_art_view (request):
    blog = BlogPost.objects.filter(category__category__name="Kunstschule")[0:6]
    teacher_art = get_teachers_from_category("Kunstschule")
    context = { 'blog': blog, 
                'teacher_art': teacher_art,}
    return render (request, 'teaching/teaching_art.html', context)

def teaching_prices_view (request):
    return render (request, 'teaching/prices.html')
