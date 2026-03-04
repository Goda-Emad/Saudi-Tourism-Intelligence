import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ══════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════
st.set_page_config(
    page_title="Seasonality · Saudi Tourism Intelligence",
    page_icon="📅",
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
        "page_title":       "📅 Seasonality Analysis",
        "subtitle":         "Peak & Low Seasons · Monthly Patterns · Ramadan vs Summer",
        "built_by":         "Built by",
        "dark_mode":        "🌙 Dark",
        "light_mode":       "☀️ Light",
        "lang_toggle":      "🌐 العربية",
        "pages":            "Navigation",
        "page_overview":    "🏠 Overview",
        "page_trends":      "📈 Tourist Trends",
        "page_season":      "📅 Seasonality",
        "page_spend":       "💰 Spending",
        "page_overnight":   "🏨 Overnight Stays",
        "page_forecast":    "🔮 Forecasting",
        "page_segment":     "🎯 Segmentation",
        "page_carbon":      "🌱 Carbon Impact",
        # KPIs
        "peak_month":       "Peak Month",
        "low_month":        "Low Month",
        "peak_diff":        "Peak vs Low",
        "inbound_peak":     "Inbound Peak",
        "domestic_peak":    "Domestic Peak",
        # Sections
        "monthly_avg":      "Average Monthly Tourists (All Years)",
        "monthly_heatmap":  "Monthly Heatmap by Year",
        "seasonal_compare": "Seasonal Comparison: Inbound vs Domestic",
        "quarter_analysis": "Quarterly Analysis",
        "ramadan_effect":   "Ramadan & Holiday Effect",
        "radar_chart":      "Seasonal Radar Chart",
        # Labels
        "inbound":          "Inbound",
        "domestic":         "Domestic",
        "total":            "Total",
        "tourists_k":       "Tourists (Thousands)",
        "tourists_m":       "Tourists (Millions)",
        "month":            "Month",
        "quarter":          "Quarter",
        "filter_type":      "Tourist Type",
        "all_types":        "All",
        "insight_title":    "Key Insights",
        "i1": "January is the overall peak month with 73,127K tourists — 41% above Low Season",
        "i2": "Inbound peaks in December (winter tourism) — Domestic peaks in July (summer holidays)",
        "i3": "Q1 (Jan–Mar) and Q3 (Jul–Sep) are nearly equal — both are high seasons",
        "i4": "May is the lowest month — Ramadan + heat causes -29% below annual average",
        "q1": "Q1 · Jan–Mar",
        "q2": "Q2 · Apr–Jun",
        "q3": "Q3 · Jul–Sep",
        "q4": "Q4 · Oct–Dec",
        "ramadan_note":     "Ramadan Effect: Inbound ↑ (Religious), Domestic ↓ (travel slows)",
        "summer_note":      "Summer Effect: Domestic ↑ (school holidays), Inbound ↓ (heat)",
    },
    "AR": {
        "page_title":       "📅 تحليل الموسمية",
        "subtitle":         "ذروة ومواسم الانخفاض · الأنماط الشهرية · رمضان مقابل الصيف",
        "built_by":         "من تطوير",
        "dark_mode":        "🌙 داكن",
        "light_mode":       "☀️ فاتح",
        "lang_toggle":      "🌐 English",
        "pages":            "التنقل",
        "page_overview":    "🏠 نظرة عامة",
        "page_trends":      "📈 اتجاهات السياحة",
        "page_season":      "📅 الموسمية",
        "page_spend":       "💰 الإنفاق",
        "page_overnight":   "🏨 ليالي الإقامة",
        "page_forecast":    "🔮 التوقعات",
        "page_segment":     "🎯 تقسيم السياح",
        "page_carbon":      "🌱 الأثر الكربوني",
        "peak_month":       "شهر الذروة",
        "low_month":        "أدنى شهر",
        "peak_diff":        "الذروة مقابل الأدنى",
        "inbound_peak":     "ذروة الوافدين",
        "domestic_peak":    "ذروة المحليين",
        "monthly_avg":      "متوسط السياح الشهري (كل السنوات)",
        "monthly_heatmap":  "خريطة حرارية شهرية حسب السنة",
        "seasonal_compare": "مقارنة موسمية: وافد مقابل محلي",
        "quarter_analysis": "التحليل الربعي",
        "ramadan_effect":   "تأثير رمضان والإجازات",
        "radar_chart":      "مخطط رادار الموسمية",
        "inbound":          "وافد",
        "domestic":         "محلي",
        "total":            "إجمالي",
        "tourists_k":       "السياح (ألف)",
        "tourists_m":       "السياح (مليون)",
        "month":            "الشهر",
        "quarter":          "الربع",
        "filter_type":      "نوع السائح",
        "all_types":        "الكل",
        "insight_title":    "أبرز الاستنتاجات",
        "i1": "يناير هو شهر الذروة الكلية بـ 73,127 ألف سائح — أعلى بـ 41% من موسم الانخفاض",
        "i2": "الوافدون يبلغون ذروتهم في ديسمبر (سياحة الشتاء) — المحليون في يوليو (إجازة الصيف)",
        "i3": "الربع الأول (يناير–مارس) والثالث (يوليو–سبتمبر) متقاربان — كلاهما موسم مرتفع",
        "i4": "مايو هو الأدنى — رمضان + الحر يسببان -29% دون المتوسط السنوي",
        "q1": "ر1 · يناير–مارس",
        "q2": "ر2 · أبريل–يونيو",
        "q3": "ر3 · يوليو–سبتمبر",
        "q4": "ر4 · أكتوبر–ديسمبر",
        "ramadan_note":     "تأثير رمضان: الوافدون ↑ (ديني)، المحليون ↓ (تباطؤ السفر)",
        "summer_note":      "تأثير الصيف: المحليون ↑ (إجازات المدارس)، الوافدون ↓ (الحر)",
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
    accent_orange  = "#FF9800"
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
    accent_orange  = "#E65100"
    border_color   = "#CBD5E0"
    chart_bg       = "rgba(244,247,251,0)"
    plotly_template= "plotly_white"

dir_attr = 'rtl' if lang == "AR" else 'ltr'

# ══════════════════════════════════════════
# DATA
# ══════════════════════════════════════════
months_en  = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
months_ar  = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
months_lbl = months_ar if lang == "AR" else months_en

# Monthly totals (thousands) — all years aggregated
total_monthly   = [73127, 61529, 62585, 56938, 51868, 62935, 67220, 65582, 58646, 55202, 66627, 62376]
inbound_monthly = [2470,  2130,  2800,  2320,  1890,  2120,  2220,  2160,  1930,  1880,  2220,  2590]
domestic_monthly= [6960,  5320,  5710,  5330,  4780,  7850,  9610,  7980,  5790,  5370,  7350,  8110]

# Yearly monthly heatmap data (inbound, thousands)
heatmap_years = list(range(2015, 2025))
heatmap_data  = [
    [1189,1103, 978, 912, 589, 703, 701, 570, 589, 490, 487, 427],  # 2015
    [1100,1050, 920, 870, 560, 670, 660, 540, 560, 460, 460, 410],  # 2016
    [1000, 950, 850, 800, 500, 600, 600, 480, 500, 410, 410, 360],  # 2017
    [ 980, 930, 830, 780, 490, 590, 580, 460, 480, 400, 395, 350],  # 2018
    [1100,1050, 960, 900, 560, 670, 660, 540, 560, 460, 460, 410],  # 2019
    [ 180, 160, 140, 130,  80, 100, 100,  80,  90,  70,  70,  60],  # 2020 COVID
    [ 120, 110,  90,  85,  60,  80,  80,  60,  70,  55,  55,  50],  # 2021
    [ 900, 850, 780, 720, 440, 530, 520, 420, 450, 360, 355, 315],  # 2022
    [1800,1700,1560,1440, 900,1060,1050, 840, 900, 720, 720, 640],  # 2023
    [2470,2130,2800,2320,1890,2120,2220,2160,1930,1880,2220,2590],  # 2024
]

# Quarterly
quarters_lbl = [t["q1"], t["q2"], t["q3"], t["q4"]]
inbound_q    = [7400,  6330,  6310,  7250]
domestic_q   = [17990, 17960, 23380, 22830]

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
    content: '📅';
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
  .kpi-sub {{
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 4px;
    color: {text_secondary};
    font-family: 'IBM Plex Mono', monospace;
  }}

  .section-title {{
    font-size: 1.05rem;
    font-weight: 700;
    color: {text_primary};
    margin: 24px 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid {accent_gold};
  }}

  .insight-card {{
    background: {bg_card};
    border: 1px solid {border_color};
    border-radius: 12px;
    padding: 14px 16px;
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 10px;
  }}
  .insight-icon {{ font-size: 1.2rem; flex-shrink: 0; margin-top: 2px; }}
  .insight-text {{
    font-size: 0.83rem;
    color: {text_primary};
    line-height: 1.5;
  }}

  .note-box {{
    background: {bg_card2};
    border: 1px solid {border_color};
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 0.82rem;
    color: {text_secondary};
    margin-top: 10px;
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
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════

# ── Shared sidebar (identical across all pages) ──────────────────
import base64 as _b64mod, glob as _glob, os as _os

def _get_logo():
    try:
        base = _os.path.dirname(_os.path.abspath(__file__))
        for p in ["assets/logo.jpg","assets/logo.png"]:
            fp = _os.path.join(base, p)
            if _os.path.exists(fp):
                with open(fp,"rb") as f:
                    d = _b64mod.b64encode(f.read()).decode()
                ext = "png" if p.endswith("png") else "jpeg"
                return f"data:image/{ext};base64,{d}"
    except: pass
    return ""

_logo_src = _get_logo()
_logo_img = (f'<img src="{_logo_src}" style="height:42px;border-radius:8px;"/>'
             if _logo_src else '<span style="font-size:2rem;">🇸🇦</span>')

NAV_EN = [
    ("🏠  Overview",        "Overview.py"),
    ("📈  Tourist Trends",   "Tourist_Trends.py"),
    ("📅  Seasonality",      "Seasonality.py"),
    ("💰  Spending",         "Spending.py"),
    ("🏨  Overnight Stays",  "Overnight_Stays.py"),
    ("🔮  Forecasting",      "Forecasting.py"),
    ("🎯  Segmentation",     "Segmentation.py"),
    ("🌱  Carbon Impact",    "Carbon_Impact.py"),
]
NAV_AR = [
    ("🏠  النظرة التنفيذية", "Overview.py"),
    ("📈  اتجاهات السياحة",  "Tourist_Trends.py"),
    ("📅  الموسمية",         "Seasonality.py"),
    ("💰  الإنفاق",          "Spending.py"),
    ("🏨  ليالي الإقامة",    "Overnight_Stays.py"),
    ("🔮  التوقعات",         "Forecasting.py"),
    ("🎯  التقسيم",          "Segmentation.py"),
    ("🌱  الأثر الكربوني",   "Carbon_Impact.py"),
]

_C_NAV   = "#031414" if THEME=="dark" else "#172025"
_C_WHITE = "#F4F9F8" if THEME=="dark" else "#0D1A1E"
_C_TEAL  = "#17B19B"
_C_GREY  = "#A1A6B7" if THEME=="dark" else "#374151"
_C_GOLD  = "#C9A84C"
_C_BDR   = "#2A3235" if THEME=="dark" else "#C8D8D5"
_FF      = "Tajawal" if LANG=="AR" else "IBM Plex Sans"

st.markdown(
    "<style>"
    f"[data-testid='stSidebar']{{background:{_C_NAV}!important;border-right:1px solid {_C_BDR}!important;}}"
    f"[data-testid='stSidebar'] div,span,p,label{{color:{_C_WHITE}!important;}}"
    "[data-testid='stSidebar'] .stButton>button{"
    f"background:transparent!important;border:1px solid transparent!important;"
    f"color:{_C_GREY}!important;border-radius:8px!important;"
    "width:100%!important;font-size:.84rem!important;font-weight:500!important;"
    "padding:9px 12px!important;margin-bottom:2px!important;transition:all .15s!important;}"
    "[data-testid='stSidebar'] .stButton>button:hover{"
    f"background:{_C_TEAL}22!important;color:{_C_TEAL}!important;border-color:{_C_TEAL}44!important;}}"
    "[data-testid='stSidebar'] div:nth-child(3) .stButton>button,"
    "[data-testid='stSidebar'] div:nth-child(4) .stButton>button{"
    "background:#2A3235!important;border:1px solid #3A4C50!important;"
    "color:#F4F9F8!important;font-weight:600!important;margin-bottom:5px!important;}"
    "[data-testid='stSidebar'] div:nth-child(3) .stButton>button:hover,"
    "[data-testid='stSidebar'] div:nth-child(4) .stButton>button:hover{"
    f"border-color:{_C_GOLD}!important;color:{_C_GOLD}!important;}}"
    "</style>",
    unsafe_allow_html=True)

with st.sidebar:
    _thm_label = ("☀️  Light" if THEME=="dark" else "🌙  Dark")
    _lng_label = ("🌐  العربية" if LANG=="EN" else "🌐  English")

    st.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;padding:16px 4px 14px;">'+_logo_img+
        f'<div><div style="font-size:.88rem;font-weight:700;color:{_C_WHITE};">'+
        ("Saudi Tourism Intelligence" if LANG=="EN" else "ذكاء السياحة السعودية")+
        f'</div><div style="font-size:.58rem;color:{_C_TEAL};font-weight:600;letter-spacing:1.2px;text-transform:uppercase;">AI ANALYTICS PLATFORM</div></div></div>',
        unsafe_allow_html=True)

    st.markdown(f'<div style="height:1px;background:{_C_BDR};margin-bottom:10px;"></div>', unsafe_allow_html=True)

    if st.button(_thm_label, key="sb_thm", use_container_width=True):
        st.session_state.theme = "light" if THEME=="dark" else "dark"; st.rerun()
    if st.button(_lng_label, key="sb_lng", use_container_width=True):
        st.session_state.lang = "AR" if LANG=="EN" else "EN"; st.rerun()

    st.markdown(f'<div style="height:1px;background:{_C_BDR};margin:10px 0 6px;"></div>', unsafe_allow_html=True)

    _nav_items = NAV_AR if LANG=="AR" else NAV_EN
    for _lbl, _fname in _nav_items:
        if st.button(_lbl, key="sb_nav_"+_fname, use_container_width=True):
            st.switch_page("pages/" + _fname)

    st.markdown(f'<div style="height:1px;background:{_C_BDR};margin:10px 0 8px;"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-size:.67rem;color:{_C_GREY};padding:0 2px;line-height:1.9;">'+
        '📦 DataSaudi · 2015–2024<br>'+
        f'🐙 <a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" target="_blank" style="color:{_C_TEAL};text-decoration:none;">GitHub</a>'+
        '  ·  '+
        f'💼 <a href="https://www.linkedin.com/in/goda-emad/" target="_blank" style="color:{_C_TEAL};text-decoration:none;">LinkedIn</a></div>',
        unsafe_allow_html=True)
# ── End sidebar ───────────────────────────────────────────────────

st.markdown(f"""
<div class='page-header'>
  <div class='page-title'>{t['page_title']}</div>
  <div class='page-subtitle'>{t['subtitle']}</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════
k1, k2, k3, k4, k5 = st.columns(5)
kpi_items = [
    (k1, "🏆", t["peak_month"],    "January",   "73,127K",  accent_gold),
    (k2, "📉", t["low_month"],     "May",        "51,868K",  accent_red),
    (k3, "📊", t["peak_diff"],     "+41.0%",     "Peak vs Low", accent_teal),
    (k4, "✈️", t["inbound_peak"],  "December",   "17,890K",  accent_blue),
    (k5, "🏠", t["domestic_peak"], "July",       "58,076K",  accent_purple),
]
for col, icon, label, val, sub, color in kpi_items:
    with col:
        st.markdown(f"""
        <div class='kpi-card'>
          <div class='kpi-icon'>{icon}</div>
          <div class='kpi-value' style='color:{color};'>{val}</div>
          <div class='kpi-label'>{label}</div>
          <div class='kpi-sub'>{sub}</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# CHART 1: Monthly Average Bar
# ══════════════════════════════════════════
st.markdown(f"<div class='section-title'>📊 {t['monthly_avg']}</div>", unsafe_allow_html=True)

if tourist_filter == t["inbound"]:
    y_data = [v/1000 for v in inbound_monthly]
    bar_color = accent_blue
elif tourist_filter == t["domestic"]:
    y_data = [v/1000 for v in domestic_monthly]
    bar_color = accent_teal
else:
    y_data = [v/1000 for v in total_monthly]
    bar_color = accent_gold

avg_val = sum(y_data) / len(y_data)
bar_colors = [accent_red if v == min(y_data) else
              accent_green if v == max(y_data) else
              bar_color for v in y_data]

fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    x=months_lbl, y=y_data,
    marker_color=bar_colors,
    text=[f"{v:.1f}M" for v in y_data],
    textposition='outside',
    textfont=dict(size=9, color=text_primary),
))
fig_bar.add_hline(
    y=avg_val,
    line_dash="dash", line_color=text_secondary, line_width=1.5,
    annotation_text=f"Avg: {avg_val:.1f}M",
    annotation_font_color=text_secondary,
    annotation_font_size=10
)

# Ramadan & Summer zones
fig_bar.add_vrect(x0=-0.5, x1=2.5,
    fillcolor=accent_gold, opacity=0.05,
    annotation_text="🌙 Ramadan", annotation_position="top left",
    annotation=dict(font_color=accent_gold, font_size=10))
fig_bar.add_vrect(x0=5.5, x1=8.5,
    fillcolor=accent_blue, opacity=0.05,
    annotation_text="☀️ Summer", annotation_position="top left",
    annotation=dict(font_color=accent_blue, font_size=10))

fig_bar.update_layout(
    template=plotly_template,
    paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
    height=360, margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(showgrid=False, tickfont=dict(size=11)),
    yaxis=dict(showgrid=True, gridcolor=border_color,
               tickfont=dict(size=10), title=t["tourists_m"]),
    font=dict(color=text_primary),
    showlegend=False,
)
st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════
# CHART 2 + 3: Heatmap + Seasonal Compare
# ══════════════════════════════════════════
heat_col, compare_col = st.columns([3, 2])

with heat_col:
    st.markdown(f"<div class='section-title'>🌡️ {t['monthly_heatmap']}</div>", unsafe_allow_html=True)

    fig_heat = go.Figure(go.Heatmap(
        z=heatmap_data,
        x=months_lbl,
        y=[str(y) for y in heatmap_years],
        colorscale=[
            [0.0,  bg_card2],
            [0.15, accent_blue],
            [0.5,  accent_teal],
            [1.0,  accent_gold],
        ],
        showscale=True,
        hovertemplate="<b>%{y} %{x}</b><br>%{z:.0f}K tourists<extra></extra>",
        colorbar=dict(
            tickfont=dict(size=9, color=text_primary),
            title=dict(text="K", font=dict(color=text_secondary, size=10))
        )
    ))
    # COVID annotation
    fig_heat.add_annotation(
        x="Jun", y="2020",
        text="COVID-19",
        showarrow=False,
        font=dict(size=10, color=accent_red),
        bgcolor=f"{accent_red}33",
        borderpad=3
    )
    fig_heat.update_layout(
        template=plotly_template,
        paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=320, margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10), autorange="reversed"),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})

with compare_col:
    st.markdown(f"<div class='section-title'>⚡ {t['seasonal_compare']}</div>", unsafe_allow_html=True)

    fig_comp = go.Figure()
    fig_comp.add_trace(go.Scatter(
        x=months_lbl, y=[v/1000 for v in inbound_monthly],
        name=t["inbound"],
        line=dict(color=accent_blue, width=2.5),
        fill='tozeroy', fillcolor=f"{accent_blue}18",
        marker=dict(size=7)
    ))
    fig_comp.add_trace(go.Scatter(
        x=months_lbl, y=[v/1000 for v in domestic_monthly],
        name=t["domestic"],
        line=dict(color=accent_teal, width=2.5),
        fill='tozeroy', fillcolor=f"{accent_teal}18",
        marker=dict(size=7)
    ))
    fig_comp.add_annotation(x="Dec", y=max([v/1000 for v in inbound_monthly]),
        text="Dec Peak", showarrow=True, arrowhead=2,
        font=dict(size=9, color=accent_blue), arrowcolor=accent_blue, ay=-30)
    fig_comp.add_annotation(x="Jul", y=max([v/1000 for v in domestic_monthly]),
        text="Jul Peak", showarrow=True, arrowhead=2,
        font=dict(size=9, color=accent_teal), arrowcolor=accent_teal, ay=-30)

    fig_comp.update_layout(
        template=plotly_template,
        paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=320, margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.18, font=dict(size=10)),
        xaxis=dict(showgrid=False, tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor=border_color,
                   tickfont=dict(size=10), title=t["tourists_m"]),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_comp, use_container_width=True, config={"displayModeBar": False})

    st.markdown(f"""
    <div class='note-box'>
      🌙 {t['ramadan_note']}<br><br>
      ☀️ {t['summer_note']}
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# CHART 4 + 5: Quarterly + Radar
# ══════════════════════════════════════════
q_col, radar_col = st.columns([2, 2])

with q_col:
    st.markdown(f"<div class='section-title'>📆 {t['quarter_analysis']}</div>", unsafe_allow_html=True)

    fig_q = go.Figure()
    fig_q.add_trace(go.Bar(
        x=quarters_lbl, y=[v/1000 for v in inbound_q],
        name=t["inbound"],
        marker_color=accent_blue, opacity=0.88
    ))
    fig_q.add_trace(go.Bar(
        x=quarters_lbl, y=[v/1000 for v in domestic_q],
        name=t["domestic"],
        marker_color=accent_teal, opacity=0.88
    ))
    fig_q.update_layout(
        template=plotly_template,
        paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=300, barmode='group',
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.18, font=dict(size=10)),
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor=border_color,
                   tickfont=dict(size=10), title=t["tourists_m"]),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_q, use_container_width=True, config={"displayModeBar": False})

with radar_col:
    st.markdown(f"<div class='section-title'>🎯 {t['radar_chart']}</div>", unsafe_allow_html=True)

    inb_norm = [v/max(inbound_monthly) for v in inbound_monthly]
    dom_norm = [v/max(domestic_monthly) for v in domestic_monthly]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=inb_norm + [inb_norm[0]],
        theta=months_lbl + [months_lbl[0]],
        fill='toself',
        name=t["inbound"],
        line_color=accent_blue,
        fillcolor=f"{accent_blue}25"
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=dom_norm + [dom_norm[0]],
        theta=months_lbl + [months_lbl[0]],
        fill='toself',
        name=t["domestic"],
        line_color=accent_teal,
        fillcolor=f"{accent_teal}25"
    ))
    fig_radar.update_layout(
        template=plotly_template,
        paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=300, margin=dict(l=30, r=30, t=20, b=10),
        polar=dict(
            bgcolor=bg_card2,
            radialaxis=dict(showticklabels=False, gridcolor=border_color),
            angularaxis=dict(tickfont=dict(size=10, color=text_primary),
                             gridcolor=border_color)
        ),
        legend=dict(orientation="h", y=-0.1, font=dict(size=10)),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════
# KEY INSIGHTS
# ══════════════════════════════════════════
st.markdown(f"<div class='section-title'>💡 {t['insight_title']}</div>", unsafe_allow_html=True)

insights = [
    ("🏆", t["i1"], accent_gold),
    ("✈️", t["i2"], accent_blue),
    ("📊", t["i3"], accent_teal),
    ("🌙", t["i4"], accent_red),
]
ins_cols = st.columns(2)
for i, (icon, text, color) in enumerate(insights):
    with ins_cols[i % 2]:
        st.markdown(f"""
        <div class='insight-card' style='border-left:3px solid {color};'>
          <div class='insight-icon'>{icon}</div>
          <div class='insight-text'>{text}</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════
st.markdown(f"""
<div class='footer-bar'>
  <div>
    <div class='footer-name'>Eng. Goda Emad — Saudi Tourism Intelligence</div>
    <div class='footer-link'>Data: DataSaudi · Ministry of Economy & Planning · 2015–2024</div>
  </div>
  <div style='display:flex;gap:14px;'>
    <div class='footer-link'><a href='https://github.com/Goda-Emad/Saudi-Tourism-Intelligence/tree/main' target='_blank'>🐙 GitHub</a></div>
    <div class='footer-link'><a href='https://www.linkedin.com/in/goda-emad/' target='_blank'>💼 LinkedIn</a></div>
  </div>
</div>
""", unsafe_allow_html=True)

