from django import template

register = template.Library()

@register.filter
def percentage(value, total):
    try:
        return (value / total) * 100 if total else 0
    except (TypeError, ZeroDivisionError):
        return 0