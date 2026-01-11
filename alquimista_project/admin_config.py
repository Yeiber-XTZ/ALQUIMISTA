"""
Configuración personalizada del Admin de Django
"""
from django.contrib.admin.apps import AdminConfig

class AlquimistaAdminConfig(AdminConfig):
    default_site = 'core.admin.AlquimistaAdminSite'
