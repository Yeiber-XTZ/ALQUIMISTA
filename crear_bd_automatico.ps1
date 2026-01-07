# Script para crear la base de datos MySQL automáticamente
$mysqlPath = "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"

Write-Host "`n=== Crear Base de Datos MySQL ===" -ForegroundColor Cyan
Write-Host "Ruta de MySQL: $mysqlPath`n" -ForegroundColor White

# Verificar que MySQL existe
if (-not (Test-Path $mysqlPath)) {
    Write-Host "[ERROR] No se encontro MySQL en: $mysqlPath" -ForegroundColor Red
    Write-Host "Ejecuta: .\encontrar_mysql.ps1 para encontrar la ruta correcta" -ForegroundColor Yellow
    exit 1
}

# Solicitar contraseña
Write-Host "[INFO] Se necesita la contraseña de MySQL (usuario root)" -ForegroundColor Yellow
Write-Host "       Si tu MySQL NO tiene contraseña, presiona Enter sin escribir nada`n" -ForegroundColor Gray

# Crear el comando SQL
$sqlCommand = "CREATE DATABASE IF NOT EXISTS alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Ejecutar MySQL
Write-Host "Ejecutando comando SQL..." -ForegroundColor Cyan
Write-Host "Comando: $sqlCommand`n" -ForegroundColor Gray

try {
    # Ejecutar MySQL con el comando SQL
    $result = & $mysqlPath -u root -p -e $sqlCommand 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Base de datos 'alquimista_db' creada exitosamente!" -ForegroundColor Green
        Write-Host "`nSiguiente paso: Ejecuta las migraciones:" -ForegroundColor Cyan
        Write-Host "  python manage.py migrate`n" -ForegroundColor Yellow
    } else {
        Write-Host "[ERROR] Error al crear la base de datos" -ForegroundColor Red
        Write-Host $result -ForegroundColor Red
        Write-Host "`nPosibles causas:" -ForegroundColor Yellow
        Write-Host "  - Contrasena incorrecta" -ForegroundColor White
        Write-Host "  - MySQL no esta corriendo" -ForegroundColor White
        Write-Host "  - Usuario no tiene permisos" -ForegroundColor White
    }
} catch {
    Write-Host "[ERROR] Error al ejecutar MySQL: $_" -ForegroundColor Red
    Write-Host "`nIntenta crear la base de datos manualmente usando MySQL Workbench" -ForegroundColor Yellow
}

Write-Host "`n"


