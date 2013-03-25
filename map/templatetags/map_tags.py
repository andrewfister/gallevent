from django import template

register = template.Library()

@register.inclusion_tag("map.html")
def show_map():
    return {}

