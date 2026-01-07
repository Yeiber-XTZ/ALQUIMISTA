# 🔧 Ejecutar Migraciones - ALQUIMISTA NELSON

## Estado Actual

✅ **Dependencias instaladas:**
- Django 4.2.27
- mysqlclient 2.2.7
- python-dotenv 1.2.1
- Pillow 11.3.0

✅ **Migraciones creadas:**
- Las migraciones ya están generadas en `core/migrations/0001_initial.py`

⚠️ **Pendiente:**
- Configurar contraseña de MySQL en `.env` (si es necesaria)
- Crear la base de datos MySQL
- Ejecutar las migraciones

## Pasos para Completar

### 1. Configurar Contraseña de MySQL (si es necesaria)

Si tu MySQL requiere contraseña, edita el archivo `.env` y agrega tu contraseña:

```env
DB_PASSWORD=tu_contraseña_aqui
```

Si tu MySQL NO tiene contraseña, deja `DB_PASSWORD=` vacío (como está ahora).

### 2. Crear la Base de Datos

Abre MySQL (Workbench, línea de comandos, o phpMyAdmin) y ejecuta:

```sql
CREATE DATABASE IF NOT EXISTS alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Ejecutar Migraciones

Ejecuta estos comandos en orden:

```bash
# Verificar configuración
python manage.py check

# Crear migraciones (si es necesario)
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

### 4. Script Automatizado

O ejecuta el script que creé:

```bash
python setup_db.py
```

Este script te pedirá la contraseña de MySQL interactivamente y ejecutará todos los pasos.

## Solución de Problemas

### Error: "Access denied for user 'root'@'localhost'"

**Solución:** Tu MySQL requiere contraseña. Edita `.env` y agrega:
```
DB_PASSWORD=tu_contraseña
```

### Error: "Unknown database 'alquimista_db'"

**Solución:** Crea la base de datos manualmente:
```sql
CREATE DATABASE alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Error: "Can't connect to MySQL server"

**Solución:** Verifica que MySQL esté corriendo:
- Windows: Servicios → MySQL
- O ejecuta: `net start MySQL` (como administrador)

## Comandos Rápidos

```bash
# Todo en uno (después de configurar .env)
python manage.py check && python manage.py makemigrations && python manage.py migrate
```


