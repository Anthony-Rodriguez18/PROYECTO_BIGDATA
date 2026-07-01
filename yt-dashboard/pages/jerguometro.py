import streamlit as st
from utils.charts import horizontal_bar
import plotly.graph_objects as go


JERGA_POLITICA = {"terruco","terruca","fujitroll","fujimorista","caviar","lapicito","rojo","libertarado","cojudigno"}
JERGA_DEMO     = {"cholo","chola","serrano","serrana","andino","llama","indio","mestizo"}


def _color(term: str) -> str:
    t = term.lower()
    if t in JERGA_POLITICA:
        return "#E05A5A"
    if t in JERGA_DEMO:
        return "#F0A84A"
    return "#7B9AF7"


def render(data: dict):
    st.markdown(
        """
        <div class="page-header">
          <div>
            <div class="page-title">Jerguómetro</div>
            <div class="page-subtitle">Spark Jobs 2 & 5 — frecuencia de jerga política y demográfica peruana</div>
          </div>
          <div class="page-badge">🗣️ SPARK</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Legend
    st.markdown(
        """
        <div style="display:flex;gap:16px;margin-bottom:20px">
          <div style="display:flex;align-items:center;gap:6px">
            <div style="width:10px;height:10px;border-radius:50%;background:#E05A5A"></div>
            <span style="font-size:0.75rem;color:#9AA5C0">Jerga política</span>
          </div>
          <div style="display:flex;align-items:center;gap:6px">
            <div style="width:10px;height:10px;border-radius:50%;background:#F0A84A"></div>
            <span style="font-size:0.75rem;color:#9AA5C0">Jerga demográfica</span>
          </div>
          <div style="display:flex;align-items:center;gap:6px">
            <div style="width:10px;height:10px;border-radius:50%;background:#7B9AF7"></div>
            <span style="font-size:0.75rem;color:#9AA5C0">Otra</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    jerg = data["spark2_jerguometro"].sort_values("frecuencia", ascending=False)
    top_pal = data["spark5_top_palabras"].sort_values("frecuencia", ascending=False)

    col_jerg, col_pal = st.columns([1, 1])

    # ── Jerguómetro ──────────────────────────────────────────────────────────
    with col_jerg:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Job 2 — Jerga política y demográfica</div>', unsafe_allow_html=True)

        if not jerg.empty:
            colors = [_color(t) for t in jerg["termino"]]
            fig = go.Figure(go.Bar(
                x=jerg["frecuencia"],
                y=jerg["termino"],
                orientation="h",
                marker=dict(color=colors, line=dict(width=0)),
                hovertemplate="%{y}: %{x} menciones<extra></extra>",
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#9AA5C0", size=11),
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(gridcolor="#2A304A", linecolor="#2A304A"),
                yaxis=dict(autorange="reversed", gridcolor="#2A304A", linecolor="#2A304A", tickfont=dict(size=11)),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Top palabras ─────────────────────────────────────────────────────────
    with col_pal:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Job 5 — Top palabras en comentarios de odio</div>', unsafe_allow_html=True)

        if not top_pal.empty:
            max_f = top_pal["frecuencia"].max()
            for _, row in top_pal.iterrows():
                pct = int(row["frecuencia"] / max_f * 100)
                c = _color(row["palabra"])
                st.markdown(
                    f"""
                    <div style="display:flex;align-items:center;gap:10px;padding:7px 0;border-bottom:1px solid #2A304A">
                      <span style="font-family:JetBrains Mono,monospace;font-size:0.82rem;
                            color:{c};min-width:110px">{row['palabra']}</span>
                      <div style="flex:1;background:#2A304A;border-radius:3px;height:6px">
                        <div style="background:{c};width:{pct}%;height:6px;border-radius:3px;
                             opacity:0.85"></div>
                      </div>
                      <span style="font-family:JetBrains Mono,monospace;font-size:0.75rem;
                            color:#5C6B8A;min-width:40px;text-align:right">{int(row['frecuencia'])}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Bubble cloud (visual bonus) ──────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Intensidad relativa de términos</div>', unsafe_allow_html=True)

    if not jerg.empty:
        import random
        random.seed(42)
        x = [random.uniform(0.05, 0.95) for _ in range(len(jerg))]
        y = [random.uniform(0.1, 0.9) for _ in range(len(jerg))]
        sizes = [max(14, int(r["frecuencia"] / jerg["frecuencia"].max() * 60)) for _, r in jerg.iterrows()]
        colors = [_color(t) for t in jerg["termino"]]
        fig_b = go.Figure(go.Scatter(
            x=x, y=y,
            mode="markers+text",
            marker=dict(size=sizes, color=colors, opacity=0.7, line=dict(width=0)),
            text=jerg["termino"],
            textfont=dict(size=10, color="#E8ECF4"),
            textposition="middle center",
            hovertemplate="%{text}: %{marker.size} menciones relativas<extra></extra>",
        ))
        fig_b.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=220,
            font=dict(family="Inter", color="#9AA5C0"),
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(visible=False), yaxis=dict(visible=False),
            showlegend=False,
        )
        st.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)
