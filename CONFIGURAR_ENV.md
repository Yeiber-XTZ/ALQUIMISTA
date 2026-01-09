# 📧 Configuración del Archivo .env

Este archivo contiene las instrucciones para configurar el archivo `.env` con todas las variables necesarias para el sistema de emails y otras configuraciones.

## 🚀 Pasos para Configurar

### 1. Crear el archivo .env

Copia el archivo `env.example.txt` y renómbralo a `.env`:

```bash
# Windows PowerShell
Copy-Item env.example.txt .env

# Windows CMD
copy env.example.txt .env

# Linux/Mac
cp env.example.txt .env
```

### 2. Editar el archivo .env

Abre el archivo `.env` con tu editor de texto y configura las siguientes variables:

#### Base de Datos (MySQL)
```env
DB_NAME=alquimista_db
DB_USER=root
DB_PASSWORD=tu_contraseña_mysql
DB_HOST=localhost
DB_PORT=3306
```

#### Django
```env
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
```

#### Email (IMPORTANTE)

**Para Desarrollo (emails en consola):**
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**Para Producción (emails reales):**

##### Opción 1: Gmail
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicacion
DEFAULT_FROM_EMAIL=noreply@alquimista.com
```

**⚠️ IMPORTANTE para Gmail:**
- No uses tu contraseña normal de Gmail
- Debes generar una "Contraseña de aplicación":
  1. Ve a: https://myaccount.google.com/apppasswords
  2. Selecciona "Correo" y "Otro (nombre personalizado)"
  3. Escribe "ALQUIMISTA" y genera
  4. Copia la contraseña de 16 caracteres
  5. Úsala en `EMAIL_HOST_PASSWORD`

##### Opción 2: Outlook/Hotmail
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@outlook.com
EMAIL_HOST_PASSWORD=tu-contraseña
DEFAULT_FROM_EMAIL=noreply@alquimista.com
```

##### Opción 3: Yahoo
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@yahoo.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicacion
DEFAULT_FROM_EMAIL=noreply@alquimista.com
```

#### Dominios ngrok (Opcional)
```env
CSRF_TRUSTED_ORIGINS=https://tu-dominio.ngrok-free.app
```

## ✅ Verificación

Después de configurar el `.env`, reinicia el servidor Django:

```bash
python manage.py runserver
```

### Probar el Sistema de Emails

1. **En Desarrollo (console backend):**
   - Registra un nuevo usuario
   - El email aparecerá en la consola donde ejecutas `runserver`

2. **En Producción (smtp backend):**
   - Registra un nuevo usuario
   - Revisa el correo del usuario registrado
   - También puedes probar la recuperación de contraseña

## 🔒 Seguridad

- ✅ El archivo `.env` está en `.gitignore` (no se subirá a Git)
- ✅ Nunca compartas tu archivo `.env`
- ✅ En producción, usa variables de entorno del servidor si es posible
- ✅ Cambia `SECRET_KEY` y `DEBUG=False` en producción

## 📝 Ejemplo Completo de .env

```env
# Base de Datos
DB_NAME=alquimista_db
DB_USER=root
DB_PASSWORD=mi_contraseña_segura
DB_HOST=localhost
DB_PORT=3306

# Django
SECRET_KEY=django-insecure-cambiar-en-produccion
DEBUG=True

# Email (Desarrollo - Console)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Email (Producción - Gmail)
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=mi-email@gmail.com
# EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
# DEFAULT_FROM_EMAIL=noreply@alquimista.com

# ngrok (si lo usas)
# CSRF_TRUSTED_ORIGINS=https://abc123.ngrok-free.app
```

## 🆘 Solución de Problemas

### Error: "SMTPAuthenticationError"
- Verifica que `EMAIL_HOST_USER` y `EMAIL_HOST_PASSWORD` sean correctos
- Para Gmail, asegúrate de usar una contraseña de aplicación, no tu contraseña normal
- Verifica que la verificación en 2 pasos esté activada en Gmail

### Error: "Connection refused"
- Verifica que `EMAIL_HOST` y `EMAIL_PORT` sean correctos
- Asegúrate de que tu firewall no bloquee la conexión SMTP

### Emails no se envían
- Verifica que `EMAIL_BACKEND` esté configurado correctamente
- Revisa los logs de Django para ver errores específicos
- En desarrollo, usa `console.EmailBackend` para ver los emails en la consola
