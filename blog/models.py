from django.db import models
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from teaching.subject import Subject
from django.utils.translation import gettext as _
from django.utils import timezone
import datetime

class Author(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    image = models.ImageField(
        upload_to='blog/author/images',
        default='author_imageDefault', blank=True,)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:  # pylint: disable=too-few-public-methods
        '''
        Meta class for Author
        '''
        ordering = ('last_name',)
        verbose_name = u'Author'
        verbose_name_plural = u'Authors'

#Function for generating year-slug-string in view
def current_year():
    return datetime.date.today().year

class BlogPost(models.Model):
    title = models.CharField(max_length=120)
    lead_paragraph = models.TextField(blank=True)
    number_of_posts = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        blank=True, null=True)
    content = RichTextField()
    image = models.ImageField(upload_to='blog/posts/images/')
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        blank=True, null=True)
    date = models.DateField(_(u"Blog Post Date"), default=timezone.now, blank=True)
    published_year = models.IntegerField(_('Year of Article'), default=current_year)
    meta_title = models.CharField(max_length=60)
    meta_description = models.TextField()
    slug = models.SlugField(_("slug"), max_length=200, unique=True)

    def __str__(self):
        return '%s: #%s %s' % (self.category, self.number_of_posts, self.title)

    class Meta:  # pylint: disable=too-few-public-methods
        '''
        Meta class for BlogPosts
        '''
        ordering = ('category', 'number_of_posts')
        verbose_name = u'Blog Post'
        verbose_name_plural = u'Blog Posts'
