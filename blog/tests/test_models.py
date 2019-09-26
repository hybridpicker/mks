import datetime

from django.test import TestCase
from django.urls import reverse
from blog.models import Author, BlogPost
from teaching.subject import Subject

class AuthorModelCase(TestCase):
    def create_author(self, first_name='Luke', last_name='Skywalker'):
        return Author.objects.create()

    def test_keyword_creation(self):
        x = self.create_author()
        self.assertTrue(isinstance(x, Author))
        self.assertEqual(x.__str__(), (x.first_name) + ' ' + x.last_name)

class BlogPostCreationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = Author.objects.create(first_name='Luke', last_name='Skywalker')
        subject = Subject.objects.create(subject='Gitarre')
        date = datetime.datetime.strptime('2018-09-17 14:00', '%Y-%m-%d %H:%M')
        BlogPost.objects.create(title='Warm Up', number_of_posts=12, category_id=subject.id,
                                date=date,
                                content='Lorem Ipsum', image='eva.png', author_id=author.id,
                                meta_title='Warm Up', meta_description='Lorem Ipsums')

    def test_student_creation(self):
        blog_post = BlogPost.objects.get(title='Warm Up')
        self.assertTrue(isinstance(blog_post, BlogPost))
        self.assertEqual(blog_post.__str__(), (str(blog_post.category) + ': #' + str(blog_post.number_of_posts) + ' ' + blog_post.title))
