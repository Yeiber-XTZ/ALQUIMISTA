"""
Módulo para el envío de emails del sistema.
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_welcome_email(user, site_settings=None):
    """
    Envía un email de bienvenida al usuario recién registrado.
    
    Args:
        user: Instancia del modelo User
        site_settings: Instancia de SiteSettings (opcional)
    """
    try:
        # Obtener información del usuario
        nombre = user.profile.nombre if hasattr(user, 'profile') and user.profile.nombre else user.username
        rol = user.profile.get_rol_display() if hasattr(user, 'profile') else 'Visitante'
        es_estudiante = hasattr(user, 'profile') and user.profile.es_estudiante
        
        # Obtener configuración del sitio
        if not site_settings:
            from .models import SiteSettings
            site_settings = SiteSettings.load()
        
        nombre_sitio = site_settings.nombre_sitio if site_settings else 'ALQUIMISTA'
        email_contacto = site_settings.email_contacto if site_settings and site_settings.email_contacto else None
        
        # Obtener URL del sitio
        site_url = 'localhost:8000'
        if settings.ALLOWED_HOSTS:
            protocol = 'https' if not settings.DEBUG else 'http'
            site_url = f'{protocol}://{settings.ALLOWED_HOSTS[0]}'
        elif hasattr(settings, 'SITE_URL'):
            site_url = settings.SITE_URL
        
        # Contexto para el template
        context = {
            'usuario': user,
            'nombre': nombre,
            'username': user.username,
            'rol': rol,
            'es_estudiante': es_estudiante,
            'nombre_sitio': nombre_sitio,
            'email_contacto': email_contacto,
            'site_url': site_url,
        }
        
        # Renderizar template HTML
        html_message = render_to_string('core/emails/welcome.html', context)
        
        # Versión en texto plano
        plain_message = strip_tags(html_message)
        
        # Asunto del email
        subject = f'¡Bienvenido/a a {nombre_sitio}! 🎉'
        
        # Enviar email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return True
    except Exception as e:
        # Log del error pero no fallar el registro
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'Error al enviar email de bienvenida: {str(e)}')
        return False
