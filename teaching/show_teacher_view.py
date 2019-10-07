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
    teacher_strings = get_teachers_from_category("Streichinstrumente")
    teacher_brass = get_teachers_from_category("Blechblasinstrumente")
    teacher_drums = get_teachers_from_category("Schlagwerk")
    teacher_vocal = get_teachers_from_category("Gesang")
    teacher_wood = get_teachers_from_category("Holzblasinstrumente")

    context = {
        'categories': categories,
        'teacher_picked': teacher_picked,
        'teacher_keys': teacher_keys,
        'teacher_strings': teacher_strings,
        'teacher_brass': teacher_brass,
        'teacher_drums': teacher_drums,
        'teacher_vocal': teacher_vocal,
        'teacher_wood': teacher_wood,
    }
    return render(request, 'teaching/all_teachers.html', context)
