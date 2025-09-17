import os
import mysql.connector
import time
import pandas as pd
from Config.ConfigDB import ConfigDB

class LoadDB:
    def __init__(self, df):
        self.df = df

    def to_csv(self, output_path):
        try:
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            self.df.to_csv(output_path, index=False)
            print(f"✅ Datos guardados en: {output_path}")
        except Exception as e:
            print(f"❌ Error al guardar datos en CSV: {e}")

    def _get_connection(self, max_retries=3, delay=5):
        """Intenta establecer una conexión con reintentos"""
        for attempt in range(max_retries):
            try:
                config = ConfigDB.MYSQL_CONFIG.copy()
                config.update({
                    'connect_timeout': 60,
                    'connection_timeout': 60,
                    'pool_size': 5,
                    'pool_reset_session': True,
                    'autocommit': True,
                    'buffered': True
                })
                return mysql.connector.connect(**config)
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Intento {attempt + 1} fallido. Reintentando en {delay} segundos...")
                    time.sleep(delay)
                else:
                    raise e

    def to_mysql(self, batch_size=50):
        conn = None
        cursor = None
        
        try:
            print("🔄 Conectando a la base de datos...")
            conn = self._get_connection()
            cursor = conn.cursor()

            print("🗑️ Eliminando tabla anterior si existe...")
            cursor.execute("DROP TABLE IF EXISTS football_matches")
            conn.commit()
            
            print("📝 Creando nueva tabla...")
            cursor.execute("""
                CREATE TABLE football_matches (
                    match_id INT PRIMARY KEY,
                    competition_code VARCHAR(10),
                    competition_name VARCHAR(100),
                    season VARCHAR(20),
                    matchday INT,
                    stage VARCHAR(50),
                    status VARCHAR(20),
                    date_utc DATETIME,
                    referee VARCHAR(100),
                    home_team_id INT,
                    home_team VARCHAR(100),
                    away_team_id INT,
                    away_team VARCHAR(100),
                    fulltime_home INT,
                    fulltime_away INT,
                    halftime_home FLOAT,
                    halftime_away FLOAT,
                    goal_difference INT,
                    total_goals INT,
                    match_outcome VARCHAR(20),
                    home_points INT,
                    away_points INT,
                    date_local_africa_cairo VARCHAR(50)
                )
            """)
            conn.commit()

            total_rows = len(self.df)
            processed_rows = 0
            batch_data = []

            print("📥 Iniciando carga de datos por lotes...")
            for _, row in self.df.iterrows():
                batch_data.append((
                    int(row['match_id']),
                    row['competition_code'],
                    row['competition_name'],
                    row['season'],
                    int(row['matchday']),
                    row['stage'],
                    row['status'],
                    row['date_utc'].split("+")[0] if isinstance(row['date_utc'], str) else None,
                    row['referee'],
                    int(row['home_team_id']),
                    row['home_team'],
                    int(row['away_team_id']),
                    row['away_team'],
                    int(row['fulltime_home']),
                    int(row['fulltime_away']),
                    float(row['halftime_home']) if not pd.isna(row['halftime_home']) else None,
                    float(row['halftime_away']) if not pd.isna(row['halftime_away']) else None,
                    int(row['goal_difference']),
                    int(row['total_goals']),
                    row['match_outcome'],
                    int(row['home_points']),
                    int(row['away_points']),
                    row['date_local_africa_cairo']
                ))

                if len(batch_data) >= batch_size or processed_rows + len(batch_data) == total_rows:
                    retry_count = 0
                    max_retries = 3
                    while retry_count < max_retries:
                        try:
                            if not conn.is_connected():
                                print("⚠️ Reconectando a la base de datos...")
                                conn = self._get_connection()
                                cursor = conn.cursor()

                            cursor.executemany("""
                                INSERT INTO football_matches (
                                    match_id, competition_code, competition_name, season, matchday, stage, status, 
                                    date_utc, referee, home_team_id, home_team, away_team_id, away_team,
                                    fulltime_home, fulltime_away, halftime_home, halftime_away, goal_difference, 
                                    total_goals, match_outcome, home_points, away_points, date_local_africa_cairo
                                ) VALUES (
                                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                                )
                            """, batch_data)
                            conn.commit()
                            processed_rows += len(batch_data)
                            print(f"📊 Progreso: {processed_rows}/{total_rows} registros procesados")
                            batch_data = []
                            break
                        except mysql.connector.Error as err:
                            retry_count += 1
                            if retry_count < max_retries:
                                print(f"⚠️ Error en lote, reintento {retry_count} de {max_retries}...")
                                time.sleep(5)
                            else:
                                raise err

            print("✅ Datos cargados exitosamente en la tabla football_matches")

        except Exception as e:
            print(f"❌ Error al cargar datos en MySQL: {str(e)}")
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            raise
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass
