"""
Portada principal · Modelo Bidireccional de Evaluación (MBE)
Vicerrectoría de Servicios Digitales · COE
"""

import streamlit as st

# ====================================================================
# CONFIGURACIÓN DE PÁGINA
# ====================================================================
st.set_page_config(
    page_title="MBE · Modelo Bidireccional de Evaluación",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ====================================================================
# ESTILOS GLOBALES
# ====================================================================
def inyectar_estilos():
    st.markdown(
        """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@100;200;300;400;500;600;700;800;900&display=swap');

        html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }

        /* SIDEBAR VERDE */
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

        /* ANIMACIONES */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(40px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes float {
            0%   { transform: translateY(0px); }
            50%  { transform: translateY(-20px); }
            100% { transform: translateY(0px); }
        }
        @keyframes pulse {
            0%   { transform: scale(1) rotate(45deg); opacity: 0.2; }
            50%  { transform: scale(1.05) rotate(45deg); opacity: 0.35; }
            100% { transform: scale(1) rotate(45deg); opacity: 0.2; }
        }
        @keyframes gradientMove {
            0%   { background-position: 0% 50%; }
            50%  { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .animate-fadeUp { animation: fadeInUp 1s ease forwards; }
        .animate-float  { animation: float 3s ease-in-out infinite; }
        .animate-pulse  { animation: pulse 2.5s ease-in-out infinite; }
        .delay-1 { animation-delay: 0.2s; opacity: 0; }
        .delay-2 { animation-delay: 0.5s; opacity: 0; }

        /* HERO */
        .hero-text .badge {
            display: inline-block;
            background: rgba(34, 197, 94, 0.12);
            color: #22c55e;
            padding: 0.35rem 1.2rem;
            border-radius: 30px;
            font-size: 0.78rem;
            font-weight: 700;
            border: 1px solid rgba(34, 197, 94, 0.15);
            margin-bottom: 1.3rem;
            letter-spacing: 1.2px;
            text-transform: uppercase;
        }
        .hero-text h1 {
            font-size: 3.6rem;
            font-weight: 900;
            line-height: 1.1;
            margin-bottom: 1.2rem;
            color: #ffffff;
        }
        .hero-text h1 .highlight {
            background: linear-gradient(135deg, #22c55e, #166534);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            background-size: 200% 200%;
            animation: gradientMove 4s ease infinite;
        }
        .hero-text p {
            font-size: 1.1rem;
            color: #94a3b8;
            line-height: 1.75;
            max-width: 580px;
            margin-bottom: 2rem;
        }

        /* FORMAS GEOMÉTRICAS */
        .hero-shapes { position: relative; width: 320px; height: 320px; margin: 0 auto; }
        .hero-shapes .box {
            width: 120px; height: 120px;
            background: linear-gradient(135deg, #22c55e, #166534);
            border-radius: 16px;
            position: absolute; top: 20px; left: 40px;
            transform: rotate(12deg);
            box-shadow: 0 20px 60px rgba(34, 197, 94, 0.25);
            animation: float 4s ease-in-out infinite;
        }
        .hero-shapes .circle {
            width: 100px; height: 100px;
            background: linear-gradient(135deg, #22c55e, #166534);
            border-radius: 50%;
            position: absolute; bottom: 40px; right: 20px;
            box-shadow: 0 20px 60px rgba(34, 197, 94, 0.2);
            animation: float 3.5s ease-in-out infinite reverse;
        }
        .hero-shapes .triangle {
            width: 80px; height: 70px;
            background: linear-gradient(135deg, #22c55e, #166534);
            clip-path: polygon(50% 0, 100% 100%, 0 100%);
            position: absolute; top: 10px; right: 30px;
            opacity: 0.6;
            animation: float 3s ease-in-out infinite 0.5s;
        }
        .hero-shapes .heart {
            width: 40px; height: 40px;
            background: #ef4444;
            transform: rotate(45deg);
            position: absolute; bottom: 0; right: 80px;
            opacity: 0.25;
            animation: pulse 2.5s ease-in-out infinite;
        }
        .hero-shapes .heart::before,
        .hero-shapes .heart::after {
            content: "";
            background: #ef4444;
            display: block;
            width: 40px; height: 40px;
            border-radius: 50%;
            position: absolute;
        }
        .hero-shapes .heart::before { top: -50%; left: 0; }
        .hero-shapes .heart::after  { top: 0; left: -50%; }
        .hero-shapes .moon {
            width: 50px; height: 50px;
            background: #fbbf24;
            border-radius: 50%;
            mask-image: radial-gradient(circle 22px at 70% 50%, transparent 100%, black calc(100% + 1%));
            -webkit-mask-image: radial-gradient(circle 22px at 70% 50%, transparent 100%, black calc(100% + 1%));
            position: absolute; top: 100px; right: 0;
            opacity: 0.35;
            animation: float 4s ease-in-out infinite 1s;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


# ====================================================================
# CONTENIDO DEL INDEX (HERO)
# ====================================================================
def renderizar_portada():
    col_texto, col_visual = st.columns([1.2, 1])

    with col_texto:
        st.markdown(
            """
        <div class="hero-text animate-fadeUp delay-1">
            <span class="badge">🎓 COE · Vicerrectoría de Servicios Digitales</span>
            <h1>
                Modelo<br />
                <span class="highlight">Bidireccional</span><br />
                de Evaluación
            </h1>
            <p>
                Analítica multimodal para evaluar el dinamismo docente a partir 
                de grabaciones de clase, con clasificación automática en 5 niveles 
                y 8 modelos analíticos.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_visual:
        st.markdown(
            """
        <div class="animate-fadeUp delay-2">
            <div class="hero-shapes">
                <div class="box animate-float"></div>
                <div class="circle animate-float"></div>
                <div class="triangle animate-float"></div>
                <div class="heart animate-pulse"></div>
                <div class="moon animate-float"></div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # Botones de acceso rápido
    col1, col2, _ = st.columns([1, 1, 2])
    with col1:
        st.page_link(
            "pages/3_rubrica.py", label="📋 Ver Rúbrica", use_container_width=True
        )
    with col2:
        st.page_link(
            "pages/4_calular_cumplimiento.py",
            label="📈 Ver Cumplimiento",
            use_container_width=True,
        )

    # Footer principal
    st.markdown(
        """
    <div style="text-align:center; color:#6b7280; font-size:0.8rem; padding:40px 0 20px 0; 
                border-top:1px solid #e5e7eb; margin-top:40px;">
        <strong>Modelo Bidireccional de Evaluación (MBE)</strong><br>
        COE · Vicerrectoría de Servicios Digitales<br>
        © CUN - Corporación Unificada Nacional de Educación Superior
    </div>
    """,
        unsafe_allow_html=True,
    )


# ====================================================================
# FUNCIÓN PRINCIPAL
# ====================================================================
def main():
    inyectar_estilos()

    # Página del index (portada)
    p_inicio = st.Page(renderizar_portada, title="Inicio", icon="🏠", default=True)

    # Páginas del menú lateral
    p_presentacion = st.Page(
        "pages/1_presentacion.py",
        title="Presentación",
        icon="🎓",
    )
    p_rubrica_uno = st.Page(
        "pages/3_rubrica.py",
        title="Rúbrica Modelo Uno",
        icon="📋",
    )
    p_rubrica_dos = st.Page(
        "pages/4_rubrica2.py",
        title="Rúbrica Modelo Dos",
        icon="📄",
    )
    p_cumplimiento = st.Page(
        "pages/4_calular_cumplimiento.py",
        title="Cumplimiento por Modelo",
        icon="📈",
    )

    # Menú lateral
    pg = st.navigation(
        {
            "Inicio": [p_inicio],
            "Informes": [p_presentacion],
            "Evaluación": [p_rubrica_uno, p_rubrica_dos],
            "Análisis": [p_cumplimiento],
        }
    )
    pg.run()

    # Footer del sidebar
    with st.sidebar:
        st.markdown(
            """
            <div class="footer-text">
                <p><b>Modelo Bidireccional de Evaluación (MBE)</b></p>
                <p>© CUN - Corporación Unificada Nacional de Educación Superior</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
