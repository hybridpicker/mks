import re
import urllib.request
import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse, HttpResponseRedirect

from .models import Student
from .forms import SignInForm

def signInView(request):
    form = SignInForm(request.POST)
    public_key = settings.RECAPTCHA_SITE_KEY
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
        subject = form.cleaned_data['subject']
        subject = dict(form.fields['subject'].choices)[int(subject)]
        adress_line = form.cleaned_data['adress_line']
        house_number = form.cleaned_data['house_number']
        postal_code = form.cleaned_data['postal_code']
        city = form.cleaned_data['city']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        from_email = request.POST['from_email']
        adress_line = request.POST['adress_line']
        house_number = request.POST['house_number']
        postal_code = request.POST['postal_code']
        city = request.POST['city']
        new_student = Student(first_name=first_name,
                              last_name=last_name,
                        #      subject=subject,
                              adress_line=adress_line,
                              house_number=house_number,
                              postal_code=postal_code,
                              city=city)
        new_student.save()
        return redirect('successfully_saved')
    return render(request, "students/signin.html", {'form':form, 'public_key': public_key})

def successView(request):
    return render(request, "students/success.html")
