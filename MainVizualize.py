from Vizualize.SportVizualize import SportVisualize
import os
import time

def main():
    try:
        print("\n📊 Iniciando proceso de visualización de datos deportivos...")
        start_time = time.time()

        # Verificar que existe el archivo CSV limpio
        csv_path = "output/football_matches_2024_2025_clean.csv"
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"No se encontró el archivo CSV en: {csv_path}")

        print("\n📈 Creando visualizaciones...")
        visualizer = SportVisualize(csv_path)
        
        # Generar todas las visualizaciones
        visualizer.generate_all_visualizations()

        # Resumen final
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        print(f"\n✨ Proceso de visualización completado en {duration} segundos")
        print("📁 Las gráficas se han guardado en la carpeta 'Vizualize/output'")

    except FileNotFoundError as e:
        print(f"\n❌ Error: {str(e)}")
        print("💡 Asegúrate de ejecutar primero el proceso ETL (main.py) para generar el archivo CSV limpio")
    except Exception as e:
        print(f"\n❌ Error durante el proceso de visualización: {str(e)}")

if __name__ == "__main__":
    main()
