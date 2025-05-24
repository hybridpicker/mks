# Add this to users/admin.py to manage 2FA notices through Django Admin
# No server restart required!

from django.contrib import admin
from django.db import models

class TwoFANotice(models.Model):
    """Admin-manageable 2FA promotional content"""
    title = models.CharField(max_length=200, default="Enhance Your Security")
    message = models.TextField(default="Two-Factor Authentication is now available!")
    is_active = models.BooleanField(default=True)
    show_until = models.DateTimeField(null=True, blank=True, help_text="Hide notice after this date")
    button_text = models.CharField(max_length=50, default="Enable 2FA")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "2FA Notice"
        verbose_name_plural = "2FA Notices"
    
    def __str__(self):
        return f"{self.title} ({'Active' if self.is_active else 'Inactive'})"

# Register in admin
@admin.register(TwoFANotice)
class TwoFANoticeAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'show_until', 'created_at']
    list_editable = ['is_active']
    list_filter = ['is_active', 'created_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'message', 'button_text')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'show_until')
        }),
    )
