import re
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import ContactKeyword


'''
Contact Student
'''
def check_message(message):
    words = re.findall("\w+",message)
    keywords = ContactKeyword.objects.all()
    for keyword in ContactKeyword.objects.all():
        if keyword.keyword in words:
            answer_keyword = ContactKeyword.objects.get(keyword__contains=keyword)
            answer = answer_keyword.answer
            return answer

def contact_mail_student(to, message, student_context, send_mail=True):
    from_email = settings.EMAIL_HOST_USER
    '''
    Preparing Mail to USER
    '''
    subject = 'Ihre Anfrage ist bei uns eingegangen - Musikschule St. Pölten'
    message = message
    answer = check_message(message)
    name = student_context.get('first_name') + ' ' + student_context.get('last_name')
    location = student_context.get('location')
    today = student_context.get('today')
    if answer == None:
        answer = ''
    html_message = render_to_string('templates/mail/answer_mail_template.html',
                                    {'context': 'values',
                                     'message': message, 'answer': answer})
    plain_message = strip_tags(html_message)

    if send_mail:
        # Sending Message to Student
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        '''
        Preparing Mail to Us
        '''
        subject = 'Neue Anfrage'
        customer_email = student_context.get('from_email')
        html_message = render_to_string('templates/mail/mail_template.html',
                                        {'context': 'values', 'name': name,
                                         'location': location, 'today': today,
                                         'customer_email': customer_email,
                                         'message': message, 'answer': answer})
        plain_message = strip_tags(html_message)
        # Sending to User
        to = settings.EMAIL_USER_RECEIVER
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    return html_message
