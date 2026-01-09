"""
Script para probar envio de email con tus credenciales
"""
import os
import django
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alquimista_project.settings')
django.setup()

from django.core.mail import get_connection, send_mail
from django.conf import settings

print("=" * 60)
print("PRUEBA DE ENVIO CON TUS CREDENCIALES")
print("=" * 60)
print()

email_host_user = os.getenv('EMAIL_HOST_USER', 'yeiber.mena.dev@ebanocompany.com')
email_host_password = os.getenv('EMAIL_HOST_PASSWORD', 'ccgkzsxkbwkwwigs')

print(f"Email: {email_host_user}")
print(f"Contrasena: {email_host_password[:10]}...")
print()

# Configuraciones a probar (las mas comunes para dominios empresariales)
configuraciones = [
    {
        'nombre': 'Google Workspace (Gmail Empresarial)',
        'EMAIL_HOST': 'smtp.gmail.com',
        'EMAIL_PORT': 587,
        'EMAIL_USE_TLS': True
    },
    {
        'nombre': 'Microsoft 365',
        'EMAIL_HOST': 'smtp.office365.com',
        'EMAIL_PORT': 587,
        'EMAIL_USE_TLS': True
    },
    {
        'nombre': 'Microsoft Outlook',
        'EMAIL_HOST': 'smtp-mail.outlook.com',
        'EMAIL_PORT': 587,
        'EMAIL_USE_TLS': True
    }
]

env_path = Path('.env')

for config in configuraciones:
    print(f"Probando: {config['nombre']}")
    print(f"  Host: {config['EMAIL_HOST']}")
    print(f"  Port: {config['EMAIL_PORT']}")
    
    try:
        # Crear conexion
        connection = get_connection(
            host=config['EMAIL_HOST'],
            port=config['EMAIL_PORT'],
            username=email_host_user,
            password=email_host_password,
            use_tls=config['EMAIL_USE_TLS'],
            timeout=15
        )
        
        # Probar conexion
        print("  Conectando...")
        connection.open()
        print("  Conexion exitosa!")
        
        # Intentar enviar email de prueba
        print("  Enviando email de prueba...")
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
        print("SUCCESS: EMAIL ENVIADO CORRECTAMENTE!")
        print("=" * 60)
        print()
        print(f"Configuracion que funciona: {config['nombre']}")
        print()
        
        # Actualizar .env con la configuracion que funciona
        contenido = env_path.read_text(encoding='utf-8')
        lineas = contenido.split('\n')
        nuevas_lineas = []
        
        for linea in lineas:
            if linea.startswith('EMAIL_HOST='):
                nuevas_lineas.append(f"EMAIL_HOST={config['EMAIL_HOST']}")
            elif linea.startswith('EMAIL_PORT='):
                nuevas_lineas.append(f"EMAIL_PORT={config['EMAIL_PORT']}")
            elif linea.startswith('EMAIL_USE_TLS='):
                nuevas_lineas.append(f"EMAIL_USE_TLS={config['EMAIL_USE_TLS']}")
            else:
                nuevas_lineas.append(linea)
        
        env_path.write_text('\n'.join(nuevas_lineas), encoding='utf-8')
        
        print("Configuracion aplicada en .env:")
        print(f"  EMAIL_HOST={config['EMAIL_HOST']}")
        print(f"  EMAIL_PORT={config['EMAIL_PORT']}")
        print(f"  EMAIL_USE_TLS={config['EMAIL_USE_TLS']}")
        print()
        print("Revisa tu bandeja de entrada (y spam) en:", email_host_user)
        print()
        print("REINICIA el servidor Django para aplicar los cambios")
        exit(0)
        
    except Exception as e:
        error_msg = str(e)
        if 'authentication' in error_msg.lower() or '535' in error_msg:
            print(f"  ERROR: Autenticacion fallida")
            print(f"         (Esta configuracion no es la correcta)")
        elif 'timeout' in error_msg.lower() or '10060' in error_msg:
            print(f"  ERROR: Timeout de conexion")
            print(f"         (El servidor SMTP no responde)")
        else:
            print(f"  ERROR: {type(e).__name__}: {error_msg[:80]}")
        print()
        continue

print("=" * 60)
print("NO SE PUDO ENVIAR EL EMAIL CON NINGUNA CONFIGURACION")
print("=" * 60)
print()
print("Posibles causas:")
print("1. Las credenciales no son correctas")
print("2. El servidor SMTP es diferente (contacta a tu administrador)")
print("3. Problema de conexion a internet o firewall")
print()
print("Puedes verificar en tu otro proyecto que funciona:")
print("- Que EMAIL_HOST este usando")
print("- Y copiar esa configuracion aqui")
