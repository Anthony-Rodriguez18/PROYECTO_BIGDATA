import streamlit as st
from utils.charts import line_chart, PALETTE
import plotly.graph_objects as go


def render(data: dict):
    st.markdown(
        f"""
        <div class="page-header">
          <div>
            <div class="page-title">Tiempo real</div>
            <div class="page-subtitle">Resultados de Apache Flink · auto-refresh cada 30s</div>
          </div>
          <div class="page-badge">⚡ STREAMING</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    auto = st.toggle("Auto-refresh (30s)", value=False)
    if auto:
        import time
        st.info("Auto-refresh activo — la página se recargará cada 30 segundos.")
        time.sleep(30)
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Frecuencia de ingesta (Flink Job 1) ──────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title"><span style="color:#4F6AF5">Job 1</span> — Frecuencia de ingesta por minuto</div>',
        unsafe_allow_html=True,
    )
    freq = data["flink1_frecuencia"]
    if not freq.empty and "window_start" in freq.columns and "count" in freq.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=freq["window_start"], y=freq["count"],
            mode="lines",
            line=dict(color="#4F6AF5", width=2),
            fill="tozeroy",
            fillcolor="rgba(79,106,245,0.1)",
            hovertemplate="Ventana %{x}: %{y} comentarios<extra></extra>",
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#9AA5C0", size=11),
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(gridcolor="#2A304A", linecolor="#2A304A", tickangle=-45, tickfont=dict(size=9)),
            yaxis=dict(gridcolor="#2A304A", linecolor="#2A304A"),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Pico máximo", f"{int(freq['count'].max())} msg/min")
        with col2:
            st.metric("Promedio", f"{freq['count'].mean():.0f} msg/min")
        with col3:
            st.metric("Última ventana", f"{int(freq['count'].iloc[-1])} msg/min")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tasa odio vs neutral (Flink Job 2) ───────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title"><span style="color:#4F6AF5">Job 2</span> — Tasa de odio vs neutral en vivo</div>',
        unsafe_allow_html=True,
    )
    tasa = data["flink2_tasa"]
    if not tasa.empty and "window" in tasa.columns:
        cats = [c for c in ["ODIO_POLITICO", "ODIO_DEMOGRAFICO", "ODIO_GENERAL", "NEUTRAL"] if c in tasa.columns]
        fig2 = go.Figure()
        for cat in cats:
            fig2.add_trace(go.Scatter(
                x=tasa["window"], y=tasa[cat],
                name=cat,
                mode="lines",
                line=dict(color=PALETTE.get(cat, "#5C6B8A"), width=2),
                stackgroup="one",
                hovertemplate=f"{cat}: %{{y}}<extra></extra>",
            ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#9AA5C0", size=11),
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(gridcolor="#2A304A", linecolor="#2A304A", tickangle=-45, tickfont=dict(size=9)),
            yaxis=dict(gridcolor="#2A304A", linecolor="#2A304A"),
            legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)", font=dict(size=10)),
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

        # last window stats
        if len(tasa) > 0:
            last = tasa.iloc[-1]
            cols = st.columns(4)
            for col, cat in zip(cols, ["ODIO_POLITICO","ODIO_DEMOGRAFICO","ODIO_GENERAL","NEUTRAL"]):
                val = int(last.get(cat, 0))
                color = PALETTE.get(cat, "#5C6B8A")
                with col:
                    st.markdown(
                        f"""
                        <div style="background:#1E2235;border:1px solid #2A304A;border-radius:10px;padding:12px;border-top:3px solid {color}">
                          <div style="font-size:0.65rem;color:#5C6B8A;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:4px">{cat}</div>
                          <div style="font-size:1.4rem;font-weight:700;color:#E8ECF4">{val}</div>
                          <div style="font-size:0.7rem;color:#5C6B8A">última ventana</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
    st.markdown('</div>', unsafe_allow_html=True)
