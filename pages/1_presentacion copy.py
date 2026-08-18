"""
Dashboard - Presentación
Página de introducción, articulación pedagógica (4 Pilares + Preguntas CUN Experience),
modelos de IA/MALA, tarjetas ejecutivas y modales con fundamento científico.
Versión con Opción 1 (Informal/Coloquial) y Opción 2 (Formal/Institucional) - AMBAS VISIBLES
"""

import warnings
import streamlit as st

warnings.filterwarnings("ignore")

# ====================================================================
# CONFIGURACIÓN DE PÁGINA
# ====================================================================
st.set_page_config(
    page_title="Dashboard CUN - Inteligencia Académica",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ====================================================================
# DICCIONARIO DE PREGUNTAS CUN - DOS VERSIONES
# ====================================================================
PREGUNTAS_CUN = {
    "P1": {
        "opcion_1": "¿El profe hizo pausas en la clase para resolver dudas, hacer preguntas o poner ejercicios prácticos?",
        "opcion_2": "El docente realizó pausas periódicas durante la sesión para responder inquietudes, realizar preguntas o promover actividades prácticas.",
        "pilar": "Aprendizaje Activo",
        "metricas": ["DME_s", "DTE_ratio"],
        "icono": "🎙️",
    },
    "P2": {
        "opcion_1": "¿La forma de explicar del profe y la actitud que le puso a la clase hicieron que no te distrajeras?",
        "opcion_2": "El dinamismo de la explicación y el entusiasmo demostrado por el docente facilitaron mantener el foco de atención durante la sesión.",
        "pilar": "Neuroeducación y Atención",
        "metricas": ["Tone_CoV", "Enthusiasm_Score"],
        "icono": "🗣️",
    },
    "P3": {
        "opcion_1": "¿El profe usó bien la cámara y se expresó con las manos y el cuerpo para hacer la clase dinámica?",
        "opcion_2": "La expresividad corporal del docente y su interacción frente a la cámara contribuyeron al desarrollo fluido y cercano de la clase.",
        "pilar": "Cognición Encarnada",
        "metricas": ["IMP_promedio", "sigma2_IM"],
        "icono": "🧍",
    },
    "P4": {
        "opcion_1": "¿La clase se transmitió bien (el audio, el video y la pantalla compartida) sin trabarse ni cortarse?",
        "opcion_2": "La transmisión de la clase (calidad de audio, fluidez de video y pantalla compartida) se mantuvo constante y sin interrupciones técnicas.",
        "pilar": "Carga Cognitiva Extraña",
        "metricas": ["Jitter_Score"],
        "icono": "💻",
    },
}

# ====================================================================
# DICCIONARIO INTEGRADO: PILARES, MODELOS DE IA Y METADATOS
# ====================================================================
MODELOS_INFO = {
    "DME_s": {
        "nombre": "Control del Monólogo",
        "nombre_gerencial": "Control del Monólogo",
        "icono": "🎙️",
        "categoria": "Audio / Interacción",
        "pilar": "Pilar 1: Aprendizaje Activo",
        "sustento_neuropedagogico": "Las exposiciones ininterrumpidas prolongadas inducen pasividad atencional. Pausas cortas facilitan la consolidación en memoria de trabajo.",
        "resumen": "Mide la duración promedio de las intervenciones habladas continuas del docente sin pausa o interrupción.",
        "evalua": "Capacidad del docente para pausar y dar paso a la participación del estudiante.",
        "bueno": "< 3.5 segundos entre pausas clave",
        "malo": "≥ 3.5 segundos de monólogo continuo",
        "autores": "Flanders, N. A. (1970)",
        "cita_apa": "Flanders, N. A. (1970). Analyzing teaching behavior. Addison-Wesley.",
        "doi": "https://doi.org/10.1207/s15516709cog1202_4",
        "limite": 3.5,
        "condicion": "menor",
        "corto": "Monólogo",
        "pregunta_key": "P1",
    },
    "Tone_CoV": {
        "nombre": "Expresividad Vocal",
        "nombre_gerencial": "Expresividad Vocal",
        "icono": "🗣️",
        "categoria": "Audio / Prosodia",
        "pilar": "Pilar 2: Neuroeducación",
        "sustento_neuropedagogico": "El coeficiente de variación tonal evita el acostumbramiento atencional y mantiene receptiva la corteza auditiva.",
        "resumen": "Coeficiente de variación de la frecuencia fundamental (F0) para evaluar dinamismo acústico.",
        "evalua": "Rango y flexibilidad de entonación durante la clase.",
        "bueno": "> 0.32 de variación tonal",
        "malo": "≤ 0.32 (tono monótono)",
        "autores": "Scherer, K. R. (2003)",
        "cita_apa": "Scherer, K. R. (2003). Vocal communication of emotion: A review of research paradigms. Speech Communication, 40(1-2), 227–256.",
        "doi": "https://doi.org/10.1016/S0167-6393(02)00084-5",
        "limite": 0.32,
        "condicion": "mayor",
        "corto": "Expresividad",
        "pregunta_key": "P2",
    },
    "Enthusiasm_Score": {
        "nombre": "Energía y Proyección",
        "nombre_gerencial": "Energía y Proyección",
        "icono": "🔥",
        "categoria": "Audio / Entusiasmo",
        "pilar": "Pilar 2: Neuroeducación",
        "sustento_neuropedagogico": "El entusiasmo percibido estimula el sistema límbico e incrementa la motivación intrínseca del estudiante.",
        "resumen": "Puntaje compuesto de energía acústica e intensidad sonora promedio.",
        "evalua": "Nivel de vitalidad y proyección de la voz del docente.",
        "bueno": "> 0.15 de índice de energía",
        "malo": "≤ 0.15 (proyección baja o apática)",
        "autores": "Immordino-Yang, M. H., & Damasio, A. (2007)",
        "cita_apa": "Immordino-Yang, M. H., & Damasio, A. (2007). We feel, therefore we learn. Mind, Brain, and Education, 1(1), 3–10.",
        "doi": "https://doi.org/10.1111/j.1751-228X.2007.00004.x",
        "limite": 0.15,
        "condicion": "mayor",
        "corto": "Energía",
        "pregunta_key": "P2",
    },
    "DTE_ratio": {
        "nombre": "Nivel de Interacción",
        "nombre_gerencial": "Nivel de Interacción",
        "icono": "🤝",
        "categoria": "Audio / Diarización",
        "pilar": "Pilar 1: Aprendizaje Activo",
        "sustento_neuropedagogico": "El equilibrio en el tiempo de habla promueve el diálogo socrático y la co-construcción del conocimiento.",
        "resumen": "Proporción de tiempo de habla del docente respecto al tiempo total de la sesión.",
        "evalua": "Porcentaje del tiempo dominado por el profesor frente a la participación de estudiantes.",
        "bueno": "≤ 50% de uso del tiempo total",
        "malo": "> 50% de uso exclusivo del canal",
        "autores": "Vygotsky, L. S. (1978)",
        "cita_apa": "Vygotsky, L. S. (1978). Mind in society. Harvard University Press.",
        "doi": "https://doi.org/10.1207/s15516709cog1202_4",
        "limite": 0.5,
        "condicion": "menor_igual",
        "corto": "Interacción",
        "pregunta_key": "P1",
    },
    "IMP_promedio": {
        "nombre": "Presencia Corporal",
        "nombre_gerencial": "Presencia Corporal",
        "icono": "🧍",
        "categoria": "Video / Visión Artificial",
        "pilar": "Pilar 3: Cognición Encarnada",
        "sustento_neuropedagogico": "Los gestos facilitan la comprensión conceptual al acompañar la carga del habla con señales visuales.",
        "resumen": "Promedio de movimiento e intensidad de movimiento corporal detectado por visión por computadora.",
        "evalua": "Gesticulación y postura corporal frente a cámara.",
        "bueno": "> 4.0 puntos de movilidad",
        "malo": "≤ 4.0 (movilidad muy estática)",
        "autores": "Barsalou, L. W. (2008)",
        "cita_apa": "Barsalou, L. W. (2008). Grounded cognition. Annual Review of Psychology, 59, 617–645.",
        "doi": "https://doi.org/10.1146/annurev.psych.59.103006.093639",
        "limite": 4.0,
        "condicion": "mayor",
        "corto": "Presencia",
        "pregunta_key": "P3",
    },
    "sigma2_IM": {
        "nombre": "Dinamismo y Ritmo",
        "nombre_gerencial": "Dinamismo y Ritmo",
        "icono": "🔄",
        "categoria": "Video / Cinemática",
        "pilar": "Pilar 3: Cognición Encarnada",
        "sustento_neuropedagogico": "La variabilidad del movimiento mantiene el foco atencional evitando patrones corporales monótonos.",
        "resumen": "Varianza de la intensidad de movimiento en secuencias de video.",
        "evalua": "Fluidez y ritmo de los desplazamientos y expresiones corporales.",
        "bueno": "> 8.5 de varianza de movimiento",
        "malo": "≤ 8.5 (postura rígida)",
        "autores": "Barsalou, L. W. (2008)",
        "cita_apa": "Barsalou, L. W. (2008). Grounded cognition. Annual Review of Psychology, 59, 617–645.",
        "doi": "https://doi.org/10.1146/annurev.psych.59.103006.093639",
        "limite": 8.5,
        "condicion": "mayor",
        "corto": "Dinamismo",
        "pregunta_key": "P3",
    },
    "Jitter_Score": {
        "nombre": "Estabilidad Técnica",
        "nombre_gerencial": "Estabilidad Técnica",
        "icono": "💻",
        "categoria": "Calidad Técnica / Streaming",
        "pilar": "Pilar 4: Carga Cognitiva Extraña",
        "sustento_neuropedagogico": "Interrupciones o cortes técnicos consumen recursos atencionales que deberían ir hacia la comprensión académica.",
        "resumen": "Métrica de estabilidad de transmisión de fotogramas y señal de audio.",
        "evalua": "Fluidez técnica del video y transmisión.",
        "bueno": "> 0.40 de estabilidad técnica",
        "malo": "≤ 0.40 (interrupciones o latencia alta)",
        "autores": "Sweller, J. (1988)",
        "cita_apa": "Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. Cognitive Science, 12(2), 257–285.",
        "doi": "https://doi.org/10.1207/s15516709cog1202_4",
        "limite": 0.4,
        "condicion": "mayor",
        "corto": "Estabilidad",
        "pregunta_key": "P4",
    },
}

# ====================================================================
# IMPORTAR TABLA COMPARATIVA
# ====================================================================
try:
    from pages.tabla_comparativa import bondades_modelo
except ImportError:
    try:
        from tabla_comparativa import bondades_modelo
    except ImportError:
        st.warning("⚠️ No se encuentra tabla_comparativa.py")
        bondades_modelo = None


# ====================================================================
# FUNCIÓN PARA OBTENER LAS PREGUNTAS (AMBAS VERSIONES)
# ====================================================================
def obtener_preguntas(pregunta_key: str) -> tuple:
    """Obtiene ambas versiones de una pregunta."""
    if pregunta_key in PREGUNTAS_CUN:
        return (
            PREGUNTAS_CUN[pregunta_key]["opcion_1"],
            PREGUNTAS_CUN[pregunta_key]["opcion_2"],
        )
    return "Pregunta no encontrada", "Pregunta no encontrada"


# ====================================================================
# FUNCIONES DE UI
# ====================================================================


def inyectar_estilos():
    """Inyecta todos los estilos CSS de la aplicación."""
    st.markdown(
        """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Montserrat', sans-serif;
        }
        
        /* Badges */
        .badge-opcion {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 0.65rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .badge-opcion-1 { background-color: #fff3cd; color: #856404; }
        .badge-opcion-2 { background-color: #cce5ff; color: #004085; }
        
        /* Tarjetas de modelos */
        .card-container {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 18px;
            margin-bottom: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            height: 380px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .card-container:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.1);
        }
        .card-header-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #1a7a3a;
            margin: 0;
        }
        .card-badge {
            font-size: 0.72rem;
            background-color: #e8f5e9;
            color: #1a7a3a;
            padding: 3px 8px;
            border-radius: 12px;
            font-weight: 700;
        }
        .card-pilar-text {
            font-size: 0.78rem;
            font-weight: 600;
            color: #2e9e4e;
            margin-top: 4px;
            margin-bottom: 6px;
        }
        .card-body-text {
            font-size: 0.85rem;
            color: #424242;
            line-height: 1.35;
        }
        .card-rule {
            font-size: 0.78rem;
            background-color: #f8f9f9;
            padding: 6px 10px;
            border-radius: 6px;
            margin-top: 6px;
        }
        .card-pregunta {
            font-size: 0.72rem;
            color: #1a3a2a;
            background-color: #f0f7f2;
            padding: 5px 8px;
            border-radius: 6px;
            margin-top: 3px;
            border-left: 3px solid #1a7a3a;
            font-style: italic;
            line-height: 1.3;
        }
        .card-pregunta-op1 { border-left-color: #ffc107; background-color: #fffef0; }
        .card-pregunta-op2 { border-left-color: #0d6efd; background-color: #f0f5ff; }
        .label-opcion {
            font-size: 0.6rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            display: inline-block;
        }
        .label-op1 { color: #856404; }
        .label-op2 { color: #004085; }
        
        /* Botones CUN */
        div.stButton > button {
            background: linear-gradient(135deg, #1a7a3a, #2e9e4e) !important;
            color: white !important;
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover {
            transform: scale(1.02) !important;
            box-shadow: 0 4px 12px rgba(26, 122, 58, 0.4) !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 700 !important;
        }
        
        /* Banners */
        .banner-cun {
            background: linear-gradient(135deg, #0d5a2a, #1a7a3a, #2e9e4e) !important;
            padding: 22px;
            border-radius: 12px;
            text-align: center;
            color: white;
            margin-bottom: 25px;
        }
        .banner-pedagogico {
            background: linear-gradient(135deg, #0d5a2a 0%, #1a7a3a 100%);
            color: white;
            padding: 22px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .flecha-conector {
            text-align: center;
            font-size: 26px;
            color: #1a7a3a;
            margin: -10px 0 15px 0;
            font-weight: bold;
        }
        
        /* Tarjetas de pilares */
        .tarjeta-pilar {
            background-color: #FFFFFF;
            border-left: 5px solid #1a7a3a;
            border-radius: 10px;
            padding: 18px;
            margin-bottom: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            transition: transform 0.2s ease-in-out;
        }
        .tarjeta-pilar:hover { transform: translateY(-2px); }
        .circulo-icono {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 16px;
            color: white;
            margin-bottom: 10px;
        }
        .circulo-verde { background-color: #10B981; }
        .circulo-amarillo { background-color: #F59E0B; }
        .circulo-azul { background-color: #3B82F6; }
        .circulo-morado { background-color: #8B5CF6; }
        
        .badge-metrica {
            display: inline-block;
            background-color: #E8F5E9;
            border: 1px solid #C8E6C9;
            border-radius: 6px;
            padding: 3px 8px;
            font-family: monospace;
            font-size: 12px;
            font-weight: 700;
            color: #1B5E20;
            margin: 2px 2px;
        }
        .cita-apa {
            padding-left: 20px;
            text-indent: -20px;
            margin-bottom: 10px;
            line-height: 1.4;
            font-size: 13px;
            color: #374151;
        }
        .pregunta-cun {
            padding: 8px 12px;
            border-radius: 6px;
            font-style: italic;
            font-size: 13px;
            margin: 4px 0;
            line-height: 1.4;
        }
        .pregunta-op1 {
            background-color: #fffef0;
            border-left: 4px solid #ffc107;
            color: #5a4400;
        }
        .pregunta-op2 {
            background-color: #f0f5ff;
            border-left: 4px solid #0d6efd;
            color: #003380;
        }
        .label-pregunta {
            font-size: 0.6rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .label-pregunta-op1 { color: #856404; }
        .label-pregunta-op2 { color: #004085; }
        
        /* CUN360 */
        .cun360-header {
            background: linear-gradient(135deg, #0d5a2a, #1a7a3a, #2e9e4e);
            padding: 25px 30px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        }
        .cun360-card-beneficio {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            height: 100%;
            border: 1px solid #e8e8e8;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: transform 0.2s ease;
        }
        .cun360-card-beneficio:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        }
        .cun360-justificacion {
            background-color: #f8faf9;
            border-left: 5px solid #1a7a3a;
            padding: 18px 22px;
            border-radius: 8px;
            margin: 15px 0;
        }
        
        /* Modal ejemplo */
        .modal-ejemplo-header {
            background: linear-gradient(135deg, #f8faf9, #e8f5e9);
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 16px;
            border: 1px solid #c8e6c9;
        }
        .modal-ejemplo-header span { font-weight: 600; color: #1a7a3a; }
        .modal-barra-container {
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 6px 0;
        }
        .modal-barra-label {
            min-width: 160px;
            font-size: 0.82rem;
            font-weight: 600;
            color: #333;
        }
        .modal-barra-bg {
            flex: 1;
            height: 20px;
            background-color: #e8e8e8;
            border-radius: 10px;
            overflow: hidden;
        }
        .modal-barra-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 0.6s ease;
        }
        .modal-barra-valor {
            min-width: 35px;
            font-weight: 700;
            font-size: 0.85rem;
            text-align: right;
        }
        .modal-barra-badge {
            font-size: 0.7rem;
            font-weight: 700;
            padding: 2px 10px;
            border-radius: 12px;
            min-width: 30px;
            text-align: center;
        }
        .modal-barra-badge-verde { background-color: #86efac; color: #065f46; }
        .modal-barra-badge-amarillo { background-color: #fcd34d; color: #92400e; }
        .modal-barra-badge-rojo { background-color: #fca5a5; color: #7f1d1d; }
        .modal-resumen-card {
            background-color: #f8faf9;
            border-radius: 10px;
            padding: 16px 20px;
            border: 1px solid #e0e0e0;
        }
        .modal-fortaleza { color: #065f46; padding: 4px 0; }
        .modal-mejora { color: #7f1d1d; padding: 4px 0; }
        .modal-recomendacion {
            background-color: #f0f7ff;
            border-left: 4px solid #1a7a3a;
            padding: 12px 16px;
            border-radius: 6px;
            margin: 6px 0;
        }
        .modal-recomendacion strong { color: #1a7a3a; }
        .modal-recomendacion ul { margin: 4px 0 0 0; padding-left: 20px; font-size: 0.85rem; }
        .modal-recomendacion li { margin: 2px 0; }
    </style>
    """,
        unsafe_allow_html=True,
    )


def renderizar_banner_principal():
    """Renderiza el banner principal de la aplicación."""
    st.markdown(
        """
    <div class="banner-cun">
        <h2 style="margin: 0; color: white; font-family: 'Montserrat', sans-serif; font-weight: 800;">📊 Inteligencia Académica CUN</h2>
        <p style="margin: 8px 0 0 0; font-size: 1.05rem; font-family: 'Montserrat', sans-serif; font-weight: 300;">
            Analítica avanzada de grabaciones para la toma de decisiones directivas y fortalecimiento del Capital Social
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def renderizar_version_preguntas():
    """Renderiza el encabezado con las dos versiones de preguntas."""
    st.markdown("### 📝 Versiones de las preguntas CUN Experience")

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown(
            """
        <div style="background-color: #fff3cd; padding: 12px 16px; border-radius: 10px; border: 2px solid #ffc107;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 24px;">🎓</span>
                <div>
                    <div style="font-weight: 700; color: #856404;">Opción 1: Versión Estudiantil</div>
                    <div style="font-size: 0.8rem; color: #856404;">Lenguaje informal / coloquial Bogotá<br>Para estudiantes 15-25 años en LMS/móvil</div>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col_v2:
        st.markdown(
            """
        <div style="background-color: #cce5ff; padding: 12px 16px; border-radius: 10px; border: 2px solid #0d6efd;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 24px;">📋</span>
                <div>
                    <div style="font-weight: 700; color: #004085;">Opción 2: Versión Ejecutiva</div>
                    <div style="font-size: 0.8rem; color: #004085;">Lenguaje formal / institucional<br>Para informes ejecutivos y acreditación</div>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    st.divider()


def renderizar_proposito_estrategico():
    """Renderiza el propósito estratégico para docentes y Capital Social."""
    st.markdown("### 🎯 Propósito del Ecosistema Integrado")
    col_doc, col_th = st.columns(2)
    with col_doc:
        st.info("""
        **👨‍🏫 Para los Docentes:**
        * Conocer el diagnóstico objetivo de sus clases grabadas.
        * Recibir retroalimentación técnica, vocal y pedagógica.
        * Guiar su plan de mejora continua de forma constructiva.
        """)
    with col_th:
        st.success("""
        **🏢 Para Talento Humano y Capital Social:**
        * Triangular encuestas de percepción con métricas duras de IA.
        * Diseñar programas de formación docente a la medida.
        * Fortalecer la excelencia académica institucional en la CUN.
        """)
    st.divider()


def renderizar_justificacion_pedagogica():
    """Renderiza la justificación pedagógica con los 4 pilares y ambas versiones de preguntas."""
    st.markdown(
        """
        <div class="banner-pedagogico">
            <h2 style="color: white; margin: 0;">🎓 Fundamentación Neuropedagógica y Modelo MALA</h2>
            <p style="margin-top: 6px; font-size: 15px; opacity: 0.95;">
                Integración de la percepción del estudiante (CUN Experience) con métricas objetivas de IA
            </p>
            <div style="margin-top: 10px; display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
                <span><span class="badge-opcion badge-opcion-1">🎓 Opción 1: Estudiantil (Informal)</span></span>
                <span><span class="badge-opcion badge-opcion-2">📋 Opción 2: Ejecutiva (Formal)</span></span>
            </div>
        </div>
        <div class="flecha-conector">▼</div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("""
    El modelo de evaluación docente de la **CUN** trasciende la simple percepción subjetiva. Articula la 
    evaluación de los estudiantes con la **Analítica Multimodal del Aprendizaje (MALA)**, sustentando cada pregunta 
    de encuesta y cada parámetro de Inteligencia Artificial en **4 Pilares Pedagógicos fundamentales**.
    """)
    st.write("")

    col1, col2 = st.columns(2)
    p1a, p1b = obtener_preguntas("P1")
    p2a, p2b = obtener_preguntas("P2")
    p3a, p3b = obtener_preguntas("P3")
    p4a, p4b = obtener_preguntas("P4")

    with col1:
        st.markdown(
            f"""
            <div class="tarjeta-pilar" style="border-left-color: #10B981;">
                <div class="circulo-icono circulo-verde">1</div>
                <h4 style="margin: 0 0 6px 0; color: #065F46;">Aprendizaje Activo y Socio-Constructivismo</h4>
                <div style="margin: 6px 0;">
                    <div class="pregunta-cun pregunta-op1"><span class="label-pregunta label-pregunta-op1">🎓 Opción 1:</span> {p1a}</div>
                    <div class="pregunta-cun pregunta-op2"><span class="label-pregunta label-pregunta-op2">📋 Opción 2:</span> {p1b}</div>
                </div>
                <hr style="margin: 8px 0;">
                <p style="font-size: 12.5px; color: #4B5563;">
                    <b>🧠 Sustento:</b> Las exposiciones ininterrumpidas mayores a 10 min inducen acomodación pasiva. El aprendizaje activo requiere que el estudiante procese y argumente en memoria de trabajo (Vygotsky, 1978; Flanders, 1970).
                </p>
                <p style="font-size: 12px; margin-top: 6px; margin-bottom: 0;">
                    <b>⚙️ Métricas de IA:</b> 
                    <span class="badge-metrica">DME_s &lt; 3.5s</span>
                    <span class="badge-metrica">DTE_ratio ≤ 50%</span>
                </p>
            </div>
            <div class="tarjeta-pilar" style="border-left-color: #3B82F6;">
                <div class="circulo-icono circulo-azul">3</div>
                <h4 style="margin: 0 0 6px 0; color: #1E40AF;">Cognición Encarnada y Presencia Social</h4>
                <div style="margin: 6px 0;">
                    <div class="pregunta-cun pregunta-op1"><span class="label-pregunta label-pregunta-op1">🎓 Opción 1:</span> {p3a}</div>
                    <div class="pregunta-cun pregunta-op2"><span class="label-pregunta label-pregunta-op2">📋 Opción 2:</span> {p3b}</div>
                </div>
                <hr style="margin: 8px 0;">
                <p style="font-size: 12.5px; color: #4B5563;">
                    <b>🧠 Sustento:</b> Según la <i>Embodied Cognition</i> (Barsalou, 2008), los conceptos abstractos se comprenden mejor acompañados de gesticulación no verbal. Una imagen fija o estática genera frialdad y distanciamiento pedagógico.
                </p>
                <p style="font-size: 12px; margin-top: 6px; margin-bottom: 0;">
                    <b>⚙️ Métricas de IA:</b> 
                    <span class="badge-metrica">IMP_promedio &gt; 4.0</span>
                    <span class="badge-metrica">sigma2_IM &gt; 8.5</span>
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="tarjeta-pilar" style="border-left-color: #F59E0B;">
                <div class="circulo-icono circulo-amarillo">2</div>
                <h4 style="margin: 0 0 6px 0; color: #92400E;">Neuroeducación y Captura de la Atención</h4>
                <div style="margin: 6px 0;">
                    <div class="pregunta-cun pregunta-op1"><span class="label-pregunta label-pregunta-op1">🎓 Opción 1:</span> {p2a}</div>
                    <div class="pregunta-cun pregunta-op2"><span class="label-pregunta label-pregunta-op2">📋 Opción 2:</span> {p2b}</div>
                </div>
                <hr style="margin: 8px 0;">
                <p style="font-size: 12.5px; color: #4B5563;">
                    <b>🧠 Sustento:</b> El sistema atencional (SARA) filtra tonos monótonos para ahorrar energía metabólica. Las modulaciones de entonación e intensidad actúan como estímulos re-activadores de la atención (Scherer, 2003).
                </p>
                <p style="font-size: 12px; margin-top: 6px; margin-bottom: 0;">
                    <b>⚙️ Métricas de IA:</b> 
                    <span class="badge-metrica">Tone_CoV &gt; 0.32</span>
                    <span class="badge-metrica">Enthusiasm &gt; 0.15</span>
                </p>
            </div>
            <div class="tarjeta-pilar" style="border-left-color: #8B5CF6;">
                <div class="circulo-icono circulo-morado">4</div>
                <h4 style="margin: 0 0 6px 0; color: #5B21B6;">Teoría de la Carga Cognitiva Extraña</h4>
                <div style="margin: 6px 0;">
                    <div class="pregunta-cun pregunta-op1"><span class="label-pregunta label-pregunta-op1">🎓 Opción 1:</span> {p4a}</div>
                    <div class="pregunta-cun pregunta-op2"><span class="label-pregunta label-pregunta-op2">📋 Opción 2:</span> {p4b}</div>
                </div>
                <hr style="margin: 8px 0;">
                <p style="font-size: 12.5px; color: #4B5563;">
                    <b>🧠 Sustento:</b> Fallas técnicas, video pixelado o congelamientos imponen "carga extraña" a la memoria de trabajo (Sweller, 1988), impidiendo que el estudiante procese el contenido académico real.
                </p>
                <p style="font-size: 12px; margin-top: 6px; margin-bottom: 0;">
                    <b>⚙️ Métricas de IA:</b> 
                    <span class="badge-metrica">Jitter_Score &gt; 0.40</span>
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    # Matriz de triangulación
    with st.expander(
        "📊 Matriz General de Triangulación (Percepción Estudiantil vs. Métrica IA)",
        expanded=False,
    ):
        st.markdown(f"""
        | Pregunta *CUN Experience* | Pilar Pedagógico | Modelo de IA / Métrica | Umbral Aceptable | Diagnóstico |
        | :--- | :--- | :--- | :--- | :--- |
        | **🎓 Opción 1:** {p1a}<br>**📋 Opción 2:** {p1b} | Aprendizaje Activo | `DME_s` / `DTE_ratio` | $< 3.5\\text{{s}}$ / $\\le 50\\%$ | Fomenta participación vs. Cátedra expositiva |
        | **🎓 Opción 1:** {p2a}<br>**📋 Opción 2:** {p2b} | Neuroeducación | `Tone_CoV` / `Enthusiasm` | $> 0.32$ / $> 0.15$ | Excelente entonación vs. Tono monótono |
        | **🎓 Opción 1:** {p3a}<br>**📋 Opción 2:** {p3b} | Cognición Encarnada | `IMP_promedio` / `sigma2_IM` | $> 4.0$ / $> 8.5$ | Cercanía vs. Docente estático |
        | **🎓 Opción 1:** {p4a}<br>**📋 Opción 2:** {p4b} | Carga Cognitiva | `Jitter_Score` | $> 0.40$ | Transmisión fluida vs. Soporte técnico |
        """)

    with st.expander(
        "📚 Respaldo Bibliográfico Oficial (APA 7.ª Edición)", expanded=False
    ):
        st.markdown(
            """
            <div class="cita-apa">
                Barsalou, L. W. (2008). Grounded cognition. <i>Annual Review of Psychology</i>, 59, 617–645. 
                <a href="https://doi.org/10.1146/annurev.psych.59.103006.093639" target="_blank">https://doi.org/10.1146/annurev.psych.59.103006.093639</a>
            </div>
            <div class="cita-apa">
                Flanders, N. A. (1970). <i>Analyzing teaching behavior</i>. Addison-Wesley.
            </div>
            <div class="cita-apa">
                Immordino-Yang, M. H., & Damasio, A. (2007). We feel, therefore we learn: The relevance of affective and social neuroscience to education. <i>Mind, Brain, and Education</i>, 1(1), 3–10. 
                <a href="https://doi.org/10.1111/j.1751-228X.2007.00004.x" target="_blank">https://doi.org/10.1111/j.1751-228X.2007.00004.x</a>
            </div>
            <div class="cita-apa">
                Scherer, K. R. (2003). Vocal communication of emotion: A review of research paradigms. <i>Speech Communication</i>, 40(1-2), 227–256. 
                <a href="https://doi.org/10.1016/S0167-6393(02)00084-5" target="_blank">https://doi.org/10.1016/S0167-6393(02)00084-5</a>
            </div>
            <div class="cita-apa">
                Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. <i>Cognitive Science</i>, 12(2), 257–285. 
                <a href="https://doi.org/10.1207/s15516709cog1202_4" target="_blank">https://doi.org/10.1207/s15516709cog1202_4</a>
            </div>
            """,
            unsafe_allow_html=True,
        )


def renderizar_tarjeta(clave_modelo: str):
    """Renderiza una tarjeta ejecutiva para un modelo de IA específico."""
    info = MODELOS_INFO[clave_modelo]
    pregunta_key = info.get("pregunta_key", "")
    p1, p2 = (
        obtener_preguntas(pregunta_key)
        if pregunta_key
        else ("Pregunta no asociada", "Pregunta no asociada")
    )

    html_card = f"""
    <div class="card-container">
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="card-header-title">{info['icono']} {info['nombre_gerencial']}</span>
                <span class="card-badge">{clave_modelo}</span>
            </div>
            <div class="card-pilar-text">{info['pilar']}</div>
            <p class="card-body-text">{info['resumen']}</p>
            <div style="margin-top: 4px;">
                <div class="card-pregunta card-pregunta-op1">
                    <span class="label-opcion label-op1">🎓 Opción 1:</span> {p1}
                </div>
                <div class="card-pregunta card-pregunta-op2">
                    <span class="label-opcion label-op2">📋 Opción 2:</span> {p2}
                </div>
            </div>
        </div>
        <div>
            <div class="card-rule">
                🟢 <b>Aceptable:</b> {info['bueno']} <br>
                🔴 <b>Atención:</b> {info['malo']}
            </div>
        </div>
    </div>
    """
    st.markdown(html_card, unsafe_allow_html=True)
    if st.button(
        "🔬 Ver fundamento completo",
        key=f"btn_{clave_modelo}",
        use_container_width=True,
    ):
        mostrar_modal_modelo(clave_modelo)


@st.dialog("🔬 Fundamento Neuro-Pedagógico y Analítica de IA")
def mostrar_modal_modelo(clave_modelo: str):
    """Modal con el fundamento científico completo de un modelo."""
    info = MODELOS_INFO[clave_modelo]
    pregunta_key = info.get("pregunta_key", "")
    p1, p2 = (
        obtener_preguntas(pregunta_key)
        if pregunta_key
        else ("Pregunta no asociada", "Pregunta no asociada")
    )

    st.markdown(f"### {info['icono']} {info['nombre_gerencial']} (`{clave_modelo}`)")
    st.caption(f"Categoría: **{info['categoria']}** | Pilar: **{info['pilar']}**")
    st.markdown("---")
    st.markdown("#### ❓ Preguntas del Instrumento (*CUN Experience*)")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("**🎓 Opción 1 (Estudiantil - Informal):**")
        st.info(f"{p1}")
    with col_m2:
        st.markdown("**📋 Opción 2 (Ejecutiva - Formal):**")
        st.info(f"{p2}")
    st.markdown("#### 🧠 Sustento Neuro-Pedagógico de la Pregunta")
    st.write(info["sustento_neuropedagogico"])
    st.markdown("---")
    st.markdown("#### ⚙️ Modelo de IA y Parámetro Algorítmico")
    st.write(info["resumen"])
    st.write(f"**¿Qué evalúa en el aula?:** {info['evalua']}")
    col_b, col_m = st.columns(2)
    with col_b:
        st.success(f"🟢 **Rango Aceptable (Bueno):**\n\n`{info['bueno']}`")
    with col_m:
        st.error(f"🔴 **Rango Crítico (Atención):**\n\n`{info['malo']}`")
    st.markdown("---")
    st.markdown("#### 📚 Soporte Científico y Referencia APA 7")
    st.write(f"**Investigadores / Referentes:** {info['autores']}")
    st.markdown(f"**Cita Bibliográfica:**\n> *{info['cita_apa']}*")
    st.markdown(
        f'<a href="{info["doi"]}" target="_blank" style="text-decoration: none;">'
        f'<button style="background-color: #1a7a3a; color: white; border: none; padding: 8px 15px; '
        f'border-radius: 5px; cursor: pointer; font-family: Montserrat, sans-serif; font-weight: 600;">🔗 Consultar Publicación Científica (DOI)</button></a>',
        unsafe_allow_html=True,
    )


def renderizar_modelos_ia():
    """Renderiza la sección de modelos analíticos y tarjetas."""
    st.markdown("### 🔬 Modelos Analíticos y Métricas de IA")
    st.write(
        "A continuación se detallan los 7 modelos multimodales asociados a los pilares pedagógicos y preguntas de evaluación:"
    )

    cols = st.columns(3)
    for index, clave in enumerate(MODELOS_INFO.keys()):
        with cols[index % 3]:
            renderizar_tarjeta(clave)


def renderizar_seccion_cun360():
    """Renderiza la sección CUN360 con justificación, objetivos y botón para ver ejemplo."""
    st.markdown(
        """
        <div class="cun360-header">
            <h2>🏢 CUN360 - Ecosistema de Evaluación y Desarrollo Docente</h2>
            <p>Transformamos la evaluación en una herramienta de crecimiento continuo</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="cun360-justificacion">
            <p style="font-size: 1.05rem; font-weight: 600; color: #1a7a3a; margin-bottom: 8px;">
                📌 ¿Por qué CUN360?
            </p>
            <p>
                <b>La retroalimentación continua mejora la práctica docente.</b> CUN360 es un ecosistema 
                integral que almacena los resultados de la evaluación docente (percepción estudiantil + métricas 
                de IA) para ofrecer <b>retroalimentación personalizada, seguimiento evolutivo y datos 
                accionables</b> para la toma de decisiones institucionales.
            </p>
            <p style="margin-top: 8px; font-size: 0.92rem; color: #4a5568;">
                <b>Referente:</b> Hattie, J. (2012). <i>Visible Learning for Teachers</i>. Routledge.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_doc, col_rh = st.columns(2)
    with col_doc:
        st.markdown(
            """
            <div class="cun360-card-beneficio">
                <h4>🎓 Para el Docente</h4>
                <ul>
                    <li>✅ <b>Calificación por clase:</b> Nota numérica y semáforo para cada clase grabada</li>
                    <li>✅ <b>Calificación estudiantes:</b> Promedio de respuestas de la encuesta CUN Experience</li>
                    <li>✅ <b>Calificación IA:</b> Puntaje objetivo generado por los modelos MALA</li>
                    <li>✅ <b>Calificación Global:</b> Puntaje combinado (estudiantes + IA) ponderado</li>
                    <li>✅ <b>Evolución temporal:</b> Gráfica de mejora o decrecimiento en el tiempo</li>
                    <li>✅ <b>Recomendaciones personalizadas:</b> Sugerencias accionables para cada métrica</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_rh:
        st.markdown(
            """
            <div class="cun360-card-beneficio">
                <h4>🏢 Para Capital Social (RH)</h4>
                <ul>
                    <li>✅ <b>Tablero Power BI:</b> Dashboard interactivo con todos los indicadores agregados</li>
                    <li>✅ <b>Ranking de docentes:</b> Listado con mejor desempeño y mayor progreso</li>
                    <li>✅ <b>Filtros avanzados:</b> Por facultad, programa, asignatura, rango de fechas</li>
                    <li>✅ <b>Alertas tempranas:</b> Detección de docentes que requieren apoyo urgente</li>
                    <li>✅ <b>Programas de formación:</b> Generación automática de recomendaciones formativas</li>
                    <li>✅ <b>Dashboard de acreditación:</b> Evidencia objetiva para procesos de acreditación</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### 🎯 Objetivos del Ecosistema CUN360")

    col_obj1, col_obj2 = st.columns(2)
    with col_obj1:
        st.markdown(
            """
            <div style="background-color: #f0fdf4; padding: 16px 20px; border-radius: 10px; border: 1px solid #86efac; height: 100%;">
                <h5 style="color: #065f46; margin: 0 0 8px 0;">🎓 Para el Docente</h5>
                <ul style="font-size: 0.9rem; color: #333; line-height: 1.8; padding-left: 20px; margin: 0;">
                    <li>Empoderar al docente con datos objetivos sobre su práctica</li>
                    <li>Fomentar una cultura de mejora continua y autoevaluación</li>
                    <li>Reducir la ansiedad de la evaluación al hacerla transparente</li>
                    <li>Proveer retroalimentación accionable (no solo una nota, qué hacer)</li>
                    <li>Reconocer y visibilizar las buenas prácticas docentes</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_obj2:
        st.markdown(
            """
            <div style="background-color: #eff6ff; padding: 16px 20px; border-radius: 10px; border: 1px solid #93c5fd; height: 100%;">
                <h5 style="color: #1e40af; margin: 0 0 8px 0;">🏢 Para Capital Social</h5>
                <ul style="font-size: 0.9rem; color: #333; line-height: 1.8; padding-left: 20px; margin: 0;">
                    <li>Transformar la gestión del talento docente de reactiva a proactiva</li>
                    <li>Reducir la deserción y mejorar la retención de profesores</li>
                    <li>Asegurar estándares mínimos de calidad docente</li>
                    <li>Crear un banco de mejores prácticas docentes para compartir</li>
                    <li>Posicionar a la CUN como líder en innovación educativa</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; margin: 20px 0 10px 0;">
            <p style="font-size: 0.95rem; color: #555; margin-bottom: 12px;">
                🔍 Explora cómo se vería la calificación de una clase en CUN Experience
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "📊 Ver ejemplo de calificación de una clase",
        key="btn_modal_ejemplo",
        use_container_width=True,
    ):
        mostrar_modal_ejemplo_calificacion()


@st.dialog("🔬 Ejemplo de Calificación CUN Experience - Clase Individual")
def mostrar_modal_ejemplo_calificacion():
    """Modal que muestra un ejemplo detallado de calificación de una clase."""

    ejemplo = {
        "docente": "Juan Pérez",
        "asignatura": "Cálculo I",
        "fecha": "15/05/2026",
        "duracion": "90 min",
        "calificaciones": {
            "P1_Aprendizaje_Activo": 8.5,
            "P2_Neuroeducacion": 6.2,
            "P3_Cognicion_Encarnada": 9.1,
            "P4_Carga_Cognitiva": 4.3,
        },
        "metricas_ia": {
            "DME_s": 2.8,
            "DTE_ratio": 0.42,
            "Tone_CoV": 0.28,
            "Enthusiasm_Score": 0.12,
            "IMP_promedio": 5.2,
            "sigma2_IM": 9.8,
            "Jitter_Score": 0.35,
        },
        "global": 7.0,
        "estado": "Aceptable",
    }

    # Encabezado
    st.markdown(
        f"""
        <div class="modal-ejemplo-header">
            <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                <span>👨‍🏫 {ejemplo['docente']}</span>
                <span>📚 {ejemplo['asignatura']}</span>
                <span>📅 {ejemplo['fecha']}</span>
                <span>⏱️ {ejemplo['duracion']}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Gráfico y barras
    col_radar, col_barras = st.columns([1, 1.2])

    with col_radar:
        st.markdown("#### 🕷️ Métricas IA (Modelos)")
        try:
            import plotly.graph_objects as go

            categorias = [
                "Monólogo",
                "Expresividad",
                "Energía",
                "Interacción",
                "Presencia",
                "Dinamismo",
                "Estabilidad",
            ]
            valores = [
                max(0, min(10, 10 - ejemplo["metricas_ia"]["DME_s"])),
                max(0, min(10, ejemplo["metricas_ia"]["Tone_CoV"] * 31.25)),
                max(0, min(10, ejemplo["metricas_ia"]["Enthusiasm_Score"] * 66.67)),
                max(0, min(10, (1 - ejemplo["metricas_ia"]["DTE_ratio"]) * 20)),
                max(0, min(10, ejemplo["metricas_ia"]["IMP_promedio"] * 1.92)),
                max(0, min(10, ejemplo["metricas_ia"]["sigma2_IM"] * 1.02)),
                max(0, min(10, ejemplo["metricas_ia"]["Jitter_Score"] * 25)),
            ]
            fig = go.Figure(
                data=go.Scatterpolar(
                    r=valores,
                    theta=categorias,
                    fill="toself",
                    line=dict(color="#1a7a3a", width=2),
                    fillcolor="rgba(26, 122, 58, 0.25)",
                    name="Métricas IA",
                )
            )
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10],
                        tickfont=dict(size=9),
                        gridcolor="#e0e0e0",
                    ),
                    angularaxis=dict(
                        tickfont=dict(size=10, color="#1a7a3a"), gridcolor="#e0e0e0"
                    ),
                ),
                showlegend=False,
                height=320,
                margin=dict(l=30, r=30, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(
                fig, use_container_width=True, config={"displayModeBar": False}
            )
        except ImportError:
            st.warning("⚠️ Instala plotly: `pip install plotly`")
            for key, value in ejemplo["metricas_ia"].items():
                st.write(f"• `{key}`: {value}")

    with col_barras:
        st.markdown("#### 📝 Calificaciones por Pregunta")
        preguntas = [
            (
                "P1 - Aprendizaje Activo",
                ejemplo["calificaciones"]["P1_Aprendizaje_Activo"],
            ),
            ("P2 - Neuroeducación", ejemplo["calificaciones"]["P2_Neuroeducacion"]),
            (
                "P3 - Cognición Encarnada",
                ejemplo["calificaciones"]["P3_Cognicion_Encarnada"],
            ),
            ("P4 - Carga Cognitiva", ejemplo["calificaciones"]["P4_Carga_Cognitiva"]),
        ]
        for label, valor in preguntas:
            if valor >= 8.5:
                color, badge, badge_class = (
                    "#22c55e",
                    "🟢 Excelente",
                    "modal-barra-badge-verde",
                )
            elif valor >= 6.0:
                color, badge, badge_class = (
                    "#eab308",
                    "🟡 Aceptable",
                    "modal-barra-badge-amarillo",
                )
            else:
                color, badge, badge_class = (
                    "#ef4444",
                    "🔴 Atención",
                    "modal-barra-badge-rojo",
                )
            porcentaje = (valor / 10) * 100
            st.markdown(
                f"""
                <div class="modal-barra-container">
                    <div class="modal-barra-label">{label}</div>
                    <div class="modal-barra-bg">
                        <div class="modal-barra-fill" style="width: {porcentaje}%; background-color: {color};"></div>
                    </div>
                    <div class="modal-barra-valor">{valor:.1f}</div>
                    <span class="modal-barra-badge {badge_class}">{badge}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # Resumen ejecutivo
    st.markdown("#### 📈 Resumen Ejecutivo")
    col_global, col_estado, col_ratio = st.columns(3)
    with col_global:
        st.metric(
            label="Calificación Global",
            value=f"{ejemplo['global']:.1f}",
            delta="+" if ejemplo["global"] >= 6.0 else "-",
        )
    with col_estado:
        estado_icono = (
            "🟢"
            if ejemplo["global"] >= 8.5
            else "🟡" if ejemplo["global"] >= 6.0 else "🔴"
        )
        st.markdown(
            f"""
            <div style="background-color: #f8faf9; padding: 12px 16px; border-radius: 8px; text-align: center; height: 100%;">
                <p style="margin: 0; font-size: 0.75rem; color: #666;">Estado General</p>
                <p style="margin: 0; font-size: 1.6rem; font-weight: 700;">{estado_icono}</p>
                <p style="margin: 0; font-size: 0.85rem; font-weight: 600; color: #333;">{ejemplo['estado']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_ratio:
        aprobadas = sum(1 for v in ejemplo["calificaciones"].values() if v >= 6.0)
        total = len(ejemplo["calificaciones"])
        st.metric(
            label="Métricas aprobadas",
            value=f"{aprobadas}/{total}",
            delta=f"{int((aprobadas/total)*100)}%",
        )

    st.markdown("---")

    # Fortalezas y áreas de mejora
    col_fort, col_mej = st.columns(2)
    sorted_calif = sorted(
        ejemplo["calificaciones"].items(), key=lambda x: x[1], reverse=True
    )

    with col_fort:
        st.markdown("#### ✅ Fortalezas")
        for key, valor in sorted_calif[:2]:
            nombre = (
                key.replace("_", " ")
                .replace("P1", "P1 -")
                .replace("P2", "P2 -")
                .replace("P3", "P3 -")
                .replace("P4", "P4 -")
            )
            st.markdown(
                f'<div class="modal-fortaleza">✅ {nombre}: <span style="font-weight: 700; color: #22c55e;">{valor:.1f}</span></div>',
                unsafe_allow_html=True,
            )

    with col_mej:
        st.markdown("#### ⚠️ Áreas de mejora")
        for key, valor in sorted_calif[-2:]:
            nombre = (
                key.replace("_", " ")
                .replace("P1", "P1 -")
                .replace("P2", "P2 -")
                .replace("P3", "P3 -")
                .replace("P4", "P4 -")
            )
            st.markdown(
                f'<div class="modal-mejora">⚠️ {nombre}: <span style="font-weight: 700; color: #ef4444;">{valor:.1f}</span></div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # Recomendaciones
    st.markdown("#### 💡 Recomendaciones Personalizadas")
    st.markdown("*Basado en los resultados de esta clase, te sugerimos:*")

    recomendaciones = []
    if ejemplo["calificaciones"]["P4_Carga_Cognitiva"] < 6.0:
        recomendaciones.append(
            {
                "area": "🔧 Estabilidad Técnica (P4)",
                "sugerencias": [
                    "Verifica tu conexión a internet antes de cada clase",
                    "Prueba el equipo de audio/video 10 minutos antes",
                    "Ten un plan B por si falla la conexión",
                ],
            }
        )
    if ejemplo["calificaciones"]["P2_Neuroeducacion"] < 6.0:
        recomendaciones.append(
            {
                "area": "🗣️ Neuroeducación y Atención (P2)",
                "sugerencias": [
                    "Varía más el tono de voz durante la explicación",
                    "Usa preguntas retóricas para mantener la atención",
                    "Incorpora cambios de ritmo: rápido/lento, alto/bajo",
                ],
            }
        )
    if ejemplo["calificaciones"]["P1_Aprendizaje_Activo"] < 6.0:
        recomendaciones.append(
            {
                "area": "🤝 Aprendizaje Activo (P1)",
                "sugerencias": [
                    "Haz pausas cada 10-15 minutos para preguntas",
                    "Incorpora ejercicios prácticos cortos",
                    "Usa la técnica 'Think-Pair-Share'",
                ],
            }
        )
    if ejemplo["calificaciones"]["P3_Cognicion_Encarnada"] < 6.0:
        recomendaciones.append(
            {
                "area": "🧍 Cognición Encarnada (P3)",
                "sugerencias": [
                    "Gesticula más al explicar conceptos clave",
                    "Mantén contacto visual con la cámara",
                    "Varía tu posición frente a la cámara",
                ],
            }
        )

    if not recomendaciones:
        st.success("🎉 ¡Excelente desempeño en todas las áreas! Sigue así.")
    else:
        for rec in recomendaciones:
            st.markdown(
                f"""
                <div class="modal-recomendacion">
                    <strong>{rec['area']}</strong>
                    <ul>{''.join([f'<li>{s}</li>' for s in rec['sugerencias']])}</ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("#### 📚 Recursos Recomendados")
    col_rec1, col_rec2 = st.columns(2)
    with col_rec1:
        st.markdown(
            """
        <div style="background-color: #f0fdf4; padding: 12px 16px; border-radius: 8px; border: 1px solid #86efac;">
            <p style="margin: 0; font-weight: 600; color: #065f46;">📹 Videos Formativos</p>
            <ul style="font-size: 0.85rem; margin: 4px 0 0 0; padding-left: 20px;">
                <li>"Cómo mejorar tu presencia en cámara"</li>
                <li>"Técnicas de comunicación efectiva"</li>
                <li>"Estrategias de aprendizaje activo"</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col_rec2:
        st.markdown(
            """
        <div style="background-color: #eff6ff; padding: 12px 16px; border-radius: 8px; border: 1px solid #93c5fd;">
            <p style="margin: 0; font-weight: 600; color: #1e40af;">📖 Lecturas Recomendadas</p>
            <ul style="font-size: 0.85rem; margin: 4px 0 0 0; padding-left: 20px;">
                <li>Hattie - "Visible Learning"</li>
                <li>Barsalou - "Grounded Cognition"</li>
                <li>Sweller - "Cognitive Load Theory"</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.caption(
        "💡 Este es un ejemplo ilustrativo. Los datos reales provendrán de las grabaciones de clase."
    )


def renderizar_footer():
    """Renderiza el footer de la aplicación."""
    st.markdown("---")
    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f2:
        st.markdown(
            """
            <div style="text-align: center; padding: 20px 0 10px 0;">
                <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; margin-bottom: 10px;">
                    <span style="color: #1a7a3a; font-weight: 600;">📊 CUN Experience</span>
                    <span style="color: #666;">|</span>
                    <span style="color: #1a7a3a; font-weight: 600;">🤖 MALA Analytics</span>
                    <span style="color: #666;">|</span>
                    <span style="color: #1a7a3a; font-weight: 600;">🧠 Neuroeducación</span>
                </div>
                <p style="color: #888; font-size: 0.8rem; margin: 0;">
                    © 2026 CUN - Corporación Unificada Nacional de Educación Superior
                </p>
                <p style="color: #aaa; font-size: 0.7rem; margin: 4px 0 0 0;">
                    Desarrollado con ❤️ para el fortalecimiento del Capital Social y la Excelencia Docente
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ====================================================================
# FUNCIÓN PRINCIPAL
# ====================================================================
def main(df_filtrado=None):
    """Función principal que orquesta todas las secciones de la aplicación."""
    inyectar_estilos()
    renderizar_banner_principal()
    renderizar_version_preguntas()
    renderizar_proposito_estrategico()
    renderizar_justificacion_pedagogica()
    st.divider()
    renderizar_modelos_ia()
    st.divider()
    renderizar_seccion_cun360()
    renderizar_footer()


# ====================================================================
# EJECUCIÓN PRINCIPAL
# ====================================================================
if __name__ == "__main__":
    main()
