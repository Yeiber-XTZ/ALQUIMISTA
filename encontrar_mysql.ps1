# Script para encontrar la ruta de MySQL en Windows
Write-Host "`n=== Buscando instalacion de MySQL ===" -ForegroundColor Cyan

# Rutas comunes donde MySQL se instala
$rutasComunes = @(
    "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
    "C:\Program Files\MySQL\MySQL Server 8.1\bin\mysql.exe",
    "C:\Program Files\MySQL\MySQL Server 8.2\bin\mysql.exe",
    "C:\Program Files\MySQL\MySQL Server 8.3\bin\mysql.exe",
    "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe",
    "C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysql.exe",
    "C:\Program Files (x86)\MySQL\MySQL Server 5.7\bin\mysql.exe",
    "C:\xampp\mysql\bin\mysql.exe",
    "C:\wamp64\bin\mysql\mysql8.0.xx\bin\mysql.exe",
    "C:\wamp\bin\mysql\mysql8.0.xx\bin\mysql.exe"
)

$mysqlEncontrado = $null

# Buscar en rutas comunes
foreach ($ruta in $rutasComunes) {
    if (Test-Path $ruta) {
        $mysqlEncontrado = $ruta
        Write-Host "[OK] MySQL encontrado en: $ruta" -ForegroundColor Green
        break
    }
}

# Si no se encuentra en rutas comunes, buscar en Program Files
if (-not $mysqlEncontrado) {
    Write-Host "`nBuscando en Program Files..." -ForegroundColor Yellow
    
    $programFiles = @(
        "C:\Program Files\MySQL",
        "C:\Program Files (x86)\MySQL"
    )
    
    foreach ($basePath in $programFiles) {
        if (Test-Path $basePath) {
            $mysqlDirs = Get-ChildItem -Path $basePath -Directory -ErrorAction SilentlyContinue
            foreach ($dir in $mysqlDirs) {
                $mysqlPath = Join-Path $dir.FullName "bin\mysql.exe"
                if (Test-Path $mysqlPath) {
                    $mysqlEncontrado = $mysqlPath
                    Write-Host "[OK] MySQL encontrado en: $mysqlPath" -ForegroundColor Green
                    break
                }
            }
            if ($mysqlEncontrado) { break }
        }
    }
}

# Buscar en servicios de Windows
if (-not $mysqlEncontrado) {
    Write-Host "`nBuscando servicio MySQL..." -ForegroundColor Yellow
    $servicios = Get-Service | Where-Object {$_.Name -like "*MySQL*"}
    if ($servicios) {
        Write-Host "[INFO] Servicio MySQL encontrado:" -ForegroundColor Cyan
        foreach ($servicio in $servicios) {
            Write-Host "  - $($servicio.Name) (Estado: $($servicio.Status))" -ForegroundColor White
        }
        Write-Host "`n[INFO] MySQL esta instalado pero no se encontro la ruta del ejecutable." -ForegroundColor Yellow
        Write-Host "       Busca manualmente en: C:\Program Files\MySQL\" -ForegroundColor Yellow
    }
}

# Resultado final
if ($mysqlEncontrado) {
    Write-Host "`n=== RESULTADO ===" -ForegroundColor Green
    Write-Host "Ruta completa: $mysqlEncontrado" -ForegroundColor White
    Write-Host "`nPara usar MySQL, ejecuta:" -ForegroundColor Cyan
    Write-Host "  `"$mysqlEncontrado`" -u root -p" -ForegroundColor Yellow
    
    # Crear un alias temporal
    $rutaBin = Split-Path $mysqlEncontrado -Parent
    Write-Host "`nO agrega esta ruta al PATH:" -ForegroundColor Cyan
    Write-Host "  $rutaBin" -ForegroundColor White
    
    # Guardar la ruta en un archivo
    $rutaBin | Out-File -FilePath "mysql_path.txt" -Encoding utf8
    Write-Host "`n[OK] Ruta guardada en: mysql_path.txt" -ForegroundColor Green
} else {
    Write-Host "`n[ERROR] No se encontro MySQL en las ubicaciones comunes." -ForegroundColor Red
    Write-Host "`nPosibles soluciones:" -ForegroundColor Yellow
    Write-Host "  1. Instala MySQL desde: https://dev.mysql.com/downloads/installer/" -ForegroundColor White
    Write-Host "  2. O usa MySQL Workbench (mas facil)" -ForegroundColor White
    Write-Host "  3. O usa XAMPP/WAMP que incluye MySQL" -ForegroundColor White
    Write-Host "  4. Busca manualmente en: C:\Program Files\MySQL\" -ForegroundColor White
}

Write-Host "`n"

