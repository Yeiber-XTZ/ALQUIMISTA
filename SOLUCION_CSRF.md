# Solución para Error CSRF con ngrok

## Problema
Cuando el dominio de ngrok cambia, Django bloquea las solicitudes POST por seguridad CSRF.

## Solución Rápida

### Opción 1: Agregar el nuevo dominio manualmente

1. Abre `alquimista_project/settings.py`
2. Busca la sección `CSRF_TRUSTED_ORIGINS` (línea ~45)
3. Agrega el nuevo dominio de ngrok en formato `'https://tu-dominio.ngrok-free.app'`
4. Reinicia el servidor Django

Ejemplo:
```python
CSRF_TRUSTED_ORIGINS = [
    'https://e81b08a7b841.ngrok-free.app',  # Dominio anterior
    'https://NUEVO-DOMINIO.ngrok-free.app',  # Agrega aquí el nuevo dominio
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
```

### Opción 2: Usar variable de entorno

1. Establece la variable de entorno antes de ejecutar Django:
```bash
# Windows PowerShell
$env:CSRF_TRUSTED_ORIGINS="https://nuevo-dominio.ngrok-free.app"

# Windows CMD
set CSRF_TRUSTED_ORIGINS=https://nuevo-dominio.ngrok-free.app

# Linux/Mac
export CSRF_TRUSTED_ORIGINS="https://nuevo-dominio.ngrok-free.app"
```

2. Ejecuta el servidor Django normalmente

### Opción 3: Obtener el dominio automáticamente desde ngrok

Si tienes ngrok ejecutándose, puedes obtener el dominio con:
```bash
# Windows PowerShell
$ngrokUrl = (Invoke-WebRequest -Uri http://localhost:4040/api/tunnels -UseBasicParsing | ConvertFrom-Json).tunnels[0].public_url
echo "Agrega esto a CSRF_TRUSTED_ORIGINS: $ngrokUrl"
```

## Verificación

Después de agregar el dominio:
1. Reinicia el servidor Django
2. Intenta enviar un formulario nuevamente
3. El error CSRF debería desaparecer

## Nota Importante

⚠️ **SOLO PARA DESARROLLO**: Esta configuración es solo para desarrollo local. En producción, debes:
- Deshabilitar `DEBUG = False`
- Configurar `ALLOWED_HOSTS` con dominios específicos
- Configurar `CSRF_TRUSTED_ORIGINS` solo con tus dominios de producción
