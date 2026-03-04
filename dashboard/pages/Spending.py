import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Spending Analysis · Saudi Tourism Intelligence",
    page_icon="💰",
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
        "page_title":"💰 Spending Analysis",
        "subtitle":"Inbound vs Domestic · Per Trip · Per Night · Expenditure by Purpose",
        "built_by":"Built by","dark_mode":"🌙 Dark","light_mode":"☀️ Light","lang_toggle":"🌐 العربية",
        "pages":"Navigation","page_overview":"🏠 Overview","page_trends":"📈 Tourist Trends",
        "page_season":"📅 Seasonality","page_spend":"💰 Spending","page_overnight":"🏨 Overnight Stays",
        "page_forecast":"🔮 Forecasting","page_segment":"🎯 Segmentation","page_carbon":"🌱 Carbon Impact",
        "avg_trip_in":"Avg Spend/Trip (Inbound)","avg_trip_dom":"Avg Spend/Trip (Domestic)",
        "avg_night_in":"Avg Spend/Night (Inbound)","avg_night_dom":"Avg Spend/Night (Domestic)",
        "spend_ratio":"Inbound vs Domestic Ratio",
        "trip_trend":"Average Spending per Trip — Trend","night_trend":"Average Spending per Night — Trend",
        "expenditure":"Total Expenditure by Purpose (Billions SAR)","monthly_spend":"Monthly Spending Pattern",
        "spend_compare":"Spending Comparison: Key Milestones","best_month":"Best Spending Month",
        "inbound":"Inbound","domestic":"Domestic","religious":"Religious","leisure":"Leisure",
        "business":"Business","vfr":"VFR","other":"Other","year":"Year","sar":"SAR",
        "billions":"Billions SAR","filter_type":"Tourist Type","all_types":"All",
        "insight_title":"Key Insights",
        "i1":"Inbound tourists spend 4x more than Domestic per trip (SAR 5,007 vs SAR 1,242)",
        "i2":"Religious purpose generates the highest total expenditure — 391 Billion SAR (2014-2022)",
        "i3":"Best single month: August 2019 — SAR 13,053 per Inbound trip",
        "i4":"Inbound spending collapsed -35% in 2020 (COVID) then surged to SAR 5,907 in 2022",
        "growth_label":"Growth 2015 to 2024","covid_low":"COVID Low (2020)","peak_spend":"Peak Spending",
    },
    "AR": {
        "page_title":"💰 تحليل الإنفاق",
        "subtitle":"وافد مقابل محلي · لكل رحلة · لكل ليلة · الإنفاق حسب الغرض",
        "built_by":"من تطوير","dark_mode":"🌙 داكن","light_mode":"☀️ فاتح","lang_toggle":"🌐 English",
        "pages":"التنقل","page_overview":"🏠 نظرة عامة","page_trends":"📈 اتجاهات السياحة",
        "page_season":"📅 الموسمية","page_spend":"💰 الإنفاق","page_overnight":"🏨 ليالي الإقامة",
        "page_forecast":"🔮 التوقعات","page_segment":"🎯 تقسيم السياح","page_carbon":"🌱 الأثر الكربوني",
        "avg_trip_in":"متوسط إنفاق/رحلة (وافد)","avg_trip_dom":"متوسط إنفاق/رحلة (محلي)",
        "avg_night_in":"متوسط إنفاق/ليلة (وافد)","avg_night_dom":"متوسط إنفاق/ليلة (محلي)",
        "spend_ratio":"نسبة الوافد للمحلي",
        "trip_trend":"متوسط الإنفاق لكل رحلة — الاتجاه","night_trend":"متوسط الإنفاق لكل ليلة — الاتجاه",
        "expenditure":"إجمالي الإنفاق حسب الغرض (مليار ريال)","monthly_spend":"النمط الشهري للإنفاق",
        "spend_compare":"مقارنة الإنفاق: المحطات الرئيسية","best_month":"أفضل شهر إنفاقاً",
        "inbound":"وافد","domestic":"محلي","religious":"ديني","leisure":"ترفيه",
        "business":"أعمال","vfr":"زيارة أهل","other":"أخرى","year":"السنة","sar":"ريال",
        "billions":"مليار ريال","filter_type":"نوع السائح","all_types":"الكل",
        "insight_title":"أبرز الاستنتاجات",
        "i1":"الوافدون ينفقون 4 أضعاف المحليين لكل رحلة (5,007 مقابل 1,242 ريال)",
        "i2":"الغرض الديني يولد أعلى إنفاق إجمالي — 391 مليار ريال (2014-2022)",
        "i3":"أفضل شهر: أغسطس 2019 — 13,053 ريال لكل رحلة وافدة",
        "i4":"إنفاق الوافدين انهار -35% في 2020 ثم قفز لـ 5,907 ريال في 2022",
        "growth_label":"نمو 2015 إلى 2024","covid_low":"أدنى كوفيد (2020)","peak_spend":"ذروة الإنفاق",
    }
}
t = T[lang]

if theme == "dark":
    bg_main="#0D1B2A"; bg_card="#1A2B3C"; bg_card2="#162233"
    text_primary="#F0F4F8"; text_secondary="#8FA8C0"
    accent_teal="#00C9B1"; accent_gold="#F0A500"; accent_blue="#3A86FF"
    accent_green="#00E676"; accent_red="#FF5252"; accent_purple="#BB86FC"
    border_color="#2A3F55"; chart_bg="rgba(13,27,42,0)"; plotly_template="plotly_dark"
else:
    bg_main="#F4F7FB"; bg_card="#FFFFFF"; bg_card2="#EDF2F7"
    text_primary="#1A2B3C"; text_secondary="#4A6080"
    accent_teal="#009688"; accent_gold="#E08C00"; accent_blue="#1565C0"
    accent_green="#2E7D32"; accent_red="#C62828"; accent_purple="#6A1B9A"
    border_color="#CBD5E0"; chart_bg="rgba(244,247,251,0)"; plotly_template="plotly_white"

dir_attr = 'rtl' if lang == "AR" else 'ltr'

years = list(range(2015, 2025))
inbound_trip  = [4598,4923,5524,5538,5304,3469,4181,5907,5007,5622]
domestic_trip = [1043,1235,1052,1114,1284,1029,1586,1352,1390,1336]
inbound_night  = [392,420,435,448,436,318,398,510,430,482]
domestic_night = [190,204,195,198,209,182,241,218,214,234]
months_en = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
months_ar = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
months_lbl = months_ar if lang == "AR" else months_en
monthly_inbound_spend  = [5200,5800,6200,5100,4800,5400,6800,7200,5600,4900,5300,6100]
monthly_domestic_spend = [1100,1050,1150,1200,1300,1400,1600,1550,1200,1100,1050,1250]
exp_purposes = ["Religious","Business","VFR","Leisure","Other"]
exp_inbound  = [391.20,123.60,71.10,34.52,29.09]
exp_domestic = [82.40,65.30,95.20,45.60,83.50]
exp_labels   = [t["religious"],t["business"],t["vfr"],t["leisure"],t["other"]]

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
    border: 1px solid {border_color}; border-left: 4px solid {accent_gold};
    border-radius: 16px; padding: 28px 32px; margin-bottom: 24px;
    position: relative; overflow: hidden;
  }}
  .page-header::after {{
    content: '💰'; position: absolute; right: 24px; top: 50%;
    transform: translateY(-50%); font-size: 4rem; opacity: 0.08;
  }}
  .page-title {{ font-size: 1.9rem; font-weight: 800; color: {text_primary}; margin: 0 0 4px 0; }}
  .page-subtitle {{ font-size: 0.88rem; color: {accent_gold}; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; }}
  .kpi-card {{
    background: {bg_card}; border: 1px solid {border_color}; border-radius: 14px;
    padding: 18px 14px; text-align: center; height: 100%; transition: transform 0.2s;
  }}
  .kpi-card:hover {{ transform: translateY(-2px); }}
  .kpi-icon {{ font-size: 1.5rem; margin-bottom: 6px; }}
  .kpi-value {{ font-size: 1.45rem; font-weight: 800; line-height: 1.1; font-family: 'IBM Plex Mono', monospace; }}
  .kpi-label {{ font-size: 0.66rem; color: {text_secondary}; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; margin-top: 4px; }}
  .kpi-sub {{ font-size: 0.74rem; font-weight: 600; margin-top: 4px; font-family: 'IBM Plex Mono', monospace; }}
  .section-title {{
    font-size: 1.05rem; font-weight: 700; color: {text_primary};
    margin: 24px 0 12px 0; padding-bottom: 8px; border-bottom: 2px solid {accent_gold};
  }}
  .compare-card {{ background: {bg_card}; border: 1px solid {border_color}; border-radius: 14px; padding: 20px; height: 100%; }}
  .compare-title {{ font-size: 0.78rem; font-weight: 700; color: {text_secondary}; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 16px; }}
  .compare-row {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid {border_color}; }}
  .compare-row:last-child {{ border-bottom: none; }}
  .compare-label {{ font-size: 0.82rem; color: {text_primary}; font-weight: 500; }}
  .compare-val {{ font-size: 0.85rem; font-weight: 700; font-family: 'IBM Plex Mono', monospace; }}
  .insight-card {{
    background: {bg_card}; border: 1px solid {border_color}; border-radius: 12px;
    padding: 14px 16px; display: flex; align-items: flex-start; gap: 10px; margin-bottom: 10px;
  }}
  .insight-icon {{ font-size: 1.2rem; flex-shrink: 0; margin-top: 2px; }}
  .insight-text {{ font-size: 0.83rem; color: {text_primary}; line-height: 1.5; }}
  .footer-bar {{
    background: {bg_card}; border: 1px solid {border_color}; border-radius: 12px;
    padding: 14px 20px; margin-top: 28px; display: flex;
    justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;
  }}
  .footer-name {{ font-size: 0.82rem; font-weight: 700; color: {accent_teal}; }}
  .footer-link {{ font-size: 0.75rem; color: {text_secondary}; }}
  .footer-link a {{ color: {accent_blue} !important; text-decoration: none; font-weight: 600; }}
</style>
""", unsafe_allow_html=True)


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

k1,k2,k3,k4,k5 = st.columns(5)
kpi_items = [
    (k1,"✈️💰",t["avg_trip_in"],"SAR 5,007","All-years avg",accent_gold),
    (k2,"🏠💰",t["avg_trip_dom"],"SAR 1,242","All-years avg",accent_teal),
    (k3,"🌙💰",t["avg_night_in"],"SAR 482","Per night",accent_blue),
    (k4,"🏡💰",t["avg_night_dom"],"SAR 234","Per night",accent_purple),
    (k5,"⚖️",t["spend_ratio"],"4.0x","Inbound/Domestic",accent_red),
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

st.markdown(f"<div class='section-title'>📈 {t['trip_trend']}</div>", unsafe_allow_html=True)

y_s, y_e = year_range
idx_s = years.index(y_s); idx_e = years.index(y_e)+1
f_years = years[idx_s:idx_e]

trip_col, night_col = st.columns(2)

with trip_col:
    fig_trip = go.Figure()
    if tourist_filter in [t["all_types"], t["inbound"]]:
        fig_trip.add_trace(go.Scatter(
            x=f_years, y=inbound_trip[idx_s:idx_e], name=t["inbound"],
            line=dict(color=accent_gold, width=2.5),
            fill='tozeroy', fillcolor=f"{accent_gold}15",
            marker=dict(size=8, color=accent_gold, line=dict(color=bg_card, width=2))
        ))
    if tourist_filter in [t["all_types"], t["domestic"]]:
        fig_trip.add_trace(go.Scatter(
            x=f_years, y=domestic_trip[idx_s:idx_e], name=t["domestic"],
            line=dict(color=accent_teal, width=2.5),
            fill='tozeroy', fillcolor=f"{accent_teal}15",
            marker=dict(size=8, color=accent_teal, line=dict(color=bg_card, width=2))
        ))
    fig_trip.add_vrect(x0=2019.5, x1=2021.5, fillcolor=accent_red, opacity=0.07,
        annotation_text="COVID", annotation=dict(font_color=accent_red, font_size=10))
    fig_trip.update_layout(
        template=plotly_template, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=300, margin=dict(l=10,r=10,t=20,b=10),
        legend=dict(orientation="h", y=-0.15, font=dict(size=10)),
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor=border_color, tickfont=dict(size=10),
                   title=t["sar"], tickprefix="SAR "),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_trip, use_container_width=True, config={"displayModeBar": False})

with night_col:
    st.markdown(f"<div style='font-size:0.9rem;font-weight:700;color:{text_primary};margin-bottom:8px;'>🌙 {t['night_trend']}</div>", unsafe_allow_html=True)
    fig_night = go.Figure()
    if tourist_filter in [t["all_types"], t["inbound"]]:
        fig_night.add_trace(go.Bar(x=f_years, y=inbound_night[idx_s:idx_e],
            name=t["inbound"], marker_color=accent_blue, opacity=0.85))
    if tourist_filter in [t["all_types"], t["domestic"]]:
        fig_night.add_trace(go.Bar(x=f_years, y=domestic_night[idx_s:idx_e],
            name=t["domestic"], marker_color=accent_teal, opacity=0.85))
    fig_night.update_layout(
        template=plotly_template, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=300, barmode='group', margin=dict(l=10,r=10,t=10,b=10),
        legend=dict(orientation="h", y=-0.15, font=dict(size=10)),
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor=border_color, tickfont=dict(size=10),
                   title=t["sar"], tickprefix="SAR "),
        font=dict(color=text_primary), bargap=0.25
    )
    st.plotly_chart(fig_night, use_container_width=True, config={"displayModeBar": False})

st.markdown(f"<div class='section-title'>🏆 {t['expenditure']}</div>", unsafe_allow_html=True)
exp_col, monthly_col = st.columns([3, 2])

with exp_col:
    exp_colors = [accent_gold, accent_blue, accent_purple, accent_teal, text_secondary]
    fig_exp = go.Figure()
    fig_exp.add_trace(go.Bar(x=exp_labels, y=exp_inbound, name=t["inbound"],
        marker_color=exp_colors,
        text=[f"{v:.1f}B" for v in exp_inbound],
        textposition='outside', textfont=dict(size=10, color=text_primary)))
    fig_exp.add_trace(go.Bar(x=exp_labels, y=exp_domestic, name=t["domestic"],
        marker_color=[f"{c}88" for c in exp_colors],
        text=[f"{v:.1f}B" for v in exp_domestic],
        textposition='outside', textfont=dict(size=10, color=text_primary)))
    fig_exp.update_layout(
        template=plotly_template, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=320, barmode='group', margin=dict(l=10,r=10,t=30,b=10),
        legend=dict(orientation="h", y=-0.15, font=dict(size=11)),
        xaxis=dict(showgrid=False, tickfont=dict(size=11)),
        yaxis=dict(showgrid=True, gridcolor=border_color, tickfont=dict(size=10), title=t["billions"]),
        font=dict(color=text_primary), bargap=0.2
    )
    st.plotly_chart(fig_exp, use_container_width=True, config={"displayModeBar": False})

with monthly_col:
    st.markdown(f"<div style='font-size:0.9rem;font-weight:700;color:{text_primary};margin-bottom:8px;'>📅 {t['monthly_spend']}</div>", unsafe_allow_html=True)
    fig_monthly = go.Figure()
    if tourist_filter in [t["all_types"], t["inbound"]]:
        fig_monthly.add_trace(go.Scatter(x=months_lbl, y=monthly_inbound_spend, name=t["inbound"],
            line=dict(color=accent_gold, width=2.5), fill='tozeroy', fillcolor=f"{accent_gold}18",
            marker=dict(size=7)))
    if tourist_filter in [t["all_types"], t["domestic"]]:
        fig_monthly.add_trace(go.Scatter(x=months_lbl, y=monthly_domestic_spend, name=t["domestic"],
            line=dict(color=accent_teal, width=2.5), fill='tozeroy', fillcolor=f"{accent_teal}18",
            marker=dict(size=7)))
    fig_monthly.update_layout(
        template=plotly_template, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=320, margin=dict(l=10,r=10,t=10,b=10),
        legend=dict(orientation="h", y=-0.18, font=dict(size=10)),
        xaxis=dict(showgrid=False, tickfont=dict(size=9), tickangle=45),
        yaxis=dict(showgrid=True, gridcolor=border_color, tickfont=dict(size=10),
                   title=t["sar"], tickprefix="SAR "),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_monthly, use_container_width=True, config={"displayModeBar": False})

st.markdown(f"<div class='section-title'>⚖️ {t['spend_compare']}</div>", unsafe_allow_html=True)
cmp_col1, cmp_col2, cmp_col3 = st.columns(3)

with cmp_col1:
    st.markdown(f"""
    <div class='compare-card'>
      <div class='compare-title'>✈️ {t['inbound']} — {t['avg_trip_in']}</div>
      <div class='compare-row'><span class='compare-label'>2015</span><span class='compare-val' style='color:{text_secondary};'>SAR 4,598</span></div>
      <div class='compare-row'><span class='compare-label'>{t['covid_low']}</span><span class='compare-val' style='color:{accent_red};'>SAR 3,469</span></div>
      <div class='compare-row'><span class='compare-label'>{t['peak_spend']}</span><span class='compare-val' style='color:{accent_gold};'>SAR 5,907</span></div>
      <div class='compare-row'><span class='compare-label'>2024</span><span class='compare-val' style='color:{accent_teal};'>SAR 5,622</span></div>
      <div class='compare-row'><span class='compare-label'>{t['growth_label']}</span><span class='compare-val' style='color:{accent_green};'>+22.3%</span></div>
    </div>""", unsafe_allow_html=True)

with cmp_col2:
    st.markdown(f"""
    <div class='compare-card'>
      <div class='compare-title'>🏠 {t['domestic']} — {t['avg_trip_dom']}</div>
      <div class='compare-row'><span class='compare-label'>2015</span><span class='compare-val' style='color:{text_secondary};'>SAR 1,043</span></div>
      <div class='compare-row'><span class='compare-label'>{t['covid_low']}</span><span class='compare-val' style='color:{accent_red};'>SAR 1,029</span></div>
      <div class='compare-row'><span class='compare-label'>{t['peak_spend']}</span><span class='compare-val' style='color:{accent_gold};'>SAR 1,586</span></div>
      <div class='compare-row'><span class='compare-label'>2024</span><span class='compare-val' style='color:{accent_teal};'>SAR 1,336</span></div>
      <div class='compare-row'><span class='compare-label'>{t['growth_label']}</span><span class='compare-val' style='color:{accent_green};'>+28.1%</span></div>
    </div>""", unsafe_allow_html=True)

with cmp_col3:
    fig_donut = go.Figure(go.Pie(
        labels=exp_labels, values=exp_inbound, hole=0.60,
        marker=dict(colors=[accent_gold,accent_blue,accent_purple,accent_teal,text_secondary],
                    line=dict(color=bg_main, width=2)),
        textfont=dict(size=10),
        hovertemplate="<b>%{label}</b><br>%{value:.1f}B SAR<extra></extra>"
    ))
    fig_donut.add_annotation(text=f"<b>649B</b><br>Total", x=0.5, y=0.5,
        showarrow=False, font=dict(size=12, color=text_primary))
    fig_donut.update_layout(
        template=plotly_template, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=280, margin=dict(l=10,r=10,t=30,b=10),
        showlegend=True, legend=dict(orientation="v", font=dict(size=9), x=1.0),
        font=dict(color=text_primary),
        title=dict(text=f"Inbound Expenditure Split", font=dict(size=11), x=0.5)
    )
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

st.markdown(f"<div class='section-title'>💡 {t['insight_title']}</div>", unsafe_allow_html=True)
insights = [
    ("💰", t["i1"], accent_gold),
    ("🕌", t["i2"], accent_purple),
    ("🏆", t["i3"], accent_blue),
    ("📉", t["i4"], accent_red),
]
ins_cols = st.columns(2)
for i, (icon, text_val, color) in enumerate(insights):
    with ins_cols[i % 2]:
        st.markdown(f"""
        <div class='insight-card' style='border-left:3px solid {color};'>
          <div class='insight-icon'>{icon}</div>
          <div class='insight-text'>{text_val}</div>
        </div>""", unsafe_allow_html=True)

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
