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
        'host': os.getenv('DBHOST'),
        'user': os.getenv('DBUSER'),
        'password': os.getenv('DBPASSWORD'),
        'port': os.getenv('DBPORT'),
        'database': os.getenv('DBDATABASE_NAME')
    }
