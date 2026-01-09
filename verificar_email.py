"""
Script para verificar la configuracion de email
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

print("=" * 60)
print("VERIFICACION DE CONFIGURACION DE EMAIL")
print("=" * 60)
print()

# Verificar variables
email_backend = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
email_host = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
email_port = os.getenv('EMAIL_PORT', '587')
email_use_tls = os.getenv('EMAIL_USE_TLS', 'True')
email_host_user = os.getenv('EMAIL_HOST_USER', '')
email_host_password = os.getenv('EMAIL_HOST_PASSWORD', '')
default_from_email = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@alquimista.com')

print("CONFIGURACION ACTUAL:")
print("-" * 60)
print(f"EMAIL_BACKEND: {email_backend}")
print(f"EMAIL_HOST: {email_host}")
print(f"EMAIL_PORT: {email_port}")
print(f"EMAIL_USE_TLS: {email_use_tls}")
print(f"EMAIL_HOST_USER: {email_host_user if email_host_user else '(VACIO)'}")
print(f"EMAIL_HOST_PASSWORD: {'*' * len(email_host_password) if email_host_password else '(VACIO)'}")
print(f"DEFAULT_FROM_EMAIL: {default_from_email}")
print()

# Diagnostico
print("DIAGNOSTICO:")
print("-" * 60)

if 'console' in email_backend.lower():
    print("PROBLEMA: Estas usando el backend de CONSOLA")
    print("Los emails se muestran en la consola, no se envian realmente")
    print()
    print("SOLUCION: Cambia en .env:")
    print("EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend")
    print()
else:
    print("OK: Backend SMTP configurado correctamente")
    print()

if not email_host_user:
    print("PROBLEMA: EMAIL_HOST_USER esta vacio")
    print("Necesitas configurar tu email de Gmail")
    print()
    print("SOLUCION: Agrega en .env:")
    print("EMAIL_HOST_USER=tu-email@gmail.com")
    print()
else:
    print(f"OK: EMAIL_HOST_USER configurado: {email_host_user}")
    print()

if not email_host_password:
    print("PROBLEMA: EMAIL_HOST_PASSWORD esta vacio")
    print("Necesitas una contrasena de aplicacion de Gmail")
    print()
    print("SOLUCION:")
    print("1. Ve a: https://myaccount.google.com/apppasswords")
    print("2. Genera una contrasena de aplicacion")
    print("3. Agrega en .env:")
    print("EMAIL_HOST_PASSWORD=tu-contrasena-de-aplicacion")
    print()
else:
    print("OK: EMAIL_HOST_PASSWORD configurado (contrasena oculta)")
    print()

# Resumen
print("=" * 60)
print("RESUMEN:")
print("=" * 60)

if 'console' in email_backend.lower() or not email_host_user or not email_host_password:
    print("La configuracion NO esta lista para enviar emails reales")
    print()
    print("Para enviar emails reales, necesitas:")
    print("1. Cambiar EMAIL_BACKEND a smtp.EmailBackend")
    print("2. Configurar EMAIL_HOST_USER con tu email de Gmail")
    print("3. Configurar EMAIL_HOST_PASSWORD con contrasena de aplicacion")
else:
    print("La configuracion esta lista para enviar emails reales")
    print()
    print("Reinicia el servidor Django para aplicar los cambios")
