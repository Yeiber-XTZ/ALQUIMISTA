"""
Script para crear la base de datos MySQL automáticamente
Ejecuta: python crear_base_datos.py
"""
import os
from dotenv import load_dotenv

load_dotenv()

def crear_base_datos():
    """Intenta crear la base de datos usando mysqlclient."""
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
        
        # Conectar a MySQL (sin especificar base de datos)
        connection = MySQLdb.connect(
            host=host,
            port=port,
            user=user,
            passwd=password
        )
        
        cursor = connection.cursor()
        
        # Crear base de datos
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"\n[OK] Base de datos '{db_name}' creada exitosamente!")
            print(f"     O ya existia previamente.")
        except MySQLdb.Error as e:
            print(f"\n[ERROR] No se pudo crear la base de datos: {e}")
            print("\nIntenta crearla manualmente usando uno de los metodos siguientes.")
            return False
        
        cursor.close()
        connection.close()
        
        return True
        
    except ImportError:
        print("[ERROR] mysqlclient no esta disponible.")
        print("        Usa uno de los metodos manuales siguientes.")
        return False
    except MySQLdb.Error as e:
        print(f"\n[ERROR] Error de conexion a MySQL: {e}")
        print("\nPosibles causas:")
        print("  1. MySQL no esta corriendo")
        print("  2. Credenciales incorrectas en .env")
        print("  3. Usuario no tiene permisos para crear bases de datos")
        print("\nIntenta crearla manualmente usando uno de los metodos siguientes.")
        return False
    except Exception as e:
        print(f"\n[ERROR] Error inesperado: {e}")
        return False

def mostrar_instrucciones_manuales():
    """Muestra instrucciones para crear la base de datos manualmente."""
    db_name = os.getenv('DB_NAME', 'alquimista_db')
    
    print("\n" + "="*60)
    print("METODOS MANUALES PARA CREAR LA BASE DE DATOS")
    print("="*60)
    
    print("\n1. DESDE LA LINEA DE COMANDOS DE MYSQL:")
    print("-" * 60)
    print("Abre una terminal y ejecuta:")
    print("  mysql -u root -p")
    print("\nLuego ejecuta:")
    print(f"  CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print("  exit;")
    
    print("\n2. DESDE MYSQL WORKBENCH:")
    print("-" * 60)
    print("1. Abre MySQL Workbench")
    print("2. Conectate a tu servidor MySQL")
    print("3. En la pestaña 'Query', escribe:")
    print(f"   CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print("4. Ejecuta la consulta (Ctrl+Enter)")
    
    print("\n3. DESDE PHPMYADMIN:")
    print("-" * 60)
    print("1. Abre phpMyAdmin en tu navegador")
    print("2. Ve a la pestaña 'Bases de datos'")
    print(f"3. Escribe '{db_name}' en 'Crear base de datos'")
    print("4. Selecciona 'utf8mb4_unicode_ci' como intercalacion")
    print("5. Click en 'Crear'")
    
    print("\n4. DESDE XAMPP/WAMP:")
    print("-" * 60)
    print("1. Abre phpMyAdmin (http://localhost/phpmyadmin)")
    print("2. Ve a la pestaña 'Bases de datos'")
    print(f"3. Escribe '{db_name}' en 'Crear base de datos'")
    print("4. Selecciona 'utf8mb4_unicode_ci' como intercalacion")
    print("5. Click en 'Crear'")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    if crear_base_datos():
        print("\n[OK] Base de datos lista. Ahora puedes ejecutar:")
        print("     python manage.py migrate")
    else:
        mostrar_instrucciones_manuales()

