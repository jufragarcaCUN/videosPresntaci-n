from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st

# 1. Configuración de la ventana
st.set_page_config(
    page_title="Dashboard Académico | CUN",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Estilos personalizados (CSS)
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0d5a2a, #1a7a3a, #2e9e4e) !important;
        }
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        .footer-text {
            text-align: center;
            color: #e0e0e0 !important;
            font-size: 0.85rem;
            margin-top: 20px;
            padding-top: 10px;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
        }
    </style>
""",
    unsafe_allow_html=True,
)


def diagnosticar_carpeta_actual():
    """Imprime en la pantalla principal todos los archivos que detecta Python en la ruta de index.py"""
    base_dir = Path(__file__).resolve().parent

    st.subheader("🔍 Diagnóstico de Archivos en la Ruta de `index.py`", divider="green")
    st.info(f"**Ruta detectada por Python:** `{base_dir}`")

    if base_dir.exists():
        elementos = sorted(list(base_dir.iterdir()))
        if elementos:
            st.write("**Lista de archivos y carpetas encontrados:**")
            col1, col2 = st.columns(2)
            for i, item in enumerate(elementos):
                icon = "📁 [CARPETA]" if item.is_dir() else "📄 [ARCHIVO]"
                if "excel" in item.name.lower() or "exel" in item.name.lower():
                    texto = f"**{icon} {item.name} 👈 (EXCEL DETECTADO)**"
                else:
                    texto = f"{icon} {item.name}"

                if i % 2 == 0:
                    col1.markdown(texto)
                else:
                    col2.markdown(texto)
        else:
            st.warning("⚠️ La carpeta donde está index.py está completamente vacía.")
    else:
        st.error(f"❌ La ruta base no existe: {base_dir}")


@st.cache_data
def load_data():
    base_dir = Path(__file__).resolve().parent

    excel_path = base_dir / "exel_entrada.xlsx"
    if not excel_path.exists():
        excel_path = base_dir / "excel_entrada.xlsx"

    if not excel_path.exists():
        return (
            None,
            f"No se encontró 'exel_entrada.xlsx' ni 'excel_entrada.xlsx' en: {base_dir}",
        )

    try:
        df = pd.read_excel(excel_path)

        multi_value_cols = [
            "grupo",
            "nom_materia",
            "creditos",
            "capacidad",
            "num_inscritos",
            "porcentaje_ocupacion_aula",
            "cod_periodo_grupo",
        ]
        for col in multi_value_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.split("|").str[0]
                if col in [
                    "creditos",
                    "capacidad",
                    "num_inscritos",
                    "porcentaje_ocupacion_aula",
                ]:
                    df[col] = pd.to_numeric(df[col], errors="coerce")

        date_columns = ["fecha", "fec_contrato", "fec_fin"]
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        numeric_columns = [
            "pro_evaluacion_autoevaluacion_docente",
            "pro_evaluacion_evaluacion_por_estudiantes",
            "num_encuestas_evaluacion_por_estudiantes",
            "sigma2_IM",
            "Porcentaje_Certeza",
            "Jitter_Score",
            "IMP_promedio",
            "CPM",
            "DME_s",
            "DTE_ratio",
            "Enthusiasm_Score",
            "Tone_CoV",
            "capacidad",
            "num_inscritos",
            "creditos",
        ]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.replace(["NULL", "null", "NaN", "", " "], np.nan)
        if "CPM" in df.columns:
            df["CPM"] = df["CPM"] / 1000

        return df, None

    except Exception as e:
        return None, f"Error al leer el archivo Excel: {str(e)}"


def main():
    # 1. Carga de datos
    df, error_msg = load_data()

    # 2. Si falla la carga, muestra el error Y ejecuta la función de diagnóstico
    if df is None:
        st.error(f"❌ {error_msg}")
        diagnosticar_carpeta_actual()
        st.stop()

    # 3. Guardar en Session State
    st.session_state["df_filtrado"] = df

    # 4. Configurar navegación (Solo Hoja de Presentación)
    p_presentacion = st.Page("pages/1_presentacion.py", title="Presentación", icon="🎓")

    pg = st.navigation({"Informes": [p_presentacion]})
    pg.run()

    # Footer
    with st.sidebar:
        st.markdown(
            """
            <div class="footer-text">
                <p><b>Dashboard Académico CUN</b></p>
                <p>© CUN - Corporación Unificada Nacional de Educación Superior</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
