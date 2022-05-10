import re
import urllib.request
import json
import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core import mail
from django.core.mail.message import BadHeaderError
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse, HttpResponseRedirect

from .models import Student, Parent
from .forms import SignInForm
from teaching.subject import Subject

def mail_new_student(from_email, student_context, send_mail=True):
    '''
    Preparing Mail to RECEIVER
    '''
    subject = 'Wir haben einen neue Anmeldung'
    name = student_context.get('first_name') + ' ' + student_context.get('last_name')
    today = student_context.get('today')
    instrument = student_context.get('instrument')
    html_message = render_to_string('templates/mail/new_student_template.html',
                                    {'context': 'values',
                                     'name': name,
                                     'today': today,
                                     'instrument': instrument})
    plain_message = strip_tags(html_message)
    to = settings.EMAIL_USER_RECEIVER

    if send_mail:

        """
        #TODO: get attachment to automate message
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        '''
        Preparing Mail to Student
        '''
        subject = 'Musikschule St. Pölten Anmeldung'
        to = student_context.get('from_email')
        if student_context.get('instrument') == "Musikalische Früherziehung":
            html_message = render_to_string('templates/mail/answer_mail_template_eme.html',
                                            {'context': 'values',})
        else:
            html_message = render_to_string('templates/mail/answer_mail_template_music.html',
                                            {'context': 'values',})
        plain_message = strip_tags(html_message)
        # Sending to User
        to = settings.EMAIL_USER_RECEIVER
        """

        '''
        Sending Message to music_school
        '''
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

    return html_message


def signInView(request):
    form = SignInForm(request.POST)
    public_key = settings.RECAPTCHA_SITE_KEY
    if request.method == 'POST':
        form = SignInForm(request.POST)
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
            '''
            Clean data
            '''
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            from_email = form.cleaned_data['from_email']
            subject = form.cleaned_data['subject']
            adress_line = form.cleaned_data['adress_line']
            house_number = form.cleaned_data['house_number']
            postal_code = form.cleaned_data['postal_code']
            city = form.cleaned_data['city']
            email = form.cleaned_data['from_email']
            parent_first_name = request.POST['parent_first_name']
            parent_last_name = request.POST['parent_last_name']
            phone = request.POST['phone']
            '''
            Request Data
            '''
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            parent_first_name = request.POST['parent_first_name']
            parent_last_name = request.POST['parent_last_name']
            from_email = request.POST['from_email']
            birthdate_year = request.POST['birthdate_year']
            birthdate_month = request.POST['birthdate_month']
            birthdate_day = request.POST['birthdate_day']
            adress_line = request.POST['adress_line']
            subject = form.cleaned_data['subject'].id
            house_number = request.POST['house_number']
            postal_code = request.POST['postal_code']
            city = request.POST['city']
            email = request.POST['from_email']
            phone = request.POST['phone']
            date_string = birthdate_month + ' ' + birthdate_day + ' ' + birthdate_year
            birthdate = datetime.datetime.strptime(date_string, '%m %d %Y')
            new_parent = Parent(first_name=parent_first_name,
                                last_name=parent_last_name,
                                house_number=house_number,
                                postal_code=postal_code,
                                adress_line=adress_line,
                                city=city,
                                email=email,
                                phone=phone)
            new_parent.save()
            new_student = Student(first_name=first_name,
                                  last_name=last_name,
                                  birth_date=birthdate,
                                  subject_id=subject,
                                  parent_id=new_parent.id)
            new_student.save()
            '''
            After Saving Student send Message
            '''
            now = datetime.datetime.now()
            today = now.date()
            instrument = Subject.objects.get(id=subject).subject
            student_context = {
                'first_name': first_name,
                'last_name': last_name,
                'instrument': instrument,
                'today': today,
                'from_email': from_email,
            }
            from_email = settings.EMAIL_HOST_USER
            try:
                mail_new_student(from_email, student_context, send_mail=True)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('student_successfully_saved')
    else:
        form = SignInForm()
    return render(request, "students/signin.html", {'form':form, 'public_key': public_key})

def successView(request):
    return render(request, "students/success.html")
