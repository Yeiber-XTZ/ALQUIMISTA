"""
Script para configurar SMTP para Google Workspace
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
        nuevas_lineas.append('EMAIL_HOST=smtp.gmail.com')
    elif linea.startswith('EMAIL_PORT='):
        nuevas_lineas.append('EMAIL_PORT=587')
    elif linea.startswith('EMAIL_USE_TLS='):
        nuevas_lineas.append('EMAIL_USE_TLS=True')
    else:
        nuevas_lineas.append(linea)

env_path.write_text('\n'.join(nuevas_lineas), encoding='utf-8')

print("SUCCESS: Configuracion SMTP para Google Workspace aplicada")
print()
print("Configuracion:")
print("  EMAIL_HOST=smtp.gmail.com")
print("  EMAIL_PORT=587")
print("  EMAIL_USE_TLS=True")
print()
print("IMPORTANTE:")
print("1. Asegurate de tener verificacion en 2 pasos activada")
print("2. Genera una contrasena de aplicacion: https://myaccount.google.com/apppasswords")
print("3. Usa esa contrasena en EMAIL_HOST_PASSWORD")
print("4. REINICIA el servidor Django")
