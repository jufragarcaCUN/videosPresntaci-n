# pages/tabla_comparativa.py

import streamlit as st


def bondades_modelo():
    with st.expander(
        "📊 Comparativa: Modelo CUN vs Plataformas Competidoras", expanded=False
    ):

        # CSS
        st.markdown(
            """
        <style>
            .comparativa-container {
                font-family: 'Montserrat', sans-serif;
                overflow-x: auto;
                margin: 10px 0;
            }
            .comparativa-container table {
                width: 100%;
                border-collapse: collapse;
                font-size: 11px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }
            .comparativa-container th {
                background: linear-gradient(135deg, #0d5a2a, #1a7a3a);
                color: white;
                padding: 10px 8px;
                text-align: center;
                font-weight: 700;
                font-size: 10px;
                border: 1px solid #1a7a3a;
                position: sticky;
                top: 0;
            }
            .comparativa-container td {
                padding: 8px 6px;
                border: 1px solid #e0e0e0;
                vertical-align: middle;
                text-align: center;
                font-size: 10px;
            }
            .comparativa-container tr:nth-child(even) {
                background-color: #f8f9fa;
            }
            .comparativa-container tr:hover {
                background-color: #e8f5e9;
            }
            .comparativa-container .columna-cun {
                background-color: #e8f5e9 !important;
                font-weight: 600;
            }
            .comparativa-container .badge-verde {
                background-color: #10B981;
                color: white;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 9px;
                font-weight: 700;
                display: inline-block;
            }
            .comparativa-container .badge-rojo {
                background-color: #EF4444;
                color: white;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 9px;
                font-weight: 700;
                display: inline-block;
            }
            .comparativa-container .badge-amarillo {
                background-color: #F59E0B;
                color: white;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 9px;
                font-weight: 700;
                display: inline-block;
            }
            .comparativa-container .texto-verde {
                color: #10B981;
                font-weight: 700;
            }
            .comparativa-container .texto-rojo {
                color: #EF4444;
                font-weight: 700;
            }
            @media (max-width: 768px) {
                .comparativa-container table {
                    font-size: 9px;
                }
                .comparativa-container th, 
                .comparativa-container td {
                    padding: 4px;
                }
            }
        </style>
        """,
            unsafe_allow_html=True,
        )

        # TABLA - EL HTML DEBE ESTAR EN UNA SOLA CADENA SIN INTERRUPCIONES
        tabla_html = """
        <div class="comparativa-container">
        <table>
            <thead>
                <tr>
                    <th style="min-width: 160px;">Característica</th>
                    <th class="columna-cun" style="min-width: 150px;">✅ Modelo CUN</th>
                    <th style="min-width: 100px;">TeachFX</th>
                    <th style="min-width: 100px;">Edthena</th>
                    <th style="min-width: 100px;">Sibme</th>
                    <th style="min-width: 100px;">HiTeach</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="text-align: left; font-weight: 600;">Enfoque Principal</td>
                    <td class="columna-cun" style="text-align: left;">Análisis completo video/audio con base neuropedagógica (4 Pilares + CUN Experience)</td>
                    <td style="text-align: left;">Análisis de discurso en el aula</td>
                    <td style="text-align: left;">Coaching virtual con IA</td>
                    <td style="text-align: left;">IA, coaching y colaboración</td>
                    <td style="text-align: left;">Enseñanza digital con gamificación</td>
                </tr>
                <tr>
                    <td style="text-align: left; font-weight: 600;">Fundamento Pedagógico</td>
                    <td class="columna-cun"><span class="badge-verde">SÍ</span> (4 Pilares)</td>
                    <td><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                </tr>
                <tr>
                    <td style="text-align: left; font-weight: 600;">Vinculación con Encuesta</td>
                    <td class="columna-cun"><span class="badge-verde">SÍ</span> (CUN Experience)</td>
                    <td><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                </tr>
                <tr>
                    <td style="text-align: left; font-weight: 600;">Análisis de Audio</td>
                    <td class="columna-cun" style="text-align: left;"><span class="badge-verde">4 métricas</span></td>
                    <td style="text-align: left;"><span class="badge-verde">SÍ</span></td>
                    <td style="text-align: left;"><span class="badge-verde">SÍ</span></td>
                    <td style="text-align: left;"><span class="badge-verde">SÍ</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                </tr>
                <tr>
                    <td style="text-align: left; font-weight: 600;">Análisis de Video</td>
                    <td class="columna-cun" style="text-align: left;"><span class="badge-verde">3 métricas</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-verde">SÍ</span></td>
                    <td><span class="badge-verde">SÍ</span></td>
                    <td><span class="badge-verde">SÍ</span></td>
                </tr>
                <tr>
                    <td style="text-align: left; font-weight: 600;">Métrica Técnica</td>
                    <td class="columna-cun"><span class="badge-verde">SÍ</span> (Jitter_Score)</td>
                    <td><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                </tr>
                <tr>
                    <td style="text-align: left; font-weight: 600;">Clasificación de Clases</td>
                    <td class="columna-cun"><span class="badge-verde">SÍ</span> (Aburrido / Entretenido)</td>
                    <td><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                </tr>
                <tr>
                    <td style="text-align: left; font-weight: 600;">Transcripción Automática</td>
                    <td class="columna-cun"><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-verde">SÍ</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                </tr>
                <tr>
                    <td style="text-align: left; font-weight: 600;">IA Generativa / Copilot</td>
                    <td class="columna-cun"><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                    <td><span class="badge-verde">SÍ</span> (AI Coach)</td>
                    <td><span class="badge-verde">SÍ</span> (Copilot)</td>
                    <td><span class="badge-verde">SÍ</span> (AI GPT)</td>
                </tr>
                <tr>
                    <td style="text-align: left; font-weight: 600;">Coaching / Feedback</td>
                    <td class="columna-cun">❌ No aplica</td>
                    <td><span class="badge-verde">SÍ</span></td>
                    <td><span class="badge-verde">SÍ</span></td>
                    <td><span class="badge-verde">SÍ</span></td>
                    <td>❌ No</td>
                </tr>
                <tr>
                    <td style="text-align: left; font-weight: 600;">Automación</td>
                    <td class="columna-cun"><span class="badge-verde">100% Automatizado</span></td>
                    <td><span class="badge-verde">100%</span></td>
                    <td><span class="badge-verde">100%</span></td>
                    <td><span class="badge-amarillo">Híbrido</span></td>
                    <td><span class="badge-verde">Automatizado</span></td>
                </tr>
                <tr>
                    <td style="text-align: left; font-weight: 600;">Modelo de Precios</td>
                    <td class="columna-cun" style="font-weight: 700; color: #1a7a3a;">💰 Sin costo</td>
                    <td>💰 $10k-$30k</td>
                    <td>💰 ~$3,450/año</td>
                    <td>💰 Por usuario</td>
                    <td>💰 ~$30 USD/año</td>
                </tr>
                <tr>
                    <td style="text-align: left; font-weight: 600;">Sustento Científico</td>
                    <td class="columna-cun"><span class="badge-verde">SÍ</span> (APA, DOI)</td>
                    <td><span class="badge-verde">SÍ</span></td>
                    <td><span class="badge-verde">SÍ</span></td>
                    <td><span class="badge-verde">SÍ</span></td>
                    <td><span class="badge-rojo">NO</span></td>
                </tr>
            </tbody>
        </table>
        </div>
        """

        st.markdown(tabla_html, unsafe_allow_html=True)

        # Ventajas y Brechas
        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
            <div style="background: #d4edda; border-radius: 8px; padding: 12px 16px; border-left: 4px solid #1a7a3a;">
                <h4 style="color: #0d5a2a; margin: 0 0 6px 0;">✅ Ventajas del Modelo CUN</h4>
                <ul style="margin: 0; padding-left: 18px; font-size: 12px; color: #155724;">
                    <li><strong>Sin costo de licencias</strong> — Ahorro de $10k-$30k anuales</li>
                    <li><strong>Fundamento Pedagógico</strong> — 4 Pilares + Preguntas CUN</li>
                    <li><strong>Visión 360°</strong> — Audio + Video + Técnica + Entorno</li>
                    <li><strong>Clasificación Automática</strong> — Aburrido vs Entretenido</li>
                    <li><strong>100% Automatizado</strong> — Sin revisión humana</li>
                </ul>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
            <div style="background: #f8d7da; border-radius: 8px; padding: 12px 16px; border-left: 4px solid #dc3545;">
                <h4 style="color: #721c24; margin: 0 0 6px 0;">⚠️ Brechas del Modelo CUN</h4>
                <ul style="margin: 0; padding-left: 18px; font-size: 12px; color: #721c24;">
                    <li><strong>Transcripción automática</strong> — Lo tiene Sibme</li>
                    <li><strong>IA Generativa / Copilot</strong> — Lo tienen Edthena, Sibme, HiTeach</li>
                    <li><strong>Coaching/Feedback con IA</strong> — Lo tienen Edthena y Sibme</li>
                </ul>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.caption(
            "📌 Tabla comparativa basada en información de la presentación y referencias públicas de cada plataforma."
        )
