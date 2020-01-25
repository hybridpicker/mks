from django.shortcuts import render, redirect
from django.template import RequestContext
from django.db.models import Max

import random

from school.models import MusicSchool
from events.models import Event
from teaching.models import Teacher
from gallery.models import Photo
# Create your views here.

def get_random_pic():
   max_id = Photo.objects.filter(category_id=1).aggregate(max_id=Max("id"))['max_id']
   while True:
       pk = random.randint(1, max_id)
       photo = Photo.objects.filter(category_id=1, pk=pk).first()
       if photo:
           return photo

def home (request):
    school_data = MusicSchool.objects.all().first()
    name = school_data.school_name
    logo = school_data.school_logo
    events = Event.objects.all()
    teachers = Teacher.objects.all()
    teacher_counter = len(teachers)
    middle_pic = get_random_pic()
    context = {
        'events': events,
        'name': name,
        'logo': logo,
        'teacher_counter': teacher_counter,
        'middle_pic': middle_pic,
        }
    return render(request, 'home/index.html', context)

def impressum (request):
    return render (request, 'home/impressum.html')

def history (request):
    return render (request, 'home/history.html')

def view_404(request, *args, **kwargs):
    return redirect('home_view')
