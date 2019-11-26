from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from school.models import MusicSchool
from events.models import Event
from teaching.models import Teacher

# Create your views here.

def home (request):
    school_data = MusicSchool.objects.all().first()
    name = school_data.school_name
    logo = school_data.school_logo
    events = Event.objects.all()
    teachers = Teacher.objects.all()
    teacher_counter = len(teachers)
    context = {
        'events': events,
        'name': name,
        'logo': logo,
        'teacher_counter': teacher_counter,
        }
    return render(request, 'home/index.html', context)

def impressum (request):
    return render (request, 'home/impressum.html')

def history (request):
    return render (request, 'home/history.html')

def sitemap (request):
    return render (request, 'sitemap.xml')

def view_404(request, *args, **kwargs):
    return redirect('home_view')
