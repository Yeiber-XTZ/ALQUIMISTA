"""
Script Python para crear la base de datos MySQL
Este método es más confiable porque usa mysqlclient directamente
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def crear_base_datos():
    """Crea la base de datos usando mysqlclient."""
    try:
        import MySQLdb
        
        host = os.getenv('DB_HOST', 'localhost')
        port = int(os.getenv('DB_PORT', '3306'))
        user = os.getenv('DB_USER', 'root')
        password = os.getenv('DB_PASSWORD', '')
        db_name = os.getenv('DB_NAME', 'alquimista_db')
        
        print("="*60)
        print("Creando base de datos MySQL...")
        print("="*60)
        print(f"Host: {host}")
        print(f"Puerto: {port}")
        print(f"Usuario: {user}")
        print(f"Base de datos: {db_name}")
        print("="*60)
        
        # Si no hay contraseña en .env, pedirla
        if not password:
            print("\n[INFO] No se encontro DB_PASSWORD en .env")
            password = input("Ingresa la contrasena de MySQL (o Enter si no tiene): ")
        
        # Conectar a MySQL (sin especificar base de datos)
        try:
            connection = MySQLdb.connect(
                host=host,
                port=port,
                user=user,
                passwd=password
            )
        except MySQLdb.Error as e:
            if "Access denied" in str(e):
                print(f"\n[ERROR] Acceso denegado. Verifica la contrasena.")
                print("        Si tu MySQL tiene contrasena, agregala al archivo .env:")
                print("        DB_PASSWORD=tu_contrasena")
                return False
            else:
                print(f"\n[ERROR] Error de conexion: {e}")
                return False
        
        cursor = connection.cursor()
        
        # Crear base de datos
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"\n[OK] Base de datos '{db_name}' creada exitosamente!")
            print(f"     O ya existia previamente.")
            
            # Verificar
            cursor.execute("SHOW DATABASES LIKE %s", (db_name,))
            result = cursor.fetchone()
            if result:
                print(f"[OK] Base de datos verificada: {result[0]}")
            
        except MySQLdb.Error as e:
            print(f"\n[ERROR] No se pudo crear la base de datos: {e}")
            return False
        
        cursor.close()
        connection.close()
        
        print("\n" + "="*60)
        print("[OK] Base de datos lista!")
        print("="*60)
        print("\nSiguiente paso: Ejecuta las migraciones:")
        print("  python manage.py migrate\n")
        
        return True
        
    except ImportError:
        print("[ERROR] mysqlclient no esta disponible.")
        print("        Instala con: pip install mysqlclient")
        return False
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}")
        return False

if __name__ == '__main__':
    crear_base_datos()


