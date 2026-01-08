from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Facet

class StaticViewSitemap(Sitemap):
    """Sitemap para páginas estáticas."""
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return ['core:index', 'core:contact']

    def location(self, item):
        return reverse(item)

class FacetSitemap(Sitemap):
    """Sitemap para facetas."""
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Facet.objects.filter(activo=True)

    def location(self, obj):
        return reverse('core:index') + f'#facet-{obj.slug}'
    
    def lastmod(self, obj):
        return obj.fecha_actualizacion
