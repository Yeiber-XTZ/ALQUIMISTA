"""
Script para configurar las variables de entorno en el archivo .env
"""
import os
from pathlib import Path

# Ruta del archivo .env
env_path = Path('.env')

# Variables de email a agregar
email_config = """
# ============================================
# CONFIGURACION DE EMAIL
# ============================================
# Backend de Email (console para desarrollo, smtp para produccion)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Configuracion SMTP (solo necesario si EMAIL_BACKEND es smtp.EmailBackend)
# Para Gmail, usa una contrasena de aplicacion: https://myaccount.google.com/apppasswords
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@alquimista.com
"""

def configurar_env():
    """Agrega las variables de email al archivo .env si no existen"""
    if not env_path.exists():
        print("El archivo .env no existe. Creando desde env.example.txt...")
        example_path = Path('env.example.txt')
        if example_path.exists():
            env_path.write_text(example_path.read_text(), encoding='utf-8')
        else:
            print("Tampoco existe env.example.txt")
            return False
    
    # Leer contenido actual
    contenido_actual = env_path.read_text(encoding='utf-8')
    
    # Verificar si ya tiene configuracion de email
    if 'EMAIL_BACKEND' in contenido_actual:
        print("El archivo .env ya tiene configuracion de email")
        print("\nConfiguracion actual de email:")
        for linea in contenido_actual.split('\n'):
            if 'EMAIL' in linea and not linea.strip().startswith('#'):
                print(f"  {linea}")
        return True
    
    # Agregar configuracion de email
    print("Agregando configuracion de email al archivo .env...")
    
    # Agregar al final del archivo
    nuevo_contenido = contenido_actual.rstrip() + email_config
    
    # Guardar
    env_path.write_text(nuevo_contenido, encoding='utf-8')
    
    print("Configuracion de email agregada exitosamente!")
    print("\nVariables agregadas:")
    print("  - EMAIL_BACKEND (console para desarrollo)")
    print("  - EMAIL_HOST (smtp.gmail.com)")
    print("  - EMAIL_PORT (587)")
    print("  - EMAIL_USE_TLS (True)")
    print("  - EMAIL_HOST_USER (vacio - configurar con tu email)")
    print("  - EMAIL_HOST_PASSWORD (vacio - configurar con contrasena de aplicacion)")
    print("  - DEFAULT_FROM_EMAIL (noreply@alquimista.com)")
    
    print("\nIMPORTANTE:")
    print("  1. Para desarrollo: Los emails se mostraran en la consola (ya configurado)")
    print("  2. Para produccion: Edita .env y cambia:")
    print("     - EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend")
    print("     - EMAIL_HOST_USER=tu-email@gmail.com")
    print("     - EMAIL_HOST_PASSWORD=tu-contrasena-de-aplicacion")
    print("  3. Para Gmail, genera una contrasena de aplicacion en:")
    print("     https://myaccount.google.com/apppasswords")
    
    return True

if __name__ == '__main__':
    try:
        configurar_env()
    except Exception as e:
        print(f"Error: {e}")
