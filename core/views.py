from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q, Prefetch
from .models import Facet, Milestone, ContactMessage, SiteSettings, MilestoneImage
from .decorators import staff_required

def index(request):
    """
    Vista principal del sitio público.
    Muestra todas las facetas con sus hitos en formato de scroll horizontal.
    Cada hito es una diapositiva completa.
    """
    # Obtener configuración del sitio
    site_settings = SiteSettings.load()
    
    # Obtener todas las facetas activas ordenadas con sus hitos e imágenes
    facets = Facet.objects.filter(activo=True).order_by('orden').prefetch_related(
        Prefetch(
            'hitos',
            queryset=Milestone.objects.filter(activo=True).order_by('orden', 'año').prefetch_related(
                Prefetch(
                    'imagenes',
                    queryset=MilestoneImage.objects.filter(activo=True).order_by('orden')
                )
            )
        )
    )
    
    # Para cada faceta, obtener sus hitos activos ordenados y calcular total de slides
    for facet in facets:
        facet.hitos_activos = list(facet.hitos.all())
        # Calcular total de slides para esta faceta: 1 (título) + hitos
        facet.total_slides = 1 + len(facet.hitos_activos)
    
    context = {
        'facets': facets,
        'site_settings': site_settings,
    }
    return render(request, 'core/index.html', context)

def contact(request):
    """
    Página de contacto (GET) y procesamiento (POST).
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        if nombre and email and mensaje:
            ContactMessage.objects.create(nombre=nombre, email=email, mensaje=mensaje)
            messages.success(request, '¡Mensaje enviado correctamente!')
            return redirect('core:contact')
        else:
            messages.error(request, 'Por favor completa todos los campos.')
            return redirect('core:contact')
    # GET
    from .models import SiteSettings
    site_settings = SiteSettings.load() if hasattr(SiteSettings, 'load') else None
    return render(request, 'core/contact.html', {'site_settings': site_settings})


# ==================== VISTAS DEL PANEL DE STAFF ====================

@staff_required
def staff_dashboard(request):
    """Dashboard principal del panel de staff."""
    stats = {
        'total_facetas': Facet.objects.count(),
        'facetas_activas': Facet.objects.filter(activo=True).count(),
        'total_hitos': Milestone.objects.count(),
        'hitos_activos': Milestone.objects.filter(activo=True).count(),
        'mensajes_no_leidos': ContactMessage.objects.filter(leido=False).count(),
        'total_mensajes': ContactMessage.objects.count(),
    }
    
    # Últimas facetas
    ultimas_facetas = Facet.objects.all().order_by('-fecha_creacion')[:5]
    
    # Últimos mensajes
    ultimos_mensajes = ContactMessage.objects.all().order_by('-fecha_creacion')[:5]
    
    context = {
        'stats': stats,
        'ultimas_facetas': ultimas_facetas,
        'ultimos_mensajes': ultimos_mensajes,
        'unread_count': stats['mensajes_no_leidos'],  # Para el template base
    }
    return render(request, 'staff/dashboard.html', context)


# ==================== CONFIGURACIÓN GENERAL DEL SITIO ====================

@staff_required
def staff_site_settings(request):
    """Editar configuración general del sitio."""
    from .models import SiteSettings
    settings = SiteSettings.load()
    
    if request.method == 'POST':
        try:
            settings.nombre_sitio = request.POST.get('nombre_sitio', 'ALQUIMISTA NELSON')
            settings.descripcion_general = request.POST.get('descripcion_general', '')
            settings.email_contacto = request.POST.get('email_contacto', '')
            settings.telefono = request.POST.get('telefono', '')
            settings.direccion = request.POST.get('direccion', '')
            settings.facebook_url = request.POST.get('facebook_url', '')
            settings.instagram_url = request.POST.get('instagram_url', '')
            settings.twitter_url = request.POST.get('twitter_url', '')
            settings.linkedin_url = request.POST.get('linkedin_url', '')
            settings.youtube_url = request.POST.get('youtube_url', '')
            # Hero Section
            settings.texto_hero = request.POST.get('texto_hero', 'ALQUIMISTA')
            settings.subtitulo_hero = request.POST.get('subtitulo_hero', 'Scroll to explore')
            
            if 'logo' in request.FILES:
                settings.logo = request.FILES['logo']
            
            if 'imagen_hero' in request.FILES:
                settings.imagen_hero = request.FILES['imagen_hero']
            
            settings.save()
            messages.success(request, 'Configuración del sitio actualizada exitosamente.')
            return redirect('core:staff_site_settings')
        except Exception as e:
            messages.error(request, f'Error al actualizar la configuración: {str(e)}')
    
    return render(request, 'staff/site_settings.html', {'settings': settings})


# ==================== GESTIÓN DE FACETAS ====================

@staff_required
def staff_facets_list(request):
    """Lista de todas las facetas."""
    facets = Facet.objects.all().annotate(
        num_hitos=Count('hitos')
    ).order_by('orden', 'titulo')
    return render(request, 'staff/facets_list.html', {'facets': facets})

@staff_required
def staff_facet_create(request):
    """Crear una nueva faceta."""
    if request.method == 'POST':
        try:
            facet = Facet.objects.create(
                titulo=request.POST.get('titulo'),
                descripcion=request.POST.get('descripcion', ''),
                orden=int(request.POST.get('orden', 0)),
                activo=request.POST.get('activo') == 'on'
            )
            if 'imagen_hero' in request.FILES:
                facet.imagen_hero = request.FILES['imagen_hero']
                facet.save()
            messages.success(request, f'Faceta "{facet.titulo}" creada exitosamente.')
            return redirect('core:staff_facets_list')
        except Exception as e:
            messages.error(request, f'Error al crear la faceta: {str(e)}')
    return render(request, 'staff/facet_form.html', {'form_action': 'create'})

@staff_required
def staff_facet_edit(request, pk):
    """Editar una faceta existente."""
    facet = get_object_or_404(Facet, pk=pk)
    if request.method == 'POST':
        try:
            facet.titulo = request.POST.get('titulo')
            facet.descripcion = request.POST.get('descripcion', '')
            facet.orden = int(request.POST.get('orden', 0))
            facet.activo = request.POST.get('activo') == 'on'
            if 'imagen_hero' in request.FILES:
                facet.imagen_hero = request.FILES['imagen_hero']
            facet.save()
            messages.success(request, f'Faceta "{facet.titulo}" actualizada exitosamente.')
            return redirect('core:staff_facets_list')
        except Exception as e:
            messages.error(request, f'Error al actualizar la faceta: {str(e)}')
    return render(request, 'staff/facet_form.html', {'facet': facet, 'form_action': 'edit'})

@staff_required
def staff_facet_delete(request, pk):
    """Eliminar una faceta."""
    facet = get_object_or_404(Facet, pk=pk)
    if request.method == 'POST':
        titulo = facet.titulo
        facet.delete()
        messages.success(request, f'Faceta "{titulo}" eliminada exitosamente.')
        return redirect('core:staff_facets_list')
    return render(request, 'staff/facet_delete.html', {'facet': facet})


# ==================== GESTIÓN DE HITOS ====================

@staff_required
def staff_milestones_list(request, facet_id=None):
    """Lista de hitos, opcionalmente filtrados por faceta."""
    if facet_id:
        facet = get_object_or_404(Facet, pk=facet_id)
        milestones = Milestone.objects.filter(faceta=facet).order_by('orden', 'año')
        return render(request, 'staff/milestones_list.html', {
            'milestones': milestones,
            'facet': facet
        })
    milestones = Milestone.objects.all().select_related('faceta').order_by('faceta__orden', 'orden', 'año')
    return render(request, 'staff/milestones_list.html', {'milestones': milestones})

@staff_required
def staff_milestone_create(request, facet_id=None):
    """Crear un nuevo hito."""
    facet = None
    if facet_id:
        facet = get_object_or_404(Facet, pk=facet_id)
    
    if request.method == 'POST':
        try:
            faceta_id = request.POST.get('faceta')
            faceta_obj = get_object_or_404(Facet, pk=faceta_id)
            
            milestone = Milestone.objects.create(
                faceta=faceta_obj,
                titulo=request.POST.get('titulo'),
                descripcion=request.POST.get('descripcion', ''),
                año=int(request.POST.get('año')) if request.POST.get('año') else None,
                orden=int(request.POST.get('orden', 0)),
                activo=request.POST.get('activo') == 'on'
            )
            if 'imagen' in request.FILES:
                milestone.imagen = request.FILES['imagen']
                milestone.save()
            messages.success(request, f'Hito "{milestone.titulo}" creado exitosamente.')
            return redirect('core:staff_milestones_list_by_facet', facet_id=faceta_obj.id)
        except Exception as e:
            messages.error(request, f'Error al crear el hito: {str(e)}')
    
    facets = Facet.objects.all().order_by('orden')
    return render(request, 'staff/milestone_form.html', {
        'facets': facets,
        'facet': facet,
        'form_action': 'create'
    })

@staff_required
def staff_milestone_edit(request, pk):
    """Editar un hito existente."""
    milestone = get_object_or_404(Milestone, pk=pk)
    if request.method == 'POST':
        try:
            faceta_id = request.POST.get('faceta')
            milestone.faceta = get_object_or_404(Facet, pk=faceta_id)
            milestone.titulo = request.POST.get('titulo')
            milestone.descripcion = request.POST.get('descripcion', '')
            milestone.año = int(request.POST.get('año')) if request.POST.get('año') else None
            milestone.orden = int(request.POST.get('orden', 0))
            milestone.activo = request.POST.get('activo') == 'on'
            if 'imagen' in request.FILES:
                milestone.imagen = request.FILES['imagen']
            milestone.save()
            messages.success(request, f'Hito "{milestone.titulo}" actualizado exitosamente.')
            return redirect('core:staff_milestones_list_by_facet', facet_id=milestone.faceta.id)
        except Exception as e:
            messages.error(request, f'Error al actualizar el hito: {str(e)}')
    
    facets = Facet.objects.all().order_by('orden')
    return render(request, 'staff/milestone_form.html', {
        'milestone': milestone,
        'facets': facets,
        'form_action': 'edit'
    })

@staff_required
def staff_milestone_delete(request, pk):
    """Eliminar un hito."""
    milestone = get_object_or_404(Milestone, pk=pk)
    if request.method == 'POST':
        titulo = milestone.titulo
        facet_id = milestone.faceta.id
        milestone.delete()
        messages.success(request, f'Hito "{titulo}" eliminado exitosamente.')
        return redirect('core:staff_milestones_list_by_facet', facet_id=facet_id)
    return render(request, 'staff/milestone_delete.html', {'milestone': milestone})


# ==================== GESTIÓN DE MENSAJES ====================

@staff_required
def staff_messages_list(request):
    """Lista de mensajes de contacto."""
    messages_list = ContactMessage.objects.all().order_by('-fecha_creacion')
    unread_count = ContactMessage.objects.filter(leido=False).count()
    return render(request, 'staff/messages_list.html', {
        'messages': messages_list,
        'unread_count': unread_count,
    })

@staff_required
def staff_message_detail(request, pk):
    """Detalle de un mensaje de contacto."""
    message_obj = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST' and 'mark_read' in request.POST:
        message_obj.leido = True
        message_obj.save()
        messages.success(request, 'Mensaje marcado como leído.')
        return redirect('core:staff_message_detail', pk=pk)
    unread_count = ContactMessage.objects.filter(leido=False).count()
    return render(request, 'staff/message_detail.html', {
        'message_obj': message_obj,
        'unread_count': unread_count,
    })

@staff_required
def staff_message_delete(request, pk):
    """Eliminar un mensaje de contacto."""
    message_obj = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        message_obj.delete()
        messages.success(request, 'Mensaje eliminado exitosamente.')
        return redirect('core:staff_messages_list')
    return render(request, 'staff/message_delete.html', {'message_obj': message_obj})
