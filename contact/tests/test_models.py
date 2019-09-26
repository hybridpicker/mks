from django.test import TestCase
from contact.models import ContactKeyword
from contact.forms import ContactForm
from django.utils.html import strip_tags
from contact.models import ContactKeyword
from contact.email import contact_mail_student, check_message
from django.core import mail

# Create your tests here.
class ContactKeywordTestCase(TestCase):
    def create_keyword(self, keyword="kosten", answer="Herzlichen Dank für Ihre Anfrage"):
        return ContactKeyword.objects.create()

    def test_keyword_creation(self):
        x = self.create_keyword()
        self.assertTrue(isinstance(x, ContactKeyword))
        self.assertEqual(x.__str__(), x.keyword)

class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail('Subject here', 'Here is the message.',
            'from@example.com', ['to@example.com'],
            fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')
