"""
Script para probar el envio de un email de prueba
"""
import os
import django
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alquimista_project.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 60)
print("PRUEBA DE ENVIO DE EMAIL")
print("=" * 60)
print()

# Verificar configuracion
print("Configuracion actual:")
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print()

# Intentar enviar email de prueba
try:
    print("Intentando enviar email de prueba...")
    print(f"Desde: {settings.DEFAULT_FROM_EMAIL}")
    print(f"Para: {settings.EMAIL_HOST_USER}")
    print()
    
    send_mail(
        subject='Prueba de Email - ALQUIMISTA',
        message='Este es un email de prueba. Si recibes esto, la configuracion funciona correctamente.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.EMAIL_HOST_USER],
        fail_silently=False,
    )
    
    print("SUCCESS: Email enviado correctamente!")
    print(f"Revisa la bandeja de entrada de: {settings.EMAIL_HOST_USER}")
    print("(Tambien revisa la carpeta de spam)")
    
except Exception as e:
    print("ERROR al enviar email:")
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {str(e)}")
    print()
    print("POSIBLES SOLUCIONES:")
    print("1. Verifica que EMAIL_HOST_USER sea un email valido")
    print("2. Verifica que EMAIL_HOST_PASSWORD sea una contrasena de aplicacion correcta")
    print("3. Si usas Gmail, asegurate de tener activada la verificacion en 2 pasos")
    print("4. Si usas otro proveedor, verifica la configuracion SMTP")
    print()
    if "authentication" in str(e).lower() or "smtp" in str(e).lower():
        print("ERROR DE AUTENTICACION:")
        print("- Verifica que la contrasena de aplicacion sea correcta")
        print("- Para Gmail: https://myaccount.google.com/apppasswords")
        print("- Asegurate de usar una contrasena de APLICACION, no tu contrasena normal")
