from ckeditor.widgets import CKEditorWidget
from django.utils.translation import gettext as _
from django import forms

from home.models import IndexText
from students.models import Student, Parent

class IndexForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = IndexText
        fields = ['content', 'lead_paragraph']

class SingleStudentDataForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'birth_date', 'subject', 
                  'teacher', 'note', 'trial_lesson', 'parent', ]

class ParentDataForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['first_name', 'last_name', 'adress_line', 'house_number',
                'postal_code', 'city', 'email', 'phone']

class SingleStudentDataFormCoordinator(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['teacher', 'note', 'trial_lesson']