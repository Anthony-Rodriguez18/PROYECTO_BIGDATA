import streamlit as st
import plotly.graph_objects as go


def _gauge(value, max_val, color, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"size": 12, "color": "#9AA5C0", "family": "Inter"}},
        number={"font": {"size": 22, "color": "#E8ECF4", "family": "Inter"}},
        gauge={
            "axis": {"range": [0, max_val], "tickcolor": "#5C6B8A", "tickfont": {"size": 9}},
            "bar": {"color": color},
            "bgcolor": "#1E2235",
            "bordercolor": "#2A304A",
            "steps": [{"range": [0, max_val], "color": "#232840"}],
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        height=160,
        margin=dict(l=20, r=20, t=30, b=10),
        font=dict(family="Inter"),
    )
    return fig


def render(data: dict):
    st.markdown(
        """
        <div class="page-header">
          <div>
            <div class="page-title">Métricas técnicas</div>
            <div class="page-subtitle">Throughput, latencia y volumen del pipeline</div>
          </div>
          <div class="page-badge">📈 PIPELINE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    m = data["metricas"]

    # ── Gauges ────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Rendimiento del pipeline</div>', unsafe_allow_html=True)

    g1, g2, g3 = st.columns(3)
    with g1:
        fig = _gauge(m["throughput_productor_msg_min"], 200, "#4F6AF5", "Throughput Productor (msg/min)")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with g2:
        fig = _gauge(m["throughput_flink_msg_min"], 200, "#4ECBA4", "Throughput Flink (msg/min)")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with g3:
        fig = _gauge(m["latencia_promedio_s"], 10, "#F0A84A", "Latencia promedio (s)")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Full metrics table ────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Tabla de métricas completa</div>', unsafe_allow_html=True)

    rows = [
        ("Total comentarios enviados",      f"{m['total_comentarios_enviados']:,}",   "Kafka Producer",  "Cantidad total simulada"),
        ("Throughput del productor",         f"{m['throughput_productor_msg_min']} msg/min", "Kafka Producer", "Velocidad de envío"),
        ("Throughput de Flink",              f"{m['throughput_flink_msg_min']} msg/min",     "Flink",          "Velocidad clasificación streaming"),
        ("Latencia promedio",                f"{m['latencia_promedio_s']} s",          "Flink",           "Tiempo ingreso → procesamiento"),
        ("Total ODIO_POLITICO",              f"{m['total_odio_politico']:,}",          "Spark / Flink",   "Comentarios odio político"),
        ("Total ODIO_DEMOGRAFICO",           f"{m['total_odio_demografico']:,}",       "Spark / Flink",   "Comentarios discriminatorios"),
        ("Total ODIO_GENERAL",               f"{m['total_odio_general']:,}",           "Spark / Flink",   "Odio sin jerga específica"),
        ("Total NEUTRAL",                    f"{m['total_neutral']:,}",                "Spark / Flink",   "Comentarios no ofensivos"),
    ]

    header_cols = st.columns([2.5, 1.5, 1.2, 2.5])
    for col, h in zip(header_cols, ["MÉTRICA", "VALOR", "HERRAMIENTA", "INTERPRETACIÓN"]):
        with col:
            st.markdown(
                f'<div style="font-size:0.65rem;font-weight:600;letter-spacing:0.1em;color:#5C6B8A;'
                f'text-transform:uppercase;padding-bottom:8px;border-bottom:1px solid #2A304A">{h}</div>',
                unsafe_allow_html=True,
            )

    for metric, value, tool, desc in rows:
        c1, c2, c3, c4 = st.columns([2.5, 1.5, 1.2, 2.5])
        with c1:
            st.markdown(f'<div style="font-size:0.8rem;color:#E8ECF4;padding:10px 0;border-bottom:1px solid #1E2235">{metric}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div style="font-size:0.8rem;font-weight:600;color:#4F6AF5;font-family:JetBrains Mono,monospace;padding:10px 0;border-bottom:1px solid #1E2235">{value}</div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div style="font-size:0.72rem;color:#9AA5C0;padding:10px 0;border-bottom:1px solid #1E2235">{tool}</div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div style="font-size:0.75rem;color:#5C6B8A;padding:10px 0;border-bottom:1px solid #1E2235">{desc}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Formulas ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Fórmulas aplicadas</div>', unsafe_allow_html=True)

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown(
            """
            <div style="background:#0F1117;border-radius:8px;padding:16px;border:1px solid #2A304A">
              <div style="font-size:0.7rem;color:#4F6AF5;font-weight:600;margin-bottom:8px;letter-spacing:0.08em">THROUGHPUT</div>
              <div style="font-family:JetBrains Mono,monospace;font-size:0.85rem;color:#E8ECF4">
                T = mensajes / tiempo_total_seg
              </div>
              <div style="font-size:0.72rem;color:#5C6B8A;margin-top:8px">
                Ejemplo: 600 msgs / 600s = 1 msg/s = 60 msg/min
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_f2:
        st.markdown(
            """
            <div style="background:#0F1117;border-radius:8px;padding:16px;border:1px solid #2A304A">
              <div style="font-size:0.7rem;color:#4ECBA4;font-weight:600;margin-bottom:8px;letter-spacing:0.08em">LATENCIA PROMEDIO</div>
              <div style="font-family:JetBrains Mono,monospace;font-size:0.85rem;color:#E8ECF4">
                L = avg(ts_salida − ts_entrada)
              </div>
              <div style="font-size:0.72rem;color:#5C6B8A;margin-top:8px">
                ts_ingesta se añade al mensaje Kafka como time.time()
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)
