"""
Script para configurar SMTP para Microsoft 365
"""
from pathlib import Path

env_path = Path('.env')

if not env_path.exists():
    print("ERROR: El archivo .env no existe")
    exit(1)

contenido = env_path.read_text(encoding='utf-8')
lineas = contenido.split('\n')
nuevas_lineas = []

for linea in lineas:
    if linea.startswith('EMAIL_HOST='):
        nuevas_lineas.append('EMAIL_HOST=smtp.office365.com')
    elif linea.startswith('EMAIL_PORT='):
        nuevas_lineas.append('EMAIL_PORT=587')
    elif linea.startswith('EMAIL_USE_TLS='):
        nuevas_lineas.append('EMAIL_USE_TLS=True')
    else:
        nuevas_lineas.append(linea)

env_path.write_text('\n'.join(nuevas_lineas), encoding='utf-8')

print("SUCCESS: Configuracion SMTP para Microsoft 365 aplicada")
print()
print("Configuracion:")
print("  EMAIL_HOST=smtp.office365.com")
print("  EMAIL_PORT=587")
print("  EMAIL_USE_TLS=True")
print()
print("IMPORTANTE:")
print("1. Si tienes verificacion en 2 pasos, genera una contrasena de aplicacion")
print("2. Si NO tienes 2FA, usa tu contrasena normal de Microsoft")
print("3. REINICIA el servidor Django")
