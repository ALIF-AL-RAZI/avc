from django import template

register = template.Library()

@register.simple_tag
def text(name, css_class='', label=''):
    """
    Renders a text input field with the specified name, CSS class, and label.
    """
    return f'<input type="text" name="{name}" class="{css_class}" placeholder="{label}">'