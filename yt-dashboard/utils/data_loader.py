"""
Data loader for YT Political Monitor dashboard.

Priority:
  1. AWS S3  (if boto3 + credentials available)
  2. Local files in ./data/ folder
  3. Simulated data (fallback for demo / development)
"""

import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any

import pandas as pd
import streamlit as st


# ── S3 paths ────────────────────────────────────────────────────────────────

S3_BUCKET = os.getenv("S3_BUCKET", "tu-bucket-elecciones")
S3_PREFIX_RT = "output/tiempo_real"
S3_PREFIX_HIST = "output/historico"

S3_PATHS = {
    # Realtime jobs / Flink-like outputs
    "job_flink1_frecuencia": f"s3://{S3_BUCKET}/{S3_PREFIX_RT}/job1_frecuencia/",
    "job_flink2_tasa": f"s3://{S3_BUCKET}/{S3_PREFIX_RT}/job2_tasa/",
    "job_flink3_alertas": f"s3://{S3_BUCKET}/{S3_PREFIX_RT}/job3_alertas/",
    "job_flink4_top_videos": f"s3://{S3_BUCKET}/{S3_PREFIX_RT}/job4_top_videos/",
    "job_flink5_trolls": f"s3://{S3_BUCKET}/{S3_PREFIX_RT}/job5_trolls/",

    # Historical jobs / Spark-like outputs
    "job_spark1_distribucion": f"s3://{S3_BUCKET}/{S3_PREFIX_HIST}/job1_distribucion.json/",
    "job_spark2_jerguometro": f"s3://{S3_BUCKET}/{S3_PREFIX_HIST}/job2_jerguometro.json/",
    "job_spark3_longitud": f"s3://{S3_BUCKET}/{S3_PREFIX_HIST}/job3_longitud.json/",
    "job_spark4_polarizacion": f"s3://{S3_BUCKET}/{S3_PREFIX_HIST}/job4_polarizacion.json/",
    "job_spark5_top_palabras": f"s3://{S3_BUCKET}/{S3_PREFIX_HIST}/job5_top_palabras.json/",
}


# ─────────────────────────────────────────────────────────────────────────────
# S3 reader
# ─────────────────────────────────────────────────────────────────────────────

def _read_s3_json(s3_path: str) -> Optional[List[Dict[str, Any]]]:
    """
    Reads JSON or JSONL files from an S3 prefix.

    Returns:
        list[dict] if records were found.
        None if the prefix does not exist, is empty, or AWS credentials fail.
    """
    try:
        import boto3

        print(f"[S3] Intentando leer: {s3_path}")

        s3 = boto3.client("s3")

        without_scheme = s3_path.replace("s3://", "")
        bucket = without_scheme.split("/")[0]
        key_prefix = "/".join(without_scheme.split("/")[1:])

        response = s3.list_objects_v2(Bucket=bucket, Prefix=key_prefix)
        objects = response.get("Contents", [])

        print(f"[S3] Objetos encontrados en {key_prefix}: {len(objects)}")

        if not objects:
            return None

        records: List[Dict[str, Any]] = []

        # Read old → new so charts keep chronological order
        for obj in sorted(objects, key=lambda x: x["LastModified"]):
            key = obj["Key"]

            if key.endswith("/"):
                continue

            try:
                body = s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode("utf-8")
            except Exception as e:
                print(f"[S3 ERROR] No se pudo leer objeto {key}: {e}")
                continue

            content = body.strip()

            if not content:
                continue

            # Try full JSON first
            try:
                parsed = json.loads(content)

                if isinstance(parsed, list):
                    for item in parsed:
                        if isinstance(item, dict):
                            records.append(item)
                elif isinstance(parsed, dict):
                    records.append(parsed)

                continue

            except Exception:
                pass

            # Fallback: JSON Lines
            for line in content.splitlines():
                line = line.strip()

                if not line:
                    continue

                try:
                    parsed_line = json.loads(line)
                    if isinstance(parsed_line, dict):
                        records.append(parsed_line)
                except Exception as e:
                    print(f"[S3 WARNING] Línea inválida en {key}: {e}")

        print(f"[S3] Registros cargados desde {key_prefix}: {len(records)}")

        return records if records else None

    except Exception as e:
        print(f"[S3 ERROR] No se pudo leer {s3_path}: {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Local file reader
# ─────────────────────────────────────────────────────────────────────────────

def _read_local_json(filename: str) -> Optional[List[Dict[str, Any]]]:
    path = Path(__file__).parent.parent / "data" / filename

    if not path.exists():
        return None

    try:
        content = path.read_text(encoding="utf-8").strip()

        if not content:
            return None

        try:
            data = json.loads(content)
            return data if isinstance(data, list) else [data]
        except Exception:
            records = []

            for line in content.splitlines():
                try:
                    item = json.loads(line)
                    if isinstance(item, dict):
                        records.append(item)
                except Exception:
                    pass

            return records or None

    except Exception as e:
        print(f"[LOCAL ERROR] No se pudo leer {filename}: {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Simulated data
# ─────────────────────────────────────────────────────────────────────────────

QUERIES = [
    "fujimorismo Peru",
    "Dina Boluarte",
    "Congreso Peru",
    "terruqueo Peru",
    "racismo Peru politica",
]

CATEGORIES = [
    "ODIO_POLITICO",
    "ODIO_DEMOGRAFICO",
    "ODIO_GENERAL",
    "NEUTRAL",
]

VIDEOS = [
    "Debate presidencial Peru 2026",
    "Dina Boluarte discurso",
    "Congreso Peru sesion plenaria",
    "Fujimori entrevista exclusiva",
    "Peru elecciones analisis",
]

AUTHORS = [
    "user_politico1",
    "troll_anon",
    "peruano_libre",
    "antifuji99",
    "debate_fan",
    "cholo_power",
    "ser_andino",
    "lima_centro",
    "congreso_watcher",
    "rojo_terror",
]

JERGA_POLITICA = [
    "terruco",
    "terruca",
    "fujitroll",
    "fujimorista",
    "caviar",
    "lapicito",
    "rojo",
    "libertarado",
    "cojudigno",
]

JERGA_DEMO = [
    "cholo",
    "chola",
    "serrano",
    "serrana",
    "andino",
    "llama",
    "indio",
    "mestizo",
]


def _simulated_frecuencia() -> List[Dict[str, Any]]:
    now = datetime.now()

    return [
        {
            "window_start": (now - timedelta(minutes=i)).strftime("%H:%M"),
            "count": random.randint(20, 120),
        }
        for i in range(30, 0, -1)
    ]


def _simulated_tasa() -> List[Dict[str, Any]]:
    now = datetime.now()
    rows = []

    for i in range(20, 0, -1):
        t = (now - timedelta(seconds=i * 10)).strftime("%H:%M:%S")
        base = random.randint(5, 30)

        rows.append(
            {
                "window": t,
                "ODIO_POLITICO": base,
                "ODIO_DEMOGRAFICO": int(base * 0.4),
                "ODIO_GENERAL": int(base * 0.6),
                "NEUTRAL": random.randint(10, 50),
            }
        )

    return rows


def _simulated_alertas() -> List[Dict[str, Any]]:
    now = datetime.now()

    templates = [
        "Pico de ODIO_POLITICO detectado en ventana",
        "Alta concentración de comentarios agresivos sobre política peruana",
        "Umbral superado de ODIO_DEMOGRAFICO en 60s",
        "Alerta: video con alta concentración de comentarios de odio",
        "Pico de polarización detectado",
    ]

    alerts = []

    for i in range(8):
        alerts.append(
            {
                "timestamp": (now - timedelta(minutes=i * 3)).strftime("%H:%M:%S"),
                "message": random.choice(templates),
                "level": random.choice(["HIGH", "HIGH", "MEDIUM", "MEDIUM", "LOW"]),
            }
        )

    return alerts


def _simulated_top_videos() -> List[Dict[str, Any]]:
    return [
        {
            "video_title": v,
            "odio_count": random.randint(40, 300),
            "query": random.choice(QUERIES),
        }
        for v in VIDEOS
    ]


def _simulated_trolls() -> List[Dict[str, Any]]:
    return sorted(
        [
            {
                "author": a,
                "hate_count": random.randint(5, 80),
            }
            for a in AUTHORS
        ],
        key=lambda x: -x["hate_count"],
    )


def _simulated_distribucion() -> List[Dict[str, Any]]:
    total = 5847

    return [
        {"clasificacion": "ODIO_POLITICO", "count": int(total * 0.31)},
        {"clasificacion": "ODIO_DEMOGRAFICO", "count": int(total * 0.18)},
        {"clasificacion": "ODIO_GENERAL", "count": int(total * 0.22)},
        {"clasificacion": "NEUTRAL", "count": int(total * 0.29)},
    ]


def _simulated_jerguometro() -> List[Dict[str, Any]]:
    terms = JERGA_POLITICA + JERGA_DEMO

    return sorted(
        [
            {
                "termino": t,
                "frecuencia": random.randint(30, 400),
            }
            for t in terms
        ],
        key=lambda x: -x["frecuencia"],
    )


def _simulated_longitud() -> List[Dict[str, Any]]:
    return [
        {
            "clasificacion": c,
            "longitud_promedio": round(random.uniform(40, 180), 1),
        }
        for c in CATEGORIES
    ]


def _simulated_polarizacion() -> Dict[str, Any]:
    pol = random.randint(800, 1800)
    demo = random.randint(400, 900)

    return {
        "odio_politico": pol,
        "odio_demografico": demo,
        "ratio": round(pol / demo, 2) if demo else 0,
        "total_odio": pol + demo,
    }


def _simulated_top_palabras() -> List[Dict[str, Any]]:
    palabras = [
        "terruco",
        "voto",
        "fujimori",
        "caviar",
        "cholo",
        "elecciones",
        "congreso",
        "corrupt",
        "ladron",
        "peru",
        "presidente",
        "izquierda",
        "derecha",
        "serrano",
        "andino",
        "wasi",
    ]

    return sorted(
        [
            {
                "palabra": p,
                "frecuencia": random.randint(20, 500),
            }
            for p in palabras
        ],
        key=lambda x: -x["frecuencia"],
    )[:12]


def _simulated_metricas() -> Dict[str, Any]:
    return {
        "total_comentarios_enviados": 5847,
        "throughput_productor_msg_min": 60,
        "throughput_flink_msg_min": 58,
        "latencia_promedio_s": 1.3,
        "total_odio_politico": 1812,
        "total_odio_demografico": 1053,
        "total_odio_general": 1286,
        "total_neutral": 1696,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Real-data builders
# ─────────────────────────────────────────────────────────────────────────────

def _ensure_category_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensures the realtime dataframe has all expected category columns.
    """
    cols = [
        "ODIO_POLITICO",
        "ODIO_DEMOGRAFICO",
        "ODIO_GENERAL",
        "NEUTRAL",
    ]

    for col in cols:
        if col not in df.columns:
            df[col] = 0

        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    return df


def build_metricas_from_real_data(flink2_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Builds dashboard summary metrics from realtime classification rates.

    Uses:
      output/tiempo_real/job2_tasa/
    """
    if flink2_df.empty:
        print("[METRICAS] flink2_tasa vacío. Usando métricas simuladas.")
        return _simulated_metricas()

    flink2_df = _ensure_category_columns(flink2_df.copy())

    total_odio_politico = int(flink2_df["ODIO_POLITICO"].sum())
    total_odio_demografico = int(flink2_df["ODIO_DEMOGRAFICO"].sum())
    total_odio_general = int(flink2_df["ODIO_GENERAL"].sum())
    total_neutral = int(flink2_df["NEUTRAL"].sum())

    total = (
        total_odio_politico
        + total_odio_demografico
        + total_odio_general
        + total_neutral
    )

    # Basic throughput approximation from realtime windows
    windows_count = len(flink2_df)
    throughput = round(total / windows_count, 2) if windows_count else 0

    print(
        "[METRICAS] Reales desde S3 | "
        f"total={total}, politico={total_odio_politico}, "
        f"demo={total_odio_demografico}, general={total_odio_general}, "
        f"neutral={total_neutral}"
    )

    return {
        "total_comentarios_enviados": total,
        "throughput_productor_msg_min": throughput,
        "throughput_flink_msg_min": throughput,
        "latencia_promedio_s": 0,
        "total_odio_politico": total_odio_politico,
        "total_odio_demografico": total_odio_demografico,
        "total_odio_general": total_odio_general,
        "total_neutral": total_neutral,
    }


def build_distribucion_from_realtime(flink2_df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Builds historical distribution from realtime data when Spark historical
    outputs are not available yet.
    """
    if flink2_df.empty:
        print("[SPARK1] flink2_tasa vacío. Usando distribución simulada.")
        return _simulated_distribucion()

    flink2_df = _ensure_category_columns(flink2_df.copy())

    return [
        {
            "clasificacion": "ODIO_POLITICO",
            "count": int(flink2_df["ODIO_POLITICO"].sum()),
        },
        {
            "clasificacion": "ODIO_DEMOGRAFICO",
            "count": int(flink2_df["ODIO_DEMOGRAFICO"].sum()),
        },
        {
            "clasificacion": "ODIO_GENERAL",
            "count": int(flink2_df["ODIO_GENERAL"].sum()),
        },
        {
            "clasificacion": "NEUTRAL",
            "count": int(flink2_df["NEUTRAL"].sum()),
        },
    ]


def build_polarizacion_from_realtime(flink2_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Builds polarization indicator from realtime data if Spark job4 is missing.
    """
    if flink2_df.empty:
        return _simulated_polarizacion()

    flink2_df = _ensure_category_columns(flink2_df.copy())

    odio_politico = int(flink2_df["ODIO_POLITICO"].sum())
    odio_demografico = int(flink2_df["ODIO_DEMOGRAFICO"].sum())
    total_odio = odio_politico + odio_demografico

    ratio = round(odio_politico / odio_demografico, 2) if odio_demografico else 0

    return {
        "odio_politico": odio_politico,
        "odio_demografico": odio_demografico,
        "ratio": ratio,
        "total_odio": total_odio,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Public loader
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=30)
def load_all_data() -> Dict[str, Any]:
    """
    Tries S3 → local files → simulated data.
    Returns a unified dict consumed by all pages.
    """

    def get(s3_key: str, local_file: str, sim_fn):
        d = _read_s3_json(S3_PATHS[s3_key])

        if d:
            print(f"[DATA_LOADER] {s3_key}: usando S3")
            return d, "s3"

        d = _read_local_json(local_file)

        if d:
            print(f"[DATA_LOADER] {s3_key}: usando LOCAL")
            return d, "local"

        print(f"[DATA_LOADER] {s3_key}: usando SIMULADO")
        return sim_fn(), "simulated"

    # Realtime outputs
    flink1, src1 = get(
        "job_flink1_frecuencia",
        "flink1_frecuencia.json",
        _simulated_frecuencia,
    )

    flink2, src2 = get(
        "job_flink2_tasa",
        "flink2_tasa.json",
        _simulated_tasa,
    )

    flink3, src3 = get(
        "job_flink3_alertas",
        "flink3_alertas.json",
        _simulated_alertas,
    )

    flink4, src4 = get(
        "job_flink4_top_videos",
        "flink4_top_videos.json",
        _simulated_top_videos,
    )

    flink5, src5 = get(
        "job_flink5_trolls",
        "flink5_trolls.json",
        _simulated_trolls,
    )

    flink1_df = pd.DataFrame(flink1)
    flink2_df = pd.DataFrame(flink2)
    flink3_df = pd.DataFrame(flink3)
    flink4_df = pd.DataFrame(flink4)
    flink5_df = pd.DataFrame(flink5)

    # Historical outputs
    spark1, src_spark1 = get(
        "job_spark1_distribucion",
        "spark1_distribucion.json",
        _simulated_distribucion,
    )

    spark2, src_spark2 = get(
        "job_spark2_jerguometro",
        "spark2_jerguometro.json",
        _simulated_jerguometro,
    )

    spark3, src_spark3 = get(
        "job_spark3_longitud",
        "spark3_longitud.json",
        _simulated_longitud,
    )

    # If Spark historical distribution does not exist yet,
    # derive it from realtime S3 data.
    if src_spark1 == "simulated" and src2 == "s3":
        print("[DATA_LOADER] spark1_distribucion: construido desde realtime S3")
        spark1 = build_distribucion_from_realtime(flink2_df)
        src_spark1 = "s3_realtime_derived"

    # Polarization can be read from Spark or derived from realtime
    pol = _read_s3_json(S3_PATHS["job_spark4_polarizacion"])

    if pol:
        print("[DATA_LOADER] job_spark4_polarizacion: usando S3")
        spark4 = pol[0] if isinstance(pol, list) else pol
        src_spark4 = "s3"
    elif src2 == "s3":
        print("[DATA_LOADER] spark4_polarizacion: construido desde realtime S3")
        spark4 = build_polarizacion_from_realtime(flink2_df)
        src_spark4 = "s3_realtime_derived"
    else:
        print("[DATA_LOADER] job_spark4_polarizacion: usando SIMULADO")
        spark4 = _simulated_polarizacion()
        src_spark4 = "simulated"

    spark5, src_spark5 = get(
        "job_spark5_top_palabras",
        "spark5_top_palabras.json",
        _simulated_top_palabras,
    )

    # Metrics now come from real realtime data when available
    if src2 == "s3":
        metricas = build_metricas_from_real_data(flink2_df)
    else:
        print("[METRICAS] No hay job2_tasa en S3. Usando métricas simuladas.")
        metricas = _simulated_metricas()

    real_sources = [
        src1,
        src2,
        src3,
        src4,
        src5,
        src_spark1,
        src_spark2,
        src_spark3,
        src_spark4,
        src_spark5,
    ]

    if "s3" in real_sources or "s3_realtime_derived" in real_sources:
        source = "s3"
    elif "local" in real_sources:
        source = "local"
    else:
        source = "simulated"

    print(f"[DATA_LOADER] Fuente global del dashboard: {source}")

    return {
        "source": source,
        "flink1_frecuencia": flink1_df,
        "flink2_tasa": flink2_df,
        "flink3_alertas": flink3_df,
        "flink4_top_videos": flink4_df,
        "flink5_trolls": flink5_df,
        "spark1_distribucion": pd.DataFrame(spark1),
        "spark2_jerguometro": pd.DataFrame(spark2),
        "spark3_longitud": pd.DataFrame(spark3),
        "spark4_polarizacion": spark4,
        "spark5_top_palabras": pd.DataFrame(spark5),
        "metricas": metricas,
        "last_updated": datetime.now().strftime("%H:%M:%S"),
    }