from django.http import HttpResponse
from django.template import loader
import requests
from website.helper import *
from website.templatetags import *
from django.shortcuts import render
import xmltodict
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.conf import settings


#API
api = settings.ENDPOINT_API



## GET COMPANY DATA ##
def getCompanyData(request):
    company_def, type = get_slug_or_server(request)
    
    company = requests.get(api+'get-company/?'+type+'='+company_def).json()
    company_info = requests.get(api+'website/informations-read/?'+type+'='+company_def).json()  

    header_menu = getMenu(company['id'], 'header')
    footer_menu = getMenu(company['id'], "footer")
    
    return company, header_menu, footer_menu, company_info


#####################################################################################################

def index(request):
    company, header_menu, footer_menu, company_info = getCompanyData(request)

    template_path = company_info.get('url', 'molla-1')
    template = loader.get_template(template_path+'/pages/home/index.html')

    sections = getPages(company['id'])

    messages = []
    try:
        i = 1
        for sec in sections['data']:
            i = i+1
            if sec['slug'] == 'message':
                messages.append(sec)
            if sec['slug'] == 'menu-with-banner':
                try:
                    menu_id = sec.get('values').get('menus_widget').get('menu_id')
                    menu = getMenu(company['id'],position="", menu_id = menu_id )

                    sec.get('values')['menu_data'] = menu
                except Exception as e:
                    print('error',str(e))
                    pass
    except Exception as e:
        pass
    
           
    
    if len(messages) > 0 :
        for msg in messages:
            i = sections['data'].index(msg)
            text = msg['values'].get('text',"")
            sections['data'][i]['values']['text'] = text.replace('"','')
   

    context = {
        "company": company,
        "header": header_menu,
        "footer": footer_menu,
        "social_links": company_info.get('contact_settings', {}),
        "company_info": company_info,
        "page_type": "home",
        "sections": sections['data'],
        "seo": {
            "title": company.get('name', ''),
            "description": company.get('name', ''), 
            "image": company.get('logo', {}), 
            "url": request.build_absolute_uri()
        }
    }
    return HttpResponse(template.render(context, request))

def checkout(request):
    company, header_menu, footer_menu, company_info = getCompanyData(request)   

    transporters = None
    if company['works_with_transport']:
        res = requests.get(api+"transports-read/?company="+company['id']).json()
        transporters = res['results']


    template_path = company_info.get('url', 'molla-1')
    template = loader.get_template(template_path+'/pages/checkout/index.html')


    context = {
        "company": company,
        "header": header_menu,
        "footer": footer_menu,
        "social_links": company_info.get('contact_settings', {}),
        "company_info": company_info,
        "page_type": "checkout",

        "seo": {
            "title": "checkout", 
            "description": "", 
            "image": "", 
            "url": request.build_absolute_uri()
        },

        "transporters": transporters
    }
    return HttpResponse(template.render(context, request))

def categories(request):
    company, header_menu, footer_menu, company_info = getCompanyData(request)   
  
    template_path = company_info.get('url', 'molla-1')
    template = loader.get_template(template_path+'/pages/categories/index.html')

    context = {
        "company": company,
        "header": header_menu,
        "footer": footer_menu,
        "social_links": company_info.get('contact_settings', {}),
        "company_info": company_info,
        "page_type": "product_group",

        "seo":{
            "title": "categpry", 
            "description": "", 
            "image": "", 
            "url": request.build_absolute_uri()
        },
    }
    return HttpResponse(template.render(context, request))


'''
GET PRODUCT ITEM
'''
def product(request, product_id, cat_id = "", cat_slug = "",  slug = ""):
    company, header_menu, footer_menu, company_info = getCompanyData(request)   

    product = getProduct(company['id'], product_id)

    relatedProducts = getListOfProducts(ids_not_in = [product_id], has_category=cat_id, company_id = company['id'])

    colors = getProductColor(product)

    #CHOOSE TEMPLATE
    template_path = company_info.get('url', 'molla-1')
    template = loader.get_template(template_path+'/pages/product/index.html')

    context = {
        "company": company,
        "header": header_menu,
        "footer": footer_menu,
        "social_links": company_info.get('contact_settings', {}),
        "company_info": company_info,
        "page_type": "product",
        "page_contents": product.get("id"),

        "seo":{
            "title": product.get('seo_title', ''),
            "description": product.get('seo_description', ''),
            "image": product.get('photo', ''),
            "url": request.build_absolute_uri()
        },

        "product": product,
        "category": product.get('_category', {}),
        "relatedProducts": relatedProducts.get('results', [])
    }
    return HttpResponse(template.render(context, request))



'''
GET PRODUCT LIST BY CATEGORY
'''
def product_list(request, cat_id, cat_slug):
    company, header_menu, footer_menu, company_info = getCompanyData(request)   

    page_number = int(request.GET.get('page', '1'))

    category = getCategory(company['id'], cat_id)


    #CHOOSE TEMPLATE
    template_path = company_info.get('url', 'molla-1')
    template = loader.get_template(template_path+'/pages/product-list/index.html')


    context = {
        "company": company,
        "category": category,
        "header": header_menu,
        "footer": footer_menu,
        "social_links": company_info.get('contact_settings', {}),
        "company_info": company_info,
        "page_type": "product_group",

        "seo":{
            "title": category.get('seo_title'), 
            "description": category.get('seo_description'), 
            "image": category.get('image', {}),#.get('image', ''), 

            "url": request.build_absolute_uri()
        },
    }
    return HttpResponse(template.render(context, request))


'''
WISH LIST PAGE
'''
def wishlist(request):
    company, header_menu, footer_menu, company_info = getCompanyData(request)   

    #CHOOSE TEMPLATE
    template_path = company_info.get('url', 'molla-1')
    template = loader.get_template(template_path+'/pages/whishlist/index.html')

    context = {
        "company": company,
        "header": header_menu,
        "footer": footer_menu,
        "social_links": company_info.get('contact_settings', {}),
        "company_info": company_info,
        "page_type": "wishlist",

        "seo":{
            "title": "favoirs", 
            "description": "", 
            "image": "", 
            "url": request.build_absolute_uri()
        },
    }
    return HttpResponse(template.render(context, request))


'''
CART PAGE
'''
def cart(request):
    company, header_menu, footer_menu, company_info = getCompanyData(request)   

    transporters = None
    if company['works_with_transport']:
        transporters = requests.get(api+"transports-read/?company="+company['id']).json()
        transporters = transporters['results']

    #CHOOSE TEMPLATE
    template_path = company_info.get('url', 'molla-1')
    template = loader.get_template(template_path+'/pages/cart/index.html')

    context = {
        "company": company,
        "header": header_menu,
        "footer": footer_menu,
        "social_links": company_info.get('contact_settings', {}),
        "company_info": company_info,
        "page_type": "cart",

        "seo":{
            "title": "panier", 
            "description": "", 
            "image": "", 
            "url": request.build_absolute_uri()
        },

        "transporters": transporters
    }
    return HttpResponse(template.render(context, request))



'''
GET ACCOUNT
'''
def account(request):
    company, header_menu, footer_menu, company_info = getCompanyData(request)   

    #CHOOSE TEMPLATE
    template_path = company_info.get('url', 'molla-1')
    template = loader.get_template(template_path+'/pages/account/index.html')

    context = {
        "company": company,
        "header": header_menu,
        "footer": footer_menu,
        "social_links": company_info.get('contact_settings', {}),
        "company_info": company_info,
        "page_type": "account",

        "seo":{
            "title": "mon compte", 
            "description": "", 
            "image": "", 
            "url": request.build_absolute_uri()
        }
    }
    return HttpResponse(template.render(context, request))




'''
GET CONTACT PAGE
'''
def contact(request):
    company, header_menu, footer_menu, company_info = getCompanyData(request)   

    #CHOOSE TEMPLATE
    template_path = company_info.get('url', 'molla-1')
    template = loader.get_template(template_path+'/pages/contact/index.html')

    context = {
        "company": company,
        "header": header_menu,
        "footer": footer_menu,
        "social_links": company_info.get('contact_settings', {}),
        "company_info": company_info,
        "page_type": "contact",

        "seo":{
            "title": "contact", 
            "description": "", 
            "image": "", 
            "url": request.build_absolute_uri()
        }
    }
    return HttpResponse(template.render(context, request))    


def paymentsuccess(request,order_id):
    company, header_menu, footer_menu, company_info = getCompanyData(request) 

    #CHOOSE TEMPLATE
    template_path = company_info.get('url', 'molla-1')
    template = loader.get_template(template_path+'/pages/paiment-status/index.html')
  
    context = {
        "company": company,
        "header": header_menu,
        "footer": footer_menu,
        "social_links": company_info.get('contact_settings', {}),
        "company_info": company_info,
        "page_type": "paymentsuccess",
        "payment_success":True,

        "seo":{
            "title": "SUCCESS Payment", 
            "description": "", 
            "image": "", 
            "url": request.build_absolute_uri()
        }
    }
    return HttpResponse(template.render(context, request))    

def paymentfailed(request, order_id):
    company, header_menu, footer_menu, company_info = getCompanyData(request)   
    
    #CHOOSE TEMPLATE
    template_path = company_info.get('url', 'molla-1')
    template = loader.get_template(template_path+'/pages/paiment-status/index.html')
  
    context = {
        "company": company,
        "header": header_menu,
        "footer": footer_menu,
        "social_links": company_info.get('contact_settings', {}),
        "company_info": company_info,
        "page_type": "paymentfailed",
        "payment_success":False,
        "seo":{
            "title": "SUCCESS Payment", 
            "description": "", 
            "image": "", 
            "url": request.build_absolute_uri()
        }
    }
    return HttpResponse(template.render(context, request))    

'''
GET SEARCH PAGE
'''
def search(request):
    company, header_menu, footer_menu, company_info = getCompanyData(request)   

    #CHOOSE TEMPLATE
    template_path = company_info.get('url', 'molla-1')
    template = loader.get_template(template_path+'/pages/search/index.html')

    context = {
        "company": company,
        "header": header_menu,
        "footer": footer_menu,
        "social_links": company_info.get('contact_settings', {}),
        "company_info": company_info,
        "page_type": "search",

        "seo":{
            "title": "search", 
            "description": "", 
            "image": "", 
            "url": request.build_absolute_uri()
        }
    }
    return HttpResponse(template.render(context, request))  


'''
GET RESET PASSWORD PAGE
'''
def reset_pass(request):
    company, header_menu, footer_menu, company_info = getCompanyData(request)   

    #CHOOSE TEMPLATE
    template_path = company_info.get('url', 'molla-1')
    template = loader.get_template(template_path+'/pages/reset-pass/index.html')

    context = {
        "company": company,
        "header": header_menu,
        "footer": footer_menu,
        "social_links": company_info.get('contact_settings', {}),
        "company_info": company_info,
        "page_type": "reset",

        "seo":{
            "title": "réinitialisation de mot de passe", 
            "description": "", 
            "image": "", 
            "url": request.build_absolute_uri()
        }
    }
    return HttpResponse(template.render(context, request))


######################################################### SITEMAP ######################################


'''
SITEMAP PAGE
'''
def sitemap(request):
    company, header_menu, footer_menu, company_info = getCompanyData(request)   

    sitemap = getSitemap(company['id'])

    #DELETE IDs
    for item in sitemap['value']['urlset']['url']:
        del item['id']

    xml_sitemap = xmltodict.unparse(sitemap['value'], pretty=True)

    return HttpResponse(xml_sitemap, content_type='text/xml')  



######################################################### ERRORS ######################################


'''
Handle 404 Errors
'''
def error404(request, exception):
    company, header_menu, footer_menu, company_info = getCompanyData(request)   

    #CHOOSE TEMPLATE
    template_path = company_info.get('url', 'molla-1')
    template = loader.get_template(template_path+'/pages/errors/index.html')

    context = {
        "company": company,
        "header": header_menu,
        "footer": footer_menu,
        "social_links": company_info.get('contact_settings', {}),
        "company_info": company_info,
        "page_type": "error-404",

        "seo":{
            "title": "404", 
            "description": "", 
            "image": "", 
            "url": request.build_absolute_uri()
        }
    }
    return HttpResponse(template.render(context, request), status=404)        


'''
Handle 500 Errors
'''
def error500(request):
    company, header_menu, footer_menu, company_info = getCompanyData(request)   

    #CHOOSE TEMPLATE
    template_path = company_info.get('url', 'molla-1')
    template = loader.get_template(template_path+'/pages/errors/index.html')

    context = {
        "company": company,
        "header": header_menu,
        "footer": footer_menu,
        "social_links": company_info.get('contact_settings', {}),
        "company_info": company_info,
        "page_type": "error-500",

        "seo":{
            "title": "500", 
            "description": "", 
            "image": "", 
            "url": request.build_absolute_uri()
        }
    }
    return HttpResponse(template.render(context, request), status=500)
