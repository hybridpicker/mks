from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.
def home (request):
    return render(request, 'home/index.html')

def impressum (request):
    return render (request, 'home/impressum.html')

def sitemap (request):
    return render (request, 'sitemap.xml')

def view_404(request, *args, **kwargs):
    return redirect('home_view')
