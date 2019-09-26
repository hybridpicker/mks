import datetime

from django.test import TestCase
from django.urls import reverse
from blog.models import Author, BlogPost
from teaching.subject import Subject

# Create your tests here.

class BlogGuitarSummaryViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = Author.objects.create(first_name='Luke', last_name='Skywalker')
        subject = Subject.objects.create(subject='Gitarre')
        date = datetime.datetime.strptime('2018-09-17 14:00', '%Y-%m-%d %H:%M')
        #Create 13 Blog Posts TestCase
        number_of_blog_posts = 13
        for number_of_posts in range (number_of_blog_posts):
            BlogPost.objects.create(title='Warm Up', number_of_posts=f'{number_of_posts}', category_id=subject.id,
                                    date=date, slug=f'{number_of_posts}',
                                    content='Lorem Ipsum', image='eva.png', author_id=author.id,
                                    meta_title='Warm Up', meta_description='Lorem Ipsums')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('blog_guitar_summary'))
        self.assertEqual(response.status_code, 200)

    def test_view_templates(self):
        #Check actual Template
        response = self.client.get(reverse('blog_guitar_summary'))
        self.assertTemplateUsed(response, 'blog/summary.html')

    def blog_post_list_is_21(self):
        response = self.client.get(reverse('blog_guitar_summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('all_blogs' in response.context)
        self.assertTrue(len(response.context['all_blogs']) == 21)
