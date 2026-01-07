# 🚀 Guía de Configuración - ALQUIMISTA NELSON

## 📋 Requisitos Previos

- **Python 3.10+** instalado
- **MySQL** instalado y corriendo
- **pip** (gestor de paquetes de Python)

## 🔧 Pasos de Instalación

### 1. Crear Base de Datos MySQL

Abre MySQL y ejecuta:

```sql
CREATE DATABASE alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Configurar Variables de Entorno

El archivo `.env` ya está creado con valores por defecto. Si necesitas modificarlo:

```env
DB_NAME=alquimista_db
DB_USER=root
DB_PASSWORD=tu_contraseña_mysql
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=tu-secret-key-generado
DEBUG=True
```

**Nota:** Si tu MySQL no tiene contraseña, deja `DB_PASSWORD` vacío.

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar Migraciones

```bash
python manage.py migrate
```

O usa el script de inicialización:

```bash
python setup.py
```

### 5. Crear Superusuario

```bash
python manage.py createsuperuser
```

**Importante:** Cuando se te solicite, asegúrate de marcar `is_staff=True` para poder acceder al panel de administración.

### 6. Iniciar el Servidor

```bash
python manage.py runserver
```

## 🌐 Acceso al Sistema

- **Frontend Público:** http://127.0.0.1:8000/
- **Panel de Staff:** http://127.0.0.1:8000/staff/
- **Admin Django (opcional):** http://127.0.0.1:8000/admin/

## 📁 Estructura del Proyecto

```
ALQUIMISTA/
├── alquimista_project/     # Configuración del proyecto
├── core/                   # App principal
│   ├── models.py          # Modelos: Facet, Milestone, ContactMessage
│   ├── views.py           # Vistas públicas y del staff
│   ├── urls.py            # URLs
│   └── ...
├── templates/
│   ├── core/              # Templates públicos
│   └── staff/             # Templates del panel de staff
├── static/                # Archivos estáticos
├── media/                 # Archivos multimedia subidos
├── .env                   # Variables de entorno (no se sube a git)
└── requirements.txt       # Dependencias
```

## 🎨 Características

### Frontend Público
- ✅ Scroll horizontal tipo galería (inspirado en lebronjames.com)
- ✅ Animaciones con GSAP ScrollTrigger
- ✅ Diseño responsive con Tailwind CSS
- ✅ Formulario de contacto funcional

### Panel de Staff
- ✅ Dashboard con estadísticas
- ✅ Gestión completa de Facetas (CRUD)
- ✅ Gestión completa de Hitos (CRUD)
- ✅ Gestión de Mensajes de Contacto
- ✅ Interfaz moderna y fácil de usar

## 🐛 Solución de Problemas

### Error de conexión a MySQL
- Verifica que MySQL esté corriendo
- Verifica las credenciales en `.env`
- Asegúrate de que la base de datos exista

### Error al ejecutar migraciones
- Verifica que la base de datos esté creada
- Verifica las credenciales en `.env`
- Asegúrate de tener permisos en MySQL

### No se ven los archivos estáticos
- Ejecuta: `python manage.py collectstatic`
- Verifica que `DEBUG=True` en `.env`

## 📝 Notas Importantes

- El proyecto está configurado para **desarrollo local**
- Los archivos multimedia se almacenan en `media/`
- Los archivos estáticos se recopilan en `staticfiles/`
- El archivo `.env` NO se sube a git (está en `.gitignore`)

## 🎯 Próximos Pasos

1. Accede al panel de staff: http://127.0.0.1:8000/staff/
2. Crea tu primera Faceta
3. Agrega Hitos a la faceta
4. Sube imágenes para las facetas y hitos
5. ¡Disfruta del scroll horizontal en el frontend!


