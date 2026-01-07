# Script de inicialización para ALQUIMISTA NELSON
# Ejecuta: .\init.ps1

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "🏀 ALQUIMISTA NELSON - Inicialización Completa" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "manage.py")) {
    Write-Host "❌ Error: No se encontró manage.py. Asegúrate de estar en el directorio raíz del proyecto." -ForegroundColor Red
    exit 1
}

# Paso 1: Verificar configuración
Write-Host "📋 Verificando configuración de Django..." -ForegroundColor Yellow
python manage.py check
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Error en la verificación. Revisa la configuración." -ForegroundColor Red
    exit 1
}

# Paso 2: Crear migraciones
Write-Host "`n📋 Creando migraciones..." -ForegroundColor Yellow
python manage.py makemigrations
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Error al crear migraciones." -ForegroundColor Red
    exit 1
}

# Paso 3: Aplicar migraciones
Write-Host "`n📋 Aplicando migraciones a la base de datos..." -ForegroundColor Yellow
python manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Error al aplicar migraciones." -ForegroundColor Red
    Write-Host "`n💡 Posibles soluciones:" -ForegroundColor Yellow
    Write-Host "   1. Verifica que MySQL esté corriendo" -ForegroundColor White
    Write-Host "   2. Verifica las credenciales en .env" -ForegroundColor White
    Write-Host "   3. Crea la base de datos manualmente:" -ForegroundColor White
    Write-Host "      CREATE DATABASE alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`n" -ForegroundColor White
    exit 1
}

Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "✅ ¡Inicialización completada exitosamente!" -ForegroundColor Green
Write-Host "============================================================`n" -ForegroundColor Green

Write-Host "📝 Próximos pasos:" -ForegroundColor Cyan
Write-Host "   1. Crea un superusuario: python manage.py createsuperuser" -ForegroundColor White
Write-Host "      (Asegúrate de marcar is_staff=True)" -ForegroundColor Gray
Write-Host "   2. Inicia el servidor: python manage.py runserver" -ForegroundColor White
Write-Host "   3. Accede a:" -ForegroundColor White
Write-Host "      - Frontend público: http://127.0.0.1:8000/" -ForegroundColor Gray
Write-Host "      - Panel de staff: http://127.0.0.1:8000/staff/`n" -ForegroundColor Gray


