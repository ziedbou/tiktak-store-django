from django import template
from slugify import slugify

register = template.Library()

@register.filter
def get_prod_link(product):
    try:
        category = product.get('_category', {})
        category_id = category.get('id')
        category_slug = category.get('seo_slug')
        product_id = product.get('id')
        product_slug = product.get('seo_slug')

        if not product_slug:
            slug = slugify(product['name'])


        if not category_slug:
            category_slug = slugify('category-'+product['name'])

        return '/product/{}/{}/{}/{}'.format(category_id, category_slug, product_id, product_slug ) 

    except Exception as e:
        print(e)
        return ''

@register.filter
def calculate_new_price(prod):
    return prod['price'] - prod['discount']

@register.filter
def get_prod_attrs(prod):
    attrs = []
    attrs_str = ''
    for attr in prod['_attributs']:
        attrs.append(attr['name'])
        attrs = list(set(attrs))
        attrs_str = ' '.join(str(id) for id in attrs)

    return attrs_str



@register.filter
def getAttr(dictionary, key):
    return dictionary.get(key,'')



@register.filter
def hasSubProductsColor(product):
    if product and len(product.get('declinaisons', None)):
        result = False
        for dec in product['declinaisons']:
            for attr in dec['_attributs']:
                result = result or attr['is_color']
        return result
    else:
        return False


@register.filter
def getObjInArr(arr, args ):
    attr,value,display = args.split(',')

    value = eval(value) if value == 'True' or value == 'False' else value

    if len(arr):
        obj = next((x for x in arr if x[attr] == value), None)
        if display:
            return obj[display]
        else :
            return obj
    else :
        return None


@register.filter
def getattr(obj, args):
    (attribute, default) = args.split(',')
    try:
        return obj.__getattribute__(attribute)
    except AttributeError:
         return  obj.get(attribute, default)
    except:
        return eval(default)

@register.filter
def removeDuplicate(arr):
    return list(dict.fromkeys(arr))



@register.filter
def findColors(product):
    colors = []
    todisplay = {}
    for dec in product['declinaisons']:
        for attr in dec.get('_attributs',[]):
            if attr['is_color']:
                
                colors.append({
                    "id": attr['id'],
                    "name":attr["name"],
                    "color":attr["value"],
                    "image": dec['photo'] ,
                    "image_thumb": dec['photo_thumb'] 
                })
                
    colors.sort(key=lambda x: x['image'], reverse=False)

    for color in colors : 
        todisplay[color['id']] = color


    return list(todisplay.values())



@register.filter
def image_thumb(product):
    images = []
    thumbs = []
    for image in product['images']:
        if image['image'] not in thumbs:
            images.append(image)
            thumbs.append(image['image'])
    for dec in product['declinaisons']:
        for image in dec['images']:
            if image and image['image'] not in thumbs:
                images.append(image)
                thumbs.append(image.get('image',''))

    return images


