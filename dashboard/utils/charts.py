# utils/charts.py
"""
Chart Creation Functions
دوال إنشاء الرسوم البيانية
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ═══════════════════════════════════════════════════════
# BASE CHARTS
# ═══════════════════════════════════════════════════════
def create_trend_chart(df, x_col, y_col, title, color=None, template="plotly_dark"):
    """إنشاء رسم بياني للاتجاهات"""
    fig = px.line(
        df, x=x_col, y=y_col,
        title=title,
        color=color,
        template=template
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", y=-0.2)
    )
    return fig

def create_bar_chart(df, x_col, y_col, title, color=None, barmode='group', template="plotly_dark"):
    """إنشاء رسم بياني أعمدة"""
    fig = px.bar(
        df, x=x_col, y=y_col,
        title=title,
        color=color,
        barmode=barmode,
        template=template
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", y=-0.2)
    )
    return fig

def create_line_chart(df, x_col, y_col, title, color=None, template="plotly_dark"):
    """إنشاء رسم بياني خطي"""
    fig = px.line(
        df, x=x_col, y=y_col,
        title=title,
        color=color,
        template=template
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", y=-0.2)
    )
    return fig

def create_area_chart(df, x_col, y_col, title, color=None, template="plotly_dark"):
    """إنشاء رسم بياني مساحي"""
    fig = px.area(
        df, x=x_col, y=y_col,
        title=title,
        color=color,
        template=template
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", y=-0.2)
    )
    return fig

def create_pie_chart(values, labels, title, colors=None, template="plotly_dark"):
    """إنشاء رسم بياني دائري"""
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors) if colors else None,
        textinfo='label+percent',
        textposition='auto'
    )])
    fig.update_layout(
        title=title,
        template=template,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    return fig

def create_heatmap(data, x_labels, y_labels, title, colorscale='Viridis', template="plotly_dark"):
    """إنشاء خريطة حرارية"""
    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=x_labels,
        y=y_labels,
        colorscale=colorscale,
        text=[[f"{val:.1f}" for val in row] for row in data],
        texttemplate="%{text}",
        textfont=dict(size=9),
        hovertemplate="<b>%{y}</b><br>%{x}: %{z:.1f}<extra></extra>"
    ))
    fig.update_layout(
        title=title,
        template=template,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    return fig

def create_radar_chart(categories, values, title, color=None, template="plotly_dark"):
    """إنشاء رسم بياني رادار"""
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        line=dict(color=color) if color else None,
        marker=dict(color=color) if color else None
    ))
    fig.update_layout(
        title=title,
        template=template,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(values)*1.1]
            )
        ),
        margin=dict(l=40, r=40, t=30, b=10)
    )
    return fig

# ═══════════════════════════════════════════════════════
# COMPARISON CHARTS
# ═══════════════════════════════════════════════════════
def create_comparison_chart(inbound_data, domestic_data, years, title, template="plotly_dark"):
    """مقارنة بين الوافدين والمحليين"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=years,
        y=inbound_data,
        name='Inbound',
        marker_color='#3A86FF',
        text=[f"{v:.1f}M" for v in inbound_data],
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        x=years,
        y=domestic_data,
        name='Domestic',
        marker_color='#00C9B1',
        text=[f"{v:.1f}M" for v in domestic_data],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=title,
        template=template,
        barmode='group',
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", y=-0.2),
        xaxis=dict(tickangle=-45)
    )
    return fig

# ═══════════════════════════════════════════════════════
# FORECAST CHARTS
# ═══════════════════════════════════════════════════════
def create_forecast_chart(historical, forecast, dates, title, template="plotly_dark"):
    """إنشاء رسم بياني للتوقعات"""
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=dates[:len(historical)],
        y=historical,
        name='Historical',
        line=dict(color='#3A86FF', width=3),
        mode='lines+markers',
        marker=dict(size=6)
    ))
    
    # Forecast data
    forecast_dates = dates[len(historical)-1:]
    forecast_values = [historical[-1]] + forecast
    
    fig.add_trace(go.Scatter(
        x=forecast_dates,
        y=forecast_values,
        name='Forecast',
        line=dict(color='#F0A500', width=3, dash='dash'),
        mode='lines+markers',
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title=title,
        template=template,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", y=-0.2),
        xaxis=dict(tickangle=-45)
    )
    return fig

# ═══════════════════════════════════════════════════════
# CARBON CHARTS
# ═══════════════════════════════════════════════════════
def create_carbon_chart(years, emissions, title, template="plotly_dark"):
    """إنشاء رسم بياني للكربون"""
    fig = go.Figure()
    
    colors = ['#FF5252' if i > 0 else '#00E676' for i in range(len(emissions))]
    
    fig.add_trace(go.Bar(
        x=years,
        y=emissions,
        marker_color=colors,
        text=[f"{e:.1f} Mt" for e in emissions],
        textposition='outside',
        textfont=dict(size=10)
    ))
    
    fig.update_layout(
        title=title,
        template=template,
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(title="CO₂ (Megatons)", gridcolor='rgba(128,128,128,0.2)'),
        xaxis=dict(tickangle=-45)
    )
    return fig

def create_sustainability_scenarios(years, scenarios, title, template="plotly_dark"):
    """إنشاء رسم بياني لسيناريوهات الاستدامة"""
    fig = go.Figure()
    
    colors = ['#FF5252', '#F0A500', '#00C9B1', '#3A86FF']
    
    for i, (name, data) in enumerate(scenarios.items()):
        fig.add_trace(go.Scatter(
            x=years,
            y=data,
            name=name,
            line=dict(color=colors[i % len(colors)], width=2.5),
            mode='lines+markers',
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title=title,
        template=template,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", y=-0.2),
        xaxis=dict(tickangle=-45),
        yaxis=dict(title="CO₂ (Megatons)")
    )
    return fig

# ═══════════════════════════════════════════════════════
# SEGMENTATION CHARTS
# ═══════════════════════════════════════════════════════
def create_segment_chart(segments, values, title, colors=None, template="plotly_dark"):
    """إنشاء رسم بياني للشرائح"""
    if colors is None:
        colors = ['#F0A500', '#3A86FF', '#00C9B1']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=segments,
        y=values,
        marker_color=colors,
        text=[f"{v:.0f}" for v in values],
        textposition='outside',
        textfont=dict(size=11)
    ))
    
    fig.update_layout(
        title=title,
        template=template,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(tickangle=-15),
        yaxis=dict(gridcolor='rgba(128,128,128,0.2)')
    )
    return fig

# ═══════════════════════════════════════════════════════
# GAUGE CHART
# ═══════════════════════════════════════════════════════
def create_gauge_chart(value, title, max_value=100, template="plotly_dark"):
    """إنشاء مقياس (Gauge)"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': "#00C9B1"},
            'steps': [
                {'range': [0, max_value/3], 'color': "#FF5252"},
                {'range': [max_value/3, 2*max_value/3], 'color': "#F0A500"},
                {'range': [2*max_value/3, max_value], 'color': "#00E676"}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(
        template=template,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    return fig
