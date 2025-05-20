"""
Compatibility middleware for django-allauth 0.50.0

This provides a dummy AccountMiddleware that does nothing,
but satisfies allauth's requirement for the middleware to be present.
"""

class AccountMiddleware:
    """Dummy middleware for compatibility with allauth 0.50.0"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Do nothing - this is just for compatibility
        response = self.get_response(request)
        return response
