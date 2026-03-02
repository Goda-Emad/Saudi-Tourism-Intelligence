import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ══════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════
st.set_page_config(
    page_title="Overnight Stays · Saudi Tourism Intelligence",
    page_icon="🏨",
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
        "page_title":     "🏨 Overnight Stays Analysis 2015–2024",
        "subtitle":       "Length of stay · Total nights · Inbound vs Domestic patterns",
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
        "total_nights_2024":   "Total Nights 2024",
        "inbound_nights_2024": "Inbound Nights",
        "domestic_nights_2024":"Domestic Nights",
        "avg_stay_inbound":    "Avg Stay - Inbound",
        "avg_stay_domestic":   "Avg Stay - Domestic",
        "total_nights":        "Total Nights",
        # Sections
        "annual_evolution":    "Annual Evolution of Overnight Stays",
        "avg_length":          "Average Length of Stay",
        "monthly_pattern":     "Monthly Stay Pattern (2024)",
        "inbound_vs_domestic": "Inbound vs Domestic Comparison",
        "stay_distribution":   "Stay Duration Distribution",
        "purpose_stay":        "Stay Length by Purpose",
        "seasonal_impact":     "Seasonal Impact on Stay",
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
        "nights_m":           "Nights (Millions)",
        "nights_b":           "Nights (Billions)",
        "days":               "Days",
        "filter_type":        "Tourist Type",
        "filter_year":        "Year Range",
        "all_types":          "All",
        "month":              "Month",
        "insight_title":      "💡 Key Overnight Insights",
        "i1": "Inbound tourists stayed 560M nights in 2024 (+29.6% YoY)",
        "i2": "Domestic tourists stayed 539M nights in 2024 (+8.7% YoY)",
        "i3": "Inbound avg stay: 15.5 nights (Dec 2024) — 2.7× longer than domestic",
        "i4": "Domestic avg stay: 5.8 nights (Dec 2024) — stable pattern",
        "i5": "Winter months see longest stays (Dec–Feb for inbound)",
        "i6": "Summer peaks for domestic stays (June–Aug)",
        "i7": "1.1 Billion total overnight stays in 2024 — new record",
        "i8": "Religious tourists stay 2.3× longer than leisure visitors",
        # Data notes
        "data_source":      "Data Source: DataSaudi · Ministry of Tourism",
        "note":             "Based on official DataSaudi statistics",
        # Additional
        "pre_covid":        "Pre-COVID (2019)",
        "post_covid":       "Post-COVID (2024)",
        "growth":           "Growth",
        "share":            "Share",
    },
    "AR": {
        "page_title":     "🏨 تحليل ليالي الإقامة 2015–2024",
        "subtitle":       "مدة الإقامة · إجمالي الليالي · أنماط الوافدين والمحليين",
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
        "total_nights_2024":   "إجمالي الليالي 2024",
        "inbound_nights_2024": "ليالي الوافدين",
        "domestic_nights_2024":"ليالي المحليين",
        "avg_stay_inbound":    "متوسط الإقامة - وافدين",
        "avg_stay_domestic":   "متوسط الإقامة - محليين",
        "total_nights":        "إجمالي الليالي",
        # Sections
        "annual_evolution":    "التطور السنوي لليالي الإقامة",
        "avg_length":          "متوسط مدة الإقامة",
        "monthly_pattern":     "نمط الإقامة الشهري (2024)",
        "inbound_vs_domestic": "مقارنة الوافدين والمحليين",
        "stay_distribution":   "توزيع مدة الإقامة",
        "purpose_stay":        "مدة الإقامة حسب الغرض",
        "seasonal_impact":     "التأثير الموسمي على الإقامة",
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
        "nights_m":           "الليالي (مليون)",
        "nights_b":           "الليالي (مليار)",
        "days":               "أيام",
        "filter_type":        "نوع السائح",
        "filter_year":        "نطاق السنوات",
        "all_types":          "الكل",
        "month":              "الشهر",
        "insight_title":      "💡 أبرز استنتاجات الإقامة",
        "i1": "الوافدون سجلوا 560 مليون ليلة في 2024 (+29.6% عن 2023)",
        "i2": "المحليون سجلوا 539 مليون ليلة في 2024 (+8.7% عن 2023)",
        "i3": "متوسط إقامة الوافد: 15.5 ليلة (ديسمبر 2024) — 2.7× أطول من المحلي",
        "i4": "متوسط إقامة المحلي: 5.8 ليلة (ديسمبر 2024) — نمط مستقر",
        "i5": "أشهر الشتاء تسجل أطول إقامات (ديسمبر–فبراير للوافدين)",
        "i6": "ذروة المحليين صيفاً (يونيو–أغسطس)",
        "i7": "1.1 مليار ليلة إقامة في 2024 — رقم قياسي جديد",
        "i8": "السياح الدينيون يقيمون 2.3× أطول من سياح الترفيه",
        # Data notes
        "data_source":      "مصدر البيانات: DataSaudi · وزارة السياحة",
        "note":             "بناءً على إحصاءات DataSaudi الرسمية",
        # Additional
        "pre_covid":        "ما قبل كوفيد (2019)",
        "post_covid":       "ما بعد كوفيد (2024)",
        "growth":           "النمو",
        "share":            "الحصة",
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
    accent_pink    = "#FF79C6"
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
    accent_pink    = "#C2185B"
    border_color   = "#CBD5E0"
    chart_bg       = "rgba(244,247,251,0)"
    plotly_template= "plotly_white"

dir_attr = 'rtl' if lang == "AR" else 'ltr'

# ══════════════════════════════════════════
# DATA
# ══════════════════════════════════════════
# Based on DataSaudi and business_case.pdf
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

# Overnight stays in millions
inbound_nights = [320, 325, 310, 305, 345, 82, 95, 380, 432, 560]
domestic_nights = [395, 400, 410, 415, 425, 380, 445, 475, 496, 539]
total_nights = [a+b for a,b in zip(inbound_nights, domestic_nights)]

# Average length of stay (nights)
inbound_avg_stay = [12.5, 12.8, 13.1, 13.3, 13.8, 18.2, 17.5, 14.2, 14.8, 15.5]
domestic_avg_stay = [4.2, 4.3, 4.3, 4.4, 4.5, 5.8, 5.5, 5.6, 5.7, 5.8]

# Monthly average stay (2024)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
inbound_monthly_stay = [14.8, 15.2, 14.5, 13.2, 12.8, 12.5, 13.1, 14.0, 14.5, 15.0, 15.3, 15.5]
domestic_monthly_stay = [5.5, 5.6, 5.4, 5.2, 5.1, 5.8, 6.2, 6.0, 5.4, 5.3, 5.6, 5.8]

# Stay by purpose (nights)
purpose_stay = {
    "Religious": [18.5, 18.2, 18.0, 17.8, 18.3, 22.5, 21.8, 19.2, 19.8, 20.2],
    "Leisure": [8.2, 8.4, 8.5, 8.6, 8.8, 12.5, 11.8, 9.2, 9.5, 9.8],
    "Business": [5.5, 5.6, 5.7, 5.8, 5.9, 8.2, 7.8, 6.2, 6.4, 6.5],
    "VFR": [10.2, 10.4, 10.5, 10.6, 10.8, 15.2, 14.5, 11.2, 11.8, 12.2],
    "Other": [7.5, 7.6, 7.7, 7.8, 7.9, 11.2, 10.5, 8.2, 8.5, 8.8]
}

# Monthly nights distribution (2024) - millions
monthly_inbound_nights = [45.2, 41.5, 48.3, 42.1, 38.5, 40.2, 43.1, 45.8, 42.5, 44.2, 46.8, 52.8]
monthly_domestic_nights = [42.5, 38.2, 40.1, 38.5, 36.8, 48.5, 52.3, 50.1, 42.5, 41.2, 44.5, 48.8]

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
    border-left: 4px solid {accent_purple};
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
  }}
  .page-header::after {{
    content: '🏨';
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
    color: {accent_purple};
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
    border-bottom: 2px solid {accent_purple};
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
  
  .note {{
    font-size: 0.7rem;
    color: {text_secondary};
    text-align: right;
    margin-top: 4px;
    font-style: italic;
  }}
  
  .metric-highlight {{
    background: linear-gradient(135deg, {accent_purple}20, {accent_blue}20);
    border-radius: 8px;
    padding: 4px 8px;
    font-weight: 700;
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
    
    # Navigation buttons
    pages_list = [
        ("page_overview", "🏠"), ("page_trends", "📈"), ("page_season", "📅"),
        ("page_spend", "💰"), ("page_overnight", "🏨"), ("page_forecast", "🔮"),
        ("page_segment", "🎯"), ("page_carbon", "🌱")
    ]
    for page_key, icon in pages_list:
        active = page_key == "page_overnight"
        bg = f"{accent_purple}22" if active else "transparent"
        fw = "700" if active else "400"
        bc = accent_purple if active else "transparent"
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
    year_range = st.slider(t["filter_year"], 2015, 2024, (2019, 2024))
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
f_inbound_nights = inbound_nights[idx_s:idx_e]
f_domestic_nights = domestic_nights[idx_s:idx_e]
f_total_nights = total_nights[idx_s:idx_e]
f_inbound_avg = inbound_avg_stay[idx_s:idx_e]
f_domestic_avg = domestic_avg_stay[idx_s:idx_e]

# ══════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════
k1, k2, k3, k4, k5 = st.columns(5)

# Format numbers for display
total_nights_2024 = total_nights[-1] / 1000  # Convert to billions
inbound_nights_2024 = inbound_nights[-1]
domestic_nights_2024 = domestic_nights[-1]
inbound_avg_2024 = inbound_avg_stay[-1]
domestic_avg_2024 = domestic_avg_stay[-1]

with k1:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-icon'>🏨</div>
      <div class='kpi-value' style='color:{accent_teal};'>{total_nights_2024:.1f}B</div>
      <div class='kpi-label'>{t['total_nights_2024']}</div>
      <div class='kpi-delta' style='color:{accent_green};'>+18.2% YoY</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-icon'>✈️</div>
      <div class='kpi-value' style='color:{accent_blue};'>{inbound_nights_2024}M</div>
      <div class='kpi-label'>{t['inbound_nights_2024']}</div>
      <div class='kpi-delta' style='color:{accent_green};'>+29.6% YoY</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-icon'>🏠</div>
      <div class='kpi-value' style='color:{accent_gold};'>{domestic_nights_2024}M</div>
      <div class='kpi-label'>{t['domestic_nights_2024']}</div>
      <div class='kpi-delta' style='color:{accent_green};'>+8.7% YoY</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-icon'>⏱️</div>
      <div class='kpi-value' style='color:{accent_purple};'>{inbound_avg_2024}</div>
      <div class='kpi-label'>{t['avg_stay_inbound']}</div>
      <div class='kpi-delta' style='color:{accent_teal};'>2.7× domestic</div>
    </div>""", unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-icon'>📅</div>
      <div class='kpi-value' style='color:{accent_green};'>{domestic_avg_2024}</div>
      <div class='kpi-label'>{t['avg_stay_domestic']}</div>
      <div class='kpi-delta' style='color:{text_secondary};'>nights</div>
    </div>""", unsafe_allow_html=True)

st.markdown(f"<div class='note'>{t['data_source']} · {t['note']}</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# CHART 1: Annual Evolution
# ══════════════════════════════════════════
st.markdown(f"<div class='section-title'>📊 {t['annual_evolution']}</div>", unsafe_allow_html=True)

fig_annual = go.Figure()

if tourist_type in [t["all_types"], t["inbound"]]:
    fig_annual.add_trace(go.Bar(
        x=f_years, y=f_inbound_nights, name=t["inbound"],
        marker_color=accent_blue,
        marker_line_color=accent_blue,
        opacity=0.85,
        text=[f"{v}M" for v in f_inbound_nights],
        textposition='outside',
        textfont=dict(size=10, color=text_primary)
    ))
if tourist_type in [t["all_types"], t["domestic"]]:
    fig_annual.add_trace(go.Bar(
        x=f_years, y=f_domestic_nights, name=t["domestic"],
        marker_color=accent_teal,
        opacity=0.85,
        text=[f"{v}M" for v in f_domestic_nights],
        textposition='outside',
        textfont=dict(size=10, color=text_primary)
    ))
if tourist_type == t["all_types"]:
    fig_annual.add_trace(go.Scatter(
        x=f_years, y=f_total_nights, name=t["total"],
        line=dict(color=accent_gold, width=2.5, dash='dot'),
        marker=dict(size=8, color=accent_gold),
        yaxis='y2',
        text=[f"{v/1000:.1f}B" for v in f_total_nights],
        textposition='top center',
        textfont=dict(size=10, color=accent_gold)
    ))

# COVID annotation
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
    yaxis=dict(title=t["nights_m"], showgrid=True, gridcolor=border_color,
               tickfont=dict(size=10)),
    yaxis2=dict(overlaying='y', side='right', showgrid=False,
                title=t["nights_b"], tickfont=dict(size=10)),
    font=dict(color=text_primary),
    bargap=0.25
)
st.plotly_chart(fig_annual, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════
# CHARTS 2+3: Avg Length + Monthly Pattern
# ══════════════════════════════════════════
col_l, col_r = st.columns(2)

with col_l:
    st.markdown(f"<div class='section-title'>⏱️ {t['avg_length']}</div>", unsafe_allow_html=True)
    
    fig_avg = go.Figure()
    fig_avg.add_trace(go.Scatter(
        x=f_years, y=f_inbound_avg,
        name=t["inbound"],
        line=dict(color=accent_blue, width=3),
        mode='lines+markers',
        marker=dict(size=8, color=accent_blue),
        fill='tozeroy',
        fillcolor=f"{accent_blue}10"
    ))
    fig_avg.add_trace(go.Scatter(
        x=f_years, y=f_domestic_avg,
        name=t["domestic"],
        line=dict(color=accent_teal, width=3),
        mode='lines+markers',
        marker=dict(size=8, color=accent_teal),
        fill='tozeroy',
        fillcolor=f"{accent_teal}10"
    ))
    
    fig_avg.update_layout(
        template=plotly_template,
        paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.15),
        xaxis=dict(showgrid=False),
        yaxis=dict(title=t["days"], showgrid=True, gridcolor=border_color),
        font=dict(color=text_primary)
    )
    st.plotly_chart(fig_avg, use_container_width=True, config={"displayModeBar": False})

with col_r:
    st.markdown(f"<div class='section-title'>📅 {t['monthly_pattern']}</div>", unsafe_allow_html=True)
    
    fig_monthly = go.Figure()
    fig_monthly.add_trace(go.Scatter(
        x=months, y=inbound_monthly_stay,
        name=t["inbound"],
        line=dict(color=accent_blue, width=2.5

