"""mks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import include, path, re_path
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static

import home.views
import teaching.views


admin.autodiscover()

from django.conf.urls import include, url
from django.contrib import admin

from django.contrib.sitemaps.views import sitemap

from home.sitemaps import Static_Sitemap

sitemaps = {
    'static': Static_Sitemap(),
}


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^blog/', include('blog.urls')),
    re_path(r'^blogedit/', include('blog.edit_urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),

#    re_path(r'^instruments/', include('instruments.urls')),
    path('', home.views.home, name='home_view'),
    path('impressum/', home.views.impressum, name='impressum'),
    path('geschichte/', home.views.history, name='history'),
    path('team/', include('users.urls')),
    path('', include('contact.urls')),
    path('', include('downloadsection.urls')),
    path('', include('gallery.urls')),
    path('', include('teaching.urls')),
    path('', include('students.urls')),
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'home.views.view_404'
handler500 = 'home.views.view_404'

#if settings.DEBUG:
#    import debug_toolbar
#    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
