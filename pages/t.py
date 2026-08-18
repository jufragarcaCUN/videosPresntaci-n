# pages/t.py
import streamlit as st


def mostrar_tarjetas():
    """
    Muestra las tarjetas de resumen ejecutivo.
    Toma el dataframe de session_state directamente.
    """

    # Verificar que existan datos en session_state
    if "df_filtrado" not in st.session_state or st.session_state["df_filtrado"] is None:
        st.warning("⚠️ No hay datos cargados.")
        return

    df = st.session_state["df_filtrado"].copy()

    if df.empty:
        st.warning("⚠️ El dataframe está vacío.")
        return

    # ============================================================
    # CÁLCULO DE MÉTRICAS
    # ============================================================
    total_grabaciones = len(df)
    total_docentes = (
        df["nombres_apellidos"].nunique() if "nombres_apellidos" in df.columns else 0
    )
    total_areas = df["area"].nunique() if "area" in df.columns else 0

    aburridos = 0
    entretenidos = 0

    if "Clase_Predicha" in df.columns:
        aburridos = len(df[df["Clase_Predicha"].astype(str).str.upper() == "ABURRIDO"])
        entretenidos = len(
            df[df["Clase_Predicha"].astype(str).str.upper() == "ENTRETENIDO"]
        )

    # ============================================================
    # CSS PARA TARJETAS
    # ============================================================
    st.markdown(
        """
    <style>
        .card-cun-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            padding: 5px;
        }
        .card-cun {
            border-radius: 12px;
            padding: 20px 15px;
            text-align: center;
            color: white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            transition: all 0.3s ease;
            cursor: default;
            min-height: 150px;
            width: 100%;
            max-width: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border: none;
        }
        .card-cun:hover {
            transform: scale(1.08);
            box-shadow: 0 8px 30px rgba(0,0,0,0.35);
            transition: all 0.3s ease;
        }
        .card-cun-green {
            background: linear-gradient(135deg, #1a7a3a, #2e9e4e);
        }
        .card-cun-light-green {
            background: linear-gradient(135deg, #2e9e4e, #4caf7a);
        }
        .card-cun-dark-green {
            background: linear-gradient(135deg, #0d5a2a, #1a7a3a);
        }
        .card-cun-mint {
            background: linear-gradient(135deg, #4caf7a, #81c784);
        }
        .card-cun-icon {
            font-size: 2.5rem;
            margin-bottom: 5px;
        }
        .card-cun-number {
            font-size: 2.8rem;
            font-weight: 700;
            margin: 2px 0;
            line-height: 1.2;
        }
        .card-cun-label {
            font-size: 0.9rem;
            opacity: 0.9;
            font-weight: 500;
        }
        .card-cun:hover .card-cun-label {
            opacity: 1;
            font-weight: 600;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # ============================================================
    # CREAR TARJETAS - 5 COLUMNAS
    # ============================================================
    def crear_tarjeta(icono, numero, label, color_class):
        return f"""
        <div class="card-cun-wrapper">
            <div class="card-cun {color_class}">
                <div class="card-cun-icon">{icono}</div>
                <div class="card-cun-number">{numero}</div>
                <div class="card-cun-label">{label}</div>
            </div>
        </div>
        """

    col1, col2, col3, col4, col5 = st.columns(5, gap="small")

    with col1:
        st.markdown(
            crear_tarjeta(
                "📹", total_grabaciones, "Total Grabaciones", "card-cun-green"
            ),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            crear_tarjeta(
                "👨‍🏫", total_docentes, "Total Docentes", "card-cun-light-green"
            ),
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            crear_tarjeta("📚", total_areas, "Total programas", "card-cun-mint"),
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            crear_tarjeta("😴", aburridos, "Clases Aburridas", "card-cun-dark-green"),
            unsafe_allow_html=True,
        )

    with col5:
        st.markdown(
            crear_tarjeta("🎉", entretenidos, "Clases Entretenidas", "card-cun-green"),
            unsafe_allow_html=True,
        )
