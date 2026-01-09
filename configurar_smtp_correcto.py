"""
Script para configurar SMTP segun el proveedor de email
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

env_path = Path('.env')
email_host_user = os.getenv('EMAIL_HOST_USER', '')

if not email_host_user:
    print("ERROR: EMAIL_HOST_USER no esta configurado")
    exit(1)

print("=" * 60)
print("CONFIGURACION SMTP SEGUN PROVEEDOR")
print("=" * 60)
print()
print(f"Email configurado: {email_host_user}")
print()

# Detectar proveedor
proveedor = None
if '@gmail.com' in email_host_user.lower():
    proveedor = 'Gmail'
elif '@outlook.com' in email_host_user.lower() or '@hotmail.com' in email_host_user.lower():
    proveedor = 'Outlook/Hotmail'
elif '@yahoo.com' in email_host_user.lower():
    proveedor = 'Yahoo'
else:
    # Dominio personalizado
    dominio = email_host_user.split('@')[1] if '@' in email_host_user else 'desconocido'
    proveedor = f'Dominio personalizado ({dominio})'

print(f"Proveedor detectado: {proveedor}")
print()

# Leer .env actual
contenido = env_path.read_text(encoding='utf-8')
lineas = contenido.split('\n')
nuevas_lineas = []

# Configuraciones por proveedor
configuraciones = {
    'Gmail': {
        'EMAIL_HOST': 'smtp.gmail.com',
        'EMAIL_PORT': '587',
        'EMAIL_USE_TLS': 'True'
    },
    'Outlook/Hotmail': {
        'EMAIL_HOST': 'smtp-mail.outlook.com',
        'EMAIL_PORT': '587',
        'EMAIL_USE_TLS': 'True'
    },
    'Yahoo': {
        'EMAIL_HOST': 'smtp.mail.yahoo.com',
        'EMAIL_PORT': '587',
        'EMAIL_USE_TLS': 'True'
    }
}

# Actualizar configuracion
for linea in lineas:
    if linea.startswith('EMAIL_HOST='):
        if proveedor in configuraciones:
            nuevas_lineas.append(f"EMAIL_HOST={configuraciones[proveedor]['EMAIL_HOST']}")
        else:
            nuevas_lineas.append(linea)  # Mantener la actual
    elif linea.startswith('EMAIL_PORT='):
        if proveedor in configuraciones:
            nuevas_lineas.append(f"EMAIL_PORT={configuraciones[proveedor]['EMAIL_PORT']}")
        else:
            nuevas_lineas.append(linea)
    elif linea.startswith('EMAIL_USE_TLS='):
        if proveedor in configuraciones:
            nuevas_lineas.append(f"EMAIL_USE_TLS={configuraciones[proveedor]['EMAIL_USE_TLS']}")
        else:
            nuevas_lineas.append(linea)
    else:
        nuevas_lineas.append(linea)

# Guardar cambios
env_path.write_text('\n'.join(nuevas_lineas), encoding='utf-8')

if proveedor in configuraciones:
    print("SUCCESS: Configuracion SMTP actualizada para", proveedor)
    print()
    print("Configuracion aplicada:")
    for key, value in configuraciones[proveedor].items():
        print(f"  {key}: {value}")
    print()
    
    if proveedor == 'Gmail':
        print("IMPORTANTE para Gmail:")
        print("1. Activa la verificacion en 2 pasos: https://myaccount.google.com/security")
        print("2. Genera una contrasena de aplicacion: https://myaccount.google.com/apppasswords")
        print("3. Usa esa contrasena en EMAIL_HOST_PASSWORD (no tu contrasena normal)")
    elif proveedor == 'Outlook/Hotmail':
        print("IMPORTANTE para Outlook/Hotmail:")
        print("1. Usa tu contrasena normal de Microsoft")
        print("2. Si tienes verificacion en 2 pasos, genera una contrasena de aplicacion")
    elif proveedor == 'Yahoo':
        print("IMPORTANTE para Yahoo:")
        print("1. Genera una contrasena de aplicacion en tu cuenta de Yahoo")
        print("2. Usa esa contrasena en EMAIL_HOST_PASSWORD")
else:
    print("ATENCION: Dominio personalizado detectado")
    print()
    print("Para dominios personalizados, necesitas:")
    print("1. Conocer el servidor SMTP de tu proveedor de email")
    print("2. Configurar manualmente EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS")
    print()
    print("Configuracion actual mantenida:")
    print(f"  EMAIL_HOST: {os.getenv('EMAIL_HOST', 'smtp.gmail.com')}")
    print(f"  EMAIL_PORT: {os.getenv('EMAIL_PORT', '587')}")
    print()
    print("Si tu dominio usa Gmail (Google Workspace), usa:")
    print("  EMAIL_HOST=smtp.gmail.com")
    print("  EMAIL_PORT=587")
    print("  EMAIL_USE_TLS=True")
    print()
    print("Si tu dominio usa Microsoft 365/Exchange, usa:")
    print("  EMAIL_HOST=smtp.office365.com")
    print("  EMAIL_PORT=587")
    print("  EMAIL_USE_TLS=True")

print()
print("REINICIA el servidor Django para aplicar los cambios")
