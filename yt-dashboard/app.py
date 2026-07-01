import streamlit as st

st.set_page_config(
    page_title="YT Political Monitor",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import inject_styles
from utils.data_loader import load_all_data
from pages import (
    resumen,
    tiempo_real,
    alertas,
    videos_criticos,
    autores,
    historico,
    jerguometro,
    metricas,
)

inject_styles()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <span class="brand-icon">📡</span>
            <span class="brand-name">YT Monitor</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="sidebar-label">ANÁLISIS POLÍTICO PERÚ</div>', unsafe_allow_html=True)
    st.markdown("---")

    nav_items = {
        "📊  Resumen general":   "resumen",
        "⚡  Tiempo real":       "tiempo_real",
        "🚨  Alertas":           "alertas",
        "🎬  Videos críticos":   "videos_criticos",
        "👤  Autores activos":   "autores",
        "📂  Histórico":         "historico",
        "🗣️  Jerguómetro":       "jerguometro",
        "📈  Métricas técnicas": "metricas",
    }

    if "page" not in st.session_state:
        st.session_state.page = "resumen"

    for label, key in nav_items.items():
        active = "nav-item active" if st.session_state.page == key else "nav-item"
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

    st.markdown("---")
    st.markdown(
        '<div class="sidebar-footer">Fuente: YouTube Data API v3<br>Pipeline: Kafka · Flink · Spark · S3</div>',
        unsafe_allow_html=True,
    )

# ── Load data ─────────────────────────────────────────────────────────────────
data = load_all_data()

# ── Route ─────────────────────────────────────────────────────────────────────
page = st.session_state.page
if page == "resumen":
    resumen.render(data)
elif page == "tiempo_real":
    tiempo_real.render(data)
elif page == "alertas":
    alertas.render(data)
elif page == "videos_criticos":
    videos_criticos.render(data)
elif page == "autores":
    autores.render(data)
elif page == "historico":
    historico.render(data)
elif page == "jerguometro":
    jerguometro.render(data)
elif page == "metricas":
    metricas.render(data)
