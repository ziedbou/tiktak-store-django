from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .views import *
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', index, name='index'), 
    path('reset-password/', reset_pass, name='reset-password'), 
    path('checkout', checkout, name='checkout'), 
    path('categories/', categories, name='categories'), 
    path('product/<cat_id>/<cat_slug>/<product_id>/<slug>/', product, name='product'), 
    path('product/<product_id>', product, name='product-short'), 
    path('product-list/<cat_id>/<cat_slug>/', product_list, name='product_list'), 
    path('wishlist', wishlist, name='wishlist'), 
    path('cart', cart, name='cart'), 
    path('account', account, name='account'),
    path('contact', contact, name='contact'),
    path('checkout/success-payment/<order_id>', paymentsuccess),
    path('checkout/failed-payment/<order_id>', paymentfailed),
    path('search', search, name='search'),
    path('sitemap.xml', sitemap, name='sitemap'),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain"))
 
]
