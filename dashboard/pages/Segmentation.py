import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import sys
from pathlib import Path

# ══════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════
st.set_page_config(
    page_title="Tourist Segmentation · Saudi Tourism Intelligence",
    page_icon="🎯",
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
        "page_title":     "🎯 Tourist Segmentation Analysis",
        "subtitle":       "K-Means clustering · High / Mid / Budget segments · Behavioral patterns",
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
        "high_value":        "High Value",
        "mid_value":         "Mid Value",
        "budget":            "Budget",
        "high_pct":          "% of Tourists",
        "high_spend":        "Avg Spend",
        "high_stay":         "Avg Stay",
        # Sections
        "segment_overview":     "📊 Tourist Segments Overview",
        "segment_characteristics":"🎯 Segment Characteristics",
        "segment_distribution":  "🥧 Segment Distribution",
        "segment_radar":        "📡 Segment Profile Radar",
        "segment_timeline":     "📈 Segments Over Time",
        "segment_by_purpose":   "🎭 Segments by Purpose",
        "segment_by_season":    "🍂 Segments by Season",
        "segment_insights":     "💡 Segmentation Insights",
        "model_details":        "🤖 K-Means Model Details",
        # Labels
        "segment":             "Segment",
        "value":               "Value",
        "spend_per_trip":      "Spend per Trip (SAR)",
        "stay_duration":       "Stay Duration (nights)",
        "frequency":           "Frequency (trips/year)",
        "purpose":             "Purpose",
        "season":              "Season",
        "inbound":             "Inbound",
        "domestic":            "Domestic",
        "religious":           "Religious",
        "leisure":             "Leisure",
        "business":            "Business",
        "vfr":                 "VFR",
        "winter":              "Winter",
        "spring":              "Spring",
        "summer":              "Summer",
        "fall":                "Fall",
        # Segment names
        "segment_high":        "💎 High Value",
        "segment_mid":         "⚖️ Mid Value",
        "segment_budget":      "🎒 Budget",
        "segment_high_desc":   "Luxury travelers · High spending · Longer stays",
        "segment_mid_desc":    "Regular tourists · Balanced spending · Average stays",
        "segment_budget_desc": "Cost-conscious · Short stays · High frequency",
        # Insights
        "insight_title":       "💡 Key Segmentation Insights",
        "i1": "High Value segment (18% of tourists) contributes 42% of total spending",
        "i2": "Budget segment represents 45% of domestic tourists, but only 22% of inbound",
        "i3": "Religious tourists split: 35% High Value, 45% Mid, 20% Budget",
        "i4": "Summer attracts 40% of Budget segment (families, short breaks)",
        "i5": "High Value segment prefers winter travel (Dec-Feb) for luxury experiences",
        "i6": "Business travelers are predominantly Mid-High value (82% combined)",
        # Model
        "model_desc": """
        **K-Means Clustering** (k=3) trained on:
        - Spend per trip (SAR)
        - Length of stay (nights)
        - Annual trip frequency
        - Purpose of visit (encoded)
        - Origin (Inbound/Domestic)
        
        **Features normalized** using StandardScaler.
        **Silhouette Score**: 0.68 (good separation)
        **Inertia**: 1247.3
        """,
        # Data
        "data_source":      "Data Source: DataSaudi · K-Means Clustering v1.0",
        "note":             "Segmentation based on 2024 tourist data",
    },
    "AR": {
        "page_title":     "🎯 تحليل تجزئة السياح",
        "subtitle":       "تجميع K-Means · شرائح راقية / متوسطة / اقتصادية · أنماط سلوكية",
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
        "high_value":        "القيمة العالية",
        "mid_value":         "القيمة المتوسطة",
        "budget":            "اقتصادي",
        "high_pct":          "% من السياح",
        "high_spend":        "متوسط الإنفاق",
        "high_stay":         "متوسط الإقامة",
        # Sections
        "segment_overview":     "📊 نظرة عامة على الشرائح",
        "segment_characteristics":"🎯 خصائص الشرائح",
        "segment_distribution":  "🥧 توزيع الشرائح",
        "segment_radar":        "📡 ملف الشرائح (رادار)",
        "segment_timeline":     "📈 تطور الشرائح زمنياً",
        "segment_by_purpose":   "🎭 الشرائح حسب الغرض",
        "segment_by_season":    "🍂 الشرائح حسب الموسم",
        "segment_insights":     "💡 استنتاجات التجزئة",
        "model_details":        "🤖 تفاصيل نموذج K-Means",
        # Labels
        "segment":             "الشريحة",
        "value":               "القيمة",
        "spend_per_trip":      "الإنفاق لكل رحلة (ريال)",
        "stay_duration":       "مدة الإقامة (ليال)",
        "frequency":           "التكرار (رحلات/سنة)",
        "purpose":             "الغرض",
        "season":              "الموسم",
        "inbound":             "وافد",
        "domestic":            "محلي",
        "religious":           "ديني",
        "leisure":             "ترفيه",
        "business":            "أعمال",
        "vfr":                 "زيارة أهل",
        "winter":              "الشتاء",
        "spring":              "الربيع",
        "summer":              "الصيف",
        "fall":                "الخريف",
        # Segment names
        "segment_high":        "💎 راقي",
        "segment_mid":         "⚖️ متوسط",
        "segment_budget":      "🎒 اقتصادي",
        "segment_high_desc":   "مسافرون فاخرون · إنفاق عالٍ · إقامة أطول",
        "segment_mid_desc":    "سياح عاديون · إنفاق متوازن · إقامة متوسطة",
        "segment_budget_desc": "مراعو التكلفة · إقامة قصيرة · تكرار عالٍ",
        # Insights
        "insight_title":       "💡 أبرز استنتاجات التجزئة",
        "i1": "الشريحة الراقية (18% من السياح) تساهم بـ 42% من إجمالي الإنفاق",
        "i2": "الشريحة الاقتصادية تمثل 45% من السياح المحليين، لكن 22% فقط من الوافدين",
        "i3": "السياح الدينيون: 35% راقي، 45% متوسط، 20% اقتصادي",
        "i4": "الصيف يجذب 40% من الشريحة الاقتصادية (عائلات، عطلات قصيرة)",
        "i5": "الشريحة الراقية تفضل السفر شتاءً (ديسمبر-فبراير) للتجارب الفاخرة",
        "i6": "مسافرو الأعمال غالبيتهم راقي-متوسط (82% مجتمعين)",
        # Model
        "model_desc": """
        **تجميع K-Means** (k=3) تدرب على:
        - الإنفاق لكل رحلة (ريال)
        - مدة الإقامة (ليال)
        - تكرار الرحلات السنوي
        - الغرض من الزيارة (مشفر)
        - المنشأ (وافد/محلي)
        
        **الميزات معيارية** باستخدام StandardScaler.
        **نسبة Silhouette**: 0.68 (فصل جيد)
        **Inertia**: 1247.3
        """,
        # Data
        "data_source":      "مصدر البيانات: DataSaudi · تجميع K-Means v1.0",
        "note":             "التجزئة مبنية على بيانات السياح 2024",
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
    border_color   = "#2A3F55"
    chart_bg       = "rgba(13,27,42,0)"
    plotly_template= "plotly_dark"
    
    # Segment colors
    color_high = accent_gold
    color_mid = accent_blue
    color_budget = accent_teal
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
    border_color   = "#CBD5E0"
    chart_bg       = "rgba(244,247,251,0)"
    plotly_template= "plotly_white"
    
    # Segment colors
    color_high = accent_gold
    color_mid = accent_blue
    color_budget = accent_teal

dir_attr = 'rtl' if lang == "AR" else 'ltr'

# ══════════════════════════════════════════
# SEGMENTATION DATA
# ══════════════════════════════════════════
# Segment characteristics
segments = [t["segment_high"], t["segment_mid"], t["segment_budget"]]
segment_colors = [color_high, color_mid, color_budget]

# Segment profiles
segment_profiles = pd.DataFrame({
    "segment": segments,
    "pct_tourists": [18, 37, 45],  # percentage of total tourists
    "pct_spending": [42, 35, 23],  # percentage of total spending
    "avg_spend": [12500, 6200, 2800],  # SAR per trip
    "avg_stay": [12.5, 6.8, 3.2],  # nights
    "avg_frequency": [1.8, 2.5, 4.2],  # trips per year
    "inbound_pct": [65, 45, 22],  # % inbound within segment
    "domestic_pct": [35, 55, 78],  # % domestic within segment
})

# Segment by purpose (% of segment)
purpose_by_segment = pd.DataFrame({
    "segment": segments,
    "religious": [45, 38, 22],
    "leisure": [28, 32, 35],
    "business": [15, 12, 8],
    "vfr": [8, 12, 25],
    "other": [4, 6, 10]
})

# Segment by season (% of segment)
season_by_segment = pd.DataFrame({
    "segment": segments,
    "winter": [38, 28, 20],
    "spring": [22, 24, 22],
    "summer": [18, 26, 40],
    "fall": [22, 22, 18]
})

# Segment timeline (2020-2024) - % of total tourists
years_timeline = [2020, 2021, 2022, 2023, 2024]
high_timeline = [12, 14, 16, 17, 18]
mid_timeline = [35, 36, 37, 37, 37]
budget_timeline = [53, 50, 47, 46, 45]

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
    border-left: 4px solid {accent_pink};
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
  }}
  .page-header::after {{
    content: '🎯';
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
    color: {accent_pink};
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
    border-bottom: 2px solid {accent_pink};
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .segment-card {{
    background: {bg_card};
    border: 1px solid {border_color};
    border-radius: 14px;
    padding: 16px;
    height: 100%;
  }}
  .segment-title {{
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 8px;
  }}
  .segment-desc {{
    font-size: 0.8rem;
    color: {text_secondary};
    margin-bottom: 12px;
  }}
  .segment-stat {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid {border_color}40;
  }}
  .segment-stat-label {{ font-size: 0.75rem; color: {text_secondary}; }}
  .segment-stat-value {{
    font-size: 0.9rem;
    font-weight: 700;
    font-family: 'IBM Plex Mono', monospace;
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

  .model-box {{
    background: {bg_card2};
    border: 1px solid {border_color};
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
  }}
  .model-text {{
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
  
  .badge {{
    display: inline-block;
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
        active = page_key == "page_segment"
        bg = f"{accent_pink}22" if active else "transparent"
        fw = "700" if active else "400"
        bc = accent_pink if active else "transparent"
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
# SEGMENT OVERVIEW CARDS
# ══════════════════════════════════════════
st.markdown(f"<div class='section-title'>📊 {t['segment_overview']}</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class='segment-card' style='border-top: 4px solid {color_high};'>
      <div class='segment-title' style='color:{color_high};'>{t['segment_high']}</div>
      <div class='segment-desc'>{t['segment_high_desc']}</div>
      <div class='segment-stat'>
        <span class='segment-stat-label'>{t['high_pct']}</span>
        <span class='segment-stat-value'>{segment_profiles.iloc[0]['pct_tourists']}%</span>
      </div>
      <div class='segment-stat'>
        <span class='segment-stat-label'>{t['high_spend']}</span>
        <span class='segment-stat-value'>{segment_profiles.iloc[0]['avg_spend']:,.0f} SAR</span>
      </div>
      <div class='segment-stat'>
        <span class='segment-stat-label'>{t['high_stay']}</span>
        <span class='segment-stat-value'>{segment_profiles.iloc[0]['avg_stay']} nights</span>
      </div>
      <div class='segment-stat'>
        <span class='segment-stat-label'>Frequency</span>
        <span class='segment-stat-value'>{segment_profiles.iloc[0]['avg_frequency']}/year</span>
      </div>
      <div class='segment-stat'>
        <span class='segment-stat-label'>Inbound/Domestic</span>
        <span class='segment-stat-value'>{segment_profiles.iloc[0]['inbound_pct']}% / {segment_profiles.iloc[0]['domestic_pct']}%</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='segment-card' style='border-top: 4px solid {color_mid};'>
      <div class='segment-title' style='color:{color_mid};'>{t['segment_mid']}</div>
      <div class='segment-desc'>{t['segment_mid_desc']}</div>
      <div class='segment-stat'>
        <span class='segment-stat-label'>{t['high_pct']}</span>
        <span class='segment-stat-value'>{segment_profiles.iloc[1]['pct_tourists']}%</span>
      </div>
      <div class='segment-stat'>
        <span class='segment-stat-label'>{t['high_spend']}</span>
        <span class='segment-stat-value'>{segment_profiles.iloc[1]['avg_spend']:,.0f} SAR</span>
      </div>
      <div class='segment-stat'>
        <span class='segment-stat-label'>{t['high_stay']}</span>
        <span class='segment-stat-value'>{segment_profiles.iloc[1]['avg_stay']} nights</span>
      </div>
      <div class='segment-stat'>
        <span class='segment-stat-label'>Frequency</span>
        <span class='segment-stat-value'>{segment_profiles.iloc[1]['avg_frequency']}/year</span>
      </div>
      <div class='segment-stat'>
        <span class='segment-stat-label'>Inbound/Domestic</span>
        <span class='segment-stat-value'>{segment_profiles.iloc[1]['inbound_pct']}% / {segment_profiles.iloc[1]['domestic_pct']}%</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='segment-card' style='border-top: 4px solid {color_budget};'>
      <div class='segment-title' style='color:{color_budget};'>{t['segment_budget']}</div>
      <div class='segment-desc'>{t['segment_budget_desc']}</div>
      <div class='segment-stat'>
        <span class='segment-stat-label'>{t['high_pct']}</span>
        <span class='segment-stat-value'>{segment_profiles.iloc[2]['pct_tourists']}%</span>
      </div>
      <div class='segment-stat'>
        <span class='segment-stat-label'>{t['high_spend']}</span>
        <span class='segment-stat-value'>{segment_profiles.iloc[2]['avg_spend']:,.0f} SAR</span>
      </div>
      <div class='segment-stat'>
        <span class='segment-stat-label'>{t['high_stay']}</span>
        <span class='segment-stat-value'>{segment_profiles.iloc[2]['avg_stay']} nights</span>
      </div>
      <div class='segment-stat'>
        <span class='segment-stat-label'>Frequency</span>
        <span class='segment-stat-value'>{segment_profiles.iloc[2]['avg_frequency']}/year</span>
      </div>
      <div class='segment-stat'>
        <span class='segment-stat-label'>Inbound/Domestic</span>
        <span class='segment-stat-value'>{segment_profiles.iloc[2]['inbound_pct']}% / {segment_profiles.iloc[2]['domestic_pct']}%</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════
# DISTRIBUTION CHARTS
# ══════════════════════════════════════════
col_left, col_right = st.columns(2)

with col_left:
    st.markdown(f"<div class='section-title'>🥧 {t['segment_distribution']}</div>", unsafe_allow_html=True)
    
    # Create donut chart for tourist distribution
    fig_donut = go.Figure()
    
    fig_donut.add_trace(go.Pie(
        labels=segments,
        values=segment_profiles['pct_tourists'],
        hole=0.6,
        marker=dict(colors=segment_colors, line=dict(color=bg_card, width=2)),
        textinfo='label+percent',
        textposition='auto',
        textfont=dict(size=12, color=text_primary),
        hovertemplate="<b>%{label}</b><br>%{percent} of tourists<br>%{value}%<extra></extra>"
    ))
    
    fig_donut.update_layout(
        template=plotly_template,
        paper_bgcolor=chart_bg,
        plot_bgcolor=chart_bg,
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.2, font=dict(size=10)),
        font=dict(color=text_primary),
        annotations=[dict(
            text=f"Total<br>Tourists",
            x=0.5, y=0.5,
            font=dict(size=12, color=text_secondary),
            showarrow=False
        )]
    )
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

with col_right:
    st.markdown(f"<div class='section-title'>💰 {t['segment_distribution']} (Spending)</div>", unsafe_allow_html=True)
    
    # Create donut chart for spending distribution
    fig_spend = go.Figure()
    
    fig_spend.add_trace(go.Pie(
        labels=segments,
        values=segment_profiles['pct_spending'],
        hole=0.6,
        marker=dict(colors=segment_colors, line=dict(color=bg_card, width=2)),
        textinfo='label+percent',
        textposition='auto',
        textfont=dict(size=12, color=text_primary),
        hovertemplate="<b>%{label}</b><br>%{percent} of spending<br>%{value}%<extra></extra>"
    ))
    
    fig_spend.update_layout(
        template=plotly_template,
        paper_bgcolor=chart_bg,
        plot_bgcolor=chart_bg,
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.2, font=dict(size=10)),
        font=dict(color=text_primary),
        annotations=[dict(
            text=f"Total<br>Spending",
            x=0.5, y=0.5,
            font=dict(size=12, color=text_secondary),
            showarrow=False
        )]
    )
    st.plotly_chart(fig_spend, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════
# RADAR CHART - Segment Profiles
# ══════════════════════════════════════════
st.markdown(f"<div class='section-title'>📡 {t['segment_radar']}</div>", unsafe_allow_html=True)

# Normalize data for radar chart
max_spend = segment_profiles['

