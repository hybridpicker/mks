from django.apps import AppConfig
import sys
import importlib.util

class MksConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'mks'
    verbose_name = 'MKS Project Configuration'
    
    def ready(self):
        """
        Set up allauth compatibility when the app is ready.
        This ensures the compatibility middleware is available before any
        other apps try to import it.
        """
        self._setup_allauth_compatibility()
    
    def _setup_allauth_compatibility(self):
        """Setup allauth middleware compatibility for older versions."""
        try:
            # Check if allauth.account.middleware already exists
            middleware_spec = importlib.util.find_spec('allauth.account.middleware')
            if middleware_spec is not None:
                # Middleware already exists, no need for compatibility
                return
            
            # Try to import allauth to see if it's installed
            try:
                import allauth
            except ImportError:
                # allauth is not installed, no need for compatibility
                return
            
            # Create compatibility middleware for older allauth versions
            import types
            
            # Create the middleware module
            middleware_module = types.ModuleType('allauth.account.middleware')
            
            # Define the AccountMiddleware class for compatibility
            class AccountMiddleware:
                """
                Compatibility middleware for django-allauth < 0.51.0
                
                This middleware does nothing but provides the expected interface
                that newer Django configurations expect when using allauth.
                """
                
                def __init__(self, get_response):
                    self.get_response = get_response

                def __call__(self, request):
                    response = self.get_response(request)
                    return response
            
            # Add the middleware class to the module
            middleware_module.AccountMiddleware = AccountMiddleware
            
            # Inject the module into sys.modules so it can be imported
            sys.modules['allauth.account.middleware'] = middleware_module
            
            # Try to set it as an attribute on allauth.account if it exists
            try:
                import allauth.account
                allauth.account.middleware = middleware_module
            except (ImportError, AttributeError):
                # allauth.account doesn't exist or can't be modified
                # The sys.modules injection should be sufficient
                pass
                
        except Exception as e:
            # Log the error but don't fail the app startup
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Failed to setup allauth compatibility: {e}")
