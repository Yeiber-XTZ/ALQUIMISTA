"""
Script para activar el envio de emails reales via SMTP
"""
import os
from pathlib import Path

env_path = Path('.env')

if not env_path.exists():
    print("ERROR: El archivo .env no existe")
    exit(1)

# Leer contenido actual
contenido = env_path.read_text(encoding='utf-8')

# Verificar si ya tiene SMTP configurado
if 'EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend' in contenido:
    print("El backend SMTP ya esta activado")
    print("Si los emails no se envian, verifica:")
    print("1. Que EMAIL_HOST_USER tenga tu email correcto")
    print("2. Que EMAIL_HOST_PASSWORD tenga una contrasena de aplicacion valida")
    print("3. Que hayas reiniciado el servidor Django")
    exit(0)

# Cambiar de console a smtp
if 'EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend' in contenido:
    nuevo_contenido = contenido.replace(
        'EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend',
        'EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend'
    )
    env_path.write_text(nuevo_contenido, encoding='utf-8')
    print("SUCCESS: Backend SMTP activado correctamente")
    print()
    print("IMPORTANTE:")
    print("1. Verifica que EMAIL_HOST_USER tenga tu email de Gmail")
    print("2. Verifica que EMAIL_HOST_PASSWORD tenga una contrasena de aplicacion")
    print("3. REINICIA el servidor Django (Ctrl+C y luego python manage.py runserver)")
    print()
    print("Para generar una contrasena de aplicacion de Gmail:")
    print("https://myaccount.google.com/apppasswords")
else:
    # Buscar cualquier otra configuracion de EMAIL_BACKEND
    lineas = contenido.split('\n')
    nueva_contenido = []
    encontrado = False
    
    for linea in lineas:
        if linea.startswith('EMAIL_BACKEND='):
            nueva_contenido.append('EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend')
            encontrado = True
        else:
            nueva_contenido.append(linea)
    
    if encontrado:
        env_path.write_text('\n'.join(nueva_contenido), encoding='utf-8')
        print("SUCCESS: Backend SMTP activado correctamente")
    else:
        # Agregar la configuracion si no existe
        nuevo_contenido = contenido.rstrip() + '\nEMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend\n'
        env_path.write_text(nuevo_contenido, encoding='utf-8')
        print("SUCCESS: Backend SMTP agregado al archivo .env")
    
    print()
    print("IMPORTANTE:")
    print("1. Verifica que EMAIL_HOST_USER tenga tu email de Gmail")
    print("2. Verifica que EMAIL_HOST_PASSWORD tenga una contrasena de aplicacion")
    print("3. REINICIA el servidor Django (Ctrl+C y luego python manage.py runserver)")
