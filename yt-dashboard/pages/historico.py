import streamlit as st
from utils.charts import donut_chart, horizontal_bar, PALETTE
import plotly.graph_objects as go


def render(data: dict):
    st.markdown(
        """
        <div class="page-header">
          <div>
            <div class="page-title">Análisis histórico</div>
            <div class="page-subtitle">Apache Spark batch — agregaciones sobre el dataset completo</div>
          </div>
          <div class="page-badge">📂 SPARK</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Job 1: Distribución global ───────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title"><span style="color:#4ECBA4">Job 1</span> — Distribución global de clases</div>',
        unsafe_allow_html=True,
    )
    dist = data["spark1_distribucion"]
    col_d, col_stats = st.columns([1, 1])
    with col_d:
        if not dist.empty:
            fig = donut_chart(dist, "clasificacion", "count")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with col_stats:
        st.markdown("<br>", unsafe_allow_html=True)
        total = int(dist["count"].sum()) if not dist.empty else 0
        for _, row in dist.iterrows():
            cat = row["clasificacion"]
            val = int(row["count"])
            pct = val / total * 100 if total else 0
            color = PALETTE.get(cat, "#5C6B8A")
            st.markdown(
                f"""
                <div style="margin-bottom:14px">
                  <div style="display:flex;justify-content:space-between;margin-bottom:5px">
                    <span style="font-size:0.8rem;color:#9AA5C0">{cat}</span>
                    <span style="font-size:0.8rem;font-family:JetBrains Mono,monospace;color:#E8ECF4">
                      {val:,} <span style="color:#5C6B8A">({pct:.1f}%)</span>
                    </span>
                  </div>
                  <div style="background:#2A304A;border-radius:4px;height:7px">
                    <div style="background:{color};width:{pct:.1f}%;height:7px;border-radius:4px"></div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Job 3: Longitud promedio ─────────────────────────────────────────────
    col_long, col_polar = st.columns(2)

    with col_long:
        st.markdown('<div class="section-card" style="height:100%">', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-title"><span style="color:#4ECBA4">Job 3</span> — Longitud promedio por clase</div>',
            unsafe_allow_html=True,
        )
        lon = data["spark3_longitud"]
        if not lon.empty and "clasificacion" in lon.columns and "longitud_promedio" in lon.columns:
            colors = [PALETTE.get(c, "#5C6B8A") for c in lon["clasificacion"]]
            fig3 = go.Figure(go.Bar(
                x=lon["clasificacion"],
                y=lon["longitud_promedio"],
                marker=dict(color=colors, line=dict(width=0)),
                hovertemplate="%{x}: %{y:.1f} chars<extra></extra>",
            ))
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#9AA5C0", size=11),
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(gridcolor="#2A304A", linecolor="#2A304A"),
                yaxis=dict(gridcolor="#2A304A", linecolor="#2A304A", title="caracteres promedio"),
                showlegend=False,
            )
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_polar:
        st.markdown('<div class="section-card" style="height:100%">', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-title"><span style="color:#4ECBA4">Job 4</span> — Ratio de polarización</div>',
            unsafe_allow_html=True,
        )
        pol = data["spark4_polarizacion"]
        if pol:
            op  = pol.get("odio_politico", 0)
            od  = pol.get("odio_demografico", 0)
            rat = pol.get("ratio", 0)
            tot = pol.get("total_odio", op + od)

            st.markdown(
                f"""
                <div style="text-align:center;padding:20px 0">
                  <div style="font-size:3rem;font-weight:700;color:#E8ECF4;letter-spacing:-0.04em">{rat}</div>
                  <div style="font-size:0.8rem;color:#5C6B8A;margin-bottom:24px">odio político / odio demográfico</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            fig4 = go.Figure(go.Bar(
                x=["ODIO_POLÍTICO", "ODIO_DEMOGRÁFICO"],
                y=[op, od],
                marker=dict(color=["#E05A5A", "#F0A84A"], line=dict(width=0)),
                hovertemplate="%{x}: %{y:,}<extra></extra>",
            ))
            fig4.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#9AA5C0", size=11),
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(gridcolor="#2A304A", linecolor="#2A304A"),
                yaxis=dict(gridcolor="#2A304A", linecolor="#2A304A"),
                showlegend=False,
            )
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)
