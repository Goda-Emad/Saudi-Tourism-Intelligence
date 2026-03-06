# ═══════════════════════════════════════════════════════════════════
#  Saudi Tourism Intelligence — Tourist Trends
#  Author : Eng. Goda Emad   |   Design : DataSaudi
# ═══════════════════════════════════════════════════════════════════
import streamlit as st
import plotly.graph_objects as go
import base64, os, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in [_HERE, _ROOT]:
    if _p not in sys.path: sys.path.insert(0, _p)

from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="Tourist Trends · Saudi Tourism Intelligence",
    page_icon="📈", layout="wide",
    initial_sidebar_state="expanded",
)
for k, v in [("lang","EN"),("theme","dark")]:
    if k not in st.session_state: st.session_state[k] = v

THEME, LANG = render_sidebar()

# ── Colors — v3 Professional Palette ────────────────────────────
C = {
    "teal":"#17B19B","teal_act":"#149581","bg":"#1A1E1F",
    "sec_bg":"#161B1C","card_bg":"#1E2528","navbar":"#031414",
    "white":"#F4F9F8","grey":"#A1A6B7","foot_txt":"#B5B8B7",
    "border":"#2A3235",
    "blue":  "#4D9FFF",
    "gold":  "#D4A843",
    "green": "#2ECC71",
    "red":   "#FF4757",
    "orange":"#FF7F3F",
    "purple":"#C67FFF",
    "p_religious":"#E85D75",
    "p_leisure":  "#17B19B",
    "p_business": "#4D9FFF",
    "p_vfr":      "#FF7F3F",
    "p_other":    "#8B95A8",
} if THEME=="dark" else {
    "teal":"#17B19B","teal_act":"#149581","bg":"#F0F5F4",
    "sec_bg":"#E4EDEB","card_bg":"#FFFFFF","navbar":"#172025",
    "white":"#0D1A1E","grey":"#4A5568","foot_txt":"#6B7280",
    "border":"#CBD5E0",
    "blue":  "#1565C0",
    "gold":  "#B8892A",
    "green": "#16A34A",
    "red":   "#DC2626",
    "orange":"#E06010",
    "purple":"#6A1B9A",
    "p_religious":"#C0304A",
    "p_leisure":  "#17B19B",
    "p_business": "#1565C0",
    "p_vfr":      "#E06010",
    "p_other":    "#6B7280",
}

def clr(k): return C.get(k, C["teal"])
ff      = "Tajawal" if LANG=="AR" else "IBM Plex Sans"
dir_val = "rtl"     if LANG=="AR" else "ltr"
txt_col = C["white"]

accent_teal   = C["teal"]
accent_gold   = C["gold"]
accent_blue   = C["blue"]
accent_green  = C["green"]
accent_red    = C["red"]
accent_purple = C["purple"]
bg_card       = C["card_bg"]

purpose_colors = {
    "Religious": C["p_religious"],
    "Leisure":   C["p_leisure"],
    "Business":  C["p_business"],
    "VFR":       C["p_vfr"],
    "Other":     C["p_other"],
}

def rgba(hex_color, alpha=0.15):
    h = hex_color.lstrip('#')
    r,g,b = int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"

@st.cache_data(show_spinner=False)
def _b64(p):
    try:
        with open(os.path.join(_ROOT,p),"rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

logo_b64 = _b64("assets/logo.jpg")
logo_src = "data:image/jpeg;base64,"+logo_b64 if logo_b64 else ""
logo_img = (f'<img src="{logo_src}" style="height:42px;border-radius:8px;"/>'
            if logo_src else '<span style="font-size:2rem;">🇸🇦</span>')

TR = {
"EN":{
    "page_title":"📈 Tourist Trends 2015–2024",
    "subtitle":"Annual & Monthly Tourist Analysis · Inbound vs Domestic",
    "total_2024":"Total Tourists 2024","inbound_2024":"Inbound 2024",
    "domestic_2024":"Domestic 2024","yoy_growth":"YoY Growth 2024",
    "covid_drop":"COVID Drop 2020","recovery":"Recovery ×",
    "annual_trend":"Annual Tourist Trend 2015–2024",
    "by_purpose":"Tourists by Purpose (Annual)",
    "inbound_vs_dom":"Inbound vs Domestic Split",
    "monthly_trend":"Monthly Tourist Distribution (2024)",
    "purpose_heatmap":"Purpose Heatmap by Year",
    "covid_analysis":"COVID-19 Impact Analysis",
    "total":"Total","inbound":"Inbound","domestic":"Domestic",
    "religious":"Religious","leisure":"Leisure","business":"Business",
    "vfr":"VFR","other":"Other","year":"Year","tourists_m":"Tourists (Millions)",
    "filter_type":"Tourist Type","filter_year":"Year Range","all_types":"All",
    "insight_title":"Key Insights",
    "i1":"2024 reached all-time high: 115.9M tourists — +6.2% YoY vs 2023",
    "i2":"Domestic tourism is 3× larger than Inbound (86.2M vs 29.7M)",
    "i3":"Leisure surpassed Religious as #1 purpose for Inbound tourists in 2024",
    "i4":"COVID caused -29.2% drop in 2020, Inbound surged +618% by 2024 vs 2020",
    "pre_covid":"Pre-COVID (2019)","during_covid":"COVID (2020)",
    "post_covid":"Post-COVID (2024)","change":"Change",
},
"AR":{
    "page_title":"📈 اتجاهات السياحة 2015–2024",
    "subtitle":"تحليل سنوي وشهري · الوافدون مقابل المحليون",
    "total_2024":"إجمالي السياح 2024","inbound_2024":"الوافدون 2024",
    "domestic_2024":"المحليون 2024","yoy_growth":"نمو سنوي 2024",
    "covid_drop":"انخفاض كوفيد 2020","recovery":"معدل التعافي ×",
    "annual_trend":"الاتجاه السنوي للسياحة 2015–2024",
    "by_purpose":"السياح حسب الغرض (سنوي)",
    "inbound_vs_dom":"الوافدون مقابل المحليون",
    "monthly_trend":"التوزيع الشهري للسياح (2024)",
    "purpose_heatmap":"خريطة الغرض السياحي حسب السنة",
    "covid_analysis":"تحليل تأثير كوفيد-19",
    "total":"الإجمالي","inbound":"وافد","domestic":"محلي",
    "religious":"ديني","leisure":"ترفيه","business":"أعمال",
    "vfr":"زيارة أهل","other":"أخرى","year":"السنة",
    "tourists_m":"السياح (مليون)",
    "filter_type":"نوع السائح","filter_year":"نطاق السنوات","all_types":"الكل",
    "insight_title":"أبرز الاستنتاجات",
    "i1":"2024 سجّل أعلى رقم تاريخي: 115.9M سائح — +6.2% سنوياً مقارنة بـ 2023",
    "i2":"السياحة المحلية أكبر 3× من الوافدة (86.2M مقابل 29.7M)",
    "i3":"الترفيه تجاوز الديني كأول غرض سياحي للوافدين في 2024",
    "i4":"كوفيد تسبب في انخفاض -29.2% عام 2020، ارتفع الوافدون +618% بحلول 2024",
    "pre_covid":"ما قبل كوفيد (2019)","during_covid":"كوفيد (2020)",
    "post_covid":"ما بعد كوفيد (2024)","change":"التغيير",
},
}
t = TR[LANG]

# ── Data ─────────────────────────────────────────────────────────
years          = list(range(2015,2025))
inbound_annual = [17.99,18.04,16.11,15.33,17.53,4.14,3.48,16.64,27.18,29.73]
domestic_annual= [46.45,45.04,43.82,43.26,47.81,42.11,63.83,77.84,81.92,86.16]
total_annual   = [a+b for a,b in zip(inbound_annual,domestic_annual)]

purpose_data = {
    "Religious": [8.00,7.50,7.00,6.80,8.37,0.80,0.60,5.50,9.50,12.30],
    "Leisure":   [3.00,3.20,2.80,2.60,2.99,0.90,1.00,4.80,6.20, 7.50],
    "Business":  [2.40,2.60,2.20,2.10,2.13,0.60,0.50,1.80,2.50, 2.00],
    "VFR":       [3.10,3.20,2.80,2.60,2.82,1.20,1.00,3.20,5.00, 5.95],
    "Other":     [1.49,1.54,1.31,1.23,1.22,0.64,0.38,1.34,3.98, 2.00],
}

MONTHS_EN = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTHS_AR = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
months    = MONTHS_AR if LANG=="AR" else MONTHS_EN

monthly_inbound  = [2.75,2.37,3.11,2.58,2.10,2.36,2.47,2.40,2.15,2.09,2.47,2.88]
monthly_domestic = [7.48,5.72,6.14,5.73,5.14,8.44,10.32,8.58,6.22,5.77,7.90,8.72]

# ════════════════════════════════════════════════════════════════════
# CSS
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
    f"font-family:'{ff}',sans-serif;color:{txt_col}!important;}}"
    f"[data-testid='stMain'] label,[data-testid='stMain'] p,"
    f"[data-testid='stMain'] span,[data-testid='stWidgetLabel'] p,"
    f"[data-testid='stSlider'] span,[data-testid='stSlider'] p,"
    f".stRadio label div p{{color:{txt_col}!important;}}"
    f".covid-table{{width:100%;border-collapse:collapse;font-size:.85rem;}}"
    f".covid-table th{{background:{C['sec_bg']};color:{C['grey']};padding:10px 14px;"
    f"text-align:left;font-size:.72rem;text-transform:uppercase;letter-spacing:.8px;"
    f"border-bottom:1px solid {C['border']};}}"
    f".covid-table td{{padding:10px 14px;color:{txt_col};"
    f"border-bottom:1px solid {C['border']};"
    f"font-family:'IBM Plex Mono',monospace;font-size:.82rem;}}"
    ".covid-table tr:last-child td{border-bottom:none;}"
    "</style>",
    unsafe_allow_html=True)

# ── helpers ──────────────────────────────────────────────────────
def sec_head(badge, h2):
    return (
        f'<div style="margin-bottom:18px;">'
        f'<div style="display:inline-block;background:{C["blue"]}22;'
        f'border:1px solid {C["blue"]}55;color:{C["blue"]};'
        f'font-size:.57rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;'
        f'padding:4px 12px;border-radius:4px;margin-bottom:10px;">{badge}</div>'
        f'<div style="font-size:1.25rem;font-weight:700;color:{txt_col};">{h2}</div>'
        f'</div>')

def kpi_card(ico,lbl,val,delta,ck,dc):
    return (
        f'<div class="ds-card" style="background:{C["card_bg"]};border:1px solid {C["border"]};'
        f'border-top:3px solid {clr(ck)};border-radius:10px;padding:20px 16px;text-align:center;">'
        f'<div style="font-size:1.4rem;margin-bottom:6px;">{ico}</div>'
        f'<div style="font-size:1.45rem;font-weight:800;color:{clr(ck)};'
        f'font-family:IBM Plex Mono,monospace;letter-spacing:-1px;line-height:1.1;">{val}</div>'
        f'<div style="font-size:.62rem;color:{C["grey"]};text-transform:uppercase;'
        f'letter-spacing:.8px;font-weight:600;margin:6px 0 4px;">{lbl}</div>'
        f'<div style="font-size:.75rem;font-weight:700;color:{clr(dc)};">{delta}</div>'
        f'</div>')

def apply_layout(fig, height=340):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=C["grey"], family=ff),
        height=height, margin=dict(l=10,r=10,t=36,b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11, color=txt_col),
                    orientation="h", y=-0.14),
        xaxis=dict(gridcolor="rgba(42,50,53,0.4)", linecolor=C["border"],
                   tickfont=dict(size=10), showgrid=False),
        yaxis=dict(gridcolor="rgba(42,50,53,0.4)", linecolor=C["border"],
                   tickfont=dict(size=10)))
    return fig

def chart(fig):
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

def divider():
    st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
                unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div style="background:{C["navbar"]};border-bottom:1px solid {C["border"]};'
    f'padding:24px 40px 20px;">'
    f'<div style="display:inline-block;background:{C["blue"]}22;border:1px solid {C["blue"]}55;'
    f'color:{C["blue"]};font-size:.57rem;font-weight:700;letter-spacing:2.5px;'
    f'text-transform:uppercase;padding:4px 12px;border-radius:4px;margin-bottom:10px;">'
    f'TOURIST TRENDS · 2015–2024</div>'
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
    +kpi_card("🌍",t["total_2024"],   "115.9M","+6.2%",  "teal",  "green")
    +kpi_card("✈️",t["inbound_2024"], "29.7M", "+9.4%",  "blue",  "green")
    +kpi_card("🏠",t["domestic_2024"],"86.2M", "+5.2%",  "gold",  "green")
    +kpi_card("😷",t["covid_drop"],   "-29.2%","2020",   "red",   "red")
    +kpi_card("🚀",t["recovery"],     "1.72×", "2021→24","purple","green")
    +'</div></div>',
    unsafe_allow_html=True)

st.markdown(f'<div style="height:1px;background:{C["border"]};margin:20px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# FILTERS
# ════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding:16px 40px 0;">', unsafe_allow_html=True)
fc, yc = st.columns([1,2])
with fc:
    tourist_type = st.radio(t["filter_type"],
        [t["all_types"],t["inbound"],t["domestic"]],
        horizontal=True, key="tt_tf")
with yc:
    year_range = st.slider(t["filter_year"], 2015, 2024, (2015,2024), key="tt_yr")
st.markdown('</div>', unsafe_allow_html=True)

y_start, y_end = year_range
idx_s      = years.index(y_start)
idx_e      = years.index(y_end)+1
f_years    = years[idx_s:idx_e]
f_inbound  = inbound_annual[idx_s:idx_e]
f_domestic = domestic_annual[idx_s:idx_e]
f_total    = total_annual[idx_s:idx_e]

show_inb = tourist_type in [t["all_types"],t["inbound"]]
show_dom = tourist_type in [t["all_types"],t["domestic"]]

# ════════════════════════════════════════════════════════════════════
# CHART 1 — Annual Trend
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:24px 40px 0;">{sec_head("ANNUAL",t["annual_trend"])}</div>',
            unsafe_allow_html=True)
st.markdown('<div style="padding:0 40px;">', unsafe_allow_html=True)
fig_annual = go.Figure()

if show_dom:
    fig_annual.add_trace(go.Bar(
        x=f_years, y=f_domestic, name=t["domestic"],
        marker_color=accent_teal, opacity=0.90,
        hovertemplate="<b>%{x}</b>: %{y:.2f}M<extra></extra>"))
if show_inb:
    fig_annual.add_trace(go.Bar(
        x=f_years, y=f_inbound, name=t["inbound"],
        marker_color=accent_blue, opacity=0.90,
        hovertemplate="<b>%{x}</b>: %{y:.2f}M<extra></extra>"))
if tourist_type == t["all_types"]:
    fig_annual.add_trace(go.Scatter(
        x=f_years, y=f_total, name=t["total"],
        line=dict(color=accent_gold, width=2.5, dash='dot'),
        marker=dict(size=7, color=accent_gold,
                    line=dict(color=C["bg"], width=1.5)),
        yaxis='y2',
        hovertemplate="<b>%{x}</b> Total: %{y:.2f}M<extra></extra>"))

if y_start <= 2020 <= y_end:
    fig_annual.add_vrect(x0=2019.5, x1=2021.5,
        fillcolor=rgba(accent_red, 0.08), line_width=0,
        annotation_text="COVID-19",
        annotation=dict(font_color=accent_red, font_size=11))

apply_layout(fig_annual, height=380)
fig_annual.update_layout(
    barmode='group', bargap=0.22,
    yaxis=dict(title=t["tourists_m"], showgrid=True,
               gridcolor="rgba(42,50,53,0.4)", tickfont=dict(size=10)),
    yaxis2=dict(overlaying='y', side='right', showgrid=False,
                title=f"{t['total']} (M)", tickfont=dict(size=10)))
chart(fig_annual)
st.markdown('</div>', unsafe_allow_html=True)
divider()

# ════════════════════════════════════════════════════════════════════
# CHARTS 2+3 — Purpose | Split
# ════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding:24px 40px 0;">', unsafe_allow_html=True)
col_l, col_r = st.columns([3,2], gap="large")

with col_l:
    st.markdown(sec_head("PURPOSE",t["by_purpose"]), unsafe_allow_html=True)
    fig_purpose = go.Figure()
    for purpose, values in purpose_data.items():
        fig_purpose.add_trace(go.Bar(
            x=f_years, y=values[idx_s:idx_e],
            name=t[purpose.lower()],
            marker_color=purpose_colors[purpose], opacity=0.92,
            hovertemplate=f"<b>{purpose}</b> %{{x}}: %{{y:.2f}}M<extra></extra>"))
    apply_layout(fig_purpose, height=320)
    fig_purpose.update_layout(barmode='stack', bargap=0.2)
    chart(fig_purpose)

with col_r:
    st.markdown(sec_head("SPLIT",t["inbound_vs_dom"]), unsafe_allow_html=True)
    total_f = [a+b for a,b in zip(f_inbound,f_domestic)]
    inb_pct = [round(a/c*100,1) for a,c in zip(f_inbound,total_f)]
    dom_pct = [round(b/c*100,1) for b,c in zip(f_domestic,total_f)]
    fig_split = go.Figure()
    fig_split.add_trace(go.Bar(
        x=f_years, y=dom_pct, name=t["domestic"],
        marker_color=accent_teal, opacity=0.90,
        hovertemplate="<b>%{x}</b> Domestic: %{y:.1f}%<extra></extra>"))
    fig_split.add_trace(go.Bar(
        x=f_years, y=inb_pct, name=t["inbound"],
        marker_color=accent_blue, opacity=0.90,
        hovertemplate="<b>%{x}</b> Inbound: %{y:.1f}%<extra></extra>"))
    apply_layout(fig_split, height=320)
    fig_split.update_layout(barmode='stack', bargap=0.2)
    fig_split.update_yaxes(ticksuffix="%")
    chart(fig_split)

st.markdown('</div>', unsafe_allow_html=True)
divider()

# ════════════════════════════════════════════════════════════════════
# CHART 4 — Monthly Distribution
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:24px 40px 0;">{sec_head("MONTHLY",t["monthly_trend"])}</div>',
            unsafe_allow_html=True)
st.markdown('<div style="padding:0 40px;">', unsafe_allow_html=True)
fig_monthly = go.Figure()
fig_monthly.add_trace(go.Scatter(
    x=months, y=monthly_domestic, name=t["domestic"],
    line=dict(color=accent_teal, width=2.5),
    fill='tozeroy', fillcolor=rgba(accent_teal, 0.13),
    marker=dict(size=8, color=accent_teal,
                line=dict(color=bg_card, width=2)),
    hovertemplate="<b>%{x}</b>: %{y:.2f}M<extra></extra>"))
fig_monthly.add_trace(go.Scatter(
    x=months, y=monthly_inbound, name=t["inbound"],
    line=dict(color=accent_blue, width=2.5),
    fill='tozeroy', fillcolor=rgba(accent_blue, 0.13),
    marker=dict(size=8, color=accent_blue,
                line=dict(color=bg_card, width=2)),
    hovertemplate="<b>%{x}</b>: %{y:.2f}M<extra></extra>"))
fig_monthly.add_annotation(
    x=months[2], y=max(monthly_inbound),
    text="Inbound Peak\nRamadan/Umrah" if LANG=="EN" else "ذروة الوافدين\nرمضان/عمرة",
    showarrow=True, arrowhead=2,
    font=dict(size=10, color=accent_blue), arrowcolor=accent_blue, ay=-40,
    bgcolor=C["card_bg"], bordercolor=accent_blue, borderwidth=1, borderpad=3)
fig_monthly.add_annotation(
    x=months[6], y=max(monthly_domestic),
    text="Domestic Peak\nSummer" if LANG=="EN" else "ذروة المحليين\nالصيف",
    showarrow=True, arrowhead=2,
    font=dict(size=10, color=accent_teal), arrowcolor=accent_teal, ay=-40,
    bgcolor=C["card_bg"], bordercolor=accent_teal, borderwidth=1, borderpad=3)
apply_layout(fig_monthly, height=320)
fig_monthly.update_yaxes(title_text=t["tourists_m"])
chart(fig_monthly)
st.markdown('</div>', unsafe_allow_html=True)
divider()

# ════════════════════════════════════════════════════════════════════
# CHART 5 + COVID TABLE
# ════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding:24px 40px 0;">', unsafe_allow_html=True)
heatmap_col, covid_col = st.columns([3,2], gap="large")

with heatmap_col:
    st.markdown(sec_head("HEATMAP",t["purpose_heatmap"]), unsafe_allow_html=True)
    purposes_list = ["Religious","Leisure","Business","VFR","Other"]
    heat_data = [purpose_data[p] for p in purposes_list]
    fig_heat = go.Figure(go.Heatmap(
        z=heat_data,
        x=[str(y) for y in years],
        y=[t[p.lower()] for p in purposes_list],
        colorscale=[
            [0.00, C["sec_bg"]],
            [0.30, C["p_business"]],
            [0.65, C["p_leisure"]],
            [1.00, C["p_religious"]],
        ],
        showscale=True,
        xgap=3, ygap=3,
        text=[[f"{v:.1f}M" for v in row] for row in heat_data],
        texttemplate="%{text}",
        textfont=dict(size=9, color=txt_col),
        hovertemplate="<b>%{y}</b><br>%{x}: %{z:.2f}M<extra></extra>"))
    apply_layout(fig_heat, height=280)
    fig_heat.update_layout(
        yaxis=dict(type="category", tickfont=dict(size=10, color=txt_col)),
        xaxis=dict(tickfont=dict(size=10, color=txt_col)),
        margin=dict(l=10,r=10,t=10,b=10))
    chart(fig_heat)

with covid_col:
    st.markdown(sec_head("COVID",t["covid_analysis"]), unsafe_allow_html=True)
    covid_rows = [
        (t["inbound"],  "17.53M","4.14M", "29.73M","-76.4%", "+618.6%"),
        (t["domestic"], "47.81M","42.11M","86.16M", "-11.9%", "+104.6%"),
        (t["total"],    "65.34M","46.25M","115.89M","-29.2%", "+150.6%"),
    ]
    table_html = (
        f"<table class='covid-table'><thead><tr>"
        f"<th>{t['filter_type']}</th>"
        f"<th>{t['pre_covid']}</th>"
        f"<th>{t['during_covid']}</th>"
        f"<th>{t['post_covid']}</th>"
        f"<th>2019→2020</th><th>2020→2024</th>"
        f"</tr></thead><tbody>")
    for row in covid_rows:
        table_html += (
            f"<tr>"
            f"<td style='font-weight:700;color:{txt_col};'>{row[0]}</td>"
            f"<td>{row[1]}</td><td>{row[2]}</td>"
            f"<td style='color:{accent_teal};font-weight:700;'>{row[3]}</td>"
            f"<td style='color:{accent_red};font-weight:700;'>{row[4]}</td>"
            f"<td style='color:{accent_green};font-weight:700;'>{row[5]}</td>"
            f"</tr>")
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
divider()

# ════════════════════════════════════════════════════════════════════
# KEY INSIGHTS
# ════════════════════════════════════════════════════════════════════
insights = [
    ("🏆",t["i1"],"teal"),
    ("🏠",t["i2"],"gold"),
    ("🏖️",t["i3"],"blue"),
    ("😷",t["i4"],"red"),
]
ins_html = (f'<div style="padding:24px 40px 40px;">{sec_head("INSIGHTS",t["insight_title"])}'
            f'<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;">')
for ico, txt_i, ck in insights:
    ins_html += (
        f'<div style="background:{C["card_bg"]};border:1px solid {C["border"]};'
        f'border-left:3px solid {clr(ck)};border-radius:12px;'
        f'padding:14px 16px;display:flex;align-items:flex-start;gap:10px;">'
        f'<div style="font-size:1.2rem;flex-shrink:0;margin-top:2px;">{ico}</div>'
        f'<div style="font-size:.83rem;color:{txt_col};line-height:1.65;">{txt_i}</div>'
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
    f'<div><div style="font-size:.88rem;font-weight:700;color:{C["teal"]};">Saudi Tourism Intelligence</div>'
    f'<div style="font-size:.66rem;color:{C["foot_txt"]};margin-top:2px;">📈 Tourist Trends · Eng. Goda Emad</div>'
    f'</div></div>'
    f'<div style="display:flex;gap:20px;">'
    f'<a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" target="_blank" '
    f'style="font-size:.75rem;color:{C["foot_txt"]};text-decoration:none;">🐙 GitHub</a>'
    f'<a href="https://datasaudi.sa" target="_blank" '
    f'style="font-size:.75rem;color:{C["teal"]};text-decoration:none;font-weight:600;">📊 DataSaudi</a>'
    f'</div></div>',
    unsafe_allow_html=True)
