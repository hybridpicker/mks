from django.apps import AppConfig
import sys
import importlib.util

class MksConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'mks'
    
    def ready(self):
        """
        Set up allauth compatibility when the app is ready.
        This ensures the compatibility middleware is available before any
        other apps try to import it.
        """
        # Check if allauth.account.middleware exists
        try:
            middleware_spec = importlib.util.find_spec('allauth.account.middleware')
            if middleware_spec is None:
                # The middleware module doesn't exist in this allauth version
                # Create a mock module with the AccountMiddleware
                import types
                
                # Create the middleware module
                middleware_module = types.ModuleType('allauth.account.middleware')
                
                # Define the AccountMiddleware class
                class AccountMiddleware:
                    """Compatibility middleware for django-allauth < 0.51.0"""
                    
                    def __init__(self, get_response):
                        self.get_response = get_response

                    def __call__(self, request):
                        response = self.get_response(request)
                        return response
                
                # Add the middleware to the module
                middleware_module.AccountMiddleware = AccountMiddleware
                
                # Inject the module into sys.modules
                sys.modules['allauth.account.middleware'] = middleware_module
                
                # Ensure the parent package exists
                if 'allauth.account' not in sys.modules:
                    try:
                        import allauth.account
                        # Add the middleware as an attribute to the account package
                        allauth.account.middleware = middleware_module
                    except ImportError:
                        # allauth.account doesn't exist, create it too
                        account_module = types.ModuleType('allauth.account')
                        account_module.middleware = middleware_module
                        sys.modules['allauth.account'] = account_module
                        
                        # Also ensure allauth exists
                        if 'allauth' not in sys.modules:
                            allauth_module = types.ModuleType('allauth')
                            allauth_module.account = account_module
                            sys.modules['allauth'] = allauth_module
                
        except ImportError:
            # allauth is not installed, skip the compatibility fix
            pass
