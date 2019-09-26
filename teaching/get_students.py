from django.shortcuts import render
from students.models import Student
from students.gender import Gender
from teaching.models import Teacher


# Create your views here.
def request_teacher_id(user):
    teacher = Teacher.objects.get(user=user)
    return teacher.id
    '''
    getting teacher_id from logged-in user
    '''

def get_all_students(request):
    teacher_id = request_teacher_id(request.user)
    students = Student.objects.filter(teacher=teacher_id)
    # Model data
    context = {
                'students': students,
                }
    return render(request, 'teaching/all_students.html', context)

def get_alibi_pic(image, gender, student):
    gender = str(gender)
    image_url = str(image)
    gender_male = Gender.objects.get(gender="Male")
    gender_female = Gender.objects.get(gender="Female")
    if image_url == '/media/student_imageDefault' and gender == str(gender_male):
        image = '/media/students/images/signup_male.jpg'
        return image
    elif image_url == '/media/student_imageDefault' and gender == str(gender_female):
        image = '/media/students/images/signup_female.png'
        return image
    else:
        image = student.image.url
        return image

def get_student(request):
    student_id = request.GET['student']
    student = Student.objects.get(id=student_id)
    gender = student.gender
    first_name = student.first_name
    last_name = student.last_name
    adressline = student.adress_line
    house_number = student.house_number
    postal_code = student.postal_code
    city = student.city
    location = student.location
    email = student.email
    country = student.country
    start_date = student.start_date
    lesson_form = student.lesson_form
    image = student.image.url
    image = get_alibi_pic(image, gender, student)
    # Model data
    context = {
                'first_name': first_name,
                'last_name': last_name,
                'image': image,
                'adressline': adressline,
                'house_number': house_number,
                'postal_code': postal_code,
                'city': city,
                'postal_code': postal_code,
                'location': location,
                'email': email,
                'country': country,
                'start_date': start_date,
                'lesson_form': lesson_form,
                }
    return render(request, 'teaching/single_student.html', context)
