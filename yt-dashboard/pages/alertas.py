import streamlit as st


LEVEL_COLOR = {"HIGH": "#E05A5A", "MEDIUM": "#F0A84A", "LOW": "#4ECBA4"}
LEVEL_LABEL = {"HIGH": "CRÍTICA", "MEDIUM": "MEDIA", "LOW": "BAJA"}


def render(data: dict):
    st.markdown(
        """
        <div class="page-header">
          <div>
            <div class="page-title">Alertas de polarización</div>
            <div class="page-subtitle">Flink Job 3 — picos de odio político en ventanas deslizantes</div>
          </div>
          <div class="page-badge">🚨 EN VIVO</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    alerts = data["flink3_alertas"]

    if alerts.empty:
        st.info("Sin alertas registradas en este período.")
        return

    high   = alerts[alerts["level"] == "HIGH"]
    medium = alerts[alerts["level"] == "MEDIUM"]
    low    = alerts[alerts["level"] == "LOW"]

    c1, c2, c3 = st.columns(3)
    for col, df, label, color in [
        (c1, high,   "CRÍTICAS",  "#E05A5A"),
        (c2, medium, "MEDIAS",    "#F0A84A"),
        (c3, low,    "BAJAS",     "#4ECBA4"),
    ]:
        with col:
            st.markdown(
                f"""
                <div class="stat-card" style="border-top:3px solid {color}">
                  <div class="stat-label">{label}</div>
                  <div class="stat-value" style="color:{color}">{len(df)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Alert feed ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Feed de alertas recientes</div>', unsafe_allow_html=True)

    for _, row in alerts.iterrows():
        level = row.get("level", "LOW")
        color = LEVEL_COLOR.get(level, "#5C6B8A")
        label = LEVEL_LABEL.get(level, level)
        msg   = row.get("message", "")
        ts    = row.get("timestamp", "")

        st.markdown(
            f"""
            <div style="display:flex;align-items:flex-start;gap:14px;padding:14px 0;border-bottom:1px solid #2A304A">
              <div style="margin-top:4px">
                <div style="width:10px;height:10px;border-radius:50%;background:{color};
                     {'box-shadow:0 0 8px ' + color if level == 'HIGH' else ''}"></div>
              </div>
              <div style="flex:1">
                <div style="font-size:0.82rem;color:#E8ECF4;line-height:1.5">{msg}</div>
              </div>
              <div style="display:flex;flex-direction:column;align-items:flex-end;gap:6px;flex-shrink:0">
                <span style="font-size:0.62rem;font-weight:700;letter-spacing:0.08em;padding:3px 8px;border-radius:20px;
                     background:{color}22;color:{color}">{label}</span>
                <span style="font-family:JetBrains Mono,monospace;font-size:0.68rem;color:#5C6B8A">{ts}</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Explanation ───────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="background:#1E2235;border:1px solid #2A304A;border-left:3px solid #4F6AF5;
             border-radius:8px;padding:14px 16px;margin-top:16px">
          <div style="font-size:0.75rem;color:#7B9AF7;font-weight:600;margin-bottom:4px">¿CÓMO SE GENERAN?</div>
          <div style="font-size:0.8rem;color:#9AA5C0;line-height:1.6">
            Flink evalúa ventanas deslizantes de 60 segundos sobre el topic
            <code style="background:#0F1117;padding:1px 5px;border-radius:3px;font-size:0.75rem">youtube_comentarios_crudos</code>.
            Si en una ventana se supera el umbral de menciones clasificadas como
            <strong style="color:#E05A5A">ODIO_POLITICO</strong>, se genera una alerta y se escribe en
            <code style="background:#0F1117;padding:1px 5px;border-radius:3px;font-size:0.75rem">s3://…/tiempo_real/job3_alertas/</code>.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
