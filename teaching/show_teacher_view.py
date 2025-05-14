from django.shortcuts import render, redirect
from django.db.models import Case, When, Value, IntegerField

from teaching.models import Teacher, GroupPhoto
from teaching.subject import SubjectCategory, Subject

def get_teachers_from_category(subject_name):
    i = 1
    y = None  # Initialisiere y
    from django.core.exceptions import ObjectDoesNotExist
    try:
        category = SubjectCategory.objects.get(name=subject_name)
        subjects = category.subject_set.all()
        
        if not subjects.exists():  # Wenn keine Subjects vorhanden sind
            from django.db.models import QuerySet
            return Teacher.objects.none()  # Leeres QuerySet zurückgeben
        
        for x in subjects:
            ''''
            y = new query set
            '''
            z = x.teacher_set.all()
            if i > 1:
                y = y | z
            else:
                y = z
            i += 1
        return y.distinct() if y is not None else Teacher.objects.none()
    except ObjectDoesNotExist:
        return Teacher.objects.none()  # Statt None ein leeres QuerySet zurückgeben
        
def show_teacher_view(request):
    group_photo = GroupPhoto.objects.all().first()
    categories = SubjectCategory.objects.all()
    teacher_picked = get_teachers_from_category("Zupfinstrumente")
    teacher_keys = get_teachers_from_category("Tasteninstrumente")
    teacher_strings = get_teachers_from_category("Streichinstrumente")
    teacher_brass = get_teachers_from_category("Blechblasinstrumente")
    teacher_drums = get_teachers_from_category("Schlagwerk")
    teacher_vocal = get_teachers_from_category("Gesang")
    teacher_wood = get_teachers_from_category("Holzblasinstrumente")
    teacher_dance = get_teachers_from_category("Tanz")
    
    # Retrieve the QuerySet for the Direktion group
    director_qs = get_teachers_from_category("Direktion")
    
    # Annotate each teacher with a flag 'is_director'
    director = director_qs.annotate(
        is_director=Case(
            # Use the correct field name: 'subject__subject'
            When(subject__subject="Direktion", then=Value(0)),
            default=Value(1),
            output_field=IntegerField()
        )
    ).order_by("is_director", "last_name")
    
    secretary = get_teachers_from_category("Sekretariat")
    elementary_teaching = get_teachers_from_category("Musikalische Früherziehung")
    
    context = {
        'group_photo': group_photo,
        'categories': categories,
        'director': director,
        'secretary': secretary,
        'teacher_picked': teacher_picked,
        'teacher_keys': teacher_keys,
        'teacher_strings': teacher_strings,
        'teacher_brass': teacher_brass,
        'teacher_drums': teacher_drums,
        'teacher_vocal': teacher_vocal,
        'teacher_wood': teacher_wood,
        'teacher_dance': teacher_dance,
        'elementary_teaching': elementary_teaching,
    }
    return render(request, 'teaching/all_teachers.html', context)

