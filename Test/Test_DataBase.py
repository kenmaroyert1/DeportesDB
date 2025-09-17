import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

def probar_conexion():
    """Prueba la conexión a la base de datos MySQL"""
    try:
        # Cargar variables de entorno
        load_dotenv()
        
        # Intentar establecer la conexión
        print("Intentando conectar a la base de datos...")
        connection = mysql.connector.connect(
            host=os.getenv('DBHOST'),
            user=os.getenv('DBUSER'),
            password=os.getenv('DBPASSWORD'),
            port=os.getenv('DBPORT'),
            database=os.getenv('DBDATABASE_NAME')
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