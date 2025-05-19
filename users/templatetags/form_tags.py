from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Add CSS class to form field widget"""
    if field.field.widget.attrs.get('class'):
        field.field.widget.attrs['class'] += ' ' + css_class
    else:
        field.field.widget.attrs['class'] = css_class
    return field