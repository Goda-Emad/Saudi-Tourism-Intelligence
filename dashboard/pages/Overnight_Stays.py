# ═══════════════════════════════════════════════════════════════════
#  Saudi Tourism Intelligence — Overnight Stays
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
    page_title="Overnight Stays · Saudi Tourism Intelligence",
    page_icon="🏨", layout="wide",
    initial_sidebar_state="expanded",
)

for k, v in [("lang","EN"),("theme","dark")]:
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
} if THEME=="dark" else {
    "teal":"#17B19B","teal_act":"#149581","bg":"#F0F5F4",
    "sec_bg":"#E4EDEB","card_bg":"#FFFFFF","navbar":"#172025",
    "white":"#F4F9F8","grey":"#9DBFBA","foot_txt":"#9DBFBA",
    "border":"#2A3235","orange":"#E8A020","gold":"#C9A84C",
    "blue":"#1565C0","green":"#16A34A","red":"#DC2626","purple":"#6A1B9A",
}
def clr(k): return C.get(k, C["teal"])
ff      = "Tajawal" if LANG=="AR" else "IBM Plex Sans"
dir_val = "rtl"     if LANG=="AR" else "ltr"

# ── Logo ─────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def _b64(p):
    try:
        with open(os.path.join(_ROOT, p), "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

logo_b64 = _b64("assets/logo.jpg")
logo_src = "data:image/jpeg;base64,"+logo_b64 if logo_b64 else ""
logo_img = (f'<img src="{logo_src}" style="height:42px;border-radius:8px;"/>'
            if logo_src else '<span style="font-size:2rem;">🇸🇦</span>')

# ── Translations ─────────────────────────────────────────────────
TR = {
"EN":{
    "title":"🏨 Overnight Stays Analysis",
    "sub_pg":"Annual & Monthly Patterns · Length of Stay · COVID Recovery · Inbound vs Domestic",
    "f_type":"Tourist Type","f_all":"All","f_year":"Year Range",
    "kpi_total":"Total Stays 2024","kpi_inb":"Inbound Nights 2024",
    "kpi_dom":"Domestic Nights 2024","kpi_los_in":"Avg Stay — Inbound",
    "kpi_los_dom":"Avg Stay — Domestic",
    "s1":"ANNUAL TREND","s1h":"Annual Overnight Stays 2015–2024",
    "s2":"LENGTH OF STAY","s2h":"Average Length of Stay per Tourist Type",
    "s3":"MONTHLY PATTERN","s3h":"Monthly Distribution of Overnight Stays",
    "s4":"INBOUND VS DOMESTIC","s4h":"Share of Overnight Stays by Type (%)",
    "s5":"COVID-19 IMPACT","s5h":"Collapse & Recovery Analysis",
    "s6":"KEY INSIGHTS","s6h":"Overnight Intelligence",
    "inbound":"Inbound","domestic":"Domestic","total":"Total",
    "nights":"Nights","nights_k":"Stays (Thousands)","nights_m":"Stays (Millions)",
    "pre_covid":"Pre-COVID (2019)","covid_yr":"COVID (2020)","post_covid":"Post-COVID (2024)",
    "drop":"Drop","recovery":"Recovery","growth":"Recovery Growth 2021–2024",
    "ins":[
        ("🏆","2024: Inbound nights (560M) surpassed Domestic (539M) for the first time ever!","teal"),
        ("⏰","Inbound avg stay surged: 8.6 nights (2021) → 19.2 nights (2024) — +123%","blue"),
        ("😷","COVID caused -80% collapse in Inbound nights vs only -15% for Domestic","red"),
        ("🚀","Inbound recovery 2021→2024: +1,663% — one of the fastest globally","green"),
    ],
},
"AR":{
    "title":"🏨 تحليل ليالي الإقامة",
    "sub_pg":"الأنماط السنوية والشهرية · مدة الإقامة · تعافي كوفيد · الوافد مقابل المحلي",
    "f_type":"نوع السائح","f_all":"الكل","f_year":"نطاق السنوات",
    "kpi_total":"إجمالي الليالي 2024","kpi_inb":"ليالي الوافدين 2024",
    "kpi_dom":"ليالي المحليين 2024","kpi_los_in":"متوسط الإقامة — وافد",
    "kpi_los_dom":"متوسط الإقامة — محلي",
    "s1":"الاتجاه السنوي","s1h":"ليالي الإقامة السنوية 2015–2024",
    "s2":"مدة الإقامة","s2h":"متوسط مدة الإقامة حسب نوع السائح",
    "s3":"النمط الشهري","s3h":"التوزيع الشهري لليالي الإقامة",
    "s4":"الوافد مقابل المحلي","s4h":"حصة ليالي الإقامة حسب النوع (%)",
    "s5":"تأثير كوفيد-19","s5h":"تحليل الانهيار والتعافي",
    "s6":"الاستنتاجات الرئيسية","s6h":"ذكاء ليالي الإقامة",
    "inbound":"وافد","domestic":"محلي","total":"إجمالي",
    "nights":"ليالي","nights_k":"الليالي (ألف)","nights_m":"الليالي (مليون)",
    "pre_covid":"قبل كوفيد (2019)","covid_yr":"كوفيد (2020)","post_covid":"بعد كوفيد (2024)",
    "drop":"انخفاض","recovery":"تعافي","growth":"نمو التعافي 2021–2024",
    "ins":[
        ("🏆","2024: ليالي الوافدين (560M) تجاوزت المحليين (539M) لأول مرة في التاريخ!","teal"),
        ("⏰","متوسط إقامة الوافد: 8.6 ليلة (2021) → 19.2 ليلة (2024) — +123%","blue"),
        ("😷","كوفيد تسبب في انهيار -80% في ليالي الوافدين مقابل -15% فقط للمحليين","red"),
        ("🚀","تعافي الوافدين 2021→2024: +1,663% — من أسرع التعافيات السياحية عالمياً","green"),
    ],
},
}
t = TR[LANG]

# ── Data ─────────────────────────────────────────────────────────
YEARS = list(range(2015, 2025))
INB_STAYS = [193084,187225,171036,173929,189036,37824,31771,270728,432299,560227]
DOM_STAYS = [240853,235804,224212,232122,268751,228538,353331,369606,495341,538618]
TOT_STAYS = [a+b for a,b in zip(INB_STAYS,DOM_STAYS)]

LOS_INB = [10.36,9.90,9.54,10.10,9.79,5.90,8.58,16.56,15.65,19.22]
LOS_DOM = [5.15,5.23,5.09,5.34,5.62,5.31,5.41,4.58,5.93,6.11]

MONTHS_EN = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTHS_AR = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
MONTHS    = MONTHS_AR if LANG=="AR" else MONTHS_EN

MON_INB = [18923,17234,22745,19876,16543,18234,19876,18543,16234,15876,18234,20890]
MON_DOM = [28765,24532,26543,25432,22345,35678,39225,36543,28765,26543,32456,38765]

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
    ".ds-card{transition:transform .22s,box-shadow .22s,border-color .22s;}"
    ".ds-card:hover{transform:translateY(-3px);"
    "box-shadow:0 10px 28px rgba(23,177,155,.18)!important;}"
    f"html,body,[data-testid='stAppViewContainer'],[data-testid='stMain']"
    f"{{background:{C['bg']}!important;direction:{dir_val};"
    f"font-family:'{ff}',sans-serif;color:{C['white']}!important;}}"
    "</style>",
    unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════════
def sec_head(badge, h2):
    return (
        f'<div style="margin-bottom:18px;">'
        f'<div style="display:inline-block;background:{C["teal"]}15;'
        f'border:1px solid {C["teal"]}44;color:{C["teal"]};'
        f'font-size:.57rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;'
        f'padding:4px 12px;border-radius:4px;margin-bottom:10px;">{badge}</div>'
        f'<div style="font-size:1.25rem;font-weight:700;color:{C["white"]};">{h2}</div>'
        f'</div>')

def kpi_card(ico, lbl, val, sub, ck):
    return (
        f'<div class="ds-card" style="background:{C["card_bg"]};border:1px solid {C["border"]};'
        f'border-top:3px solid {clr(ck)};border-radius:10px;padding:20px 16px;text-align:center;">'
        f'<div style="font-size:1.4rem;margin-bottom:6px;">{ico}</div>'
        f'<div style="font-size:1.5rem;font-weight:800;color:{clr(ck)};'
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
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

# ════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div style="background:{C["navbar"]};border-bottom:1px solid {C["border"]};'
    f'padding:24px 40px 20px;">'
    f'<div style="display:inline-block;background:{C["blue"]}22;border:1px solid {C["blue"]}55;'
    f'color:{C["blue"]};font-size:.57rem;font-weight:700;letter-spacing:2.5px;'
    f'text-transform:uppercase;padding:4px 12px;border-radius:4px;margin-bottom:10px;">'
    f'OVERNIGHT STAYS · LENGTH OF STAY</div>'
    f'<div style="font-size:1.85rem;font-weight:800;color:#F4F9F8;'
    f'letter-spacing:-.5px;margin-bottom:5px;">{t["title"]}</div>'
    f'<div style="font-size:.82rem;color:#A1A6B7;">{t["sub_pg"]}</div>'
    f'</div>',
    unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# KPI STRIP
# ════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div style="padding:24px 40px 0;">'
    f'<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;">'
    +kpi_card("🌙",t["kpi_total"],"1.10B","+19.1% YoY","teal")
    +kpi_card("✈️",t["kpi_inb"],"560M","+29.6% YoY","blue")
    +kpi_card("🏠",t["kpi_dom"],"539M","+8.7% YoY","gold")
    +kpi_card("⏰",t["kpi_los_in"],"19.2 nights","+23% YoY","purple")
    +kpi_card("🏡",t["kpi_los_dom"],"6.1 nights","+3% YoY","green")
    +'</div></div>',
    unsafe_allow_html=True)

st.markdown(f'<div style="height:1px;background:{C["border"]};margin:20px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# FILTERS
# ════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding:16px 40px 0;">', unsafe_allow_html=True)
fc1, fc2 = st.columns([1,3])
with fc1:
    tourist_filter = st.radio(
        t["f_type"],
        [t["f_all"], t["inbound"], t["domestic"]],
        horizontal=True, key="tf")
with fc2:
    year_range = st.slider(
        t["f_year"], 2015, 2024, (2015, 2024), key="yr")
st.markdown('</div>', unsafe_allow_html=True)

y_s, y_e   = year_range
idx_s      = YEARS.index(y_s)
idx_e      = YEARS.index(y_e) + 1
f_years    = YEARS[idx_s:idx_e]
f_inb      = INB_STAYS[idx_s:idx_e]
f_dom      = DOM_STAYS[idx_s:idx_e]
f_tot      = TOT_STAYS[idx_s:idx_e]
f_los_inb  = LOS_INB[idx_s:idx_e]
f_los_dom  = LOS_DOM[idx_s:idx_e]

show_inb = tourist_filter in [t["f_all"], t["inbound"]]
show_dom = tourist_filter in [t["f_all"], t["domestic"]]

# ════════════════════════════════════════════════════════════════════
# CHART 1 — Annual Trend
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:20px 40px 0;">{sec_head(t["s1"],t["s1h"])}</div>',
            unsafe_allow_html=True)

fig1 = go.Figure()
if show_inb:
    fig1.add_trace(go.Bar(
        x=f_years, y=[v/1000 for v in f_inb],
        name=t["inbound"], marker_color=C["blue"], opacity=0.88,
        hovertemplate="%{x}: <b>%{y:.0f}M nights</b><extra></extra>"))
if show_dom:
    fig1.add_trace(go.Bar(
        x=f_years, y=[v/1000 for v in f_dom],
        name=t["domestic"], marker_color=C["teal"], opacity=0.88,
        hovertemplate="%{x}: <b>%{y:.0f}M nights</b><extra></extra>"))
if tourist_filter == t["f_all"]:
    fig1.add_trace(go.Scatter(
        x=f_years, y=[v/1000 for v in f_tot],
        name=t["total"], line=dict(color=C["gold"], width=2.5, dash='dot'),
        marker=dict(size=7), yaxis='y2',
        hovertemplate="%{x}: <b>%{y:.0f}M total</b><extra></extra>"))

fig1.add_vrect(x0=2019.5, x1=2021.5,
    fillcolor="rgba(239,68,68,0.08)", line_width=0,
    annotation_text="COVID-19",
    annotation_font=dict(color=C["red"], size=10))

apply_layout(fig1, height=360)
fig1.update_layout(
    barmode='group', bargap=0.25,
    yaxis=dict(title=t["nights_m"], gridcolor="rgba(42,50,53,0.4)",
               tickfont=dict(size=10)),
    yaxis2=dict(overlaying='y', side='right', showgrid=False,
                title=f"Total ({t['nights_m']})", tickfont=dict(size=10)))

st.markdown('<div style="padding:0 40px;">', unsafe_allow_html=True)
chart(fig1)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# CHARTS 2+3 — Length of Stay | Monthly Distribution
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:28px 40px 0;">', unsafe_allow_html=True)
c2, c3 = st.columns(2, gap="large")

with c2:
    st.markdown(sec_head(t["s2"], t["s2h"]), unsafe_allow_html=True)
    fig2 = go.Figure()
    if show_inb:
        fig2.add_trace(go.Scatter(
            x=f_years, y=f_los_inb,
            name=t["inbound"], line=dict(color=C["blue"], width=2.5),
            fill='tozeroy', fillcolor="rgba(58,134,255,0.1)",
            marker=dict(size=8, color=C["blue"], line=dict(color=C["navbar"],width=2)),
            text=[f"{v:.1f}" for v in f_los_inb],
            textposition='top center', mode='lines+markers+text',
            textfont=dict(size=9, color=C["blue"])))
    if show_dom:
        fig2.add_trace(go.Scatter(
            x=f_years, y=f_los_dom,
            name=t["domestic"], line=dict(color=C["teal"], width=2.5),
            fill='tozeroy', fillcolor="rgba(23,177,155,0.1)",
            marker=dict(size=8, color=C["teal"], line=dict(color=C["navbar"],width=2)),
            text=[f"{v:.1f}" for v in f_los_dom],
            textposition='top center', mode='lines+markers+text',
            textfont=dict(size=9, color=C["teal"])))
    if y_e == 2024:
        fig2.add_annotation(x=2024, y=19.22,
            text="🏆 19.2 nights — All-time high",
            showarrow=True, arrowhead=2,
            font=dict(size=9, color=C["gold"]),
            arrowcolor=C["gold"], ay=-40,
            bgcolor=C["card_bg"], bordercolor=C["gold"],
            borderwidth=1, borderpad=3)
    apply_layout(fig2, height=320)
    fig2.update_yaxes(title_text=t["nights"])
    chart(fig2)

with c3:
    st.markdown(sec_head(t["s3"], t["s3h"]), unsafe_allow_html=True)
    fig3 = go.Figure()
    if show_inb:
        fig3.add_trace(go.Scatter(
            x=MONTHS, y=MON_INB,
            name=t["inbound"], line=dict(color=C["blue"], width=2.5),
            fill='tozeroy', fillcolor="rgba(58,134,255,0.1)",
            marker=dict(size=7, color=C["blue"]),
            hovertemplate="<b>%{x}</b>: %{y:,}K<extra></extra>"))
    if show_dom:
        fig3.add_trace(go.Scatter(
            x=MONTHS, y=MON_DOM,
            name=t["domestic"], line=dict(color=C["teal"], width=2.5),
            fill='tozeroy', fillcolor="rgba(23,177,155,0.1)",
            marker=dict(size=7, color=C["teal"]),
            hovertemplate="<b>%{x}</b>: %{y:,}K<extra></extra>"))
    # Peak annotations
    fig3.add_annotation(x="Mar" if LANG=="EN" else "مارس", y=22745,
        text="Inbound Peak" if LANG=="EN" else "ذروة الوافدين",
        showarrow=True, arrowhead=2,
        font=dict(size=9, color=C["blue"]),
        arrowcolor=C["blue"], ay=-35)
    fig3.add_annotation(x="Jul" if LANG=="EN" else "يوليو", y=39225,
        text="Domestic Peak" if LANG=="EN" else "ذروة المحليين",
        showarrow=True, arrowhead=2,
        font=dict(size=9, color=C["teal"]),
        arrowcolor=C["teal"], ay=-35)
    apply_layout(fig3, height=320)
    fig3.update_layout(
        xaxis=dict(tickangle=45, tickfont=dict(size=9), showgrid=False))
    fig3.update_yaxes(title_text=t["nights_k"])
    chart(fig3)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# CHARTS 4+5 — Split % | COVID Impact Table + Recovery Chart
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:28px 40px 0;">', unsafe_allow_html=True)
c4, c5 = st.columns([2,3], gap="large")

with c4:
    st.markdown(sec_head(t["s4"], t["s4h"]), unsafe_allow_html=True)
    inb_pct = [round(a/(a+b)*100,1) for a,b in zip(f_inb, f_dom)]
    dom_pct = [round(b/(a+b)*100,1) for a,b in zip(f_inb, f_dom)]
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=f_years, y=inb_pct, name=t["inbound"],
        marker_color=C["blue"], opacity=0.88,
        hovertemplate="%{x}: <b>%{y}%</b><extra></extra>"))
    fig4.add_trace(go.Bar(
        x=f_years, y=dom_pct, name=t["domestic"],
        marker_color=C["teal"], opacity=0.88,
        hovertemplate="%{x}: <b>%{y}%</b><extra></extra>"))
    apply_layout(fig4, height=300)
    fig4.update_layout(barmode='stack')
    fig4.update_yaxes(ticksuffix="%")
    chart(fig4)

with c5:
    st.markdown(sec_head(t["s5"], t["s5h"]), unsafe_allow_html=True)

    # COVID comparison table
    covid_rows = [
        (t["inbound"],  "189,036K", "37,824K",  "560,227K", "-80.0%", "+1,663%"),
        (t["domestic"], "268,751K", "228,538K", "538,618K", "-15.0%",   "+136%"),
        (t["total"],    "457,787K", "266,362K","1,098,845K","-41.8%",   "+312%"),
    ]
    th = (f'<th style="background:{C["sec_bg"]};color:{C["grey"]};padding:8px 10px;'
          f'text-align:right;font-size:.68rem;text-transform:uppercase;'
          f'letter-spacing:.8px;border-bottom:1px solid {C["border"]};">')
    th_l = th.replace("text-align:right", "text-align:left")
    tbl = (f'<table style="width:100%;border-collapse:collapse;font-size:.8rem;">'
           f'<thead><tr>'
           f'{th_l}{t["f_type"]}</th>'
           f'{th}{t["pre_covid"]}</th>'
           f'{th}{t["covid_yr"]}</th>'
           f'{th}{t["post_covid"]}</th>'
           f'{th}{t["drop"]}</th>'
           f'{th}{t["recovery"]}</th>'
           f'</tr></thead><tbody>')
    for row in covid_rows:
        tbl += (f'<tr>'
                f'<td style="padding:8px 10px;color:#F4F9F8;font-weight:700;'
                f'border-bottom:1px solid {C["border"]};">{row[0]}</td>'
                f'<td style="padding:8px 10px;color:{C["grey"]};text-align:right;'
                f'font-family:IBM Plex Mono,monospace;border-bottom:1px solid {C["border"]};">{row[1]}</td>'
                f'<td style="padding:8px 10px;color:{C["red"]};text-align:right;font-weight:700;'
                f'font-family:IBM Plex Mono,monospace;border-bottom:1px solid {C["border"]};">{row[2]}</td>'
                f'<td style="padding:8px 10px;color:{C["teal"]};text-align:right;font-weight:700;'
                f'font-family:IBM Plex Mono,monospace;border-bottom:1px solid {C["border"]};">{row[3]}</td>'
                f'<td style="padding:8px 10px;color:{C["red"]};text-align:right;font-weight:700;'
                f'font-family:IBM Plex Mono,monospace;border-bottom:1px solid {C["border"]};">{row[4]}</td>'
                f'<td style="padding:8px 10px;color:{C["green"]};text-align:right;font-weight:700;'
                f'font-family:IBM Plex Mono,monospace;border-bottom:1px solid {C["border"]};">{row[5]}</td>'
                f'</tr>')
    tbl += '</tbody></table>'
    st.markdown(tbl, unsafe_allow_html=True)

    # Recovery bar chart
    st.markdown(
        f'<div style="font-size:.84rem;font-weight:700;color:#F4F9F8;'
        f'margin:16px 0 8px;">🚀 {t["growth"]}</div>',
        unsafe_allow_html=True)
    rec_yrs = [2021, 2022, 2023, 2024]
    rec_inb = [31771, 270728, 432299, 560227]
    fig5 = go.Figure(go.Bar(
        x=rec_yrs, y=[v/1000 for v in rec_inb],
        marker_color=[C["blue"],C["blue"],C["blue"],C["gold"]],
        text=[f"{v/1000:.0f}M" for v in rec_inb],
        textposition='outside',
        textfont=dict(size=10, color=C["grey"]),
        opacity=0.88,
        hovertemplate="%{x}: <b>%{y:.0f}M nights</b><extra></extra>"))
    fig5.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=C["grey"], family=ff),
        height=200, margin=dict(l=10,r=10,t=10,b=10),
        showlegend=False,
        xaxis=dict(showgrid=False, tickfont=dict(size=11)),
        yaxis=dict(gridcolor="rgba(42,50,53,0.4)", tickfont=dict(size=10)))
    chart(fig5)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# KEY INSIGHTS
# ════════════════════════════════════════════════════════════════════
ins_html = f'<div style="padding:28px 40px 40px;">{sec_head(t["s6"],t["s6h"])}'
ins_html += f'<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;">'
for ico, txt, ck in t["ins"]:
    ins_html += (
        f'<div style="background:{C["card_bg"]};border:1px solid {C["border"]};'
        f'border-left:3px solid {clr(ck)};border-radius:10px;'
        f'padding:16px 18px;display:flex;align-items:flex-start;gap:12px;">'
        f'<div style="font-size:1.2rem;flex-shrink:0;margin-top:2px;">{ico}</div>'
        f'<div style="font-size:.83rem;color:{C["white"]};line-height:1.65;">{txt}</div>'
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
    f'<div style="font-size:.66rem;color:#B5B8B7;margin-top:2px;">🏨 Overnight Stays · Eng. Goda Emad</div>'
    f'</div></div>'
    f'<div style="display:flex;gap:20px;">'
    f'<a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" target="_blank" '
    f'style="font-size:.75rem;color:#B5B8B7;text-decoration:none;">🐙 GitHub</a>'
    f'<a href="https://datasaudi.sa" target="_blank" '
    f'style="font-size:.75rem;color:{C["teal"]};text-decoration:none;font-weight:600;">📊 DataSaudi</a>'
    f'</div></div>',
    unsafe_allow_html=True)
