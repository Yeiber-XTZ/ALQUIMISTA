# 📚 GUÍA COMPLETA: Crear Base de Datos MySQL para ALQUIMISTA NELSON

## 📋 Índice
1. [Verificar que MySQL esté corriendo](#1-verificar-que-mysql-esté-corriendo)
2. [Método 1: MySQL Workbench (GUI - Más Fácil)](#método-1-mysql-workbench-gui---más-fácil)
3. [Método 2: Línea de Comandos (Terminal)](#método-2-línea-de-comandos-terminal)
4. [Método 3: phpMyAdmin (XAMPP/WAMP)](#método-3-phpmyadmin-xamppwamp)
5. [Método 4: HeidiSQL (Alternativa)](#método-4-heidisql-alternativa)
6. [Configurar el archivo .env](#configurar-el-archivo-env)
7. [Verificar que todo funciona](#verificar-que-todo-funciona)
8. [Solución de Problemas](#solución-de-problemas)

---

## 1. Verificar que MySQL esté corriendo

### En Windows:

**Opción A: Desde el Administrador de Tareas**
1. Presiona `Ctrl + Shift + Esc` para abrir el Administrador de Tareas
2. Ve a la pestaña "Servicios"
3. Busca "MySQL" o "MySQL80" o "MySQL57"
4. Verifica que el estado sea "En ejecución"
5. Si no está corriendo, haz clic derecho → "Iniciar"

**Opción B: Desde Servicios**
1. Presiona `Windows + R`
2. Escribe: `services.msc` y presiona Enter
3. Busca "MySQL" en la lista
4. Verifica que el estado sea "En ejecución"
5. Si no está, haz clic derecho → "Iniciar"

**Opción C: Desde PowerShell (como Administrador)**
```powershell
# Ver estado de MySQL
Get-Service | Where-Object {$_.Name -like "*MySQL*"}

# Iniciar MySQL (si está detenido)
Start-Service MySQL80
# O el nombre que corresponda: MySQL57, MySQL, etc.
```

---

## Método 1: MySQL Workbench (GUI - Más Fácil)

### Paso 1: Abrir MySQL Workbench

1. **Busca MySQL Workbench** en el menú de inicio de Windows
2. **Haz clic** para abrirlo
3. Si no lo tienes instalado:
   - Descárgalo de: https://dev.mysql.com/downloads/workbench/
   - O instálalo desde el instalador de MySQL

### Paso 2: Conectarte al Servidor

1. En la pantalla principal de MySQL Workbench, verás una lista de conexiones
2. **Busca una conexión** que diga algo como:
   - "Local instance MySQL80"
   - "localhost"
   - O cualquier conexión que hayas creado antes
3. **Haz doble clic** en la conexión
   - O haz clic derecho → "Open Connection"
4. Si te pide contraseña:
   - Ingresa la contraseña de tu usuario `root`
   - Si no tienes contraseña, déjala vacía y presiona OK
   - Si no recuerdas la contraseña, ve a la sección de "Solución de Problemas"

### Paso 3: Abrir una Nueva Query

1. Una vez conectado, verás la interfaz principal
2. En la barra de herramientas superior, busca el botón **"SQL"** o **"Query"**
3. O simplemente presiona `Ctrl + T` para abrir una nueva pestaña de query
4. Verás un área de texto grande donde puedes escribir SQL

### Paso 4: Escribir el Comando SQL

En el área de texto, copia y pega exactamente esto:

```sql
CREATE DATABASE alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Explicación del comando:**
- `CREATE DATABASE` - Crea una nueva base de datos
- `alquimista_db` - Nombre de la base de datos (debe coincidir con DB_NAME en .env)
- `CHARACTER SET utf8mb4` - Usa UTF-8 completo (soporta emojis y caracteres especiales)
- `COLLATE utf8mb4_unicode_ci` - Reglas de comparación y ordenamiento

### Paso 5: Ejecutar el Comando

1. **Selecciona todo el texto** del comando (Ctrl + A)
2. **Presiona `Ctrl + Enter`** para ejecutar
   - O haz clic en el botón ⚡ "Execute" (rayo) en la barra de herramientas
   - O ve a Query → Execute (All or Selection)

### Paso 6: Verificar que se Creó

1. En el panel izquierdo, busca la sección **"SCHEMAS"**
2. Si no ves la base de datos nueva:
   - Haz clic derecho en "SCHEMAS"
   - Selecciona **"Refresh All"**
3. Deberías ver `alquimista_db` en la lista de bases de datos
4. Si aparece, ¡listo! La base de datos está creada

### Paso 7: Verificar Detalles (Opcional)

Para verificar que se creó correctamente, ejecuta:

```sql
SHOW DATABASES LIKE 'alquimista_db';
```

Deberías ver una fila con el nombre de la base de datos.

---

## Método 2: Línea de Comandos (Terminal)

### Paso 1: Abrir PowerShell o CMD

1. Presiona `Windows + X`
2. Selecciona **"Windows PowerShell"** o **"Terminal"**
3. O busca "PowerShell" o "CMD" en el menú de inicio

### Paso 2: Navegar a la Carpeta del Proyecto (Opcional)

Si quieres estar en la carpeta del proyecto:

```powershell
cd E:\dev\ALQUIMISTA
```

### Paso 3: Encontrar la Ruta de MySQL

**Opción A: Si MySQL está en el PATH**

Simplemente ejecuta:
```powershell
mysql --version
```

Si muestra la versión, MySQL está en el PATH y puedes continuar.

**Opción B: Si MySQL NO está en el PATH**

Necesitas encontrar la ruta de MySQL. Busca en estas ubicaciones comunes:

```
C:\Program Files\MySQL\MySQL Server 8.0\bin\
C:\Program Files\MySQL\MySQL Server 8.1\bin\
C:\Program Files\MySQL\MySQL Server 5.7\bin\
C:\xampp\mysql\bin\
C:\wamp64\bin\mysql\mysql8.0.xx\bin\
```

**Para encontrar la ruta exacta:**
1. Abre el Explorador de Archivos
2. Ve a `C:\Program Files\MySQL\`
3. Busca una carpeta que diga "MySQL Server X.X"
4. Entra a esa carpeta → `bin`
5. Copia la ruta completa

### Paso 4: Conectar a MySQL

**Si MySQL está en el PATH:**
```powershell
mysql -u root -p
```

**Si MySQL NO está en el PATH:**
```powershell
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```
(Reemplaza la ruta con la tuya)

**Explicación:**
- `-u root` - Usuario root
- `-p` - Te pedirá la contraseña

**Cuando te pida la contraseña:**
- Si tu MySQL tiene contraseña: escríbela y presiona Enter
- Si NO tiene contraseña: simplemente presiona Enter

### Paso 5: Verificar que Estás Conectado

Deberías ver algo como:

```
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is X
Server version: 8.0.xx MySQL Community Server

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

El prompt `mysql>` significa que estás conectado.

### Paso 6: Crear la Base de Datos

En el prompt `mysql>`, escribe (o copia y pega):

```sql
CREATE DATABASE alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**IMPORTANTE:** Debes terminar con punto y coma (`;`) y presionar Enter.

### Paso 7: Verificar que se Creó

Ejecuta:

```sql
SHOW DATABASES;
```

Deberías ver `alquimista_db` en la lista.

### Paso 8: Salir de MySQL

```sql
exit;
```

O simplemente presiona `Ctrl + C`

---

## Método 3: phpMyAdmin (XAMPP/WAMP)

### Paso 1: Iniciar XAMPP o WAMP

1. **Si usas XAMPP:**
   - Abre el Panel de Control de XAMPP
   - Haz clic en "Start" junto a "Apache"
   - Haz clic en "Start" junto a "MySQL"
   - Ambos deben ponerse en verde

2. **Si usas WAMP:**
   - Abre WAMP
   - Espera a que el icono se ponga verde
   - Si está naranja o rojo, haz clic derecho → "Start All Services"

### Paso 2: Abrir phpMyAdmin

1. Abre tu navegador web (Chrome, Firefox, Edge, etc.)
2. Ve a una de estas URLs:
   - **XAMPP:** http://localhost/phpmyadmin
   - **WAMP:** http://localhost/phpmyadmin
   - O http://127.0.0.1/phpmyadmin

3. Deberías ver la interfaz de phpMyAdmin

### Paso 3: Crear la Base de Datos

1. En el menú superior, haz clic en la pestaña **"Bases de datos"**
2. En la sección **"Crear base de datos"**:
   - **Nombre de la base de datos:** Escribe `alquimista_db`
   - **Intercalación:** Selecciona `utf8mb4_unicode_ci`
     - Si no ves esta opción, busca en el menú desplegable
     - O selecciona "utf8mb4" y luego busca "unicode_ci"
3. Haz clic en el botón **"Crear"**

### Paso 4: Verificar

1. En el panel izquierdo, deberías ver `alquimista_db` en la lista
2. Si no aparece, haz clic en "Actualizar" o presiona F5
3. Haz clic en `alquimista_db` para verificar que está vacía (sin tablas aún)

---

## Método 4: HeidiSQL (Alternativa)

### Paso 1: Descargar e Instalar HeidiSQL

1. Descarga desde: https://www.heidisql.com/download.php
2. Instala el programa
3. Ábrelo

### Paso 2: Crear una Nueva Sesión

1. En la pantalla de inicio, haz clic en **"Nuevo"**
2. Configura la conexión:
   - **Red:** Selecciona "MySQL (TCP/IP)"
   - **Hostname / IP:** `127.0.0.1` o `localhost`
   - **Usuario:** `root`
   - **Contraseña:** (la de tu MySQL, o déjala vacía)
   - **Puerto:** `3306`
3. Haz clic en **"Abrir"**

### Paso 3: Crear la Base de Datos

1. En el panel izquierdo, haz clic derecho en cualquier lugar
2. Selecciona **"Crear nuevo" → "Base de datos..."**
3. En el cuadro de diálogo:
   - **Nombre:** `alquimista_db`
   - **Intercalación:** `utf8mb4_unicode_ci`
4. Haz clic en **"OK"**

### Paso 4: Verificar

La base de datos debería aparecer en el panel izquierdo.

---

## Configurar el archivo .env

### Paso 1: Abrir el archivo .env

1. Ve a la carpeta del proyecto: `E:\dev\ALQUIMISTA`
2. Abre el archivo `.env` con cualquier editor de texto:
   - Bloc de notas
   - Notepad++
   - Visual Studio Code
   - Cualquier editor

### Paso 2: Verificar/Editar la Configuración

El archivo debería verse así:

```env
# Database Configuration (MySQL Local)
DB_NAME=alquimista_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306

# Django Secret Key
SECRET_KEY=)4v$a01g((&i36f@-b^@xf2tcka$lca5kl*7q3)v1kzxa&-t7+

# Debug Mode (set to False in production)
DEBUG=True
```

### Paso 3: Configurar la Contraseña (si es necesaria)

**Si tu MySQL tiene contraseña:**
- En la línea `DB_PASSWORD=`, escribe tu contraseña:
  ```env
  DB_PASSWORD=tu_contraseña_aqui
  ```

**Si tu MySQL NO tiene contraseña:**
- Déjala vacía (como está):
  ```env
  DB_PASSWORD=
  ```

### Paso 4: Guardar el Archivo

1. Presiona `Ctrl + S` para guardar
2. O File → Save

---

## Verificar que todo funciona

### Paso 1: Verificar la Conexión

Ejecuta en PowerShell (desde la carpeta del proyecto):

```powershell
python manage.py check
```

Deberías ver:
```
System check identified no issues (0 silenced).
```

Si hay errores, ve a la sección "Solución de Problemas".

### Paso 2: Ejecutar las Migraciones

```powershell
python manage.py migrate
```

Deberías ver algo como:

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, core, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
  Applying core.0001_initial... OK
```

Si ves "OK" al final de cada línea, ¡todo está funcionando!

### Paso 3: Verificar las Tablas Creadas

Puedes verificar en MySQL Workbench o phpMyAdmin que se crearon las tablas:

- `core_facet`
- `core_milestone`
- `core_contactmessage`
- Y otras tablas del sistema de Django

---

## Solución de Problemas

### Error: "Access denied for user 'root'@'localhost'"

**Causa:** MySQL requiere contraseña pero no está configurada en `.env`

**Solución:**
1. Abre el archivo `.env`
2. Agrega tu contraseña:
   ```env
   DB_PASSWORD=tu_contraseña_real
   ```
3. Guarda el archivo
4. Intenta de nuevo

**Si no recuerdas la contraseña:**
1. Abre MySQL Workbench
2. Ve a Server → Users and Privileges
3. Selecciona el usuario `root`
4. Haz clic en "Change Password"
5. O crea un nuevo usuario con permisos

### Error: "Unknown database 'alquimista_db'"

**Causa:** La base de datos no existe

**Solución:**
1. Sigue uno de los métodos arriba para crear la base de datos
2. Verifica que el nombre sea exactamente `alquimista_db` (sin espacios, mayúsculas/minúsculas)

### Error: "Can't connect to MySQL server"

**Causa:** MySQL no está corriendo

**Solución:**
1. Ve a Servicios de Windows (services.msc)
2. Busca MySQL
3. Si está detenido, inícialo
4. Si no aparece, MySQL no está instalado o el servicio no está configurado

### Error: "mysql: command not found"

**Causa:** MySQL no está en el PATH

**Solución:**
1. Encuentra la ruta de MySQL (normalmente en `C:\Program Files\MySQL\`)
2. Usa la ruta completa:
   ```powershell
   "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
   ```
3. O agrega MySQL al PATH del sistema

### Error al ejecutar migraciones: "Table already exists"

**Causa:** Las tablas ya existen (migraciones ejecutadas previamente)

**Solución:**
- Esto no es un error, significa que las migraciones ya se aplicaron
- Si quieres empezar de cero, elimina la base de datos y créala de nuevo

### La base de datos se crea pero las migraciones fallan

**Causa:** Permisos insuficientes o configuración incorrecta

**Solución:**
1. Verifica que el usuario `root` tenga todos los permisos
2. En MySQL Workbench: Server → Users and Privileges → root → Administrative Roles → marca "DBA"
3. Verifica que `DB_NAME` en `.env` coincida exactamente con el nombre de la base de datos

---

## Comandos Rápidos de Referencia

### Crear base de datos:
```sql
CREATE DATABASE alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Ver todas las bases de datos:
```sql
SHOW DATABASES;
```

### Verificar que existe:
```sql
SHOW DATABASES LIKE 'alquimista_db';
```

### Eliminar base de datos (si necesitas empezar de nuevo):
```sql
DROP DATABASE IF EXISTS alquimista_db;
```

### Ver tablas en la base de datos:
```sql
USE alquimista_db;
SHOW TABLES;
```

---

## Checklist Final

Antes de continuar, verifica que:

- [ ] MySQL está corriendo
- [ ] La base de datos `alquimista_db` existe
- [ ] El archivo `.env` está configurado correctamente
- [ ] `DB_PASSWORD` está configurado (si es necesaria)
- [ ] `python manage.py check` no muestra errores
- [ ] `python manage.py migrate` se ejecuta sin errores

---

## Siguiente Paso

Una vez que la base de datos esté creada y las migraciones ejecutadas:

1. **Crea un superusuario:**
   ```powershell
   python manage.py createsuperuser
   ```
   - Username: (elige uno)
   - Email: (opcional)
   - Password: (elige una contraseña segura)
   - **IMPORTANTE:** Cuando te pregunte "Is staff?", responde `yes` o `y`

2. **Inicia el servidor:**
   ```powershell
   python manage.py runserver
   ```

3. **Accede al sitio:**
   - Frontend: http://127.0.0.1:8000/
   - Panel Staff: http://127.0.0.1:8000/staff/

---

¡Listo! Si sigues estos pasos detalladamente, deberías poder crear la base de datos sin problemas. Si encuentras algún error específico, consulta la sección "Solución de Problemas" o compárteme el mensaje de error exacto.

