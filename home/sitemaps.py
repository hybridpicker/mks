from django.contrib.sitemaps import Sitemap
from django.urls import reverse


from django.conf import settings
from django.urls import URLResolver, URLPattern


class Static_Sitemap(Sitemap):

    priority = 1.0
    changefreq = 'yearly'

    def items(self):
        return ['home_view',
                'impressum',
                'history',
                'all_teachers',
                'contact_email',
                'teaching_art',
                'teaching_prices',
                'teaching_music',
                'gallery_view']

    def location(self, item):
        return reverse(item)
