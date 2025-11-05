import pandas as pd
import time
from Config.ConfigDB import ConfigDB
import mysql.connector
from datetime import datetime

class BatchLoader:
    def __init__(self, df, batch_size=10, interval_seconds=60):
        """
        Inicializa el cargador por lotes.
        
        Args:
            df (pandas.DataFrame): DataFrame con los datos a cargar
            batch_size (int): Cantidad de registros por lote (default: 10)
            interval_seconds (int): Intervalo entre lotes en segundos (default: 60)
        """
        self.df = df
        self.batch_size = batch_size
        self.interval = interval_seconds
        self.current_position = 0

    def _get_connection(self):
        """Establece conexión con la base de datos"""
        try:
            return mysql.connector.connect(**ConfigDB.MYSQL_CONFIG)
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def _insert_batch(self, batch_df, cursor):
        """Inserta un lote de registros en la base de datos"""
        try:
            values = [tuple(x) for x in batch_df.values]
            cursor.executemany("""
                INSERT INTO football_matches (
                    competition_code, competition_name, season, match_id, matchday,
                    stage, status, date_utc, referee, home_team_id, home_team,
                    away_team_id, away_team, fulltime_home, fulltime_away,
                    halftime_home, halftime_away, goal_difference, total_goals,
                    match_outcome, home_points, away_points, date_local_africa_cairo
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, values)
            return True
        except Exception as e:
            print(f"Error al insertar lote: {e}")
            return False

    def process_in_batches(self):
        """Procesa los datos en lotes con intervalo de tiempo"""
        total_records = len(self.df)
        
        while self.current_position < total_records:
            start_time = time.time()
            
            # Obtener el próximo lote
            end_position = min(self.current_position + self.batch_size, total_records)
            batch = self.df.iloc[self.current_position:end_position]
            
            # Establecer conexión
            conn = self._get_connection()
            if not conn:
                print("No se pudo establecer conexión. Reintentando en el próximo ciclo...")
                time.sleep(self.interval)
                continue

            try:
                cursor = conn.cursor()
                
                # Insertar lote
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
                print(f"Procesando lote de {len(batch)} registros...")
                
                if self._insert_batch(batch, cursor):
                    conn.commit()
                    print(f"✅ Lote insertado correctamente")
                    print(f"Progreso: {self.current_position + len(batch)}/{total_records} registros")
                    self.current_position = end_position
                else:
                    print("❌ Error al insertar lote")

            except Exception as e:
                print(f"Error durante el proceso: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()

            # Calcular tiempo de espera
            elapsed_time = time.time() - start_time
            wait_time = max(0, self.interval - elapsed_time)
            
            if wait_time > 0 and self.current_position < total_records:
                print(f"\nEsperando {wait_time:.1f} segundos para el siguiente lote...")
                time.sleep(wait_time)