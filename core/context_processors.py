from .models import ContactMessage

def staff_context(request):
    """
    Context processor para el panel de staff.
    Agrega el conteo de mensajes no leídos a todos los templates del staff.
    """
    if request.user.is_authenticated and request.user.is_staff:
        return {
            'unread_count': ContactMessage.objects.filter(leido=False).count(),
        }
    return {}

