from django.contrib import admin
from django.contrib.admin.apps import AdminConfig

# Personalizar el Admin de Django
admin.site.site_header = 'ALQUIMISTA - Panel de Administración'
admin.site.site_title = 'ALQUIMISTA Admin'
admin.site.index_title = 'Panel de Control'

# Register your models here.
