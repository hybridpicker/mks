from teaching.models import Teacher

def save_teachers():
    for line in open('teacher.txt'):
       line = line.split(" | ")
       gender = line[0]
       first_name = line[1]
       last_name = line[2]

       Teacher.objects.create(gender_id=gender,
                              first_name=first_name,
                              last_name=last_name)
