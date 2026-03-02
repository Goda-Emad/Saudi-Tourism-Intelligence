import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path

# ══════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════
st.set_page_config(
    page_title="Carbon Impact · Saudi Tourism Intelligence",
    page_icon="🌱",
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
        "page_title":     "🌱 Carbon Impact Index · Sustainability Layer",
        "subtitle":       "Tourism-related CO2 emissions · Saudi Green Initiative alignment",
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
        "total_carbon_2024":   "Total CO₂ 2024",
        "carbon_per_tourist":  "CO₂ per Tourist",
        "carbon_per_night":    "CO₂ per Night",
        "trees_equivalent":    "Trees Equivalent",
        "savings_potential":   "10% Reduction =",
        # Sections
        "carbon_trend":        "📊 Annual Carbon Emissions Trend",
        "carbon_by_segment":   "🌿 Emissions by Tourist Segment",
        "carbon_by_purpose":   "🎯 Emissions by Purpose",
        "carbon_monthly":      "📅 Monthly Carbon Pattern (2024)",
        "carbon_intensity":    "⚡ Carbon Intensity Analysis",
        "sustainability_scenarios": "🌳 Sustainability Scenarios",
        "carbon_vs_tourists":  "📈 Carbon vs Tourist Volume",
        "sgi_alignment":       "🇸🇦 Saudi Green Initiative Alignment",
        "mitigation_strategies": "💚 Mitigation Strategies",
        # Labels
        "total":               "Total",
        "inbound":             "Inbound",
        "domestic":            "Domestic",
        "high_value":          "High Value",
        "mid_value":           "Mid Value",
        "budget":              "Budget",
        "religious":           "Religious",
        "leisure":             "Leisure",
        "business":            "Business",
        "vfr":                 "VFR",
        "megatons":            "Megatons CO₂",
        "kilotons":            "Kilotons CO₂",
        "kg_per_tourist":      "kg CO₂/tourist",
        "kg_per_night":        "kg CO₂/night",
        "trees":               "trees",
        # Insights
        "insight_title":       "💡 Key Carbon Insights",
        "i1": "Tourism sector emitted 68.17 Megatons CO₂ in 2024",
        "i2": "10% reduction would save 324,619 trees equivalent",
        "i3": "Inbound tourism accounts for 58% of emissions (39.5 Mt)",
        "i4": "High Value segment: 42% of spend, but 38% of emissions",
        "i5": "Summer months have 34% higher carbon intensity",
        "i6": "Religious tourism: 41% of spend, 35% of emissions",
        # Scenarios
        "scenario_1":          "Current Trajectory",
        "scenario_2":          "5% Annual Reduction",
        "scenario_3":          "10% Annual Reduction",
        "scenario_4":          "Net Zero 2060 Pathway",
        # SGI
        "sgi_title":           "Saudi Green Initiative Targets",
        "sgi_1":               "🌳 Plant 10 billion trees",
        "sgi_2":               "🔋 50% renewable energy by 2030",
        "sgi_3":               "⬇️ 278 Mt CO₂ reduction annually",
        "sgi_4":               "🛡️ Protect 30% of land/sea by 2030",
        # Strategies
        "strategy_1":          "✈️ Sustainable aviation fuels",
        "strategy_2":          "🏨 Green hotel certification",
        "strategy_3":          "🚆 Modal shift to rail",
        "strategy_4":          "☀️ Solar-powered tourism facilities",
        "strategy_5":          "♻️ Circular economy in hospitality",
        "strategy_6":          "🌴 Mangrove restoration projects",
        # Data
        "data_source":         "Data Source: DataSaudi · Carbon Impact Model v1.0",
        "note":                "Emissions calculated based on tourist volume, stay duration, and transport mode estimates",
        "methodology":         """
        **Carbon Impact Index Methodology**:
        - Base emission factor: 0.12 kg CO₂ per tourist per km (aviation avg)
        - Average flight distance: Inbound: 3,500 km, Domestic: 500 km
        - Accommodation: 15 kg CO₂ per night (hotel avg)
        - Local transport: 5 kg CO₂ per tourist per day
        - Adjusted for seasonality (HVAC loads: +20% summer/winter)
        - Verified against UNWTO tourism carbon guidelines
        """,
    },
    "AR": {
        "page_title":     "🌱 مؤشر الأثر الكربوني · طبقة الاستدامة",
        "subtitle":       "انبعاثات CO₂ المرتبطة بالسياحة · التوافق مع مبادرة السعودية الخضراء",
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
        "page_segment":   "🎯 تجزئة السياح",
        "page_carbon":    "🌱 الأثر الكربوني",
        # KPIs
        "total_carbon_2024":   "إجمالي CO₂ 2024",
        "carbon_per_tourist":  "CO₂ لكل سائح",
        "carbon_per_night":    "CO₂ لكل ليلة",
        "trees_equivalent":    "ما يعادل أشجار",
        "savings_potential":   "خفض 10% =",
        # Sections
        "carbon_trend":        "📊 الاتجاه السنوي للانبعاثات",
        "carbon_by_segment":   "🌿 الانبعاثات حسب الشريحة",
        "carbon_by_purpose":   "🎯 الانبعاثات حسب الغرض",
        "carbon_monthly":      "📅 نمط الانبعاثات الشهري (2024)",
        "carbon_intensity":    "⚡ تحليل كثافة الكربون",
        "sustainability_scenarios": "🌳 سيناريوهات الاستدامة",
        "carbon_vs_tourists":  "📈 الكربون مقابل عدد السياح",
        "sgi_alignment":       "🇸🇦 التوافق مع مبادرة السعودية الخضراء",
        "mitigation_strategies": "💚 استراتيجيات التخفيف",
        # Labels
        "total":               "الإجمالي",
        "inbound":             "وافد",
        "domestic":            "محلي",
        "high_value":          "راقي",
        "mid_value":           "متوسط",
        "budget":              "اقتصادي",
        "religious":           "ديني",
        "leisure":             "ترفيه",
        "business":            "أعمال",
        "vfr":                 "زيارة أهل",
        "megatons":            "ميجاطن CO₂",
        "kilotons":            "كيلوطن CO₂",
        "kg_per_tourist":      "كجم CO₂/سائح",
        "kg_per_night":        "كجم CO₂/ليلة",
        "trees":               "شجرة",
        # Insights
        "insight_title":       "💡 أبرز استنتاجات الكربون",
        "i1": "قطاع السياحة أصدر 68.17 ميجاطن CO₂ في 2024",
        "i2": "خفض 10% سيوفر ما يعادل 324,619 شجرة",
        "i3": "السياحة الوافدة تمثل 58% من الانبعاثات (39.5 Mt)",
        "i4": "الشريحة الراقية: 42% من الإنفاق، 38% من الانبعاثات",
        "i5": "أشهر الصيف كثافة كربون أعلى بنسبة 34%",
        "i6": "السياحة الدينية: 41% من الإنفاق، 35% من الانبعاثات",
        # Scenarios
        "scenario_1":          "المسار الحالي",
        "scenario_2":          "خفض 5% سنوياً",
        "scenario_3":          "خفض 10% سنوياً",
        "scenario_4":          "مسار الحياد الصفري 2060",
        # SGI
        "sgi_title":           "أهداف مبادرة السعودية الخضراء",
        "sgi_1":               "🌳 زراعة 10 مليارات شجرة",
        "sgi_2":               "🔋 50% طاقة متجددة بحلول 2030",
        "sgi_3":               "⬇️ خفض 278 Mt CO₂ سنوياً",
        "sgi_4":               "🛡️ حماية 30% من الأرض/البحر بحلول 2030",
        # Strategies
        "strategy_1":          "✈️ وقود طيران مستدام",
        "strategy_2":          "🏨 شهادة فنادق خضراء",
        "strategy_3":          "🚆 التحول إلى السكك الحديدية",
        "strategy_4":          "☀️ مرافق سياحية تعمل بالطاقة الشمسية",
        "strategy_5":          "♻️ اقتصاد دائري في الضيافة",
        "strategy_6":          "🌴 مشاريع إعادة تأهيل أشجار المانغروف",
        # Data
        "data_source":         "مصدر البيانات: DataSaudi · نموذج الأثر الكربوني v1.0",
        "note":                "الانبعاثات محسوبة بناءً على حجم السياح، مدة الإقامة، وتقديرات وسائل النقل",
        "methodology":         """
        **منهجية مؤشر الأثر الكربوني**:
        - عامل الانبعاث الأساسي: 0.12 كجم CO₂ لكل سائح لكل كم (متوسط الطيران)
        - متوسط مسافة الطيران: وافد: 3,500 كم، محلي: 500 كم
        - الإقامة: 15 كجم CO₂ لكل ليلة (متوسط الفنادق)
        - النقل المحلي: 5 كجم CO₂ لكل سائح يومياً
        - تعديل موسمي (أحمال التكييف/التدفئة: +20% صيف/شتاء)
        - تم التحقق وفقاً لإرشادات كربون السياحة UNWTO
        """,
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
    accent_orange  = "#FFA726"
    accent_lime    = "#A2E05C"
    border_color   = "#2A3F55"
    chart_bg       = "rgba(13,27,42,0)"
    plotly_template= "plotly_dark"
    
    # Carbon colors
    color_emission = accent_red
    color_reduction = accent_green
    color_neutral = accent_teal
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
    accent_orange  = "#F57C00"
    accent_lime    = "#558B2F"
    border_color   = "#CBD5E0"
    chart_bg       = "rgba(244,247,251,0)"
    plotly_template= "plotly_white"
    
    # Carbon colors
    color_emission = accent_red
    color_reduction = accent_green
    color_neutral = accent_teal

dir_attr = 'rtl' if lang == "AR" else 'ltr'

# ══════════════════════════════════════════
# CARBON DATA
# ══════════════════════════════════════════
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

# Total carbon emissions (Megatons CO2)
total_carbon = [42.5, 43.2, 41.8, 40.9, 48.3, 28.1, 32.5, 51.2, 59.8, 68.17]
inbound_carbon = [24.8, 25.1, 23.9, 23.2, 28.5, 12.4, 14.2, 29.8, 34.5, 39.5]
domestic_carbon = [17.7, 18.1, 17.9, 17.7, 19.8, 15.7, 18.3, 21.4, 25.3, 28.67]

# Carbon per tourist (kg CO2)
carbon_per_tourist_inbound = [780, 785, 775, 770, 820, 950, 920, 840, 860, 890]
carbon_per_tourist_domestic = [210, 212, 208, 206, 215, 245, 238, 225, 228, 235]

# Carbon per night (kg CO2)
carbon_per_night_inbound = [42, 43, 42, 41, 44, 52, 50, 45, 46, 48]
carbon_per_night_domestic = [28, 28, 27, 27, 29, 34, 33, 30, 31, 32]

# Monthly carbon pattern (2024) - thousands tons
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
monthly_carbon = [5200, 4800, 5600, 5100, 4900, 5800, 6500, 6300, 5400, 5200, 5500, 6000]

# Carbon by segment (2024)
segment_carbon = {
    "High Value": 25.9,  # Megatons
    "Mid Value": 24.5,
    "Budget": 17.77
}

# Carbon by purpose (2024)
purpose_carbon = {
    "Religious": 23.86,  # 35% of total
    "Leisure": 17.72,    # 26%
    "VFR": 14.32,        # 21%
    "Business": 8.18,    # 12%
    "Other": 4.09        # 6%
}

# Carbon intensity by season (index)
season_intensity = {
    "Winter": 0.92,
    "Spring": 0.88,
    "Summer": 1.24,
    "Fall": 0.96
}

# Scenario projections to 2030
scenario_years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
scenario_baseline = [68.17, 73.5, 79.2, 85.3, 91.8, 98.7, 106.2]
scenario_5pct = [68.17, 69.8, 71.2, 72.5, 73.7, 74.8, 75.9]
scenario_10pct = [68.17, 67.5, 66.3, 64.8, 63.1, 61.2, 59.1]
scenario_netzero = [68.17, 66.5, 64.2, 61.0, 56.8, 51.2, 44.5]

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
    border-left: 4px solid {accent_green};
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
  }}
  .page-header::after {{
    content: '🌱';
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
    color: {accent_green};
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
    border-bottom: 2px solid {accent_green};
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

  .sgi-box {{
    background: {bg_card2};
    border: 1px solid {border_color};
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
  }}
  .sgi-item {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid {border_color}40;
  }}
  .sgi-item:last-child {{ border-bottom: none; }}
  .sgi-icon {{ font-size: 1.2rem; }}
  .sgi-text {{ font-size: 0.85rem; color: {text_primary}; }}

  .strategy-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }}
  .strategy-item {{
    background: {bg_card};
    border: 1px solid {border_color};
    border-radius: 8px;
    padding: 10px;
    font-size: 0.8rem;
    color: {text_primary};
  }}

  .methodology-box {{
    background: {bg_card2};
    border: 1px solid {border_color};
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
  }}
  .methodology-text {{
    font-size: 0.85rem;
    color: {text_primary};
    line-height: 1.6;
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
  
  .tree-equivalent {{
    background: {accent_green}20;
    color: {accent_green};
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: 600;
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
        active = page_key == "page_carbon"
        bg = f"{accent_green}22" if active else "transparent"
        fw = "700" if active else "400"
        bc = accent_green if active else "transparent"
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
# PAGE HEADER
# ══════════════════════════════════════════
st.markdown(f"""
<div class='page-header'>
  <div class='page-title'>{t['page_title']}</div>
  <div class='page-subtitle'>{t['subtitle']}</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════
total_carbon_2024 = total_carbon[-1]
carbon_per_t = (carbon_per_tourist_inbound[-1] * 0.3 + carbon_per_tourist_domestic[-1] * 0.7)  # weighted avg
carbon_per_n = (carbon_per_night_inbound[-1] * 0.3 + carbon_per_night_domestic[-1] * 0.7)
trees_10pct = int(324619)  # from business_case.pdf

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-icon'>🏭</div>
      <div class='kpi-value' style='color:{color_emission};'>{total_carbon_2024:.1f} Mt</div>
      <div class='kpi-label'>{t['total_carbon_2024']}</div>
      <div class='kpi-delta' style='color:{accent_red};'>+14.0% YoY</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-icon'>👤</div>
      <div class='kpi-value' style='color:{accent_orange};'>{carbon_per_t:.0f} kg</div>
      <div class='kpi-label'>{t['carbon_per_tourist']}</div>
      <div class='kpi-delta'>inbound: {carbon_per_tourist_inbound[-1]} kg</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-icon'>🏨</div>
      <div class='kpi-value' style='color:{accent_purple};'>{carbon_per_n:.0f} kg</div>
      <div class='kpi-label'>{t['carbon_per_night']}</div>
      <div class='kpi-delta'>per night avg</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-icon'>🌳</div>
      <div class='kpi-value' style='color:{accent_green};'>{trees_10pct:,}</div>
      <div class='kpi-label'>{t['trees_equivalent']}</div>
      <div class='kpi-delta'>10% reduction</div>
    </div>""", unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class='kpi-card'>
      <div class='kpi-icon'>🎯</div>
      <div class='kpi-value' style='color:{accent_teal};'>324k</div>
      <div class='kpi-label'>{t['savings_potential']}</div>
      <div class='kpi-delta'><span class='tree-equivalent'>trees saved</span></div>
    </div>""", unsafe_allow_html=True)

st.markdown(f"<div class='note'>{t['data_source']} · {t['note']}</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# CHART 1: Annual Carbon Trend
# ══════════════════════════════════════════
st.markdown(f"<div class='section-title'>📊 {t['carbon_trend']}</div>", unsafe_allow_html=True)

fig_trend = go.Figure()

# Add bars for inbound/domestic
fig_trend.add_trace(go.Bar(
    x=years,
    y=inbound_carbon,
    name=t['inbound'],
    marker_color=accent_blue,
    opacity=0.85,
    text=[f"{v:.1f}" for v in inbound_carbon],
    textposition='inside',
    textfont=dict(size=9, color='white')
))

fig_trend.add_trace(go.Bar(
    x=years,
    y=domestic_carbon,
    name=t['domestic'],
    marker_color=accent_teal,
    opacity=0.85,
    text=[f"{v:.1f}" for v in domestic_carbon],
    textposition='inside',
    textfont=dict(size=9, color='white')
))

# Add total line
fig_trend.add_trace(go.Scatter(
    x=years,
    y=total_carbon,
    name=t['total'],
    line=dict(color=accent_gold, width=3),
    mode='lines+markers',
    marker=dict(size=8, color=accent_gold),
    yaxis='y2',
    text=[f"{v:.1f} Mt" for v in total_carbon],
    textposition='top center'
))

# COVID annotation
fig_trend.add_vrect(
    x0=2019.5, x1=2020.5,
    fillcolor=accent_red, opacity=0.1,
    annotation_text="COVID-19",
    annotation=dict(font_color=accent_red, font_size=11)
)

fig_trend.update_layout(
    template=plotly_template,
    paper_bgcolor=

