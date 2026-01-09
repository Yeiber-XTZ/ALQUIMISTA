"""
Probar con puerto 465 (SSL) en lugar de 587 (TLS)
"""
import os
import django
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alquimista_project.settings')
django.setup()

from django.core.mail import get_connection, send_mail
from django.conf import settings

print("=" * 60)
print("PROBANDO CON PUERTO 465 (SSL)")
print("=" * 60)
print()

email_host_user = os.getenv('EMAIL_HOST_USER', 'yeiber.mena.dev@ebanocompany.com')
email_host_password = os.getenv('EMAIL_HOST_PASSWORD', 'ccgkzsxkbwkwwigs')

# Configuracion con SSL (puerto 465)
try:
    print("Configuracion:")
    print("  EMAIL_HOST=smtp.gmail.com")
    print("  EMAIL_PORT=465")
    print("  EMAIL_USE_SSL=True")
    print()
    print("Conectando...")
    
    connection = get_connection(
        host='smtp.gmail.com',
        port=465,
        username=email_host_user,
        password=email_host_password,
        use_ssl=True,  # SSL en lugar de TLS
        use_tls=False,
        timeout=15
    )
    
    connection.open()
    print("Conexion exitosa!")
    
    print("Enviando email de prueba...")
    send_mail(
        subject='Prueba de Email - ALQUIMISTA',
        message='Este es un email de prueba. Si recibes esto, la configuracion funciona correctamente.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email_host_user],
        connection=connection,
        fail_silently=False,
    )
    
    connection.close()
    
    print()
    print("=" * 60)
    print("SUCCESS: EMAIL ENVIADO CON PUERTO 465!")
    print("=" * 60)
    print()
    
    # Actualizar .env
    env_path = Path('.env')
    contenido = env_path.read_text(encoding='utf-8')
    lineas = contenido.split('\n')
    nuevas_lineas = []
    
    for linea in lineas:
        if linea.startswith('EMAIL_PORT='):
            nuevas_lineas.append('EMAIL_PORT=465')
        elif linea.startswith('EMAIL_USE_TLS='):
            nuevas_lineas.append('EMAIL_USE_TLS=False')
            nuevas_lineas.append('EMAIL_USE_SSL=True')
        elif linea.startswith('EMAIL_USE_SSL='):
            nuevas_lineas.append('EMAIL_USE_SSL=True')
        elif not linea.startswith('EMAIL_USE_SSL='):
            nuevas_lineas.append(linea)
    
    env_path.write_text('\n'.join(nuevas_lineas), encoding='utf-8')
    
    print("Configuracion aplicada en .env:")
    print("  EMAIL_PORT=465")
    print("  EMAIL_USE_SSL=True")
    print("  EMAIL_USE_TLS=False")
    print()
    print("Revisa tu bandeja de entrada en:", email_host_user)
    print()
    print("REINICIA el servidor Django")
    
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {str(e)[:150]}")
    print()
    print("El puerto 465 tampoco funciona.")
    print()
    print("Por favor, revisa en tu otro proyecto que funciona:")
    print("1. Que valor exacto tiene EMAIL_HOST?")
    print("2. Que valor exacto tiene EMAIL_PORT?")
    print("3. Tiene EMAIL_USE_TLS o EMAIL_USE_SSL?")
    print()
    print("O copia todas las lineas de EMAIL de ese proyecto aqui")
