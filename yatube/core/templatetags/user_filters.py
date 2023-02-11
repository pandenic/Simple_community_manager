"""Model is used for user filters."""
from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """Add attributes to tags."""
    return field.as_widget(attrs={'class': css})
