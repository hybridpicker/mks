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
from schedule.models import Event
from lessoncalendar.models import LessonEvent
from lessoncalendar.lessonevent import create_lesson_event
from students.models import Student
from teaching.models import Teacher
from django.contrib.auth.forms import AuthenticationForm


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

def calendar_request(request):
    '''
    Requesting calendar and form for creating new LessonEvent
    '''
    def request_calendar_slug(user):
        teacher = Teacher.objects.get(user=user)
        calendar_slug = teacher.calendar.slug
        return calendar_slug
        '''
        Getting Calendar Slug from Logged-In Teacher
        '''
    calendar_slug = request_calendar_slug(request.user)
    form = create_lesson_event(request.POST)
    if form.is_valid():
        date = request.POST['date']
        time = request.POST['time']
        text = request.POST['text_field']
        student_id = request.POST['student']
        start = get_date_time(date, time)
        print(start)
        end = get_end_time(start, student_id)
        student = Student.objects.get(pk=student_id)
        new_count = increment_counter(student_id)
        counter = student.lesson_count
        counter += 1
        calendar = get_calendar(student_id)
        title = get_title(student, counter)
        try:
            new_event = Event(start=start, end=end, title=title,
                              calendar=calendar, description=text,)
            new_event.save()
            new_lesson_event = LessonEvent(event=new_event, student=student)
            new_lesson_event.save()
            return HttpResponseRedirect(request.path)
        except IntegrityError:
            new_event = Event(start=start, end=end, title=student,
                              calendar=calendar, description=text,)
            new_event.save()
            return HttpResponseRedirect(request.path)
    else:
        print('Form not valid')
    context = {
        'form': form,
        'slug': calendar_slug,
    }
    return render(request, 'lessons/calendar/fullcalendar.html', context)
