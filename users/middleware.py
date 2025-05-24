"""
2FA Enforcement Middleware for MKS Portal
Forces users to setup 2FA after first login
"""

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext as _


class Enforce2FAMiddleware:
    """
    Middleware that enforces 2FA setup for all users
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs that don't require 2FA check
        self.exempt_urls = [
            '/team/login/',
            '/team/logout/',
            '/team/2fa/setup/',
            '/team/2fa/verify/',
            '/team/2fa/settings/',
            '/team/2fa/disable/',
            '/team/2fa/backup-codes/regenerate/',
            '/admin/',  # Django admin
            '/static/',  # Static files
            '/media/',   # Media files
        ]

    def __call__(self, request):
        # Process the request
        response = self.get_response(request)
        
        # Check if user needs 2FA setup
        if self.should_enforce_2fa(request):
            return redirect('users:2fa_setup')
        
        return response

    def should_enforce_2fa(self, request):
        """
        Determine if 2FA should be enforced for this request
        """
        # Skip if user is not authenticated
        if not request.user.is_authenticated:
            return False
        
        # Skip if URL is exempt
        if any(request.path.startswith(url) for url in self.exempt_urls):
            return False
        
        # Skip if user already has 2FA enabled
        if request.user.is_2fa_enabled:
            return False
        
        # Skip if user is on 2FA setup page
        if request.path in [reverse('users:2fa_setup'), reverse('users:2fa_settings')]:
            return False
        
        # Enforce 2FA for all authenticated users without 2FA
        return True


class TwoFactorSetupRedirectMiddleware:
    """
    Alternative middleware with more granular control
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs that are always accessible without 2FA
        self.always_allowed = [
            '/team/login/',
            '/team/logout/',
            '/team/2fa/',  # All 2FA URLs
            '/admin/',
            '/static/',
            '/media/',
        ]
        
        # URLs that require 2FA to be setup but not necessarily verified
        self.requires_2fa_setup = [
            '/team/',
            '/controlling/',
            '/blogedit/',
            '/galerie/',
        ]

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if we need to redirect to 2FA setup
        if self.needs_2fa_redirect(request):
            messages.warning(
                request, 
                _('Für die Sicherheit Ihres Kontos müssen Sie die Zwei-Faktor-Authentifizierung einrichten.')
            )
            return redirect('users:2fa_setup')
        
        return response

    def needs_2fa_redirect(self, request):
        """Check if user needs to be redirected to 2FA setup"""
        
        # Skip if not authenticated
        if not request.user.is_authenticated:
            return False
            
        # Skip if already has 2FA
        if request.user.is_2fa_enabled:
            return False
            
        # Skip always allowed URLs
        if any(request.path.startswith(url) for url in self.always_allowed):
            return False
            
        # Check if accessing protected area
        if any(request.path.startswith(url) for url in self.requires_2fa_setup):
            return True
            
        return False
