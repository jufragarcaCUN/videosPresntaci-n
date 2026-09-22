"""
Rúbrica Modelo Dos · Modelo Bidireccional de Evaluación (MBE)
Segmentación por bloques de 15 minutos · 8 Modelos Analíticos · Escala T
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
    page_title="Rúbrica Modelo Dos · MBE",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# El CSS está en la MISMA carpeta que este archivo (pages/)
BASE_DIR = Path(__file__).resolve().parent


# ====================================================================
# CONSTANTES: MODELOS M0 - M7
# ====================================================================
MODELOS_INFO = {
    "M0": {
        "codigo": "M0",
        "nombre": "CMP Individual / Cortes",
        "metrica": "CPM",
        "icono": "🎬",
        "categoria": "Video / Edición",
        "peso": 0.125,
        "que_hace": "Mide la tasa de variación y cortes de plano por minuto (CPM) o el Comportamiento Multimodal Ponderado (CMP) individual.",
        "como_lo_hace": "Analiza las transiciones y cortes de escena en la señal de video usando detectores de contenido visual en ventanas de tiempo.",
        "para_que": "Evaluar el ritmo de edición/cambio de plano o contar con un diagnóstico atomizado de la dinámica del canal de entrada.",
        "que_obtiene": "Un valor de cortes por minuto (CPM) acotado en [0.00, 5.00].",
        "que_significa": "Muestra la frecuencia con la que cambia el estímulo visual o la estabilidad/variación aislada en la dimensión.",
        "escenario_contraste": "Una clase con cambios dinámicos de toma o apoyo visual frente a una toma fija e inalterada durante toda la sesión.",
        "evaluacion_15min": "Mide la densidad de cambios de plano y la contribución individual dentro del bloque de 900 segundos.",
        "lectura": "Permite evaluar la tasa de fragmentación y dinamización visual, detectando si la presentación se mantiene en una sola toma estática o si tiene dinamismo de encuadre.",
        "niveles": {
            "Deficiente": {
                "rango": "CPM ≤ 0.10",
                "desc": "Toma fija estática; sin cambios en el bloque",
            },
            "Bajo": {
                "rango": "0.10 < CPM ≤ 0.14",
                "desc": "Plano casi inalterado; apoyo escaso",
            },
            "Promedio": {
                "rango": "0.14 < CPM ≤ 0.25",
                "desc": "Transiciones moderadas cada 4–7 min",
            },
            "Alto": {
                "rango": "0.25 < CPM ≤ 0.50",
                "desc": "Ritmo ágil; pausas y cambios frecuentes",
            },
            "Sobresaliente": {
                "rango": "CPM > 0.50",
                "desc": "Ritmo de edición ágil; dinamismo constante",
            },
        },
    },
    "M1": {
        "codigo": "M1",
        "nombre": "Control del Monólogo",
        "metrica": "DME_s",
        "icono": "🎙️",
        "categoria": "Audio / Interacción",
        "peso": 0.125,
        "que_hace": "Mide la duración media de los episodios continuos (DME en segundos) o tramos sin pausas del discurso.",
        "como_lo_hace": "Calcula el tiempo continuo promedio entre transiciones/pausas en la línea temporal del bloque.",
        "para_que": "Identificar si el docente realiza pausas pedagógicas estructuradas o si incurre en monólogos extensos que desgasten la atención del estudiante.",
        "que_obtiene": "Un valor numérico continuo expresado en segundos (s) acotado en [0.0, 900.0].",
        "que_significa": "Un valor bajo indica pausas frecuentes para dar espacio a la asimilación e interacción; un valor alto refleja un monólogo denso y continuo.",
        "escenario_contraste": "Un docente con tramos continuos de 10 minutos sin pausas versus un docente con intervenciones cortas y segmentadas.",
        "evaluacion_15min": "Mide la densidad de fragmentación del discurso y la distribución de las explicaciones en unidades manejables.",
        "lectura": "Si el bloque registra un tramo de ≥ 600 s, la carga cognitiva es crítica; si registra tramos de < 120 s, el sesgo de monólogo cae drásticamente.",
        "niveles": {
            "Deficiente": {
                "rango": "DME ≥ 600 s",
                "desc": "Monólogo denso sin pausas; > 10 min seguidos",
            },
            "Bajo": {
                "rango": "420 s ≤ DME < 600 s",
                "desc": "Monólogos largos; pausas muy escasas",
            },
            "Promedio": {
                "rango": "240 s ≤ DME < 420 s",
                "desc": "Explicaciones continuas de 4–7 min",
            },
            "Alto": {
                "rango": "120 s ≤ DME < 240 s",
                "desc": "Ritmo ágil; pausas frecuentes",
            },
            "Sobresaliente": {
                "rango": "DME < 120 s",
                "desc": "Alta fragmentación pedagógica y dinamismo",
            },
        },
    },
    "M2": {
        "codigo": "M2",
        "nombre": "Nivel de Interacción",
        "metrica": "DTE_ratio",
        "icono": "🤝",
        "categoria": "Audio / Diarización",
        "peso": 0.125,
        "que_hace": "Mide la proporción de ocupación activa del canal de voz por parte del docente respecto al tiempo total disponible en el bloque de 15 minutos (900 segundos).",
        "como_lo_hace": "Mediante el análisis del canal de audio con Silero VAD, contabiliza milisegundo a milisegundo el tiempo real de habla del docente dentro del intervalo de 900 segundos.",
        "para_que": "Evaluar el equilibrio entre la exposición oral del docente y los espacios destinados a pausas de asimilación, preguntas, actividades o intervenciones de los estudiantes.",
        "que_obtiene": "Un valor numérico continuo (ratio) acotado en un rango de 0.00 a 0.95.",
        "que_significa": "Un valor mayor no indica necesariamente un mejor resultado. La evaluación sigue una distribución no lineal (curva de campana): ratios balanceados (0.50–0.60) reflejan el punto de equilibrio pedagógico óptimo; valores extremos señalan acaparamiento del canal de voz (> 0.90) o inactividad/ausencia de habla (< 0.10).",
        "escenario_contraste": "Un docente con un monólogo ininterrumpido durante 14 minutos (93% de ocupación) frente a un docente que habla 8.5 minutos (56% de ocupación) permitiendo la interacción activa.",
        "evaluacion_15min": "Determina la densidad de uso del canal de voz durante los 900 segundos del bloque analizado.",
        "lectura": "Un ratio en el rango óptimo 0.50–0.60 asigna Sobresaliente (T ≥ 65). Desviaciones hacia los extremos (< 0.20 o > 0.80) penalizan con rangos Bajo o Deficiente (20%–40%).",
        "niveles": {
            "Deficiente": {
                "rango": "DTE < 0.10 ó DTE > 0.90",
                "desc": "Ausencia de habla o acaparamiento del 90%",
            },
            "Bajo": {
                "rango": "0.10 ≤ DTE < 0.20 ó 0.80 < DTE ≤ 0.90",
                "desc": "Uso muy escaso o monólogo dominante",
            },
            "Promedio": {
                "rango": "0.20 ≤ DTE < 0.40 ó 0.70 < DTE ≤ 0.80",
                "desc": "Interacción moderada / clase estándar",
            },
            "Alto": {
                "rango": "0.40 ≤ DTE < 0.50 ó 0.60 < DTE ≤ 0.70",
                "desc": "Buen equilibrio exposición / alumnos",
            },
            "Sobresaliente": {
                "rango": "0.50 ≤ DTE ≤ 0.60",
                "desc": "Punto de equilibrio óptimo de interacción",
            },
        },
    },
    "M3": {
        "codigo": "M3",
        "nombre": "Estabilidad Técnica",
        "metrica": "Jitter_Score",
        "icono": "💻",
        "categoria": "Calidad Técnica / Streaming",
        "peso": 0.125,
        "que_hace": "Mide la fluidez y continuidad de la señal visual/técnica durante la clase.",
        "como_lo_hace": "Evalúa las variaciones en los intervalos temporales entre fotogramas para detectar anomalías, congelamientos o saltos de transmisión.",
        "para_que": "Controlar la Carga Cognitiva Extraña, asegurando que congelamientos o caídas en la transmisión no alteren la evaluación.",
        "que_obtiene": "Un índice de estabilidad en un rango continuo de 0.20 a 1.00.",
        "que_significa": "Valores cercanos a 1.00 indican una transmisión fluida y limpia; valores bajos (< 0.50) alertan sobre congelamientos o lag.",
        "escenario_contraste": "Una clase con video continuo sin interrupciones versus una clase con micro-cortes continuos por problemas de red.",
        "evaluacion_15min": "Tasa de degradación del flujo técnico en el bloque.",
        "lectura": "Ponderador de validez técnica. Un Jitter bajo invalida la interpretación pedagógica del bloque debido a la mala calidad del stream.",
        "niveles": {
            "Deficiente": {
                "rango": "Jitter < 0.30",
                "desc": "Congelamientos graves; invalida el bloque",
            },
            "Bajo": {
                "rango": "0.30 ≤ Jitter < 0.50",
                "desc": "Cortes frecuentes de video/audio",
            },
            "Promedio": {
                "rango": "0.50 ≤ Jitter < 0.75",
                "desc": "Micro-pausas esporádicas de red",
            },
            "Alto": {
                "rango": "0.75 ≤ Jitter < 0.90",
                "desc": "Transmisión fluida con variaciones mínimas",
            },
            "Sobresaliente": {
                "rango": "Jitter ≥ 0.90",
                "desc": "Transmisión técnica perfecta y estable",
            },
        },
    },
    "M4": {
        "codigo": "M4",
        "nombre": "Modulación y Expresividad",
        "metrica": "Tone_CoV",
        "icono": "🗣️",
        "categoria": "Audio / Prosodia",
        "peso": 0.125,
        "que_hace": "Mide el coeficiente de variación y modulación de la señal (Tone_CoV) sobre los tramos con voz real detectada por VAD.",
        "como_lo_hace": "Calcula el coeficiente de variación (desviación estándar dividida entre la media) de los parámetros de frecuencia fundamental (f0) extraídos con PyIN en momentos activos.",
        "para_que": "Cuantificar la riqueza de matices, la expresividad y detectar patrones planos o monótonos.",
        "que_obtiene": "Un coeficiente escalar ajustado en rango habitual entre 0.00 y 0.35.",
        "que_significa": "Coeficientes bajos (< 0.06) denotan un patrón plano e invariable; coeficientes altos (≥ 0.25) indican una modulación rica y expresiva.",
        "escenario_contraste": "Una explicación robótica y plana frente a una explicación con inflexiones, énfasis y dinamismo.",
        "evaluacion_15min": "La variabilidad y modulación del estímulo a lo largo del bloque.",
        "lectura": "Dispersión muy baja indica monotonía y riesgo de fatiga auditiva. Dispersión alta indica uso didáctico del ritmo y la modulación.",
        "niveles": {
            "Deficiente": {
                "rango": "Tone_CoV < 0.06",
                "desc": "Voz totalmente plana, robótica o leída",
            },
            "Bajo": {
                "rango": "0.06 ≤ Tone_CoV < 0.12",
                "desc": "Poca modulación vocal; monótona",
            },
            "Promedio": {
                "rango": "0.12 ≤ Tone_CoV < 0.18",
                "desc": "Modulación estándar conversacional",
            },
            "Alto": {
                "rango": "0.18 ≤ Tone_CoV < 0.25",
                "desc": "Voz expresiva con énfasis pedagógico",
            },
            "Sobresaliente": {
                "rango": "Tone_CoV ≥ 0.25",
                "desc": "Gran riqueza tonal, dinamismo e inflexión",
            },
        },
    },
    "M5": {
        "codigo": "M5",
        "nombre": "Presencia Corporal",
        "metrica": "IMP_promedio",
        "icono": "🧍",
        "categoria": "Video / Visión Artificial",
        "peso": 0.125,
        "que_hace": "Mide la cantidad e intensidad promedio del movimiento corporal y gestual del docente (IMP).",
        "como_lo_hace": "Calcula la diferencia absoluta de los fotogramas (flujo de movimiento) cuadro a cuadro en la región de interés (ROI) del rostro/cuerpo, con penalización por inactividad en sub-ventanas de 3 min.",
        "para_que": "Evaluar la presencia kinésica y el uso activo del cuerpo/manos como apoyo pedagógico.",
        "que_obtiene": "Un valor escalar normalizado entre 0.000 y 1.000 de intensidad media de movimiento.",
        "que_significa": "Valores bajos (< 0.001) indican una postura rígida, estática o docente fuera de encuadre; valores de 0.020 - 0.050+ reflejan dinamismo físico y presencia corporal activa.",
        "escenario_contraste": "Un docente inmóvil en la silla mirando fijo a la cámara versus un docente que gesticula activamente con las manos.",
        "evaluacion_15min": "Volumetría e intensidad global del movimiento físico en la ventana de 900 segundos.",
        "lectura": "Un valor cercano a cero identifica pasividad física extrema ('docente estatua'). Valores por encima de 0.020 confirman presencia activa en cámara.",
        "niveles": {
            "Deficiente": {
                "rango": "IMP < 0.001",
                "desc": "Inmovilidad total; docente fuera de cámara",
            },
            "Bajo": {
                "rango": "0.001 ≤ IMP < 0.005",
                "desc": "Postura rígida; escaso movimiento",
            },
            "Promedio": {
                "rango": "0.010 ≤ IMP < 0.020",
                "desc": "Gesticulación natural de soporte",
            },
            "Alto": {
                "rango": "0.020 ≤ IMP < 0.050",
                "desc": "Presencia corporal activa y expresiva",
            },
            "Sobresaliente": {
                "rango": "IMP ≥ 0.050",
                "desc": "Alto despliegue físico y dinamismo",
            },
        },
    },
    "M6": {
        "codigo": "M6",
        "nombre": "Energía y Proyección",
        "metrica": "Enthusiasm_Score",
        "icono": "🔥",
        "categoria": "Audio / Entusiasmo",
        "peso": 0.125,
        "que_hace": "Mide el volumen real y continuo que percibe el oído humano, en lugar de medir solo ruidos o picos repentinos.",
        "como_lo_hace": "Convierte todos los altibajos de la onda de voz en valores positivos y calcula la potencia constante de la voz a lo largo del tiempo.",
        "para_que": "Evitar que un aplauso o un grito instantáneo engañen al sistema, asegurando que se mida la energía real del discurso.",
        "que_obtiene": "Un número que representa la fuerza promedio verdadera con la que habló la persona.",
        "que_significa": "Un RMS bajo significa que la persona habló en voz muy baja, murmurando o lejos del micrófono la mayor parte del tiempo. Un RMS alto significa que mantuvo una voz firme, fuerte y constante durante toda la exposición.",
        "escenario_contraste": "Analogía del auto: el pico máximo es la velocidad máxima alcanzada por un segundo al pisar el acelerador; el valor RMS es la velocidad promedio real a la que viajó el auto durante todo el camino.",
        "evaluacion_15min": "Permite saber si el expositor mantuvo una potencia de voz sólida durante los 15 minutos continuos.",
        "lectura": "Es el dato clave que dice qué tan fuerte se sintió la voz en verdad, libre de silencios o ruidos engañosos.",
        "niveles": {
            "Deficiente": {
                "rango": "Enthusiasm < 0.01",
                "desc": "Murmullo inaudible, desgano o mic lejano",
            },
            "Bajo": {
                "rango": "0.01 ≤ Enthusiasm < 0.03",
                "desc": "Proyección baja, tono apagado",
            },
            "Promedio": {
                "rango": "0.03 ≤ Enthusiasm < 0.08",
                "desc": "Volumen y proyección estándar",
            },
            "Alto": {
                "rango": "0.08 ≤ Enthusiasm < 0.15",
                "desc": "Proyección firme, clara y enérgica",
            },
            "Sobresaliente": {
                "rango": "Enthusiasm ≥ 0.15",
                "desc": "Voz potente, entusiasmada y con autoridad",
            },
        },
    },
    "M7": {
        "codigo": "M7",
        "nombre": "Dinamismo y Ritmo",
        "metrica": "sigma2_IM",
        "icono": "🔄",
        "categoria": "Video / Cinemática",
        "peso": 0.125,
        "que_hace": "Mide la varianza del movimiento corporal (σ²_IM), evaluando la alternancia entre pausa y movimiento.",
        "como_lo_hace": "Calcula la varianza y dispersión de las muestras de movimiento extraídas en el bloque de 15 minutos con escalamiento para análisis rítmico.",
        "para_que": "Verificar si el docente altera estratégicamente momentos de reposo para explicar con momentos de énfasis gestual.",
        "que_obtiene": "Un escalar de varianza del movimiento acotado en [0.00, 1.00].",
        "que_significa": "Varianza cercana a cero (< 0.01) indica postura congelada o sin alternancia; varianza alta (≥ 0.50) refleja un ritmo dinámico y versátil.",
        "escenario_contraste": "Docente estático o con tic constante (varianza ~0) versus docente que alterna pausas de explicación con gesticulación enérgica de énfasis.",
        "evaluacion_15min": "La frecuencia de cambio o alternancia del dinamismo (ritmo) en el bloque.",
        "lectura": "Una varianza muy baja señala rigidez o monotonía en el patrón físico. Una varianza adecuada confirma versatilidad rítmica y pausas dinámicas.",
        "niveles": {
            "Deficiente": {
                "rango": "sigma2_IM < 0.000",
                "desc": "Ritmo plano; postura sin cambios",
            },
            "Bajo": {
                "rango": "0.008 ≤ sigma2_IM < 0.03",
                "desc": "Movimiento repetitivo o baja alternancia",
            },
            "Promedio": {
                "rango": "0.03 ≤ sigma2_IM < 0.10",
                "desc": "Alternancia regular entre calma y gestos",
            },
            "Alto": {
                "rango": "0.10 ≤ sigma2_IM < 0.25",
                "desc": "Uso estratégico de pausas y énfasis físico",
            },
            "Sobresaliente": {
                "rango": "sigma2_IM ≥ 0.25",
                "desc": "Gran versatilidad y dinamismo rítmico",
            },
        },
    },
}


# ====================================================================
# UTILIDADES
# ====================================================================
def cargar_estilos():
    """Carga el archivo estilos.css desde la misma carpeta."""
    ruta_css = BASE_DIR / "estilos.css"
    if ruta_css.exists():
        with open(ruta_css, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ No se encontró `estilos.css` en: `{ruta_css}`")


# ====================================================================
# BLOQUES DE RENDERIZADO
# ====================================================================
def bloque_banner():
    st.markdown(
        """
    <div class="banner-mbe">
        <h1>📄 Rúbrica Modelo Dos</h1>
        <p class="subtitulo">Modelo Bidireccional de Evaluación · Segmentación por bloques de 15 minutos</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def bloque_metodologia():
    st.markdown(
        """
    <div class="banner-seccion">
        <h2>📐 Metodología de Evaluación y Estratificación Temporal</h2>
        <p>Bloques fijos de 15 minutos (900 segundos)</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("""
    La evaluación del desempeño se realiza mediante un esquema de segmentación por bloques fijos de 
    **15 minutos (900 segundos)**. Esta estrategia estandariza la unidad de observación psicométrica, 
    permitiendo evaluar de forma equivalente tanto clases cortas (15–30 min) como clases largas (60–120 min).

    Para cada bloque de 15 minutos se calcula de manera independiente el rendimiento de cada modelo analítico. 
    La calificación final de la sesión para cada modelo se obtiene dividiendo la suma de los resultados de 
    cada bloque entre el número total de bloques analizados (**N**).
    """)
    st.latex(
        r"Resultado\ Final\ del\ Modelo = \frac{\sum_{i=1}^{N} Resultado\ del\ Bloque_i}{N}"
    )


def bloque_banner_modelos():
    st.markdown(
        """
    <div class="banner-seccion">
        <h2>🧩 Desglose y Procesamiento de cada Modelo Analítico</h2>
        <p>8 modelos · Peso uniforme de 12.5% sobre el Score T Global</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def bloque_tarjeta_modelo(codigo: str, info: dict):
    """Tarjeta individual de un modelo."""
    with st.container(border=True):
        col_titulo, col_badges = st.columns([3, 2])

        with col_titulo:
            st.markdown(f"### {info['icono']} {codigo}: {info['nombre']}")

        with col_badges:
            st.markdown(
                f"<div style='text-align:right; padding-top:10px;'>"
                f"<span class='modelo-metrica'>{info['metrica']}</span>&nbsp;"
                f"<span class='modelo-peso'>Peso: {info['peso']:.3f}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.caption(f"📂 {info['categoria']}")
        st.write(info["que_hace"])

        if st.button(
            "🔬 Ver fundamento completo",
            key=f"btn_{codigo}",
            use_container_width=True,
        ):
            mostrar_modal_modelo(codigo)


def bloque_modelos():
    """Itera los 8 modelos en 2 columnas."""
    cols = st.columns(2)
    for index, (codigo, info) in enumerate(MODELOS_INFO.items()):
        with cols[index % 2]:
            bloque_tarjeta_modelo(codigo, info)


@st.dialog("🔬 Fundamento del Modelo Analítico", width="large")
def mostrar_modal_modelo(codigo: str):
    info = MODELOS_INFO[codigo]

    st.markdown(f"### {info['icono']} {info['codigo']} · {info['nombre']}")
    st.caption(
        f"Métrica: **{info['metrica']}** · Categoría: **{info['categoria']}** · Peso: **{info['peso']:.3f}**"
    )

    st.divider()

    st.markdown("#### ❓ ¿Qué hace?")
    st.write(info["que_hace"])

    st.markdown("#### ⚙️ ¿Cómo lo hace?")
    st.write(info["como_lo_hace"])

    st.markdown("#### 🎯 ¿Para qué lo hace?")
    st.write(info["para_que"])

    st.markdown("#### 📊 ¿Qué obtiene?")
    st.write(info["que_obtiene"])

    st.markdown("#### 💡 ¿Qué significa?")
    st.info(info["que_significa"])

    st.markdown("#### 🔄 Escenario de contraste")
    st.write(info["escenario_contraste"])

    st.markdown("#### ⏱️ Evaluación en los 15 min")
    st.write(info["evaluacion_15min"])

    st.divider()
    st.markdown("#### 📋 Tabla de Clasificación en 5 Niveles")

    filas = []
    for nivel, datos in info["niveles"].items():
        filas.append(
            {
                "Nivel": nivel,
                "Rango": datos["rango"],
                "Descripción": datos["desc"],
            }
        )
    df = pd.DataFrame(filas)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("#### 📖 Lectura del resultado")
    st.success(info["lectura"])


def bloque_tabla_maestra():
    st.markdown(
        """
    <div class="banner-seccion">
        <h2>📋 Tabla Maestra de Clasificación en 5 Niveles</h2>
        <p>Interpretación psicométrica por bloque de 15 minutos · Escala T</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("""
    La siguiente tabla detalla la interpretación psicométrica y los rangos numéricos exactos 
    alineados con el código Python ejecutable en el sistema.
    """)

    filas = []
    for codigo, info in MODELOS_INFO.items():
        n = info["niveles"]
        filas.append(
            {
                "Modelo": f"{codigo}: {info['nombre']}",
                "Métrica": info["metrica"],
                "Deficiente (T<35)": n["Deficiente"]["rango"],
                "Bajo (35≤T<45)": n["Bajo"]["rango"],
                "Promedio (45≤T<55)": n["Promedio"]["rango"],
                "Alto (55≤T<65)": n["Alto"]["rango"],
                "Sobresaliente (T≥65)": n["Sobresaliente"]["rango"],
            }
        )
    df = pd.DataFrame(filas)
    st.dataframe(df, use_container_width=True, hide_index=True)


def bloque_score_global():
    st.markdown(
        """
    <div class="banner-seccion">
        <h2>📊 Score T Global e Inferencia Bivalente</h2>
        <p>Estandarización, cálculo ponderado y clasificación final de la clase</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🎯 Estandarización a Puntos T")
        df_pt = pd.DataFrame(
            {
                "Nivel": [
                    "Deficiente / Crítico",
                    "Bajo / En Riesgo",
                    "Promedio / Aceptable",
                    "Alto / Deseable",
                    "Sobresaliente / Óptimo",
                ],
                "Puntos T": [30.0, 40.0, 50.0, 60.0, 70.0],
                "Cumplimiento": ["20%", "40%", "60%", "80%", "100%"],
            }
        )
        st.dataframe(df_pt, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("#### 🧮 Fórmula del Score T Global")
        st.latex(
            r"Score\_T\_Global = \sum_{k=0}^{7} \left( Puntos\_T(M_k) \times w_k \right)"
        )
        st.markdown("""
        Con **peso uniforme** `w_k = 0.125` para los 8 modelos, la fórmula se reduce al 
        **promedio aritmético** de los puntos T:

        `Score_T_Global = (Σ Puntos_T(Mk)) / 8`
        """)


def bloque_inferencia():
    st.divider()
    st.markdown("#### 🏁 Inferencia de Estado de la Clase")

    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):
            st.success("### ✅ ENTRETENIDO (Estado = 1)")
            st.markdown("Se cumple **simultáneamente**:")
            st.markdown("""
            - Al menos **4 modelos** con cumplimiento ≥ 60%  
              *o* **Score_T_Global ≥ 48.0**
            - **Regla de Guarda Pedagógica:**
                - DTE_ratio ≥ 0.15 (voz activa mínima)
                - IMP_promedio ≥ 0.0005 (presencia en cámara mínima)
            """)

    with col4:
        with st.container(border=True):
            st.error("### ❌ ABURRIDO (Estado = 0)")
            st.markdown(
                "Se asigna cuando **NO** se cumple la Regla de Guarda Pedagógica o los umbrales mínimos:"
            )
            st.markdown("""
            - DTE_ratio < 0.15 (ausencia de voz activa)
            - IMP_promedio < 0.0005 (docente fuera de cámara)
            - Menos de 4 modelos con cumplimiento ≥ 60%  
              *y* Score_T_Global < 48.0
            """)


def bloque_footer():
    st.divider()
    st.markdown(
        """
    <div style="text-align:center; color:#6b7280; font-size:0.82rem; padding:20px 0;">
        <strong>Modelo Bidireccional de Evaluación (MBE)</strong> · Rúbrica Modelo Dos<br>
        Segmentación en bloques de 15 min · Escala T de 5 niveles · Inferencia bivalente<br><br>
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
    bloque_metodologia()
    st.divider()
    bloque_banner_modelos()
    bloque_modelos()
    st.divider()
    bloque_tabla_maestra()
    st.divider()
    bloque_score_global()
    bloque_inferencia()
    bloque_footer()


main()
