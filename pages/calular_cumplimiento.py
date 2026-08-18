# calcular_cumplimiento.py
import numpy as np
import pandas as pd

# Reglas y metas por cada métrica
METRICAS_CONFIG = {
    "DME_s": {"limite": 3.5, "condicion": "menor"},
    "Tone_CoV": {"limite": 0.32, "condicion": "mayor"},
    "Enthusiasm_Score": {"limite": 0.15, "condicion": "mayor"},
    "DTE_ratio": {"limite": 0.5, "condicion": "menor_igual"},
    "IMP_promedio": {"limite": 4.0, "condicion": "mayor"},
    "sigma2_IM": {"limite": 8.5, "condicion": "mayor"},
    "Jitter_Score": {"limite": 0.4, "condicion": "mayor"},
}


def calcular_cumplimiento_df(df, config=METRICAS_CONFIG):
    """Aplica el cálculo de cumplimiento a todas las filas y columnas del DataFrame."""
    df_resultado = df.copy()

    for metrica, cfg in config.items():
        if metrica in df_resultado.columns:
            limite = cfg["limite"]
            condicion = cfg["condicion"]

            # 1. Convierte a numérico
            s = pd.to_numeric(df_resultado[metrica], errors="coerce")

            # 2. Ceros pasan a NaN (fallo técnico / dato no medido)
            s = s.replace(0, np.nan)

            # 3. Cálculo de cumplimiento según condición
            if condicion in ["mayor", "mayor_igual"]:
                pct = (s / limite) * 100.0

            elif condicion in ["menor", "menor_igual"]:
                pct = (1.0 - (s / limite)) * 100.0

            else:
                pct = np.nan

            # 4. Acotar entre 0.0% y 100.0%
            df_resultado[f"{metrica}_cumplimiento"] = np.clip(pct, 0.0, 100.0)

    return df_resultado


def calcular_cumplimiento(valor, columna, config=METRICAS_CONFIG):
    """Mantiene compatibilidad para evaluar un único valor si alguna función antigua lo requiere."""
    if pd.isna(valor) or columna not in config:
        return np.nan

    try:
        val = float(str(valor).replace(",", "."))
    except (ValueError, TypeError):
        return np.nan

    if val == 0:
        return np.nan

    cfg = config[columna]
    limite = cfg["limite"]
    condicion = cfg["condicion"]

    if condicion in ["mayor", "mayor_igual"]:
        pct = (val / limite) * 100.0
    elif condicion in ["menor", "menor_igual"]:
        pct = (1.0 - (val / limite)) * 100.0
    else:
        return np.nan

    return float(np.clip(pct, 0.0, 100.0))
