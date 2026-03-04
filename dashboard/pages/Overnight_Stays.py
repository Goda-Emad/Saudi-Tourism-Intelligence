import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Overnight Stays · Saudi Tourism Intelligence",
    page_icon="🏨",
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
        "page_title":"🏨 Overnight Stays Analysis",
        "subtitle":"Annual & Monthly Patterns · Length of Stay · Inbound vs Domestic",
        "built_by":"Built by","dark_mode":"🌙 Dark","light_mode":"☀️ Light","lang_toggle":"🌐 العربية",
        "pages":"Navigation","page_overview":"🏠 Overview","page_trends":"📈 Tourist Trends",
        "page_season":"📅 Seasonality","page_spend":"💰 Spending","page_overnight":"🏨 Overnight Stays",
        "page_forecast":"🔮 Forecasting","page_segment":"🎯 Segmentation","page_carbon":"🌱 Carbon Impact",
        "kpi_total":"Total Overnight Stays 2024","kpi_inbound":"Inbound Nights 2024",
        "kpi_domestic":"Domestic Nights 2024","kpi_los_in":"Avg Length of Stay (Inbound)",
        "kpi_los_dom":"Avg Length of Stay (Domestic)",
        "annual_trend":"Annual Overnight Stays Trend 2015–2024",
        "los_trend":"Average Length of Stay — Trend",
        "monthly_dist":"Monthly Distribution of Overnight Stays",
        "inbound_vs_dom":"Inbound vs Domestic Split (%)",
        "covid_impact":"COVID-19 Impact on Overnight Stays",
        "growth_chart":"Recovery Growth 2021–2024",
        "inbound":"Inbound","domestic":"Domestic","total":"Total",
        "nights_k":"Overnight Stays (Thousands)","nights_m":"Overnight Stays (Millions)",
        "nights":"Nights","filter_type":"Tourist Type","all_types":"All",
        "year_range":"Year Range","insight_title":"Key Insights",
        "i1":"2024: Inbound overnight stays (560M) surpassed Domestic (539M) for the first time!",
        "i2":"Inbound avg length of stay surged from 8.6 nights (2021) to 19.2 nights (2024) — +123%",
        "i3":"COVID caused -80% collapse in Inbound nights (2020) vs only -15% for Domestic",
        "i4":"Inbound recovery 2021 to 2024: +1,663% — one of the fastest tourism recoveries globally",
        "pre_covid":"Pre-COVID (2019)","covid_year":"COVID (2020)","post_covid":"Post-COVID (2024)",
        "drop":"Drop","recovery":"Recovery",
    },
    "AR": {
        "page_title":"🏨 تحليل ليالي الإقامة",
        "subtitle":"الأنماط السنوية والشهرية · مدة الإقامة · الوافد مقابل المحلي",
        "built_by":"من تطوير","dark_mode":"🌙 داكن","light_mode":"☀️ فاتح","lang_toggle":"🌐 English",
        "pages":"التنقل","page_overview":"🏠 نظرة عامة","page_trends":"📈 اتجاهات السياحة",
        "page_season":"📅 الموسمية","page_spend":"💰 الإنفاق","page_overnight":"🏨 ليالي الإقامة",
        "page_forecast":"🔮 التوقعات","page_segment":"🎯 تقسيم السياح","page_carbon":"🌱 الأثر الكربوني",
        "kpi_total":"إجمالي ليالي الإقامة 2024","kpi_inbound":"ليالي الوافدين 2024",
        "kpi_domestic":"ليالي المحليين 2024","kpi_los_in":"متوسط مدة الإقامة (وافد)",
        "kpi_los_dom":"متوسط مدة الإقامة (محلي)",
        "annual_trend":"اتجاه ليالي الإقامة السنوي 2015–2024",
        "los_trend":"متوسط مدة الإقامة — الاتجاه",
        "monthly_dist":"التوزيع الشهري لليالي الإقامة",
        "inbound_vs_dom":"الوافد مقابل المحلي (%)",
        "covid_impact":"تأثير كوفيد-19 على ليالي الإقامة",
        "growth_chart":"نمو التعافي 2021–2024",
        "inbound":"وافد","domestic":"محلي","total":"إجمالي",
        "nights_k":"الليالي (ألف)","nights_m":"الليالي (مليون)",
        "nights":"ليالي","filter_type":"نوع السائح","all_types":"الكل",
        "year_range":"نطاق السنوات","insight_title":"أبرز الاستنتاجات",
        "i1":"2024: ليالي الوافدين (560M) تجاوزت المحليين (539M) لأول مرة في التاريخ!",
        "i2":"متوسط إقامة الوافد قفز من 8.6 ليلة (2021) إلى 19.2 ليلة (2024) — +123%",
        "i3":"كوفيد تسبب في انهيار -80% في ليالي الوافدين مقابل -15% فقط للمحليين",
        "i4":"تعافي الوافدين 2021 إلى 2024: +1,663% — من أسرع التعافيات السياحية عالمياً",
        "pre_covid":"قبل كوفيد (2019)","covid_year":"كوفيد (2020)","post_covid":"بعد كوفيد (2024)",
        "drop":"انخفاض","recovery":"تعافي",
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
years = list(range(2015, 2025))
inbound_stays  = [193084,187225,171036,173929,189036,37824,31771,270728,432299,560227]
domestic_stays = [240853,235804,224212,232122,268751,228538,353331,369606,495341,538618]
total_stays    = [a+b for a,b in zip(inbound_stays,domestic_stays)]

los_inbound  = [10.36,9.90,9.54,10.10,9.79,5.90,8.58,16.56,15.65,19.22]
los_domestic = [5.15,5.23,5.09,5.34,5.62,5.31,5.41,4.58,5.93,6.11]

months_en = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
months_ar = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
months_lbl = months_ar if lang=="AR" else months_en
monthly_inbound_stays  = [18923,17234,22745,19876,16543,18234,19876,18543,16234,15876,18234,20890]
monthly_domestic_stays = [28765,24532,26543,25432,22345,35678,39225,36543,28765,26543,32456,38765]

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
    border: 1px solid {border_color}; border-left: 4px solid {accent_blue};
    border-radius: 16px; padding: 28px 32px; margin-bottom: 24px;
    position: relative; overflow: hidden;
  }}
  .page-header::after {{ content: '🏨'; position: absolute; right: 24px; top: 50%; transform: translateY(-50%); font-size: 4rem; opacity: 0.08; }}
  .page-title {{ font-size: 1.9rem; font-weight: 800; color: {text_primary}; margin: 0 0 4px 0; }}
  .page-subtitle {{ font-size: 0.88rem; color: {accent_blue}; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; }}
  .kpi-card {{ background: {bg_card}; border: 1px solid {border_color}; border-radius: 14px; padding: 18px 14px; text-align: center; height: 100%; transition: transform 0.2s; }}
  .kpi-card:hover {{ transform: translateY(-2px); }}
  .kpi-icon {{ font-size: 1.5rem; margin-bottom: 6px; }}
  .kpi-value {{ font-size: 1.4rem; font-weight: 800; line-height: 1.1; font-family: 'IBM Plex Mono', monospace; }}
  .kpi-label {{ font-size: 0.64rem; color: {text_secondary}; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; margin-top: 4px; }}
  .kpi-sub {{ font-size: 0.73rem; font-weight: 600; margin-top: 4px; font-family: 'IBM Plex Mono', monospace; }}
  .section-title {{ font-size: 1.05rem; font-weight: 700; color: {text_primary}; margin: 24px 0 12px 0; padding-bottom: 8px; border-bottom: 2px solid {accent_blue}; }}
  .covid-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
  .covid-card {{ background: {bg_card}; border: 1px solid {border_color}; border-radius: 12px; padding: 16px 18px; }}
  .covid-header {{ font-size: 0.75rem; font-weight: 700; color: {text_secondary}; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 12px; }}
  .covid-row {{ display: flex; justify-content: space-between; padding: 7px 0; border-bottom: 1px solid {border_color}; }}
  .covid-row:last-child {{ border-bottom: none; }}
  .covid-label {{ font-size: 0.8rem; color: {text_primary}; }}
  .covid-val {{ font-size: 0.82rem; font-weight: 700; font-family: 'IBM Plex Mono', monospace; }}
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

# KPIs
k1,k2,k3,k4,k5 = st.columns(5)
kpi_items = [
    (k1,"🌙",t["kpi_total"],"1.10B","+19.1% YoY",accent_teal),
    (k2,"✈️",t["kpi_inbound"],"560M","+29.6% YoY",accent_blue),
    (k3,"🏠",t["kpi_domestic"],"539M","+8.7% YoY",accent_gold),
    (k4,"⏰",t["kpi_los_in"],"19.2 nights","+23% YoY",accent_purple),
    (k5,"🏡",t["kpi_los_dom"],"6.1 nights","+3% YoY",accent_green),
]
for col, icon, label, val, sub, color in kpi_items:
    with col:
        st.markdown(f"""
        <div class='kpi-card'>
          <div class='kpi-icon'>{icon}</div>
          <div class='kpi-value' style='color:{color};'>{val}</div>
          <div class='kpi-label'>{label}</div>
          <div class='kpi-sub' style='color:{accent_green};'>{sub}</div>
        </div>""", unsafe_allow_html=True)

# FILTER
y_s, y_e = year_range
idx_s = years.index(y_s); idx_e = years.index(y_e)+1
f_years = years[idx_s:idx_e]

# CHART 1: Annual Trend
st.markdown(f"<div class='section-title'>📊 {t['annual_trend']}</div>", unsafe_allow_html=True)

fig_annual = go.Figure()
if tourist_filter in [t["all_types"], t["inbound"]]:
    fig_annual.add_trace(go.Bar(x=f_years, y=[v/1000 for v in inbound_stays[idx_s:idx_e]],
        name=t["inbound"], marker_color=accent_blue, opacity=0.88))
if tourist_filter in [t["all_types"], t["domestic"]]:
    fig_annual.add_trace(go.Bar(x=f_years, y=[v/1000 for v in domestic_stays[idx_s:idx_e]],
        name=t["domestic"], marker_color=accent_teal, opacity=0.88))
if tourist_filter == t["all_types"]:
    fig_annual.add_trace(go.Scatter(x=f_years, y=[v/1000 for v in total_stays[idx_s:idx_e]],
        name=t["total"], line=dict(color=accent_gold, width=2.5, dash='dot'),
        marker=dict(size=7), yaxis='y2'))
fig_annual.add_vrect(x0=2019.5, x1=2021.5, fillcolor=accent_red, opacity=0.07,
    annotation_text="COVID-19", annotation=dict(font_color=accent_red, font_size=10))
fig_annual.update_layout(
    template=plotly_template, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
    height=360, barmode='group', margin=dict(l=10,r=10,t=20,b=10),
    legend=dict(orientation="h", y=-0.12, font=dict(size=11)),
    xaxis=dict(showgrid=False, tickfont=dict(size=11)),
    yaxis=dict(title="Million Nights", showgrid=True, gridcolor=border_color, tickfont=dict(size=10)),
    yaxis2=dict(overlaying='y', side='right', showgrid=False, title="Total (M)", tickfont=dict(size=10)),
    font=dict(color=text_primary), bargap=0.25
)
st.plotly_chart(fig_annual, use_container_width=True, config={"displayModeBar": False})

# CHART 2+3: LOS + Monthly
los_col, monthly_col = st.columns(2)

with los_col:
    st.markdown(f"<div class='section-title'>⏰ {t['los_trend']}</div>", unsafe_allow_html=True)
    fig_los = go.Figure()
    if tourist_filter in [t["all_types"], t["inbound"]]:
        fig_los.add_trace(go.Scatter(x=f_years, y=los_inbound[idx_s:idx_e],
            name=t["inbound"], line=dict(color=accent_blue, width=2.5),
            fill='tozeroy', fillcolor=f"{accent_blue}18",
            marker=dict(size=8, color=accent_blue, line=dict(color=bg_card,width=2)),
            text=[f"{v:.1f}" for v in los_inbound[idx_s:idx_e]],
            textposition='top center', mode='lines+markers+text',
            textfont=dict(size=9, color=accent_blue)))
    if tourist_filter in [t["all_types"], t["domestic"]]:
        fig_los.add_trace(go.Scatter(x=f_years, y=los_domestic[idx_s:idx_e],
            name=t["domestic"], line=dict(color=accent_teal, width=2.5),
            fill='tozeroy', fillcolor=f"{accent_teal}18",
            marker=dict(size=8, color=accent_teal, line=dict(color=bg_card,width=2)),
            text=[f"{v:.1f}" for v in los_domestic[idx_s:idx_e]],
            textposition='top center', mode='lines+markers+text',
            textfont=dict(size=9, color=accent_teal)))
    fig_los.add_annotation(x=2024, y=19.22,
        text="19.2 nights<br>All-time high!",
        showarrow=True, arrowhead=2,
        font=dict(size=9, color=accent_gold), arrowcolor=accent_gold, ay=-40)
    fig_los.update_layout(
        template=plotly_template, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=320, margin=dict(l=10,r=10,t=20,b=10),
        legend=dict(orientation="h", y=-0.15, font=dict(size=10)),
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor=border_color, tickfont=dict(size=10), title=t["nights"]),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_los, use_container_width=True, config={"displayModeBar": False})

with monthly_col:
    st.markdown(f"<div class='section-title'>📅 {t['monthly_dist']}</div>", unsafe_allow_html=True)
    fig_monthly = go.Figure()
    if tourist_filter in [t["all_types"], t["inbound"]]:
        fig_monthly.add_trace(go.Scatter(x=months_lbl, y=monthly_inbound_stays,
            name=t["inbound"], line=dict(color=accent_blue, width=2.5),
            fill='tozeroy', fillcolor=f"{accent_blue}18", marker=dict(size=7)))
    if tourist_filter in [t["all_types"], t["domestic"]]:
        fig_monthly.add_trace(go.Scatter(x=months_lbl, y=monthly_domestic_stays,
            name=t["domestic"], line=dict(color=accent_teal, width=2.5),
            fill='tozeroy', fillcolor=f"{accent_teal}18", marker=dict(size=7)))
    fig_monthly.add_annotation(x="Mar", y=22745,
        text="Inbound Peak", showarrow=True, arrowhead=2,
        font=dict(size=9, color=accent_blue), arrowcolor=accent_blue, ay=-35)
    fig_monthly.add_annotation(x="Jul", y=39225,
        text="Domestic Peak", showarrow=True, arrowhead=2,
        font=dict(size=9, color=accent_teal), arrowcolor=accent_teal, ay=-35)
    fig_monthly.update_layout(
        template=plotly_template, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=320, margin=dict(l=10,r=10,t=20,b=10),
        legend=dict(orientation="h", y=-0.18, font=dict(size=10)),
        xaxis=dict(showgrid=False, tickfont=dict(size=9), tickangle=45),
        yaxis=dict(showgrid=True, gridcolor=border_color, tickfont=dict(size=10), title=t["nights_k"]),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_monthly, use_container_width=True, config={"displayModeBar": False})

# CHART 4+5: Split % + COVID Table
split_col, covid_col = st.columns([2, 3])

with split_col:
    st.markdown(f"<div class='section-title'>⚖️ {t['inbound_vs_dom']}</div>", unsafe_allow_html=True)
    inb_pct = [round(a/(a+b)*100,1) for a,b in zip(inbound_stays[idx_s:idx_e], domestic_stays[idx_s:idx_e])]
    dom_pct = [round(b/(a+b)*100,1) for a,b in zip(inbound_stays[idx_s:idx_e], domestic_stays[idx_s:idx_e])]
    fig_split = go.Figure()
    fig_split.add_trace(go.Bar(x=f_years, y=inb_pct, name=t["inbound"],
        marker_color=accent_blue, opacity=0.88))
    fig_split.add_trace(go.Bar(x=f_years, y=dom_pct, name=t["domestic"],
        marker_color=accent_teal, opacity=0.88))
    fig_split.update_layout(
        template=plotly_template, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=280, barmode='stack', margin=dict(l=10,r=10,t=10,b=10),
        legend=dict(orientation="h", y=-0.18, font=dict(size=10)),
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor=border_color, tickfont=dict(size=10), ticksuffix="%"),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_split, use_container_width=True, config={"displayModeBar": False})

with covid_col:
    st.markdown(f"<div class='section-title'>😷 {t['covid_impact']}</div>", unsafe_allow_html=True)
    covid_data = [
        (t["inbound"],  "189,036K", "37,824K",  "560,227K", "-80.0%", "+1,663%"),
        (t["domestic"], "268,751K", "228,538K", "538,618K", "-15.0%",   "+136%"),
        (t["total"],    "457,787K", "266,362K","1,098,845K","-41.8%",   "+312%"),
    ]
    table_html = f"""
    <table style='width:100%;border-collapse:collapse;font-size:0.82rem;'>
      <thead>
        <tr>
          <th style='background:{bg_card2};color:{text_secondary};padding:9px 12px;text-align:left;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.8px;border-bottom:1px solid {border_color};'>{t['filter_type']}</th>
          <th style='background:{bg_card2};color:{text_secondary};padding:9px 12px;text-align:right;font-size:0.7rem;text-transform:uppercase;border-bottom:1px solid {border_color};'>{t['pre_covid']}</th>
          <th style='background:{bg_card2};color:{text_secondary};padding:9px 12px;text-align:right;font-size:0.7rem;text-transform:uppercase;border-bottom:1px solid {border_color};'>{t['covid_year']}</th>
          <th style='background:{bg_card2};color:{text_secondary};padding:9px 12px;text-align:right;font-size:0.7rem;text-transform:uppercase;border-bottom:1px solid {border_color};'>{t['post_covid']}</th>
          <th style='background:{bg_card2};color:{text_secondary};padding:9px 12px;text-align:right;font-size:0.7rem;text-transform:uppercase;border-bottom:1px solid {border_color};'>{t['drop']}</th>
          <th style='background:{bg_card2};color:{text_secondary};padding:9px 12px;text-align:right;font-size:0.7rem;text-transform:uppercase;border-bottom:1px solid {border_color};'>{t['recovery']}</th>
        </tr>
      </thead>
      <tbody>"""
    for row in covid_data:
        table_html += f"""
        <tr>
          <td style='padding:9px 12px;color:{text_primary};font-weight:700;border-bottom:1px solid {border_color};'>{row[0]}</td>
          <td style='padding:9px 12px;color:{text_secondary};text-align:right;font-family:IBM Plex Mono,monospace;border-bottom:1px solid {border_color};'>{row[1]}</td>
          <td style='padding:9px 12px;color:{accent_red};text-align:right;font-weight:700;font-family:IBM Plex Mono,monospace;border-bottom:1px solid {border_color};'>{row[2]}</td>
          <td style='padding:9px 12px;color:{accent_teal};text-align:right;font-weight:700;font-family:IBM Plex Mono,monospace;border-bottom:1px solid {border_color};'>{row[3]}</td>
          <td style='padding:9px 12px;color:{accent_red};text-align:right;font-weight:700;font-family:IBM Plex Mono,monospace;border-bottom:1px solid {border_color};'>{row[4]}</td>
          <td style='padding:9px 12px;color:{accent_green};text-align:right;font-weight:700;font-family:IBM Plex Mono,monospace;border-bottom:1px solid {border_color};'>{row[5]}</td>
        </tr>"""
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)

    # Recovery bar
    st.markdown(f"<div style='margin-top:16px;font-size:0.85rem;font-weight:700;color:{text_primary};margin-bottom:8px;'>🚀 {t['growth_chart']}</div>", unsafe_allow_html=True)
    recovery_years = [2021, 2022, 2023, 2024]
    inb_recovery = [31771, 270728, 432299, 560227]
    fig_rec = go.Figure(go.Bar(
        x=recovery_years, y=[v/1000 for v in inb_recovery],
        marker_color=[accent_blue if i<3 else accent_gold for i in range(4)],
        text=[f"{v/1000:.0f}M" for v in inb_recovery],
        textposition='outside', textfont=dict(size=10, color=text_primary),
        opacity=0.88
    ))
    fig_rec.update_layout(
        template=plotly_template, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=200, margin=dict(l=10,r=10,t=10,b=10),
        xaxis=dict(showgrid=False, tickfont=dict(size=11)),
        yaxis=dict(showgrid=True, gridcolor=border_color, tickfont=dict(size=10)),
        font=dict(color=text_primary), showlegend=False
    )
    st.plotly_chart(fig_rec, use_container_width=True, config={"displayModeBar": False})

# KEY INSIGHTS
st.markdown(f"<div class='section-title'>💡 {t['insight_title']}</div>", unsafe_allow_html=True)
insights = [
    ("🏆", t["i1"], accent_teal),
    ("⏰", t["i2"], accent_blue),
    ("😷", t["i3"], accent_red),
    ("🚀", t["i4"], accent_green),
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
