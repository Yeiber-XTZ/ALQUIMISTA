# 🔐 Solución: Configurar Contraseña de MySQL

## El Problema

MySQL requiere contraseña pero no está configurada en el archivo `.env`.

## ✅ Solución Rápida

### Paso 1: Agregar Contraseña al archivo .env

1. **Abre el archivo `.env`** en la carpeta del proyecto (`E:\dev\ALQUIMISTA\.env`)

2. **Busca esta línea:**
   ```env
   DB_PASSWORD=
   ```

3. **Agrega tu contraseña de MySQL:**
   ```env
   DB_PASSWORD=tu_contraseña_aqui
   ```
   
   **Ejemplo:**
   ```env
   DB_PASSWORD=MiPassword123
   ```

4. **Guarda el archivo** (Ctrl + S)

### Paso 2: Crear la Base de Datos

Ahora ejecuta:

```powershell
python crear_bd_python.py
```

Este script leerá la contraseña del archivo `.env` y creará la base de datos automáticamente.

---

## 🔍 Si No Recuerdas la Contraseña

### Opción A: Restablecer Contraseña de MySQL

1. Abre MySQL Workbench
2. Ve a: **Server** → **Users and Privileges**
3. Selecciona el usuario `root`
4. Haz clic en **"Change Password"**
5. Ingresa una nueva contraseña
6. Guarda los cambios

### Opción B: Crear Nuevo Usuario

1. Abre MySQL Workbench
2. Ve a: **Server** → **Users and Privileges**
3. Haz clic en **"Add Account"**
4. Configura:
   - **Login Name:** `alquimista_user`
   - **Password:** (elige una contraseña)
   - **Administrative Roles:** Marca "DBA"
5. Guarda
6. Actualiza `.env`:
   ```env
   DB_USER=alquimista_user
   DB_PASSWORD=tu_nueva_contraseña
   ```

---

## 🚀 Método Alternativo: Crear Base de Datos Manualmente

Si prefieres no usar scripts, crea la base de datos manualmente:

### Usando MySQL Workbench:

1. Abre MySQL Workbench
2. Conéctate a tu servidor
3. Presiona `Ctrl + T` para nueva query
4. Ejecuta:
   ```sql
   CREATE DATABASE alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
5. Verifica en el panel izquierdo (SCHEMAS → Refresh All)

### Usando Línea de Comandos:

```powershell
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

Luego ingresa tu contraseña cuando te la pida, y ejecuta el SQL.

---

## ✅ Después de Configurar

Una vez que:
- ✅ La contraseña esté en `.env`
- ✅ La base de datos esté creada

Ejecuta las migraciones:

```powershell
python manage.py migrate
```

---

## 📝 Resumen de Pasos

1. **Edita `.env`** y agrega `DB_PASSWORD=tu_contraseña`
2. **Guarda el archivo**
3. **Ejecuta:** `python crear_bd_python.py`
4. **Ejecuta:** `python manage.py migrate`

¡Listo! 🎉


