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

from django.urls import include, re_path
from django.contrib import admin

from django.contrib.sitemaps.views import sitemap

from home.sitemaps import Static_Sitemap

sitemaps = {
    'static': Static_Sitemap(),
}


urlpatterns = [
    path('', include('maintenance.urls')),  # Wartungsmodus - muss als erstes kommen
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^blog/', include('blog.urls')),
    re_path(r'^blogedit/', include('blog.edit_urls')),
    re_path(r'^tinymce/', include('tinymce.urls')),  # Added TinyMCE URLs

#    re_path(r'^instruments/', include('instruments.urls')),
    path('', home.views.home, name='home_view'),
    path('impressum/', home.views.impressum, name='impressum'),
    path('geschichte/', home.views.history, name='history'),
    path('logo/', home.views.logo, name='logo'),
    path('team/', include('users.urls', namespace='users')),
    path('controlling/', include('controlling.urls', namespace='controlling')),
    path('', include('contact.urls')),
    path('', include('downloadsection.urls')),
    path('', include('gallery.urls')),
    path('lehrende/', include('teaching.urls', namespace='teaching')),
    # path('standorte/', include('location.urls', namespace='location')), 
    path('tanz-und-bewegung/', include('dance.urls', namespace='dance')),
    path('projekte/', include('projects.urls', namespace='projects')),
    path('', include('students.urls')),
    path('', include('faq.urls')),
    path('hexe-rabaukel/', include('invitation.urls')),
    path('midi-band/', include('midi_band.urls')),

    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'home.views.view_404'
handler500 = 'home.views.view_404'

#if settings.DEBUG:
#    import debug_toolbar
#    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
