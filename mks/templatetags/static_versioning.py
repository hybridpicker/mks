from django import template
from django.templatetags.static import static
import time

register = template.Library()

@register.simple_tag
def versioned_static(path):
    """
    Add a version query parameter to the static file URL to bust cache.
    The version is the current timestamp to ensure browsers always load the latest version.
    """
    version = int(time.time())
    static_url = static(path)
    return f"{static_url}?v={version}"
