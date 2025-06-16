from django import template
register = template.Library()

@register.filter
def range_(value):
    return range(value)
