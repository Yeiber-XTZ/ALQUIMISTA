"""
Script para copiar la configuracion de email desde otro proyecto
"""
from pathlib import Path

print("=" * 60)
print("COPIAR CONFIGURACION DE EMAIL")
print("=" * 60)
print()
print("Por favor, revisa tu otro proyecto que funciona y dime:")
print()
print("1. Que valor tiene EMAIL_HOST? (ej: smtp.gmail.com, smtp.office365.com, etc.)")
print("2. Que valor tiene EMAIL_PORT? (ej: 587, 465, etc.)")
print("3. Que valor tiene EMAIL_USE_TLS? (True o False)")
print()
print("O si prefieres, puedes copiar directamente las lineas de EMAIL del otro proyecto")
print("y las actualizo aqui automaticamente.")
print()
print("Mientras tanto, voy a actualizar las credenciales que me diste...")

env_path = Path('.env')

if not env_path.exists():
    print("ERROR: El archivo .env no existe")
    exit(1)

# Credenciales que me dio el usuario
EMAIL_HOST_USER = 'yeiber.mena.dev@ebanocompany.com'
EMAIL_HOST_PASSWORD = 'ccgkzsxkbwkwwigs'

# Leer contenido actual
contenido = env_path.read_text(encoding='utf-8')
lineas = contenido.split('\n')
nuevas_lineas = []

for linea in lineas:
    if linea.startswith('EMAIL_HOST_USER='):
        nuevas_lineas.append(f'EMAIL_HOST_USER={EMAIL_HOST_USER}')
    elif linea.startswith('EMAIL_HOST_PASSWORD='):
        nuevas_lineas.append(f'EMAIL_HOST_PASSWORD={EMAIL_HOST_PASSWORD}')
    else:
        nuevas_lineas.append(linea)

# Guardar
env_path.write_text('\n'.join(nuevas_lineas), encoding='utf-8')

print()
print("SUCCESS: Credenciales actualizadas")
print(f"  EMAIL_HOST_USER={EMAIL_HOST_USER}")
print(f"  EMAIL_HOST_PASSWORD={EMAIL_HOST_PASSWORD[:10]}...")
print()
print("Ahora necesito que me digas el EMAIL_HOST de tu otro proyecto")
