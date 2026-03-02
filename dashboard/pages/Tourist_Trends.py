import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ══════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════
st.set_page_config(
    page_title="Tourist Trends · Saudi Tourism Intelligence",
    page_icon="📈",
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
        "page_title":     "📈 Tourist Trends 2015–2024",
        "subtitle":       "Annual & Monthly Tourist Analysis · Inbound vs Domestic",
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
        "total_2024":     "Total Tourists 2024",
        "inbound_2024":   "Inbound 2024",
        "domestic_2024":  "Domestic 2024",
        "yoy_growth":     "YoY Growth 2024",
        "covid_drop":     "COVID Drop 2020",
        "recovery":       "Recovery ×",
        # Sections
        "annual_trend":   "Annual Tourist Trend 2015–2024",
        "by_purpose":     "Tourists by Purpose (Annual)",
        "inbound_vs_dom": "Inbound vs Domestic Split",
        "monthly_trend":  "Monthly Tourist Distribution",
        "purpose_heatmap":"Purpose Heatmap by Year",
        "covid_analysis": "COVID-19 Impact Analysis",
        # Labels
        "total":          "Total",
        "inbound":        "Inbound",
        "domestic":       "Domestic",
        "religious":      "Religious",
        "leisure":        "Leisure",
        "business":       "Business",
        "vfr":            "VFR",
        "other":          "Other",
        "year":           "Year",
        "tourists_m":     "Tourists (Millions)",
        "filter_type":    "Tourist Type",
        "filter_year":    "Year Range",
        "all_types":      "All",
        "insight_title":  "Key Insights",
        "i1": "2024 reached all-time high: 115.8M tourists — +72% vs 2021",
        "i2": "Domestic tourism is 3× larger than Inbound (86M vs 30M)",
        "i3": "Leisure surpassed Religious as #1 purpose in 2024",
        "i4": "COVID caused -29.2% drop in 2020, full recovery by 2022",
        "pre_covid":      "Pre-COVID (2019)",
        "during_covid":   "COVID (2020)",
        "post_covid":     "Post-COVID (2024)",
        "change":         "Change",
    },
    "AR": {
        "page_title":     "📈 اتجاهات السياحة 2015–2024",
        "subtitle":       "تحليل سنوي وشهري · الوافدون مقابل المحليون",
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
        "total_2024":     "إجمالي السياح 2024",
        "inbound_2024":   "الوافدون 2024",
        "domestic_2024":  "المحليون 2024",
        "yoy_growth":     "نمو سنوي 2024",
        "covid_drop":     "انخفاض كوفيد 2020",
        "recovery":       "معدل التعافي ×",
        # Sections
        "annual_trend":   "الاتجاه السنوي للسياحة 2015–2024",
        "by_purpose":     "السياح حسب الغرض (سنوي)",
        "inbound_vs_dom": "الوافدون مقابل المحليون",
        "monthly_trend":  "التوزيع الشهري للسياح",
        "purpose_heatmap":"خريطة الغرض السياحي حسب السنة",
        "covid_analysis": "تحليل تأثير كوفيد-19",
        # Labels
        "total":          "الإجمالي",
        "inbound":        "وافد",
        "domestic":       "محلي",
        "religious":      "ديني",
        "leisure":        "ترفيه",
        "business":       "أعمال",
        "vfr":            "زيارة أهل",
        "other":          "أخرى",
        "year":           "السنة",
        "tourists_m":     "السياح (مليون)",
        "filter_type":    "نوع السائح",
        "filter_year":    "نطاق السنوات",
        "all_types":      "الكل",
        "insight_title":  "أبرز الاستنتاجات",
        "i1": "2024 سجّل أعلى رقم تاريخي: 115.8M سائح — +72% مقارنة بـ 2021",
        "i2": "السياحة المحلية أكبر 3 مرات من الوافدة (86M مقابل 30M)",
        "i3": "الترفيه تجاوز الديني كأول غرض سياحي في 2024",
        "i4": "كوفيد تسبب في انخفاض -29.2% عام 2020، تعافٍ كامل بحلول 2022",
        "pre_covid":      "ما قبل كوفيد (2019)",
        "during_covid":   "كوفيد (2020)",
        "post_covid":     "ما بعد كوفيد (2024)",
        "change":         "التغيير",
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
years = list(range(2015, 2025))

inbound_annual = [17.99, 18.04, 16.11, 15.33, 17.53, 4.14, 3.48, 16.64, 27.18, 29.73]
domestic_annual= [46.45, 45.04, 43.82, 43.26, 47.81, 42.11, 63.83, 77.84, 81.92, 86.16]
total_annual   = [a+b for a,b in zip(inbound_annual, domestic_annual)]

purpose_data = {
    "Religious": [8.00, 7.50, 7.00, 6.80, 9.80, 0.80, 0.60, 5.50, 9.50, 12.30],
    "Leisure":   [3.00, 3.20, 2.80, 2.60, 3.50, 0.90, 1.00, 4.80, 6.20,  7.50],
    "Business":  [2.40, 2.60, 2.20, 2.10, 2.50, 0.60, 0.50, 1.80, 2.50,  2.00],
    "VFR":       [3.10, 3.20, 2.80, 2.60, 3.30, 1.20, 1.00, 3.20, 5.00,  5.95],
    "Other":     [1.49, 1.54, 1.31, 1.23, 1.43, 0.64, 0.38, 1.34, 3.98,  2.00],
}

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
monthly_inbound  = [2.47,2.13,2.80,2.32,1.89,2.12,2.22,2.16,1.93,1.88,2.22,2.59]
monthly_domestic = [6.96,5.32,5.71,5.33,4.78,7.85,9.61,7.98,5.79,5.37,7.35,8.11]

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
    border-left: 4px solid {accent_blue};
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
  }}
  .page-header::after {{
    content: '📈';
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
    color: {accent_blue};
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
    border-bottom: 2px solid {accent_blue};
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

  .covid-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
  }}
  .covid-table th {{
    background: {bg_card2};
    color: {text_secondary};
    padding: 10px 14px;
    text-align: left;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    border-bottom: 1px solid {border_color};
  }}
  .covid-table td {{
    padding: 10px 14px;
    color: {text_primary};
    border-bottom: 1px solid {border_color};
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
  }}
  .covid-table tr:last-child td {{ border-bottom: none; }}

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
    for p in ["page_overview","page_trends","page_season","page_spend",
              "page_overnight","page_forecast","page_segment","page_carbon"]:
        active = p == "page_trends"
        bg = f"{accent_blue}22" if active else "transparent"
        fw = "700" if active else "400"
        bc = accent_blue if active else "transparent"
        st.markdown(f"<div style='padding:7px 10px;border-radius:8px;background:{bg};border-left:3px solid {bc};font-size:0.83rem;font-weight:{fw};color:{text_primary};margin-bottom:3px;'>{t[p]}</div>", unsafe_allow_html=True)

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
    year_range = st.slider(t["filter_year"], 2015, 2024, (2015, 2024))
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
f_years    = years[idx_s:idx_e]
f_inbound  = inbound_annual[idx_s:idx_e]
f_domestic = domestic_annual[idx_s:idx_e]
f_total    = total_annual[idx_s:idx_e]

# ══════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════
k1, k2, k3, k4, k5 = st.columns(5)
kpi_data = [
    (k1, "🌍", t["total_2024"],   "115.8M", "+8.1%",  accent_teal,   accent_green),
    (k2, "✈️", t["inbound_2024"], "29.7M",  "+8.4%",  accent_blue,   accent_green),
    (k3, "🏠", t["domestic_2024"],"86.2M",  "+5.2%",  accent_gold,   accent_green),
    (k4, "😷", t["covid_drop"],   "-29.2%", "2020",   accent_red,    accent_red),
    (k5, "🚀", t["recovery"],     "1.72×",  "2021→24",accent_purple, accent_green),
]
for col, icon, label, val, delta, color, dc in kpi_data:
    with col:
        st.markdown(f"""
        <div class='kpi-card'>
          <div class='kpi-icon'>{icon}</div>
          <div class='kpi-value' style='color:{color};'>{val}</div>
          <div class='kpi-label'>{label}</div>
          <div class='kpi-delta' style='color:{dc};'>{delta}</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# CHART 1: Annual Trend
# ══════════════════════════════════════════
st.markdown(f"<div class='section-title'>📊 {t['annual_trend']}</div>", unsafe_allow_html=True)

fig_annual = go.Figure()

if tourist_type in [t["all_types"], t["inbound"]]:
    fig_annual.add_trace(go.Bar(
        x=f_years, y=f_inbound, name=t["inbound"],
        marker_color=accent_blue,
        marker_line_color=accent_blue,
        opacity=0.85
    ))
if tourist_type in [t["all_types"], t["domestic"]]:
    fig_annual.add_trace(go.Bar(
        x=f_years, y=f_domestic, name=t["domestic"],
        marker_color=accent_teal,
        opacity=0.85
    ))
if tourist_type == t["all_types"]:
    fig_annual.add_trace(go.Scatter(
        x=f_years, y=f_total, name=t["total"],
        line=dict(color=accent_gold, width=2.5, dash='dot'),
        marker=dict(size=7, color=accent_gold),
        yaxis='y2'
    ))

fig_annual.add_vrect(x0=2019.5, x1=2021.5,
    fillcolor=accent_red, opacity=0.07,
    annotation_text="COVID-19",
    annotation=dict(font_color=accent_red, font_size=11))

fig_annual.update_layout(
    template=plotly_template,
    paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
    height=380, barmode='group',
    margin=dict(l=10, r=10, t=20, b=10),
    legend=dict(orientation="h", y=-0.12, font=dict(size=11)),
    xaxis=dict(showgrid=False, tickfont=dict(size=11)),
    yaxis=dict(title=t["tourists_m"], showgrid=True, gridcolor=border_color,
               tickfont=dict(size=10)),
    yaxis2=dict(overlaying='y', side='right', showgrid=False,
                title=f"{t['total']} (M)", tickfont=dict(size=10)),
    font=dict(color=text_primary),
    bargap=0.25
)
st.plotly_chart(fig_annual, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════
# CHART 2+3: Purpose + Split
# ══════════════════════════════════════════
col_l, col_r = st.columns([3, 2])

with col_l:
    st.markdown(f"<div class='section-title'>🎯 {t['by_purpose']}</div>", unsafe_allow_html=True)

    purpose_colors = {
        "Religious": accent_gold,
        "Leisure":   accent_teal,
        "Business":  accent_blue,
        "VFR":       accent_purple,
        "Other":     text_secondary,
    }
    fig_purpose = go.Figure()
    for purpose, values in purpose_data.items():
        fv = values[idx_s:idx_e]
        fig_purpose.add_trace(go.Bar(
            x=f_years, y=fv,
            name=t[purpose.lower().replace(" ","")],
            marker_color=purpose_colors[purpose],
            opacity=0.88
        ))
    fig_purpose.update_layout(
        template=plotly_template,
        paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=320, barmode='stack',
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.18, font=dict(size=10)),
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor=border_color, tickfont=dict(size=10)),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_purpose, use_container_width=True, config={"displayModeBar": False})

with col_r:
    st.markdown(f"<div class='section-title'>⚖️ {t['inbound_vs_dom']}</div>", unsafe_allow_html=True)

    fig_split = go.Figure()
    total_f = [a+b for a,b in zip(f_inbound, f_domestic)]
    inb_pct = [round(a/c*100,1) for a,c in zip(f_inbound, total_f)]
    dom_pct = [round(b/c*100,1) for b,c in zip(f_domestic, total_f)]

    fig_split.add_trace(go.Bar(
        x=f_years, y=inb_pct, name=t["inbound"],
        marker_color=accent_blue, opacity=0.88
    ))
    fig_split.add_trace(go.Bar(
        x=f_years, y=dom_pct, name=t["domestic"],
        marker_color=accent_teal, opacity=0.88
    ))
    fig_split.update_layout(
        template=plotly_template,
        paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=320, barmode='stack',
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.18, font=dict(size=10)),
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor=border_color,
                   tickfont=dict(size=10), ticksuffix="%"),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_split, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════
# CHART 4: Monthly Distribution
# ══════════════════════════════════════════
st.markdown(f"<div class='section-title'>📅 {t['monthly_trend']}</div>", unsafe_allow_html=True)

fig_monthly = go.Figure()
fig_monthly.add_trace(go.Scatter(
    x=months, y=monthly_inbound,
    name=t["inbound"],
    line=dict(color=accent_blue, width=2.5),
    fill='tozeroy', fillcolor=f"{accent_blue}20",
    marker=dict(size=8, color=accent_blue,
                line=dict(color=bg_card, width=2))
))
fig_monthly.add_trace(go.Scatter(
    x=months, y=monthly_domestic,
    name=t["domestic"],
    line=dict(color=accent_teal, width=2.5),
    fill='tozeroy', fillcolor=f"{accent_teal}20",
    marker=dict(size=8, color=accent_teal,
                line=dict(color=bg_card, width=2))
))
# Annotations
fig_monthly.add_annotation(x="Mar", y=2.80,
    text="Inbound Peak<br>Ramadan/Umrah",
    showarrow=True, arrowhead=2,
    font=dict(size=10, color=accent_blue),
    arrowcolor=accent_blue, ay=-40)
fig_monthly.add_annotation(x="Jul", y=9.61,
    text="Domestic Peak<br>Summer",
    showarrow=True, arrowhead=2,
    font=dict(size=10, color=accent_teal),
    arrowcolor=accent_teal, ay=-40)

fig_monthly.update_layout(
    template=plotly_template,
    paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
    height=320, margin=dict(l=10, r=10, t=20, b=10),
    legend=dict(orientation="h", y=-0.12, font=dict(size=11)),
    xaxis=dict(showgrid=False, tickfont=dict(size=11)),
    yaxis=dict(title=t["tourists_m"], showgrid=True,
               gridcolor=border_color, tickfont=dict(size=10)),
    font=dict(color=text_primary),
)
st.plotly_chart(fig_monthly, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════
# CHART 5 + COVID TABLE
# ══════════════════════════════════════════
heatmap_col, covid_col = st.columns([3, 2])

with heatmap_col:
    st.markdown(f"<div class='section-title'>🌡️ {t['purpose_heatmap']}</div>", unsafe_allow_html=True)

    heat_data = []
    purposes_list = ["Religious","Leisure","Business","VFR","Other"]
    for p in purposes_list:
        heat_data.append(purpose_data[p])

    fig_heat = go.Figure(go.Heatmap(
        z=heat_data,
        x=[str(y) for y in years],
        y=[t[p.lower().replace(" ","")] for p in purposes_list],
        colorscale=[[0, bg_card2], [0.5, accent_blue], [1, accent_teal]],
        showscale=True,
        text=[[f"{v:.1f}M" for v in row] for row in heat_data],
        texttemplate="%{text}",
        textfont=dict(size=9, color=text_primary),
        hovertemplate="<b>%{y}</b><br>%{x}: %{z:.2f}M<extra></extra>"
    ))
    fig_heat.update_layout(
        template=plotly_template,
        paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=280, margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10)),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})

with covid_col:
    st.markdown(f"<div class='section-title'>😷 {t['covid_analysis']}</div>", unsafe_allow_html=True)

    covid_rows = [
        (t["inbound"],  "17.53M", "4.14M",  "29.73M", "-76.4%", "+618.6%"),
        (t["domestic"], "47.81M", "42.11M", "86.16M", "-11.9%", "+104.6%"),
        (t["total"],    "65.33M", "46.25M","115.89M", "-29.2%", "+150.6%"),
    ]
    table_html = f"""
    <table class='covid-table'>
      <thead>
        <tr>
          <th>{t['filter_type']}</th>
          <th>{t['pre_covid']}</th>
          <th>{t['during_covid']}</th>
          <th>{t['post_covid']}</th>
          <th>2019→2020
