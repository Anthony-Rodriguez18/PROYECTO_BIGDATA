import streamlit as st

def inject_styles():
    st.markdown(
        """
        <style>
        /* ── Google Fonts ── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        /* ── Root palette ── */
        :root {
            --bg-base:      #0F1117;
            --bg-surface:   #181C27;
            --bg-card:      #1E2235;
            --bg-card-alt:  #232840;
            --accent:       #4F6AF5;
            --accent-soft:  #3B51D4;
            --accent-glow:  rgba(79,106,245,0.18);
            --danger:       #E05A5A;
            --danger-soft:  rgba(224,90,90,0.15);
            --warn:         #F0A84A;
            --warn-soft:    rgba(240,168,74,0.15);
            --ok:           #4ECBA4;
            --ok-soft:      rgba(78,203,164,0.15);
            --neutral:      #7B8DB0;
            --text-primary: #E8ECF4;
            --text-secondary:#9AA5C0;
            --text-dim:     #5C6B8A;
            --border:       #2A304A;
            --border-light: #313959;
        }

        /* ── Global reset ── */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: var(--bg-base) !important;
            font-family: 'Inter', sans-serif;
            color: var(--text-primary);
        }

        [data-testid="stMain"] {
            background-color: var(--bg-base) !important;
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background-color: var(--bg-surface) !important;
            border-right: 1px solid var(--border) !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.5rem;
        }

        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 0 1rem 0.5rem;
        }

        .brand-icon {
            font-size: 1.6rem;
        }

        .brand-name {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.02em;
        }

        .sidebar-label {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.62rem;
            font-weight: 500;
            color: var(--accent);
            letter-spacing: 0.12em;
            padding: 0 1rem 0.5rem;
        }

        /* Nav buttons */
        [data-testid="stSidebar"] button {
            background: transparent !important;
            border: none !important;
            color: var(--text-secondary) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            text-align: left !important;
            padding: 0.55rem 1rem !important;
            border-radius: 8px !important;
            transition: all 0.15s ease !important;
            margin-bottom: 2px !important;
        }

        [data-testid="stSidebar"] button:hover {
            background: var(--accent-glow) !important;
            color: var(--text-primary) !important;
        }

        [data-testid="stSidebar"] button:focus {
            background: var(--accent-glow) !important;
            color: var(--accent) !important;
            box-shadow: none !important;
        }

        .sidebar-footer {
            font-size: 0.72rem;
            color: var(--text-dim);
            line-height: 1.6;
            padding: 0.5rem 1rem;
        }

        /* ── Main content ── */
        .block-container {
            padding: 2rem 2rem 3rem !important;
            max-width: 100% !important;
        }

        /* ── Page header ── */
        .page-header {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            margin-bottom: 1.75rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }

        .page-title {
            font-size: 1.6rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.03em;
            margin: 0;
        }

        .page-subtitle {
            font-size: 0.8rem;
            color: var(--text-dim);
            font-family: 'JetBrains Mono', monospace;
            margin-top: 4px;
        }

        .page-badge {
            font-size: 0.7rem;
            font-family: 'JetBrains Mono', monospace;
            background: var(--accent-glow);
            color: var(--accent);
            border: 1px solid var(--accent);
            border-radius: 20px;
            padding: 4px 12px;
        }

        /* ── Stat cards ── */
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            position: relative;
            overflow: hidden;
            transition: border-color 0.2s;
        }

        .stat-card:hover {
            border-color: var(--border-light);
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: var(--accent);
            border-radius: 12px 12px 0 0;
        }

        .stat-card.danger::before  { background: var(--danger); }
        .stat-card.warn::before    { background: var(--warn); }
        .stat-card.ok::before      { background: var(--ok); }
        .stat-card.neutral::before { background: var(--neutral); }

        .stat-label {
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            color: var(--text-dim);
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.04em;
            line-height: 1;
        }

        .stat-delta {
            font-size: 0.78rem;
            color: var(--text-secondary);
            margin-top: 0.4rem;
        }

        .stat-delta.up   { color: var(--danger); }
        .stat-delta.down { color: var(--ok); }

        /* ── Section cards ── */
        .section-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1.25rem;
        }

        .section-title {
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            color: var(--text-secondary);
            text-transform: uppercase;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .section-title::after {
            content: '';
            flex: 1;
            height: 1px;
            background: var(--border);
        }

        /* ── Alert rows ── */
        .alert-row {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 0.75rem 0;
            border-bottom: 1px solid var(--border);
        }

        .alert-row:last-child { border-bottom: none; }

        .alert-dot {
            width: 8px; height: 8px;
            border-radius: 50%;
            flex-shrink: 0;
        }

        .alert-dot.high   { background: var(--danger); box-shadow: 0 0 6px var(--danger); }
        .alert-dot.medium { background: var(--warn); }
        .alert-dot.low    { background: var(--ok); }

        .alert-text {
            font-size: 0.82rem;
            color: var(--text-primary);
            flex: 1;
        }

        .alert-time {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            color: var(--text-dim);
        }

        /* ── Tag pills ── */
        .tag {
            display: inline-block;
            font-size: 0.65rem;
            font-weight: 600;
            letter-spacing: 0.06em;
            padding: 3px 9px;
            border-radius: 20px;
            text-transform: uppercase;
        }

        .tag-odio-politico   { background: rgba(224,90,90,0.2);  color: #E05A5A; }
        .tag-odio-demografico{ background: rgba(240,168,74,0.2); color: #F0A84A; }
        .tag-odio-general    { background: rgba(79,106,245,0.2); color: #7B9AF7; }
        .tag-neutral         { background: rgba(78,203,164,0.15);color: #4ECBA4; }

        /* ── Table overrides ── */
        [data-testid="stDataFrame"] {
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
            overflow: hidden !important;
        }

        /* ── Divider ── */
        hr { border-color: var(--border) !important; }

        /* ── Plotly chart bg ── */
        .js-plotly-plot .plotly .bg {
            fill: transparent !important;
        }

        /* ── Streamlit overrides ── */
        [data-testid="metric-container"] {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1rem;
        }

        [data-testid="stMetric"] label {
            color: var(--text-dim) !important;
            font-size: 0.72rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase !important;
        }

        [data-testid="stMetricValue"] {
            color: var(--text-primary) !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
        }

        [data-testid="stMetricDelta"] {
            font-size: 0.78rem !important;
        }

        /* scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg-base); }
        ::-webkit-scrollbar-thumb { background: var(--border-light); border-radius: 3px; }
        </style>
        """,
        unsafe_allow_html=True,
    )
