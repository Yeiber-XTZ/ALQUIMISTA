from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Prefetch
from .models import Facet, Milestone, ContactMessage, SiteSettings, MilestoneImage, UserFacetPreference
from .decorators import staff_required
from .forms import CustomUserCreationForm, FacetSelectionForm, LoginForm, FacetManagementForm

def index(request):
    """
    Vista principal del sitio público.
    Muestra todas las facetas con sus hitos en formato de scroll horizontal.
    Cada hito es una diapositiva completa.
    Si el usuario está autenticado, solo muestra las facetas que ha seleccionado.
    """
    # Obtener configuración del sitio
    site_settings = SiteSettings.load()
    
    # Si el usuario está autenticado, filtrar facetas según sus preferencias
    if request.user.is_authenticated:
        # Obtener IDs de facetas seleccionadas por el usuario, ordenadas por prioridad
        user_facets = UserFacetPreference.objects.filter(
            usuario=request.user
        ).select_related('faceta').order_by('prioridad', 'faceta__orden')
        
        facet_ids = [pref.faceta_id for pref in user_facets]
        
        if facet_ids:
            # Obtener solo las facetas seleccionadas por el usuario
            facets = Facet.objects.filter(
                id__in=facet_ids,
                activo=True
            ).prefetch_related(
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
            
            # Crear un diccionario para mantener el orden de prioridad del usuario
            priority_map = {pref.faceta_id: pref.prioridad for pref in user_facets}
            facets_list = list(facets)
            facets_list.sort(key=lambda x: (priority_map.get(x.id, 999), x.orden))
            facets = facets_list
        else:
            # Usuario autenticado pero sin facetas seleccionadas
            facets = []
    else:
        # Usuario no autenticado: mostrar todas las facetas activas
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
    from django.utils import timezone
    message_obj = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        if 'mark_read' in request.POST:
            message_obj.leido = True
            message_obj.save()
            messages.success(request, 'Mensaje marcado como leído.')
            return redirect('core:staff_message_detail', pk=pk)
        elif 'send_response' in request.POST:
            respuesta = request.POST.get('respuesta', '').strip()
            if respuesta:
                message_obj.respuesta = respuesta
                message_obj.fecha_respuesta = timezone.now()
                message_obj.leido = True  # Marcar como leído al responder
                message_obj.save()
                messages.success(request, 'Respuesta guardada exitosamente.')
                return redirect('core:staff_message_detail', pk=pk)
            else:
                messages.error(request, 'La respuesta no puede estar vacía.')
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


# ==================== AUTENTICACIÓN Y GESTIÓN DE USUARIOS ====================

def register(request):
    """Vista de registro de usuarios."""
    site_settings = SiteSettings.load()
    
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        facet_form = FacetSelectionForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            
            # Guardar preferencias de facetas
            selected_facets = []
            for key, value in request.POST.items():
                if key.startswith('facet_') and value == 'on':
                    facet_id = int(key.replace('facet_', ''))
                    priority = int(request.POST.get(f'priority_{facet_id}', 0))
                    selected_facets.append((facet_id, priority))
            
            # Crear preferencias de facetas
            for facet_id, priority in selected_facets:
                try:
                    facet = Facet.objects.get(id=facet_id, activo=True)
                    UserFacetPreference.objects.create(
                        usuario=user,
                        faceta=facet,
                        prioridad=priority
                    )
                except Facet.DoesNotExist:
                    pass
            
            # Iniciar sesión automáticamente
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'¡Bienvenido, {username}! Tu cuenta ha sido creada exitosamente.')
                return redirect('core:index')
        
        return render(request, 'core/register.html', {
            'user_form': user_form,
            'facet_form': facet_form,
            'site_settings': site_settings,
        })
    
    # GET
    user_form = CustomUserCreationForm()
    facet_form = FacetSelectionForm()
    return render(request, 'core/register.html', {
        'user_form': user_form,
        'facet_form': facet_form,
        'site_settings': site_settings,
    })


def user_login(request):
    """Vista de inicio de sesión."""
    site_settings = SiteSettings.load()
    
    if request.user.is_authenticated:
        return redirect('core:index')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'¡Bienvenido de nuevo, {username}!')
                next_url = request.GET.get('next', 'core:index')
                return redirect(next_url)
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    
    return render(request, 'core/login.html', {
        'form': form,
        'site_settings': site_settings,
    })


def user_logout(request):
    """Vista de cierre de sesión."""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('core:index')


@login_required
def manage_facets(request):
    """Vista para gestionar las facetas seleccionadas por el usuario."""
    site_settings = SiteSettings.load()
    
    if request.method == 'POST':
        form = FacetManagementForm(request.user, request.POST)
        
        # Obtener facetas seleccionadas y sus prioridades
        selected_facets = {}
        for key, value in request.POST.items():
            if key.startswith('facet_') and value == 'on':
                facet_id = int(key.replace('facet_', ''))
                priority = int(request.POST.get(f'priority_{facet_id}', 0))
                selected_facets[facet_id] = priority
        
        # Eliminar preferencias de facetas no seleccionadas
        UserFacetPreference.objects.filter(usuario=request.user).exclude(
            faceta_id__in=selected_facets.keys()
        ).delete()
        
        # Actualizar o crear preferencias
        for facet_id, priority in selected_facets.items():
            UserFacetPreference.objects.update_or_create(
                usuario=request.user,
                faceta_id=facet_id,
                defaults={'prioridad': priority}
            )
        
        messages.success(request, 'Tus preferencias de facetas han sido actualizadas.')
        return redirect('core:manage_facets')
    
    # GET
    form = FacetManagementForm(request.user)
    # Obtener facetas para el template
    facets = Facet.objects.filter(activo=True).order_by('orden')
    user_preferences = {
        pref.faceta_id: pref.prioridad 
        for pref in UserFacetPreference.objects.filter(usuario=request.user)
    }
    
    facets_data = []
    for facet in facets:
        facets_data.append({
            'facet': facet,
            'is_selected': facet.id in user_preferences,
            'priority': user_preferences.get(facet.id, 0)
        })
    
    return render(request, 'core/manage_facets.html', {
        'form': form,
        'facets_data': facets_data,
        'site_settings': site_settings,
    })
