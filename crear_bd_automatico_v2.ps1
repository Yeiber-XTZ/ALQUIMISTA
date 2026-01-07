# Script mejorado para crear la base de datos MySQL
$mysqlPath = "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"

Write-Host "`n=== Crear Base de Datos MySQL ===" -ForegroundColor Cyan
Write-Host "Ruta de MySQL: $mysqlPath`n" -ForegroundColor White

# Verificar que MySQL existe
if (-not (Test-Path $mysqlPath)) {
    Write-Host "[ERROR] No se encontro MySQL en: $mysqlPath" -ForegroundColor Red
    exit 1
}

# Solicitar contraseña de forma segura
Write-Host "[INFO] Se necesita la contrasena de MySQL (usuario root)" -ForegroundColor Yellow
Write-Host "       Si tu MySQL NO tiene contrasena, presiona Enter sin escribir nada`n" -ForegroundColor Gray

$securePassword = Read-Host "Ingresa la contrasena de MySQL" -AsSecureString
$password = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
)

# Crear el comando SQL
$sqlCommand = "CREATE DATABASE IF NOT EXISTS alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Crear archivo temporal con el SQL
$tempSqlFile = Join-Path $env:TEMP "create_db_$(Get-Random).sql"
$sqlCommand | Out-File -FilePath $tempSqlFile -Encoding utf8 -NoNewline

Write-Host "`nEjecutando comando SQL..." -ForegroundColor Cyan

try {
    # Ejecutar MySQL con el archivo SQL
    if ($password) {
        # Con contraseña
        $result = & $mysqlPath -u root -p"$password" -e $sqlCommand 2>&1
    } else {
        # Sin contraseña
        $result = & $mysqlPath -u root -e $sqlCommand 2>&1
    }
    
    # Limpiar archivo temporal
    Remove-Item $tempSqlFile -ErrorAction SilentlyContinue
    
    if ($LASTEXITCODE -eq 0 -and -not ($result -match "ERROR")) {
        Write-Host "[OK] Base de datos 'alquimista_db' creada exitosamente!" -ForegroundColor Green
        Write-Host "`nSiguiente paso: Ejecuta las migraciones:" -ForegroundColor Cyan
        Write-Host "  python manage.py migrate`n" -ForegroundColor Yellow
    } else {
        Write-Host "[ERROR] Error al crear la base de datos" -ForegroundColor Red
        if ($result) {
            Write-Host $result -ForegroundColor Red
        }
        Write-Host "`nPosibles causas:" -ForegroundColor Yellow
        Write-Host "  - Contrasena incorrecta" -ForegroundColor White
        Write-Host "  - MySQL no esta corriendo" -ForegroundColor White
        Write-Host "  - Usuario no tiene permisos" -ForegroundColor White
        Write-Host "`nIntenta usar MySQL Workbench o el metodo manual.`n" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[ERROR] Error al ejecutar MySQL: $_" -ForegroundColor Red
    Write-Host "`nIntenta crear la base de datos manualmente usando MySQL Workbench" -ForegroundColor Yellow
}

Write-Host "`n"

