from django.shortcuts import render, redirect
from teaching.lesson_form import LessonForm

def prices_teaching_view(request):
    prices = LessonForm.objects.all()
    context = {
        'prices': prices,
    }
    return render(request, 'teaching/prices.html', context)
