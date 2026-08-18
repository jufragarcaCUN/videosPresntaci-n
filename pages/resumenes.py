import streamlit as st
import pandas as pd


def mostrar_recomendaciones():
    st.subheader("💡 Recomendaciones por Docente")

    if "df_filtrado" not in st.session_state:
        st.warning("⚠️ No hay datos cargados en session_state.")
        return

    df = st.session_state["df_filtrado"]

    if df is None or df.empty:
        st.warning("⚠️ El conjunto de datos está vacío.")
        return

    col_docente = "nombres_apellidos"
    col_recomendacion = "recomen_falencia"

    if col_docente not in df.columns:
        st.error(f"⚠️ No se encontró la columna '{col_docente}' en los datos.")
        return

    # Obtener lista de docentes únicos ordenados
    lista_docentes = sorted([str(d) for d in df[col_docente].dropna().unique()])

    if not lista_docentes:
        st.info("No hay docentes disponibles en los datos.")
        return

    # Único selectbox para filtrar por docente
    docente_sel = st.selectbox(
        "🎯 Selecciona un docente para desplegar sus recomendaciones:",
        options=["-- Selecciona un docente --"] + lista_docentes,
        key="select_docente_recomendaciones",
    )

    if docente_sel and docente_sel != "-- Selecciona un docente --":
        df_docente = df[df[col_docente] == docente_sel]

        st.markdown(f"### 📋 Recomendaciones para: **{docente_sel}**")

        if col_recomendacion in df.columns:
            recomendaciones = df_docente[col_recomendacion].dropna().unique()

            if len(recomendaciones) > 0:
                for idx, rec in enumerate(recomendaciones, 1):
                    st.info(f"**{idx}.** {rec}")
            else:
                st.warning("No hay recomendaciones registradas para este docente.")
        else:
            st.error(
                f"⚠️ No se encontró la columna '{col_recomendacion}' en los datos."
            )
