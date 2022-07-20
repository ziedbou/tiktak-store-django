from django import template

register = template.Library()

@register.simple_tag
def paginate(param, next):
    if next:
        next_page = param['page'] + 1
    else:
        next_page = param['page'] - 1

    return '/product-list/{}/{}/?page={}'.format(param['id'], param['slug'],next_page) 
