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

def create_pie_chart(values, labels, title, colors=None, template="plotly_dark"):
    """إنشاء رسم بياني دائري"""
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors) if colors else None
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
        textfont=dict(size=9)
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
        line=dict(color=color) if color else None
    ))
    fig.update_layout(
        title=title,
        template=template,
        polar=dict(radialaxis=dict(visible=True, range=[0, max(values)*1.1])),
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
        marker_color='#3A86FF'
    ))
    
    fig.add_trace(go.Bar(
        x=years,
        y=domestic_data,
        name='Domestic',
        marker_color='#00C9B1'
    ))
    
    fig.update_layout(
        title=title,
        template=template,
        barmode='group',
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", y=-0.2)
    )
    return fig

def create_stacked_chart(df, x_col, y_cols, title, template="plotly_dark"):
    """إنشاء رسم بياني مكدس"""
    fig = go.Figure()
    
    for col in y_cols:
        fig.add_trace(go.Bar(
            x=df[x_col],
            y=df[col],
            name=col
        ))
    
    fig.update_layout(
        title=title,
        template=template,
        barmode='stack',
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", y=-0.2)
    )
    return fig

# ═══════════════════════════════════════════════════════
# FORECAST CHARTS
# ═══════════════════════════════════════════════════════
def create_forecast_chart(historical, forecast, dates, title, template="plotly_dark"):
    """إنشاء رسم بياني للتوقعات"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates[:len(historical)],
        y=historical,
        name='Historical',
        line=dict(color='#3A86FF', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=dates[len(historical)-1:],
        y=[historical[-1]] + forecast,
        name='Forecast',
        line=dict(color='#F0A500', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=title,
        template=template,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", y=-0.2)
    )
    return fig

# ═══════════════════════════════════════════════════════
# CARBON CHARTS
# ═══════════════════════════════════════════════════════
def create_carbon_chart(years, emissions, title, template="plotly_dark"):
    """إنشاء رسم بياني للكربون"""
    fig = go.Figure()
    
    colors = ['#FF5252' if e > 0 else '#00E676' for e in emissions]
    
    fig.add_trace(go.Bar(
        x=years,
        y=emissions,
        marker_color=colors,
        text=[f"{e:.1f} Mt" for e in emissions],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=title,
        template=template,
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(title="CO₂ (Megatons)")
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
            line=dict(color=colors[i % len(colors)], width=2.5)
        ))
    
    fig.update_layout(
        title=title,
        template=template,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", y=-0.2)
    )
    return fig

# ═══════════════════════════════════════════════════════
# SEGMENTATION CHARTS
# ═══════════════════════════════════════════════════════
def create_segment_chart(segments, values, title, colors=None, template="plotly_dark"):
    """إنشاء رسم بياني للشرائح"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=segments,
        y=values,
        marker_color=colors if colors else ['#F0A500', '#3A86FF', '#00C9B1'],
        text=[f"{v:.0f}" for v in values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=title,
        template=template,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(tickangle=-15)
    )
    return fig

# ═══════════════════════════════════════════════════════
# SPECIALIZED CHARTS
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
    # ═══════════════════════════════════════════════════════
# NEW DATA LOADERS for additional files
# ═══════════════════════════════════════════════════════

@st.cache_data
def load_forecast_data():
    """تحميل بيانات التوقعات 2025-2026"""
    base_path = Path(__file__).parent.parent.parent / "data" / "clean"
    file_path = base_path / "06_Demand_Forecast_2025_2026.csv"
    
    df = load_csv_file(file_path)
    
    # إذا الملف مش موجود، نرجع بيانات افتراضية
    if df.empty:
        df = create_sample_forecast_data()
    
    return df

@st.cache_data
def load_segments_data():
    """تحميل بيانات تجزئة السياح"""
    base_path = Path(__file__).parent.parent.parent / "data" / "clean"
    file_path = base_path / "07_Tourist_Segments.csv"
    
    df = load_csv_file(file_path)
    
    if df.empty:
        df = create_sample_segments_data()
    
    return df

# ═══════════════════════════════════════════════════════
# SAMPLE DATA CREATORS for new files
# ═══════════════════════════════════════════════════════

def create_sample_forecast_data():
    """إنشاء بيانات توقعات تجريبية (من business_case.pdf)"""
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # 2025 forecast (thousands)
    forecast_2025 = [12307, 11850, 12100, 11500, 11200, 11800,
                     12200, 12100, 11600, 11400, 11800, 12500]
    
    # 2026 forecast (thousands)
    forecast_2026 = [13680, 13100, 13350, 12700, 12350, 13000,
                     13450, 13350, 12800, 12550, 13000, 13800]
    
    # Confidence intervals
    lower_2025 = [int(f * 0.92) for f in forecast_2025]
    upper_2025 = [int(f * 1.08) for f in forecast_2025]
    lower_2026 = [int(f * 0.92) for f in forecast_2026]
    upper_2026 = [int(f * 1.08) for f in forecast_2026]
    
    # Create dataframe
    data = []
    for i, month in enumerate(months):
        # 2025
        data.append({
            'Month': month,
            'Year': 2025,
            'Forecast_Total': forecast_2025[i],
            'Lower_Bound': lower_2025[i],
            'Upper_Bound': upper_2025[i],
            'Inbound_Pct': 28,
            'Domestic_Pct': 72
        })
        # 2026
        data.append({
            'Month': month,
            'Year': 2026,
            'Forecast_Total': forecast_2026[i],
            'Lower_Bound': lower_2026[i],
            'Upper_Bound': upper_2026[i],
            'Inbound_Pct': 30,
            'Domestic_Pct': 70
        })
    
    return pd.DataFrame(data)

def create_sample_segments_data():
    """إنشاء بيانات تجزئة السياح تجريبية"""
    
    segments = [
        {
            'Segment': 'High Value',
            'Percentage': 18,
            'Avg_Spend': 12500,
            'Avg_Stay': 12.5,
            'Frequency': 1.8,
            'Inbound_Pct': 65,
            'Domestic_Pct': 35,
            'Religious_Pct': 45,
            'Leisure_Pct': 28,
            'Business_Pct': 15,
            'VFR_Pct': 8,
            'Other_Pct': 4,
            'Winter_Pct': 38,
            'Spring_Pct': 22,
            'Summer_Pct': 18,
            'Fall_Pct': 22
        },
        {
            'Segment': 'Mid Value',
            'Percentage': 37,
            'Avg_Spend': 6200,
            'Avg_Stay': 6.8,
            'Frequency': 2.5,
            'Inbound_Pct': 45,
            'Domestic_Pct': 55,
            'Religious_Pct': 38,
            'Leisure_Pct': 32,
            'Business_Pct': 12,
            'VFR_Pct': 12,
            'Other_Pct': 6,
            'Winter_Pct': 28,
            'Spring_Pct': 24,
            'Summer_Pct': 26,
            'Fall_Pct': 22
        },
        {
            'Segment': 'Budget',
            'Percentage': 45,
            'Avg_Spend': 2800,
            'Avg_Stay': 3.2,
            'Frequency': 4.2,
            'Inbound_Pct': 22,
            'Domestic_Pct': 78,
            'Religious_Pct': 22,
            'Leisure_Pct': 35,
            'Business_Pct': 8,
            'VFR_Pct': 25,
            'Other_Pct': 10,
            'Winter_Pct': 20,
            'Spring_Pct': 22,
            'Summer_Pct': 40,
            'Fall_Pct': 18
        }
    ]
    
    return pd.DataFrame(segments)

# ═══════════════════════════════════════════════════════
# UPDATE BULK LOADER
# ═══════════════════════════════════════════════════════

@st.cache_data
def load_all_datasets():
    """تحميل جميع مجموعات البيانات (محدث)"""
    return {
        'tourist': load_tourist_data(),
        'spending': load_spending_data(),
        'overnight': load_overnight_data(),
        'carbon': load_carbon_data(),
        'forecast': load_forecast_data(),      # ✅ جديد
        'segments': load_segments_data()       # ✅ جديد
    }
