@echo off
REM Script de inicialización para ALQUIMISTA NELSON
REM Ejecuta: init.bat

echo.
echo ============================================================
echo 🏀 ALQUIMISTA NELSON - Inicialización Completa
echo ============================================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist manage.py (
    echo ❌ Error: No se encontró manage.py. Asegúrate de estar en el directorio raíz del proyecto.
    pause
    exit /b 1
)

REM Paso 1: Verificar configuración
echo 📋 Verificando configuración de Django...
python manage.py check
if errorlevel 1 (
    echo.
    echo ❌ Error en la verificación. Revisa la configuración.
    pause
    exit /b 1
)

REM Paso 2: Crear migraciones
echo.
echo 📋 Creando migraciones...
python manage.py makemigrations
if errorlevel 1 (
    echo.
    echo ❌ Error al crear migraciones.
    pause
    exit /b 1
)

REM Paso 3: Aplicar migraciones
echo.
echo 📋 Aplicando migraciones a la base de datos...
python manage.py migrate
if errorlevel 1 (
    echo.
    echo ❌ Error al aplicar migraciones.
    echo.
    echo 💡 Posibles soluciones:
    echo    1. Verifica que MySQL esté corriendo
    echo    2. Verifica las credenciales en .env
    echo    3. Crea la base de datos manualmente:
    echo       CREATE DATABASE alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ✅ ¡Inicialización completada exitosamente!
echo ============================================================
echo.
echo 📝 Próximos pasos:
echo    1. Crea un superusuario: python manage.py createsuperuser
echo       (Asegúrate de marcar is_staff=True)
echo    2. Inicia el servidor: python manage.py runserver
echo    3. Accede a:
echo       - Frontend público: http://127.0.0.1:8000/
echo       - Panel de staff: http://127.0.0.1:8000/staff/
echo.
pause


