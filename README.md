# 📡 YT Political Monitor — Dashboard

Dashboard de visualización para la plataforma Big Data de detección de discurso discriminatorio y polarización política en YouTube (contexto político peruano).

Consume los resultados generados por **Apache Flink** (tiempo real) y **Apache Spark** (batch histórico) almacenados en **AWS S3**.

---

## Estructura del proyecto

```
yt-dashboard/
├── app.py                  # Entry point de Streamlit
├── requirements.txt
├── pages/
│   ├── resumen.py          # Resumen general (KPIs + distribución)
│   ├── tiempo_real.py      # Flink Jobs 1 y 2 — frecuencia y tasa
│   ├── alertas.py          # Flink Job 3 — alertas de polarización
│   ├── videos_criticos.py  # Flink Job 4 — top videos tóxicos
│   ├── autores.py          # Flink Job 5 — autores activos
│   ├── historico.py        # Spark Jobs 1, 3, 4 — análisis batch
│   ├── jerguometro.py      # Spark Jobs 2 y 5 — jerga peruana
│   └── metricas.py         # Throughput, latencia, tabla de métricas
├── utils/
│   ├── styles.py           # CSS global inyectado en Streamlit
│   ├── charts.py           # Helpers de Plotly con tema oscuro
│   └── data_loader.py      # Lógica de carga: S3 → local → simulado
└── data/                   # (Opcional) JSONs locales para pruebas
```

---

## Requisitos

- Python 3.10 o superior
- Pip actualizado

---

## Instalación

### 1. Clonar / copiar el proyecto

```bash
# Si tienes el .zip, descomprimirlo y entrar a la carpeta
cd yt-dashboard
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv

# Activar en Linux/macOS
source venv/bin/activate

# Activar en Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Modos de ejecución

El dashboard funciona en tres modos automáticamente, en este orden de prioridad:

| Modo | Cuándo se activa | Descripción |
|------|-----------------|-------------|
| **S3 en vivo** | Cuando `boto3` encuentra credenciales AWS válidas | Lee los JSONs reales de tus jobs Flink y Spark |
| **Local** | Cuando hay archivos en `./data/` | Lee JSONs locales (útil para pruebas sin AWS) |
| **Demo simulada** | Siempre como fallback | Genera datos ficticios realistas |

---

## Configuración AWS S3 (modo en vivo)

### Opción A — Variables de entorno

```bash
export AWS_ACCESS_KEY_ID=TU_ACCESS_KEY
export AWS_SECRET_ACCESS_KEY=TU_SECRET_KEY
export AWS_DEFAULT_REGION=us-east-1
export S3_BUCKET=tu-bucket-elecciones
```

### Opción B — Archivo de credenciales AWS

```bash
# Instalar AWS CLI si no lo tienes
pip install awscli

# Configurar credenciales
aws configure
```

Te pedirá:
```
AWS Access Key ID: TU_ACCESS_KEY
AWS Secret Access Key: TU_SECRET_KEY
Default region name: us-east-1
Default output format: json
```

Esto crea `~/.aws/credentials` automáticamente.

### Verificar conexión

```bash
aws s3 ls s3://tu-bucket-elecciones/output/
```

Si ves las carpetas `tiempo_real/` e `historico/`, la conexión es correcta.

---

## Rutas S3 que consume el dashboard

El dashboard espera exactamente esta estructura en tu bucket:

```
s3://tu-bucket-elecciones/output/
├── tiempo_real/
│   ├── job1_frecuencia/        ← Flink Job 1: frecuencia por minuto
│   ├── job2_tasa/              ← Flink Job 2: tasa odio vs neutral
│   ├── job3_alertas/           ← Flink Job 3: alertas críticas
│   ├── job4_top_videos/        ← Flink Job 4: videos más tóxicos
│   └── job5_trolls/            ← Flink Job 5: autores activos
└── historico/
    ├── job1_distribucion.json/ ← Spark Job 1: distribución global
    ├── job2_jerguometro.json/  ← Spark Job 2: frecuencia de jerga
    ├── job3_longitud.json/     ← Spark Job 3: longitud promedio
    ├── job4_polarizacion.json/ ← Spark Job 4: ratio polarización
    └── job5_top_palabras.json/ ← Spark Job 5: top palabras odio
```

> Si el nombre de tu bucket es diferente, cambia la variable de entorno `S3_BUCKET` o edita la línea en `utils/data_loader.py`:
> ```python
> S3_BUCKET = os.getenv("S3_BUCKET", "tu-bucket-elecciones")
> ```

---

## Formato esperado de los archivos JSON

Cada carpeta en S3 puede contener uno o más archivos `.json` con registros en formato **JSON Lines** (un objeto por línea).

### Flink Job 1 — `job1_frecuencia/`
```json
{"window_start": "14:23", "count": 87}
{"window_start": "14:24", "count": 103}
```

### Flink Job 2 — `job2_tasa/`
```json
{"window": "14:23:00", "ODIO_POLITICO": 12, "ODIO_DEMOGRAFICO": 5, "ODIO_GENERAL": 8, "NEUTRAL": 30}
```

### Flink Job 3 — `job3_alertas/`
```json
{"timestamp": "14:23:45", "message": "Pico detectado: 45 menciones de terruco", "level": "HIGH"}
```
Valores válidos para `level`: `HIGH`, `MEDIUM`, `LOW`

### Flink Job 4 — `job4_top_videos/`
```json
{"video_title": "Debate presidencial Peru 2026", "odio_count": 234, "query": "fujimorismo Peru"}
```

### Flink Job 5 — `job5_trolls/`
```json
{"author": "user_anon_123", "hate_count": 47}
```

### Spark Job 1 — `job1_distribucion.json/`
```json
{"clasificacion": "ODIO_POLITICO", "count": 1812}
{"clasificacion": "ODIO_DEMOGRAFICO", "count": 1053}
{"clasificacion": "ODIO_GENERAL", "count": 1286}
{"clasificacion": "NEUTRAL", "count": 1696}
```

### Spark Job 2 — `job2_jerguometro.json/`
```json
{"termino": "terruco", "frecuencia": 342}
{"termino": "caviar", "frecuencia": 287}
```

### Spark Job 3 — `job3_longitud.json/`
```json
{"clasificacion": "ODIO_POLITICO", "longitud_promedio": 142.3}
```

### Spark Job 4 — `job4_polarizacion.json/`
```json
{"odio_politico": 1812, "odio_demografico": 1053, "ratio": 1.72, "total_odio": 2865}
```

### Spark Job 5 — `job5_top_palabras.json/`
```json
{"palabra": "terruco", "frecuencia": 342}
{"palabra": "fujimori", "frecuencia": 289}
```

---

## Pruebas con archivos locales (sin AWS)

Crea la carpeta `data/` dentro del proyecto y coloca archivos con los nombres exactos:

```
data/
├── flink1_frecuencia.json
├── flink2_tasa.json
├── flink3_alertas.json
├── flink4_top_videos.json
├── flink5_trolls.json
├── spark1_distribucion.json
├── spark2_jerguometro.json
├── spark3_longitud.json
├── spark4_polarizacion.json
└── spark5_top_palabras.json
```

---

## Ejecutar el dashboard

```bash
streamlit run app.py
```

Abre automáticamente `http://localhost:8501` en tu navegador.

### Opciones adicionales

```bash
# Cambiar puerto
streamlit run app.py --server.port 8502

# Modo sin abrir navegador automáticamente
streamlit run app.py --server.headless true

# Con bucket S3 personalizado
S3_BUCKET=mi-bucket streamlit run app.py
```

---

## Auto-refresh en tiempo real

En la página **Tiempo real**, hay un toggle de auto-refresh. Al activarlo, el dashboard recarga los datos de S3 cada **30 segundos**, simulando monitoreo en vivo durante la presentación.

> Para la demo: activa el pipeline completo en AWS, luego activa el toggle. Cada vez que Flink escriba en S3, el dashboard mostrará los nuevos datos en la siguiente recarga.

---

## Dependencias

| Librería | Versión mínima | Uso |
|----------|---------------|-----|
| `streamlit` | 1.35.0 | Framework del dashboard |
| `plotly` | 5.20.0 | Gráficas interactivas |
| `pandas` | 2.0.0 | Manejo de datos tabulares |
| `boto3` | 1.34.0 | Conexión con AWS S3 |

---

## Secciones del dashboard

| Sección | Fuente | Descripción |
|---------|--------|-------------|
| Resumen general | Spark Job 1 + Flink Job 4 | KPIs totales y distribución |
| Tiempo real | Flink Jobs 1 y 2 | Frecuencia e ingesta en vivo |
| Alertas | Flink Job 3 | Picos de odio político |
| Videos críticos | Flink Job 4 | Ranking de toxicidad por video |
| Autores activos | Flink Job 5 | Usuarios con más comentarios de odio |
| Histórico | Spark Jobs 1, 3, 4 | Distribución, longitud, polarización |
| Jerguómetro | Spark Jobs 2 y 5 | Frecuencia de jerga peruana |
| Métricas técnicas | Pipeline completo | Throughput, latencia, tabla |
