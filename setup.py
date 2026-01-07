"""
Script de inicialización para el proyecto ALQUIMISTA NELSON
Ejecuta: python setup.py
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado."""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        return False

def main():
    print("\n" + "="*60)
    print("🏀 ALQUIMISTA NELSON - Script de Inicialización")
    print("="*60)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('manage.py'):
        print("❌ Error: No se encontró manage.py. Asegúrate de estar en el directorio raíz del proyecto.")
        sys.exit(1)
    
    # Verificar que existe .env
    if not os.path.exists('.env'):
        print("⚠️  Advertencia: No se encontró el archivo .env")
        print("   Se creará uno con valores por defecto.")
        # El .env ya debería estar creado, pero por si acaso...
    
    steps = [
        ("python manage.py check", "Verificando configuración de Django"),
        ("python manage.py makemigrations", "Creando migraciones"),
        ("python manage.py migrate", "Aplicando migraciones a la base de datos"),
    ]
    
    print("\n✅ Pasos a ejecutar:")
    for i, (cmd, desc) in enumerate(steps, 1):
        print(f"   {i}. {desc}")
    
    response = input("\n¿Deseas continuar? (s/n): ").lower()
    if response != 's':
        print("❌ Operación cancelada.")
        sys.exit(0)
    
    # Ejecutar pasos
    for cmd, desc in steps:
        if not run_command(cmd, desc):
            print(f"\n❌ Falló: {desc}")
            print("   Por favor, verifica los errores arriba y corrige la configuración.")
            sys.exit(1)
    
    print("\n" + "="*60)
    print("✅ ¡Inicialización completada!")
    print("="*60)
    print("\n📝 Próximos pasos:")
    print("   1. Crea un superusuario: python manage.py createsuperuser")
    print("      (Asegúrate de marcar is_staff=True)")
    print("   2. Inicia el servidor: python manage.py runserver")
    print("   3. Accede a:")
    print("      - Frontend público: http://127.0.0.1:8000/")
    print("      - Panel de staff: http://127.0.0.1:8000/staff/")
    print("\n💡 Nota: Asegúrate de que MySQL esté corriendo y la base de datos 'alquimista_db' esté creada.")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()

