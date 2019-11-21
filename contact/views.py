from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from contact.forms import ContactForm
from contact.email import contact_mail_student, contact_mail_mks
from teaching.subject import Subject
from students.models import Student
from students.gender import Gender
import datetime
from django.conf import settings
import urllib
import json
from django.contrib import messages


def save_image(url):
    student = Student()
    name = urlparse(url).path.split('/')[-1]
    content = urllib.request.urlopen(url)

def emailView(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        secret_key = settings.RECAPTCHA_SECRET_KEY
        data = {
        'response': request.POST.get('g-recaptcha-response'),
        'secret': secret_key
        }
        url = 'https://www.google.com/recaptcha/api/siteverify'
        data = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request(url, data=data)

        # verify the token submitted with the form is valid
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())

        # result will be a dict containing 'success' and 'action'.
        # it is important to verify both

        if (not result['success']) or (not result['action'] == 'submit'):
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return HttpResponse('Invalid reCAPTCHA. Please try again')

        # end captcha verification
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        from_email = form.cleaned_data['from_email']
        message = form.cleaned_data['message']
        subject = form.cleaned_data['subject']
        subject = dict(form.fields['subject'].choices)[int(subject)]
        gender_id = request.POST['gender']
        gender_object = Gender.objects.get(pk=gender_id)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        from_email = request.POST['from_email']
        lesson_counter = 0
        #new_student = Student(gender=gender_object,
        #                      first_name=first_name,
        #                      last_name=last_name,
        #                      subject=subject_object,
        #                      lesson_count=lesson_counter)
        #new_student.save()
        subject = str(subject)
        now = datetime.datetime.now()
        today = now.date()
        student_context = {
            'first_name': first_name,
            'last_name': last_name,
            'today': today,
            'subject': subject,
            'from_email': from_email,
        }
        try:
            contact_mail_student(from_email, subject, message, student_context)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        context = {
            'form': form,
            'site_key': settings.RECAPTCHA_SITE_KEY,
        }
        return redirect('success_contact')
    return render(request, "contact/email.html", {'form': form})

def successView(request):
    return render(request, "contact/success.html")
