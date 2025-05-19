from django.shortcuts import render, redirect
from faq.models import FAQ
from faq.forms import FaqForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def faq_view (request):
    faqs = FAQ.objects.all()
    context = {
        'faqs': faqs,
    }
    return render (request, 'faq/faq.html', context)

@login_required(login_url='/team/login/')
def get_faq(request):
#    faqs = FAQ.objects.all().first()
    faqs = request.GET['pk']
    faqs = FAQ.objects.get(pk=faqs)
    if request.method == "POST":
        form = FaqForm(request.POST, instance=faqs)
        if form.is_valid():
            faq = form.save(commit=False)
            faq.save()
            return redirect('get_all_faqs')
    else:
        form = FaqForm(instance=faqs)
    # Model data
    context = {
        'form': form,
        }
    return render(request, 'faq/faq_form.html', context)

@login_required(login_url='/team/login/')
def create_faq(request):
    if request.method == "POST":
        form = FaqForm(request.POST)
        if form.is_valid():
            faq = form.save(commit=False)
            faq.save()
            return redirect('get_all_faqs')
    else:
        form = FaqForm()
    # Model data
    context = {
        'form': form,
        'is_new': True,
        }
    return render(request, 'faq/faq_form.html', context)

@login_required(login_url='/team/login/')
def get_all_faqs(request):
    faqs = FAQ.objects.all()
    context ={
        'faqs': faqs,
    }
    return render (request, 'faq/all_edit.html', context)