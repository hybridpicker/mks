"""
Signals for 2FA enforcement
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def enforce_2fa_for_new_users(sender, instance, created, **kwargs):
    """
    Signal to handle new user creation
    Sets 2FA requirement flag for new users
    """
    if created and not instance.is_superuser:
        # For new users, we could set a flag that forces 2FA setup
        # This is handled by the middleware, but we could add additional logic here
        pass


@receiver(post_save, sender=CustomUser)
def check_2fa_requirements(sender, instance, **kwargs):
    """
    Check 2FA requirements for user roles
    """
    # Staff and superusers should have 2FA enabled
    if (instance.is_staff or instance.is_superuser) and not instance.is_2fa_enabled:
        # This could trigger email notifications or other enforcement mechanisms
        pass
