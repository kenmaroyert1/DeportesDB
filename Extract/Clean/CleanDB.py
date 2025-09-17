import pandas as pd
from Config.ConfigBig import Config

class CleanDB:
    """
    Limpieza universal (aplicable a cualquier CSV, optimizada ahora para football_matches).
    Incluye:
    - Eliminación de duplicados
    - Manejo de NA en columnas de texto
    - Limpieza de valores no deseados
    - Relleno de datos ausentes en columnas numéricas
    - QA de tipos de datos (tipificación correcta)
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    # --- pasos atómicos (encadenables) ---

    def remove_duplicates(self):
        if Config.DROP_DUPLICATES:
            self.df = self.df.drop_duplicates()
        return self

    def handle_na_text(self):
        # Relleno genérico para columnas de texto
        text_cols = self.df.select_dtypes(include=["object"]).columns
        if len(text_cols) > 0:
            self.df[text_cols] = self.df[text_cols].fillna(Config.FILL_TEXT_DEFAULT)
        return self

    def remove_unwanted_values(self):
        # Limpieza de caracteres no deseados en columnas de texto
        text_cols = self.df.select_dtypes(include=["object"]).columns
        for col in text_cols:
            self.df[col] = (
                self.df[col]
                .astype(str)
                .str.strip()
                .str.replace(Config.UNWANTED_PATTERN, "", regex=True)
            )
        return self

    def fill_missing_numeric(self):
        # Convertir a numérico lo que se pueda y rellenar NA
        num_candidates = self.df.columns.difference(
            self.df.select_dtypes(include=["object", "bool", "datetime64[ns]"]).columns
        )
        for col in num_candidates:
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

        num_cols = self.df.select_dtypes(include=["number"]).columns
        if len(num_cols) == 0:
            return self

        strat = Config.NUMERIC_MISSING_STRATEGY
        if strat == "zero":
            self.df[num_cols] = self.df[num_cols].fillna(0)
        elif strat == "mean":
            self.df[num_cols] = self.df[num_cols].fillna(self.df[num_cols].mean())
        elif strat == "median":
            self.df[num_cols] = self.df[num_cols].fillna(self.df[num_cols].median())
        elif strat == "mode":
            self.df[num_cols] = self.df[num_cols].fillna(self.df[num_cols].mode().iloc[0])
        else:
            self.df[num_cols] = self.df[num_cols].fillna(0)
        return self

    def qa_types(self):
        """
        Tipos razonables en football_matches:
        - match_id debe ser int
        - goles, puntos y diferencias: int
        - halftime_*: float
        - fechas: datetime
        """
        if "match_id" in self.df.columns:
            self.df["match_id"] = pd.to_numeric(self.df["match_id"], errors="coerce").fillna(0).astype(int)

        numeric_int_cols = [
            "matchday", "home_team_id", "away_team_id",
            "fulltime_home", "fulltime_away",
            "goal_difference", "total_goals",
            "home_points", "away_points"
        ]
        for col in numeric_int_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors="coerce").fillna(0).astype(int)

        numeric_float_cols = ["halftime_home", "halftime_away"]
        for col in numeric_float_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors="coerce").astype(float)

        date_cols = ["date_utc", "date_local_africa_cairo"]
        for col in date_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors="coerce")

        return self

    # --- pipeline principal ---

    def universal_clean(self) -> pd.DataFrame:
        """
        Ejecuta todos los pasos de limpieza (universal).
        """
        return (
            self.remove_duplicates()
                .handle_na_text()
                .remove_unwanted_values()
                .fill_missing_numeric()
                .qa_types()
                .df
        )
