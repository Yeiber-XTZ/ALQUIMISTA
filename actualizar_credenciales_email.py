"""
Script para actualizar las credenciales de email desde otro proyecto
"""
from pathlib import Path

env_path = Path('.env')

if not env_path.exists():
    print("ERROR: El archivo .env no existe")
    exit(1)

# Credenciales del otro proyecto que funciona
EMAIL_HOST_USER = 'yeiber.mena.dev@ebanocompany.com'
EMAIL_HOST_PASSWORD = 'ccgkzsxkbwkwwigs'

# Leer contenido actual
contenido = env_path.read_text(encoding='utf-8')
lineas = contenido.split('\n')
nuevas_lineas = []
actualizado = False

for linea in lineas:
    if linea.startswith('EMAIL_HOST_USER='):
        nuevas_lineas.append(f'EMAIL_HOST_USER={EMAIL_HOST_USER}')
        actualizado = True
    elif linea.startswith('EMAIL_HOST_PASSWORD='):
        nuevas_lineas.append(f'EMAIL_HOST_PASSWORD={EMAIL_HOST_PASSWORD}')
        actualizado = True
    else:
        nuevas_lineas.append(linea)

# Si no existian, agregarlas
if not actualizado:
    nuevas_lineas.append(f'EMAIL_HOST_USER={EMAIL_HOST_USER}')
    nuevas_lineas.append(f'EMAIL_HOST_PASSWORD={EMAIL_HOST_PASSWORD}')

# Guardar
env_path.write_text('\n'.join(nuevas_lineas), encoding='utf-8')

print("SUCCESS: Credenciales de email actualizadas")
print()
print("Configuracion aplicada:")
print(f"  EMAIL_HOST_USER={EMAIL_HOST_USER}")
print(f"  EMAIL_HOST_PASSWORD={EMAIL_HOST_PASSWORD[:10]}...")
print()
print("Ahora necesitamos verificar el EMAIL_HOST correcto.")
print("Probando configuraciones comunes...")
