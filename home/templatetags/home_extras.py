from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """
    Splits the value by the argument and returns a list.
    Usage: {{ value|split:"separator" }}
    """
    return value.split(arg)
