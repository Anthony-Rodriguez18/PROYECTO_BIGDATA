import streamlit as st
from utils.charts import horizontal_bar


def render(data: dict):
    st.markdown(
        """
        <div class="page-header">
          <div>
            <div class="page-title">Videos críticos</div>
            <div class="page-subtitle">Flink Job 4 — videos con mayor concentración de comentarios tóxicos</div>
          </div>
          <div class="page-badge">🎬 FLINK</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = data["flink4_top_videos"].sort_values("odio_count", ascending=False)

    if df.empty:
        st.info("Sin datos de videos disponibles.")
        return

    # ── KPIs ─────────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""<div class="stat-card danger">
              <div class="stat-label">VIDEO MÁS TÓXICO</div>
              <div style="font-size:1rem;font-weight:600;color:#E8ECF4;margin-top:6px;line-height:1.3">
                {df.iloc[0]['video_title'][:40]}…
              </div>
            </div>""", unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""<div class="stat-card warn">
              <div class="stat-label">PICO DE ODIO</div>
              <div class="stat-value">{int(df['odio_count'].max()):,}</div>
              <div class="stat-delta">comentarios de odio</div>
            </div>""", unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""<div class="stat-card">
              <div class="stat-label">VIDEOS MONITOREADOS</div>
              <div class="stat-value">{len(df)}</div>
            </div>""", unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_chart, col_table = st.columns([1.2, 1])

    with col_chart:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Ranking por comentarios de odio</div>', unsafe_allow_html=True)
        fig = horizontal_bar(df, "video_title", "odio_count", color="#E05A5A")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_table:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Detalle por video</div>', unsafe_allow_html=True)
        max_val = df["odio_count"].max()
        for _, row in df.iterrows():
            pct = int(row["odio_count"] / max_val * 100)
            rank_color = "#E05A5A" if pct > 70 else ("#F0A84A" if pct > 40 else "#4ECBA4")
            st.markdown(
                f"""
                <div style="padding:10px 0;border-bottom:1px solid #2A304A">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                    <span style="font-size:0.8rem;color:#E8ECF4">{row['video_title'][:35]}…</span>
                    <span style="font-family:JetBrains Mono,monospace;font-size:0.78rem;font-weight:600;color:{rank_color}">
                      {int(row['odio_count'])}
                    </span>
                  </div>
                  <div style="display:flex;align-items:center;gap:8px">
                    <div style="flex:1;background:#2A304A;border-radius:3px;height:4px">
                      <div style="background:{rank_color};width:{pct}%;height:4px;border-radius:3px"></div>
                    </div>
                    <span style="font-size:0.65rem;color:#5C6B8A;font-family:JetBrains Mono,monospace">{row.get('query','')[:20]}</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)
