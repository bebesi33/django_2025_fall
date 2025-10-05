from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@stringfilter
@register.filter(name="choose_every_third")
def choose_every_third(value: str):
    return value[::3]
