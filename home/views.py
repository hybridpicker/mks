from django.shortcuts import render, redirect
from django.template import RequestContext
from django.db.models import Max

import random
import json

from school.models import MusicSchool
from events.models import Event
from teaching.models import Teacher
from gallery.models import Photo
from blog.models import BlogPost
# Create your views here.

def get_random_pic():
   max_id = Photo.objects.filter(category_id=1).aggregate(max_id=Max("id"))['max_id']
   while True:
       pk = random.randint(1, max_id)
       photo = Photo.objects.filter(category_id=1, pk=pk).first()
       if photo:
           return photo

def get_photo_data():
    photo_data = {}
    photos = Photo.objects.filter(category_id=1)
    i = 0
    for photo in photos:
        photo_data[i] = photo.image.url
        i += 1
    return photo_data


def home (request):
    school_data = MusicSchool.objects.all().first()
    name = school_data.school_name
    logo = school_data.school_logo
    events = Event.objects.all()
    teachers = Teacher.objects.all()
    blog = BlogPost.objects.all().order_by('-date')[0:3]
    teacher_counter = len(teachers)
    middle_pic = get_random_pic()
    photos = get_photo_data()
    context = {
        'blog': blog,
        'events': events,
        'name': name,
        'logo': logo,
        'teacher_counter': teacher_counter,
        'middle_pic': middle_pic,
        'photos': photos,
        }
    return render(request, 'home/index.html', context)

def impressum (request):
    return render (request, 'home/impressum.html')

def history (request):
    return render (request, 'home/history.html')

def view_404(request, *args, **kwargs):
    return redirect('home_view')
