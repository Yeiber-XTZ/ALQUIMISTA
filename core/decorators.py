from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def staff_required(view_func):
    """
    Decorador que verifica que el usuario sea staff.
    Redirige al login si no está autenticado o no es staff.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión para acceder a esta sección.')
            return redirect('admin:login')
        if not request.user.is_staff:
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('core:index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


