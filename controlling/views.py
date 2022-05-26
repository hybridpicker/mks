from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.shortcuts import render, redirect

from students.models import Student, Parent
from home.models import IndexText
from controlling.forms import IndexForm, SingleStudentDataForm
from controlling.forms import SingleStudentDataFormCoordinator, ParentDataForm
from teaching.models import Teacher

from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
@login_required(login_url='/team/login/')
@staff_member_required
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
def get_all_students_coordinator(request):
    try:
        user_id = request.GET['user_id']
        category = Teacher.objects.get(user_id=user_id).subject_coordinator.all()
        category_id = category[0].id
        students = Student.objects.filter(subject__category=category_id)
        context = {
            'students': students,
            'category': category[0]
            }
    except Exception as e: 
        print(e)
        context = {'error': True}
    return render(request, 'controlling/all_students_coordinator.html', context)

@login_required(login_url='/team/login/')
@staff_member_required
def get_student(request):
    student_id = request.GET['id']
    student = Student.objects.get(id=student_id)
    parent = student.parent.id
    parent = Parent.objects.get(id=parent)
    if request.method == "POST":
        form = SingleStudentDataForm(request.POST, instance=student)
        parent_form = ParentDataForm(request.POST, instance=parent)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            parent = parent_form.save(commit=False)
            parent.save()
    else:
        form = SingleStudentDataForm(instance=student)
        parent_form = ParentDataForm(instance=parent)
    first_name = student.first_name
    last_name = student.last_name
    start_date = student.start_date

    # Model data
    context = {
                'first_name': first_name,
                'last_name': last_name,
                'start_date': start_date,
                'form': form,
                'parent_form': parent_form,
                }
    return render(request, 'controlling/single_student.html', context)

@login_required(login_url='/team/login/')
def get_student_coordinator(request):
    student_id = request.GET['id']
    student = Student.objects.get(id=student_id)
    if request.method == "POST":
        form = SingleStudentDataFormCoordinator(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
    else:
        form = SingleStudentDataFormCoordinator(instance=student)
    first_name = student.first_name
    last_name = student.last_name
    start_date = student.start_date
    subject = student.subject
    birth_date = student.birth_date
    note = student.note
    trial_lesson = student.trial_lesson
    teacher = student.teacher
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
                'note': note,
                'trial_lesson': trial_lesson,
                'teacher': teacher,
                'form': form,
                }
        
    return render(request, 'controlling/single_student_coordinator.html', context)

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