from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

def staff_required(view_func):
    """
    Decorador que verifica que el usuario sea staff.
    Redirige al login personalizado si no está autenticado o no es staff.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión para acceder a esta sección.')
            # Redirigir al login personalizado con el parámetro 'next' para volver después del login
            login_url = reverse('core:login')
            next_url = request.get_full_path()
            return redirect(f'{login_url}?next={next_url}')
        if not request.user.is_staff:
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('core:index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def estudiante_required(view_func):
    """
    Decorador que verifica que el usuario tenga rol de Estudiante.
    Redirige al login si no está autenticado o al index si no es estudiante.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión para acceder al material de clase.')
            return redirect('core:login')
        
        # Verificar si el usuario tiene perfil y es estudiante
        if hasattr(request.user, 'profile'):
            if not request.user.profile.es_estudiante:
                messages.error(request, 'Solo los estudiantes pueden acceder al material de clase.')
                return redirect('core:index')
        else:
            # Si no tiene perfil, crear uno con rol visitante
            from .models import UserProfile
            UserProfile.objects.create(usuario=request.user, rol='visitante')
            messages.error(request, 'Solo los estudiantes pueden acceder al material de clase.')
            return redirect('core:index')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view


