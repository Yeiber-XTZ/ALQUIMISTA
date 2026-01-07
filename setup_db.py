"""
Script interactivo para configurar la base de datos y ejecutar migraciones
"""
import os
import subprocess
import sys

def update_env_file(password):
    """Actualiza el archivo .env con la contraseña de MySQL."""
    env_file = '.env'
    
    # Leer el archivo .env
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Actualizar DB_PASSWORD
        updated_lines = []
        for line in lines:
            if line.startswith('DB_PASSWORD='):
                updated_lines.append(f'DB_PASSWORD={password}\n')
            else:
                updated_lines.append(line)
        
        # Escribir el archivo actualizado
        with open(env_file, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        
        print("[OK] Archivo .env actualizado con la contrasena de MySQL.")
        return True
    else:
        print("[ERROR] No se encontro el archivo .env")
        return False

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado."""
    print(f"\n📋 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {e.stderr if e.stderr else 'Error desconocido'}")
        return False

def main():
    import sys
    import io
    # Configurar stdout para UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("\n" + "="*60)
    print("ALQUIMISTA NELSON - Configuracion de Base de Datos")
    print("="*60)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('manage.py'):
        print("[ERROR] No se encontro manage.py.")
        sys.exit(1)
    
    # Solicitar contraseña de MySQL
    print("\n[INFO] MySQL requiere una contrasena para el usuario 'root'.")
    print("       Si tu MySQL no tiene contrasena, presiona Enter sin escribir nada.")
    password = input("       Ingresa la contrasena de MySQL (o Enter si no tiene): ")
    
    # Actualizar .env
    if not update_env_file(password):
        sys.exit(1)
    
    # Ejecutar comandos
    commands = [
        ("python manage.py check", "Verificando configuración"),
        ("python manage.py makemigrations", "Creando migraciones"),
        ("python manage.py migrate", "Aplicando migraciones"),
    ]
    
    print("\n[INFO] Ejecutando comandos...\n")
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            print(f"\n[ERROR] Fallo: {desc}")
            print("\n[INFO] Posibles soluciones:")
            print("   1. Verifica que MySQL este corriendo")
            print("   2. Verifica que la contrasena sea correcta")
            print("   3. Crea la base de datos manualmente:")
            print("      CREATE DATABASE alquimista_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            sys.exit(1)
    
    print("\n" + "="*60)
    print("[OK] Configuracion completada exitosamente!")
    print("="*60)
    print("\n📝 Próximos pasos:")
    print("   1. Crea un superusuario: python manage.py createsuperuser")
    print("   2. Inicia el servidor: python manage.py runserver")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()

