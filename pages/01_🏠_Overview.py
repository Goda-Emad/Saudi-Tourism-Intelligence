import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ══════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════
st.set_page_config(
    page_title="Saudi Tourism Intelligence",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════
# LANGUAGE & THEME STATE
# ══════════════════════════════════════════
if "lang" not in st.session_state:
    st.session_state.lang = "EN"
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

lang = st.session_state.lang
theme = st.session_state.theme

# ══════════════════════════════════════════
# TRANSLATIONS
# ══════════════════════════════════════════
T = {
    "EN": {
        "title": "Saudi Tourism Intelligence",
        "subtitle": "AI-Powered Analytics Platform · Vision 2030",
        "overview": "Executive Overview",
        "built_by": "Built by",
        "data_source": "Data Source",
        "data_desc": "DataSaudi — Ministry of Economy & Planning",
        "coverage": "Coverage",
        "coverage_val": "2015 – 2024 · 11 Datasets · 3,210 Records",
        "total_tourists": "Total Tourists 2024",
        "inbound": "Inbound Tourists",
        "domestic": "Domestic Tourists",
        "overnight": "Overnight Stays",
        "avg_spending": "Avg Spending (Inbound)",
        "carbon": "Carbon Impact",
        "recovery": "Recovery 2021→2024",
        "peak_year": "Peak Year",
        "covid_drop": "COVID Drop 2020",
        "top_purpose": "Top Purpose 2024",
        "key_insights": "Key Insights",
        "insight_1": "Leisure overtook Religious as top purpose in 2024 — Vision 2030 working!",
        "insight_2": "Inbound tourists spend 4x more than Domestic per trip",
        "insight_3": "Inbound overnight stays grew +1,663% from 2021 to 2024",
        "insight_4": "10% carbon reduction = saving 324,619 trees equivalent",
        "tourists_trend": "Tourist Trend 2015–2024",
        "inbound_label": "Inbound",
        "domestic_label": "Domestic",
        "purposes": "2024 Tourist Purpose Breakdown",
        "forecast_preview": "Demand Forecast Preview 2025–2026",
        "peak_2025": "Peak 2025",
        "peak_2026": "Peak 2026",
        "pages": "Navigation",
        "page_overview": "🏠 Overview",
        "page_trends": "📈 Tourist Trends",
        "page_season": "📅 Seasonality",
        "page_spend": "💰 Spending",
        "page_overnight": "🏨 Overnight Stays",
        "page_forecast": "🔮 Forecasting",
        "page_segment": "🎯 Segmentation",
        "page_carbon": "🌱 Carbon Impact",
        "dark_mode": "🌙 Dark",
        "light_mode": "☀️ Light",
        "lang_toggle": "🌐 العربية",
        "methodology": "Methodology",
        "m1": "Prophet · Demand Forecasting",
        "m2": "K-Means · Tourist Segmentation",
        "m3": "Gradient Boosting · Spending Prediction (R²=0.986)",
    },
    "AR": {
        "title": "ذكاء السياحة السعودية",
        "subtitle": "منصة تحليلات مدعومة بالذكاء الاصطناعي · رؤية 2030",
        "overview": "نظرة تنفيذية عامة",
        "built_by": "من تطوير",
        "data_source": "مصدر البيانات",
        "data_desc": "داتا السعودية — وزارة الاقتصاد والتخطيط",
        "coverage": "التغطية",
        "coverage_val": "2015 – 2024 · 11 مجموعة بيانات · 3,210 سجل",
        "total_tourists": "إجمالي السياح 2024",
        "inbound": "السياح الوافدون",
        "domestic": "السياح المحليون",
        "overnight": "ليالي الإقامة",
        "avg_spending": "متوسط الإنفاق (وافد)",
        "carbon": "الأثر الكربوني",
        "recovery": "التعافي 2021←2024",
        "peak_year": "أفضل سنة",
        "covid_drop": "انخفاض كوفيد 2020",
        "top_purpose": "أبرز غرض 2024",
        "key_insights": "أبرز الاستنتاجات",
        "insight_1": "الترفيه تجاوز الديني كأول غرض سياحي في 2024 — رؤية 2030 تعمل!",
        "insight_2": "السائح الوافد ينفق 4 أضعاف السائح المحلي لكل رحلة",
        "insight_3": "ليالي إقامة الوافدين نمت +1,663% من 2021 إلى 2024",
        "insight_4": "تخفيض 10% كربون = توفير ما يعادل زراعة 324,619 شجرة",
        "tourists_trend": "اتجاه السياحة 2015–2024",
        "inbound_label": "وافد",
        "domestic_label": "محلي",
        "purposes": "توزيع أغراض السياحة 2024",
        "forecast_preview": "معاينة توقعات الطلب 2025–2026",
        "peak_2025": "ذروة 2025",
        "peak_2026": "ذروة 2026",
        "pages": "التنقل",
        "page_overview": "🏠 نظرة عامة",
        "page_trends": "📈 اتجاهات السياحة",
        "page_season": "📅 الموسمية",
        "page_spend": "💰 الإنفاق",
        "page_overnight": "🏨 ليالي الإقامة",
        "page_forecast": "🔮 التوقعات",
        "page_segment": "🎯 تقسيم السياح",
        "page_carbon": "🌱 الأثر الكربوني",
        "dark_mode": "🌙 داكن",
        "light_mode": "☀️ فاتح",
        "lang_toggle": "🌐 English",
        "methodology": "المنهجية",
        "m1": "Prophet · توقع الطلب",
        "m2": "K-Means · تقسيم السياح",
        "m3": "Gradient Boosting · توقع الإنفاق (R²=0.986)",
    }
}
t = T[lang]

# ══════════════════════════════════════════
# THEME COLORS
# ══════════════════════════════════════════
if theme == "dark":
    bg_main       = "#0D1B2A"
    bg_card       = "#1A2B3C"
    bg_card2      = "#162233"
    text_primary  = "#F0F4F8"
    text_secondary= "#8FA8C0"
    accent_teal   = "#00C9B1"
    accent_gold   = "#F0A500"
    accent_blue   = "#3A86FF"
    accent_green  = "#00E676"
    accent_red    = "#FF5252"
    border_color  = "#2A3F55"
    chart_bg      = "rgba(13,27,42,0)"
    plotly_template = "plotly_dark"
else:
    bg_main       = "#F4F7FB"
    bg_card       = "#FFFFFF"
    bg_card2      = "#EDF2F7"
    text_primary  = "#1A2B3C"
    text_secondary= "#4A6080"
    accent_teal   = "#009688"
    accent_gold   = "#E08C00"
    accent_blue   = "#1565C0"
    accent_green  = "#2E7D32"
    accent_red    = "#C62828"
    border_color  = "#CBD5E0"
    chart_bg      = "rgba(244,247,251,0)"
    plotly_template = "plotly_white"

dir_attr = 'rtl' if lang == "AR" else 'ltr'

# ══════════════════════════════════════════
# CSS
# ══════════════════════════════════════════
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=IBM+Plex+Mono:wght@400;600&family=Tajawal:wght@300;400;700;800&display=swap');

  html, body, [data-testid="stAppViewContainer"] {{
    background-color: {bg_main} !important;
    font-family: {'Tajawal' if lang=='AR' else 'Sora'}, sans-serif;
    direction: {dir_attr};
  }}
  [data-testid="stSidebar"] {{
    background: {bg_card} !important;
    border-right: 1px solid {border_color};
  }}
  [data-testid="stSidebar"] * {{ color: {text_primary} !important; }}

  .hero-banner {{
    background: linear-gradient(135deg, {bg_card} 0%, {bg_card2} 100%);
    border: 1px solid {border_color};
    border-left: 4px solid {accent_teal};
    border-radius: 16px;
    padding: 32px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
  }}
  .hero-banner::before {{
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, {accent_teal}22 0%, transparent 70%);
    border-radius: 50%;
  }}
  .hero-title {{
    font-size: 2.2rem;
    font-weight: 800;
    color: {text_primary};
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
  }}
  .hero-subtitle {{
    font-size: 1rem;
    color: {accent_teal};
    font-weight: 600;
    margin: 0 0 16px 0;
    letter-spacing: 1px;
    text-transform: uppercase;
  }}
  .hero-meta {{
    display: flex;
    gap: 24px;
    flex-wrap: wrap;
    margin-top: 12px;
  }}
  .meta-item {{
    display: flex;
    flex-direction: column;
  }}
  .meta-label {{
    font-size: 0.7rem;
    color: {text_secondary};
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
  }}
  .meta-value {{
    font-size: 0.85rem;
    color: {text_primary};
    font-weight: 600;
  }}
  .kpi-card {{
    background: {bg_card};
    border: 1px solid {border_color};
    border-radius: 14px;
    padding: 20px 18px;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
    height: 100%;
  }}
  .kpi-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 8px 24px {accent_teal}22;
  }}
  .kpi-icon {{ font-size: 1.6rem; margin-bottom: 6px; }}
  .kpi-value {{
    font-size: 1.6rem;
    font-weight: 800;
    color: {accent_teal};
    line-height: 1.1;
    font-family: 'IBM Plex Mono', monospace;
  }}
  .kpi-label {{
    font-size: 0.72rem;
    color: {text_secondary};
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 600;
    margin-top: 4px;
  }}
  .kpi-delta {{
    font-size: 0.78rem;
    font-weight: 700;
    margin-top: 6px;
    font-family: 'IBM Plex Mono', monospace;
  }}

  .insight-card {{
    background: {bg_card};
    border: 1px solid {border_color};
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 10px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
  }}
  .insight-icon {{
    font-size: 1.3rem;
    flex-shrink: 0;
    margin-top: 2px;
  }}
  .insight-text {{
    font-size: 0.88rem;
    color: {text_primary};
    line-height: 1.5;
    font-weight: 400;
  }}

  .section-title {{
    font-size: 1.1rem;
    font-weight: 700;
    color: {text_primary};
    margin: 28px 0 14px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid {accent_teal};
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .method-pill {{
    display: inline-block;
    background: {bg_card2};
    border: 1px solid {border_color};
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.78rem;
    color: {text_primary};
    font-weight: 600;
    margin: 4px;
  }}

  .footer-bar {{
    background: {bg_card};
    border: 1px solid {border_color};
    border-radius: 12px;
    padding: 16px 24px;
    margin-top: 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
  }}
  .footer-name {{
    font-size: 0.85rem;
    font-weight: 700;
    color: {accent_teal};
  }}
  .footer-link {{
    font-size: 0.78rem;
    color: {text_secondary};
  }}
  .footer-link a {{
    color: {accent_blue} !important;
    text-decoration: none;
    font-weight: 600;
  }}

  div[data-testid="stVerticalBlock"] > div {{ gap: 0 !important; }}
  .stPlotlyChart {{ border-radius: 12px; overflow: hidden; }}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════
with st.sidebar:
    st.image("assets/logo.png", use_column_width=True)
    st.markdown(f"<div style='text-align:center; font-size:0.7rem; color:{text_secondary}; margin-bottom:16px;'>{t['subtitle']}</div>", unsafe_allow_html=True)
    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button(t["dark_mode"] if theme == "light" else t["light_mode"], use_container_width=True):
            st.session_state.theme = "light" if theme == "dark" else "dark"
            st.rerun()
    with col_b:
        if st.button(t["lang_toggle"], use_container_width=True):
            st.session_state.lang = "AR" if lang == "EN" else "EN"
            st.rerun()

    st.divider()
    st.markdown(f"<div style='font-size:0.75rem; font-weight:700; color:{text_secondary}; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;'>{t['pages']}</div>", unsafe_allow_html=True)
    pages = ["page_overview","page_trends","page_season","page_spend",
             "page_overnight","page_forecast","page_segment","page_carbon"]
    for p in pages:
        st.markdown(f"<div style='padding:6px 10px; border-radius:8px; font-size:0.85rem; color:{text_primary}; margin-bottom:2px;'>{t[p]}</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown(f"""
    <div style='font-size:0.72rem; color:{text_secondary};'>
      <div style='font-weight:700; color:{accent_teal}; margin-bottom:4px;'>{t['built_by']}</div>
      <div style='color:{text_primary}; font-weight:600;'>Eng. Goda Emad</div>
      <a href='https://github.com/Goda-Emad/Saudi-Tourism-Intelligence/tree/main' target='_blank'
         style='color:{accent_blue}; font-size:0.7rem;'>🐙 GitHub</a> &nbsp;
      <a href='https://www.linkedin.com/in/goda-emad/' target='_blank'
         style='color:{accent_blue}; font-size:0.7rem;'>💼 LinkedIn</a>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════
# HERO BANNER
# ══════════════════════════════════════════
st.markdown(f"""
<div class='hero-banner'>
  <div class='hero-title'>🇸🇦 {t['title']}</div>
  <div class='hero-subtitle'>{t['subtitle']}</div>
  <div class='hero-meta'>
    <div class='meta-item'>
      <span class='meta-label'>{t['data_source']}</span>
      <span class='meta-value'>{t['data_desc']}</span>
    </div>
    <div class='meta-item'>
      <span class='meta-label'>{t['coverage']}</span>
      <span class='meta-value'>{t['coverage_val']}</span>
    </div>
    <div class='meta-item'>
      <span class='meta-label'>{t['built_by']}</span>
      <span class='meta-value'>Eng. Goda Emad</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# KPI CARDS — ROW 1
# ══════════════════════════════════════════
st.markdown(f"<div class='section-title'>📊 {t['overview']}</div>", unsafe_allow_html=True)

kpis_row1 = [
    ("🌍", t["total_tourists"],  "115.8M",  f"+8.1% YoY",   accent_teal),
    ("✈️", t["inbound"],         "29.7M",   "+8.4% YoY",    accent_blue),
    ("🏠", t["domestic"],        "86.2M",   "+5.2% YoY",    accent_gold),
    ("🌙", t["overnight"],       "1.1B",    "+19.1% YoY",   accent_green),
]

cols = st.columns(4)
for col, (icon, label, val, delta, color) in zip(cols, kpis_row1):
    with col:
        st.markdown(f"""
        <div class='kpi-card'>
          <div class='kpi-icon'>{icon}</div>
          <div class='kpi-value' style='color:{color};'>{val}</div>
          <div class='kpi-label'>{label}</div>
          <div class='kpi-delta' style='color:{accent_green};'>{delta}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='margin:10px 0;'></div>", unsafe_allow_html=True)

# KPI CARDS — ROW 2
kpis_row2 = [
    ("💰", t["avg_spending"],  "SAR 5,622", "+12.3% YoY",  accent_gold),
    ("🌱", t["carbon"],        "68.17 MT",  "+23.2% YoY",  accent_red),
    ("🚀", t["recovery"],      "×1.72",     "2021 → 2024", accent_teal),
    ("📅", t["peak_year"],     "2024",      "All-time high",accent_blue),
]

cols2 = st.columns(4)
for col, (icon, label, val, delta, color) in zip(cols2, kpis_row2):
    with col:
        st.markdown(f"""
        <div class='kpi-card'>
          <div class='kpi-icon'>{icon}</div>
          <div class='kpi-value' style='color:{color};'>{val}</div>
          <div class='kpi-label'>{label}</div>
          <div class='kpi-delta' style='color:{text_secondary};'>{delta}</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════
# CHARTS ROW
# ══════════════════════════════════════════
st.markdown(f"<div class='section-title'>📈 {t['tourists_trend']}</div>", unsafe_allow_html=True)

chart_col, pie_col = st.columns([3, 2])

# Trend Chart
with chart_col:
    years = list(range(2015, 2025))
    inbound_data =  [17.99, 18.04, 16.11, 15.33, 17.53, 4.14, 3.48, 16.64, 27.18, 29.73]
    domestic_data = [46.45, 45.04, 43.82, 43.26, 47.81, 42.11, 63.83, 77.84, 81.92, 86.16]

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=years, y=inbound_data, name=t["inbound_label"],
        line=dict(color=accent_blue, width=2.5),
        fill='tozeroy', fillcolor=f"{accent_blue}15",
        marker=dict(size=6)
    ))
    fig_trend.add_trace(go.Scatter(
        x=years, y=domestic_data, name=t["domestic_label"],
        line=dict(color=accent_teal, width=2.5),
        fill='tozeroy', fillcolor=f"{accent_teal}15",
        marker=dict(size=6)
    ))
    fig_trend.add_vrect(x0=2019.5, x1=2021.5,
        fillcolor=accent_red, opacity=0.08,
        annotation_text="COVID-19", annotation_position="top left",
        annotation=dict(font_color=accent_red, font_size=10))
    fig_trend.update_layout(
        template=plotly_template,
        paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=320, margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", y=-0.15, font=dict(size=11)),
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor=border_color,
                   tickfont=dict(size=10), title="Millions"),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})

# Purpose Pie
with pie_col:
    purposes = ["Leisure", "VFR", "Religious", "Business", "Other"]
    values   = [39.8, 36.0, 23.7, 10.9, 5.4]
    colors   = [accent_teal, accent_blue, accent_gold, accent_green, text_secondary]

    fig_pie = go.Figure(go.Pie(
        labels=purposes, values=values,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color=bg_main, width=2)),
        textfont=dict(size=11),
        hovertemplate="<b>%{label}</b><br>%{value}M tourists<extra></extra>"
    ))
    fig_pie.add_annotation(
        text="<b>115.8M</b><br>Total",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=12, color=text_primary)
    )
    fig_pie.update_layout(
        template=plotly_template,
        paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=320, margin=dict(l=10, r=10, t=20, b=10),
        showlegend=True,
        legend=dict(orientation="v", font=dict(size=10), x=1.0),
        font=dict(color=text_primary),
        title=dict(text=t["purposes"], font=dict(size=12), x=0.5)
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════
# INSIGHTS + FORECAST PREVIEW
# ══════════════════════════════════════════
ins_col, fore_col = st.columns([1, 1])

with ins_col:
    st.markdown(f"<div class='section-title'>💡 {t['key_insights']}</div>", unsafe_allow_html=True)
    insights = [
        ("🏖️", t["insight_1"], accent_teal),
        ("💰", t["insight_2"], accent_gold),
        ("🚀", t["insight_3"], accent_blue),
        ("🌱", t["insight_4"], accent_green),
    ]
    for icon, text, color in insights:
        st.markdown(f"""
        <div class='insight-card' style='border-left: 3px solid {color};'>
          <div class='insight-icon'>{icon}</div>
          <div class='insight-text'>{text}</div>
        </div>
        """, unsafe_allow_html=True)

with fore_col:
    st.markdown(f"<div class='section-title'>🔮 {t['forecast_preview']}</div>", unsafe_allow_html=True)

    months_2025 = [f"2025-{str(m).zfill(2)}" for m in range(1,13)]
    months_2026 = [f"2026-{str(m).zfill(2)}" for m in range(1,13)]
    forecast_2025 = [12307,10628,10812,10074,8964,11238,11832,11124,9846,9561,11710,10798]
    forecast_2026 = [13680,11797,11963,11180,9927,12458,13063,12290,10831,10550,12905,11897]

    all_months = months_2025 + months_2026
    all_forecast = forecast_2025 + forecast_2026

    fig_fore = go.Figure()
    fig_fore.add_trace(go.Scatter(
        x=months_2025, y=forecast_2025, name="2025",
        line=dict(color=accent_blue, width=2.5, dash='dot'),
        marker=dict(size=5)
    ))
    fig_fore.add_trace(go.Scatter(
        x=months_2026, y=forecast_2026, name="2026",
        line=dict(color=accent_teal, width=2.5),
        marker=dict(size=5)
    ))
    fig_fore.update_layout(
        template=plotly_template,
        paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=280, margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.18, font=dict(size=11)),
        xaxis=dict(showgrid=False, tickangle=45, tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor=border_color,
                   tickfont=dict(size=10), title="K Tourists"),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_fore, use_container_width=True, config={"displayModeBar": False})

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown(f"""
        <div class='kpi-card' style='padding:14px;'>
          <div class='kpi-icon'>📅</div>
          <div class='kpi-value' style='font-size:1.2rem; color:{accent_blue};'>12,307K</div>
          <div class='kpi-label'>{t['peak_2025']} · Jan</div>
        </div>""", unsafe_allow_html=True)
    with col_f2:
        st.markdown(f"""
        <div class='kpi-card' style='padding:14px;'>
          <div class='kpi-icon'>📅</div>
          <div class='kpi-value' style='font-size:1.2rem; color:{accent_teal};'>13,680K</div>
          <div class='kpi-label'>{t['peak_2026']} · Jan</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# METHODOLOGY
# ══════════════════════════════════════════
st.markdown(f"<div class='section-title'>🧠 {t['methodology']}</div>", unsafe_allow_html=True)
st.markdown(f"""
<div style='display:flex; flex-wrap:wrap; gap:8px; margin-bottom:8px;'>
  <span class='method-pill'>🔮 {t['m1']}</span>
  <span class='method-pill'>🎯 {t['m2']}</span>
  <span class='method-pill'>💰 {t['m3']}</span>
  <span class='method-pill'>📊 Plotly · Streamlit</span>
  <span class='method-pill'>🐍 Python · Pandas · Scikit-learn</span>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════
st.markdown(f"""
<div class='footer-bar'>
  <div>
    <div class='footer-name'>Eng. Goda Emad — Saudi Tourism Intelligence</div>
    <div class='footer-link'>Data: DataSaudi · Ministry of Economy & Planning · 2015–2024</div>
  </div>
  <div style='display:flex; gap:16px;'>
    <div class='footer-link'>
      <a href='https://github.com/Goda-Emad/Saudi-Tourism-Intelligence/tree/main' target='_blank'>🐙 GitHub</a>
    </div>
    <div class='footer-link'>
      <a href='https://www.linkedin.com/in/goda-emad/' target='_blank'>💼 LinkedIn</a>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
