import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Forecasting · Saudi Tourism Intelligence",
    page_icon="🔮",
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
        "page_title":"🔮 Demand Forecasting 2025–2026",
        "subtitle":"Prophet Model · Monthly Predictions · Confidence Intervals · Vision 2030 Progress",
        "built_by":"Built by","dark_mode":"🌙 Dark","light_mode":"☀️ Light","lang_toggle":"🌐 العربية",
        "pages":"Navigation","page_overview":"🏠 Overview","page_trends":"📈 Tourist Trends",
        "page_season":"📅 Seasonality","page_spend":"💰 Spending","page_overnight":"🏨 Overnight Stays",
        "page_forecast":"🔮 Forecasting","page_segment":"🎯 Segmentation","page_carbon":"🌱 Carbon Impact",
        "kpi_peak25":"Peak Month 2025","kpi_peak26":"Peak Month 2026",
        "kpi_total25":"Total Forecast 2025","kpi_total26":"Total Forecast 2026",
        "kpi_yoy":"YoY Growth","model":"Model","accuracy":"Accuracy",
        "forecast_chart":"Monthly Forecast 2025–2026 with Confidence Intervals",
        "historical":"Historical vs Forecast","vision2030":"Vision 2030 Progress Tracker",
        "monthly_table":"Monthly Forecast Table","trend_decomp":"Seasonal Pattern (Historical)",
        "inbound":"Inbound","domestic":"Domestic","total":"Total",
        "forecast":"Forecast","upper":"Upper Bound","lower":"Lower Bound",
        "historical_lbl":"Historical","target":"Target","actual":"Actual",
        "month":"Month","tourists_k":"Tourists (K)","tourists_m":"Tourists (M)",
        "filter_year":"Forecast Year","both_years":"2025 & 2026",
        "insight_title":"Key Insights",
        "i1":"January 2026 is the predicted peak at 13,680K tourists — highest ever forecasted",
        "i2":"2026 forecast shows +11.1% growth over 2025 — aligned with Vision 2030 trajectory",
        "i3":"Seasonal pattern is consistent: Jan & Jul peaks, May low — same as historical",
        "i4":"At current growth rate, Saudi Arabia will reach 150M tourist target by 2029",
        "vision_note":"Vision 2030 Target: 150 Million Tourists",
        "progress":"Progress to Target",
        "yr2024":"2024 Actual","yr2025":"2025 Forecast","yr2026":"2026 Forecast","yr2030":"2030 Target",
    },
    "AR": {
        "page_title":"🔮 توقعات الطلب 2025–2026",
        "subtitle":"نموذج Prophet · توقعات شهرية · فترات الثقة · تقدم رؤية 2030",
        "built_by":"من تطوير","dark_mode":"🌙 داكن","light_mode":"☀️ فاتح","lang_toggle":"🌐 English",
        "pages":"التنقل","page_overview":"🏠 نظرة عامة","page_trends":"📈 اتجاهات السياحة",
        "page_season":"📅 الموسمية","page_spend":"💰 الإنفاق","page_overnight":"🏨 ليالي الإقامة",
        "page_forecast":"🔮 التوقعات","page_segment":"🎯 تقسيم السياح","page_carbon":"🌱 الأثر الكربوني",
        "kpi_peak25":"ذروة 2025","kpi_peak26":"ذروة 2026",
        "kpi_total25":"إجمالي توقعات 2025","kpi_total26":"إجمالي توقعات 2026",
        "kpi_yoy":"نمو سنوي","model":"النموذج","accuracy":"الدقة",
        "forecast_chart":"التوقعات الشهرية 2025–2026 مع فترات الثقة",
        "historical":"التاريخي مقابل التوقع","vision2030":"متتبع تقدم رؤية 2030",
        "monthly_table":"جدول التوقعات الشهرية","trend_decomp":"النمط الموسمي (التاريخي)",
        "inbound":"وافد","domestic":"محلي","total":"إجمالي",
        "forecast":"توقع","upper":"الحد الأعلى","lower":"الحد الأدنى",
        "historical_lbl":"تاريخي","target":"الهدف","actual":"الفعلي",
        "month":"الشهر","tourists_k":"السياح (ألف)","tourists_m":"السياح (مليون)",
        "filter_year":"سنة التوقع","both_years":"2025 و 2026",
        "insight_title":"أبرز الاستنتاجات",
        "i1":"يناير 2026 هو الذروة المتوقعة بـ 13,680K سائح — أعلى توقع في التاريخ",
        "i2":"توقعات 2026 تظهر +11.1% نمواً عن 2025 — متوافق مع مسار رؤية 2030",
        "i3":"النمط الموسمي ثابت: ذروة يناير ويوليو، انخفاض مايو — كالتاريخي",
        "i4":"بالمعدل الحالي، ستصل السعودية لهدف 150M سائح بحلول 2029",
        "vision_note":"هدف رؤية 2030: 150 مليون سائح",
        "progress":"التقدم نحو الهدف",
        "yr2024":"فعلي 2024","yr2025":"توقع 2025","yr2026":"توقع 2026","yr2030":"هدف 2030",
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

# DATA
months_en = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
months_ar = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
months_lbl = months_ar if lang=="AR" else months_en

forecast_2025 = [12307,10628,10812,10074,8964,11238,11832,11124,9846,9561,11710,10798]
forecast_2026 = [13680,11797,11963,11180,9927,12458,13063,12290,10831,10550,12905,11897]
lower_2025    = [10664,9022,9146,8509,7237,9536,10251,9507,8016,7914,10088,9203]
upper_2025    = [13969,12301,12422,11662,10622,12807,13522,12770,11391,11131,13380,12477]
lower_2026    = [11938,10188,10328,9532,8349,10700,11361,10799,9094,8863,11223,10321]
upper_2026    = [15330,13355,13516,12805,11695,14131,14719,13899,12415,12190,14546,13537]

historical_years = list(range(2015, 2025))
historical_total = [64.4,63.1,59.9,58.6,65.3,46.2,67.3,94.5,109.1,115.9]
total_2025 = sum(forecast_2025)/1000
total_2026 = sum(forecast_2026)/1000

vision_data = {
    "years": [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030],
    "actual": [65.3, 46.2, 67.3, 94.5, 109.1, 115.9, None, None, None, None, None, None],
    "forecast": [None, None, None, None, None, 115.9, total_2025, total_2026, 125.0, 135.0, 145.0, 150.0],
    "target": [None]*11 + [150.0],
}

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
    border: 1px solid {border_color}; border-left: 4px solid {accent_purple};
    border-radius: 16px; padding: 28px 32px; margin-bottom: 24px;
    position: relative; overflow: hidden;
  }}
  .page-header::after {{ content: '🔮'; position: absolute; right: 24px; top: 50%; transform: translateY(-50%); font-size: 4rem; opacity: 0.08; }}
  .page-title {{ font-size: 1.9rem; font-weight: 800; color: {text_primary}; margin: 0 0 4px 0; }}
  .page-subtitle {{ font-size: 0.88rem; color: {accent_purple}; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; }}
  .kpi-card {{ background: {bg_card}; border: 1px solid {border_color}; border-radius: 14px; padding: 18px 14px; text-align: center; height: 100%; transition: transform 0.2s; }}
  .kpi-card:hover {{ transform: translateY(-2px); }}
  .kpi-icon {{ font-size: 1.5rem; margin-bottom: 6px; }}
  .kpi-value {{ font-size: 1.45rem; font-weight: 800; line-height: 1.1; font-family: 'IBM Plex Mono', monospace; }}
  .kpi-label {{ font-size: 0.64rem; color: {text_secondary}; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; margin-top: 4px; }}
  .kpi-sub {{ font-size: 0.73rem; font-weight: 600; margin-top: 4px; font-family: 'IBM Plex Mono', monospace; }}
  .section-title {{ font-size: 1.05rem; font-weight: 700; color: {text_primary}; margin: 24px 0 12px 0; padding-bottom: 8px; border-bottom: 2px solid {accent_purple}; }}
  .model-badge {{
    display: inline-flex; align-items: center; gap: 8px;
    background: {bg_card2}; border: 1px solid {border_color};
    border-radius: 20px; padding: 6px 14px;
    font-size: 0.78rem; color: {text_primary}; font-weight: 600; margin: 4px;
  }}
  .forecast-table {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; }}
  .forecast-table th {{ background: {bg_card2}; color: {text_secondary}; padding: 9px 12px; text-align: center; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.8px; border-bottom: 1px solid {border_color}; }}
  .forecast-table td {{ padding: 8px 12px; text-align: center; border-bottom: 1px solid {border_color}; font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; color: {text_primary}; }}
  .forecast-table tr:last-child td {{ border-bottom: none; }}
  .forecast-table tr:hover td {{ background: {bg_card2}; }}
  .progress-bar-bg {{ background: {bg_card2}; border-radius: 8px; height: 12px; overflow: hidden; margin: 6px 0; }}
  .progress-bar-fill {{ height: 100%; border-radius: 8px; transition: width 0.5s ease; }}
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

# Model Badge
st.markdown(f"""
<div style='margin-bottom:16px;'>
  <span class='model-badge'>🔮 {t['model']}: Facebook Prophet</span>
  <span class='model-badge'>📊 MAE: 284K tourists</span>
  <span class='model-badge'>✅ Seasonality: Multiplicative</span>
  <span class='model-badge'>📅 Training: 2015–2024 (120 months)</span>
</div>""", unsafe_allow_html=True)

# KPIs
k1,k2,k3,k4,k5,k6 = st.columns(6)
kpi_items = [
    (k1,"📅",t["kpi_peak25"],"Jan 2025","12,307K",accent_blue),
    (k2,"📅",t["kpi_peak26"],"Jan 2026","13,680K",accent_purple),
    (k3,"🌍",t["kpi_total25"],f"{total_2025:.1f}M","+8.5% vs 2024",accent_teal),
    (k4,"🌍",t["kpi_total26"],f"{total_2026:.1f}M","+11.1% vs 2025",accent_gold),
    (k5,"📉","Low Month 2025","May 2025","8,964K",accent_red),
    (k6,"📉","Low Month 2026","May 2026","9,927K",accent_red),
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

# CHART 1: Main Forecast with CI
st.markdown(f"<div class='section-title'>📈 {t['forecast_chart']}</div>", unsafe_allow_html=True)

months_2025 = [f"2025-{str(m).zfill(2)}" for m in range(1,13)]
months_2026 = [f"2026-{str(m).zfill(2)}" for m in range(1,13)]

fig_fore = go.Figure()

if year_filter in [t["both_years"], "2025"]:
    fig_fore.add_trace(go.Scatter(
        x=months_2025+months_2025[::-1],
        y=upper_2025+lower_2025[::-1],
        fill='toself', fillcolor=f"{accent_blue}20",
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=True, name=f"CI 2025",
        hoverinfo='skip'
    ))
    fig_fore.add_trace(go.Scatter(
        x=months_2025, y=forecast_2025,
        name="2025", line=dict(color=accent_blue, width=2.5, dash='dot'),
        marker=dict(size=7, color=accent_blue, line=dict(color=bg_card,width=2)),
        hovertemplate="<b>%{x}</b><br>Forecast: %{y:,.0f}K<extra></extra>"
    ))

if year_filter in [t["both_years"], "2026"]:
    fig_fore.add_trace(go.Scatter(
        x=months_2026+months_2026[::-1],
        y=upper_2026+lower_2026[::-1],
        fill='toself', fillcolor=f"{accent_purple}20",
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=True, name=f"CI 2026",
        hoverinfo='skip'
    ))
    fig_fore.add_trace(go.Scatter(
        x=months_2026, y=forecast_2026,
        name="2026", line=dict(color=accent_purple, width=2.5),
        marker=dict(size=7, color=accent_purple, line=dict(color=bg_card,width=2)),
        hovertemplate="<b>%{x}</b><br>Forecast: %{y:,.0f}K<extra></extra>"
    ))

fig_fore.add_annotation(x="2026-01", y=13680,
    text="Peak: 13,680K", showarrow=True, arrowhead=2,
    font=dict(size=10, color=accent_gold), arrowcolor=accent_gold, ay=-40)
fig_fore.add_annotation(x="2025-05", y=8964,
    text="Low: 8,964K", showarrow=True, arrowhead=2,
    font=dict(size=10, color=accent_red), arrowcolor=accent_red, ay=40)

fig_fore.update_layout(
    template=plotly_template, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
    height=380, margin=dict(l=10,r=10,t=20,b=10),
    legend=dict(orientation="h", y=-0.12, font=dict(size=11)),
    xaxis=dict(showgrid=False, tickfont=dict(size=10), tickangle=45),
    yaxis=dict(showgrid=True, gridcolor=border_color, tickfont=dict(size=10), title=t["tourists_k"]),
    font=dict(color=text_primary),
)
st.plotly_chart(fig_fore, use_container_width=True, config={"displayModeBar": False})

# CHART 2+3: Historical vs Forecast + Vision 2030
hist_col, vision_col = st.columns([3, 2])

with hist_col:
    st.markdown(f"<div class='section-title'>📊 {t['historical']}</div>", unsafe_allow_html=True)
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Scatter(
        x=historical_years, y=historical_total,
        name=t["historical_lbl"], line=dict(color=accent_teal, width=2.5),
        fill='tozeroy', fillcolor=f"{accent_teal}15",
        marker=dict(size=7)
    ))
    fig_hist.add_trace(go.Scatter(
        x=[2024, 2025, 2026],
        y=[115.9, total_2025, total_2026],
        name=t["forecast"], line=dict(color=accent_purple, width=2.5, dash='dash'),
        marker=dict(size=8, symbol='diamond', color=accent_purple,
                    line=dict(color=bg_card,width=2))
    ))
    fig_hist.add_vrect(x0=2024.5, x1=2026.5,
        fillcolor=accent_purple, opacity=0.05,
        annotation_text="Forecast Zone",
        annotation=dict(font_color=accent_purple, font_size=10))
    fig_hist.update_layout(
        template=plotly_template, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=300, margin=dict(l=10,r=10,t=20,b=10),
        legend=dict(orientation="h", y=-0.15, font=dict(size=11)),
        xaxis=dict(showgrid=False, tickfont=dict(size=11)),
        yaxis=dict(showgrid=True, gridcolor=border_color, tickfont=dict(size=10), title=t["tourists_m"]),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar": False})

with vision_col:
    st.markdown(f"<div class='section-title'>🎯 {t['vision2030']}</div>", unsafe_allow_html=True)
    milestones = [
        (t["yr2024"], 115.9, 150, accent_teal),
        (t["yr2025"], total_2025, 150, accent_blue),
        (t["yr2026"], total_2026, 150, accent_purple),
        (t["yr2030"], 150, 150, accent_gold),
    ]
    for label, val, target, color in milestones:
        pct = min(val/target*100, 100)
        st.markdown(f"""
        <div style='margin-bottom:14px;'>
          <div style='display:flex;justify-content:space-between;margin-bottom:4px;'>
            <span style='font-size:0.82rem;font-weight:600;color:{text_primary};'>{label}</span>
            <span style='font-size:0.82rem;font-weight:700;color:{color};font-family:IBM Plex Mono,monospace;'>{val:.1f}M / {target}M</span>
          </div>
          <div class='progress-bar-bg'>
            <div class='progress-bar-fill' style='width:{pct:.1f}%;background:{color};'></div>
          </div>
          <div style='font-size:0.7rem;color:{text_secondary};text-align:right;'>{pct:.1f}% {t['progress']}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:{bg_card2};border:1px solid {border_color};border-radius:10px;padding:12px 14px;margin-top:8px;'>
      <div style='font-size:0.78rem;font-weight:700;color:{accent_gold};margin-bottom:4px;'>🎯 {t['vision_note']}</div>
      <div style='font-size:0.75rem;color:{text_secondary};'>At current growth rate (+11% YoY), target achievable by 2029</div>
    </div>""", unsafe_allow_html=True)

# MONTHLY TABLE
st.markdown(f"<div class='section-title'>📋 {t['monthly_table']}</div>", unsafe_allow_html=True)

table_html = f"""
<table class='forecast-table'>
  <thead>
    <tr>
      <th>{t['month']}</th>
      <th>2025 {t['forecast']}</th>
      <th>2025 {t['lower']}</th>
      <th>2025 {t['upper']}</th>
      <th>2026 {t['forecast']}</th>
      <th>2026 {t['lower']}</th>
      <th>2026 {t['upper']}</th>
      <th>YoY</th>
    </tr>
  </thead>
  <tbody>"""

for i, m in enumerate(months_lbl):
    yoy = round((forecast_2026[i] - forecast_2025[i]) / forecast_2025[i] * 100, 1)
    yoy_color = accent_green if yoy > 0 else accent_red
    peak_25 = forecast_2025[i] == max(forecast_2025)
    peak_26 = forecast_2026[i] == max(forecast_2026)
    row_bg = f"background:{bg_card2};" if (peak_25 or peak_26) else ""
    table_html += f"""
    <tr style='{row_bg}'>
      <td style='font-weight:600;color:{text_primary};font-family:Sora,sans-serif;'>{m}</td>
      <td style='color:{accent_blue};font-weight:{"700" if peak_25 else "400"};'>{forecast_2025[i]:,}</td>
      <td style='color:{text_secondary};'>{lower_2025[i]:,}</td>
      <td style='color:{text_secondary};'>{upper_2025[i]:,}</td>
      <td style='color:{accent_purple};font-weight:{"700" if peak_26 else "400"};'>{forecast_2026[i]:,}</td>
      <td style='color:{text_secondary};'>{lower_2026[i]:,}</td>
      <td style='color:{text_secondary};'>{upper_2026[i]:,}</td>
      <td style='color:{yoy_color};font-weight:700;'>+{yoy}%</td>
    </tr>"""

total_25 = sum(forecast_2025)
total_26 = sum(forecast_2026)
total_yoy = round((total_26-total_25)/total_25*100,1)
table_html += f"""
    <tr style='background:{bg_card2};border-top:2px solid {accent_purple};'>
      <td style='font-weight:800;color:{text_primary};font-family:Sora,sans-serif;'>TOTAL</td>
      <td style='color:{accent_blue};font-weight:800;'>{total_25:,}</td>
      <td style='color:{text_secondary};'>-</td>
      <td style='color:{text_secondary};'>-</td>
      <td style='color:{accent_purple};font-weight:800;'>{total_26:,}</td>
      <td style='color:{text_secondary};'>-</td>
      <td style='color:{text_secondary};'>-</td>
      <td style='color:{accent_green};font-weight:800;'>+{total_yoy}%</td>
    </tr>
  </tbody>
</table>"""
st.markdown(table_html, unsafe_allow_html=True)

# KEY INSIGHTS
st.markdown(f"<div class='section-title'>💡 {t['insight_title']}</div>", unsafe_allow_html=True)
insights = [
    ("🏆", t["i1"], accent_purple),
    ("📈", t["i2"], accent_blue),
    ("📅", t["i3"], accent_teal),
    ("🎯", t["i4"], accent_gold),
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
