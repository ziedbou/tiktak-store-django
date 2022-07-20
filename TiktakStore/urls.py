from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from website.views import error404, error500
from django.conf.urls import handler404, handler500
# from website.sitemap_views import custom_sitemap_index, custom_sitemap_section


urlpatterns = [
    path('', include('website.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = error404
handler500 = error500
