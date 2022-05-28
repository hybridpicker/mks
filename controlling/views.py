from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import datetime

from django.shortcuts import render, redirect

from students.models import Student, Parent
from home.models import IndexText
from controlling.forms import IndexForm, SingleStudentDataForm
from controlling.forms import SingleStudentDataFormCoordinator, ParentDataForm
from teaching.models import Teacher
from students.forms import SignInForm
from teaching.models import SubjectCategory

from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
@login_required(login_url='/team/login/')
@staff_member_required
def get_all_students(request):
    students = Student.objects.all().order_by('-start_date')
    categories = SubjectCategory.objects.all().exclude(hidden=True)
    try:
        student_id = request.GET['id']
        Student.objects.filter(id=student_id).delete()
    except MultiValueDictKeyError:
        pass
    try:
        category_id = request.GET['category']
        students = Student.objects.filter(subject__category=category_id)
    except MultiValueDictKeyError:
        pass

    # Model data
    context = {
        'students': students,
        'categories': categories,
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
    parent_id = student.parent.id
    parent = Parent.objects.get(id=parent_id)
    parent_name = parent.first_name + ' ' + parent.last_name
    if request.method == "POST":
        form = SingleStudentDataForm(request.POST, instance=student)
        parent_form = ParentDataForm(request.POST, instance=parent)
        if form.is_valid():
            student = form.save()
            student.save()
        if parent_form.is_valid():
            parent = parent_form.save(commit=False)
            parent.save()
        return redirect('get_controlling_students')
    else:
        form = SingleStudentDataForm(instance=student)
        parent_form = ParentDataForm(instance=parent)

    start_date = student.start_date

    # Model data
    context = {
                'start_date': start_date,
                'form': form,
                'parent_form': parent_form,
                'parent_id': parent_id,
                'parent_name': parent_name,
                }
    return render(request, 'controlling/single_student.html', context)

@login_required(login_url='/team/login/')
@staff_member_required
def get_parent(request):
    parent_id = request.GET['id']
    parent = Parent.objects.get(id=parent_id)
    if request.method == "POST":
        form = ParentDataForm(request.POST, instance=parent)
        if form.is_valid():
            parent = form.save(commit=False)
            parent.save()
        return redirect('get_controlling_students')
    else:
        form = ParentDataForm(instance=parent)

    # Model data
    context = {
                'form': form,
                }
    return render(request, 'controlling/single_parent.html', context)

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

@login_required(login_url='/team/login/')
@staff_member_required
def newStudentView(request):
    form = SignInForm(request.POST)
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            '''
            Clean data
            '''
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            from_email = form.cleaned_data['from_email']
            subject = form.cleaned_data['subject']
            adress_line = form.cleaned_data['adress_line']
            house_number = form.cleaned_data['house_number']
            postal_code = form.cleaned_data['postal_code']
            city = form.cleaned_data['city']
            email = form.cleaned_data['from_email']
            parent_first_name = request.POST['parent_first_name']
            parent_last_name = request.POST['parent_last_name']
            phone = request.POST['phone']
            '''
            Request Data
            '''
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            parent_first_name = request.POST['parent_first_name']
            parent_last_name = request.POST['parent_last_name']
            from_email = request.POST['from_email']
            birthdate_year = request.POST['birthdate_year']
            birthdate_month = request.POST['birthdate_month']
            birthdate_day = request.POST['birthdate_day']
            adress_line = request.POST['adress_line']
            subject = form.cleaned_data['subject'].id
            house_number = request.POST['house_number']
            postal_code = request.POST['postal_code']
            city = request.POST['city']
            email = request.POST['from_email']
            phone = request.POST['phone']
            date_string = birthdate_month + ' ' + birthdate_day + ' ' + birthdate_year
            birthdate = datetime.datetime.strptime(date_string, '%m %d %Y')
            new_parent = Parent(first_name=parent_first_name,
                                last_name=parent_last_name,
                                house_number=house_number,
                                postal_code=postal_code,
                                adress_line=adress_line,
                                city=city,
                                email=email,
                                phone=phone)
            new_parent.save()
            new_student = Student(first_name=first_name,
                                  last_name=last_name,
                                  birth_date=birthdate,
                                  subject_id=subject,
                                  parent_id=new_parent.id)
            new_student.save()
            return redirect('new_student_saved')
    else:
        form = SignInForm()
    return render(request, "controlling/new_student.html", {'form':form})

@login_required(login_url='/team/login/')
@staff_member_required
def newStudentSuccessView(request):
    return render(request, "controlling/new_student_success.html")