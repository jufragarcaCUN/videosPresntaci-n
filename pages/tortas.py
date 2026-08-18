# pages/tortas.py
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ==============================================================================
# 1. CONFIGURACIÓN Y LÓGICA DE CÁLCULO DE CUMPLIMIENTO
# ==============================================================================

# Diccionario con los límites técnicos y reglas para cada métrica evaluada
METRICAS_CONFIG = {
    "DME_s": {"limite": 3.5, "condicion": "menor"},
    "Tone_CoV": {"limite": 0.32, "condicion": "mayor"},
    "Enthusiasm_Score": {"limite": 0.15, "condicion": "mayor"},
    "DTE_ratio": {"limite": 0.5, "condicion": "menor_igual"},
    "IMP_promedio": {"limite": 4.0, "condicion": "mayor"},
    "sigma2_IM": {"limite": 8.5, "condicion": "mayor"},
    "Jitter_Score": {"limite": 0.4, "condicion": "mayor"},
}


def calcular_cumplimiento_global_dataframe(df, config=METRICAS_CONFIG):
    """
    Calcula el porcentaje de cumplimiento (0% a 100%) para cada métrica individual
    y luego calcula el promedio general en la columna 'cumplimiento_global'.
    """
    df_calc = df.copy()
    cols_calculadas = []

    for metrica, cfg in config.items():
        if metrica in df_calc.columns:
            limite = cfg["limite"]
            condicion = cfg["condicion"]

            # 1. Convierte la columna a numérico reemplazando comas por puntos en caso de strings
            s = pd.to_numeric(
                df_calc[metrica].astype(str).str.replace(",", "."), errors="coerce"
            )

            # 2. Los valores 0 se reemplazan por NaN para no distorsionar las mediciones
            s = s.replace(0, np.nan)

            # 3. Cálculo matemático según el tipo de regla (mayor que o menor que)
            if condicion in ["mayor", "mayor_igual"]:
                pct = (s / limite) * 100.0
            elif condicion in ["menor", "menor_igual"]:
                pct = (1.0 - (s / limite)) * 100.0
            else:
                pct = np.nan

            # 4. Asegura que el porcentaje esté acotado entre 0% y 100% usando np.clip
            col_name = f"{metrica}_cumplimiento"
            df_calc[col_name] = np.clip(pct, 0.0, 100.0)
            cols_calculadas.append(col_name)

    # Si se calcularon métricas, saca el promedio por fila (omitiendo valores vacíos/NaN)
    if cols_calculadas:
        df_calc["cumplimiento_global"] = df_calc[cols_calculadas].mean(
            axis=1, skipna=True
        )
    else:
        df_calc["cumplimiento_global"] = 0.0

    return df_calc


# ==============================================================================
# 2. RENDERIZADO DE LA INTERFAZ Y GRÁFICOS (TORTAS)
# ==============================================================================


def mostrar_tortas(prefix="tortas"):
    """
    Función principal que renderiza las 3 columnas de indicadores: Docentes, Programas y Materias.
    """
    # Verificación de datos cargados en la sesión de Streamlit
    if "df_filtrado" not in st.session_state or st.session_state["df_filtrado"] is None:
        st.warning("⚠️ No hay datos cargados.")
        return

    df = st.session_state["df_filtrado"].copy()

    if df.empty:
        st.warning("⚠️ El dataframe está vacío.")
        return

    # Procesa las métricas de cumplimiento antes de graficar
    df = calcular_cumplimiento_global_dataframe(df)

    # Inyección de estilos CSS para las tarjetas y badges de la interfaz
    st.markdown(
        """
    <style>
        .card-torta-title { font-size: 1.1rem; font-weight: 700; color: #1a7a3a; text-align: center; margin-bottom: 8px; }
        .metric-box { background: #f8f9fa; border-radius: 8px; padding: 12px 10px; text-align: center; border-left: 3px solid #1a7a3a; }
        .metric-box .label { font-size: 0.7rem; color: #6c757d; text-transform: uppercase; letter-spacing: 0.5px; }
        .metric-box .value { font-size: 1.4rem; font-weight: 600; color: #1a1a1a; }
        .metric-box .sub { font-size: 0.7rem; color: #6c757d; }
        .divider { border-top: 1px solid #e9ecef; margin: 12px 0; }
        .badge-green { background: #d4edda; color: #155724; padding: 2px 10px; border-radius: 12px; font-size: 0.7rem; font-weight: 600; }
        .badge-yellow { background: #fff3cd; color: #856404; padding: 2px 10px; border-radius: 12px; font-size: 0.7rem; font-weight: 600; }
        .badge-red { background: #f8d7da; color: #721c24; padding: 2px 10px; border-radius: 12px; font-size: 0.7rem; font-weight: 600; }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Crea las 3 columnas principales
    col1, col2, col3 = st.columns(3)

    # --- 1. DOCENTES ---
    with col1:
        st.markdown(
            '<div class="card-torta-title">👨‍🏫 Cumplimiento por Docente</div>',
            unsafe_allow_html=True,
        )
        if "nombres_apellidos" in df.columns:
            df_doc = df[
                df["nombres_apellidos"].notna() & (df["nombres_apellidos"] != "")
            ]
            if not df_doc.empty:
                render_tarjeta_cumplimiento(
                    df_doc, "nombres_apellidos", "Docente", prefix, "doc"
                )
            else:
                st.info("No hay datos")

    # --- 2. PROGRAMAS ---
    with col2:
        st.markdown(
            '<div class="card-torta-title">📚 Cumplimiento por Programa</div>',
            unsafe_allow_html=True,
        )
        if "area" in df.columns:
            df_area = df[df["area"].notna() & (df["area"] != "")]
            if not df_area.empty:
                render_tarjeta_cumplimiento(df_area, "area", "Programa", prefix, "prog")
            else:
                st.info("No hay datos")

    # --- 3. MATERIAS ---
    with col3:
        st.markdown(
            '<div class="card-torta-title">📖 Cumplimiento por Materia</div>',
            unsafe_allow_html=True,
        )
        if "nom_materia" in df.columns:
            df_mat = df[df["nom_materia"].notna() & (df["nom_materia"] != "")]
            if not df_mat.empty:
                render_tarjeta_cumplimiento(
                    df_mat, "nom_materia", "Materia", prefix, "mat"
                )
            else:
                st.info("No hay datos")


def render_tarjeta_cumplimiento(df_sub, columna_agrupacion, etiqueta, prefix, tag):
    """
    Calcula la distribución por niveles (Alto, Medio, Bajo), renderiza el gráfico Plotly (torta)
    y dibuja el botón para abrir la ventana modal.
    """
    # Agrupa por la columna solicitada y saca el promedio de cumplimiento global
    promedios = df_sub.groupby(columna_agrupacion)["cumplimiento_global"].mean()

    # Conteo según rangos de clasificación
    altos = (promedios >= 60).sum()
    medios = ((promedios >= 40) & (promedios < 60)).sum()
    bajos = (promedios < 40).sum()
    total_entidades = len(promedios)

    # Creación del gráfico de dona con Plotly
    fig = px.pie(
        names=["Alto (>60%)", "Medio (40-60%)", "Bajo (<40%)"],
        values=[altos, medios, bajos],
        title=f"Total: {total_entidades} {etiqueta.lower()}s",
        color_discrete_map={
            "Alto (>60%)": "#2e9e4e",
            "Medio (40-60%)": "#ffc107",
            "Bajo (<40%)": "#dc3545",
        },
        hole=0.3,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(showlegend=True, height=280, margin=dict(l=10, r=10, t=30, b=10))

    # Muestra el gráfico en la interfaz con su clave única de Streamlit
    st.plotly_chart(fig, use_container_width=True, key=f"{prefix}_torta_{tag}_v4")

    # Botón que abre el modal decorado con @st.dialog
    if st.button(
        "📊 Ver análisis",
        key=f"{prefix}_btn_{tag}_v4",
        use_container_width=True,
    ):
        mostrar_modal_estadistico(df_sub, etiqueta, columna_agrupacion)


# ==============================================================================
# 3. MODAL ESTADÍSTICO CON EXPANDER DESPLEGABLE
# ==============================================================================


@st.dialog("📊 ANÁLISIS ESTADÍSTICO DE CUMPLIMIENTO", width="large")
def mostrar_modal_estadistico(df, titulo, columna_agrupacion):
    """
    Ventana modal interactiva que presenta las estadísticas descriptivas
    e incluye un contenedor desplegable (st.expander) con la tabla detallada.
    """
    # Cálculo del promedio de cumplimiento individual
    cumplimiento_por_elemento = df.groupby(columna_agrupacion)[
        "cumplimiento_global"
    ].mean()

    total_elementos = len(cumplimiento_por_elemento)
    total_registros = len(df)

    # Métricas estadísticas básicas
    media = cumplimiento_por_elemento.mean()
    mediana = cumplimiento_por_elemento.median()

    modas = cumplimiento_por_elemento.round(1).mode()
    moda = modas.values[0] if not modas.empty else None

    desviacion = cumplimiento_por_elemento.std()

    # Encabezado del modal
    st.markdown(f"### 📊 Cumplimiento Promedio de {titulo}s")
    st.caption(
        f"{total_elementos} {titulo.lower()}s evaluados · {total_registros} clases/registros analizados"
    )

    st.markdown("---")

    # Bloques métricos de Media, Mediana y Moda
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="metric-box"><div class="label">📊 Media Cumplimiento</div><div class="value">{media:.1f}%</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="metric-box"><div class="label">📊 Mediana</div><div class="value">{mediana:.1f}%</div></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f'<div class="metric-box"><div class="label">📊 Moda</div><div class="value">{f"{moda:.1f}%" if moda is not None else "N/A"}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Distribución en categorías (Bajo, Medio, Alto)
    st.markdown(f"**📊 Distribución de {titulo}s por Nivel de Cumplimiento**")

    bins = [-1, 40, 60, 100.1]
    labels = ["🔴 Bajo (<40%)", "🟡 Medio (40-60%)", "🟢 Alto (>60%)"]
    rangos_cut = pd.cut(
        cumplimiento_por_elemento, bins=bins, labels=labels, right=False
    )
    distribucion = rangos_cut.value_counts().sort_index()

    col1, col2, col3 = st.columns(3)
    rangos_config = {
        "🔴 Bajo (<40%)": ("#f8d7da", "#721c24"),
        "🟡 Medio (40-60%)": ("#fff3cd", "#856404"),
        "🟢 Alto (>60%)": ("#d4edda", "#155724"),
    }

    for idx, (rango_nombre, (bg, color)) in enumerate(rangos_config.items()):
        with [col1, col2, col3][idx]:
            cantidad = distribucion.get(rango_nombre, 0)
            pct = (cantidad / total_elementos) * 100 if total_elementos > 0 else 0
            st.markdown(
                f"""
            <div style="background:{bg}; border-radius:8px; padding:10px; text-align:center;">
                <div style="font-size:0.75rem; color:{color}; font-weight:600;">{rango_nombre}</div>
                <div style="font-size:1.4rem; font-weight:700; color:{color};">{cantidad} {titulo.lower()}s</div>
                <div style="font-size:0.75rem; color:{color};">{pct:.1f}% del total</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Evaluación del badge de estado general
    if media >= 70:
        badge, msg = "badge-green", "✅ Cumplimiento ALTO"
    elif media >= 50:
        badge, msg = "badge-yellow", "⚠️ Cumplimiento MEDIO"
    else:
        badge, msg = "badge-red", "🔴 Cumplimiento BAJO"

    desviacion_val = desviacion if pd.notna(desviacion) else 0.0

    st.markdown(
        f"""
    <div style="display:flex; justify-content:space-between; align-items:center; background:#f8f9fa; border-radius:8px; padding:10px 16px;">
        <span style="font-weight:500;">Resumen General</span>
        <span>Cumplimiento Promedio: <strong>{media:.1f}%</strong></span>
        <span>Desviación Estándar: <strong>{desviacion_val:.1f}%</strong></span>
        <span class="{badge}">{msg}</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ==========================================================================
    # EXPANDER DESPLEGABLE CON TABLA DE DETALLE INDIVIDUAL Y NIVEL DE CUMPLIMIENTO
    # ==========================================================================
    with st.expander(f"📋 Ver desglose detallado por cada {titulo.lower()}"):
        # 1. Creamos la base de la tabla ordenada por cumplimiento
        df_detalle = (
            cumplimiento_por_elemento.reset_index()
            .rename(
                columns={
                    columna_agrupacion: titulo,
                    "cumplimiento_global": "Cumplimiento (%)",
                }
            )
            .sort_values(by="Cumplimiento (%)", ascending=False)
        )

        # 2. Definimos las reglas para categorizar el nivel
        condiciones = [
            df_detalle["Cumplimiento (%)"] >= 60,
            (df_detalle["Cumplimiento (%)"] >= 40)
            & (df_detalle["Cumplimiento (%)"] < 60),
            df_detalle["Cumplimiento (%)"] < 40,
        ]
        etiquetas_nivel = ["🟢 Alto (>60%)", "🟡 Medio (40-60%)", "🔴 Bajo (<40%)"]

        # 3. Asignamos la nueva columna con el nivel correspondiente
        df_detalle["Nivel de Cumplimiento"] = np.select(
            condiciones, etiquetas_nivel, default="Sin Datos"
        )

        # 4. Renderizamos la tabla final
        st.dataframe(
            df_detalle.style.format({"Cumplimiento (%)": "{:.1f}%"}),
            use_container_width=True,
            hide_index=True,
        )
