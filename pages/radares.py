import textwrap
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Dashboard de Cumplimiento Docente",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Configuración global de métricas
METRICAS_CONFIG = {
    "DME_s": {
        "nombre": "Duración del monólogo",
        "limite": 3.5,
        "condicion": "menor",
        "corto": "DME_s",
    },
    "Tone_CoV": {
        "nombre": "Variación de la voz",
        "limite": 0.32,
        "condicion": "mayor",
        "corto": "Tone_CoV",
    },
    "Enthusiasm_Score": {
        "nombre": "Nivel de energía",
        "limite": 0.15,
        "condicion": "mayor",
        "corto": "Enthusiasm",
    },
    "DTE_ratio": {
        "nombre": "Porcentaje de habla",
        "limite": 0.5,
        "condicion": "menor_igual",
        "corto": "DTE_ratio",
    },
    "IMP_promedio": {
        "nombre": "Movimiento promedio",
        "limite": 4.0,
        "condicion": "mayor",
        "corto": "IMP_prom",
    },
    "sigma2_IM": {
        "nombre": "Cambios de movimiento",
        "limite": 8.5,
        "condicion": "mayor",
        "corto": "sigma2_IM",
    },
    "Jitter_Score": {
        "nombre": "Estabilidad técnica",
        "limite": 0.4,
        "condicion": "mayor",
        "corto": "Jitter",
    },
}


# ==========================================
# 2. GENERADOR DE DATOS DE PRUEBA (DEMO)
# ==========================================
def generar_datos_ejemplo():
    """Genera un DataFrame de prueba en caso de que no existan datos cargados."""
    np.random.seed(42)
    docentes = [
        "Carlos Mendoza",
        "Ana María López",
        "Javier Rodríguez",
        "Laura Gómez",
        "Felipe Torres",
        "Beatriz Morales",
        "Diego Hernández",
        "Sofía Castro",
    ]
    programas = [
        "Ingeniería de Sistemas",
        "Administración",
        "Derecho",
        "Diseño Gráfico",
    ]
    materias = [
        "Algoritmos",
        "Gestión Estratégica",
        "Derecho Civil",
        "UX/UI Design",
        "Bases de Datos",
    ]
    clases = ["ENTRETENIDO", "ABURRIDO"]

    data = []
    for _ in range(80):
        data.append(
            {
                "nombres_apellidos": np.random.choice(docentes),
                "area": np.random.choice(programas),
                "nom_materia": np.random.choice(materias),
                "Clase_Predicha": np.random.choice(clases, p=[0.7, 0.3]),
                "DME_s": round(np.random.uniform(1.5, 5.0), 2),
                "Tone_CoV": round(np.random.uniform(0.15, 0.50), 2),
                "Enthusiasm_Score": round(np.random.uniform(0.05, 0.30), 2),
                "DTE_ratio": round(np.random.uniform(0.2, 0.8), 2),
                "IMP_promedio": round(np.random.uniform(2.0, 7.0), 2),
                "sigma2_IM": round(np.random.uniform(4.0, 12.0), 2),
                "Jitter_Score": round(np.random.uniform(0.1, 0.8), 2),
            }
        )
    return pd.DataFrame(data)


# ==========================================
# 3. FUNCIONES CÁLCULOS Y LÓGICA
# ==========================================
def calcular_cumplimiento(valor, limite, condicion):
    """Calcula el porcentaje de cumplimiento (0 a 100%) en base a un límite y condición."""
    if pd.isna(valor):
        return np.nan
    try:
        val = float(str(valor).replace(",", "."))
    except (ValueError, TypeError):
        return np.nan

    if condicion in ["mayor", "mayor_igual"]:
        pct = (val / limite) * 100 if limite != 0 else 100.0
    elif condicion in ["menor", "menor_igual"]:
        pct = (limite / val) * 100 if val != 0 else 100.0
    else:
        return np.nan

    return float(np.clip(pct, 0.0, 100.0))


def calcular_promedio_cumplimiento(
    df, columna_modelo, columna_agrupacion=None, elemento=None
):
    if df is None or df.empty or columna_modelo not in df.columns:
        return np.nan

    if columna_agrupacion and elemento and elemento != "Todos":
        df_filtrado = df[df[columna_agrupacion] == elemento]
    else:
        df_filtrado = df

    if df_filtrado.empty:
        return np.nan

    config = METRICAS_CONFIG.get(columna_modelo)
    if not config:
        return np.nan

    serie_valores = df_filtrado[columna_modelo].dropna()
    if serie_valores.empty:
        return np.nan

    cumplimientos = []
    for valor in serie_valores:
        pct = calcular_cumplimiento(valor, config["limite"], config["condicion"])
        if not pd.isna(pct):
            cumplimientos.append(pct)

    return np.mean(cumplimientos) if cumplimientos else np.nan


def obtener_datos_radar(df, elementos, columna_agrupacion):
    if df is None or df.empty or columna_agrupacion not in df.columns:
        return {}

    resultados = {}
    for elemento in elementos:
        valores = {}
        for modelo in METRICAS_CONFIG.keys():
            if modelo in df.columns:
                valores[modelo] = calcular_promedio_cumplimiento(
                    df, modelo, columna_agrupacion, elemento
                )
            else:
                valores[modelo] = np.nan
        resultados[elemento] = valores
    return resultados


# ==========================================
# 4. COMPONENTES VISUALES, RADARES Y MODALES
# ==========================================
def crear_radar(datos, titulo, colores=None, altura=400):
    categorias_keys = list(METRICAS_CONFIG.keys())
    nombres_ejes = [METRICAS_CONFIG[k]["nombre"] for k in categorias_keys]

    fig = go.Figure()

    if colores is None:
        colores = ["#1f77b4", "#2ca02c", "#f39c12"]

    for idx, (nombre, valores) in enumerate(datos.items()):
        valores_ordenados = [valores.get(cat, np.nan) for cat in categorias_keys]
        color = colores[idx % len(colores)]

        fig.add_trace(
            go.Scatterpolar(
                r=valores_ordenados,
                theta=nombres_ejes,
                fill="toself",
                name=nombre,
                line_color=color,
                fillcolor=color,
                opacity=0.35,
                hovertemplate="<b>%{theta}</b><br>Cumplimiento: %{r:.1f}%<extra></extra>",
            )
        )

    # Línea de meta de referencia (75%)
    fig.add_trace(
        go.Scatterpolar(
            r=[75] * len(nombres_ejes),
            theta=nombres_ejes,
            fill=None,
            mode="lines",
            name="Meta 75%",
            line=dict(color="#dc3545", dash="dash", width=2),
            hovertemplate="Meta: 75%<extra></extra>",
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[0, 20, 40, 60, 75, 80, 100],
                ticktext=["0%", "20%", "40%", "60%", "75%", "80%", "100%"],
                gridcolor="#e0e0e0",
                linecolor="#e0e0e0",
            ),
            angularaxis=dict(
                tickfont=dict(size=10, color="#333", family="Montserrat, sans-serif"),
                gridcolor="#e0e0e0",
                linecolor="#e0e0e0",
            ),
            bgcolor="rgba(255,255,255,0.9)",
        ),
        title=dict(
            text=titulo,
            font=dict(
                size=14,
                color="#1a7a3a",
                family="Montserrat, sans-serif",
                weight="bold",
            ),
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=10, family="Montserrat, sans-serif"),
        ),
        height=altura,
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor="rgba(255,255,255,0.9)",
        plot_bgcolor="rgba(255,255,255,0.9)",
    )
    return fig


def mostrar_interpretacion(valores):
    cumplen = []
    no_cumplen = []
    for modelo, valor in valores.items():
        if pd.isna(valor):
            continue
        if valor >= 75:
            cumplen.append((modelo, valor))
        else:
            no_cumplen.append((modelo, valor))

    st.markdown("---")
    st.markdown("**📌 Interpretación**")
    col1, col2 = st.columns(2)

    with col1:
        if cumplen:
            st.markdown("**✅ Cumple (≥75%):**")
            for modelo, valor in cumplen:
                st.markdown(f"- **{METRICAS_CONFIG[modelo]['nombre']}**: {valor:.1f}%")
        else:
            st.markdown("⚠️ Ningún modelo alcanza la meta del 75%.")

    with col2:
        if no_cumplen:
            st.markdown("**🔴 Oportunidad de Mejora (<75%):**")
            for modelo, valor in no_cumplen:
                st.markdown(f"- **{METRICAS_CONFIG[modelo]['nombre']}**: {valor:.1f}%")
        else:
            st.success("🎉 ¡Todos los indicadores alcanzan o superan el 75%!")


@st.dialog("🔍 Radar - Vista Ampliada", width="large")
def mostrar_modal_radar(datos, titulo):
    fig = crear_radar(datos, titulo, altura=600)
    st.plotly_chart(fig, use_container_width=True)
    if len(datos) == 1:
        mostrar_interpretacion(list(datos.values())[0])
    st.caption("🔄 Cierra esta ventana modal para volver al panel de control")


@st.dialog("📋 Distribución de Docentes por Nivel de Cumplimiento", width="large")
def mostrar_modal_detalle_docentes(df):
    """Muestra la distribución de docentes clasificados en Bajo, Medio y Alto en un modal con expanders."""
    if df is None or df.empty or "nombres_apellidos" not in df.columns:
        st.warning("⚠️ No hay información de docentes disponible para clasificar.")
        return

    docentes_unicos = df["nombres_apellidos"].dropna().unique().tolist()
    resumen = []

    # Se calcula el promedio general de cumplimiento de cada docente a través de todas las métricas
    for docente in docentes_unicos:
        cumplimientos_docente = []
        for metrica_key in METRICAS_CONFIG.keys():
            if metrica_key in df.columns:
                pct = calcular_promedio_cumplimiento(
                    df, metrica_key, "nombres_apellidos", docente
                )
                if not pd.isna(pct):
                    cumplimientos_docente.append(pct)

        promedio_docente = (
            np.mean(cumplimientos_docente) if cumplimientos_docente else np.nan
        )
        if not pd.isna(promedio_docente):
            resumen.append(
                {
                    "nombres_apellidos": docente,
                    "Promedio_General_%": round(promedio_docente, 1),
                    "clases": len(df[df["nombres_apellidos"] == docente]),
                }
            )

    df_resumen = pd.DataFrame(resumen)

    if df_resumen.empty:
        st.info("No hay datos suficientes para calcular los promedios.")
        return

    # Clasificación por rangos
    bajo = df_resumen[df_resumen["Promedio_General_%"] < 40]
    medio = df_resumen[
        (df_resumen["Promedio_General_%"] >= 40)
        & (df_resumen["Promedio_General_%"] <= 60)
    ]
    alto = df_resumen[df_resumen["Promedio_General_%"] > 60]

    total = len(df_resumen)

    st.markdown(
        f"Se han evaluado **{total} docentes únicos** promediando su rendimiento general en todas las métricas."
    )
    st.markdown("Haz clic en cada categoría para ver el listado de docentes:")

    # 1. EXPANDER BAJO (<40%)
    pct_bajo = (len(bajo) / total) * 100
    with st.expander(
        f"🔴 **Rango Bajo (<40%)** — {len(bajo)} docente(s) ({pct_bajo:.1f}% del total)"
    ):
        if not bajo.empty:
            st.dataframe(
                bajo.sort_values(by="Promedio_General_%", ascending=True).rename(
                    columns={
                        "nombres_apellidos": "Docente",
                        "Promedio_General_%": "Cumplimiento Promedio (%)",
                        "clases": "Clases Evaluadas",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No hay docentes en este rango.")

    # 2. EXPANDER MEDIO (40-60%)
    pct_medio = (len(medio) / total) * 100
    with st.expander(
        f"🟡 **Rango Medio (40-60%)** — {len(medio)} docente(s) ({pct_medio:.1f}% del total)"
    ):
        if not medio.empty:
            st.dataframe(
                medio.sort_values(by="Promedio_General_%", ascending=False).rename(
                    columns={
                        "nombres_apellidos": "Docente",
                        "Promedio_General_%": "Cumplimiento Promedio (%)",
                        "clases": "Clases Evaluadas",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No hay docentes en este rango.")

    # 3. EXPANDER ALTO (>60%)
    pct_alto = (len(alto) / total) * 100
    with st.expander(
        f"🟢 **Rango Alto (>60%)** — {len(alto)} docente(s) ({pct_alto:.1f}% del total)"
    ):
        if not alto.empty:
            st.dataframe(
                alto.sort_values(by="Promedio_General_%", ascending=False).rename(
                    columns={
                        "nombres_apellidos": "Docente",
                        "Promedio_General_%": "Cumplimiento Promedio (%)",
                        "clases": "Clases Evaluadas",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No hay docentes en este rango.")

    st.caption("🔄 Cierra esta ventana modal para continuar explorando el panel.")


def mostrar_radar_docentes(df, elementos_seleccionados, altura=350, show_modal=True):
    if df is None or df.empty:
        return
    if not elementos_seleccionados:
        elementos_seleccionados = ["Todos"]

    datos = obtener_datos_radar(df, elementos_seleccionados, "nombres_apellidos")
    if not datos or all(
        all(pd.isna(v) for v in vals.values()) for vals in datos.values()
    ):
        st.info("No hay datos suficientes para generar el radar de docentes.")
        return

    fig = crear_radar(datos, "👨‍🏫 Comparación de Docentes", altura=altura)
    st.plotly_chart(fig, use_container_width=True)
    if show_modal:
        if st.button(
            "🔍 Ver más grande",
            key="modal_radar_docentes",
            use_container_width=True,
        ):
            mostrar_modal_radar(datos, "👨‍🏫 Comparación de Docentes")


def mostrar_radar_programas(df, elementos_seleccionados, altura=350, show_modal=True):
    if df is None or df.empty:
        return
    if not elementos_seleccionados:
        elementos_seleccionados = ["Todos"]

    datos = obtener_datos_radar(df, elementos_seleccionados, "area")
    if not datos or all(
        all(pd.isna(v) for v in vals.values()) for vals in datos.values()
    ):
        st.info("No hay datos suficientes para generar el radar de programas.")
        return

    fig = crear_radar(datos, "📚 Comparación de Programas", altura=altura)
    st.plotly_chart(fig, use_container_width=True)
    if show_modal:
        if st.button(
            "🔍 Ver más grande",
            key="modal_radar_programas",
            use_container_width=True,
        ):
            mostrar_modal_radar(datos, "📚 Comparación de Programas")


def mostrar_radar_materias(df, elementos_seleccionados, altura=350, show_modal=True):
    if df is None or df.empty:
        return
    if not elementos_seleccionados:
        elementos_seleccionados = ["Todos"]

    datos = obtener_datos_radar(df, elementos_seleccionados, "nom_materia")
    if not datos or all(
        all(pd.isna(v) for v in vals.values()) for vals in datos.values()
    ):
        st.info("No hay datos suficientes para generar el radar de materias.")
        return

    fig = crear_radar(datos, "📖 Comparación de Materias", altura=altura)
    st.plotly_chart(fig, use_container_width=True)
    if show_modal:
        if st.button(
            "🔍 Ver más grande",
            key="modal_radar_materias",
            use_container_width=True,
        ):
            mostrar_modal_radar(datos, "📖 Comparación de Materias")


# ==========================================
# 5. ESTILOS CSS Y PODIO
# ==========================================
def inyectar_css():
    css = """
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

        /* Estilos del Podio */
        .podio-container {
            display: flex;
            justify-content: center;
            align-items: flex-end;
            gap: 15px;
            margin-top: 25px;
            margin-bottom: 25px;
        }
        .tarjeta-podio {
            width: 30%;
            text-align: center;
            border-radius: 15px 15px 12px 12px;
            padding: 15px 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            color: #2c3e50;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .primero {
            height: 330px;
            background: linear-gradient(180deg, #ffe066 0%, #ffd700 100%);
            border: 2px solid #e6c200;
        }
        .segundo {
            height: 270px;
            background: linear-gradient(180deg, #f0f0f0 0%, #d6d6d6 100%);
            border: 2px solid #b8b8b8;
        }
        .tercero {
            height: 230px;
            background: linear-gradient(180deg, #f7d3ba 0%, #e09f67 100%);
            border: 2px solid #c77b38;
        }
        .medalla {
            font-size: 42px;
            line-height: 1;
        }
        .nombre-podio {
            font-size: 15px;
            font-weight: 700;
            margin-top: 5px;
            word-break: break-word;
        }
        .info-clases-podio {
            font-size: 11px;
            color: #555;
            margin-top: 2px;
            font-weight: 500;
        }
        .puntaje-podio {
            font-size: 26px;
            font-weight: 800;
            margin: 5px 0;
        }
        .puesto-podio {
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1px;
            opacity: 0.8;
        }
        .badge-cumplimiento {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 10px;
            font-weight: 700;
            margin-top: 4px;
        }
        .badge-cumple {
            background-color: #28a745;
            color: white;
        }
        .badge-nocumple {
            background-color: #dc3545;
            color: white;
        }

        /* Estilos del Footer */
        .footer-container {
            margin-top: 50px;
            padding: 20px 0;
            border-top: 1px solid #e0e0e0;
            text-align: center;
            color: #6c757d;
            font-size: 13px;
        }
        .footer-container a {
            color: #1a7a3a;
            text-decoration: none;
            font-weight: 600;
        }
        .footer-container a:hover {
            text-decoration: underline;
        }
    </style>
    """
    st.markdown(textwrap.dedent(css), unsafe_allow_html=True)


def mostrar_podio(df):
    """Muestra el podio de los 3 docentes mejor calificados en la métrica seleccionada."""
    st.markdown("### 🏆 Podio de Excelencia por Métrica")

    if df is None or df.empty or "nombres_apellidos" not in df.columns:
        st.warning("⚠️ No hay información de docentes disponible para el podio.")
        return

    # Mapeo de nombres entendibles a keys de METRICAS_CONFIG
    opciones_metricas = {
        config["nombre"]: key for key, config in METRICAS_CONFIG.items()
    }

    col_sel, col_info = st.columns([1, 2])

    with col_sel:
        metrica_nombre = st.selectbox(
            "🎯 Selecciona la métrica a evaluar:",
            options=list(opciones_metricas.keys()),
            key="selector_metrica_podio",
        )

    metrica_key = opciones_metricas[metrica_nombre]
    config_actual = METRICAS_CONFIG[metrica_key]
    limite_target = config_actual["limite"]
    condicion_target = config_actual["condicion"]

    es_menor = "menor" in condicion_target
    criterio_texto = "menor o igual" if es_menor else "mayor o igual"

    with col_info:
        st.info(
            f"🎯 **Meta para {metrica_nombre}:** El valor deseado debe ser **{criterio_texto} a {limite_target}**. "
            f"El podio promedia el cumplimiento (%) de **todas las clases de cada docente único**."
        )

    formula_mayor = (
        r"$$\text{Cumplimiento (\%)} = \min\left(100, \frac{\text{Valor Obtenido}}{\text{Meta ("
        + str(limite_target)
        + r")}} \times 100\right)$$"
    )
    formula_menor = (
        r"$$\text{Cumplimiento (\%)} = \min\left(100, \frac{\text{Meta ("
        + str(limite_target)
        + r")}}{\text{Valor Obtenido}} \times 100\right)$$"
    )

    with st.expander(
        "ℹ️ ¿Cómo se calcula este puntaje, las metas y la agrupación de docentes?"
    ):
        st.markdown(f"""
        ### 📐 Guía de Cálculo y Evaluación
        
        **1. Agrupación por Docente Único:**  
        No importa cuántas clases (1, 10 o 1,000) haya impartido un docente en el dataset; cada docente aparece **una sola vez** en la evaluación final con la media de sus resultados.

        **2. Meta Numérica Requerida:**  
        Para la métrica seleccionada ( **{metrica_nombre}** ), la meta técnica de referencia es un valor **{criterio_texto} a {limite_target}**.

        **3. Cálculo del % de Cumplimiento:**
        * **Para métricas donde un valor MAYOR es mejor** *(ej. Variación de voz, Movimiento)*:
        {formula_mayor}
        * **Para métricas donde un valor MENOR es mejor** *(ej. Monólogo, Porcentaje de habla)*:
        {formula_menor}

        ---
        📌 **Reglas del Ranking:**
        * **Estatus de Meta:** Un docente obtiene la medalla con el distintivo **`✅ Cumple`** si su porcentaje promedio general es mayor o igual al 75%. De lo contrario, aparece con **`🔴 No Cumple`**.
        """)

    if metrica_key not in df.columns:
        st.error(f"La columna '{metrica_key}' no se encuentra en el dataset.")
        return

    docentes_unicos = df["nombres_apellidos"].dropna().unique().tolist()

    resultados = []
    for docente in docentes_unicos:
        df_docente = df[df["nombres_apellidos"] == docente]
        n_clases = len(df_docente)

        pct = calcular_promedio_cumplimiento(
            df, metrica_key, "nombres_apellidos", docente
        )
        if not pd.isna(pct):
            resultados.append({"nombre": docente, "puntaje": pct, "clases": n_clases})

    if not resultados:
        st.warning("No hay datos válidos de cumplimiento para la métrica seleccionada.")
        return

    docentes_ordenados = sorted(resultados, key=lambda x: x["puntaje"], reverse=True)
    top_3 = docentes_ordenados[:3]

    medallas = ["🥇", "🥈", "🥉"]
    puestos = ["1ER LUGAR", "2DO LUGAR", "3ER LUGAR"]

    podio_data = []
    for i in range(3):
        if i < len(top_3):
            docente = top_3[i]
            cumple_meta = docente["puntaje"] >= 75.0
            podio_data.append(
                {
                    "puesto": puestos[i],
                    "nombre": docente["nombre"],
                    "puntaje": f"{docente['puntaje']:.1f}%",
                    "clases": f"{docente['clases']} clase(s) evaluada(s)",
                    "medalla": medallas[i],
                    "badge_text": (
                        "✅ Cumple (≥75%)" if cumple_meta else "🔴 No Cumple (<75%)"
                    ),
                    "badge_class": (
                        "badge-cumple" if cumple_meta else "badge-nocumple"
                    ),
                }
            )
        else:
            podio_data.append(
                {
                    "puesto": puestos[i],
                    "nombre": "Sin datos",
                    "puntaje": "N/A",
                    "clases": "0 clases",
                    "medalla": medallas[i],
                    "badge_text": "N/A",
                    "badge_class": "badge-nocumple",
                }
            )

    segundo, primero, tercero = podio_data[1], podio_data[0], podio_data[2]

    html_podio = f"""
    <div class="podio-container">
        <div class="tarjeta-podio segundo">
            <div>
                <div class="medalla">{segundo['medalla']}</div>
                <div class="puesto-podio">{segundo['puesto']}</div>
                <div class="nombre-podio">{segundo['nombre']}</div>
                <div class="info-clases-podio">{segundo['clases']}</div>
            </div>
            <div>
                <div class="puntaje-podio">{segundo['puntaje']}</div>
                <div class="badge-cumplimiento {segundo['badge_class']}">{segundo['badge_text']}</div>
            </div>
        </div>
        <div class="tarjeta-podio primero">
            <div>
                <div class="medalla">{primero['medalla']}</div>
                <div class="puesto-podio">{primero['puesto']}</div>
                <div class="nombre-podio">{primero['nombre']}</div>
                <div class="info-clases-podio">{primero['clases']}</div>
            </div>
            <div>
                <div class="puntaje-podio">{primero['puntaje']}</div>
                <div class="badge-cumplimiento {primero['badge_class']}">{primero['badge_text']}</div>
            </div>
        </div>
        <div class="tarjeta-podio tercero">
            <div>
                <div class="medalla">{tercero['medalla']}</div>
                <div class="puesto-podio">{tercero['puesto']}</div>
                <div class="nombre-podio">{tercero['nombre']}</div>
                <div class="info-clases-podio">{tercero['clases']}</div>
            </div>
            <div>
                <div class="puntaje-podio">{tercero['puntaje']}</div>
                <div class="badge-cumplimiento {tercero['badge_class']}">{tercero['badge_text']}</div>
            </div>
        </div>
    </div>
    """

    st.markdown(textwrap.dedent(html_podio), unsafe_allow_html=True)


# ==========================================
# 6. FUNCIÓN PRINCIPAL DE COMPONENTES
# ==========================================
def mostrar_radares():
    st.subheader("📊 Comparación de Modelos por Radar")
    st.markdown("**Meta:** 75% de cumplimiento en cada métrica.")
    st.caption("Selecciona máximo tres docentes, programas o materias para comparar.")

    if "df_filtrado" not in st.session_state:
        st.session_state["df_filtrado"] = generar_datos_ejemplo()

    df = st.session_state["df_filtrado"].copy()

    if df.empty:
        st.warning("⚠️ El conjunto de datos está vacío.")
        return

    inyectar_css()

    # FILTROS
    st.markdown("### 🔍 Filtros")
    col_f1, _ = st.columns([1, 3])

    with col_f1:
        clasificacion = st.selectbox(
            "🎯 Clasificación",
            options=["Todas", "Aburridas", "Entretenidas"],
            index=0,
            key="clasificacion_radar",
        )

    df_radar = df.copy()
    if clasificacion != "Todas" and "Clase_Predicha" in df_radar.columns:
        df_radar["Clase_Predicha"] = df_radar["Clase_Predicha"].astype(str).str.upper()
        if clasificacion == "Aburridas":
            df_radar = df_radar[df_radar["Clase_Predicha"] == "ABURRIDO"]
        elif clasificacion == "Entretenidas":
            df_radar = df_radar[df_radar["Clase_Predicha"] == "ENTRETENIDO"]

    if df_radar.empty:
        st.warning("⚠️ No se encontraron registros con la clasificación seleccionada.")
        return

    # LISTAS PARA MULTISELECT
    opciones_docentes = ["Todos"]
    if "nombres_apellidos" in df_radar.columns:
        opciones_docentes.extend(
            sorted(df_radar["nombres_apellidos"].dropna().unique().tolist())
        )

    opciones_programas = ["Todos"]
    if "area" in df_radar.columns:
        opciones_programas.extend(sorted(df_radar["area"].dropna().unique().tolist()))

    opciones_materias = ["Todos"]
    if "nom_materia" in df_radar.columns:
        opciones_materias.extend(
            sorted(df_radar["nom_materia"].dropna().unique().tolist())
        )

    # 1. PRIMERO: SECCIÓN DE LOS 3 RADARES
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    ALTURA_RADAR = 350

    with col1:
        with st.container(border=True):
            docentes_seleccionados = st.multiselect(
                "👨‍🏫 Seleccionar docentes",
                options=opciones_docentes,
                default=["Todos"],
                key="multiselect_docentes",
            )
            if not docentes_seleccionados:
                docentes_seleccionados = ["Todos"]
            mostrar_radar_docentes(
                df_radar,
                docentes_seleccionados,
                altura=ALTURA_RADAR,
                show_modal=True,
            )

    with col2:
        with st.container(border=True):
            programas_seleccionados = st.multiselect(
                "📚 Seleccionar programas",
                options=opciones_programas,
                default=["Todos"],
                key="multiselect_programas",
            )
            if not programas_seleccionados:
                programas_seleccionados = ["Todos"]
            mostrar_radar_programas(
                df_radar,
                programas_seleccionados,
                altura=ALTURA_RADAR,
                show_modal=True,
            )

    with col3:
        with st.container(border=True):
            materias_seleccionados = st.multiselect(
                "📖 Seleccionar materias",
                options=opciones_materias,
                default=["Todos"],
                key="multiselect_materias",
            )
            if not materias_seleccionados:
                materias_seleccionados = ["Todos"]
            mostrar_radar_materias(
                df_radar,
                materias_seleccionados,
                altura=ALTURA_RADAR,
                show_modal=True,
            )

    # 2. SECCIÓN DE BOTÓN PARA MODAL DE DETALLE Y RANGOS
    st.markdown("---")
    col_btn_modal, _ = st.columns([1, 1])
    with col_btn_modal:
        if st.button(
            "📋 Ver distribución de docentes por rango de cumplimiento",
            key="btn_modal_rangos",
            use_container_width=True,
        ):
            mostrar_modal_detalle_docentes(df_radar)

    # 3. SECCIÓN DEL PODIO
    st.markdown("---")
    mostrar_podio(df_radar)


# ==========================================
# 7. FOOTER Y EJECUCIÓN
# ==========================================
def mostrar_footer():
    """Renderiza el pie de página institucional del dashboard."""
    html_footer = """
    <div class="footer-container">
        <p><strong>Dashboard de Evaluación y Métrica de Clases</strong> | Desarrollado con Streamlit & Plotly</p>
        <p>© 2026 Todos los derechos reservados</p>
    </div>
    """
    st.markdown(textwrap.dedent(html_footer), unsafe_allow_html=True)


if __name__ == "__main__":
    mostrar_radares()
    mostrar_footer()
