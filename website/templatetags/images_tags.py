from django import template

register = template.Library()

@register.filter
def imghttps(link):
    if isinstance(link, str) and 'localhost' not in link:
        return link.replace('http:', 'https:')
    else :
        return link
   