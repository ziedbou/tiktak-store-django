from django.http import HttpResponse
from httplib2 import Response
import re
from django.conf import settings
import requests
from django.http import Http404


#API ENDPOINT
ENDPOINT_API = getattr(settings, "ENDPOINT_API", "")


def get_slug_or_server(request, *args, **kwargs):
    url = request.META['HTTP_HOST']


    host = url.split(':')[0]
    slug = host.split('.',1)[0] # : to . in prod
    host = host.replace('www.', '')


    if not "tiktak-store" in host: 

        return host, 'server'  #return full host (server)
    else:
        return slug, 'slug'



'''
-------------------
    GET MENU
-------------------
@company_id : string
@name : string
@position : string
'''
def getMenu(company_id, position="header",  name="", menu_id=None):

    params = {
        "name" : name,
        "position":position if position else "",
        "active":True,
        "company":company_id,
        "id": menu_id if menu_id else ""
    }
     
    response = requests.get(ENDPOINT_API+'website/menus-read/', params = params)

    try:
        return response.json()[0]['menus']
    except Exception as e:
        return []



'''
GET PRODUCT SERVICE
'''
def getProduct(company_id, product_id):
    params = {
        "company" :company_id
    }
    
    response = requests.get(ENDPOINT_API+'products-read/{}/'.format(product_id), params=params)
    if response.status_code == 200:
        return response.json()
    else :
        raise Http404
    

def getProductColor(product):
    colors = []
    principalImage = product.get('image_thumb','')
    for dec in product.get('declinaisons',''):
        if dec.get('image_thumb','') != principalImage :
            colors.append(dec.get('image_thumb',''))
        else :
            return False

    return colors

'''
GET LIST OF PRODUCTS
'''
def getListOfProducts(company_id, has_category="", category_in=[], direct_category="", list_ids_in=[], page=1, ids_not_in=[]):

    params = {
        "no_parent":True,
        "active":True,
        "page":str(page),
        "has_category": has_category,
        "categories_in":category_in,
        "category":direct_category,
        "ids_in":list_ids_in,
        "ids_not_in":','.join(ids_not_in),
        "company":company_id,
        "size":12
    }

    response = requests.get(ENDPOINT_API+'products-read/', params=params)
    
    try:
        if(response.status_code == 200):
            return response.json()
        else :
            raise Http404
    except Exception as e:
        raise Http404

'''
GET CATEGORY BY ID
'''
def getCategory(company_id, category_id):
    params = {
        "company" :company_id
    }

    response = requests.get(ENDPOINT_API+'categories-read/{}/'.format(category_id), params=params)

    try:
        return response.json()
    except Exception as e:
        raise Http404


'''
GET WEBSITE PAGES
'''
def getPages(company_id):

    params = {
        "company" :company_id
    }

    response = requests.get(ENDPOINT_API+'website/sections-content-read/', params=params)
    
    try:
        return response.json()
    except Exception as e:
        raise Http404


'''
GET WEBSITE SITEMAP
'''
def getSitemap(company_id):

    params = {
        "company" :company_id
    }

    response = requests.get(ENDPOINT_API+'website/company-sitemap/', params=params)

    try:
        return response.json()
    except Exception as e:
        raise Http404


