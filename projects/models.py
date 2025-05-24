from django.utils.translation import gettext as _
from django.db import models
from tinymce.models import HTMLField
from django.template.defaultfilters import slugify

class Project(models.Model):
    title = models.CharField(max_length=30)
    lead_paragraph = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='project/images/',
        default='project_imageDefault',
        blank=True)
    image_thumb = models.ImageField(
        upload_to='project/images/thumbnail',
        default='project_thumbnail_imageDefault',
        blank=True)
    image_lazy = models.ImageField(
        upload_to='project/images/lazy/',
        default='project_lazy_imageDefault',
        blank=True)
    logo = models.ImageField(
        upload_to='project/images/logo',
        default='project_logo_imageDefault',
        blank=True)
    description = HTMLField()
    press_text = models.TextField(blank=True)
    programm = models.TextField(blank=True)
    poster_img = models.ImageField(
        upload_to='project/images/poster',
        default='project_poster_imageDefault',
        blank=True)
    poster_img_thumb = models.ImageField(
        upload_to='project/images/poster/thumbnail',
        default='project_poster_thumbnail_imageDefault',
        blank=True)
    leader = models.ForeignKey(
            'teaching.Teacher',
            on_delete=models.CASCADE,
            blank=True, null=True)
    youtube_id_one = models.CharField(_(u'Youtube Video ID 1'),
        max_length=24, blank=True)
    youtube_id_two = models.CharField(_(u'Youtube Video ID 2'),
        max_length=24, blank=True)
    slug = models.SlugField(_("slug"), max_length=200,
        null=True,
        unique=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = u'Project'
        verbose_name_plural = u'Projects'
