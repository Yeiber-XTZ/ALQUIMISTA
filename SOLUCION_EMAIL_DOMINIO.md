# Solución para Envío de Emails con Dominio Personalizado

## Problema Detectado

Tu email es `yeiber.mena.dev@ebanocompany.com` (dominio personalizado), pero estás usando la configuración SMTP de Gmail, lo cual causa errores de conexión.

## Soluciones Según tu Proveedor

### Opción 1: Si usas Google Workspace (Gmail Empresarial)

**Configuración en `.env`:**
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=yeiber.mena.dev@ebanocompany.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicación
DEFAULT_FROM_EMAIL=noreply@alquimista.com
```

**Pasos:**
1. Activa la verificación en 2 pasos: https://myaccount.google.com/security
2. Genera una contraseña de aplicación: https://myaccount.google.com/apppasswords
   - Selecciona "Correo" y "Otro (nombre personalizado)"
   - Nombre: ALQUIMISTA
   - Copia la contraseña de 16 caracteres
3. Usa esa contraseña en `EMAIL_HOST_PASSWORD` (NO tu contraseña normal)

### Opción 2: Si usas Microsoft 365 / Exchange

**Configuración en `.env`:**
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=yeiber.mena.dev@ebanocompany.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicación
DEFAULT_FROM_EMAIL=noreply@alquimista.com
```

**Pasos:**
1. Si tienes verificación en 2 pasos activada:
   - Ve a: https://account.microsoft.com/security
   - Genera una contraseña de aplicación
   - Úsala en `EMAIL_HOST_PASSWORD`
2. Si NO tienes 2FA, usa tu contraseña normal de Microsoft

### Opción 3: Otro Proveedor

Contacta a tu administrador de IT para obtener:
- Servidor SMTP (ej: `mail.ebanocompany.com`)
- Puerto SMTP (comúnmente 587 o 465)
- Si requiere TLS/SSL

## Cómo Aplicar la Configuración

### Método 1: Manualmente
Edita el archivo `.env` y actualiza las líneas según tu proveedor.

### Método 2: Usando el Script
Ejecuta el script correspondiente según tu proveedor:

**Para Google Workspace:**
```bash
python configurar_google_workspace.py
```

**Para Microsoft 365:**
```bash
python configurar_microsoft365.py
```

## Verificar la Configuración

Después de configurar, ejecuta:
```bash
python test_email.py
```

Esto enviará un email de prueba a tu dirección.

## Reiniciar el Servidor

**IMPORTANTE:** Después de cambiar el `.env`, siempre reinicia el servidor Django:
1. Detén el servidor (Ctrl+C)
2. Inicia de nuevo: `python manage.py runserver`

## Solución de Problemas

### Error: "Authentication failed"
- Verifica que `EMAIL_HOST_PASSWORD` sea una contraseña de aplicación, no tu contraseña normal
- Para Google Workspace: asegúrate de tener 2FA activada

### Error: "Connection timeout"
- Verifica que `EMAIL_HOST` sea correcto para tu proveedor
- Verifica tu conexión a internet
- Algunos firewalls bloquean el puerto 587

### Error: "SMTP server not found"
- Verifica que el servidor SMTP sea correcto
- Contacta a tu administrador de IT

## Estado Actual

Tu configuración actual:
- ✅ EMAIL_BACKEND: SMTP (activado)
- ✅ EMAIL_HOST_USER: Configurado
- ✅ EMAIL_HOST_PASSWORD: Configurado
- ⚠️ EMAIL_HOST: Probablemente incorrecto (está en `smtp.gmail.com` pero tu email no es de Gmail)

**Acción requerida:** Identifica tu proveedor de email y actualiza `EMAIL_HOST` en el `.env`
