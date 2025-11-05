import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

class SportVisualize:
    def __init__(self, csv_path):
        """
        Inicializa la clase de visualización.
        
        Args:
            csv_path (str): Ruta al archivo CSV limpio
        """
        self.df = pd.read_csv(csv_path)
        # Configurar el estilo de las gráficas
        plt.style.use('seaborn-v0_8')  # Actualizado para versiones más recientes
        sns.set_palette("husl")

    def setup_plot(self, figsize=(12, 6)):
        """Configura el tamaño y estilo base de la gráfica"""
        plt.figure(figsize=figsize)

    def save_plot(self, name, dpi=300):
        """Guarda la gráfica en la carpeta de visualizaciones"""
        output_dir = Path("Vizualize/output")
        output_dir.mkdir(exist_ok=True)
        plt.savefig(output_dir / f"{name}.png", dpi=dpi, bbox_inches='tight')
        plt.close()

    def plot_goals_distribution(self):
        """Gráfica de distribución de goles por competición"""
        self.setup_plot(figsize=(15, 8))
        
        competitions = self.df.groupby('competition_name').agg({
            'total_goals': 'sum',
            'match_id': 'count'
        }).reset_index()
        
        competitions['goals_per_match'] = competitions['total_goals'] / competitions['match_id']
        
        ax = sns.barplot(
            data=competitions,
            x='competition_name',
            y='goals_per_match',
            order=competitions.sort_values('goals_per_match', ascending=False)['competition_name']
        )
        
        plt.title('Promedio de Goles por Partido en cada Competición', pad=20)
        plt.xlabel('Competición')
        plt.ylabel('Goles por Partido')
        plt.xticks(rotation=45)
        
        # Añadir valores sobre las barras
        for i in ax.containers:
            ax.bar_label(i, fmt='%.2f', padding=3)
            
        self.save_plot('goals_distribution')

    def plot_match_outcomes(self):
        """Gráfica de distribución de resultados de partidos"""
        self.setup_plot()
        
        outcomes = self.df['match_outcome'].value_counts()
        colors = ['#2ecc71', '#f1c40f', '#e74c3c']
        
        plt.pie(outcomes, labels=outcomes.index, autopct='%1.1f%%', colors=colors)
        plt.title('Distribución de Resultados de Partidos', pad=20)
        
        self.save_plot('match_outcomes')

    def plot_top_scorers(self):
        """Gráfica de equipos con más goles"""
        self.setup_plot(figsize=(15, 8))
        
        # Calcular goles totales por equipo (local + visitante)
        home_goals = self.df.groupby('home_team')['fulltime_home'].sum().reset_index()
        away_goals = self.df.groupby('away_team')['fulltime_away'].sum().reset_index()
        
        # Renombrar columnas para la concatenación
        home_goals.columns = ['team', 'goals']
        away_goals.columns = ['team', 'goals']
        
        # Concatenar y agrupar
        total_goals = pd.concat([home_goals, away_goals])\
            .groupby('team')['goals'].sum()\
            .sort_values(ascending=False)\
            .head(10)
        
        ax = sns.barplot(x=total_goals.values, y=total_goals.index)
        plt.title('Top 10 Equipos con Más Goles', pad=20)
        plt.xlabel('Número Total de Goles')
        plt.ylabel('Equipo')
        
        # Añadir valores sobre las barras
        for i in ax.containers:
            ax.bar_label(i, padding=5)
            
        self.save_plot('top_scorers')

    def plot_goals_timeline(self):
        """Gráfica de goles a lo largo del tiempo"""
        self.setup_plot(figsize=(15, 8))
        
        # Convertir fecha a datetime y ordenar
        self.df['date_utc'] = pd.to_datetime(self.df['date_utc'])
        timeline = self.df.groupby('date_utc')['total_goals'].mean().rolling(7).mean()
        
        plt.plot(timeline.index, timeline.values, linewidth=2)
        plt.title('Promedio de Goles por Partido (Media Móvil 7 días)', pad=20)
        plt.xlabel('Fecha')
        plt.ylabel('Promedio de Goles')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        self.save_plot('goals_timeline')

    def plot_home_advantage(self):
        """Gráfica de ventaja local por competición"""
        self.setup_plot(figsize=(15, 8))
        
        home_advantage = self.df.groupby('competition_name').agg({
            'home_points': 'mean',
            'match_id': 'count'
        }).sort_values('home_points', ascending=False)
        
        ax = sns.barplot(
            x=home_advantage.index,
            y='home_points',
            data=home_advantage
        )
        
        plt.title('Promedio de Puntos Locales por Competición', pad=20)
        plt.xlabel('Competición')
        plt.ylabel('Promedio de Puntos como Local')
        plt.xticks(rotation=45)
        
        # Añadir valores sobre las barras
        for i in ax.containers:
            ax.bar_label(i, fmt='%.2f', padding=3)
            
        self.save_plot('home_advantage')

    def generate_all_visualizations(self):
        """Genera todas las visualizaciones disponibles"""
        print("\n📊 Generando visualizaciones...")
        
        visualizations = [
            (self.plot_goals_distribution, "Distribución de goles"),
            (self.plot_match_outcomes, "Resultados de partidos"),
            (self.plot_top_scorers, "Top equipos goleadores"),
            (self.plot_goals_timeline, "Línea de tiempo de goles"),
            (self.plot_home_advantage, "Ventaja local")
        ]
        
        for viz_func, viz_name in visualizations:
            print(f"🎨 Generando {viz_name}...")
            viz_func()
            
        print("\n✨ Visualizaciones generadas exitosamente")
        print("📁 Las gráficas se han guardado en la carpeta 'Vizualize/output'")


def main():
    # Ruta al archivo CSV limpio
    csv_path = "output/football_matches_2024_2025_clean.csv"
    
    try:
        # Crear instancia de visualización
        visualizer = SportVisualize(csv_path)
        
        # Generar todas las visualizaciones
        visualizer.generate_all_visualizations()
        
    except Exception as e:
        print(f"\n❌ Error al generar visualizaciones: {str(e)}")

if __name__ == "__main__":
    main()
