from django.db import models
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from teaching.subject import Subject
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import datetime
from sorl.thumbnail import ImageField

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
    category = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,  # Verhindert das Löschen von Blogposts, wenn die Kategorie entfernt wird
        blank=True, null=True
    )
    content = RichTextField()
    image = models.ImageField(upload_to='blog/posts/images/', blank=True, null=True)  # Bild optional
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,  # Optionaler Autor
        blank=True, null=True
    )
    date = models.DateField(_("Blog Post Date"), default=timezone.now, blank=True)
    meta_title = models.CharField(max_length=60)
    meta_description = models.TextField()
    slug = models.SlugField(_("slug"), max_length=200, unique=True)
    ordering = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.published_year:
            self.published_year = current_year()  # Standardwert setzen
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.date.year})"

    class Meta:
        ordering = ('category', '-date', 'ordering')
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
