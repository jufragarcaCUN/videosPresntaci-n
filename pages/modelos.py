# pages/modelos.py

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np


def calcular_cumplimiento(valor, limite, condicion):
    if pd.isna(valor):
        return np.nan
    try:
        val = float(str(valor).replace(",", "."))
    except:
        return np.nan
    if condicion in ["mayor", "mayor_igual"]:
        pct = (val / limite) * 100 if limite != 0 else 100.0
    elif condicion in ["menor", "menor_igual"]:
        pct = (limite / val) * 100 if val != 0 else 100.0
    else:
        return np.nan
    return float(np.clip(pct, 0.0, 100.0))


METRICAS_CONFIG = {
    "DME_s": {"nombre": "Duración del monólogo", "limite": 3.5, "condicion": "menor"},
    "DTE_ratio": {"nombre": "Porcentaje de habla", "limite": 0.5, "condicion": "menor_igual"},
    "Tone_CoV": {"nombre": "Variación de la voz", "limite": 0.32, "condicion": "mayor"},
    "sigma2_IM": {"nombre": "Cambios de movimiento", "limite": 8.5, "condicion": "mayor"},
    "Jitter_Score": {"nombre": "Estabilidad técnica", "limite": 0.4, "condicion": "mayor"},
    "IMP_promedio": {"nombre": "Movimiento promedio", "limite": 4.0, "condicion": "mayor"},
    "Enthusiasm_Score": {"nombre": "Nivel de energía", "limite": 0.15, "condicion": "mayor"},
}


def altura():
    return st.session_state.get("altura_grafica", 600)


def calcular_percentiles(df, columna_modelo, columna_agrupacion=None, elemento=None):
    if df is None or df.empty or columna_modelo not in df.columns:
        return np.nan, np.nan, np.nan
    
    if columna_agrupacion and elemento and elemento != "Todos":
        df_filtrado = df[df[columna_agrupacion] == elemento]
    else:
        df_filtrado = df
    
    if df_filtrado.empty:
        return np.nan, np.nan, np.nan
    
    config = METRICAS_CONFIG.get(columna_modelo)
    if not config:
        return np.nan, np.nan, np.nan
    
    cumplimientos = []
    for _, row in df_filtrado.iterrows():
        valor = row[columna_modelo]
        if pd.isna(valor):
            continue
        try:
            valor = float(str(valor).replace(",", "."))
            pct = calcular_cumplimiento(valor, config["limite"], config["condicion"])
            if not pd.isna(pct):
                cumplimientos.append(pct)
        except:
            continue
    
    if not cumplimientos:
        return np.nan, np.nan, np.nan
    
    p25 = np.percentile(cumplimientos, 25)
    p50 = np.percentile(cumplimientos, 50)
    p75 = np.percentile(cumplimientos, 75)
    
    return p25, p50, p75


def obtener_datos_modelos(df, elementos, columna_agrupacion):
    if df is None or df.empty or columna_agrupacion not in df.columns:
        return {}
    
    resultados = {}
    for elemento in elementos:
        valores = {}
        for modelo in METRICAS_CONFIG.keys():
            if modelo in df.columns:
                p25, p50, p75 = calcular_percentiles(df, modelo, columna_agrupacion, elemento)
                valores[modelo] = {"P25": p25, "P50": p50, "P75": p75}
        resultados[elemento] = valores
    
    return resultados


def crear_mapa_calor(datos, titulo, altura=400):
    modelos = list(METRICAS_CONFIG.keys())
    nombres_modelos = [METRICAS_CONFIG[m]["nombre"] for m in modelos]
    
    if len(datos) == 1:
        elemento = list(datos.keys())[0]
        valores = datos[elemento]
        
        matriz = []
        for modelo in modelos:
            if modelo in valores:
                p25 = valores[modelo]["P25"]
                p50 = valores[modelo]["P50"]
                p75 = valores[modelo]["P75"]
                matriz.append([p25, p50, p75])
            else:
                matriz.append([np.nan, np.nan, np.nan])
        
        fig = px.imshow(
            matriz,
            x=["P25", "P50", "P75"],
            y=nombres_modelos,
            text_auto='.1f',
            color_continuous_scale=["#dc3545", "#ffc107", "#2e9e4e"],
            range_color=[0, 100],
            title=titulo,
            aspect="auto"
        )
        
        fig.update_layout(
            height=altura,
            xaxis_title="Percentil",
            yaxis_title="Modelo",
            font=dict(family="Montserrat, sans-serif"),
            paper_bgcolor='rgba(255,255,255,0.9)',
            plot_bgcolor='rgba(255,255,255,0.9)'
        )
        
        fig.update_traces(
            texttemplate='%{z:.1f}%',
            textfont=dict(color="white", size=12, family="Montserrat, sans-serif"),
            hovertemplate='<b>%{y}</b><br>%{x}: %{z:.1f}%<extra></extra>'
        )
        
        return fig
    
    else:
        st.warning("⚠️ Selecciona un solo elemento para ver el mapa de calor.")
        
        df_comparativa = pd.DataFrame()
        for elemento, valores in datos.items():
            for modelo in modelos:
                if modelo in valores:
                    p25 = valores[modelo]["P25"]
                    p50 = valores[modelo]["P50"]
                    p75 = valores[modelo]["P75"]
                    df_comparativa.loc[elemento, f"{modelo}_P25"] = p25
                    df_comparativa.loc[elemento, f"{modelo}_P50"] = p50
                    df_comparativa.loc[elemento, f"{modelo}_P75"] = p75
        
        st.dataframe(df_comparativa.round(1), use_container_width=True)
        return None


@st.dialog("🔍 Mapa de Calor - Ampliado", width="large")
def mostrar_modal_mapa_calor(datos, titulo):
    fig = crear_mapa_calor(datos, titulo, altura=600)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    st.caption("🔄 Cierra este modal para volver a la vista normal")


def mostrar_modelos_docentes(df, elementos_seleccionados, altura=350, show_modal=True):
    if df is None or df.empty:
        return
    if not elementos_seleccionados:
        elementos_seleccionados = ["Todos"]
    
    datos = obtener_datos_modelos(df, elementos_seleccionados, "nombres_apellidos")
    
    if not datos:
        st.info("No hay datos suficientes")
        return
    
    fig = crear_mapa_calor(datos, "📊 Mapa de Calor - Docentes", altura=altura)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    if show_modal and len(datos) == 1:
        if st.button("🔍 Ver más grande", key="modal_modelos_docentes", use_container_width=True):
            mostrar_modal_mapa_calor(datos, "📊 Mapa de Calor - Docentes")


def mostrar_modelos_programas(df, elementos_seleccionados, altura=350, show_modal=True):
    if df is None or df.empty:
        return
    if not elementos_seleccionados:
        elementos_seleccionados = ["Todos"]
    
    datos = obtener_datos_modelos(df, elementos_seleccionados, "area")
    
    if not datos:
        st.info("No hay datos suficientes")
        return
    
    fig = crear_mapa_calor(datos, "📊 Mapa de Calor - Programas", altura=altura)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    if show_modal and len(datos) == 1:
        if st.button("🔍 Ver más grande", key="modal_modelos_programas", use_container_width=True):
            mostrar_modal_mapa_calor(datos, "📊 Mapa de Calor - Programas")


def mostrar_modelos_materias(df, elementos_seleccionados, altura=350, show_modal=True):
    if df is None or df.empty:
        return
    if not elementos_seleccionados:
        elementos_seleccionados = ["Todos"]
    
    datos = obtener_datos_modelos(df, elementos_seleccionados, "nom_materia")
    
    if not datos:
        st.info("No hay datos suficientes")
        return
    
    fig = crear_mapa_calor(datos, "📊 Mapa de Calor - Materias", altura=altura)
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    if show_modal and len(datos) == 1:
        if st.button("🔍 Ver más grande", key="modal_modelos_materias", use_container_width=True):
            mostrar_modal_mapa_calor(datos, "📊 Mapa de Calor - Materias")


def inyectar_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Montserrat', sans-serif;
        }
        
        div.stButton > button {
            background: linear-gradient(135deg, #1a7a3a, #2e9e4e) !important;
            color: white !important;
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
        }
        div.stButton > button:hover {
            transform: scale(1.02) !important;
            box-shadow: 0 4px 12px rgba(26, 122, 58, 0.4) !important;
        }
        h1, h2, h3, h4, h5, h6, .stMarkdown {
            font-family: 'Montserrat', sans-serif !important;
        }
        .stSelectbox label, .stMultiSelect label {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 500 !important;
        }
    </style>
    """, unsafe_allow_html=True)


def mostrar_modelos():
    st.subheader("📊 Análisis de Modelos por Percentiles")
    
    if "df_filtrado" not in st.session_state:
        st.warning("⚠️ No hay datos en session_state")
        return
    
    df = st.session_state["df_filtrado"].copy()
    
    if df.empty:
        st.warning("⚠️ No hay datos")
        return
    
    inyectar_css()
    
    # FILTROS
    st.markdown("### 🔍 Filtros")
    col_f1, col_f2 = st.columns([1, 3])
    
    with col_f1:
        clasificacion = st.selectbox(
            "🎯 Clasificación",
            options=["Todas", "Aburridas", "Entretenidas"],
            index=0,
            key="clasificacion_modelos"
        )
    
    df_modelos = df.copy()
    if clasificacion != "Todas" and "Clase_Predicha" in df_modelos.columns:
        df_modelos["Clase_Predicha"] = df_modelos["Clase_Predicha"].astype(str).str.upper()
        if clasificacion == "Aburridas":
            df_modelos = df_modelos[df_modelos["Clase_Predicha"] == "ABURRIDO"]
        elif clasificacion == "Entretenidas":
            df_modelos = df_modelos[df_modelos["Clase_Predicha"] == "ENTRETENIDO"]
    
    if df_modelos.empty:
        st.warning("⚠️ No hay datos con el filtro seleccionado.")
        return
    
    # OPCIONES
    opciones_docentes = ["Todos"]
    if "nombres_apellidos" in df_modelos.columns:
        opciones_docentes.extend(sorted(df_modelos["nombres_apellidos"].dropna().unique().tolist()))
    
    opciones_programas = ["Todos"]
    if "area" in df_modelos.columns:
        opciones_programas.extend(sorted(df_modelos["area"].dropna().unique().tolist()))
    
    opciones_materias = ["Todos"]
    if "nom_materia" in df_modelos.columns:
        opciones_materias.extend(sorted(df_modelos["nom_materia"].dropna().unique().tolist()))
    
    # ============================================================
    # 3 MAPAS DE CALOR - CADA UNO OCUPA TODO EL ANCHO
    # ============================================================
    st.markdown("---")
    ALTURA_MODELOS = 350
    
    # DOCENTES
    st.markdown("### 👨‍🏫 Docentes")
    docentes_seleccionados = st.multiselect(
        "Seleccionar docentes",
        options=opciones_docentes,
        default=["Todos"],
        key="multiselect_modelos_docentes"
    )
    if not docentes_seleccionados:
        docentes_seleccionados = ["Todos"]
    mostrar_modelos_docentes(df_modelos, docentes_seleccionados, altura=ALTURA_MODELOS, show_modal=True)
    
    st.markdown("---")
    
    # PROGRAMAS
    st.markdown("### 📚 Programas")
    programas_seleccionados = st.multiselect(
        "Seleccionar programas",
        options=opciones_programas,
        default=["Todos"],
        key="multiselect_modelos_programas"
    )
    if not programas_seleccionados:
        programas_seleccionados = ["Todos"]
    mostrar_modelos_programas(df_modelos, programas_seleccionados, altura=ALTURA_MODELOS, show_modal=True)
    
    st.markdown("---")
    
    # MATERIAS
    st.markdown("### 📖 Materias")
    materias_seleccionados = st.multiselect(
        "Seleccionar materias",
        options=opciones_materias,
        default=["Todos"],
        key="multiselect_modelos_materias"
    )
    if not materias_seleccionados:
        materias_seleccionados = ["Todos"]
    mostrar_modelos_materias(df_modelos, materias_seleccionados, altura=ALTURA_MODELOS, show_modal=True)