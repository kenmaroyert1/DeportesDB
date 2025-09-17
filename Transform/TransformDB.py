import pandas as pd

class TransformDB:
    """
    Clase para transformar y limpiar los datos de partidos de fútbol.
    """
    def __init__(self, df):
        self.df = df

    def clean(self):
        """
        Realiza limpieza y transformación de los datos.
        """
        df = self.df.copy()

        # 1. Eliminar duplicados
        df = df.drop_duplicates()

        # 2. Eliminar filas sin match_id (clave primaria)
        df = df.dropna(subset=["match_id"])

        # 3. Asegurar que las columnas numéricas sean realmente numéricas
        num_cols = [
            "matchday", "home_team_id", "away_team_id",
            "fulltime_home", "fulltime_away",
            "halftime_home", "halftime_away",
            "goal_difference", "total_goals",
            "home_points", "away_points"
        ]
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

        # 4. Normalizar texto (strip espacios, convertir a str)
        str_cols = [
            "competition_code", "competition_name", "season",
            "stage", "status", "referee",
            "home_team", "away_team", "match_outcome",
            "date_local_africa_cairo"
        ]
        for col in str_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()

        # 5. Convertir fechas a tipo datetime
        if "date_utc" in df.columns:
            df["date_utc"] = pd.to_datetime(df["date_utc"], errors="coerce")

        # Guardar DataFrame limpio
        self.df = df
        return self.df
