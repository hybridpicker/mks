from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from students.models import Student
from home.models import IndexText
from controlling.forms import IndexForm
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
@login_required(login_url='/team/login/')
def get_all_students(request):
    students = Student.objects.all().order_by('-start_date')
    try:
        student_id = request.GET['id']
        Student.objects.filter(id=student_id).delete()
    except MultiValueDictKeyError:
        pass

    # Model data
    context = {
        'students': students,
        }
    return render(request, 'controlling/all_students.html', context)

@login_required(login_url='/team/login/')
def get_student(request):
    student_id = request.GET['id']
    student = Student.objects.get(id=student_id)
    first_name = student.first_name
    last_name = student.last_name
    start_date = student.start_date
    subject = student.subject
    birth_date = student.birth_date
    '''
    Parent data
    '''
    parent_first_name = student.parent.first_name
    parent_last_name = student.parent.last_name
    adressline = student.parent.adress_line
    house_number = student.parent.house_number
    postal_code = student.parent.postal_code
    city = student.parent.city
    email = student.parent.email
    parent_phone = student.parent.phone
    # Model data
    context = {
                'first_name': first_name,
                'last_name': last_name,
                'start_date': start_date,
                'birth_date': birth_date,
                'subject': subject,
                'parent_first_name': parent_first_name,
                'parent_last_name': parent_last_name,
                'adressline': adressline,
                'house_number': house_number,
                'postal_code': postal_code,
                'city': city,
                'postal_code': postal_code,
                'email': email,
                'parent_phone': parent_phone,
                }
    return render(request, 'controlling/single_student.html', context)

@login_required(login_url='/team/login/')
def get_index_text(request):
    text = IndexText.objects.all().first()
    if request.method == "POST":
        form = IndexForm(request.POST, instance=text)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.save()
            return redirect('home_view')
    else:
        form = IndexForm(instance=text)
    # Model data
    context = {
        'form': form,
        }
    return render(request, 'controlling/index_form.html', context)
