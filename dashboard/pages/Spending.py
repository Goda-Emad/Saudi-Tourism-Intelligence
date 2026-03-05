# ═══════════════════════════════════════════════════════════════════
#  Saudi Tourism Intelligence — Spending Analysis
#  Author : Eng. Goda Emad   |   Design : DataSaudi
# ═══════════════════════════════════════════════════════════════════
import streamlit as st
import plotly.graph_objects as go
import base64, os, sys

# ── Path setup ───────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in [_HERE, _ROOT]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="Spending Analysis · Saudi Tourism Intelligence",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

for k, v in [("lang", "EN"), ("theme", "dark")]:
    if k not in st.session_state:
        st.session_state[k] = v

THEME, LANG = render_sidebar()

# ── Colors ───────────────────────────────────────────────────────
C = {
    "teal":"#17B19B","teal_act":"#149581","bg":"#1A1E1F",
    "sec_bg":"#161B1C","card_bg":"#1E2528","navbar":"#031414",
    "white":"#F4F9F8","grey":"#A1A6B7","foot_txt":"#B5B8B7",
    "border":"#2A3235","orange":"#F4D044","gold":"#C9A84C",
    "blue":"#3A86FF","green":"#22C55E","red":"#EF4444","purple":"#BB86FC",
} if THEME == "dark" else {
    "teal":"#17B19B","teal_act":"#149581","bg":"#F0F5F4",
    "sec_bg":"#E4EDEB","card_bg":"#FFFFFF","navbar":"#172025",
    "white":"#F4F9F8","grey":"#9DBFBA","foot_txt":"#9DBFBA",
    "border":"#2A3235","orange":"#E8A020","gold":"#C9A84C",
    "blue":"#1565C0","green":"#16A34A","red":"#DC2626","purple":"#6A1B9A",
}

def clr(k): return C.get(k, C["teal"])
ff       = "Tajawal" if LANG == "AR" else "IBM Plex Sans"
dir_val  = "rtl"     if LANG == "AR" else "ltr"
txt_dark = "#F4F9F8" if THEME == "dark" else "#0D1A1E"

# Shorthand aliases
bg_main        = C["bg"]
bg_card        = C["card_bg"]
bg_card2       = C["sec_bg"]
text_primary   = txt_dark
text_secondary = C["grey"]
accent_teal    = C["teal"]
accent_gold    = C["gold"]
accent_blue    = C["blue"]
accent_green   = C["green"]
accent_red     = C["red"]
accent_purple  = C["purple"]
border_color   = C["border"]
chart_bg       = "rgba(0,0,0,0)"
plotly_template = "plotly_dark" if THEME == "dark" else "plotly_white"

# ── Helper: hex → rgba ───────────────────────────────────────────
def rgba(hex_color, alpha=0.15):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"

# ── Logo ─────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def _b64(p):
    try:
        with open(os.path.join(_ROOT, p), "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

logo_b64 = _b64("assets/logo.jpg")
logo_src = "data:image/jpeg;base64," + logo_b64 if logo_b64 else ""
logo_img = (f'<img src="{logo_src}" style="height:42px;border-radius:8px;"/>'
            if logo_src else '<span style="font-size:2rem;">🇸🇦</span>')

# ── Translations ─────────────────────────────────────────────────
TR = {
"EN": {
    "page_title":"💰 Spending Analysis",
    "subtitle":"Inbound vs Domestic · Per Trip · Per Night · Expenditure by Purpose",
    "avg_trip_in":"Avg Spend/Trip (Inbound)","avg_trip_dom":"Avg Spend/Trip (Domestic)",
    "avg_night_in":"Avg Spend/Night (Inbound)","avg_night_dom":"Avg Spend/Night (Domestic)",
    "spend_ratio":"Inbound vs Domestic Ratio",
    "trip_trend":"Average Spending per Trip — Trend",
    "night_trend":"Average Spending per Night — Trend",
    "expenditure":"Total Expenditure by Purpose (Billions SAR)",
    "monthly_spend":"Monthly Spending Pattern",
    "spend_compare":"Spending Comparison: Key Milestones",
    "inbound":"Inbound","domestic":"Domestic",
    "religious":"Religious","leisure":"Leisure",
    "business":"Business","vfr":"VFR","other":"Other",
    "sar":"SAR","billions":"Billions SAR",
    "filter_type":"Tourist Type","all_types":"All",
    "insight_title":"Key Insights",
    "i1":"Inbound tourists spend 4x more than Domestic per trip (SAR 5,007 vs SAR 1,242)",
    "i2":"Religious purpose generates the highest total expenditure — 391 Billion SAR (2014–2022)",
    "i3":"Best single month: August 2019 — SAR 13,053 per Inbound trip",
    "i4":"Inbound spending collapsed -35% in 2020 (COVID) then surged to SAR 5,907 in 2022",
    "growth_label":"Growth 2015 to 2024","covid_low":"COVID Low (2020)","peak_spend":"Peak Spending",
},
"AR": {
    "page_title":"💰 تحليل الإنفاق",
    "subtitle":"وافد مقابل محلي · لكل رحلة · لكل ليلة · الإنفاق حسب الغرض",
    "avg_trip_in":"متوسط إنفاق/رحلة (وافد)","avg_trip_dom":"متوسط إنفاق/رحلة (محلي)",
    "avg_night_in":"متوسط إنفاق/ليلة (وافد)","avg_night_dom":"متوسط إنفاق/ليلة (محلي)",
    "spend_ratio":"نسبة الوافد للمحلي",
    "trip_trend":"متوسط الإنفاق لكل رحلة — الاتجاه",
    "night_trend":"متوسط الإنفاق لكل ليلة — الاتجاه",
    "expenditure":"إجمالي الإنفاق حسب الغرض (مليار ريال)",
    "monthly_spend":"النمط الشهري للإنفاق",
    "spend_compare":"مقارنة الإنفاق: المحطات الرئيسية",
    "inbound":"وافد","domestic":"محلي",
    "religious":"ديني","leisure":"ترفيه",
    "business":"أعمال","vfr":"زيارة أهل","other":"أخرى",
    "sar":"ريال","billions":"مليار ريال",
    "filter_type":"نوع السائح","all_types":"الكل",
    "insight_title":"أبرز الاستنتاجات",
    "i1":"الوافدون ينفقون 4 أضعاف المحليين لكل رحلة (5,007 مقابل 1,242 ريال)",
    "i2":"الغرض الديني يولد أعلى إنفاق إجمالي — 391 مليار ريال (2014–2022)",
    "i3":"أفضل شهر: أغسطس 2019 — 13,053 ريال لكل رحلة وافدة",
    "i4":"إنفاق الوافدين انهار -35% في 2020 ثم قفز لـ 5,907 ريال في 2022",
    "growth_label":"نمو 2015 إلى 2024","covid_low":"أدنى كوفيد (2020)","peak_spend":"ذروة الإنفاق",
},
}
t = TR[LANG]

# ── Data ─────────────────────────────────────────────────────────
years          = list(range(2015, 2025))
inbound_trip   = [4598,4923,5524,5538,5304,3469,4181,5907,5007,5622]
domestic_trip  = [1043,1235,1052,1114,1284,1029,1586,1352,1390,1336]
inbound_night  = [392, 420, 435, 448, 436, 318, 398, 510, 430, 482]
domestic_night = [190, 204, 195, 198, 209, 182, 241, 218, 214, 234]

MONTHS_EN  = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTHS_AR  = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
months_lbl = MONTHS_AR if LANG == "AR" else MONTHS_EN

monthly_inbound_spend  = [5200,5800,6200,5100,4800,5400,6800,7200,5600,4900,5300,6100]
monthly_domestic_spend = [1100,1050,1150,1200,1300,1400,1600,1550,1200,1100,1050,1250]

exp_purposes = ["Religious","Business","VFR","Leisure","Other"]
exp_inbound  = [391.20,123.60,71.10,34.52,29.09]
exp_domestic = [82.40, 65.30, 95.20,45.60,83.50]
exp_labels   = [t["religious"],t["business"],t["vfr"],t["leisure"],t["other"]]
exp_colors   = [accent_gold, accent_blue, accent_purple, accent_teal, C["grey"]]

# ════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ════════════════════════════════════════════════════════════════════
st.markdown(
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700"
    "&family=IBM+Plex+Mono:wght@400;600;700&family=Tajawal:wght@400;700;800&display=swap');"
    "[data-testid='stHeader'],[data-testid='stToolbar'],"
    "[data-testid='stSidebarNav'],footer,#MainMenu{display:none!important;}"
    ".block-container{padding:0!important;max-width:100%!important;}"
    "section[data-testid='stMain']>div:first-child{padding-top:0!important;}"
    ".ds-card{transition:transform .22s,box-shadow .22s;}"
    ".ds-card:hover{transform:translateY(-3px);"
    "box-shadow:0 10px 28px rgba(23,177,155,.18)!important;}"
    f"html,body,[data-testid='stAppViewContainer'],[data-testid='stMain']"
    f"{{background:{C['bg']}!important;direction:{dir_val};"
    f"font-family:'{ff}',sans-serif;color:{txt_dark}!important;}}"
    "</style>",
    unsafe_allow_html=True)

# ── Helpers ──────────────────────────────────────────────────────
def sec_head(badge, h2):
    return (
        f'<div style="margin-bottom:18px;">'
        f'<div style="display:inline-block;background:{C["gold"]}15;'
        f'border:1px solid {C["gold"]}44;color:{C["gold"]};'
        f'font-size:.57rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;'
        f'padding:4px 12px;border-radius:4px;margin-bottom:10px;">{badge}</div>'
        f'<div style="font-size:1.25rem;font-weight:700;color:{txt_dark};">{h2}</div>'
        f'</div>')

def kpi_card(ico, lbl, val, sub, ck):
    return (
        f'<div class="ds-card" style="background:{C["card_bg"]};border:1px solid {C["border"]};'
        f'border-top:3px solid {clr(ck)};border-radius:10px;padding:20px 16px;text-align:center;">'
        f'<div style="font-size:1.4rem;margin-bottom:6px;">{ico}</div>'
        f'<div style="font-size:1.45rem;font-weight:800;color:{clr(ck)};'
        f'font-family:IBM Plex Mono,monospace;letter-spacing:-1px;line-height:1.1;">{val}</div>'
        f'<div style="font-size:.62rem;color:{C["grey"]};text-transform:uppercase;'
        f'letter-spacing:.8px;font-weight:600;margin:6px 0 4px;">{lbl}</div>'
        f'<div style="font-size:.72rem;color:{C["grey"]};font-family:IBM Plex Mono,monospace;">{sub}</div>'
        f'</div>')

def apply_layout(fig, height=340):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=C["grey"], family=ff),
        height=height, margin=dict(l=10,r=10,t=36,b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11),
                    orientation="h", y=-0.14),
        xaxis=dict(gridcolor="rgba(42,50,53,0.4)", linecolor="#2A3235",
                   tickfont=dict(size=10), showgrid=False),
        yaxis=dict(gridcolor="rgba(42,50,53,0.4)", linecolor="#2A3235",
                   tickfont=dict(size=10)),
    )
    return fig

def chart(fig):
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div style="background:{C["navbar"]};border-bottom:1px solid {C["border"]};'
    f'padding:24px 40px 20px;">'
    f'<div style="display:inline-block;background:{C["gold"]}22;border:1px solid {C["gold"]}55;'
    f'color:{C["gold"]};font-size:.57rem;font-weight:700;letter-spacing:2.5px;'
    f'text-transform:uppercase;padding:4px 12px;border-radius:4px;margin-bottom:10px;">'
    f'SPENDING · EXPENDITURE ANALYSIS</div>'
    f'<div style="font-size:1.85rem;font-weight:800;color:#F4F9F8;'
    f'letter-spacing:-.5px;margin-bottom:5px;">{t["page_title"]}</div>'
    f'<div style="font-size:.82rem;color:#A1A6B7;">{t["subtitle"]}</div>'
    f'</div>',
    unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# KPI STRIP
# ════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div style="padding:20px 40px 0;">'
    f'<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;">'
    + kpi_card("✈️💰", t["avg_trip_in"],   "SAR 5,007", "All-years avg", "gold")
    + kpi_card("🏠💰", t["avg_trip_dom"],  "SAR 1,242", "All-years avg", "teal")
    + kpi_card("🌙💰", t["avg_night_in"],  "SAR 482",   "Per night",     "blue")
    + kpi_card("🏡💰", t["avg_night_dom"], "SAR 234",   "Per night",     "purple")
    + kpi_card("⚖️",   t["spend_ratio"],   "4.0×",      "Inbound/Dom",   "red")
    + '</div></div>',
    unsafe_allow_html=True)

st.markdown(f'<div style="height:1px;background:{C["border"]};margin:20px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# FILTERS
# ════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding:16px 40px 0;">', unsafe_allow_html=True)
fc, yc = st.columns([1, 2])
with fc:
    tourist_filter = st.radio(
        t["filter_type"],
        [t["all_types"], t["inbound"], t["domestic"]],
        horizontal=True, key="spend_tf")
with yc:
    year_range = st.slider(
        "Year Range", min_value=2015, max_value=2024,
        value=(2015, 2024), key="spend_yr")
st.markdown('</div>', unsafe_allow_html=True)

# Slice data by year range
y_s, y_e   = year_range
idx_s      = years.index(y_s)
idx_e      = years.index(y_e) + 1
f_years    = years[idx_s:idx_e]

# ════════════════════════════════════════════════════════════════════
# CHART 1+2 — Trip Trend | Night Trend
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:24px 40px 0;">{sec_head("TREND", t["trip_trend"])}</div>',
            unsafe_allow_html=True)

st.markdown('<div style="padding:0 40px;">', unsafe_allow_html=True)
trip_col, night_col = st.columns(2, gap="large")

with trip_col:
    fig_trip = go.Figure()
    if tourist_filter in [t["all_types"], t["inbound"]]:
        fig_trip.add_trace(go.Scatter(
            x=f_years, y=inbound_trip[idx_s:idx_e], name=t["inbound"],
            line=dict(color=accent_gold, width=2.5),
            fill='tozeroy', fillcolor=rgba(accent_gold, 0.12),
            marker=dict(size=8, color=accent_gold,
                        line=dict(color=bg_card, width=2)),
            hovertemplate="<b>%{x}</b>: SAR %{y:,}<extra></extra>"
        ))
    if tourist_filter in [t["all_types"], t["domestic"]]:
        fig_trip.add_trace(go.Scatter(
            x=f_years, y=domestic_trip[idx_s:idx_e], name=t["domestic"],
            line=dict(color=accent_teal, width=2.5),
            fill='tozeroy', fillcolor=rgba(accent_teal, 0.12),
            marker=dict(size=8, color=accent_teal,
                        line=dict(color=bg_card, width=2)),
            hovertemplate="<b>%{x}</b>: SAR %{y:,}<extra></extra>"
        ))
    fig_trip.add_vrect(x0=2019.5, x1=2021.5,
        fillcolor=rgba(accent_red, 0.07), line_width=0,
        annotation_text="COVID",
        annotation=dict(font_color=accent_red, font_size=10))
    apply_layout(fig_trip, height=300)
    fig_trip.update_yaxes(title_text=t["sar"], tickprefix="SAR ")
    chart(fig_trip)

with night_col:
    st.markdown(sec_head("NIGHTLY", t["night_trend"]), unsafe_allow_html=True)
    fig_night = go.Figure()
    if tourist_filter in [t["all_types"], t["inbound"]]:
        fig_night.add_trace(go.Bar(
            x=f_years, y=inbound_night[idx_s:idx_e],
            name=t["inbound"], marker_color=accent_blue, opacity=0.85,
            hovertemplate="<b>%{x}</b>: SAR %{y}<extra></extra>"))
    if tourist_filter in [t["all_types"], t["domestic"]]:
        fig_night.add_trace(go.Bar(
            x=f_years, y=domestic_night[idx_s:idx_e],
            name=t["domestic"], marker_color=accent_teal, opacity=0.85,
            hovertemplate="<b>%{x}</b>: SAR %{y}<extra></extra>"))
    apply_layout(fig_night, height=300)
    fig_night.update_layout(barmode='group', bargap=0.25)
    fig_night.update_yaxes(title_text=t["sar"], tickprefix="SAR ")
    chart(fig_night)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# CHART 3+4 — Expenditure by Purpose | Monthly
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:24px 40px 0;">{sec_head("EXPENDITURE", t["expenditure"])}</div>',
            unsafe_allow_html=True)

st.markdown('<div style="padding:0 40px;">', unsafe_allow_html=True)
exp_col, monthly_col = st.columns([3, 2], gap="large")

with exp_col:
    fig_exp = go.Figure()
    fig_exp.add_trace(go.Bar(
        x=exp_labels, y=exp_inbound, name=t["inbound"],
        marker_color=exp_colors, opacity=0.9,
        text=[f"{v:.1f}B" for v in exp_inbound],
        textposition='outside',
        textfont=dict(size=10, color=txt_dark),
        hovertemplate="<b>%{x}</b> Inbound: %{y:.1f}B SAR<extra></extra>"))
    fig_exp.add_trace(go.Bar(
        x=exp_labels, y=exp_domestic, name=t["domestic"],
        marker_color=[rgba(c, 0.55) for c in exp_colors], opacity=0.9,
        text=[f"{v:.1f}B" for v in exp_domestic],
        textposition='outside',
        textfont=dict(size=10, color=txt_dark),
        hovertemplate="<b>%{x}</b> Domestic: %{y:.1f}B SAR<extra></extra>"))
    apply_layout(fig_exp, height=320)
    fig_exp.update_layout(barmode='group', bargap=0.2)
    fig_exp.update_yaxes(title_text=t["billions"])
    chart(fig_exp)

with monthly_col:
    st.markdown(sec_head("MONTHLY", t["monthly_spend"]), unsafe_allow_html=True)
    fig_monthly = go.Figure()
    if tourist_filter in [t["all_types"], t["inbound"]]:
        fig_monthly.add_trace(go.Scatter(
            x=months_lbl, y=monthly_inbound_spend, name=t["inbound"],
            line=dict(color=accent_gold, width=2.5),
            fill='tozeroy', fillcolor=rgba(accent_gold, 0.12),
            marker=dict(size=7),
            hovertemplate="<b>%{x}</b>: SAR %{y:,}<extra></extra>"))
    if tourist_filter in [t["all_types"], t["domestic"]]:
        fig_monthly.add_trace(go.Scatter(
            x=months_lbl, y=monthly_domestic_spend, name=t["domestic"],
            line=dict(color=accent_teal, width=2.5),
            fill='tozeroy', fillcolor=rgba(accent_teal, 0.12),
            marker=dict(size=7),
            hovertemplate="<b>%{x}</b>: SAR %{y:,}<extra></extra>"))
    apply_layout(fig_monthly, height=320)
    fig_monthly.update_layout(
        xaxis=dict(tickfont=dict(size=9), tickangle=45))
    fig_monthly.update_yaxes(title_text=t["sar"], tickprefix="SAR ")
    chart(fig_monthly)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# COMPARISON CARDS + DONUT
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:24px 40px 0;">{sec_head("MILESTONES", t["spend_compare"])}</div>',
            unsafe_allow_html=True)

st.markdown('<div style="padding:0 40px;">', unsafe_allow_html=True)
cmp_col1, cmp_col2, cmp_col3 = st.columns(3, gap="large")

def cmp_row(lbl, val, color):
    return (f'<div style="display:flex;justify-content:space-between;align-items:center;'
            f'padding:8px 0;border-bottom:1px solid {C["border"]};">'
            f'<span style="font-size:.82rem;color:{txt_dark};font-weight:500;">{lbl}</span>'
            f'<span style="font-size:.85rem;font-weight:700;font-family:IBM Plex Mono,monospace;'
            f'color:{color};">{val}</span></div>')

with cmp_col1:
    st.markdown(
        f'<div class="ds-card" style="background:{C["card_bg"]};border:1px solid {C["border"]};'
        f'border-radius:14px;padding:20px;">'
        f'<div style="font-size:.78rem;font-weight:700;color:{C["grey"]};text-transform:uppercase;'
        f'letter-spacing:.8px;margin-bottom:16px;">✈️ {t["inbound"]} — {t["avg_trip_in"]}</div>'
        + cmp_row("2015",             "SAR 4,598", C["grey"])
        + cmp_row(t["covid_low"],     "SAR 3,469", accent_red)
        + cmp_row(t["peak_spend"],    "SAR 5,907", accent_gold)
        + cmp_row("2024",             "SAR 5,622", accent_teal)
        + cmp_row(t["growth_label"],  "+22.3%",    accent_green)
        + '</div>', unsafe_allow_html=True)

with cmp_col2:
    st.markdown(
        f'<div class="ds-card" style="background:{C["card_bg"]};border:1px solid {C["border"]};'
        f'border-radius:14px;padding:20px;">'
        f'<div style="font-size:.78rem;font-weight:700;color:{C["grey"]};text-transform:uppercase;'
        f'letter-spacing:.8px;margin-bottom:16px;">🏠 {t["domestic"]} — {t["avg_trip_dom"]}</div>'
        + cmp_row("2015",             "SAR 1,043", C["grey"])
        + cmp_row(t["covid_low"],     "SAR 1,029", accent_red)
        + cmp_row(t["peak_spend"],    "SAR 1,586", accent_gold)
        + cmp_row("2024",             "SAR 1,336", accent_teal)
        + cmp_row(t["growth_label"],  "+28.1%",    accent_green)
        + '</div>', unsafe_allow_html=True)

with cmp_col3:
    fig_donut = go.Figure(go.Pie(
        labels=exp_labels, values=exp_inbound, hole=0.60,
        marker=dict(colors=exp_colors, line=dict(color=bg_main, width=2)),
        textfont=dict(size=10),
        hovertemplate="<b>%{label}</b><br>%{value:.1f}B SAR<extra></extra>"
    ))
    fig_donut.add_annotation(
        text=f"<b>649B</b><br>Total", x=0.5, y=0.5,
        showarrow=False, font=dict(size=12, color=txt_dark))
    apply_layout(fig_donut, height=280)
    fig_donut.update_layout(
        showlegend=True,
        legend=dict(orientation="v", font=dict(size=9), x=1.0),
        title=dict(text="Inbound Expenditure Split",
                   font=dict(size=11), x=0.5))
    chart(fig_donut)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# KEY INSIGHTS
# ════════════════════════════════════════════════════════════════════
insights = [
    ("💰", t["i1"], "gold"),
    ("🕌", t["i2"], "purple"),
    ("🏆", t["i3"], "blue"),
    ("📉", t["i4"], "red"),
]
ins_html = f'<div style="padding:24px 40px 40px;">{sec_head("INSIGHTS", t["insight_title"])}'
ins_html += f'<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;">'
for ico, txt_val, ck in insights:
    ins_html += (
        f'<div style="background:{C["card_bg"]};border:1px solid {C["border"]};'
        f'border-left:3px solid {clr(ck)};border-radius:12px;'
        f'padding:14px 16px;display:flex;align-items:flex-start;gap:10px;">'
        f'<div style="font-size:1.2rem;flex-shrink:0;margin-top:2px;">{ico}</div>'
        f'<div style="font-size:.83rem;color:{txt_dark};line-height:1.65;">{txt_val}</div>'
        f'</div>')
ins_html += '</div></div>'
st.markdown(ins_html, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div style="background:{C["navbar"]};border-top:2px solid {C["teal"]};'
    f'padding:22px 40px;display:flex;justify-content:space-between;'
    f'align-items:center;flex-wrap:wrap;gap:12px;">'
    f'<div style="display:flex;align-items:center;gap:14px;">{logo_img}'
    f'<div>'
    f'<div style="font-size:.88rem;font-weight:700;color:{C["teal"]};">Saudi Tourism Intelligence</div>'
    f'<div style="font-size:.66rem;color:#B5B8B7;margin-top:2px;">💰 Spending · Eng. Goda Emad</div>'
    f'</div></div>'
    f'<div style="display:flex;gap:20px;">'
    f'<a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" target="_blank" '
    f'style="font-size:.75rem;color:#B5B8B7;text-decoration:none;">🐙 GitHub</a>'
    f'<a href="https://datasaudi.sa" target="_blank" '
    f'style="font-size:.75rem;color:{C["teal"]};text-decoration:none;font-weight:600;">📊 DataSaudi</a>'
    f'</div></div>',
    unsafe_allow_html=True)
