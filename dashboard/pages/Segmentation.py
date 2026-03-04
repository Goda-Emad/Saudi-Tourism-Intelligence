import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Tourist Segmentation · Saudi Tourism Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "lang" not in st.session_state:
    st.session_state.lang = "EN"
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

lang  = st.session_state.lang
theme = st.session_state.theme

T = {
    "EN": {
        "page_title":"🎯 Tourist Segmentation",
        "subtitle":"K-Means Clustering · 3 Segments · Spending & Stay Behavior · Strategic Insights",
        "built_by":"Built by","dark_mode":"🌙 Dark","light_mode":"☀️ Light","lang_toggle":"🌐 العربية",
        "pages":"Navigation","page_overview":"🏠 Overview","page_trends":"📈 Tourist Trends",
        "page_season":"📅 Seasonality","page_spend":"💰 Spending","page_overnight":"🏨 Overnight Stays",
        "page_forecast":"🔮 Forecasting","page_segment":"🎯 Segmentation","page_carbon":"🌱 Carbon Impact",
        "seg_high":"High-Value","seg_mid":"Mid-Value","seg_budget":"Budget",
        "kpi_segments":"Total Segments","kpi_silhouette":"Silhouette Score",
        "kpi_high_spend":"High-Value Avg Spend","kpi_budget_size":"Budget Segment Size",
        "kpi_algo":"Algorithm",
        "segment_overview":"Segment Overview & Profiles",
        "scatter_title":"Spending vs Length of Stay — Cluster Map",
        "radar_title":"Segment Comparison — Radar Chart",
        "size_title":"Segment Size Distribution",
        "timeline_title":"Segment Evolution Over Time",
        "strategy_title":"Business Strategy by Segment",
        "model_info":"Model Information",
        "tourists":"Tourists","avg_trip":"Avg Spend/Trip","avg_night":"Avg Spend/Night",
        "avg_los":"Avg Length of Stay","type":"Tourist Type","years":"Years Active",
        "nights":"nights","sar":"SAR","millions":"M",
        "insight_title":"Key Insights",
        "i1":"High-Value segment emerged after 2022 — Inbound tourists now stay 17+ nights",
        "i2":"Budget segment (Domestic) is 3x larger but generates 4x less revenue per trip",
        "i3":"Inbound transitioned from Mid-Value to High-Value segment post-pandemic",
        "i4":"Targeting High-Value segment = 4.4x more revenue with same tourist count",
        "strategy_high":"Focus: Luxury experiences, long-stay packages, premium hospitality",
        "strategy_mid":"Focus: Group tours, cultural experiences, mid-range accommodation",
        "strategy_budget":"Focus: Domestic destinations, family packages, affordable activities",
        "features":"Model Features","k_choice":"K Selection (Silhouette)","features_used":"Features Used",
    },
    "AR": {
        "page_title":"🎯 تقسيم السياح",
        "subtitle":"تجميع K-Means · 3 شرائح · سلوك الإنفاق والإقامة · استنتاجات استراتيجية",
        "built_by":"من تطوير","dark_mode":"🌙 داكن","light_mode":"☀️ فاتح","lang_toggle":"🌐 English",
        "pages":"التنقل","page_overview":"🏠 نظرة عامة","page_trends":"📈 اتجاهات السياحة",
        "page_season":"📅 الموسمية","page_spend":"💰 الإنفاق","page_overnight":"🏨 ليالي الإقامة",
        "page_forecast":"🔮 التوقعات","page_segment":"🎯 تقسيم السياح","page_carbon":"🌱 الأثر الكربوني",
        "seg_high":"عالي القيمة","seg_mid":"متوسط القيمة","seg_budget":"اقتصادي",
        "kpi_segments":"إجمالي الشرائح","kpi_silhouette":"نتيجة Silhouette",
        "kpi_high_spend":"إنفاق عالي القيمة","kpi_budget_size":"حجم الشريحة الاقتصادية",
        "kpi_algo":"الخوارزمية",
        "segment_overview":"نظرة عامة على الشرائح وملفاتها",
        "scatter_title":"الإنفاق مقابل مدة الإقامة — خريطة المجموعات",
        "radar_title":"مقارنة الشرائح — مخطط رادار",
        "size_title":"توزيع أحجام الشرائح",
        "timeline_title":"تطور الشرائح عبر الزمن",
        "strategy_title":"الاستراتيجية التجارية لكل شريحة",
        "model_info":"معلومات النموذج",
        "tourists":"السياح","avg_trip":"متوسط إنفاق/رحلة","avg_night":"متوسط إنفاق/ليلة",
        "avg_los":"متوسط مدة الإقامة","type":"نوع السائح","years":"سنوات النشاط",
        "nights":"ليالي","sar":"ريال","millions":"م",
        "insight_title":"أبرز الاستنتاجات",
        "i1":"شريحة عالي القيمة ظهرت بعد 2022 — الوافدون يقيمون الآن 17+ ليلة",
        "i2":"الشريحة الاقتصادية (المحلية) أكبر 3 مرات لكنها تولد إيرادات أقل 4 مرات لكل رحلة",
        "i3":"الوافدون انتقلوا من متوسط القيمة إلى عالي القيمة بعد الجائحة",
        "i4":"استهداف شريحة عالي القيمة = إيرادات أكثر 4.4x بنفس عدد السياح",
        "strategy_high":"التركيز: تجارب فاخرة، باقات إقامة طويلة، ضيافة متميزة",
        "strategy_mid":"التركيز: جولات جماعية، تجارب ثقافية، إقامة متوسطة",
        "strategy_budget":"التركيز: وجهات محلية، باقات عائلية، أنشطة بأسعار مناسبة",
        "features":"ميزات النموذج","k_choice":"اختيار K (Silhouette)","features_used":"الميزات المستخدمة",
    }
}
t = T[lang]

if theme == "dark":
    bg_main="#0D1B2A"; bg_card="#1A2B3C"; bg_card2="#162233"
    text_primary="#F0F4F8"; text_secondary="#8FA8C0"
    accent_teal="#00C9B1"; accent_gold="#F0A500"; accent_blue="#3A86FF"
    accent_green="#00E676"; accent_red="#FF5252"; accent_purple="#BB86FC"
    accent_orange="#FF9800"
    border_color="#2A3F55"; chart_bg="rgba(13,27,42,0)"; plotly_template="plotly_dark"
else:
    bg_main="#F4F7FB"; bg_card="#FFFFFF"; bg_card2="#EDF2F7"
    text_primary="#1A2B3C"; text_secondary="#4A6080"
    accent_teal="#009688"; accent_gold="#E08C00"; accent_blue="#1565C0"
    accent_green="#2E7D32"; accent_red="#C62828"; accent_purple="#6A1B9A"
    accent_orange="#E65100"
    border_color="#CBD5E0"; chart_bg="rgba(244,247,251,0)"; plotly_template="plotly_white"

dir_attr = 'rtl' if lang == "AR" else 'ltr'

# DATA — K-Means Results
segments = {
    "high": {
        "name": t["seg_high"], "color": accent_gold, "emoji": "💎",
        "tourists": 24514, "avg_trip": 5512, "avg_night": 510,
        "avg_los": 17.1, "type": "Inbound", "years": "2022–2024",
        "revenue_index": 100,
    },
    "mid": {
        "name": t["seg_mid"], "color": accent_blue, "emoji": "🌟",
        "tourists": 13232, "avg_trip": 4791, "avg_night": 430,
        "avg_los": 9.2, "type": "Inbound", "years": "2015–2021",
        "revenue_index": 87,
    },
    "budget": {
        "name": t["seg_budget"], "color": accent_teal, "emoji": "🏠",
        "tourists": 57822, "avg_trip": 1242, "avg_night": 220,
        "avg_los": 5.4, "type": "Domestic", "years": "2015–2024",
        "revenue_index": 23,
    },
}

# Silhouette scores
k_values     = [2, 3, 4, 5]
silhouettes  = [0.568, 0.630, 0.644, 0.573]

# Scatter data (simulated cluster points)
import random
random.seed(42)
scatter_data = {
    "high":   [(random.gauss(17,1.5), random.gauss(5512,300)) for _ in range(30)],
    "mid":    [(random.gauss(9,1.2),  random.gauss(4791,280)) for _ in range(25)],
    "budget": [(random.gauss(5.4,0.8),random.gauss(1242,150)) for _ in range(60)],
}

# Timeline: segment membership per year
timeline_years = list(range(2015,2025))
high_count   = [0,0,0,0,0,0,0,1,1,1]
mid_count    = [1,1,1,1,1,1,1,0,0,0]
budget_count = [1,1,1,1,1,1,1,1,1,1]

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=IBM+Plex+Mono:wght@400;600&family=Tajawal:wght@300;400;700;800&display=swap');
  html, body, [data-testid="stAppViewContainer"] {{
    background-color: {bg_main} !important;
    font-family: {'Tajawal' if lang=='AR' else 'Sora'}, sans-serif;
    direction: {dir_attr};
  }}
  [data-testid="stSidebar"] {{ background: {bg_card} !important; border-right: 1px solid {border_color}; }}
  [data-testid="stSidebar"] * {{ color: {text_primary} !important; }}
  .page-header {{
    background: linear-gradient(135deg, {bg_card} 0%, {bg_card2} 100%);
    border: 1px solid {border_color}; border-left: 4px solid {accent_teal};
    border-radius: 16px; padding: 28px 32px; margin-bottom: 24px;
    position: relative; overflow: hidden;
  }}
  .page-header::after {{ content: '🎯'; position: absolute; right: 24px; top: 50%; transform: translateY(-50%); font-size: 4rem; opacity: 0.08; }}
  .page-title {{ font-size: 1.9rem; font-weight: 800; color: {text_primary}; margin: 0 0 4px 0; }}
  .page-subtitle {{ font-size: 0.88rem; color: {accent_teal}; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; }}
  .kpi-card {{ background: {bg_card}; border: 1px solid {border_color}; border-radius: 14px; padding: 18px 14px; text-align: center; height: 100%; transition: transform 0.2s; }}
  .kpi-card:hover {{ transform: translateY(-2px); }}
  .kpi-icon {{ font-size: 1.5rem; margin-bottom: 6px; }}
  .kpi-value {{ font-size: 1.45rem; font-weight: 800; line-height: 1.1; font-family: 'IBM Plex Mono', monospace; }}
  .kpi-label {{ font-size: 0.64rem; color: {text_secondary}; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; margin-top: 4px; }}
  .kpi-sub {{ font-size: 0.73rem; font-weight: 600; margin-top: 4px; font-family: 'IBM Plex Mono', monospace; }}
  .section-title {{ font-size: 1.05rem; font-weight: 700; color: {text_primary}; margin: 24px 0 12px 0; padding-bottom: 8px; border-bottom: 2px solid {accent_teal}; }}
  .seg-card {{
    background: {bg_card}; border: 1px solid {border_color};
    border-radius: 16px; padding: 20px 18px; height: 100%;
    transition: transform 0.2s, box-shadow 0.2s;
  }}
  .seg-card:hover {{ transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.2); }}
  .seg-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 14px; }}
  .seg-emoji {{ font-size: 1.8rem; }}
  .seg-name {{ font-size: 1.05rem; font-weight: 800; }}
  .seg-row {{ display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid {border_color}; }}
  .seg-row:last-child {{ border-bottom: none; }}
  .seg-label {{ font-size: 0.75rem; color: {text_secondary}; font-weight: 500; }}
  .seg-val {{ font-size: 0.8rem; font-weight: 700; font-family: 'IBM Plex Mono', monospace; }}
  .strategy-card {{
    background: {bg_card}; border: 1px solid {border_color};
    border-radius: 14px; padding: 18px; height: 100%;
  }}
  .strategy-icon {{ font-size: 2rem; margin-bottom: 8px; }}
  .strategy-name {{ font-size: 0.95rem; font-weight: 800; margin-bottom: 8px; }}
  .strategy-text {{ font-size: 0.8rem; color: {text_secondary}; line-height: 1.5; }}
  .revenue-bar {{ height: 8px; border-radius: 4px; margin: 8px 0; }}
  .model-badge {{ display: inline-flex; align-items: center; gap: 8px; background: {bg_card2}; border: 1px solid {border_color}; border-radius: 20px; padding: 6px 14px; font-size: 0.78rem; color: {text_primary}; font-weight: 600; margin: 4px; }}
  .insight-card {{ background: {bg_card}; border: 1px solid {border_color}; border-radius: 12px; padding: 14px 16px; display: flex; align-items: flex-start; gap: 10px; margin-bottom: 10px; }}
  .insight-icon {{ font-size: 1.2rem; flex-shrink: 0; margin-top: 2px; }}
  .insight-text {{ font-size: 0.83rem; color: {text_primary}; line-height: 1.5; }}
  .footer-bar {{ background: {bg_card}; border: 1px solid {border_color}; border-radius: 12px; padding: 14px 20px; margin-top: 28px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }}
  .footer-name {{ font-size: 0.82rem; font-weight: 700; color: {accent_teal}; }}
  .footer-link {{ font-size: 0.75rem; color: {text_secondary}; }}
  .footer-link a {{ color: {accent_blue} !important; text-decoration: none; font-weight: 600; }}
</style>
""", unsafe_allow_html=True)

# SIDEBAR

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
</div>""", unsafe_allow_html=True)

# Model Badges
st.markdown(f"""
<div style='margin-bottom:16px;'>
  <span class='model-badge'>🤖 {t['kpi_algo']}: K-Means (k=3)</span>
  <span class='model-badge'>📊 Silhouette: 0.630</span>
  <span class='model-badge'>📐 Scaler: StandardScaler</span>
  <span class='model-badge'>🗂️ {t['features_used']}: 5 features</span>
  <span class='model-badge'>📅 Data: 2015–2024</span>
</div>""", unsafe_allow_html=True)

# KPIs
k1,k2,k3,k4,k5 = st.columns(5)
kpi_items = [
    (k1,"🎯",t["kpi_segments"],"3","K-Means",accent_teal),
    (k2,"📊",t["kpi_silhouette"],"0.630","k=3 selected",accent_gold),
    (k3,"💎",t["kpi_high_spend"],"SAR 5,512","/trip avg",accent_gold),
    (k4,"🏠",t["kpi_budget_size"],"57,822K","Tourists",accent_blue),
    (k5,"⚡","Revenue Ratio","4.4×","High vs Budget",accent_purple),
]
for col, icon, label, val, sub, color in kpi_items:
    with col:
        st.markdown(f"""
        <div class='kpi-card'>
          <div class='kpi-icon'>{icon}</div>
          <div class='kpi-value' style='color:{color};'>{val}</div>
          <div class='kpi-label'>{label}</div>
          <div class='kpi-sub' style='color:{text_secondary};'>{sub}</div>
        </div>""", unsafe_allow_html=True)

# SEGMENT PROFILE CARDS
st.markdown(f"<div class='section-title'>📋 {t['segment_overview']}</div>", unsafe_allow_html=True)
seg_cols = st.columns(3)
for col, (key, seg) in zip(seg_cols, segments.items()):
    with col:
        rev_pct = seg["revenue_index"]
        st.markdown(f"""
        <div class='seg-card' style='border-top: 3px solid {seg["color"]};'>
          <div class='seg-header'>
            <span class='seg-emoji'>{seg["emoji"]}</span>
            <span class='seg-name' style='color:{seg["color"]};'>{seg["name"]}</span>
          </div>
          <div style='margin-bottom:10px;'>
            <div style='font-size:0.7rem;color:{text_secondary};margin-bottom:4px;'>Revenue Index</div>
            <div class='revenue-bar' style='background:{bg_card2};'>
              <div class='revenue-bar' style='width:{rev_pct}%;background:{seg["color"]};'></div>
            </div>
            <div style='font-size:0.72rem;color:{seg["color"]};font-weight:700;'>{rev_pct}/100</div>
          </div>
          <div class='seg-row'><span class='seg-label'>{t["tourists"]}</span><span class='seg-val' style='color:{seg["color"]};'>{seg["tourists"]:,}K</span></div>
          <div class='seg-row'><span class='seg-label'>{t["avg_trip"]}</span><span class='seg-val'>SAR {seg["avg_trip"]:,}</span></div>
          <div class='seg-row'><span class='seg-label'>{t["avg_night"]}</span><span class='seg-val'>SAR {seg["avg_night"]:,}</span></div>
          <div class='seg-row'><span class='seg-label'>{t["avg_los"]}</span><span class='seg-val'>{seg["avg_los"]} {t["nights"]}</span></div>
          <div class='seg-row'><span class='seg-label'>{t["type"]}</span><span class='seg-val'>{seg["type"]}</span></div>
          <div class='seg-row'><span class='seg-label'>{t["years"]}</span><span class='seg-val'>{seg["years"]}</span></div>
        </div>""", unsafe_allow_html=True)

# CHARTS: Scatter + Radar
st.markdown(f"<div class='section-title'>📊 {t['scatter_title']}</div>", unsafe_allow_html=True)
scatter_col, radar_col = st.columns([3, 2])

with scatter_col:
    fig_scatter = go.Figure()
    seg_colors_map = {"high": accent_gold, "mid": accent_blue, "budget": accent_teal}
    seg_names_map  = {"high": t["seg_high"], "mid": t["seg_mid"], "budget": t["seg_budget"]}
    for key, points in scatter_data.items():
        x_vals = [p[0] for p in points]
        y_vals = [p[1] for p in points]
        fig_scatter.add_trace(go.Scatter(
            x=x_vals, y=y_vals,
            mode='markers',
            name=seg_names_map[key],
            marker=dict(color=seg_colors_map[key], size=10, opacity=0.75,
                        line=dict(color=bg_card, width=1.5)),
            hovertemplate=f"<b>{seg_names_map[key]}</b><br>LOS: %{{x:.1f}} nights<br>Spend: SAR %{{y:,.0f}}<extra></extra>"
        ))
    # Centroid markers
    centroids = [
        (17.1, 5512, accent_gold, t["seg_high"]),
        (9.2,  4791, accent_blue, t["seg_mid"]),
        (5.4,  1242, accent_teal, t["seg_budget"]),
    ]
    for cx, cy, cc, cn in centroids:
        fig_scatter.add_trace(go.Scatter(
            x=[cx], y=[cy], mode='markers+text',
            marker=dict(color=cc, size=18, symbol='star',
                        line=dict(color=bg_card, width=2)),
            text=[f"⭐"], textposition='top center',
            showlegend=False,
            hovertemplate=f"<b>{cn} Centroid</b><br>LOS: {cx} nights<br>Spend: SAR {cy:,}<extra></extra>"
        ))
    fig_scatter.update_layout(
        template=plotly_template, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=360, margin=dict(l=10,r=10,t=20,b=10),
        legend=dict(orientation="h", y=-0.12, font=dict(size=11)),
        xaxis=dict(showgrid=True, gridcolor=border_color, tickfont=dict(size=10),
                   title=f"{t['avg_los']} (Nights)"),
        yaxis=dict(showgrid=True, gridcolor=border_color, tickfont=dict(size=10),
                   title=f"{t['avg_trip']} (SAR)", tickprefix="SAR "),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})

with radar_col:
    st.markdown(f"<div style='font-size:0.9rem;font-weight:700;color:{text_primary};margin-bottom:8px;'>🎯 {t['radar_title']}</div>", unsafe_allow_html=True)
    categories = ["Volume","Spend/Trip","Spend/Night","LOS","Revenue Index"]
    high_vals   = [100*24514/57822, 100, 100, 100*17.1/17.1, 100]
    mid_vals    = [100*13232/57822, 87,  84,  100*9.2/17.1,  87]
    budget_vals = [100,             23,  43,  100*5.4/17.1,  23]

    fig_radar = go.Figure()
    for name, vals, color in [
        (t["seg_high"],   high_vals,   accent_gold),
        (t["seg_mid"],    mid_vals,    accent_blue),
        (t["seg_budget"], budget_vals, accent_teal),
    ]:
        fig_radar.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=categories + [categories[0]],
            fill='toself', name=name,
            line_color=color, fillcolor=f"{color}25"
        ))
    fig_radar.update_layout(
        template=plotly_template, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=360, margin=dict(l=30,r=30,t=10,b=10),
        polar=dict(
            bgcolor=bg_card2,
            radialaxis=dict(showticklabels=False, gridcolor=border_color),
            angularaxis=dict(tickfont=dict(size=10, color=text_primary), gridcolor=border_color)
        ),
        legend=dict(orientation="h", y=-0.1, font=dict(size=10)),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

# CHART: Size + Timeline
size_col, timeline_col = st.columns([1, 2])

with size_col:
    st.markdown(f"<div class='section-title'>📏 {t['size_title']}</div>", unsafe_allow_html=True)
    fig_size = go.Figure(go.Pie(
        labels=[t["seg_high"], t["seg_mid"], t["seg_budget"]],
        values=[24514, 13232, 57822],
        hole=0.55,
        marker=dict(colors=[accent_gold, accent_blue, accent_teal],
                    line=dict(color=bg_main, width=2)),
        textfont=dict(size=10),
        hovertemplate="<b>%{label}</b><br>%{value:,}K tourists<br>%{percent}<extra></extra>"
    ))
    fig_size.add_annotation(text="<b>95.6M</b><br>Total", x=0.5, y=0.5,
        showarrow=False, font=dict(size=12, color=text_primary))
    fig_size.update_layout(
        template=plotly_template, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=280, margin=dict(l=10,r=10,t=10,b=10),
        showlegend=True, legend=dict(orientation="v", font=dict(size=10)),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_size, use_container_width=True, config={"displayModeBar": False})

with timeline_col:
    st.markdown(f"<div class='section-title'>📅 {t['timeline_title']}</div>", unsafe_allow_html=True)
    fig_tl = go.Figure()
    inbound_total = [17990,18040,16110,15330,17530,4140,3480,16640,27180,29730]
    fig_tl.add_trace(go.Bar(x=timeline_years,
        y=[v*h for v,h in zip(inbound_total, mid_vals[:len(inbound_total)] if False else [1 if x else 0 for x in mid_count])],
        name=t["seg_mid"], marker_color=accent_blue, opacity=0.85))
    fig_tl.add_trace(go.Bar(x=timeline_years,
        y=[v*h for v,h in zip(inbound_total, high_count)],
        name=t["seg_high"], marker_color=accent_gold, opacity=0.88))
    domestic_total = [46450,45040,43820,43260,47810,42110,63830,77840,81920,86160]
    fig_tl.add_trace(go.Bar(x=timeline_years, y=domestic_total,
        name=t["seg_budget"], marker_color=accent_teal, opacity=0.85))
    fig_tl.add_annotation(x=2022, y=17000,
        text="Transition:\nMid → High Value",
        showarrow=True, arrowhead=2,
        font=dict(size=9, color=accent_gold), arrowcolor=accent_gold, ay=-50)
    fig_tl.update_layout(
        template=plotly_template, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=280, barmode='stack', margin=dict(l=10,r=10,t=20,b=10),
        legend=dict(orientation="h", y=-0.18, font=dict(size=10)),
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor=border_color, tickfont=dict(size=10), title="K Tourists"),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_tl, use_container_width=True, config={"displayModeBar": False})

# SILHOUETTE CHART
sil_col, strategy_col = st.columns([1, 2])

with sil_col:
    st.markdown(f"<div class='section-title'>📐 {t['k_choice']}</div>", unsafe_allow_html=True)
    sil_colors = [accent_teal if k!=3 else accent_gold for k in k_values]
    fig_sil = go.Figure(go.Bar(
        x=[f"k={k}" for k in k_values], y=silhouettes,
        marker_color=sil_colors, opacity=0.88,
        text=[f"{s:.3f}" for s in silhouettes],
        textposition='outside', textfont=dict(size=11, color=text_primary)
    ))
    fig_sil.add_annotation(x="k=3", y=0.630,
        text="✅ Selected", showarrow=False,
        font=dict(size=10, color=accent_gold), yshift=28)
    fig_sil.update_layout(
        template=plotly_template, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=260, margin=dict(l=10,r=10,t=20,b=10),
        xaxis=dict(showgrid=False, tickfont=dict(size=12)),
        yaxis=dict(showgrid=True, gridcolor=border_color, tickfont=dict(size=10),
                   title="Silhouette Score", range=[0.5, 0.7]),
        font=dict(color=text_primary), showlegend=False
    )
    st.plotly_chart(fig_sil, use_container_width=True, config={"displayModeBar": False})

with strategy_col:
    st.markdown(f"<div class='section-title'>🚀 {t['strategy_title']}</div>", unsafe_allow_html=True)
    strat_cols = st.columns(3)
    strategies = [
        (t["seg_high"],   "💎", accent_gold,   t["strategy_high"],   "SAR 5,512/trip", "+85% Revenue"),
        (t["seg_mid"],    "🌟", accent_blue,   t["strategy_mid"],    "SAR 4,791/trip", "+48% Revenue"),
        (t["seg_budget"], "🏠", accent_teal,   t["strategy_budget"], "SAR 1,242/trip", "Volume Play"),
    ]
    for col, (name, emoji, color, strategy, spend, tag) in zip(strat_cols, strategies):
        with col:
            st.markdown(f"""
            <div class='strategy-card' style='border-top:3px solid {color};'>
              <div class='strategy-icon'>{emoji}</div>
              <div class='strategy-name' style='color:{color};'>{name}</div>
              <div style='display:flex;gap:6px;margin-bottom:10px;flex-wrap:wrap;'>
                <span style='background:{color}22;border:1px solid {color}44;border-radius:12px;padding:3px 8px;font-size:0.7rem;color:{color};font-weight:700;'>{spend}</span>
                <span style='background:{bg_card2};border:1px solid {border_color};border-radius:12px;padding:3px 8px;font-size:0.7rem;color:{text_secondary};font-weight:600;'>{tag}</span>
              </div>
              <div class='strategy-text'>{strategy}</div>
            </div>""", unsafe_allow_html=True)

# KEY INSIGHTS
st.markdown(f"<div class='section-title'>💡 {t['insight_title']}</div>", unsafe_allow_html=True)
insights = [
    ("💎", t["i1"], accent_gold),
    ("🏠", t["i2"], accent_teal),
    ("🔄", t["i3"], accent_blue),
    ("💰", t["i4"], accent_purple),
]
ins_cols = st.columns(2)
for i, (icon, text_val, color) in enumerate(insights):
    with ins_cols[i % 2]:
        st.markdown(f"""
        <div class='insight-card' style='border-left:3px solid {color};'>
          <div class='insight-icon'>{icon}</div>
          <div class='insight-text'>{text_val}</div>
        </div>""", unsafe_allow_html=True)

# FOOTER
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
</div>""", unsafe_allow_html=True)
