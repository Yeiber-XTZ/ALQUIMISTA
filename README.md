# 🏀 ALQUIMISTA NELSON

Sitio web dinámico con experiencia de scroll horizontal tipo galería, inspirado en lebronjames.com.

## 🚀 Configuración Inicial

### Requisitos Previos

- Python 3.10+
- MySQL (servidor local)
- pip (gestor de paquetes de Python)

### Pasos de Instalación Rápida

1. **Crear base de datos MySQL:**
   ```sql
   CREATE DATABASE alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **El archivo `.env` ya está creado** con valores por defecto. Si necesitas modificarlo, edita `.env` con tus credenciales de MySQL.

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar migraciones:**
   ```bash
   python manage.py migrate
   ```

5. **Crear superusuario (para el panel de staff):**
   ```bash
   python manage.py createsuperuser
   ```
   **Importante:** Asegúrate de marcar `is_staff=True` cuando se te solicite.

6. **Ejecutar servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

7. **Acceder al sitio:**
   - Frontend público: http://127.0.0.1:8000/
   - Panel de staff: http://127.0.0.1:8000/staff/
   - Django Admin: http://127.0.0.1:8000/admin/

## 📁 Estructura del Proyecto

```
ALQUIMISTA/
├── alquimista_project/     # Configuración del proyecto Django
│   ├── settings.py         # Configuración principal
│   ├── urls.py            # URLs principales
│   └── ...
├── core/                   # App principal
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Vistas
│   ├── urls.py            # URLs de la app
│   └── ...
├── templates/             # Templates HTML
├── static/                # Archivos estáticos (CSS, JS, imágenes)
├── media/                 # Archivos multimedia subidos por usuarios
├── requirements.txt       # Dependencias Python
└── .env                   # Variables de entorno (no se sube a git)
```

## 🎨 Paleta de Colores

- **Primario:** Rojo `#B8212A`
- **Secundario:** Negro `#000000`
- **Acento/Texto:** Blanco `#FFFFFF`

## 📝 Notas

- El proyecto está configurado para desarrollo local
- Los archivos multimedia se almacenan en la carpeta `media/`
- Los archivos estáticos se recopilan en `staticfiles/` con `python manage.py collectstatic`

