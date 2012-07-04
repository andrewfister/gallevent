from django import template

from gallevent.event import models

register = template.Library()

@register.inclusion_tag("map.html")
def show_map():
    return {}

