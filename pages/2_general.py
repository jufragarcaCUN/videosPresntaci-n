# pages/2_general.py

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

st.set_page_config(
    page_title="Análisis General | CUN",
    page_icon="📊",
    layout="wide",
)

# ============================================================
# IMPORTS
# ============================================================
try:
    from t import mostrar_tarjetas
except ImportError:
    st.error("❌ No se encuentra t.py")
    st.stop()

try:
    from tortas import mostrar_tortas
except ImportError:
    st.error("❌ No se encuentra tortas.py")
    st.stop()

try:
    from calular_cumplimiento import calcular_cumplimiento
except ImportError:
    st.error("❌ No se encuentra calular_cumplimiento.py")
    st.stop()

# ============================================================
# CONTENIDO
# ============================================================
st.header("📊 Análisis General")
st.markdown("---")

if "df_filtrado" not in st.session_state:
    st.error("❌ No hay datos cargados en la sesión.")
    st.stop()

# TARJETAS
mostrar_tarjetas()
st.markdown("---")

# TORTAS
st.subheader("📊 Distribución de Clases por Categoría")
mostrar_tortas()
st.markdown("---")

# ============================================================
# RADARES - LEER Y EJECUTAR EL ARCHIVO
# ============================================================


# Leer el archivo radares.py
ruta_radares = os.path.join(os.path.dirname(__file__), "radares.py")

if os.path.exists(ruta_radares):
    with open(ruta_radares, "r", encoding="utf-8") as f:
        codigo = f.read()

    # Ejecutar el código y capturar la función
    exec_globals = {}
    exec(codigo, exec_globals)

    # Llamar a la función si existe
    if "mostrar_radares" in exec_globals:
        exec_globals["mostrar_radares"]()
    else:
        st.error("❌ La función mostrar_radares() no está definida en radares.py")
else:
    st.error(f"❌ No se encuentra el archivo: {ruta_radares}")
# En la sección de imports de 2_general.py
try:
    from resumenes import mostrar_recomendaciones
except ImportError:
    st.error("❌ No se encuentra recomendaciones.py")
    st.stop()

# Al final de 2_general.py
st.markdown("---")
mostrar_recomendaciones()
