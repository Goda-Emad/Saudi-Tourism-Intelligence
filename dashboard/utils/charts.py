# ═══════════════════════════════════════════════════════════════════
#  utils/charts.py — Saudi Tourism Intelligence
#  Author : Eng. Goda Emad
#  Merged : Original chart functions + DataSaudi design system
# ═══════════════════════════════════════════════════════════════════
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd
import numpy as np

# ═══════════════════════════════════════════════════════
# LAYOUT HELPER  (DataSaudi design system)
# ═══════════════════════════════════════════════════════
def apply_layout(fig: go.Figure, height: int = 360,
                 font_color: str = "#A1A6B7",
                 font_family: str = "IBM Plex Sans",
                 template: str = "plotly_dark") -> go.Figure:
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor ="rgba(0,0,0,0)",
        font=dict(color=font_color, family=font_family),
        height=height,
        margin=dict(l=10, r=10, t=36, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11),
                    orientation="h", y=-0.2),
        xaxis=dict(gridcolor="rgba(42,50,53,0.4)",
                   linecolor="#2A3235", tickfont=dict(size=10)),
        yaxis=dict(gridcolor="rgba(42,50,53,0.4)",
                   linecolor="#2A3235", tickfont=dict(size=10)),
    )
    return fig

def render_chart(fig: go.Figure) -> None:
    st.plotly_chart(fig, use_container_width=True,
                    config={"displayModeBar": False})

# ═══════════════════════════════════════════════════════
# BASE CHARTS  (original API preserved)
# ═══════════════════════════════════════════════════════
def create_trend_chart(df, x_col, y_col, title, color=None, template="plotly_dark"):
    fig = px.line(df, x=x_col, y=y_col, title=title,
                  color=color, template=template)
    apply_layout(fig)
    return fig

def create_bar_chart(df, x_col, y_col, title, color=None,
                     barmode='group', template="plotly_dark"):
    fig = px.bar(df, x=x_col, y=y_col, title=title,
                 color=color, barmode=barmode, template=template)
    apply_layout(fig)
    return fig

def create_line_chart(df, x_col, y_col, title, color=None, template="plotly_dark"):
    fig = px.line(df, x=x_col, y=y_col, title=title,
                  color=color, template=template)
    apply_layout(fig)
    return fig

def create_area_chart(df, x_col, y_col, title, color=None, template="plotly_dark"):
    fig = px.area(df, x=x_col, y=y_col, title=title,
                  color=color, template=template)
    apply_layout(fig)
    return fig

def create_pie_chart(values, labels, title, colors=None, template="plotly_dark"):
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.45,
        marker=dict(colors=colors) if colors else None,
        textinfo='label+percent', textposition='auto'))
    fig.update_layout(title=title, template=template,
                      margin=dict(l=10,r=10,t=36,b=10))
    return fig

def create_heatmap(data, x_labels, y_labels, title,
                   colorscale='Teal', template="plotly_dark"):
    fig = go.Figure(go.Heatmap(
        z=data, x=x_labels, y=y_labels,
        colorscale=colorscale,
        text=[[f"{v:.1f}" for v in row] for row in data],
        texttemplate="%{text}", textfont=dict(size=9),
        hovertemplate="<b>%{y}</b><br>%{x}: %{z:.1f}<extra></extra>"))
    fig.update_layout(title=title, template=template,
                      margin=dict(l=10,r=10,t=36,b=10))
    return fig

def create_radar_chart(categories, values, title,
                       color="#17B19B", template="plotly_dark"):
    cats = categories + [categories[0]]
    vals = values + [values[0]]
    fig = go.Figure(go.Scatterpolar(
        r=vals, theta=cats, fill='toself',
        fillcolor=f"rgba(23,177,155,0.2)",
        line=dict(color=color, width=2),
        marker=dict(color=color, size=7)))
    fig.update_layout(
        title=title, template=template,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True,
                           gridcolor="rgba(42,50,53,0.5)",
                           tickfont=dict(size=9)),
            angularaxis=dict(gridcolor="rgba(42,50,53,0.5)",
                             tickfont=dict(size=10))),
        margin=dict(l=40,r=40,t=36,b=10))
    return fig

# ═══════════════════════════════════════════════════════
# COMPARISON CHARTS
# ═══════════════════════════════════════════════════════
def create_comparison_chart(inbound_data, domestic_data, years, title,
                             template="plotly_dark"):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=years, y=inbound_data,  name='Inbound',
                         marker_color='#17B19B', opacity=.85,
                         text=[f"{v:.1f}M" for v in inbound_data],
                         textposition='outside'))
    fig.add_trace(go.Bar(x=years, y=domestic_data, name='Domestic',
                         marker_color='#365C8D', opacity=.85,
                         text=[f"{v:.1f}M" for v in domestic_data],
                         textposition='outside'))
    apply_layout(fig)
    fig.update_layout(barmode='group', bargap=0.18)
    return fig

# ═══════════════════════════════════════════════════════
# FORECAST CHARTS
# ═══════════════════════════════════════════════════════
def create_forecast_chart(historical, forecast, dates, title,
                           lower=None, upper=None, template="plotly_dark"):
    fig = go.Figure()
    split = len(historical)
    # Confidence band
    if lower and upper:
        fig.add_trace(go.Scatter(
            x=dates[split-1:], y=[historical[-1]]+upper,
            line=dict(width=0), showlegend=False,
            hoverinfo='skip'))
        fig.add_trace(go.Scatter(
            x=dates[split-1:], y=[historical[-1]]+lower,
            fill='tonexty', fillcolor='rgba(23,177,155,0.12)',
            line=dict(width=0), name='Confidence Band'))
    # Historical
    fig.add_trace(go.Scatter(
        x=dates[:split], y=historical,
        name='Historical', line=dict(color='#17B19B', width=2.5),
        mode='lines+markers', marker=dict(size=6)))
    # Forecast
    fig.add_trace(go.Scatter(
        x=dates[split-1:], y=[historical[-1]]+list(forecast),
        name='Forecast', line=dict(color='#F4D044', width=2.5, dash='dash'),
        mode='lines+markers', marker=dict(size=6)))
    apply_layout(fig)
    return fig

# ═══════════════════════════════════════════════════════
# CARBON CHARTS
# ═══════════════════════════════════════════════════════
def create_carbon_chart(years, emissions, title, template="plotly_dark"):
    fig = go.Figure(go.Bar(
        x=years, y=emissions,
        marker_color=['#EF4444' if e > emissions[4] else '#17B19B' for e in emissions],
        text=[f"{e:.1f} Mt" for e in emissions],
        textposition='outside', textfont=dict(size=10)))
    apply_layout(fig)
    fig.update_yaxes(title_text="CO₂ (Megatons)")
    return fig

def create_sustainability_scenarios(years, scenarios, title, template="plotly_dark"):
    colors = ['#EF4444','#F4D044','#17B19B','#365C8D']
    fig = go.Figure()
    for i, (name, data) in enumerate(scenarios.items()):
        fig.add_trace(go.Scatter(
            x=years, y=data, name=name,
            line=dict(color=colors[i % len(colors)], width=2.5),
            mode='lines+markers', marker=dict(size=6)))
    apply_layout(fig)
    fig.update_yaxes(title_text="CO₂ (Megatons)")
    return fig

# ═══════════════════════════════════════════════════════
# SEGMENTATION CHARTS
# ═══════════════════════════════════════════════════════
def create_segment_chart(segments, values, title,
                         colors=None, template="plotly_dark"):
    if colors is None:
        colors = ['#F4D044','#17B19B','#365C8D']
    fig = go.Figure(go.Bar(
        x=segments, y=values, marker_color=colors,
        text=[f"{v:,.0f}" for v in values],
        textposition='outside', textfont=dict(size=11)))
    apply_layout(fig)
    return fig

# ═══════════════════════════════════════════════════════
# GAUGE CHART
# ═══════════════════════════════════════════════════════
def create_gauge_chart(value, title, max_value=100, template="plotly_dark"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value,
        title={'text': title, 'font': {'color': '#A1A6B7'}},
        domain={'x': [0,1], 'y': [0,1]},
        gauge={
            'axis': {'range': [None, max_value],
                     'tickcolor': '#A1A6B7'},
            'bar':  {'color': "#17B19B"},
            'bgcolor': "#1E2528",
            'steps': [
                {'range': [0,           max_value/3],   'color': "#EF444433"},
                {'range': [max_value/3, 2*max_value/3], 'color': "#F4D04433"},
                {'range': [2*max_value/3, max_value],   'color': "#17B19B33"},
            ],
            'threshold': {'line': {'color': "#F4F9F8", 'width': 3},
                          'thickness': 0.75, 'value': value}
        }))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="#A1A6B7"),
                      margin=dict(l=20,r=20,t=40,b=10))
    return fig

# ═══════════════════════════════════════════════════════
# HORIZONTAL BAR  (DataSaudi addition)
# ═══════════════════════════════════════════════════════
def create_horizontal_bar(labels, values, colors,
                          x_title="", vline=None, vline_label="",
                          vline_color="#17B19B", height=340):
    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker=dict(color=colors, line=dict(width=0), opacity=.88),
        text=[f"{v}" for v in values],
        textposition="outside", textfont=dict(size=11),
        hovertemplate="<b>%{y}</b>: %{x}<extra></extra>"))
    if vline is not None:
        fig.add_vline(x=vline, line_dash="dash", line_color=vline_color,
                      annotation_text=vline_label,
                      annotation_font=dict(color=vline_color, size=10))
    apply_layout(fig, height=height)
    if x_title:
        fig.update_xaxes(title_text=x_title)
    return fig
