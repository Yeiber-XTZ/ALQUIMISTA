# 📧 Guía de Configuración de Email

## ✅ Estado Actual

Las variables de email ya están configuradas en tu archivo `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@alquimista.com
```

## 🔧 Configuración Actual

### Modo Desarrollo (Activo)
- **EMAIL_BACKEND**: `console.EmailBackend`
- **Comportamiento**: Los emails se muestran en la consola cuando ejecutas `python manage.py runserver`
- **Ventaja**: No necesitas configurar SMTP, perfecto para desarrollo

### Modo Producción (Para cuando necesites enviar emails reales)

## 📝 Cómo Configurar Gmail para Enviar Emails Reales

### Paso 1: Generar Contraseña de Aplicación

1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. Activa la **Verificación en 2 pasos** (si no la tienes activada)
3. Ve a: https://myaccount.google.com/apppasswords
4. Selecciona:
   - **Aplicación**: Correo
   - **Dispositivo**: Otro (nombre personalizado)
   - **Nombre**: ALQUIMISTA
5. Haz clic en **Generar**
6. Copia la **contraseña de 16 caracteres** (ejemplo: `abcd efgh ijkl mnop`)

### Paso 2: Actualizar el archivo .env

Abre el archivo `.env` y cambia estas líneas:

```env
# Cambiar de console a smtp
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

# Agregar tu email de Gmail
EMAIL_HOST_USER=tu-email@gmail.com

# Agregar la contraseña de aplicación (sin espacios)
EMAIL_HOST_PASSWORD=abcdefghijklmnop
```

**Ejemplo completo:**
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=yeimena53@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop
DEFAULT_FROM_EMAIL=noreply@alquimista.com
```

### Paso 3: Reiniciar el Servidor

```bash
python manage.py runserver
```

## 🧪 Probar el Sistema de Emails

### En Desarrollo (Console Backend)

1. Registra un nuevo usuario en: http://127.0.0.1:8000/register/
2. Revisa la consola donde ejecutas `runserver`
3. Verás el email completo mostrado en la consola

### En Producción (SMTP Backend)

1. Configura las credenciales en `.env` (como se explicó arriba)
2. Reinicia el servidor
3. Registra un nuevo usuario
4. Revisa el correo del usuario registrado

## 🔄 Cambiar Entre Modos

### Para Desarrollo (emails en consola):
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Para Producción (emails reales):
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicacion
```

## 📧 Otros Proveedores de Email

### Outlook/Hotmail
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@outlook.com
EMAIL_HOST_PASSWORD=tu-contraseña
DEFAULT_FROM_EMAIL=noreply@alquimista.com
```

### Yahoo
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@yahoo.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicacion
DEFAULT_FROM_EMAIL=noreply@alquimista.com
```

## ⚠️ Solución de Problemas

### Error: "SMTPAuthenticationError"
- ✅ Verifica que `EMAIL_HOST_USER` sea tu email completo
- ✅ Para Gmail, usa una **contraseña de aplicación**, no tu contraseña normal
- ✅ Asegúrate de que la verificación en 2 pasos esté activada en Gmail

### Error: "Connection refused"
- ✅ Verifica que `EMAIL_HOST` y `EMAIL_PORT` sean correctos
- ✅ Asegúrate de que tu firewall no bloquee la conexión SMTP
- ✅ Prueba con otro puerto (465 para SSL)

### Los emails no se envían
- ✅ Verifica que `EMAIL_BACKEND` esté configurado como `smtp.EmailBackend`
- ✅ Revisa los logs de Django para ver errores específicos
- ✅ En desarrollo, usa `console.EmailBackend` para ver los emails en la consola

### Los emails van a spam
- ✅ Configura `DEFAULT_FROM_EMAIL` con un dominio válido
- ✅ Considera usar un servicio profesional como SendGrid o Mailgun
- ✅ Verifica los registros SPF y DKIM de tu dominio

## 📋 Checklist de Configuración

- [x] Variables de email agregadas al `.env`
- [ ] (Opcional) Configurar Gmail para producción
- [ ] (Opcional) Probar envío de emails reales
- [ ] (Opcional) Configurar dominio personalizado para `DEFAULT_FROM_EMAIL`

## 🎯 Próximos Pasos

1. **Ahora mismo**: El sistema funciona en modo desarrollo (emails en consola)
2. **Para producción**: Configura Gmail siguiendo los pasos arriba
3. **Opcional**: Considera usar un servicio profesional de email para mejor deliverability
