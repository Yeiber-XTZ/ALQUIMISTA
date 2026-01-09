"""
Script para actualizar automáticamente el dominio de ngrok en settings.py
Ejecuta este script cuando cambie tu dominio de ngrok.
"""

import re
import requests
import sys

def get_ngrok_url():
    """Obtiene la URL pública de ngrok desde la API local"""
    try:
        response = requests.get('http://localhost:4040/api/tunnels', timeout=2)
        data = response.json()
        if data.get('tunnels'):
            return data['tunnels'][0]['public_url']
    except Exception as e:
        print(f"No se pudo obtener la URL de ngrok: {e}")
        print("Asegúrate de que ngrok esté ejecutándose en el puerto 4040")
    return None

def update_settings(ngrok_url):
    """Actualiza settings.py con el nuevo dominio de ngrok"""
    settings_path = 'alquimista_project/settings.py'
    
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convertir http a https si es necesario
        if ngrok_url.startswith('http://'):
            ngrok_url = ngrok_url.replace('http://', 'https://')
        
        # Buscar y actualizar ALLOWED_HOSTS
        allowed_hosts_pattern = r"ALLOWED_HOSTS = \['localhost', '127\.0\.0\.1', '[^']+'\]"
        new_allowed_hosts = f"ALLOWED_HOSTS = ['localhost', '127.0.0.1', '{ngrok_url.replace('https://', '').replace('http://', '')}']"
        content = re.sub(allowed_hosts_pattern, new_allowed_hosts, content)
        
        # Buscar y actualizar CSRF_TRUSTED_ORIGINS
        csrf_pattern = r"('https://[^']+\.ngrok-free\.app',)"
        new_csrf_entry = f"'{ngrok_url}',"
        
        # Si ya existe una entrada ngrok, reemplazarla
        if re.search(csrf_pattern, content):
            content = re.sub(csrf_pattern, new_csrf_entry, content, count=1)
        else:
            # Si no existe, agregarla después de la primera entrada
            csrf_list_pattern = r"(CSRF_TRUSTED_ORIGINS = \[)"
            replacement = rf"\1\n    '{ngrok_url}',"
            content = re.sub(csrf_list_pattern, replacement, content)
        
        # Guardar el archivo actualizado
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Settings actualizado con el dominio: {ngrok_url}")
        print("🔄 Reinicia el servidor Django para aplicar los cambios")
        return True
        
    except Exception as e:
        print(f"❌ Error al actualizar settings.py: {e}")
        return False

if __name__ == '__main__':
    print("🔍 Buscando dominio de ngrok...")
    
    # Intentar obtener el dominio automáticamente
    ngrok_url = get_ngrok_url()
    
    if not ngrok_url:
        # Si no se puede obtener automáticamente, pedir al usuario
        print("\n⚠️  No se pudo obtener el dominio automáticamente.")
        print("Por favor, ingresa el dominio de ngrok manualmente:")
        print("Ejemplo: https://abc123.ngrok-free.app")
        ngrok_url = input("Dominio: ").strip()
        
        if not ngrok_url:
            print("❌ No se proporcionó un dominio. Saliendo...")
            sys.exit(1)
    
    # Actualizar settings
    if update_settings(ngrok_url):
        print("\n✨ ¡Listo! El dominio ha sido actualizado.")
        print("📝 Recuerda reiniciar el servidor Django.")
    else:
        print("\n❌ Hubo un error al actualizar la configuración.")
        sys.exit(1)
