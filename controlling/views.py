from django.shortcuts import render

from students.models import Student

# Create your views here.

def get_all_students(request):
    students = Student.objects.all()

    # Model data
    context = {
        'students': students,
        }
    return render(request, 'controlling/all_students.html', context)

def get_student(request):
    student_id = request.GET['id']
    student = Student.objects.get(id=student_id)
    first_name = student.first_name
    last_name = student.last_name
    adressline = student.adress_line
    house_number = student.house_number
    postal_code = student.postal_code
    city = student.city
    email = student.email
    start_date = student.start_date
    subject = student.subject
    # Model data
    context = {
                'first_name': first_name,
                'last_name': last_name,
                'adressline': adressline,
                'house_number': house_number,
                'postal_code': postal_code,
                'city': city,
                'postal_code': postal_code,
                'email': email,
                'start_date': start_date,
                'subject': subject,
                }
    return render(request, 'controlling/single_student.html', context)
