# DeportesDB - Sistema ETL y Visualización de Datos de Fútbol

## 📋 Descripción
Sistema ETL (Extract, Transform, Load) para procesar y analizar datos de partidos de fútbol de las principales ligas europeas. El proyecto incluye carga de datos a MySQL, visualizaciones estadísticas y análisis de resultados.

## 🏗️ Estructura del Proyecto
```
DeportesDB/
├── Config/                 # Configuración del proyecto
│   ├── __init__.py
│   └── ConfigDB.py        # Configuración de base de datos y rutas
├── Extract/               # Módulo de extracción de datos
│   ├── __init__.py
│   ├── ExtractDB.py      # Clase principal de extracción
│   └── Clean/            # Submódulo de limpieza
│       ├── __init__.py
│       └── CleanDB.py    # Lógica de limpieza de datos
├── Transform/            # Módulo de transformación
│   ├── __init__.py
│   └── TransformDB.py    # Transformación de datos
├── Load/                 # Módulo de carga
│   ├── __init__.py
│   ├── LoadDB.py        # Carga normal
│   └── BatchLoader.py    # Carga por lotes
├── Vizualize/           # Módulo de visualización
│   ├── __init__.py
│   ├── SportVizualize.py # Generación de gráficas
│   └── output/          # Carpeta de salida para gráficas
├── Test/                # Pruebas
│   └── Test_DataBase.py # Pruebas de conexión
├── output/              # Datos procesados
├── .env                 # Variables de entorno
├── main.py             # Script principal ETL
├── batch_load.py       # Script de carga por lotes
└── MainVizualize.py    # Script principal de visualización
```

## 🚀 Características

### ETL Pipeline
- **Extracción**: Lectura de datos desde CSV
- **Transformación**: Limpieza y preparación de datos
- **Carga**: 
  - Carga directa a MySQL
  - Sistema de carga por lotes (10 registros/minuto)
  - Manejo de reconexión y reintentos

### Visualizaciones
- Distribución de goles por competición
- Análisis de resultados (local/visitante/empate)
- Top 10 equipos goleadores
- Evolución temporal de goles
- Análisis de ventaja local

## 🛠️ Requisitos
- Python 3.x
- MySQL
- Bibliotecas Python:
  - pandas
  - mysql-connector-python
  - matplotlib
  - seaborn
  - python-dotenv

## ⚙️ Configuración

1. **Variables de Entorno**
   Crear archivo `.env` con:
   ```
   DBUSER=tu_usuario
   DBPASSWORD=tu_contraseña
   DBHOST=tu_host
   DBPORT=tu_puerto
   DBDATABASE_NAME=tu_base_de_datos
   ```

2. **Entorno Virtual e Instalación**
   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate
   pip install pandas mysql-connector-python matplotlib seaborn python-dotenv
   ```

## 📈 Uso

### Proceso ETL Completo
```bash
python main.py
```
Este comando:
1. Lee el archivo CSV de entrada
2. Limpia y transforma los datos
3. Guarda el CSV procesado
4. Carga los datos en MySQL

### Carga por Lotes
```bash
python batch_load.py
```
Realiza la carga de datos en lotes de 10 registros cada minuto.

### Generación de Visualizaciones
```bash
python MainVizualize.py
```
Genera todas las visualizaciones y las guarda en `Vizualize/output/`.

## 📊 Visualizaciones Generadas

- `goals_distribution.png`: Promedio de goles por partido en cada competición
- `match_outcomes.png`: Distribución de victorias locales, visitantes y empates
- `top_scorers.png`: Los 10 equipos más goleadores
- `goals_timeline.png`: Evolución del promedio de goles en el tiempo
- `home_advantage.png`: Análisis de la ventaja de jugar como local

## 🧪 Pruebas
Para verificar la conexión a la base de datos:
```bash
python Test/Test_DataBase.py
```

## 🔐 Seguridad
- Uso de variables de entorno para credenciales
- Manejo de conexiones seguras
- Timeouts y reconexión automática
- Validación de datos de entrada

## 📝 Notas
- Los datos se procesan en lotes para optimizar el rendimiento
- Las visualizaciones se generan en alta resolución (300 DPI)
- Se implementa manejo de errores y logging
- La estructura modular permite fácil extensión

## 👥 Contribuir
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para más detalles.

## ✨ Agradecimientos
- Datos proporcionados por las ligas de fútbol europeas
- Comunidad de Python por las bibliotecas utilizadas
