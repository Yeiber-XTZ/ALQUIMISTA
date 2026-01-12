from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Prefetch
from django.http import HttpResponse
from django.urls import reverse
from .models import Facet, Milestone, ContactMessage, SiteSettings, MilestoneImage, UserFacetPreference, Tematica, Material, MaterialPDF, MaterialVideo, MaterialPresentacion, UserProfile
from django.contrib.auth.models import User
from .decorators import staff_required, estudiante_required
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
    Página de contacto (GET) y procesamiento (POST) con validación mejorada.
    """
    site_settings = SiteSettings.load()
    
    if request.method == 'POST':
        # Rate limiting básico - evitar spam (10 mensajes por hora por IP)
        from django.core.cache import cache
        from django.utils import timezone
        from datetime import timedelta
        
        ip_address = request.META.get('REMOTE_ADDR', '')
        cache_key = f'contact_rate_limit_{ip_address}'
        message_count = cache.get(cache_key, 0)
        
        if message_count >= 10:
            messages.error(request, 'Has enviado demasiados mensajes. Por favor intenta más tarde.')
            return redirect('core:contact')
        
        # Validación y sanitización
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        mensaje = request.POST.get('mensaje', '').strip()
        
        # Validaciones básicas
        if not nombre or len(nombre) < 2:
            messages.error(request, 'El nombre debe tener al menos 2 caracteres.')
            return redirect('core:contact')
        
        if len(nombre) > 200:
            messages.error(request, 'El nombre es demasiado largo (máximo 200 caracteres).')
            return redirect('core:contact')
        
        if not email or '@' not in email:
            messages.error(request, 'Por favor ingresa un email válido.')
            return redirect('core:contact')
        
        if len(email) > 254:
            messages.error(request, 'El email es demasiado largo.')
            return redirect('core:contact')
        
        if not mensaje or len(mensaje) < 10:
            messages.error(request, 'El mensaje debe tener al menos 10 caracteres.')
            return redirect('core:contact')
        
        if len(mensaje) > 5000:
            messages.error(request, 'El mensaje es demasiado largo (máximo 5000 caracteres).')
            return redirect('core:contact')
        
        # Crear mensaje
        try:
            ContactMessage.objects.create(nombre=nombre, email=email, mensaje=mensaje)
            # Incrementar contador de rate limiting
            cache.set(cache_key, message_count + 1, 3600)  # 1 hora
            messages.success(request, '¡Mensaje enviado correctamente! Te responderemos pronto.')
        except Exception as e:
            messages.error(request, 'Hubo un error al enviar el mensaje. Por favor intenta nuevamente.')
        
        return redirect('core:contact')
    
    # GET
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
            settings.whatsapp_telefono = request.POST.get('whatsapp_telefono', '')
            
            if 'logo' in request.FILES:
                settings.logo = request.FILES['logo']
            
            if 'imagen_hero' in request.FILES:
                settings.imagen_hero = request.FILES['imagen_hero']
            
            if 'video_hero' in request.FILES:
                settings.video_hero = request.FILES['video_hero']
            
            if 'imagen_loading' in request.FILES:
                settings.imagen_loading = request.FILES['imagen_loading']
            
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
                activo=request.POST.get('activo') == 'on',
                color_fondo=request.POST.get('color_fondo', 'negro')
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
            facet.color_fondo = request.POST.get('color_fondo', 'negro')
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
                activo=request.POST.get('activo') == 'on',
                video_activo=request.POST.get('video_activo') == 'on',
                tamaño_imagen=request.POST.get('tamaño_imagen', 'mediana')
            )
            if 'imagen' in request.FILES:
                milestone.imagen = request.FILES['imagen']
            if 'video' in request.FILES:
                milestone.video = request.FILES['video']
            video_url = request.POST.get('video_url', '').strip()
            if video_url:
                milestone.video_url = video_url
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
            milestone.video_activo = request.POST.get('video_activo') == 'on'
            milestone.tamaño_imagen = request.POST.get('tamaño_imagen', 'mediana')
            if 'imagen' in request.FILES:
                milestone.imagen = request.FILES['imagen']
            if 'video' in request.FILES:
                milestone.video = request.FILES['video']
            video_url = request.POST.get('video_url', '').strip()
            if video_url:
                milestone.video_url = video_url
            elif 'video_url' in request.POST:
                milestone.video_url = None
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
            
            # Enviar email de bienvenida
            try:
                from .emails import send_welcome_email
                send_welcome_email(user, site_settings)
            except Exception as e:
                # Si falla el email, no interrumpir el registro
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f'Error al enviar email de bienvenida: {str(e)}')
            
            # Iniciar sesión automáticamente
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                # Obtener el nombre del usuario o username
                nombre_usuario = user.profile.nombre if hasattr(user, 'profile') and user.profile.nombre else username
                rol_usuario = user.profile.get_rol_display() if hasattr(user, 'profile') else 'Visitante'
                
                # Mensaje personalizado según el rol
                if hasattr(user, 'profile') and user.profile.es_estudiante:
                    mensaje_bienvenida = f'¡Bienvenido/a, {nombre_usuario}! 🎓 Tu cuenta de Estudiante ha sido creada exitosamente. Revisa tu correo para más información. Ahora tienes acceso exclusivo al Material de Clase.'
                else:
                    mensaje_bienvenida = f'¡Bienvenido/a, {nombre_usuario}! ✨ Tu cuenta ha sido creada exitosamente. Revisa tu correo para más información. Explora las diferentes facetas y descubre contenido único.'
                
                messages.success(request, mensaje_bienvenida)
                # Redirigir con parámetro para mostrar modal de bienvenida
                return redirect(reverse('core:index') + '?welcome=1')
        
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
        # Si ya está autenticado y viene de una URL de staff, redirigir al staff dashboard
        next_url = request.GET.get('next', '')
        if next_url and '/staff/' in next_url:
            return redirect('core:staff_dashboard')
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
                # Obtener la URL de destino desde POST o GET
                next_url = request.POST.get('next') or request.GET.get('next', '')
                if next_url:
                    # Validar que next_url no sea una URL externa por seguridad
                    from django.utils.http import url_has_allowed_host_and_scheme
                    if url_has_allowed_host_and_scheme(next_url, allowed_hosts=None):
                        return redirect(next_url)
                # Si no hay next_url o no es válida, redirigir según si es staff
                if user.is_staff and '/staff/' in request.path:
                    return redirect('core:staff_dashboard')
                return redirect('core:index')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    
    # Pasar next_url al template para incluirlo en el formulario
    next_url = request.GET.get('next', '')
    
    return render(request, 'core/login.html', {
        'form': form,
        'site_settings': site_settings,
        'next_url': next_url,
    })


def user_logout(request):
    """Vista de cierre de sesión."""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('core:index')


# Error handlers
def handler400(request, exception):
    """Custom 400 error handler."""
    site_settings = SiteSettings.load()
    return render(request, 'core/400.html', {'site_settings': site_settings}, status=400)

def handler403(request, exception):
    """Custom 403 error handler."""
    site_settings = SiteSettings.load()
    return render(request, 'core/403.html', {'site_settings': site_settings}, status=403)

def handler404(request, exception):
    """Custom 404 error handler."""
    site_settings = SiteSettings.load()
    return render(request, 'core/404.html', {'site_settings': site_settings}, status=404)

def handler500(request):
    """Custom 500 error handler."""
    site_settings = SiteSettings.load()
    return render(request, 'core/500.html', {'site_settings': site_settings}, status=500)

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


# ==================== CONTENIDO ESTUDIANTIL ====================

@estudiante_required
def material_clase(request):
    """
    Vista para mostrar el material de clase exclusivo para estudiantes.
    """
    site_settings = SiteSettings.load()
    tematicas = Tematica.objects.filter(activo=True).order_by('orden').prefetch_related(
        Prefetch(
            'materiales',
            queryset=Material.objects.filter(activo=True).order_by('orden').prefetch_related(
                Prefetch(
                    'pdfs',
                    queryset=MaterialPDF.objects.filter(activo=True).order_by('orden')
                ),
                Prefetch(
                    'videos',
                    queryset=MaterialVideo.objects.filter(activo=True).order_by('orden')
                ),
                Prefetch(
                    'presentaciones',
                    queryset=MaterialPresentacion.objects.filter(activo=True).order_by('orden')
                )
            )
        )
    )
    
    context = {
        'tematicas': tematicas,
        'site_settings': site_settings,
    }
    return render(request, 'core/material_clase.html', context)


# ==================== STAFF - GESTIÓN DE TEMÁTICAS Y MATERIALES ====================

@staff_required
def staff_tematicas_list(request):
    """Lista de todas las temáticas."""
    tematicas = Tematica.objects.all().annotate(
        num_materiales=Count('materiales')
    ).order_by('orden', 'titulo')
    return render(request, 'staff/tematicas_list.html', {'tematicas': tematicas})

@staff_required
def staff_tematica_create(request):
    """Crear una nueva temática."""
    if request.method == 'POST':
        try:
            tematica = Tematica.objects.create(
                titulo=request.POST.get('titulo'),
                descripcion=request.POST.get('descripcion', ''),
                orden=int(request.POST.get('orden', 0)),
                activo=request.POST.get('activo') == 'on'
            )
            messages.success(request, f'Temática "{tematica.titulo}" creada exitosamente.')
            return redirect('core:staff_tematicas_list')
        except Exception as e:
            messages.error(request, f'Error al crear la temática: {str(e)}')
    return render(request, 'staff/tematica_form.html', {'form_action': 'create'})

@staff_required
def staff_tematica_edit(request, pk):
    """Editar una temática existente."""
    tematica = get_object_or_404(Tematica, pk=pk)
    if request.method == 'POST':
        try:
            tematica.titulo = request.POST.get('titulo')
            tematica.descripcion = request.POST.get('descripcion', '')
            tematica.orden = int(request.POST.get('orden', 0))
            tematica.activo = request.POST.get('activo') == 'on'
            tematica.save()
            messages.success(request, f'Temática "{tematica.titulo}" actualizada exitosamente.')
            return redirect('core:staff_tematicas_list')
        except Exception as e:
            messages.error(request, f'Error al actualizar la temática: {str(e)}')
    return render(request, 'staff/tematica_form.html', {'tematica': tematica, 'form_action': 'edit'})

@staff_required
def staff_tematica_delete(request, pk):
    """Eliminar una temática."""
    tematica = get_object_or_404(Tematica, pk=pk)
    if request.method == 'POST':
        tematica.delete()
        messages.success(request, 'Temática eliminada exitosamente.')
        return redirect('core:staff_tematicas_list')
    return render(request, 'staff/tematica_delete.html', {'tematica': tematica})

@staff_required
def staff_materiales_list(request):
    """Lista de todos los materiales."""
    materiales = Material.objects.all().select_related('tematica').order_by('tematica__orden', 'orden', 'titulo')
    return render(request, 'staff/materiales_list.html', {'materiales': materiales})

@staff_required
def staff_material_create(request):
    """Crear un nuevo material."""
    tematicas = Tematica.objects.filter(activo=True).order_by('orden')
    if request.method == 'POST':
        try:
            tematica = get_object_or_404(Tematica, pk=request.POST.get('tematica'))
            material = Material.objects.create(
                tematica=tematica,
                titulo=request.POST.get('titulo'),
                descripcion=request.POST.get('descripcion', ''),
                orden=int(request.POST.get('orden', 0)),
                activo=request.POST.get('activo') == 'on'
            )
            
            # Procesar múltiples PDFs
            pdf_files = request.FILES.getlist('archivos_pdf')
            pdf_nombres = request.POST.getlist('pdf_nombres')
            pdf_ordenes = request.POST.getlist('pdf_ordenes')
            
            for i, pdf_file in enumerate(pdf_files):
                nombre = pdf_nombres[i] if i < len(pdf_nombres) and pdf_nombres[i] else ''
                orden = int(pdf_ordenes[i]) if i < len(pdf_ordenes) and pdf_ordenes[i] else i
                MaterialPDF.objects.create(
                    material=material,
                    archivo=pdf_file,
                    nombre=nombre,
                    orden=orden
                )
            
            # Procesar múltiples videos
            video_urls = request.POST.getlist('video_urls')
            video_archivos = request.FILES.getlist('video_archivos')
            video_nombres = request.POST.getlist('video_nombres')
            video_ordenes = request.POST.getlist('video_ordenes')
            
            # Procesar videos por URL
            for i, video_url in enumerate(video_urls):
                if video_url.strip():
                    nombre = video_nombres[i] if i < len(video_nombres) and video_nombres[i] else ''
                    orden = int(video_ordenes[i]) if i < len(video_ordenes) and video_ordenes[i] else i
                    MaterialVideo.objects.create(
                        material=material,
                        video_url=video_url,
                        nombre=nombre,
                        orden=orden
                    )
            
            # Procesar videos por archivo
            for i, video_file in enumerate(video_archivos):
                nombre = video_nombres[len(video_urls) + i] if len(video_nombres) > len(video_urls) + i and video_nombres[len(video_urls) + i] else ''
                orden = int(video_ordenes[len(video_urls) + i]) if len(video_ordenes) > len(video_urls) + i and video_ordenes[len(video_urls) + i] else len(video_urls) + i
                MaterialVideo.objects.create(
                    material=material,
                    video_archivo=video_file,
                    nombre=nombre,
                    orden=orden
                )
            
            # Procesar múltiples presentaciones
            presentacion_files = request.FILES.getlist('archivos_presentacion')
            presentacion_nombres = request.POST.getlist('presentacion_nombres')
            presentacion_ordenes = request.POST.getlist('presentacion_ordenes')
            
            for i, presentacion_file in enumerate(presentacion_files):
                nombre = presentacion_nombres[i] if i < len(presentacion_nombres) and presentacion_nombres[i] else ''
                orden = int(presentacion_ordenes[i]) if i < len(presentacion_ordenes) and presentacion_ordenes[i] else i
                MaterialPresentacion.objects.create(
                    material=material,
                    archivo=presentacion_file,
                    nombre=nombre,
                    orden=orden
                )
            
            messages.success(request, f'Material "{material.titulo}" creado exitosamente.')
            return redirect('core:staff_materiales_list')
        except Exception as e:
            messages.error(request, f'Error al crear el material: {str(e)}')
    return render(request, 'staff/material_form.html', {'form_action': 'create', 'tematicas': tematicas})

@staff_required
def staff_material_edit(request, pk):
    """Editar un material existente."""
    material = get_object_or_404(Material, pk=pk)
    tematicas = Tematica.objects.filter(activo=True).order_by('orden')
    if request.method == 'POST':
        try:
            tematica = get_object_or_404(Tematica, pk=request.POST.get('tematica'))
            material.tematica = tematica
            material.titulo = request.POST.get('titulo')
            material.descripcion = request.POST.get('descripcion', '')
            material.orden = int(request.POST.get('orden', 0))
            material.activo = request.POST.get('activo') == 'on'
            material.save()
            
            # Procesar múltiples PDFs nuevos
            pdf_files = request.FILES.getlist('archivos_pdf')
            pdf_nombres = request.POST.getlist('pdf_nombres')
            pdf_ordenes = request.POST.getlist('pdf_ordenes')
            
            for i, pdf_file in enumerate(pdf_files):
                nombre = pdf_nombres[i] if i < len(pdf_nombres) and pdf_nombres[i] else ''
                orden = int(pdf_ordenes[i]) if i < len(pdf_ordenes) and pdf_ordenes[i] else material.pdfs.count() + i
                MaterialPDF.objects.create(
                    material=material,
                    archivo=pdf_file,
                    nombre=nombre,
                    orden=orden
                )
            
            # Actualizar PDFs existentes
            pdf_ids = request.POST.getlist('pdf_ids')
            for pdf_id in pdf_ids:
                if pdf_id:
                    try:
                        pdf = MaterialPDF.objects.get(pk=pdf_id, material=material)
                        pdf_nombre_key = f'pdf_nombre_{pdf_id}'
                        pdf_orden_key = f'pdf_orden_{pdf_id}'
                        pdf_activo_key = f'pdf_activo_{pdf_id}'
                        
                        if pdf_nombre_key in request.POST:
                            pdf.nombre = request.POST[pdf_nombre_key]
                        if pdf_orden_key in request.POST:
                            pdf.orden = int(request.POST[pdf_orden_key])
                        pdf.activo = pdf_activo_key in request.POST
                        pdf.save()
                    except MaterialPDF.DoesNotExist:
                        pass
            
            # Eliminar PDFs marcados para eliminar
            pdf_delete_ids = request.POST.getlist('pdf_delete')
            for pdf_id in pdf_delete_ids:
                try:
                    MaterialPDF.objects.filter(pk=pdf_id, material=material).delete()
                except:
                    pass
            
            # Procesar múltiples videos nuevos
            video_urls = request.POST.getlist('video_urls')
            video_archivos = request.FILES.getlist('video_archivos')
            video_nombres = request.POST.getlist('video_nombres')
            video_ordenes = request.POST.getlist('video_ordenes')
            
            # Procesar videos por URL nuevos
            for i, video_url in enumerate(video_urls):
                if video_url.strip():
                    nombre = video_nombres[i] if i < len(video_nombres) and video_nombres[i] else ''
                    orden = int(video_ordenes[i]) if i < len(video_ordenes) and video_ordenes[i] else material.videos.count() + i
                    MaterialVideo.objects.create(
                        material=material,
                        video_url=video_url,
                        nombre=nombre,
                        orden=orden
                    )
            
            # Procesar videos por archivo nuevos
            for i, video_file in enumerate(video_archivos):
                nombre = video_nombres[len(video_urls) + i] if len(video_nombres) > len(video_urls) + i and video_nombres[len(video_urls) + i] else ''
                orden = int(video_ordenes[len(video_urls) + i]) if len(video_ordenes) > len(video_urls) + i and video_ordenes[len(video_urls) + i] else material.videos.count() + len(video_urls) + i
                MaterialVideo.objects.create(
                    material=material,
                    video_archivo=video_file,
                    nombre=nombre,
                    orden=orden
                )
            
            # Actualizar videos existentes
            video_ids = request.POST.getlist('video_ids')
            for video_id in video_ids:
                if video_id:
                    try:
                        video = MaterialVideo.objects.get(pk=video_id, material=material)
                        video_nombre_key = f'video_nombre_{video_id}'
                        video_url_key = f'video_url_{video_id}'
                        video_orden_key = f'video_orden_{video_id}'
                        video_activo_key = f'video_activo_{video_id}'
                        
                        if video_nombre_key in request.POST:
                            video.nombre = request.POST[video_nombre_key]
                        if video_url_key in request.POST:
                            video.video_url = request.POST[video_url_key] or None
                        if video_orden_key in request.POST:
                            video.orden = int(request.POST[video_orden_key])
                        video.activo = video_activo_key in request.POST
                        video.save()
                    except MaterialVideo.DoesNotExist:
                        pass
            
            # Eliminar videos marcados para eliminar
            video_delete_ids = request.POST.getlist('video_delete')
            for video_id in video_delete_ids:
                try:
                    MaterialVideo.objects.filter(pk=video_id, material=material).delete()
                except:
                    pass
            
            # Procesar múltiples presentaciones nuevas
            presentacion_files = request.FILES.getlist('archivos_presentacion')
            presentacion_nombres = request.POST.getlist('presentacion_nombres')
            presentacion_ordenes = request.POST.getlist('presentacion_ordenes')
            
            for i, presentacion_file in enumerate(presentacion_files):
                nombre = presentacion_nombres[i] if i < len(presentacion_nombres) and presentacion_nombres[i] else ''
                orden = int(presentacion_ordenes[i]) if i < len(presentacion_ordenes) and presentacion_ordenes[i] else material.presentaciones.count() + i
                MaterialPresentacion.objects.create(
                    material=material,
                    archivo=presentacion_file,
                    nombre=nombre,
                    orden=orden
                )
            
            # Actualizar presentaciones existentes
            presentacion_ids = request.POST.getlist('presentacion_ids')
            for presentacion_id in presentacion_ids:
                if presentacion_id:
                    try:
                        presentacion = MaterialPresentacion.objects.get(pk=presentacion_id, material=material)
                        presentacion_nombre_key = f'presentacion_nombre_{presentacion_id}'
                        presentacion_orden_key = f'presentacion_orden_{presentacion_id}'
                        presentacion_activo_key = f'presentacion_activo_{presentacion_id}'
                        
                        if presentacion_nombre_key in request.POST:
                            presentacion.nombre = request.POST[presentacion_nombre_key]
                        if presentacion_orden_key in request.POST:
                            presentacion.orden = int(request.POST[presentacion_orden_key])
                        presentacion.activo = presentacion_activo_key in request.POST
                        presentacion.save()
                    except MaterialPresentacion.DoesNotExist:
                        pass
            
            # Eliminar presentaciones marcadas para eliminar
            presentacion_delete_ids = request.POST.getlist('presentacion_delete')
            for presentacion_id in presentacion_delete_ids:
                try:
                    MaterialPresentacion.objects.filter(pk=presentacion_id, material=material).delete()
                except:
                    pass
            
            messages.success(request, f'Material "{material.titulo}" actualizado exitosamente.')
            return redirect('core:staff_materiales_list')
        except Exception as e:
            messages.error(request, f'Error al actualizar el material: {str(e)}')
    
    # Precargar PDFs, videos y presentaciones para el formulario
    material.pdfs_list = material.pdfs.all().order_by('orden')
    material.videos_list = material.videos.all().order_by('orden')
    material.presentaciones_list = material.presentaciones.all().order_by('orden')
    return render(request, 'staff/material_form.html', {'material': material, 'form_action': 'edit', 'tematicas': tematicas})

@staff_required
def staff_material_delete(request, pk):
    """Eliminar un material."""
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        messages.success(request, 'Material eliminado exitosamente.')
        return redirect('core:staff_materiales_list')
    return render(request, 'staff/material_delete.html', {'material': material})


# ==================== STAFF - GESTIÓN DE USUARIOS ====================

@staff_required
def staff_users_list(request):
    """Lista de todos los usuarios con filtros y búsqueda."""
    from django.contrib.auth.models import User
    
    # Estadísticas
    total_usuarios = User.objects.count()
    usuarios_estudiantes = UserProfile.objects.filter(rol='estudiante').count()
    usuarios_visitantes = UserProfile.objects.filter(rol='visitante').count()
    usuarios_staff = User.objects.filter(is_staff=True).count()
    superusuarios = User.objects.filter(is_superuser=True).count()
    
    stats = {
        'total_usuarios': total_usuarios,
        'usuarios_estudiantes': usuarios_estudiantes,
        'usuarios_visitantes': usuarios_visitantes,
        'usuarios_staff': usuarios_staff,
        'superusuarios': superusuarios,
    }
    
    # Búsqueda y filtros
    search_query = request.GET.get('q', '').strip()
    rol_filter = request.GET.get('rol', '').strip()
    
    # Obtener usuarios con sus perfiles
    users = User.objects.select_related('profile').all()
    
    # Aplicar búsqueda
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(profile__id_usuario__icontains=search_query)
        )
    
    # Aplicar filtro de rol
    if rol_filter:
        if rol_filter == 'estudiante':
            users = users.filter(profile__rol='estudiante')
        elif rol_filter == 'visitante':
            users = users.filter(profile__rol='visitante')
        elif rol_filter == 'staff':
            users = users.filter(is_staff=True)
        elif rol_filter == 'superuser':
            users = users.filter(is_superuser=True)
    
    users = users.order_by('-date_joined')
    
    return render(request, 'staff/users_list.html', {
        'users': users,
        'stats': stats,
        'search_query': search_query,
        'rol_filter': rol_filter,
    })

@staff_required
def staff_user_edit_permissions(request, pk):
    """Editar permisos de un usuario."""
    from django.contrib.auth.models import User
    
    user_obj = get_object_or_404(User, pk=pk)
    
    # Obtener o crear perfil
    profile, created = UserProfile.objects.get_or_create(usuario=user_obj)
    
    # Verificar si el usuario actual puede editar superusuarios
    can_edit_superuser = request.user.is_superuser
    
    if request.method == 'POST':
        try:
            # Actualizar permisos de staff
            user_obj.is_staff = 'is_staff' in request.POST
            user_obj.save()
            
            # Actualizar permisos de superusuario (solo si el usuario actual es superusuario)
            if can_edit_superuser:
                user_obj.is_superuser = 'is_superuser' in request.POST
                user_obj.save()
            
            messages.success(request, f'Permisos de "{user_obj.username}" actualizados exitosamente.')
            return redirect('core:staff_users_list')
        except Exception as e:
            messages.error(request, f'Error al actualizar los permisos: {str(e)}')
    
    return render(request, 'staff/user_edit_permissions.html', {
        'user_obj': user_obj,
        'profile': profile,
        'can_edit_superuser': can_edit_superuser,
    })
