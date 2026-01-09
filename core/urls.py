from django.urls import path
from django.contrib.sitemaps.views import sitemap
from . import views
from .robots import robots_txt
from .sitemaps import StaticViewSitemap, FacetSitemap

app_name = 'core'

# Sitemap configuration
sitemaps = {
    'static': StaticViewSitemap,
    'facets': FacetSitemap,
}

urlpatterns = [
    # Público
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    
    # SEO
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # Autenticación
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('manage-facets/', views.manage_facets, name='manage_facets'),
    
    # Contenido Estudiantil
    path('material-clase/', views.material_clase, name='material_clase'),
    
    # Staff - Dashboard
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    
    # Staff - Facetas
    path('staff/facetas/', views.staff_facets_list, name='staff_facets_list'),
    path('staff/facetas/nueva/', views.staff_facet_create, name='staff_facet_create'),
    path('staff/facetas/<int:pk>/editar/', views.staff_facet_edit, name='staff_facet_edit'),
    path('staff/facetas/<int:pk>/eliminar/', views.staff_facet_delete, name='staff_facet_delete'),
    
    # Staff - Hitos
    path('staff/hitos/', views.staff_milestones_list, name='staff_milestones_list'),
    path('staff/hitos/faceta/<int:facet_id>/', views.staff_milestones_list, name='staff_milestones_list_by_facet'),
    path('staff/hitos/nuevo/', views.staff_milestone_create, name='staff_milestone_create'),
    path('staff/hitos/faceta/<int:facet_id>/nuevo/', views.staff_milestone_create, name='staff_milestone_create_for_facet'),
    path('staff/hitos/<int:pk>/editar/', views.staff_milestone_edit, name='staff_milestone_edit'),
    path('staff/hitos/<int:pk>/eliminar/', views.staff_milestone_delete, name='staff_milestone_delete'),
    
    # Staff - Mensajes
    path('staff/mensajes/', views.staff_messages_list, name='staff_messages_list'),
    path('staff/mensajes/<int:pk>/', views.staff_message_detail, name='staff_message_detail'),
    path('staff/mensajes/<int:pk>/eliminar/', views.staff_message_delete, name='staff_message_delete'),
    
    # Staff - Configuración del Sitio
    path('staff/configuracion/', views.staff_site_settings, name='staff_site_settings'),
    
    # Staff - Temáticas
    path('staff/tematicas/', views.staff_tematicas_list, name='staff_tematicas_list'),
    path('staff/tematicas/nueva/', views.staff_tematica_create, name='staff_tematica_create'),
    path('staff/tematicas/<int:pk>/editar/', views.staff_tematica_edit, name='staff_tematica_edit'),
    path('staff/tematicas/<int:pk>/eliminar/', views.staff_tematica_delete, name='staff_tematica_delete'),
    
    # Staff - Materiales
    path('staff/materiales/', views.staff_materiales_list, name='staff_materiales_list'),
    path('staff/materiales/nuevo/', views.staff_material_create, name='staff_material_create'),
    path('staff/materiales/<int:pk>/editar/', views.staff_material_edit, name='staff_material_edit'),
    path('staff/materiales/<int:pk>/eliminar/', views.staff_material_delete, name='staff_material_delete'),
]

