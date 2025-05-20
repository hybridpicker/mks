"""
Django allauth compatibility fix for older versions

This code monkey-patches older allauth versions to provide the AccountMiddleware
that newer versions require, ensuring compatibility across different environments.
"""

import sys
import importlib.util

# Check if allauth.account.middleware exists
try:
    # Check if the middleware module exists
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
            import allauth.account
        
        # Add the middleware as an attribute to the account package
        allauth.account.middleware = middleware_module
        
except ImportError:
    # allauth is not installed, skip the compatibility fix
    pass
