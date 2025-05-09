from django.shortcuts import render, redirect
from datetime import datetime
from django.template import RequestContext
from django.db.models import Max

import random
import json

from school.models import MusicSchool
from events.models import Event
from teaching.models import Teacher
from gallery.models import Photo
from blog.models import BlogPost
from home.models import IndexText, Alert
from downloadsection.models import IndexDownload
# Create your views here.

def get_random_pic():
   max_id = Photo.objects.filter(category_id=1).aggregate(max_id=Max("id"))['max_id']
   if max_id is not None:
    while True:
        pk = random.randint(1, max_id)
        photo = Photo.objects.filter(category_id=1, pk=pk).first()
        if photo:
            return photo
    else:
        return None

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
    if school_data:
        name = school_data.school_name
        logo = school_data.school_logo
    else:
        name = None
        logo = None
    events = Event.objects.all()
    teachers = Teacher.objects.all()
    blog = BlogPost.objects.all().exclude(category__category__name="Kunstschule")[0:6]
    index_text = IndexText.objects.all().first()
    teacher_counter = len(teachers)
    middle_pic = get_random_pic()
    photos = get_photo_data()
    material_data = IndexDownload.objects.all()
    # Den aktiven Alert abrufen
    active_alert = Alert.objects.filter(is_active=True).first()  # Nur den ersten aktiven Alert anzeigen
    
    # Sticker Banner MKM_2025 aktivieren (9.5. - 10.5.2025)
    # ACHTUNG: Temporär auf True gesetzt für den Zeitraum 9.5. - 10.5.2025
    # Am 11.5.2025 auf folgenden Code umstellen:
    # today = datetime.now().date()
    # show_sticker = today.year == 2025 and today.month == 5 and (today.day == 9 or today.day == 10)
    show_sticker = True

    context = {
        'index_text': index_text,
        'blog': blog,
        'events': events,
        'material_data': material_data,
        'name': name,
        'logo': logo,
        'teacher_counter': teacher_counter,
        'middle_pic': middle_pic,
        'photos': photos,
        # Alert Mode
        'alert_message': active_alert.message if active_alert else None,
        'alert_title': active_alert.title if active_alert else None,
        # Sticker Banner
        'show_mkm_sticker': show_sticker,
        }
    return render(request, 'home/index.html', context)

def impressum (request):
    return render (request, 'home/impressum.html')

def history (request):
    return render (request, 'home/history.html')

def logo (request):
    return render (request, 'home/logo.html')

def view_404(request, *args, **kwargs):
    return redirect('home_view')
