from Config.ConfigDB import ConfigDB
from Extract.ExtractDB import ExtractDB
from Transform.TransformDB import TransformDB
from Load.BatchLoader import BatchLoader

def main():
    try:
        print("\n⚽ Iniciando proceso de carga por lotes...")
        
        # Extract
        print("\n📥 Extrayendo datos...")
        extractor = ExtractDB(ConfigDB.INPUT_PATH)
        df = extractor.extract()

        if df is not None:
            print(f"✅ Datos extraídos exitosamente. Registros encontrados: {len(df)}")

            # Transform
            print("\n🔄 Transformando datos...")
            transformer = TransformDB(df)
            df_clean = transformer.clean()
            
            print(f"✅ Datos transformados. Registros limpios: {len(df_clean)}")

            # Load en lotes
            print("\n📤 Iniciando carga por lotes...")
            batch_loader = BatchLoader(
                df=df_clean,
                batch_size=10,      # 10 registros por lote
                interval_seconds=60  # 1 minuto entre lotes
            )
            
            print("\n⏳ Comenzando proceso de carga...")
            print("Presiona Ctrl+C para detener el proceso")
            batch_loader.process_in_batches()

        else:
            print("❌ Error: No se pudieron extraer los datos")

    except KeyboardInterrupt:
        print("\n\n🛑 Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante el proceso: {e}")

if __name__ == "__main__":
    main()