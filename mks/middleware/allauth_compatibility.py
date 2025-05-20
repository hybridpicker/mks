"""
Compatibility middleware for django-allauth

This middleware automatically detects the installed allauth version and either
provides a dummy AccountMiddleware for older versions (< 0.51.0) or imports
the real middleware for newer versions.
"""

try:
    # Try to import the real middleware from newer allauth versions
    from allauth.account.middleware import AccountMiddleware
except ImportError:
    # Fallback for older allauth versions that don't have the middleware
    class AccountMiddleware:
        """Dummy middleware for compatibility with allauth < 0.51.0"""
        
        def __init__(self, get_response):
            self.get_response = get_response

        def __call__(self, request):
            # Do nothing - this is just for compatibility
            response = self.get_response(request)
            return response

# Make the middleware available under the expected name
__all__ = ['AccountMiddleware']
