# myapp/templatetags/custom_filters.py
from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter
def first_line(value):
    text = strip_tags(value)
    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if line:
            return line
    return ''

@register.filter
def markdownify(text):
    return mark_safe(markdown.markdown(text, extensions=["extra", "fenced_code", "codehilite"])
)