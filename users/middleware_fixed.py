# Verbesserte Middleware - ersetzt den Inhalt in users/middleware.py

"""
2FA Enforcement Middleware for Musik- und Kunstschule St. Pölten
Fixed version to prevent redirect loops after successful 2FA setup
"""

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext as _


class TwoFactorSetupRedirectMiddleware:
    """
    Fixed middleware that prevents redirect loops after 2FA setup
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs that are always accessible without 2FA
        self.always_allowed = [
            '/team/login/',
            '/team/logout/',
            '/team/2fa/',  # All 2FA URLs - wichtig!
            '/admin/',
            '/static/',
            '/media/',
        ]
        
        # URLs that require 2FA to be setup
        self.requires_2fa_setup = [
            '/team/',
            '/controlling/',
            '/blogedit/',
            '/galerie/',
        ]

    def __call__(self, request):
        # WICHTIG: Prüfe ZUERST ob Redirect nötig ist, dann erst Response verarbeiten
        if self.needs_2fa_redirect(request):
            messages.warning(
                request, 
                _('Für die Sicherheit Ihres Kontos müssen Sie die Zwei-Faktor-Authentifizierung einrichten.')
            )
            return redirect('users:2fa_setup')
        
        # Nur wenn kein Redirect nötig ist, normale Response verarbeiten
        response = self.get_response(request)
        return response

    def needs_2fa_redirect(self, request):
        """Check if user needs to be redirected to 2FA setup"""
        
        # Skip if not authenticated
        if not request.user.is_authenticated:
            return False
            
        # Skip if already has 2FA - DB-Check mit Refresh
        try:
            # Refresh user from DB to get latest state
            request.user.refresh_from_db()
            if request.user.is_2fa_enabled:
                return False
        except:
            # If refresh fails, assume no 2FA
            pass
            
        # Skip always allowed URLs (erweitert für 2FA-Pfade)
        if any(request.path.startswith(url) for url in self.always_allowed):
            return False
            
        # WICHTIG: Skip auch für erfolgreiche 2FA-Setup Response
        if '/2fa/' in request.path:
            return False
            
        # Check if accessing protected area
        if any(request.path.startswith(url) for url in self.requires_2fa_setup):
            return True
            
        return False


# Behalte die alte Middleware als Backup
class Enforce2FAMiddleware:
    """
    Original middleware - nicht verwenden, nur als Backup
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
