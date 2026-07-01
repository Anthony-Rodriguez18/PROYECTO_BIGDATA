import streamlit as st
from utils.charts import horizontal_bar


def render(data: dict):
    st.markdown(
        """
        <div class="page-header">
          <div>
            <div class="page-title">Autores activos</div>
            <div class="page-subtitle">Flink Job 5 — usuarios con mayor cantidad de comentarios de odio detectados</div>
          </div>
          <div class="page-badge">👤 FLINK</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="background:#1E2235;border:1px solid #F0A84A33;border-left:3px solid #F0A84A;
             border-radius:8px;padding:12px 16px;margin-bottom:20px">
          <div style="font-size:0.75rem;color:#F0A84A;font-weight:600;margin-bottom:2px">NOTA ÉTICA</div>
          <div style="font-size:0.8rem;color:#9AA5C0;line-height:1.5">
            Este análisis es exclusivamente académico y agregado. Los identificadores mostrados corresponden
            a nombres públicos de YouTube y no se cruzan con ninguna otra fuente de datos personal.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = data["flink5_trolls"].sort_values("hate_count", ascending=False)

    if df.empty:
        st.info("Sin datos de autores disponibles.")
        return

    top3 = df.head(3)
    cols = st.columns(3)
    medals = ["🥇", "🥈", "🥉"]
    for i, (col, (_, row)) in enumerate(zip(cols, top3.iterrows())):
        with col:
            st.markdown(
                f"""
                <div class="stat-card {'danger' if i == 0 else 'warn' if i == 1 else ''}">
                  <div class="stat-label">{medals[i]} PUESTO {i+1}</div>
                  <div style="font-size:1rem;font-weight:600;color:#E8ECF4;margin:6px 0 4px;
                       font-family:JetBrains Mono,monospace">{row['author']}</div>
                  <div style="font-size:1.6rem;font-weight:700;color:#E05A5A">{int(row['hate_count'])}</div>
                  <div class="stat-delta">comentarios de odio</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    col_chart, col_list = st.columns([1.2, 1])

    with col_chart:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Ranking completo</div>', unsafe_allow_html=True)
        fig = horizontal_bar(df.head(10), "author", "hate_count", color="#F0A84A")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_list:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Tabla detalle</div>', unsafe_allow_html=True)
        max_val = df["hate_count"].max()
        for rank, (_, row) in enumerate(df.iterrows(), 1):
            pct = int(row["hate_count"] / max_val * 100) if max_val else 0
            color = "#E05A5A" if pct > 70 else ("#F0A84A" if pct > 40 else "#7B9AF7")
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #2A304A">
                  <span style="font-size:0.7rem;color:#5C6B8A;font-family:JetBrains Mono,monospace;
                        min-width:22px;text-align:right">#{rank}</span>
                  <span style="flex:1;font-size:0.8rem;color:#E8ECF4;font-family:JetBrains Mono,monospace">
                    {row['author']}
                  </span>
                  <div style="width:80px;background:#2A304A;border-radius:3px;height:4px">
                    <div style="background:{color};width:{pct}%;height:4px;border-radius:3px"></div>
                  </div>
                  <span style="font-size:0.78rem;font-weight:600;color:{color};
                        font-family:JetBrains Mono,monospace;min-width:28px;text-align:right">
                    {int(row['hate_count'])}
                  </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)
