from django.shortcuts import render
from teaching.models import Teacher
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from contact.forms import ContactForm
from contact.email import contact_mail_student, contact_mail_blessond
from teaching.subject import Subject
from location.models import Location
from students.models import Student
from students.gender import Gender
import datetime

def guitar_teaching_view(request):
    teacher_data = Teacher.objects.filter(subject_id=1)
    context = {
        'teacher_data': teacher_data,
    }
    return render(request, 'teaching/guitar_lesson.html', context)

def piano_teaching_view(request):
    teacher_data = Teacher.objects.filter(subject_id=2)
    context = {
        'teacher_data': teacher_data,
    }
    return render(request, 'teaching/piano_lesson.html', context)

def vocal_teaching_view(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        from_email = form.cleaned_data['from_email']
        message = form.cleaned_data['message']
        subject = form.cleaned_data['subject']
        location = form.cleaned_data['location']
        subject_id = request.POST['subject']
        subject_object = Subject.objects.get(pk=subject_id)
        gender_id = request.POST['gender']
        gender_object = Gender.objects.get(pk=gender_id)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        location_id = request.POST['location']
        location_object = Location.objects.get(pk=location_id)
        lesson_counter = 0
        new_student = Student(gender=gender_object,
                              first_name=first_name,
                              last_name=last_name,
                              subject=subject_object,
                              location=location_object,
                              lesson_count=lesson_counter)
        new_student.save()
        subject = str(Subject.objects.get(pk=subject_id))
        now = datetime.datetime.now()
        today = now.date()
        student_context = {
            'first_name': first_name,
            'last_name': last_name,
            'location': location_object,
            'today': today,
            'subject': subject_object,
        }
        try:
            contact_mail_student(from_email, subject, message, student_context)
#               contact_mail_blessond(from_email, subject, message)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        context = {
            'form': form,
        }
        return redirect('success_contact')
    return render(request, 'teaching/vocal_lesson.html', {'form':form})
