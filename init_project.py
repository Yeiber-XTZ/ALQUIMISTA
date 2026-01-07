"""
Script completo de inicialización del proyecto ALQUIMISTA
Ejecuta: python init_project.py
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado."""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr and "warning" not in result.stderr.lower():
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr if e.stderr else e}")
        return False

def main():
    print("\n" + "="*60)
    print("🏀 ALQUIMISTA NELSON - Inicialización Completa")
    print("="*60)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('manage.py'):
        print("❌ Error: No se encontró manage.py. Asegúrate de estar en el directorio raíz del proyecto.")
        sys.exit(1)
    
    steps = [
        ("python manage.py check", "Verificando configuración de Django"),
        ("python manage.py makemigrations", "Creando migraciones"),
        ("python manage.py migrate", "Aplicando migraciones a la base de datos"),
    ]
    
    print("\n✅ Pasos a ejecutar:")
    for i, (cmd, desc) in enumerate(steps, 1):
        print(f"   {i}. {desc}")
    
    print("\n⏳ Ejecutando...\n")
    
    # Ejecutar pasos
    for cmd, desc in steps:
        if not run_command(cmd, desc):
            print(f"\n❌ Falló: {desc}")
            print("\n💡 Posibles soluciones:")
            print("   1. Verifica que MySQL esté corriendo")
            print("   2. Verifica las credenciales en .env")
            print("   3. Crea la base de datos manualmente:")
            print("      CREATE DATABASE alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            sys.exit(1)
    
    print("\n" + "="*60)
    print("✅ ¡Inicialización completada exitosamente!")
    print("="*60)
    print("\n📝 Próximos pasos:")
    print("   1. Crea un superusuario: python manage.py createsuperuser")
    print("      (Asegúrate de marcar is_staff=True)")
    print("   2. Inicia el servidor: python manage.py runserver")
    print("   3. Accede a:")
    print("      - Frontend público: http://127.0.0.1:8000/")
    print("      - Panel de staff: http://127.0.0.1:8000/staff/")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()

