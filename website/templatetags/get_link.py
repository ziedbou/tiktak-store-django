from django import template
# from slugify import slugify
from django.template.defaultfilters import slugify

register = template.Library()

@register.filter
def get_link(item):

    try:
        cat_slug = item.get('cat_slug')
        slug = item.get('slug')
        _id = str(item.get('id', ''))
        cat_id = str(item.get('cat_id', ''))

        if not slug:
            slug = slugify(item['label'])

        if not cat_slug:
            cat_slug = 'category-'+item['label']

        #IF IS CATEGORY MENU
        if item['type'] == "category":
          return '/product-list/{}/{}/'.format(_id, slug)

        #IF IS PAGE MENU
        elif item['type'] == "page":
            if item['is_home']:
                return '/'
            else:
                return '/page/{}/{}'.format(_id, slug)

        #IF IS PRODUCT MENU
        elif item['type'] == "product":
            return '/product/{}/{}/{}/{}'.format(cat_id, cat_slug, _id, slug ) 

        return ''
    except Exception as e:

        return ''




