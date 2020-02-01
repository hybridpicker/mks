from django.utils.translation import gettext as _
from django import forms

from todo.models import TodoList

class PriorityForm(forms.ModelForm):

    def __init__(self, *args, **kargs):
        super(PriorityForm, self).__init__(*args, **kargs)

    class Meta:
         model = TodoList
         fields = '__all__'
