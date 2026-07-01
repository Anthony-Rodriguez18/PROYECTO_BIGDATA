"""Shared Plotly chart helpers with consistent dark theme."""
import plotly.express as px
import plotly.graph_objects as go

PALETTE = {
    "ODIO_POLITICO":    "#E05A5A",
    "ODIO_DEMOGRAFICO": "#F0A84A",
    "ODIO_GENERAL":     "#7B9AF7",
    "NEUTRAL":          "#4ECBA4",
}

LAYOUT_DEFAULTS = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#9AA5C0", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(0,0,0,0)",
        font=dict(size=11),
    ),
    xaxis=dict(
        gridcolor="#2A304A",
        linecolor="#2A304A",
        tickfont=dict(size=10),
    ),
    yaxis=dict(
        gridcolor="#2A304A",
        linecolor="#2A304A",
        tickfont=dict(size=10),
    ),
)

def _apply(fig):
    fig.update_layout(**LAYOUT_DEFAULTS)
    return fig


def bar_chart(df, x, y, color=None, title="", horizontal=False, color_map=None):
    orientation = "h" if horizontal else "v"
    kw = dict(x=y, y=x, orientation="h") if horizontal else dict(x=x, y=y)
    if color and color_map:
        kw["color"] = color
        kw["color_discrete_map"] = color_map
    elif color:
        kw["color"] = color
    fig = px.bar(df, title=title, **kw)
    fig.update_traces(marker_line_width=0)
    return _apply(fig)


def line_chart(df, x, y_cols, title="", colors=None):
    fig = go.Figure()
    palette = colors or list(PALETTE.values())
    for i, col in enumerate(y_cols):
        fig.add_trace(go.Scatter(
            x=df[x], y=df[col], name=col,
            mode="lines",
            line=dict(color=palette[i % len(palette)], width=2),
            fill="tozeroy",
            fillcolor=palette[i % len(palette)].replace(")", ",0.08)").replace("rgb(", "rgba(").replace("#", "rgba(").replace("E05A5A,0.08)", "224,90,90,0.08)").replace("F0A84A,0.08)", "240,168,74,0.08)").replace("7B9AF7,0.08)", "123,154,247,0.08)").replace("4ECBA4,0.08)", "78,203,164,0.08)"),
        ))
    fig.update_layout(title=title)
    return _apply(fig)


def donut_chart(df, names, values, title=""):
    colors = [PALETTE.get(n, "#5C6B8A") for n in df[names]]
    fig = go.Figure(go.Pie(
        labels=df[names],
        values=df[values],
        hole=0.62,
        marker=dict(colors=colors, line=dict(color="#0F1117", width=3)),
        textfont=dict(size=11),
        hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
    ))
    fig.update_layout(title=title, showlegend=True)
    return _apply(fig)


def horizontal_bar(df, label_col, value_col, title="", color="#4F6AF5"):
    fig = go.Figure(go.Bar(
        x=df[value_col],
        y=df[label_col],
        orientation="h",
        marker=dict(color=color, line=dict(width=0)),
        hovertemplate="%{y}: %{x}<extra></extra>",
    ))
    fig.update_layout(title=title, yaxis=dict(autorange="reversed", gridcolor="#2A304A", linecolor="#2A304A", tickfont=dict(size=11)))
    return _apply(fig)
