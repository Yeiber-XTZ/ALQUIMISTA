"""
Script para probar diferentes configuraciones SMTP para dominio empresarial
"""
import os
import django
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configuraciones a probar
configuraciones = [
    {
        'nombre': 'Google Workspace (Gmail Empresarial)',
        'EMAIL_HOST': 'smtp.gmail.com',
        'EMAIL_PORT': 587,
        'EMAIL_USE_TLS': True
    },
    {
        'nombre': 'Microsoft 365 / Exchange',
        'EMAIL_HOST': 'smtp.office365.com',
        'EMAIL_PORT': 587,
        'EMAIL_USE_TLS': True
    },
    {
        'nombre': 'Microsoft 365 (Alternativa)',
        'EMAIL_HOST': 'smtp-mail.outlook.com',
        'EMAIL_PORT': 587,
        'EMAIL_USE_TLS': True
    }
]

print("=" * 60)
print("PRUEBA DE CONFIGURACIONES SMTP")
print("=" * 60)
print()

email_host_user = os.getenv('EMAIL_HOST_USER', '')
email_host_password = os.getenv('EMAIL_HOST_PASSWORD', '')

if not email_host_user or not email_host_password:
    print("ERROR: EMAIL_HOST_USER o EMAIL_HOST_PASSWORD no estan configurados")
    exit(1)

print(f"Email: {email_host_user}")
print(f"Contrasena: {'*' * len(email_host_password)}")
print()
print("Probando configuraciones comunes para dominios empresariales...")
print()

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alquimista_project.settings')
django.setup()

from django.core.mail import get_connection
from django.conf import settings

for config in configuraciones:
    print(f"Probando: {config['nombre']}")
    print(f"  Host: {config['EMAIL_HOST']}")
    print(f"  Port: {config['EMAIL_PORT']}")
    print(f"  TLS: {config['EMAIL_USE_TLS']}")
    
    try:
        # Crear conexion con esta configuracion
        connection = get_connection(
            host=config['EMAIL_HOST'],
            port=config['EMAIL_PORT'],
            username=email_host_user,
            password=email_host_password,
            use_tls=config['EMAIL_USE_TLS'],
            timeout=10  # 10 segundos de timeout
        )
        
        # Probar conexion
        connection.open()
        print("  SUCCESS: Conexion exitosa!")
        connection.close()
        
        # Si funciona, actualizar .env
        env_path = Path('.env')
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
        
        print()
        print("=" * 60)
        print("CONFIGURACION ENCONTRADA Y APLICADA!")
        print("=" * 60)
        print()
        print(f"Configuracion aplicada: {config['nombre']}")
        print(f"EMAIL_HOST={config['EMAIL_HOST']}")
        print(f"EMAIL_PORT={config['EMAIL_PORT']}")
        print(f"EMAIL_USE_TLS={config['EMAIL_USE_TLS']}")
        print()
        print("REINICIA el servidor Django y prueba enviar un email")
        exit(0)
        
    except Exception as e:
        print(f"  ERROR: {type(e).__name__}: {str(e)[:100]}")
        print()
        continue

print("=" * 60)
print("NO SE ENCONTRO UNA CONFIGURACION FUNCIONAL")
print("=" * 60)
print()
print("Opciones:")
print("1. Verifica que tu contrasena de aplicacion sea correcta")
print("2. Contacta a tu administrador de IT para obtener:")
print("   - Servidor SMTP correcto")
print("   - Puerto SMTP")
print("   - Si requiere TLS/SSL")
print()
print("3. Si usas Google Workspace, asegurate de:")
print("   - Tener verificacion en 2 pasos activada")
print("   - Usar una contrasena de aplicacion")
print()
print("4. Si usas Microsoft 365, asegurate de:")
print("   - Usar tu contrasena de Microsoft")
print("   - O generar una contrasena de aplicacion si tienes 2FA")
