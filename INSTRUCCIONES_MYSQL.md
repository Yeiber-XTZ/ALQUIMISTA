# 🎯 Instrucciones para Usar MySQL desde PowerShell

## ✅ MySQL Encontrado

Tu MySQL está instalado en:
```
C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe
```

---

## 🚀 Opción 1: Usar el Script Automático (MÁS FÁCIL)

He creado un script que creará la base de datos automáticamente:

```powershell
.\crear_bd_automatico.ps1
```

Este script:
- Te pedirá la contraseña de MySQL
- Creará la base de datos automáticamente
- Te dirá si funcionó o si hay algún error

---

## 🚀 Opción 2: Usar la Ruta Completa Manualmente

Ejecuta este comando en PowerShell:

```powershell
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

**Pasos:**
1. Copia y pega el comando arriba
2. Presiona Enter
3. Te pedirá la contraseña:
   - Si tu MySQL tiene contraseña: escríbela y presiona Enter
   - Si NO tiene contraseña: simplemente presiona Enter
4. Verás el prompt `mysql>`
5. Ejecuta este comando:
   ```sql
   CREATE DATABASE alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
6. Presiona Enter
7. Verifica que se creó:
   ```sql
   SHOW DATABASES;
   ```
8. Deberías ver `alquimista_db` en la lista
9. Sal:
   ```sql
   exit;
   ```

---

## 🚀 Opción 3: Agregar MySQL al PATH (Para Usar `mysql` Directamente)

Si quieres poder usar `mysql` directamente sin la ruta completa:

### Paso 1: Agregar al PATH del Usuario (Recomendado)

1. Presiona `Windows + R`
2. Escribe: `sysdm.cpl` y presiona Enter
3. Ve a la pestaña "Opciones avanzadas"
4. Haz clic en "Variables de entorno"
5. En "Variables de usuario", busca "Path" y haz clic en "Editar"
6. Haz clic en "Nuevo"
7. Pega esta ruta:
   ```
   C:\Program Files\MySQL\MySQL Server 8.0\bin
   ```
8. Haz clic en "Aceptar" en todas las ventanas
9. **Cierra y vuelve a abrir PowerShell** para que tome efecto

### Paso 2: Verificar

Abre una nueva PowerShell y ejecuta:

```powershell
mysql --version
```

Si muestra la versión, ya funciona. Ahora puedes usar:

```powershell
mysql -u root -p
```

---

## 🚀 Opción 4: Usar MySQL Workbench (MÁS FÁCIL - Sin Línea de Comandos)

Si prefieres no usar la línea de comandos:

1. **Abre MySQL Workbench** (búscalo en el menú de inicio)
2. **Conéctate** a tu servidor (doble clic en la conexión)
3. **Presiona `Ctrl + T`** para abrir una nueva query
4. **Copia y pega esto:**
   ```sql
   CREATE DATABASE alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
5. **Presiona `Ctrl + Enter`** para ejecutar
6. **Verifica:** En el panel izquierdo, haz clic derecho en "SCHEMAS" → "Refresh All"
7. Deberías ver `alquimista_db` en la lista

---

## 📝 Después de Crear la Base de Datos

Una vez que la base de datos esté creada:

### 1. Configurar .env (si es necesario)

Abre el archivo `.env` y verifica/edita:

```env
DB_PASSWORD=tu_contraseña_aqui
```

(Si tu MySQL no tiene contraseña, déjala vacía: `DB_PASSWORD=`)

### 2. Ejecutar Migraciones

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
  ...
  Applying core.0001_initial... OK
```

Si ves "OK" en todas las líneas, ¡todo está funcionando!

---

## 🆘 Solución de Problemas

### "Access denied for user 'root'@'localhost'"

**Solución:**
1. Abre el archivo `.env`
2. Agrega tu contraseña:
   ```env
   DB_PASSWORD=tu_contraseña_real
   ```
3. Guarda el archivo
4. Intenta de nuevo

### "Can't connect to MySQL server"

**Solución:**
1. Verifica que MySQL esté corriendo:
   - Presiona `Windows + R`
   - Escribe: `services.msc`
   - Busca "MySQL80" o "MySQL"
   - Si está detenido, haz clic derecho → "Iniciar"

### El script no funciona

**Solución:**
- Usa MySQL Workbench (Opción 4) - es más fácil y visual
- O usa la ruta completa manualmente (Opción 2)

---

## ✅ Resumen Rápido

**Método más fácil:**
```powershell
.\crear_bd_automatico.ps1
```

**O usa MySQL Workbench** (sin línea de comandos)

**Después:**
```powershell
python manage.py migrate
```

¡Listo! 🎉


