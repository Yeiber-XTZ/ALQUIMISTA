"""
Script para crear la base de datos MySQL
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Crea la base de datos si no existe."""
    try:
        # Conectar a MySQL sin especificar base de datos
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '3306')),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            db_name = os.getenv('DB_NAME', 'alquimista_db')
            
            # Crear base de datos
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ Base de datos '{db_name}' creada o ya existe.")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ Error al conectar a MySQL: {e}")
        print("\n💡 Intenta crear la base de datos manualmente:")
        print(f"   CREATE DATABASE {os.getenv('DB_NAME', 'alquimista_db')} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        return False
    except ImportError:
        print("❌ mysql-connector-python no está instalado.")
        print("💡 Intentando con mysqlclient...")
        return create_db_with_mysqlclient()

def create_db_with_mysqlclient():
    """Intenta crear la base de datos usando mysqlclient."""
    try:
        import MySQLdb
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        connection = MySQLdb.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '3306')),
            user=os.getenv('DB_USER', 'root'),
            passwd=os.getenv('DB_PASSWORD', '')
        )
        
        cursor = connection.cursor()
        db_name = os.getenv('DB_NAME', 'alquimista_db')
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ Base de datos '{db_name}' creada o ya existe.")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Por favor, crea la base de datos manualmente en MySQL:")
        print(f"   CREATE DATABASE {os.getenv('DB_NAME', 'alquimista_db')} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        return False

if __name__ == '__main__':
    print("🔧 Creando base de datos MySQL...")
    create_database()


