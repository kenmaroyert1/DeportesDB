import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

def probar_conexion():
    """Prueba la conexión a la base de datos MySQL"""
    try:
        # Verificar la existencia del archivo .env
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        print(f"\nBuscando archivo .env en: {env_path}")
        if os.path.exists(env_path):
            print("Archivo .env encontrado")
            # Cargar variables de entorno desde la ubicación específica
            load_dotenv(env_path)
        else:
            print("¡ADVERTENCIA! Archivo .env no encontrado")
        
        # Imprimir información de diagnóstico
        print("\nVariables de entorno cargadas:")
        print(f"DBHOST: {os.getenv('DBHOST', 'no definido')}")
        print(f"DBPORT: {os.getenv('DBPORT', 'no definido')}")
        print(f"DBUSER: {os.getenv('DBUSER', 'no definido')}")
        print(f"DBDATABASE_NAME: {os.getenv('DBDATABASE_NAME', 'no definido')}")
        
        # Intentar establecer la conexión
        print("Intentando conectar a la base de datos...")
        connection = mysql.connector.connect(
            host=os.getenv('DBHOST', 'localhost'),
            user=os.getenv('DBUSER', 'root'),
            password=os.getenv('DBPASSWORD', ''),
            port=int(os.getenv('DBPORT', '3306')),
            database=os.getenv('DBDATABASE_NAME', 'railway'),
            connect_timeout=60,
            autocommit=True,
            buffered=True
        )
        
        if connection.is_connected():
            print("¡Conexión exitosa!")
            
            # Obtener información del servidor
            db_info = connection.server_info
            print(f"Información del servidor MySQL: {db_info}")
            
            # Crear un cursor y ejecutar una consulta simple
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("Consulta de prueba ejecutada correctamente")
            
            cursor.close()
            connection.close()
            print("Conexión cerrada correctamente")
            return True
            
    except Error as e:
        print(f"Error al conectar a la base de datos: {str(e)}")
        return False

if __name__ == "__main__":
    probar_conexion()