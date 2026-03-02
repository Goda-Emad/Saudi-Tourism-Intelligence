import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ══════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════
st.set_page_config(
    page_title="Spending Analysis · Saudi Tourism Intelligence",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════
if "lang" not in st.session_state:
    st.session_state.lang = "EN"
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

lang  = st.session_state.lang
theme = st.session_state.theme

# ══════════════════════════════════════════
# TRANSLATIONS
# ══════════════════════════════════════════
T = {
    "EN": {
        "page_title":     "💰 Tourist Spending Analysis 2019–2024",
        "subtitle":       "Expenditure patterns · Inbound vs Domestic · Purpose-based breakdown",
        "built_by":       "Built by",
        "dark_mode":      "🌙 Dark",
        "light_mode":     "☀️ Light",
        "lang_toggle":    "🌐 العربية",
        "pages":          "Navigation",
        "page_overview":  "🏠 Overview",
        "page_trends":    "📈 Tourist Trends",
        "page_season":    "📅 Seasonality",
        "page_spend":     "💰 Spending",
        "page_overnight": "🏨 Overnight Stays",
        "page_forecast":  "🔮 Forecasting",
        "page_segment":   "🎯 Segmentation",
        "page_carbon":    "🌱 Carbon Impact",
        # KPIs
        "total_spend_2024":   "Total Spend 2024",
        "inbound_spend_2024": "Inbound Spend 2024",
        "domestic_spend_2024":"Domestic Spend 2024",
        "avg_trip_spend":     "Avg per Trip",
        "avg_night_spend":    "Avg per Night",
        "inbound_avg":        "Inbound Avg",
        "domestic_avg":       "Domestic Avg",
        # Sections
        "annual_spend":       "Annual Tourist Expenditure",
        "spend_by_purpose":   "Spending by Purpose of Visit",
        "spend_comparison":   "Inbound vs Domestic Spending",
        "monthly_spend":      "Monthly Spending Pattern (2024)",
        "top_spending":       "Top Spending Months",
        "spend_forecast":     "Spending Forecast 2025–2026",
        "purpose_breakdown":  "Purpose Breakdown by Spend",
        # Labels
        "total":              "Total",
        "inbound":            "Inbound",
        "domestic":           "Domestic",
        "religious":          "Religious",
        "leisure":            "Leisure",
        "business":           "Business",
        "vfr":                "VFR",
        "other":              "Other",
        "year":               "Year",
        "spend_bn":           "Spend (Billion SAR)",
        "spend_sar":          "Spend (SAR)",
        "filter_type":        "Tourist Type",
        "filter_year":        "Year Range",
        "all_types":          "All",
        "purpose":            "Purpose",
        "insight_title":      "💡 Key Spending Insights",
        "i1": "Inbound tourists spend 4.2× more than domestic tourists per trip",
        "i2": "Religious tourism drives 41% of total inbound spending (37.3B SAR)",
        "i3": "Peak spending month: August 2019 — 13,053 SAR per tourist",
        "i4": "Average inbound spend per night: 1,247 SAR vs domestic: 412 SAR",
        "i5": "Leisure spending grew 156% post-COVID, now 2nd largest category",
        "i6": "VFR (Visiting Friends/Relatives) accounts for 25.2% of total spend",
        # Data notes
        "data_source":      "Data Source: DataSaudi · Ministry of Tourism",
        "currency_note":    "All values in Saudi Riyal (SAR)",
    },
    "AR": {
        "page_title":     "💰 تحليل الإنفاق السياحي 2019–2024",
        "subtitle":       "أنماط الإنفاق · الوافدون مقابل المحليون · تحليل حسب الغرض",
        "built_by":       "من تطوير",
        "dark_mode":      "🌙 داكن",
        "light_mode":     "☀️ فاتح",
        "lang_toggle":    "🌐 English",
        "pages":          "التنقل",
        "page_overview":  "🏠 نظرة عامة",
        "page_trends":    "📈 اتجاهات السياحة",
        "page_season":    "📅 الموسمية",
        "page_spend":     "💰 الإنفاق",
        "page_overnight": "🏨 ليالي الإقامة",
        "page_forecast":  "🔮 التوقعات",
        "page_segment":   "🎯 تقسيم السياح",
        "page_carbon":    "🌱 الأثر الكربوني",
        # KPIs
        "total_spend_2024":   "إجمالي الإنفاق 2024",
        "inbound_spend_2024": "إنفاق الوافدين 2024",
        "domestic_spend_2024":"إنفاق المحليين 2024",
        "avg_trip_spend":     "متوسط لكل رحلة",
        "avg_night_spend":    "متوسط لكل ليلة",
        "inbound_avg":        "متوسط الوافد",
        "domestic_avg":       "متوسط المحلي",
        # Sections
        "annual_spend":       "الإنفاق السياحي السنوي",
        "spend_by_purpose":   "الإنفاق حسب غرض الزيارة",
        "spend_comparison":   "مقارنة الإنفاق (وافدون vs محليون)",
        "monthly_spend":      "نمط الإنفاق الشهري (2024)",
        "top_spending":       "أعلى شهور الإنفاق",
        "spend_forecast":     "توقعات الإنفاق 2025–2026",
        "purpose_breakdown":  "توزيع الإنفاق حسب الغرض",
        # Labels
        "total":              "الإجمالي",
        "inbound":            "وافد",
        "domestic":           "محلي",
        "religious":          "ديني",
        "leisure":            "ترفيه",
        "business":           "أعمال",
        "vfr":                "زيارة أهل",
        "other":              "أخرى",
        "year":               "السنة",
        "spend_bn":           "الإنفاق (مليار ريال)",
        "spend_sar":          "الإنفاق (ريال)",
        "filter_type":        "نوع السائح",
        "filter_year":        "نطاق السنوات",
        "all_types":          "الكل",
        "purpose":            "الغرض",
        "insight_title":      "💡 أبرز استنتاجات الإنفاق",
        "i1": "الوافدون ينفقون 4.2 أضعاف المحليين لكل رحلة",
        "i2": "السياحة الدينية تقود 41% من إنفاق الوافدين (37.3 مليار ريال)",
        "i3": "أعلى شهر إنفاق: أغسطس 2019 — 13,053 ريال لكل سائح",
        "i4": "متوسط إنفاق الوافد لكل ليلة: 1,247 ريال vs المحلي: 412 ريال",
        "i5": "إنفاق السياحة الترفيهية نما 156% بعد كوفيد، الآن ثاني أكبر فئة",
        "i6": "زيارة الأهل تمثل 25.2% من إجمالي الإنفاق",
        # Data notes
        "data_source":      "مصدر البيانات: DataSaudi · وزارة السياحة",
        "currency_note":    "جميع القيم بالريال السعودي",
    }
}
t = T[lang]

# ══════════════════════════════════════════
# THEME
# ══════════════════════════════════════════
if theme == "dark":
    bg_main        = "#0D1B2A"
    bg_card        = "#1A2B3C"
    bg_card2       = "#162233"
    text_primary   = "#F0F4F8"
    text_secondary = "#8FA8C0"
    accent_teal    = "#00C9B1"
    accent_gold    = "#F0A500"
    accent_blue    = "#3A86FF"
    accent_green   = "#00E676"
    accent_red     = "#FF5252"
    accent_purple  = "#BB86FC"
    border_color   = "#2A3F55"
    chart_bg       = "rgba(13,27,42,0)"
    plotly_template= "plotly_dark"
else:
    bg_main        = "#F4F7FB"
    bg_card        = "#FFFFFF"
    bg_card2       = "#EDF2F7"
    text_primary   = "#1A2B3C"
    text_secondary = "#4A6080"
    accent_teal    = "#009688"
    accent_gold    = "#E08C00"
    accent_blue    = "#1565C0"
    accent_green   = "#2E7D32"
    accent_red     = "#C62828"
    accent_purple  = "#6A1B9A"
    border_color   = "#CBD5E0"
    chart_bg       = "rgba(244,247,251,0)"
    plotly_template= "plotly_white"

dir_attr = 'rtl' if lang == "AR" else 'ltr'

# ══════════════════════════════════════════
# DATA
# ══════════════════════════════════════════
# Spending data based on DataSaudi and business_case.pdf
years = [2019, 2020, 2021, 2022, 2023, 2024]

# Total spending in billions SAR
inbound_spend_bn = [76.4, 12.8, 14.7, 90.9, 106.2, 119.8]  # 2024 est from growth
domestic_spend_bn = [42.3, 37.6, 48.2, 59.7, 68.4, 76.5]   # 2024 est
total_spend_bn = [a+b for a,b in zip(inbound_spend_bn, domestic_spend_bn)]

# Spending by purpose (2024) - based on DataSaudi percentages
purpose_spend_2024 = {
    "Religious": 37.3,    # 41% of inbound
    "Leisure": 22.9,      # 25.2% of inbound
    "VFR": 15.6,          # ~17%
    "Business": 8.2,      # ~9%
    "Other": 4.8,         # ~5%
}

# Average spend per trip (SAR)
inbound_avg_trip = [7820, 3540, 3980, 8210, 8920, 9450]
domestic_avg_trip = [1850, 1620, 1890, 2050, 2150, 2250]

# Average spend per night (SAR)
inbound_avg_night = [980, 420, 470, 1020, 1150, 1247]
domestic_avg_night = [340, 310, 350, 380, 395, 412]

# Monthly spending pattern (2024 - index relative to annual avg)
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
monthly_spend_index = [0.92, 0.88, 1.12, 0.98, 0.95, 1.02, 1.18, 1.24, 0.94, 0.89, 0.97, 1.06]

# Top spending months data (from business_case.pdf)
top_months = ["Aug 2019", "Dec 2023", "Mar 2024", "Jul 2024", "Jan 2024"]
top_values = [13053, 11800, 10900, 10200, 9800]

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

  .page-header {{
    background: linear-gradient(135deg, {bg_card} 0%, {bg_card2} 100%);
    border: 1px solid {border_color};
    border-left: 4px solid {accent_gold};
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
  }}
  .page-header::after {{
    content: '💰';
    position: absolute;
    right: 24px; top: 50%;
    transform: translateY(-50%);
    font-size: 4rem;
    opacity: 0.08;
  }}
  .page-title {{
    font-size: 1.9rem;
    font-weight: 800;
    color: {text_primary};
    margin: 0 0 4px 0;
  }}
  .page-subtitle {{
    font-size: 0.88rem;
    color: {accent_gold};
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
  }}

  .kpi-card {{
    background: {bg_card};
    border: 1px solid {border_color};
    border-radius: 14px;
    padding: 18px 14px;
    text-align: center;
    height: 100%;
    transition: transform 0.2s;
  }}
  .kpi-card:hover {{ transform: translateY(-2px); }}
  .kpi-icon  {{ font-size: 1.5rem; margin-bottom: 6px; }}
  .kpi-value {{
    font-size: 1.5rem;
    font-weight: 800;
    line-height: 1.1;
    font-family: 'IBM Plex Mono', monospace;
  }}
  .kpi-label {{
    font-size: 0.68rem;
    color: {text_secondary};
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 600;
    margin-top: 4px;
  }}
  .kpi-delta {{
    font-size: 0.75rem;
    font-weight: 700;
    margin-top: 4px;
    font-family: 'IBM Plex Mono', monospace;
  }}

  .section-title {{
    font-size: 1.05rem;
    font-weight: 700;
    color: {text_primary};
    margin: 24px 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid {accent_gold};
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .chart-card {{
    background: {bg_card};
    border: 1px solid {border_color};
    border-radius: 14px;
    padding: 16px;
  }}

  .insight-row {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 20px;
  }}
  .insight-card {{
    background: {bg_card};
    border: 1px solid {border_color};
    border-radius: 12px;
    padding: 14px 16px;
    display: flex;
    align-items: flex-start;
    gap: 10px;
  }}
  .insight-icon {{ font-size: 1.2rem; flex-shrink: 0; margin-top: 2px; }}
  .insight-text {{
    font-size: 0.83rem;
    color: {text_primary};
    line-height: 1.5;
  }}

  .comparison-box {{
    background: {bg_card2};
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
    border: 1px solid {border_color};
  }}
  .comp-item {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid {border_color}40;
  }}
  .comp-item:last-child {{ border-bottom: none; }}
  .comp-label {{ font-size: 0.8rem; color: {text_secondary}; }}
  .comp-value {{
    font-size: 1.1rem;
    font-weight: 700;
    font-family: 'IBM Plex Mono', monospace;
  }}

  .footer-bar {{
    background: {bg_card};
    border: 1px solid {border_color};
    border-radius: 12px;
    padding: 14px 20px;
    margin-top: 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
  }}
  .footer-name  {{ font-size: 0.82rem; font-weight: 700; color: {accent_teal}; }}
  .footer-link  {{ font-size: 0.75rem; color: {text_secondary}; }}
  .footer-link a {{ color: {accent_blue} !important; text-decoration: none; font-weight: 600; }}
  
  .currency-note {{
    font-size: 0.7rem;
    color: {text_secondary};
    text-align: right;
    margin-top: 4px;
    font-style: italic;
  }}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════
with st.sidebar:
    try:
        st.image("assets/logo.png", use_column_width=True)
    except:
        st.markdown(f"<div style='text-align:center;font-size:1.5rem;'>🇸🇦</div>", unsafe_allow_html=True)

    st.markdown(f"<div style='text-align:center;font-size:0.68rem;color:{text_secondary};margin-bottom:12px;'>Saudi Tourism Intelligence</div>", unsafe_allow_html=True)
    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button(t["light_mode"] if theme=="dark" else t["dark_mode"], use_container_width=True):
            st.session_state.theme = "light" if theme=="dark" else "dark"
            st.rerun()
    with col_b:
        if st.button(t["lang_toggle"], use_container_width=True):
            st.session_state.lang = "AR" if lang=="EN" else "EN"
            st.rerun()

    st.divider()
    st.markdown(f"<div style='font-size:0.72rem;font-weight:700;color:{text_secondary};text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>{t['pages']}</div>", unsafe_allow_html=True)
    
    # Navigation buttons (simulated)
    pages_list = [
        ("page_overview", "🏠"), ("page_trends", "📈"), ("page_season", "📅"),
        ("page_spend", "💰"), ("page_overnight", "🏨"), ("page_forecast", "🔮"),
        ("page_segment", "🎯"), ("page_carbon", "🌱")
    ]
    for page_key, icon in pages_list:
        active = page_key == "page_spend"
        bg = f"{accent_gold}22" if active else "transparent"
        fw = "700" if active else "400"
        bc = accent_gold if active else "transparent"
        st.markdown(f"<div style='padding:7px 10px;border-radius:8px;background:{bg};border-left:3px solid {bc};font-size:0.83rem;font-weight:{fw};color:{text_primary};margin-bottom:3px;'>{icon} {t[page_key]}</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown(f"""
    <div style='font-size:0.7rem;color:{text_secondary};'>
      <div style='font-weight:700;color:{accent_teal};margin-bottom:4px;'>{t['built_by']}</div>
      <div style='color:{text_primary};font-weight:600;margin-bottom:4px;'>Eng. Goda Emad</div>
      <a href='https://github.com/Goda-Emad/Saudi-Tourism-Intelligence/tree/main' target='_blank' style='color:{accent_blue};'>🐙 GitHub</a> &nbsp;
      <a href='https://www.linkedin.com/in/goda-emad/' target='_blank' style='color:{accent_blue};'>💼 LinkedIn</a>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════
# FILTERS
# ══════════════════════════════════════════
    st.divider()
    year_range = st.slider(t["filter_year"], 2019, 2024, (2019, 2024))
    tourist_type = st.selectbox(t["filter_type"],
        [t["all_types"], t["inbound"], t["domestic"]])

# ══════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════
st.markdown(f"""
<div class='page-header'>
  <div class='page-title'>{t['page_title']}</div>
  <div class='page-subtitle'>{t['subtitle']}</div>
</div>
""", unsafe_allow_html=True)

# Filter years
y_start, y_end = year_range
idx_s = years.index(y_start)
idx_e = years.index(y_end) + 1
f_years = years[idx_s:idx_e]
f_inbound_spend = inbound_spend_bn[idx_s:idx_e]
f_domestic_spend = domestic_spend_bn[idx_s:idx_e]
f_total_spend = total_spend_bn[idx_s:idx_e]
f_inbound_avg = inbound_avg_trip[idx_s:idx_e]
f_domestic_avg = domestic_avg_trip[idx_s:idx_e]

# ══════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════
k1, k2, k3, k4, k5 = st.columns(5)

# Calculate metrics
total_spend_2024 = total_spend_bn[-1]
inbound_spend_2024 = inbound_spend_bn[-1]
domestic_spend_2024 = domestic_spend_bn[-1]
inbound_avg_2024 = inbound_avg_trip[-1]
domestic_avg_2024 = domestic_avg_trip[-1]

with k1:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-icon'>💰</div>
      <div class='kpi-value' style='color:{accent_teal};'>{total_spend_2024:.1f}B</div>
      <div class='kpi-label'>{t['total_spend_2024']}</div>
      <div class='kpi-delta' style='color:{accent_green};'>+12.8% YoY</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-icon'>✈️</div>
      <div class='kpi-value' style='color:{accent_blue};'>{inbound_spend_2024:.1f}B</div>
      <div class='kpi-label'>{t['inbound_spend_2024']}</div>
      <div class='kpi-delta' style='color:{accent_green};'>+12.9% YoY</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-icon'>🏠</div>
      <div class='kpi-value' style='color:{accent_gold};'>{domestic_spend_2024:.1f}B</div>
      <div class='kpi-label'>{t['domestic_spend_2024']}</div>
      <div class='kpi-delta' style='color:{accent_green};'>+11.8% YoY</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-icon'>🎫</div>
      <div class='kpi-value' style='color:{accent_purple};'>{inbound_avg_2024:,.0f}</div>
      <div class='kpi-label'>{t['inbound_avg']}</div>
      <div class='kpi-delta' style='color:{accent_teal};'>4.2× domestic</div>
    </div>""", unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-icon'>🏨</div>
      <div class='kpi-value' style='color:{accent_green};'>{domestic_avg_2024:,.0f}</div>
      <div class='kpi-label'>{t['domestic_avg']}</div>
      <div class='kpi-delta' style='color:{text_secondary};'>per trip</div>
    </div>""", unsafe_allow_html=True)

st.markdown(f"<div class='currency-note'>{t['currency_note']}</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# CHART 1: Annual Spending Trend
# ══════════════════════════════════════════
st.markdown(f"<div class='section-title'>📊 {t['annual_spend']}</div>", unsafe_allow_html=True)

fig_annual = go.Figure()

if tourist_type in [t["all_types"], t["inbound"]]:
    fig_annual.add_trace(go.Bar(
        x=f_years, y=f_inbound_spend, name=t["inbound"],
        marker_color=accent_blue,
        marker_line_color=accent_blue,
        opacity=0.85,
        text=[f"{v:.1f}B" for v in f_inbound_spend],
        textposition='outside',
        textfont=dict(size=10, color=text_primary)
    ))
if tourist_type in [t["all_types"], t["domestic"]]:
    fig_annual.add_trace(go.Bar(
        x=f_years, y=f_domestic_spend, name=t["domestic"],
        marker_color=accent_teal,
        opacity=0.85,
        text=[f"{v:.1f}B" for v in f_domestic_spend],
        textposition='outside',
        textfont=dict(size=10, color=text_primary)
    ))
if tourist_type == t["all_types"]:
    fig_annual.add_trace(go.Scatter(
        x=f_years, y=f_total_spend, name=t["total"],
        line=dict(color=accent_gold, width=2.5, dash='dot'),
        marker=dict(size=8, color=accent_gold),
        yaxis='y2',
        text=[f"{v:.1f}B" for v in f_total_spend],
        textposition='top center',
        textfont=dict(size=10, color=accent_gold)
    ))

# Add COVID annotation
if 2020 in f_years:
    fig_annual.add_vrect(x0=2019.5, x1=2020.5,
        fillcolor=accent_red, opacity=0.07,
        annotation_text="COVID-19",
        annotation=dict(font_color=accent_red, font_size=11))

fig_annual.update_layout(
    template=plotly_template,
    paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
    height=400, barmode='group',
    margin=dict(l=10, r=10, t=20, b=10),
    legend=dict(orientation="h", y=-0.12, font=dict(size=11)),
    xaxis=dict(showgrid=False, tickfont=dict(size=11)),
    yaxis=dict(title=t["spend_bn"], showgrid=True, gridcolor=border_color,
               tickfont=dict(size=10)),
    yaxis2=dict(overlaying='y', side='right', showgrid=False,
                title=f"{t['total']} (B SAR)", tickfont=dict(size=10)),
    font=dict(color=text_primary),
    bargap=0.25
)
st.plotly_chart(fig_annual, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════
# CHART 2+3: Purpose Breakdown & Avg Comparison
# ══════════════════════════════════════════
col_l, col_r = st.columns([3, 2])

with col_l:
    st.markdown(f"<div class='section-title'>🎯 {t['spend_by_purpose']} (2024)</div>", unsafe_allow_html=True)
    
    purposes = list(purpose_spend_2024.keys())
    values = list(purpose_spend_2024.values())
    colors = [accent_gold, accent_teal, accent_purple, accent_blue, text_secondary]
    
    fig_pie = go.Figure(go.Pie(
        labels=[t[p.lower()] for p in purposes],
        values=values,
        hole=0.4,
        marker=dict(colors=colors, line=dict(color=bg_card, width=2)),
        textinfo='label+percent',
        textposition='auto',
        textfont=dict(size=11, color=text_primary),
        hovertemplate="<b>%{label}</b><br>%{value:.1f}B SAR (%{percent})<extra></extra>"
    ))
    fig_pie.update_layout(
        template=plotly_template,
        paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.2, font=dict(size=10)),
        font=dict(color=text_primary),
        annotations=[dict(
            text=f"Total<br>{sum(values):.1f}B",
            x=0.5, y=0.5,
            font=dict(size=14, color=text_primary, weight='bold'),
            showarrow=False
        )]
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

with col_r:
    st.markdown(f"<div class='section-title'>⚖️ {t['spend_comparison']}</div>", unsafe_allow_html=True)
    
    # Average comparison boxes
    st.markdown(f"""
    <div class='comparison-box'>
      <div class='comp-item'>
        <span class='comp-label'>✈️ {t['inbound']} - {t['avg_trip_spend']}</span>
        <span class='comp-value' style='color:{accent_blue};'>{inbound_avg_2024:,.0f} SAR</span>
      </div>
      <div class='comp-item'>
        <span class='comp-label'>🏠 {t['domestic']} - {t['avg_trip_spend']}</span>
        <span class='comp-value' style='color:{accent_teal};'>{domestic_avg_2024:,.0f} SAR</span>
      </div>
      <div class='comp-item' style='border-bottom: 2px solid {border_color}; margin-bottom: 8px; padding-bottom: 12px;'>
        <span class='comp-label'>📊 {t['total']} {t['avg_trip_spend']}</span>
        <span class='comp-value' style='color:{accent_gold};'>{(inbound_avg_2024*0.3 + domestic_avg_2024*0.7):,.0f} SAR</span>
      </div>
      <div class='comp-item'>
        <span class='comp-label'>✈️ {t['inbound']} - {t['avg_night_spend']}</span>
        <span class='comp-value' style='color:{accent_blue};'>{inbound_avg_night[-1]:,.0f} SAR</span>
      </div>
      <div class='comp-item'>
        <span class='comp-label'>🏠 {t['domestic']} - {t['avg_night_spend']}</span>
        <span class='comp-value' style='color:{accent_teal};'>{domestic_avg_night[-1]:,.0f} SAR</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Ratio indicator
    ratio = inbound_avg_2024 / domestic_avg_2024
    st.markdown(f"""
    <div style='background:{bg_card2}; border-radius:8px;
