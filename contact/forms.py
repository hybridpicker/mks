from django.utils.translation import gettext as _
from django import forms
from teaching.lesson_form import LessonForm
from teaching.subject import Subject
from students.gender import Gender
from teaching.models import Teacher

def get_subject_choices():
    all_teachers = Teacher.objects.all()
    subject_dir = []
    for teacher in all_teachers:
        if ',' in str(teacher.subject):
            print(',')
            duplicate_teacher = str(teacher.subject).split(", ")
            for teacher in duplicate_teacher:
                subject_dir.append(str(teacher))
        else:
            subject_dir.append(str(teacher.subject))
    subject_dir = list(dict.fromkeys(subject_dir))
    subject_dir.sort()
    index = 1
    result = []
    for item in subject_dir:
        result.append((index, item))
        index += 1
    return tuple(result)

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    from_email = forms.EmailField(label="E-Mailadresse", max_length=100, required=True)
    message = forms.CharField(label="Nachricht",widget=forms.Textarea, required=False)
    subject = forms.ChoiceField(required=False,
                                choices=get_subject_choices,
                                widget=forms.Select)
