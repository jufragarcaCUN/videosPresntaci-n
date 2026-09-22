"""
Rúbrica Modelo Dos · Instrumento P-VES (Psychometric Video Evaluation Scale)
Evaluación multimodal de clases grabadas · 4 modelos: CEP · ENA · DAE · CCF
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
    page_title="Rúbrica Modelo Dos · P-VES",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent


# ====================================================================
# CONSTANTES
# ====================================================================
NIVELES_LIKERT = ["1 - Muy Bajo", "2 - Bajo", "3 - Medio", "4 - Alto", "5 - Muy Alto"]

MODELOS_PVES = {
    "CEP": {
        "codigo": "CEP",
        "nombre": "Evaluador de Conexión y Presencia",
        "icono": "👁️",
        "dimension": "Conexión y Presencia",
        "fuentes": "Video + Audio + Chat",
        "indicador": "frontal_gaze, smiling, postura",
        "salida": "Ítems CEP1 a CEP4 (1-5)",
        "que_hace": "Cuantifica la efectividad de la presencia no verbal, el contacto visual sostenido, la gestualidad facial y la estabilidad postural del docente a lo largo de la clase.",
        "como_lo_hace": "Lanza análisis sobre la señal visual (detección de mirada frontal, apertura ocular y sonrisa) y lo cruza con el análisis prosódico de la voz (frecuencia fundamental y pausas) junto con las reacciones emocionales iniciales del chat.",
        "para_que": "Medir la capacidad de conexión interpersonal del docente según los principios comunicativos de Chris Anderson (Charlas TED), reduciendo el sesgo de la evaluación humana.",
        "que_obtiene": "Un Score de Presencia Expresiva continuo (0 a 100), compuesto por: Porcentaje de Mirada Directa, Índice de Expresividad Facial y Score de Estabilidad Postural.",
        "que_significa": "Puntaje 80–100: Docente altamente conectado con su audiencia, con mirada fija en cámara, expresión accesible y uso intencional de la voz. Puntaje < 50: Docente desconectado, con mirada fija hacia abajo (lectura continua) o postura rígida fuera de encuadre.",
        "escenario_alto": "Docente centrado, mirando a cámara el 85% del tiempo, variando el tono de voz en puntos clave y con mensajes positivos en el chat → Puntuación Likert: 5 (Excelente).",
        "escenario_bajo": "Docente inclinado leyendo apuntes fuera de cámara el 70% del tiempo, tono monotónico → Puntuación Likert: 1 (Deficiente).",
        "evaluacion_15min": "Muestrea la clase a intervalos fijos (1 segundo de análisis por cada 3 segundos de video). Divide los 15 minutos en 3 bloques de 5 minutos (Inicio, Desarrollo y Cierre) para medir si la presencia decae por fatiga.",
        "procesamiento": "Mapea la condición de mirada frontal (frontal_gaze = True), detecta la simetría de hombros y codos para verificar la postura erguida, y registra los momentos en que la comisura labial indica gesticulación positiva (smiling = True).",
        "lectura": "Genera las notas de los ítems CEP1 (Mirada), CEP2 (Gestos), CEP3 (Voz) y CEP4 (Postura) en escala Likert del 1 al 5.",
        "niveles": {
            "1 - Muy Bajo": "Mirada a cámara <20% del tiempo (frontal_gaze inactivo); lectura fija hacia abajo; postura rígida/descentrada; voz monótona y sin reacciones iniciales en el chat.",
            "2 - Bajo": "Mirada a cámara 20%-49% del tiempo; dependencia constante de notas; postura con inclinaciones severas; tono de voz poco variado.",
            "3 - Medio": "Mirada a cámara 50%-69% del tiempo; lectura intermitente de apoyos; postura centrada aceptable; tono de voz con variaciones básicas.",
            "4 - Alto": "Mirada a cámara 70%-84% del tiempo; lenguaje corporal abierto; buena modulación de voz y pausas; reacciones positivas iniciales en chat.",
            "5 - Muy Alto": "Mirada a cámara ≥ 85% del tiempo; postura erguida y centrada; gesticulación estratégica y accesible (smiling); manejo prosódico óptimo.",
        },
    },
    "ENA": {
        "codigo": "ENA",
        "nombre": "Evaluador de Estructura Narrativa y Línea Argumental",
        "icono": "📖",
        "dimension": "Estructura Narrativa",
        "fuentes": "Transcripción + Video + Chat",
        "indicador": "TEXT_DETECTION (OCR) + Coherencia",
        "salida": "Ítems ENA1 a ENA4 (1-5)",
        "que_hace": "Evalúa la coherencia pedagógica del discurso, la claridad de la 'idea fuerza' (Throughline), la presencia de un gancho inicial y la coincidencia entre la explicación oral y el texto de apoyo.",
        "como_lo_hace": "Utiliza el reconocimiento óptico de caracteres (OCR) para leer el texto en pantalla (TEXT_DETECTION), analiza la transcripción del audio para evaluar la estructura sintáctica/semántica y monitorea las preguntas de comprensión enviadas en el chat.",
        "para_que": "Verificar si la clase sigue una secuencia lógica de aprendizaje según los principios de síntesis y novedad pedagógica de Carmine Gallo (Hable como en TED).",
        "que_obtiene": "Un Índice de Coherencia Narrativa, la delimitación automática de las 3 fases de la clase (Inicio-Desarrollo-Cierre) y el Grado de Alineación Audio-Texto.",
        "que_significa": "Determina si la presentación es un monólogo desestructurado o si se articula como una secuencia didáctica orientada a objetivos claros de aprendizaje.",
        "escenario_alto": "Gancho temático en el primer minuto, diapositivas sintéticas que coinciden exactamente con lo que habla el profesor y pocas dudas conceptuales en el chat → Puntuación Likert: 5.",
        "escenario_bajo": "Introducción vaga de 4 minutos, diapositivas sobrecargadas de texto no explicado y chat saturado de confusión → Puntuación Likert: 1-2.",
        "evaluacion_15min": "Evalúa la transcripción dividida en 3 segmentos temporales: Gancho e Introducción (Minutos 0 a 3), Desarrollo Argumental (Minutos 3 a 12) y Síntesis / Cierre (Minutos 12 a 15).",
        "procesamiento": "Compara el vocabulario extraído de las diapositivas mediante OCR con las palabras clave habladas en la transcripción. Mide la distancia semántica entre la promesa planteada en el minuto 1 y las conclusiones emitidas en el minuto 15.",
        "lectura": "Transforma los índices semánticos en las calificaciones ordinales (1 a 5) de los ítems ENA1 (Gancho), ENA2 (Progresión), ENA3 (Texto de apoyo) y ENA4 (Síntesis final).",
        "niveles": {
            "1 - Muy Bajo": "Sin gancho temático en los primeros 4 min; discurso desestructurado; diapositivas saturadas no explicadas (TEXT_DETECTION); chat confundido.",
            "2 - Bajo": "Gancho tardío (>3 min); secuencia con saltos temáticos; bajo contraste entre voz y texto en pantalla; múltiples dudas en el chat.",
            "3 - Medio": "Presenta el tema al inicio pero sin pregunta detonante; sigue el orden de diapositivas con transiciones rígidas; síntesis final apresurada.",
            "4 - Alto": "Plantea una idea fuerza clara en los primeros 2 min; progresión lógica acumulativa; texto en pantalla complementa la voz; síntesis adecuada.",
            "5 - Muy Alto": "Plantea un gancho claro en los primeros 60-90 s; secuencia didáctica impecable (Throughline); perfecta concordancia texto-voz; síntesis y llamada a la acción explícita.",
        },
    },
    "DAE": {
        "codigo": "DAE",
        "nombre": "Evaluador de Dinamismo y Engagement",
        "icono": "⚡",
        "dimension": "Dinamismo y Engagement",
        "fuentes": "Video + Chat",
        "indicador": "SHOT_CHANGE_DETECTION + Tasa Chat",
        "salida": "Ítems DAE1 a DAE4 (1-5)",
        "que_hace": "Mide la cadencia visual de la producción, la variedad de estímulos, la frecuencia de cortes/cambios de plano y el volumen de interacción activa generado en la audiencia.",
        "como_lo_hace": "Suma los cortes de edición e imágenes detectados por cambio de plano (SHOT_CHANGE_DETECTION), rastrea la aparición de objetos didácticos (OBJECT_TRACKING) y mide la tasa de mensajes por minuto enviados en el chat.",
        "para_que": "Evitar la monotonía audiovisual que causa caídas de retención en entornos digitales, correlacionando el dinamismo con las métricas estándar de consumo de video.",
        "que_obtiene": "La Tasa de Cortes por Minuto (CPM), el Conteo de Entidades Visuales Interactivas y la Curva de Participación Temporal del Chat.",
        "que_significa": "Indica si la clase logra mantener un ritmo estimulante que sostenga la atención selectiva del estudiante a lo largo de los 15 minutos.",
        "escenario_alto": "Un cambio de plano o apoyo gráfico cada 15-20 segundos, uso de objetos pedagógicos y picos de mensajes en el chat ante preguntas del profesor → Puntuación Likert: 5.",
        "escenario_bajo": "Plano secuencia único y estático de 15 minutos sin apoyos visuales y chat inactivo → Puntuación Likert: 1.",
        "evaluacion_15min": "Genera un gráfico continuo de la densidad de estímulos visuales e interacciones minuto por minuto a lo largo de los 900 segundos de duración.",
        "procesamiento": "Registra los marcas de tiempo (timestamps) devueltos por la API ante cada cambio brusco de fotograma y contabiliza las cajas delimitadoras (bounding boxes) asignadas a objetos pedagógicos en pantalla.",
        "lectura": "Mapea la densidad de estímulos y la participación activa del chat a las puntuaciones Likert de los ítems DAE1 (Cortes), DAE2 (Objetos), DAE3 (Preguntas) y DAE4 (Ritmo).",
        "niveles": {
            "1 - Muy Bajo": "Toma fija estática de 15 min sin cortes (SHOT_CHANGE_DETECTION nulo); sin objetos ni interacción; chat inactivo o muerto.",
            "2 - Bajo": "Cortes de plano muy escasos (>2 min por toma); exposición verbal sin apoyos interactivos; mínima participación en el chat.",
            "3 - Medio": "Cambios de toma irregulares (1 corte por min); muestra algún recurso visual básico; genera preguntas retóricas con poca respuesta en chat.",
            "4 - Alto": "Cambios de plano bien distribuidos (cada 30-45 s); uso de objetos/esquemas (OBJECT_TRACKING); picos de respuestas en el chat ante preguntas.",
            "5 - Muy Alto": "Ritmo ágil con cambios de plano estratégicos (cada 15-30 s); manipulación activa de objetos/recursos pedagógicos; altísima participación del chat.",
        },
    },
    "CCF": {
        "codigo": "CCF",
        "nombre": "Evaluador de Claridad Conceptual y Feedback Didáctico",
        "icono": "🧠",
        "dimension": "Claridad y Feedback",
        "fuentes": "Transcripción + Audio + Chat",
        "indicador": "Similaridad NLP + Marcadores Discursivos",
        "salida": "Ítems CCF1 a CCF4 (1-5)",
        "que_hace": "Evalúa el grado de precisión pedagógica en las explicaciones, la densidad del vocabulario técnico accesible, el uso de analogías/ejemplos y la capacidad de retroalimentar dudas en tiempo real.",
        "como_lo_hace": "Analiza semánticamente la transcripción del discurso utilizando modelos NLP de procesamiento sintáctico, cruza el audio diarizado para detectar respuestas explícitas a preguntas e integra la analítica textual de preguntas/respuestas del chat.",
        "para_que": "Medir la efectividad instruccional y el andamiaje del aprendizaje, garantizando que el docente no solo presente información, sino que facilite la comprensión conceptual y aclare lagunas didácticas.",
        "que_obtiene": "El Índice de Densidad e Inteligibilidad Conceptual, el Porcentaje de Resolución de Dudas en Chat y la Tasa de Uso de Analogías / Ejemplos Ilustrativos.",
        "que_significa": "Determina si el docente adapta la complejidad del contenido a la audiencia y si atiende las barreras de aprendizaje que surgen durante la sesión.",
        "escenario_alto": "Explicación fluida con metáforas claras, lectura/mención directa de preguntas del chat con retroalimentación inmediata → Puntuación Likert: 5.",
        "escenario_bajo": "Uso de jerga incomprensible sin ejemplificación, ignorancia sistemática de dudas en el chat y explicaciones ambiguas → Puntuación Likert: 1.",
        "evaluacion_15min": "Monitorea la transcripción de audio en intervalos de 3 minutos, correlacionando las fluctuaciones de preguntas en el chat con los momentos de respuesta explícita del docente.",
        "procesamiento": "Rastrea marcadores lingüísticos de ejemplificación (ej. 'por ejemplo', 'imaginemos que', 'en otras palabras') en la transcripción y mide la similitud semántica entre las preguntas formuladas por los usuarios en el chat y las locuciones subsiguientes del docente.",
        "lectura": "Asigna las puntuaciones ordinales (1 a 5) para los ítems CCF1 (Precisión), CCF2 (Ejemplificación), CCF3 (Atención a dudas) y CCF4 (Andamiaje).",
        "niveles": {
            "1 - Muy Bajo": "Discurso ambiguo con sesgos teóricos; cero uso de ejemplos; ignora por completo las dudas del chat; no realiza andamiaje conceptual.",
            "2 - Bajo": "Vocabulario excesivamente técnico sin explicación; uso escaso de analogías (<1 en 15 min); aborda <20% de las dudas expresadas en el chat.",
            "3 - Medio": "Explicación conceptual clara pero abstracta; incluye 1-2 ejemplos básicos; responde algunas preguntas del chat al final del bloque.",
            "4 - Alto": "Buena precisión conceptual; uso frecuente de analogías aclaratorias; responde activamente al 50%-75% de las dudas del chat.",
            "5 - Muy Alto": "Explicación de alta precisión adaptada al nivel; uso continuo de analogías/casos prácticos; detecta y resuelve en tiempo real >75% de las dudas del chat.",
        },
    },
}

REFERENCIAS = [
    {
        "seccion": "🎤 Marco de Oratoria, Comunicación y Diseño Pedagógico",
        "items": [
            "Anderson, C. (2016). Charlas TED: La guía oficial de TED para hablar en público. Conecta.",
            "Gallo, C. (2014). Hable como en TED: Nueve secretos para comunicar utilizados por los mejores. Conecta.",
        ],
    },
    {
        "seccion": "📐 Fundamentación Psicométrica y Análisis Multivariado",
        "items": [
            "American Educational Research Association, American Psychological Association, & National Council on Measurement in Education. (2014). Standards for educational and psychological testing. American Educational Research Association.",
            "Hair, J. F., Black, W. C., Babin, B. J., & Anderson, R. E. (2019). Multivariate data analysis (8.ª ed.). Cengage Learning.",
            "McDonald, R. P. (1999). Test theory: A unified treatment. Lawrence Erlbaum Associates.",
            "Muñiz, J. (2018). Introducción a la psicometría. Pirámide.",
        ],
    },
    {
        "seccion": "🤖 Analítica Multimodal, Métricas y Visión por Computador",
        "items": [
            "Google Cloud. (2024). Cloud Video Intelligence API documentation. Google Developers.",
            "YouTube. (2023). Understanding audience retention in YouTube Analytics. YouTube Help.",
        ],
    },
]


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
        <h1>📄 Instrumento P-VES</h1>
        <p class="subtitulo">Psychometric Video Evaluation Scale · 4 modelos multimodales · Escala Likert 1-5</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def bloque_introduccion():
    st.markdown("""
    El instrumento **P-VES** evalúa clases grabadas en segmentos de 15 minutos mediante el análisis 
    multimodal de audio diarizado, video e interacción en chat, con el objetivo final de generar un 
    **resumen diagnóstico y formativo** por cada video analizado para optimizar el desempeño comunicativo 
    y la calidad pedagógica del docente.
    """)

    st.markdown(
        """
    <div style="background:#f0fdf4; border-left:5px solid #1a7a3a; padding:14px 18px; 
                border-radius:8px; margin:16px 0;">
        <strong style="color:#166534;">📊 Estructura Multimodal de Evaluación (4 Modelos)</strong>
        <p style="margin:6px 0 0 0; font-size:0.85rem; color:#374151;">
            Cada modelo mide una dimensión específica del desempeño docente combinando 
            distintas fuentes (video, audio, transcripción y chat) para generar puntuaciones 
            Likert del 1 al 5 en ítems específicos.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def bloque_banner_modelos():
    st.markdown(
        """
    <div class="banner-seccion">
        <h2>🧩 Detalle de los Modelos de Evaluación</h2>
        <p>4 modelos multimodales · Escala Likert 1-5</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def bloque_tarjeta_modelo(codigo: str, info: dict):
    """Tarjeta individual de un modelo P-VES."""
    with st.container(border=True):
        col_titulo, col_badges = st.columns([3, 2])

        with col_titulo:
            st.markdown(f"### {info['icono']} {codigo} · {info['nombre']}")

        with col_badges:
            st.markdown(
                f"<div style='text-align:right; padding-top:10px;'>"
                f"<span class='modelo-metrica'>{info['dimension']}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.markdown(f"**🎥 Fuentes:** {info['fuentes']}")
        st.markdown(f"**🔍 Indicador:** `{info['indicador']}`")
        st.markdown(f"**📝 Salida:** {info['salida']}")
        st.write(info["que_hace"])

        if st.button(
            "🔬 Ver fundamento completo",
            key=f"btn_{codigo}",
            use_container_width=True,
        ):
            mostrar_modal_modelo(codigo)


def bloque_modelos():
    """Itera los 4 modelos en 2 columnas."""
    cols = st.columns(2)
    for index, (codigo, info) in enumerate(MODELOS_PVES.items()):
        with cols[index % 2]:
            bloque_tarjeta_modelo(codigo, info)


@st.dialog("🔬 Fundamento del Modelo P-VES", width="large")
def mostrar_modal_modelo(codigo: str):
    info = MODELOS_PVES[codigo]

    st.markdown(f"### {info['icono']} {info['codigo']} · {info['nombre']}")
    st.caption(
        f"Dimensión: **{info['dimension']}** · Fuentes: **{info['fuentes']}** · Salida: **{info['salida']}**"
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

    st.markdown("#### 🟢 Escenario Alto")
    st.success(info["escenario_alto"])

    st.markdown("#### 🔴 Escenario Bajo")
    st.error(info["escenario_bajo"])

    st.markdown("#### ⏱️ Evaluación en los 15 min")
    st.write(info["evaluacion_15min"])

    st.markdown("#### 🔬 Procesamiento detallado")
    st.write(info["procesamiento"])

    st.divider()
    st.markdown("#### 📋 Matriz Operacional de Clasificación (Likert 1-5)")

    filas = []
    for nivel, desc in info["niveles"].items():
        filas.append({"Nivel": nivel, "Descripción": desc})
    df = pd.DataFrame(filas)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("#### 📖 Lectura del resultado")
    st.success(info["lectura"])


def bloque_matriz_resumen():
    st.markdown(
        """
    <div class="banner-seccion">
        <h2>📋 Matriz Resumen de los 4 Modelos</h2>
        <p>Dimensión · Fuentes · Indicador · Salida psicométrica</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    filas = []
    for codigo, info in MODELOS_PVES.items():
        filas.append(
            {
                "Modelo": f"{info['icono']} {codigo}",
                "Dimensión P-VES": info["dimension"],
                "Fuentes Utilizadas": info["fuentes"],
                "Indicador Clave de Entrada": info["indicador"],
                "Salida Psicométrica": info["salida"],
            }
        )
    st.dataframe(pd.DataFrame(filas), use_container_width=True, hide_index=True)


def bloque_matriz_operacional():
    st.markdown(
        """
    <div class="banner-seccion">
        <h2>📐 Matriz Operacional de Clasificación (Niveles Likert 1 a 5)</h2>
        <p>Descripción operativa de cada nivel por modelo</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    for codigo, info in MODELOS_PVES.items():
        with st.container(border=True):
            st.markdown(f"#### {info['icono']} Modelo {codigo}: {info['dimension']}")

            for nivel in NIVELES_LIKERT:
                desc = info["niveles"][nivel]
                st.markdown(f"**Nivel {nivel}:** {desc}")


def bloque_referencias():
    st.markdown(
        """
    <div class="banner-seccion">
        <h2>📚 Referencias Bibliográficas</h2>
        <p>APA 7.ª Edición</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    for grupo in REFERENCIAS:
        st.markdown(f"#### {grupo['seccion']}")
        for item in grupo["items"]:
            st.markdown(f"- {item}")


def bloque_footer():
    st.divider()
    st.markdown(
        """
    <div style="text-align:center; color:#6b7280; font-size:0.82rem; padding:20px 0;">
        <strong>Instrumento P-VES</strong> · Psychometric Video Evaluation Scale<br>
        Evaluación multimodal de clases grabadas · Escala Likert 1-5<br><br>
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
    bloque_introduccion()
    st.divider()
    bloque_banner_modelos()
    bloque_modelos()
    st.divider()
    bloque_matriz_resumen()
    st.divider()
    bloque_matriz_operacional()
    st.divider()
    bloque_referencias()
    bloque_footer()


main()
