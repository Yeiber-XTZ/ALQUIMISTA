# Script para configurar la contraseña en .env
$envFile = ".env"

Write-Host "`n=== Configurar Contrasena de MySQL ===" -ForegroundColor Cyan

if (-not (Test-Path $envFile)) {
    Write-Host "[ERROR] No se encontro el archivo .env" -ForegroundColor Red
    exit 1
}

# Leer el archivo actual
$content = Get-Content $envFile

# Verificar si ya tiene contraseña
$tienePassword = $false
foreach ($line in $content) {
    if ($line -match "^DB_PASSWORD=(.+)$" -and $matches[1] -ne "") {
        $tienePassword = $true
        Write-Host "[INFO] Ya hay una contrasena configurada en .env" -ForegroundColor Yellow
        $respuesta = Read-Host "Deseas cambiarla? (s/n)"
        if ($respuesta -ne "s" -and $respuesta -ne "S") {
            Write-Host "[INFO] Contrasena no cambiada." -ForegroundColor Green
            exit 0
        }
        break
    }
}

# Solicitar contraseña
Write-Host "`n[INFO] Ingresa la contrasena de MySQL (usuario root)" -ForegroundColor Yellow
Write-Host "       Si tu MySQL NO tiene contrasena, presiona Enter sin escribir nada`n" -ForegroundColor Gray

$securePassword = Read-Host "Contrasena de MySQL" -AsSecureString
$password = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
)

# Actualizar el archivo
$newContent = @()
foreach ($line in $content) {
    if ($line -match "^DB_PASSWORD=") {
        $newContent += "DB_PASSWORD=$password"
    } else {
        $newContent += $line
    }
}

# Escribir el archivo
$newContent | Out-File -FilePath $envFile -Encoding utf8 -NoNewline

Write-Host "`n[OK] Archivo .env actualizado!" -ForegroundColor Green

if ($password) {
    Write-Host "[INFO] Contrasena configurada. Ahora puedes ejecutar:" -ForegroundColor Cyan
    Write-Host "  python crear_bd_python.py" -ForegroundColor Yellow
} else {
    Write-Host "[INFO] Sin contrasena configurada. Si MySQL requiere contrasena," -ForegroundColor Yellow
    Write-Host "       vuelve a ejecutar este script y agrega la contrasena." -ForegroundColor Yellow
}

Write-Host "`n"


