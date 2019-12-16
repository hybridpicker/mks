from django.db import models
from django.utils.translation import gettext as _

class PhotoCategory(models.Model):
    title = models.CharField(_(u'Project Name'), max_length=50)

    def __str__(self):
        return str(self.title)

    class Meta:
        '''
        Meta class for PhotoCategory
        '''
        ordering = ['title']
        verbose_name = u'Photo Category'
        verbose_name_plural = u'Photo Categories'

class Photo(models.Model):
    title = models.CharField(_(u'Title of the Photo'), max_length=50)
    image = models.ImageField(
        upload_to='gallery/images/',
        default='gallery_imageDefault', blank=True)
    image_thumbnail = models.ImageField(
        upload_to='gallery/images/thumbnail',
        default='gallery_thumbnail_imageDefault', blank=True)
    image_lazy = models.ImageField(
        upload_to='gallery/images/lazy/',
        default='gallery_lazy_imageDefault', blank=True)
    description = models.TextField(null=True, blank=True, max_length=120)
    ordering = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(
        PhotoCategory,
        on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '%s: %s' % (self.category, self.title)

    class Meta:
        '''
        Meta class for Photo
        '''
        ordering = ['category','-ordering']
        verbose_name = u'Photo'
        verbose_name_plural = u'Photos'
