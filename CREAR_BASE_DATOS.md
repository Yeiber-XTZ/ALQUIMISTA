# 📊 Cómo Crear la Base de Datos MySQL

## 🎯 Opción 1: Desde MySQL Workbench (RECOMENDADO)

1. **Abre MySQL Workbench**
2. **Conéctate a tu servidor MySQL** (haz doble clic en la conexión)
3. **En la pestaña "Query"**, escribe este comando:

```sql
CREATE DATABASE alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

4. **Ejecuta la consulta:**
   - Presiona `Ctrl + Enter` (Windows)
   - O haz clic en el botón ⚡ "Execute"

5. **Verifica que se creó:**
   - En el panel izquierdo, haz clic derecho en "Schemas"
   - Selecciona "Refresh All"
   - Deberías ver `alquimista_db` en la lista

---

## 🎯 Opción 2: Desde la Línea de Comandos

### Windows (PowerShell o CMD):

```bash
# Conectar a MySQL (te pedirá la contraseña)
mysql -u root -p

# Una vez dentro de MySQL, ejecuta:
CREATE DATABASE alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Verificar que se creó:
SHOW DATABASES;

# Salir:
exit;
```

### Si MySQL no está en el PATH:

Busca la ruta de MySQL (normalmente en `C:\Program Files\MySQL\MySQL Server X.X\bin\`) y ejecuta:

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

---

## 🎯 Opción 3: Desde phpMyAdmin (XAMPP/WAMP)

1. **Abre phpMyAdmin** en tu navegador:
   - XAMPP: http://localhost/phpmyadmin
   - WAMP: http://localhost/phpmyadmin

2. **Ve a la pestaña "Bases de datos"** (arriba)

3. **En "Crear base de datos":**
   - Nombre: `alquimista_db`
   - Intercalación: `utf8mb4_unicode_ci`

4. **Haz clic en "Crear"**

---

## 🎯 Opción 4: Script Automático (si tienes la contraseña configurada)

Si ya configuraste `DB_PASSWORD` en tu archivo `.env`, ejecuta:

```bash
python crear_base_datos.py
```

---

## ⚠️ Importante: Configurar Contraseña en .env

**Si tu MySQL tiene contraseña**, edita el archivo `.env` y agrega:

```env
DB_PASSWORD=tu_contraseña_aqui
```

**Si tu MySQL NO tiene contraseña**, déjala vacía:

```env
DB_PASSWORD=
```

---

## ✅ Verificar que Funcionó

Después de crear la base de datos, ejecuta:

```bash
python manage.py migrate
```

Si todo está bien, verás algo como:

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, core, sessions
Running migrations:
  Applying core.0001_initial... OK
  ...
```

---

## 🆘 Problemas Comunes

### "Access denied for user 'root'@'localhost'"
- **Solución:** Tu MySQL requiere contraseña. Configúrala en `.env`

### "Unknown database 'alquimista_db'"
- **Solución:** La base de datos no existe. Créala usando uno de los métodos arriba.

### "Can't connect to MySQL server"
- **Solución:** Verifica que MySQL esté corriendo:
  - Windows: Panel de Control → Servicios → MySQL → Iniciar

---

## 📝 Comando SQL Completo

Si prefieres copiar y pegar todo de una vez:

```sql
CREATE DATABASE IF NOT EXISTS alquimista_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Verificar
SHOW DATABASES LIKE 'alquimista_db';
```


