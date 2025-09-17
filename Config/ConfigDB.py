import os
from dotenv import load_dotenv

class ConfigDB:
    """
    Clase de configuración para rutas y parámetros del ETL.
    """
    # Cargar variables de entorno
    load_dotenv()

    # Rutas de archivos
    INPUT_PATH = 'football_matches_2024_2025.csv'
    OUTPUT_PATH = 'output/football_matches_2024_2025_clean.csv'
    
    # Configuración MySQL
    MYSQL_TABLE = 'football_matches_2024_2025'
    MYSQL_CONFIG = {
        'host': os.getenv('DBHOST', 'localhost'),
        'user': os.getenv('DBUSER', 'root'),
        'password': os.getenv('DBPASSWORD', ''),
        'port': int(os.getenv('DBPORT', '3306')),
        'database': os.getenv('DBDATABASE_NAME', 'railway'),
        'connect_timeout': 60,
        'autocommit': True,
        'buffered': True
    }
