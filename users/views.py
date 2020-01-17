from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect

from django.template import RequestContext
from school.models import MusicSchool
from events.models import Event
from events.forms import EventForm
from .forms import CustomUserCreationForm
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/team/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {
        'form': form
    })

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class HomePageView(TemplateView):
    template_name = 'users/home.html'

# Create your views here.

@login_required(login_url='/team/login/')
def eventView(request):
    events = Event.objects.all()
    try:
        event_id = request.GET['id']
        Event.objects.filter(id=event_id).delete()
    except MultiValueDictKeyError:
        pass
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            venue = request.POST['venue']
            date = request.POST['date']
            time = request.POST['time']
            new_event = Event(name=name,
                              venue=venue,
                              date=date,
                              time=time)
            new_event.save()
    else:
        form = EventForm()
    context = {
        'events': events,
        'form': form,
        }
    return render(request, 'users/events.html', context)
