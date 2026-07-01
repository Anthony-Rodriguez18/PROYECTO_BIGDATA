import streamlit as st
from utils.charts import donut_chart, PALETTE


def render(data: dict):
    src_badge = "● S3 en vivo" if data["source"] == "s3" else ("● Local" if data["source"] == "local" else "● Demo simulada")
    st.markdown(
        f"""
        <div class="page-header">
          <div>
            <div class="page-title">Resumen general</div>
            <div class="page-subtitle">Última actualización: {data['last_updated']}</div>
          </div>
          <div class="page-badge">{src_badge}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    dist = data["spark1_distribucion"]
    total = int(dist["count"].sum()) if not dist.empty else 0
    odio_pol  = int(dist.loc[dist["clasificacion"] == "ODIO_POLITICO",    "count"].sum())
    odio_demo = int(dist.loc[dist["clasificacion"] == "ODIO_DEMOGRAFICO", "count"].sum())
    odio_gen  = int(dist.loc[dist["clasificacion"] == "ODIO_GENERAL",     "count"].sum())
    neutral   = int(dist.loc[dist["clasificacion"] == "NEUTRAL",          "count"].sum())
    total_odio = odio_pol + odio_demo + odio_gen
    pct_odio = round(total_odio / total * 100, 1) if total else 0

    # ── KPI row ──────────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    cards = [
        (c1, "TOTAL COMENTARIOS",    f"{total:,}",       "",                    "accent"),
        (c2, "ODIO POLÍTICO",        f"{odio_pol:,}",    "ODIO_POLITICO",       "danger"),
        (c3, "ODIO DEMOGRÁFICO",     f"{odio_demo:,}",   "ODIO_DEMOGRAFICO",    "warn"),
        (c4, "ODIO GENERAL",         f"{odio_gen:,}",    "ODIO_GENERAL",        ""),
        (c5, "NEUTRAL",              f"{neutral:,}",     "NEUTRAL",             "ok"),
    ]
    for col, label, value, cat, variant in cards:
        with col:
            st.markdown(
                f"""
                <div class="stat-card {variant}">
                  <div class="stat-label">{label}</div>
                  <div class="stat-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Donut + summary ──────────────────────────────────────────────────────
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Distribución por categoría</div>', unsafe_allow_html=True)
        if not dist.empty:
            fig = donut_chart(dist, "clasificacion", "count")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Indicadores clave</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        met1, met2 = st.columns(2)
        with met1:
            st.metric("% Contenido odio", f"{pct_odio}%", delta=f"{pct_odio - 50:.1f}pp vs 50%")
        with met2:
            ratio = data["spark4_polarizacion"]
            st.metric("Ratio polarización", f"{ratio.get('ratio', 0):.2f}",
                      help="Odio político / odio demográfico")

        st.markdown("<br>", unsafe_allow_html=True)

        rows = [
            ("ODIO_POLITICO",    odio_pol,  total),
            ("ODIO_DEMOGRAFICO", odio_demo, total),
            ("ODIO_GENERAL",     odio_gen,  total),
            ("NEUTRAL",          neutral,   total),
        ]
        for cat, val, tot in rows:
            pct = val / tot * 100 if tot else 0
            color = PALETTE.get(cat, "#5C6B8A")
            st.markdown(
                f"""
                <div style="margin-bottom:12px">
                  <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                    <span style="font-size:0.78rem;color:#9AA5C0">{cat}</span>
                    <span style="font-size:0.78rem;font-family:JetBrains Mono,monospace;color:#E8ECF4">{val:,} ({pct:.1f}%)</span>
                  </div>
                  <div style="background:#2A304A;border-radius:4px;height:6px">
                    <div style="background:{color};width:{pct}%;height:6px;border-radius:4px"></div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Top videos preview ───────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Videos con mayor toxicidad (resumen)</div>', unsafe_allow_html=True)
    tv = data["flink4_top_videos"].sort_values("odio_count", ascending=False).head(5)
    if not tv.empty:
        for _, row in tv.iterrows():
            pct_bar = min(int(row["odio_count"] / tv["odio_count"].max() * 100), 100)
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid #2A304A">
                  <div style="flex:1;font-size:0.82rem;color:#E8ECF4">{row['video_title']}</div>
                  <div style="width:160px;background:#2A304A;border-radius:4px;height:6px">
                    <div style="background:#E05A5A;width:{pct_bar}%;height:6px;border-radius:4px"></div>
                  </div>
                  <div style="font-family:JetBrains Mono,monospace;font-size:0.75rem;color:#E05A5A;min-width:40px;text-align:right">{int(row['odio_count'])}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)
