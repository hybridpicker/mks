from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

class IndexText(models.Model):
    lead_paragraph = models.TextField(
        _("Lead paragraph"),
        blank=True)
    content = RichTextField(_("Content of Index page"), blank=True)

    def __str__(self):
        return 'IndexText'
        
    class Meta:
        verbose_name = u'Index Text'
        verbose_name_plural = u'Index Texts'


class Alert(models.Model):
    """
    Model for creating alert messages that appear on the homepage
    """
    title = models.CharField(_("Alert Title"), max_length=255, default="Untitled")
    message = models.TextField(_("Alert Message"))
    is_active = models.BooleanField(_("Active"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({'Active' if self.is_active else 'Inactive'})"
    
    class Meta:
        verbose_name = u'Alert'
        verbose_name_plural = u'Alerts'


class NewsItem(models.Model):
    """
    Simple news items for the homepage - alternative to blog posts
    """
    ICON_CHOICES = [
        ('music', 'Musik'),
        ('award', 'Auszeichnung'),
        ('calendar-alt', 'Kalender'),
        ('graduation-cap', 'Bildung'),
        ('users', 'Gruppe'),
        ('bullhorn', 'Ankündigung'),
        ('star', 'Wichtig'),
        ('info-circle', 'Information'),
    ]
    
    title = models.CharField(_("Title"), max_length=100)
    content = models.TextField(_("Content"), max_length=250)  # Kurzer Inhalt
    icon = models.CharField(_("Icon"), max_length=20, choices=ICON_CHOICES, default='info-circle')
    date_added = models.DateField(_("Date"), default=timezone.now)
    is_active = models.BooleanField(_("Active"), default=True)
    order = models.PositiveIntegerField(_("Display Order"), default=0)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = u'News Item'
        verbose_name_plural = u'News Items'
        ordering = ['-date_added', 'order']