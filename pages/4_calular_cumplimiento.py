"""
Cumplimiento por Modelo · Basado en Rúbrica MBE (valores brutos)
Selector de Excel · 8 modelos · Tabla ordenada + clasificación visual
"""

import warnings
from pathlib import Path
import pandas as pd
import streamlit as st

warnings.filterwarnings("ignore")

# ====================================================================
# CONFIGURACIÓN
# ====================================================================
st.set_page_config(
    page_title="Cumplimiento por Modelo · MBE",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent.parent

# ====================================================================
# CONSTANTES
# ====================================================================
ARCHIVOS = {
    "YouTube": {"archivo": "youtube.xlsx", "icono": "▶️", "clave_ss": "df_youtube"},
    "Clopa": {"archivo": "clopa.xlsx", "icono": "🎓", "clave_ss": "df_clopa"},
    "Altos y Bajos": {
        "archivo": "altosybajos.xlsx",
        "icono": "📈",
        "clave_ss": "df_altosybajos",
    },
}

ORDEN_NIVELES = ["Deficiente", "Bajo", "Promedio", "Alto", "Sobresaliente"]

COLORES_NIVEL = {
    "Deficiente": "#dc2626",
    "Bajo": "#f97316",
    "Promedio": "#eab308",
    "Alto": "#22c55e",
    "Sobresaliente": "#15803d",
}

FONDOS_NIVEL = {
    "Deficiente": "linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)",
    "Bajo": "linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%)",
    "Promedio": "linear-gradient(135deg, #fefce8 0%, #fef9c3 100%)",
    "Alto": "linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)",
    "Sobresaliente": "linear-gradient(135deg, #f0fdf4 0%, #bbf7d0 100%)",
}

ICONOS_NIVEL = {
    "Deficiente": "❌",
    "Bajo": "⚠️",
    "Promedio": "🟡",
    "Alto": "✅",
    "Sobresaliente": "⭐",
}

MODELOS = {
    "M0": {
        "codigo": "M0",
        "nombre": "CMP Individual / Cortes",
        "metrica": "CPM",
        "icono": "🎬",
        "col_valor": "CPM",
        "direccion": "mayor_mejor",
        "clasificar": lambda v: (
            "Deficiente"
            if v <= 0.10
            else (
                "Bajo"
                if v <= 0.14
                else (
                    "Promedio"
                    if v <= 0.25
                    else "Alto" if v <= 0.50 else "Sobresaliente"
                )
            )
        ),
        "rangos": {
            "Deficiente": "CPM ≤ 0.10",
            "Bajo": "0.10 < CPM ≤ 0.14",
            "Promedio": "0.14 < CPM ≤ 0.25",
            "Alto": "0.25 < CPM ≤ 0.50",
            "Sobresaliente": "CPM > 0.50",
        },
        "explicaciones": {
            "Deficiente": "La clase es una foto fija. El docente casi no cambia de plano ni de apoyo visual.",
            "Bajo": "Casi no hay movimiento visual. El apoyo gráfico es escaso.",
            "Promedio": "Hay cambios, pero espaciados. La clase tiene momentos de dinamismo y momentos planos.",
            "Alto": "El docente cambia de plano con frecuencia. La clase se siente ágil y dinámica.",
            "Sobresaliente": "El ritmo visual es constante. Cada pocos segundos hay un cambio que reactiva la atención.",
        },
        "sustento": {
            "Deficiente": "Sin variación visual, el estudiante pierde el anclaje atencional.",
            "Bajo": "La falta de estimulación fragmentada reduce el foco atencional.",
            "Promedio": "Variación moderada mantiene ritmo visual aceptable.",
            "Alto": "El cambio visual evita la habituación y reactiva la corteza visual.",
            "Sobresaliente": "Estimulación visual continua maximiza el engagement (Barsalou, 2008).",
        },
    },
    "M1": {
        "codigo": "M1",
        "nombre": "Control del Monólogo",
        "metrica": "DME_s",
        "icono": "🎙️",
        "col_valor": "DME_s",
        "direccion": "menor_mejor",
        "clasificar": lambda v: (
            "Deficiente"
            if v >= 600
            else (
                "Bajo"
                if v >= 420
                else "Promedio" if v >= 240 else "Alto" if v >= 120 else "Sobresaliente"
            )
        ),
        "rangos": {
            "Deficiente": "DME ≥ 600 s",
            "Bajo": "420 s ≤ DME < 600 s",
            "Promedio": "240 s ≤ DME < 420 s",
            "Alto": "120 s ≤ DME < 240 s",
            "Sobresaliente": "DME < 120 s",
        },
        "explicaciones": {
            "Deficiente": "El docente habla sin parar más de 10 minutos. El estudiante queda como espectador pasivo.",
            "Bajo": "Los monólogos son largos. Las pausas son muy escasas.",
            "Promedio": "Explicaciones de 4 a 7 minutos. Hay pausas, pero podrían ser más frecuentes.",
            "Alto": "El docente hace pausas frecuentes. La clase tiene ritmo conversacional.",
            "Sobresaliente": "Fragmentación total. La clase es un diálogo, no un monólogo.",
        },
        "sustento": {
            "Deficiente": "Tramos >600 s inducen acomodación pasiva (Flanders, 1970).",
            "Bajo": "Sin pausas, la memoria de trabajo no consolida (Vygotsky, 1978).",
            "Promedio": "Rango típico de clase expositiva. Aceptable, no óptimo.",
            "Alto": "Pausas cada 2-4 min permiten asimilación y preguntas.",
            "Sobresaliente": "Alta fragmentación = máxima interacción (Vygotsky, 1978).",
        },
    },
    "M2": {
        "codigo": "M2",
        "nombre": "Nivel de Interacción",
        "metrica": "DTE_ratio",
        "icono": "🤝",
        "col_valor": "DTE_Docente_ratio",
        "direccion": "centro_mejor",
        "clasificar": lambda v: (
            "Deficiente"
            if (v < 0.10 or v > 0.90)
            else (
                "Bajo"
                if (v < 0.20 or v > 0.80)
                else (
                    "Promedio"
                    if (v < 0.40 or v > 0.70)
                    else "Alto" if (v < 0.50 or v > 0.60) else "Sobresaliente"
                )
            )
        ),
        "rangos": {
            "Deficiente": "DTE < 0.10 ó > 0.90",
            "Bajo": "0.10–0.20 ó 0.80–0.90",
            "Promedio": "0.20–0.40 ó 0.70–0.80",
            "Alto": "0.40–0.50 ó 0.60–0.70",
            "Sobresaliente": "0.50 ≤ DTE ≤ 0.60",
        },
        "explicaciones": {
            "Deficiente": "O el docente no habla, o habla el 90% del tiempo. No hay equilibrio.",
            "Bajo": "Uso muy escaso de la voz o monólogo dominante. Falta espacio para el estudiante.",
            "Promedio": "Interacción moderada. Es una clase estándar, funcional pero no óptima.",
            "Alto": "Buen equilibrio. El docente expone y deja espacio para los estudiantes.",
            "Sobresaliente": "Equilibrio perfecto. Docente y estudiantes comparten el canal de voz.",
        },
        "sustento": {
            "Deficiente": "Los extremos eliminan la co-construcción (Vygotsky, 1978).",
            "Bajo": "El desequilibrio impide el diálogo socrático.",
            "Promedio": "Hay intercambio, pero no el equilibrio óptimo.",
            "Alto": "Ratio 0.40-0.50 permite alternancia guía-participación.",
            "Sobresaliente": "Ratio 0.50-0.60 es el punto óptimo de diálogo (Vygotsky, 1978).",
        },
    },
    "M3": {
        "codigo": "M3",
        "nombre": "Estabilidad Técnica",
        "metrica": "Jitter_Score",
        "icono": "💻",
        "col_valor": "Jitter_Score",
        "direccion": "mayor_mejor",
        "clasificar": lambda v: (
            "Deficiente"
            if v < 0.30
            else (
                "Bajo"
                if v < 0.50
                else "Promedio" if v < 0.75 else "Alto" if v < 0.90 else "Sobresaliente"
            )
        ),
        "rangos": {
            "Deficiente": "Jitter < 0.30",
            "Bajo": "0.30 ≤ Jitter < 0.50",
            "Promedio": "0.50 ≤ Jitter < 0.75",
            "Alto": "0.75 ≤ Jitter < 0.90",
            "Sobresaliente": "Jitter ≥ 0.90",
        },
        "explicaciones": {
            "Deficiente": "La transmisión se congela constantemente. Es imposible seguir la clase.",
            "Bajo": "Hay cortes frecuentes de video/audio. La clase se interrumpe todo el tiempo.",
            "Promedio": "Algunas micro-pausas de red. Molestan, pero no arruinan la clase.",
            "Alto": "Transmisión fluida. Muy pocas variaciones.",
            "Sobresaliente": "Transmisión perfecta. Cero interrupciones.",
        },
        "sustento": {
            "Deficiente": "Congelamientos impiden procesar el contenido (Sweller, 1988).",
            "Bajo": "La carga extraña consume recursos del aprendizaje.",
            "Promedio": "Carga extraña manejable, aunque no ideal.",
            "Alto": "Estabilidad permite enfocar atención al contenido.",
            "Sobresaliente": "Carga extraña nula: todo va al aprendizaje (Sweller, 1988).",
        },
    },
    "M4": {
        "codigo": "M4",
        "nombre": "Modulación y Expresividad",
        "metrica": "Tone_CoV",
        "icono": "🗣️",
        "col_valor": "Tone_CoV",
        "direccion": "mayor_mejor",
        "clasificar": lambda v: (
            "Deficiente"
            if v < 0.06
            else (
                "Bajo"
                if v < 0.12
                else "Promedio" if v < 0.18 else "Alto" if v < 0.25 else "Sobresaliente"
            )
        ),
        "rangos": {
            "Deficiente": "Tone_CoV < 0.06",
            "Bajo": "0.06 ≤ Tone_CoV < 0.12",
            "Promedio": "0.12 ≤ Tone_CoV < 0.18",
            "Alto": "0.18 ≤ Tone_CoV < 0.25",
            "Sobresaliente": "Tone_CoV ≥ 0.25",
        },
        "explicaciones": {
            "Deficiente": "La voz es plana, robótica, como si leyera un teleprónter.",
            "Bajo": "Poca modulación. La voz es monótona la mayor parte del tiempo.",
            "Promedio": "Modulación estándar. Como una conversación normal.",
            "Alto": "Voz expresiva. El docente usa énfasis pedagógico.",
            "Sobresaliente": "Riqueza tonal excepcional. La voz es un instrumento pedagógico.",
        },
        "sustento": {
            "Deficiente": "La monotonía induce fatiga auditiva y el cerebro filtra.",
            "Bajo": "El sistema atencional (SARA) se desactiva ante previsibilidad.",
            "Promedio": "Variación suficiente para atención básica.",
            "Alto": "Las inflexiones reactivan la atención (Scherer, 2003).",
            "Sobresaliente": "Máxima variación = máxima reactivación (Scherer, 2003).",
        },
    },
    "M5": {
        "codigo": "M5",
        "nombre": "Presencia Corporal",
        "metrica": "IMP_promedio",
        "icono": "🧍",
        "col_valor": "IMP_promedio",
        "direccion": "mayor_mejor",
        "clasificar": lambda v: (
            "Deficiente"
            if v < 0.001
            else (
                "Bajo"
                if v < 0.005
                else (
                    "Promedio"
                    if v < 0.020
                    else "Alto" if v < 0.050 else "Sobresaliente"
                )
            )
        ),
        "rangos": {
            "Deficiente": "IMP < 0.001",
            "Bajo": "0.001 ≤ IMP < 0.005",
            "Promedio": "0.010 ≤ IMP < 0.020",
            "Alto": "0.020 ≤ IMP < 0.050",
            "Sobresaliente": "IMP ≥ 0.050",
        },
        "explicaciones": {
            "Deficiente": "El docente está inmóvil. Es una estatua frente a la cámara.",
            "Bajo": "Postura rígida. Casi no hay gestos.",
            "Promedio": "Gesticulación natural de soporte. El docente se mueve lo justo.",
            "Alto": "Presencia corporal activa. El docente usa manos y cuerpo para explicar.",
            "Sobresaliente": "Alto despliegue físico. El docente habita el espacio y comunica con el cuerpo.",
        },
        "sustento": {
            "Deficiente": "Sin movimiento, se pierde el anclaje visual de conceptos.",
            "Bajo": "La falta de gestos reduce comprensión de abstractos (Barsalou, 2008).",
            "Promedio": "El movimiento acompaña el habla de forma funcional.",
            "Alto": "La cognición corporizada facilita la comprensión.",
            "Sobresaliente": "Máxima expresión de cognición encarnada (Barsalou, 2008).",
        },
    },
    "M6": {
        "codigo": "M6",
        "nombre": "Energía y Proyección",
        "metrica": "Enthusiasm_Score",
        "icono": "🔥",
        "col_valor": "Enthusiasm_Score",
        "direccion": "mayor_mejor",
        "clasificar": lambda v: (
            "Deficiente"
            if v < 0.01
            else (
                "Bajo"
                if v < 0.03
                else "Promedio" if v < 0.08 else "Alto" if v < 0.15 else "Sobresaliente"
            )
        ),
        "rangos": {
            "Deficiente": "Enthusiasm < 0.01",
            "Bajo": "0.01 ≤ Enthusiasm < 0.03",
            "Promedio": "0.03 ≤ Enthusiasm < 0.08",
            "Alto": "0.08 ≤ Enthusiasm < 0.15",
            "Sobresaliente": "Enthusiasm ≥ 0.15",
        },
        "explicaciones": {
            "Deficiente": "La voz es un murmullo. El docente habla para sí mismo.",
            "Bajo": "Proyección baja. El tono es apagado, sin energía.",
            "Promedio": "Volumen estándar. Se escucha bien, pero sin chispa.",
            "Alto": "Proyección firme y clara. El docente transmite seguridad.",
            "Sobresaliente": "Voz potente y entusiasmada. El docente contagia energía.",
        },
        "sustento": {
            "Deficiente": "Sin proyección, no llega el estímulo acústico.",
            "Bajo": "Falta de energía vocal reduce motivación intrínseca.",
            "Promedio": "Energía funcional, pero no inspiradora.",
            "Alto": "Voz enérgica activa el sistema límbico.",
            "Sobresaliente": "El entusiasmo estimula motivación (Immordino-Yang & Damasio, 2007).",
        },
    },
    "M7": {
        "codigo": "M7",
        "nombre": "Dinamismo y Ritmo",
        "metrica": "sigma2_IM",
        "icono": "🔄",
        "col_valor": "sigma2_IM",
        "direccion": "mayor_mejor",
        "clasificar": lambda v: (
            "Deficiente"
            if v < 0.000
            else (
                "Bajo"
                if v < 0.03
                else "Promedio" if v < 0.10 else "Alto" if v < 0.25 else "Sobresaliente"
            )
        ),
        "rangos": {
            "Deficiente": "sigma2_IM < 0.000",
            "Bajo": "0.008 ≤ sigma2_IM < 0.03",
            "Promedio": "0.03 ≤ sigma2_IM < 0.10",
            "Alto": "0.10 ≤ sigma2_IM < 0.25",
            "Sobresaliente": "sigma2_IM ≥ 0.25",
        },
        "explicaciones": {
            "Deficiente": "Ritmo plano. El docente no alterna movimiento y pausa.",
            "Bajo": "Movimiento repetitivo o con tics. Poca alternancia.",
            "Promedio": "Alternancia regular. El docente alterna calma y gestos.",
            "Alto": "Uso estratégico de pausas y énfasis físico.",
            "Sobresaliente": "Gran versatilidad rítmica. El cuerpo del docente es dinámico y expresivo.",
        },
        "sustento": {
            "Deficiente": "Sin variación, la atención se habitúa (Barsalou, 2008).",
            "Bajo": "La falta de variación rítmica reduce engagement.",
            "Promedio": "El ritmo corporal mantiene atención aceptable.",
            "Alto": "Alternancia intencional mantiene el foco.",
            "Sobresaliente": "Máxima variación = potente anclaje atencional (Barsalou, 2008).",
        },
    },
}


# ====================================================================
# UTILIDADES
# ====================================================================
def cargar_estilos():
    """Lee estilos.css y lo inyecta en la página."""
    ruta_css = BASE_DIR / "estilos.css"
    if ruta_css.exists():
        with open(ruta_css, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ No se encontró `estilos.css` en: `{ruta_css}`")


@st.cache_data(show_spinner=False)
def cargar_excel(nombre_archivo: str):
    """Carga un Excel desde session_state o desde disco."""
    clave_ss_map = {
        "youtube.xlsx": "df_youtube",
        "clopa.xlsx": "df_clopa",
        "altosybajos.xlsx": "df_altosybajos",
    }
    clave_ss = clave_ss_map.get(nombre_archivo)

    if clave_ss:
        df_ss = st.session_state.get(clave_ss)
        if df_ss is not None and isinstance(df_ss, pd.DataFrame):
            return df_ss, None

    ruta = BASE_DIR / nombre_archivo
    if not ruta.exists():
        return None, f"No se encontró `{nombre_archivo}` en `{BASE_DIR}`"

    try:
        df = pd.read_excel(ruta)
        if clave_ss:
            st.session_state[clave_ss] = df
        return df, None
    except Exception as e:
        return None, f"Error al leer `{nombre_archivo}`: {str(e)}"


def ordenar_por_optimo(
    sub: pd.DataFrame, direccion: str, col_valor: str
) -> pd.DataFrame:
    """Ordena los videos de mejor a peor según la dirección del óptimo."""
    if direccion == "mayor_mejor":
        sub = sub.sort_values(col_valor, ascending=False).reset_index(drop=True)
    elif direccion == "menor_mejor":
        sub = sub.sort_values(col_valor, ascending=True).reset_index(drop=True)
    elif direccion == "centro_mejor":
        sub["_dist_optimo"] = (sub[col_valor] - 0.55).abs()
        sub = sub.sort_values("_dist_optimo", ascending=True).reset_index(drop=True)
        sub = sub.drop(columns=["_dist_optimo"])
    return sub


def colorear_nivel(valor_nivel: str) -> str:
    """Estilo CSS para pintar la celda de nivel en la tabla."""
    color = COLORES_NIVEL.get(valor_nivel, "#6b7280")
    return f"background-color: {color}; color: white; font-weight: 700; text-align: center;"


# ====================================================================
# BLOQUES DE RENDERIZADO
# ====================================================================
def bloque_banner():
    """Banner principal de la página."""
    st.markdown(
        """
    <div class="banner-mbe">
        <h1>📊 Cumplimiento por Modelo</h1>
        <p>Clasificación según Rúbrica MBE · Basada en valores brutos · 8 modelos analíticos</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def bloque_selector():
    """Selector de Excel y carga de datos. Devuelve (df, nombre_archivo)."""
    opciones = list(ARCHIVOS.keys())
    etiquetas = [f"{ARCHIVOS[o]['icono']} {o}" for o in opciones]

    seleccion = st.radio(
        "**Selecciona el archivo:**",
        options=etiquetas,
        horizontal=True,
    )

    idx = etiquetas.index(seleccion)
    nombre_archivo = ARCHIVOS[opciones[idx]]["archivo"]

    df, error = cargar_excel(nombre_archivo)

    if df is None:
        st.error(f"❌ {error}")
        return None, nombre_archivo

    st.caption(f"📁 {len(df)} videos cargados desde `{nombre_archivo}`")

    if "Video_ID" not in df.columns:
        st.error("❌ El Excel no tiene la columna `Video_ID`.")
        return None, nombre_archivo

    return df, nombre_archivo


def bloque_banner_modelo(codigo: str, info: dict, total: int):
    """Banner verde por modelo."""
    st.markdown(
        f"""
    <div class="banner-modelo">
        <h3>{info['icono']} {codigo} · {info['nombre']}</h3>
        <p>Métrica: <strong>{info['metrica']}</strong> · {total} videos analizados</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def bloque_tabla(sub: pd.DataFrame, info: dict):
    """Tabla con los videos ordenados por valor bruto."""
    st.markdown(f"##### 📋 Videos ordenados por {info['metrica']} (mejor → peor)")

    tabla = sub.copy().rename(
        columns={
            "Video_ID": "Video",
            info["col_valor"]: info["metrica"],
        }
    )
    if info["metrica"] in tabla.columns:
        tabla[info["metrica"]] = tabla[info["metrica"]].round(4)

    styled = tabla.style.map(colorear_nivel, subset=["Nivel"])

    st.dataframe(
        styled,
        use_container_width=True,
        hide_index=True,
        height=min(400, 40 + 35 * len(tabla)),
    )


def bloque_cards_niveles(sub: pd.DataFrame, info: dict, codigo: str):
    """5 cards carnosas con la clasificación por nivel."""
    st.markdown(f"#### 🎯 Clasificación final por rangos ({codigo})")
    st.caption(
        "Cada tarjeta muestra qué significa el nivel, el rango numérico exacto y cuántos videos cayeron ahí."
    )

    cols = st.columns(5)
    for i, nivel in enumerate(ORDEN_NIVELES):
        videos_nivel = sub[sub["Nivel"] == nivel]
        count = len(videos_nivel)
        color = COLORES_NIVEL[nivel]
        fondo = FONDOS_NIVEL[nivel]
        icono = ICONOS_NIVEL[nivel]
        rango = info["rangos"][nivel]
        explicacion = info["explicaciones"][nivel]
        sustento = info["sustento"][nivel]

        with cols[i]:
            st.markdown(
                f"""
            <div class="nivel-card" style="background:{fondo}; border-color:{color};">
                <div class="icono-nivel">{icono}</div>
                <div class="nombre-nivel" style="color:{color};">{nivel}</div>
                <div class="rango">{rango}</div>
                <div class="explicacion">💬 {explicacion}</div>
                <div class="sustento">🧠 {sustento}</div>
                <div class="conteo">🎬 {count} {('video' if count == 1 else 'videos')}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            if count > 0:
                with st.expander(f"Ver {count} video(s)"):
                    for v in videos_nivel["Video_ID"].tolist():
                        st.markdown(f"- {v}")
            else:
                st.caption("Sin videos en este rango.")


def renderizar_modelo(codigo: str, info: dict, df: pd.DataFrame):
    """Orquesta los bloques de un modelo específico."""
    col_valor = info["col_valor"]

    if col_valor not in df.columns:
        st.warning(f"⚠️ **{codigo}** · Falta la columna `{col_valor}` en este Excel.")
        return

    if "Video_ID" not in df.columns:
        st.warning(f"⚠️ **{codigo}** · Falta la columna `Video_ID`.")
        return

    sub = df[["Video_ID", col_valor]].copy()
    sub[col_valor] = pd.to_numeric(sub[col_valor], errors="coerce")
    sub = sub.dropna(subset=[col_valor]).reset_index(drop=True)

    if sub.empty:
        st.info(f"Sin datos válidos para **{codigo}**.")
        return

    sub["Nivel"] = sub[col_valor].apply(info["clasificar"])
    sub = ordenar_por_optimo(sub, info["direccion"], col_valor)

    bloque_banner_modelo(codigo, info, len(sub))
    bloque_tabla(sub, info)
    bloque_cards_niveles(sub, info, codigo)
    st.divider()


def bloque_modelos(df: pd.DataFrame):
    """Itera los 8 modelos y los renderiza uno debajo del otro."""
    for codigo, info in MODELOS.items():
        renderizar_modelo(codigo, info, df)


def bloque_footer():
    st.markdown(
        """
    <div style="text-align:center; color:#6b7280; font-size:0.82rem; padding:20px 0;">
        <strong>Modelo Bidireccional de Evaluación (MBE)</strong> · Cumplimiento por Modelo<br>
        Clasificación según Tabla Maestra de 5 Niveles · Valores brutos por rúbrica<br><br>
        © 2026 CUN - Corporación Unificada Nacional de Educación Superior
    </div>
    """,
        unsafe_allow_html=True,
    )


# ====================================================================
# MAIN
# ====================================================================
def main():
    cargar_estilos()
    bloque_banner()

    df, _ = bloque_selector()
    if df is None:
        st.stop()

    bloque_modelos(df)

    st.divider()
    bloque_footer()


main()
