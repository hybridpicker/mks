from django.shortcuts import render, redirect
from teaching.models import Teacher
from teaching.subject import SubjectCategory, Subject

def get_teachers_from_category(subject_name):
    i = 1
    for x in SubjectCategory.objects.get(name=subject_name).subject_set.all():
        ''''
        y = new query set
        '''
        z = x.teacher_set.all()
        if i > 1:
            y = y | z
        else:
            y = z
        i += 1
    return y

def show_teacher_view(request):
    categories = SubjectCategory.objects.all()
    teacher_picked = get_teachers_from_category("Zupfinstrumente")
    teacher_keys = get_teachers_from_category("Tasteninstrumente")

    context = {
        'categories': categories,
        'teacher_picked': teacher_picked,
        'teacher_keys': teacher_keys,
    }
    return render(request, 'teaching/all_teachers.html', context)
