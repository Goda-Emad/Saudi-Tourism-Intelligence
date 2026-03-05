# ═══════════════════════════════════════════════════════════════════
#  Saudi Tourism Intelligence — Seasonality
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
    page_title="Seasonality · Saudi Tourism Intelligence",
    page_icon="📅", layout="wide",
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
    "border":"#CBD5E0","orange":"#E8A020","gold":"#C9A84C",
    "blue":"#1565C0","green":"#16A34A","red":"#DC2626","purple":"#6A1B9A",
}
def clr(k): return C.get(k, C["teal"])
ff      = "Tajawal" if LANG=="AR" else "IBM Plex Sans"
dir_val = "rtl"     if LANG=="AR" else "ltr"
txt_dark = "#F4F9F8" if THEME=="dark" else "#0D1A1E"

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
    "title":"📅 Seasonality Analysis",
    "sub_pg":"Peak & Low Seasons · Monthly Patterns · Ramadan vs Summer · Quarterly Breakdown",
    "f_type":"Tourist Type","f_all":"All",
    "kpi_peak":"Peak Month","kpi_low":"Low Month","kpi_diff":"Peak vs Low",
    "kpi_inb_peak":"Inbound Peak","kpi_dom_peak":"Domestic Peak",
    "s1":"MONTHLY AVERAGE","s1h":"Average Monthly Tourists (All Years)",
    "s2":"HEATMAP","s2h":"Monthly Heatmap by Year (Inbound, Thousands)",
    "s3":"SEASONAL COMPARE","s3h":"Inbound vs Domestic Monthly Pattern",
    "s4":"QUARTERLY","s4h":"Quarterly Tourist Distribution",
    "s5":"RADAR","s5h":"Seasonal Radar Chart — Normalized",
    "s6":"KEY INSIGHTS","s6h":"Seasonality Intelligence",
    "inbound":"Inbound","domestic":"Domestic","total":"Total",
    "tourists_m":"Tourists (Millions)",
    "q1":"Q1 · Jan–Mar","q2":"Q2 · Apr–Jun",
    "q3":"Q3 · Jul–Sep","q4":"Q4 · Oct–Dec",
    "ramadan_note":"Ramadan Effect: Inbound ↑ (Religious tourism), Domestic ↓ (travel slows)",
    "summer_note":"Summer Effect: Domestic ↑ (school holidays), Inbound ↓ (heat deterrent)",
    "ins":[
        ("🏆","January is the overall peak month at 73,127K tourists — 41% above the Low Season","gold"),
        ("✈️","Inbound peaks in December (winter tourism) — Domestic peaks in July (school holidays)","blue"),
        ("📊","Q1 (Jan–Mar) and Q3 (Jul–Sep) are nearly equal — both are high seasons","teal"),
        ("🌙","May is the lowest month — Ramadan + summer heat causes -29% below annual average","red"),
    ],
},
"AR":{
    "title":"📅 تحليل الموسمية",
    "sub_pg":"ذروة ومواسم الانخفاض · الأنماط الشهرية · رمضان مقابل الصيف · التحليل الربعي",
    "f_type":"نوع السائح","f_all":"الكل",
    "kpi_peak":"شهر الذروة","kpi_low":"أدنى شهر","kpi_diff":"الذروة مقابل الأدنى",
    "kpi_inb_peak":"ذروة الوافدين","kpi_dom_peak":"ذروة المحليين",
    "s1":"المتوسط الشهري","s1h":"متوسط السياح الشهري (كل السنوات)",
    "s2":"الخريطة الحرارية","s2h":"خريطة حرارية شهرية حسب السنة (وافد، ألف)",
    "s3":"المقارنة الموسمية","s3h":"النمط الشهري: وافد مقابل محلي",
    "s4":"التحليل الربعي","s4h":"توزيع السياح ربعياً",
    "s5":"رادار الموسمية","s5h":"مخطط رادار الموسمية — قيم معيارية",
    "s6":"الاستنتاجات الرئيسية","s6h":"ذكاء الموسمية",
    "inbound":"وافد","domestic":"محلي","total":"إجمالي",
    "tourists_m":"السياح (مليون)",
    "q1":"ر1 · يناير–مارس","q2":"ر2 · أبريل–يونيو",
    "q3":"ر3 · يوليو–سبتمبر","q4":"ر4 · أكتوبر–ديسمبر",
    "ramadan_note":"تأثير رمضان: الوافدون ↑ (السياحة الدينية)، المحليون ↓ (تباطؤ السفر)",
    "summer_note":"تأثير الصيف: المحليون ↑ (إجازات المدارس)، الوافدون ↓ (الحر الشديد)",
    "ins":[
        ("🏆","يناير هو شهر الذروة الكلية بـ 73,127 ألف سائح — أعلى بـ 41% من موسم الانخفاض","gold"),
        ("✈️","الوافدون يبلغون ذروتهم في ديسمبر (سياحة الشتاء) — المحليون في يوليو (إجازة الصيف)","blue"),
        ("📊","الربع الأول (يناير–مارس) والثالث (يوليو–سبتمبر) متقاربان — كلاهما موسم مرتفع","teal"),
        ("🌙","مايو هو الأدنى — رمضان + الحر يسببان -29% دون المتوسط السنوي","red"),
    ],
},
}
t = TR[LANG]

# ── Data ─────────────────────────────────────────────────────────
MONTHS_EN = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTHS_AR = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
MONTHS    = MONTHS_AR if LANG=="AR" else MONTHS_EN

TOT_MON = [73127,61529,62585,56938,51868,62935,67220,65582,58646,55202,66627,62376]
INB_MON = [2470, 2130, 2800, 2320, 1890, 2120, 2220, 2160, 1930, 1880, 2220, 2590]
DOM_MON = [6960, 5320, 5710, 5330, 4780, 7850, 9610, 7980, 5790, 5370, 7350, 8110]

HEAT_YEARS = list(range(2015,2025))
HEAT_DATA  = [
    [1189,1103, 978, 912, 589, 703, 701, 570, 589, 490, 487, 427],
    [1100,1050, 920, 870, 560, 670, 660, 540, 560, 460, 460, 410],
    [1000, 950, 850, 800, 500, 600, 600, 480, 500, 410, 410, 360],
    [ 980, 930, 830, 780, 490, 590, 580, 460, 480, 400, 395, 350],
    [1100,1050, 960, 900, 560, 670, 660, 540, 560, 460, 460, 410],
    [ 180, 160, 140, 130,  80, 100, 100,  80,  90,  70,  70,  60],
    [ 120, 110,  90,  85,  60,  80,  80,  60,  70,  55,  55,  50],
    [ 900, 850, 780, 720, 440, 530, 520, 420, 450, 360, 355, 315],
    [1800,1700,1560,1440, 900,1060,1050, 840, 900, 720, 720, 640],
    [2470,2130,2800,2320,1890,2120,2220,2160,1930,1880,2220,2590],
]

QUARTERS = [t["q1"],t["q2"],t["q3"],t["q4"]]
INB_Q    = [7400,  6330,  6310,  7250]
DOM_Q    = [17990, 17960, 23380, 22830]

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
    f"font-family:'{ff}',sans-serif;color:{txt_dark}!important;}}"
    f"[data-testid='stMain'] label,[data-testid='stMain'] p,"
    f"[data-testid='stMain'] span,[data-testid='stWidgetLabel'] p,"
    f".stRadio label div p{{color:{txt_dark}!important;}}"
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
        xaxis=dict(gridcolor="rgba(42,50,53,0.4)", linecolor=C["border"],
                   tickfont=dict(size=10), showgrid=False),
        yaxis=dict(gridcolor="rgba(42,50,53,0.4)", linecolor=C["border"],
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
    f'<div style="display:inline-block;background:{C["gold"]}22;border:1px solid {C["gold"]}55;'
    f'color:{C["gold"]};font-size:.57rem;font-weight:700;letter-spacing:2.5px;'
    f'text-transform:uppercase;padding:4px 12px;border-radius:4px;margin-bottom:10px;">'
    f'SEASONALITY · MONTHLY PATTERNS</div>'
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
    +kpi_card("🏆",t["kpi_peak"],"January","73,127K","gold")
    +kpi_card("📉",t["kpi_low"],"May","51,868K","red")
    +kpi_card("📊",t["kpi_diff"],"+41.0%","Peak vs Low","teal")
    +kpi_card("✈️",t["kpi_inb_peak"],"December","17,890K","blue")
    +kpi_card("🏠",t["kpi_dom_peak"],"July","58,076K","purple")
    +'</div></div>',
    unsafe_allow_html=True)

st.markdown(f'<div style="height:1px;background:{C["border"]};margin:20px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# FILTER
# ════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding:16px 40px 0;">', unsafe_allow_html=True)
tourist_filter = st.radio(
    t["f_type"],
    [t["f_all"], t["inbound"], t["domestic"]],
    horizontal=True, key="tf")
st.markdown('</div>', unsafe_allow_html=True)

if tourist_filter == t["inbound"]:
    y_data    = [v/1000 for v in INB_MON]
    bar_color = C["blue"]
elif tourist_filter == t["domestic"]:
    y_data    = [v/1000 for v in DOM_MON]
    bar_color = C["teal"]
else:
    y_data    = [v/1000 for v in TOT_MON]
    bar_color = C["gold"]

# ════════════════════════════════════════════════════════════════════
# CHART 1 — Monthly Average Bar
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:20px 40px 0;">{sec_head(t["s1"],t["s1h"])}</div>',
            unsafe_allow_html=True)

avg_val    = sum(y_data)/len(y_data)
bar_colors = [C["red"] if v==min(y_data)
              else C["green"] if v==max(y_data)
              else bar_color for v in y_data]

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=MONTHS, y=y_data,
    marker_color=bar_colors,
    text=[f"{v:.1f}M" for v in y_data],
    textposition='outside',
    textfont=dict(size=9, color=C["grey"]),
    hovertemplate="<b>%{x}</b>: %{y:.1f}M<extra></extra>"))
fig1.add_hline(y=avg_val, line_dash="dash", line_color=C["grey"], line_width=1.5,
               annotation_text=f"Avg: {avg_val:.1f}M",
               annotation_font=dict(color=C["grey"], size=10))
fig1.add_vrect(x0=-0.5, x1=2.5,
    fillcolor="rgba(201,168,76,0.06)", line_width=0,
    annotation_text="🌙 Ramadan", annotation_position="top left",
    annotation=dict(font_color=C["gold"], font_size=10))
fig1.add_vrect(x0=5.5, x1=8.5,
    fillcolor="rgba(58,134,255,0.06)", line_width=0,
    annotation_text="☀️ Summer", annotation_position="top left",
    annotation=dict(font_color=C["blue"], font_size=10))

apply_layout(fig1, height=360)
fig1.update_layout(showlegend=False)
fig1.update_yaxes(title_text=t["tourists_m"])

st.markdown('<div style="padding:0 40px;">', unsafe_allow_html=True)
chart(fig1)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# CHARTS 2+3 — Heatmap | Seasonal Compare
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:28px 40px 0;">', unsafe_allow_html=True)
c2, c3 = st.columns([3,2], gap="large")

with c2:
    st.markdown(sec_head(t["s2"], t["s2h"]), unsafe_allow_html=True)

    # ── Theme-aware colorscale ────────────────────────────────────
    if THEME == "dark":
        heatmap_cs = [
            [0.00, "#0A1628"],
            [0.06, "#0D2744"],
            [0.18, "#0D3B6E"],
            [0.35, "#1565C0"],
            [0.55, "#1976D2"],
            [0.72, "#17B19B"],
            [0.88, "#C9A84C"],
            [1.00, "#F4D044"],
        ]
        cb_bgcolor   = "#1E2528"
        cb_border    = "#2A3235"
        cell_txt_clr = "#F4F9F8"
    else:
        heatmap_cs = [
            [0.00, "#EFF8F6"],
            [0.10, "#B2DFDB"],
            [0.28, "#4DB6AC"],
            [0.48, "#1976D2"],
            [0.68, "#17B19B"],
            [0.84, "#C9A84C"],
            [1.00, "#E65100"],
        ]
        cb_bgcolor   = "#FFFFFF"
        cb_border    = "#CBD5E0"
        cell_txt_clr = "#0D1A1E"

    # Value labels inside cells (only rows with decent data)
    text_matrix = [
        [str(v) if v >= 80 else "" for v in row]
        for row in HEAT_DATA
    ]

    fig2 = go.Figure(go.Heatmap(
        z=HEAT_DATA,
        x=MONTHS,
        y=[str(y) for y in HEAT_YEARS],
        zmin=0, zmax=2600,
        colorscale=heatmap_cs,
        showscale=True,
        text=text_matrix,
        texttemplate="%{text}",
        textfont=dict(size=8, color=cell_txt_clr, family=ff),
        xgap=3, ygap=3,
        hovertemplate="<b>%{y} · %{x}</b><br>%{z:,}K tourists<extra></extra>",
        colorbar=dict(
            thickness=16,
            len=0.90,
            bgcolor=cb_bgcolor,
            bordercolor=cb_border,
            borderwidth=1,
            outlinewidth=0,
            tickfont=dict(size=9, color=C["grey"], family=ff),
            title=dict(
                text="K tourists",
                font=dict(color=C["grey"], size=10, family=ff),
                side="top"),
            tickvals=[100, 500, 1000, 1500, 2000, 2500],
            ticktext=["100","500","1K","1.5K","2K","2.5K"],
        )
    ))

    # COVID band
    fig2.add_hrect(
        y0="2019", y1="2021",
        fillcolor="rgba(239,68,68,0.08)",
        line_color=C["red"], line_width=1,
        layer="below"
    )
    fig2.add_annotation(
        x=MONTHS[5] if LANG=="EN" else "يونيو",
        y="2020",
        text="⚠️ COVID-19",
        showarrow=False,
        font=dict(size=10, color=C["red"], family=ff),
        bgcolor="rgba(239,68,68,0.20)",
        bordercolor=C["red"], borderwidth=1, borderpad=4,
    )

    # 2024 Peak label
    fig2.add_annotation(
        x=MONTHS[2] if LANG=="EN" else "مارس",
        y="2024",
        text="📈 Peak Year",
        showarrow=False,
        font=dict(size=9, color=C["gold"], family=ff),
        bgcolor="rgba(201,168,76,0.20)",
        bordercolor=C["gold"], borderwidth=1, borderpad=3,
    )

    apply_layout(fig2, height=380)
    fig2.update_layout(
        yaxis=dict(
            type="category",
            tickfont=dict(size=11, color=C["grey"]),
            autorange="reversed",
            showgrid=False,
            linecolor=C["border"],
            ticklabelposition="outside",
        ),
        xaxis=dict(
            tickfont=dict(size=10, color=C["grey"]),
            side="bottom",
            showgrid=False,
            linecolor=C["border"],
        ),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    chart(fig2)

with c3:
    st.markdown(sec_head(t["s3"], t["s3h"]), unsafe_allow_html=True)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=MONTHS, y=[v/1000 for v in INB_MON],
        name=t["inbound"],
        line=dict(color=C["blue"], width=2.5),
        fill='tozeroy', fillcolor="rgba(58,134,255,0.12)",
        marker=dict(size=7),
        hovertemplate="<b>%{x}</b>: %{y:.2f}M<extra></extra>"))
    fig3.add_trace(go.Scatter(
        x=MONTHS, y=[v/1000 for v in DOM_MON],
        name=t["domestic"],
        line=dict(color=C["teal"], width=2.5),
        fill='tozeroy', fillcolor="rgba(23,177,155,0.12)",
        marker=dict(size=7),
        hovertemplate="<b>%{x}</b>: %{y:.2f}M<extra></extra>"))
    dec = "Dec" if LANG=="EN" else "ديسمبر"
    jul = "Jul" if LANG=="EN" else "يوليو"
    fig3.add_annotation(x=dec, y=max([v/1000 for v in INB_MON]),
        text="Dec Peak" if LANG=="EN" else "ذروة ديسمبر",
        showarrow=True, arrowhead=2,
        font=dict(size=9, color=C["blue"]),
        arrowcolor=C["blue"], ay=-30)
    fig3.add_annotation(x=jul, y=max([v/1000 for v in DOM_MON]),
        text="Jul Peak" if LANG=="EN" else "ذروة يوليو",
        showarrow=True, arrowhead=2,
        font=dict(size=9, color=C["teal"]),
        arrowcolor=C["teal"], ay=-30)
    apply_layout(fig3, height=260)
    fig3.update_layout(xaxis=dict(tickfont=dict(size=9), tickangle=45))
    fig3.update_yaxes(title_text=t["tourists_m"])
    chart(fig3)

    st.markdown(
        f'<div style="background:{C["sec_bg"]};border:1px solid {C["border"]};'
        f'border-radius:8px;padding:12px 14px;font-size:.8rem;'
        f'color:{txt_dark};line-height:1.7;">'
        f'🌙 {t["ramadan_note"]}<br><br>☀️ {t["summer_note"]}'
        f'</div>',
        unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# CHARTS 4+5 — Quarterly | Radar
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:28px 40px 0;">', unsafe_allow_html=True)
c4, c5 = st.columns(2, gap="large")

with c4:
    st.markdown(sec_head(t["s4"], t["s4h"]), unsafe_allow_html=True)
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=QUARTERS, y=[v/1000 for v in INB_Q],
        name=t["inbound"], marker_color=C["blue"], opacity=0.88,
        hovertemplate="<b>%{x}</b>: %{y:.1f}M<extra></extra>"))
    fig4.add_trace(go.Bar(
        x=QUARTERS, y=[v/1000 for v in DOM_Q],
        name=t["domestic"], marker_color=C["teal"], opacity=0.88,
        hovertemplate="<b>%{x}</b>: %{y:.1f}M<extra></extra>"))
    apply_layout(fig4, height=300)
    fig4.update_layout(barmode='group', bargap=0.25)
    fig4.update_yaxes(title_text=t["tourists_m"])
    chart(fig4)

with c5:
    st.markdown(sec_head(t["s5"], t["s5h"]), unsafe_allow_html=True)
    inb_norm = [v/max(INB_MON) for v in INB_MON]
    dom_norm = [v/max(DOM_MON) for v in DOM_MON]
    fig5 = go.Figure()
    fig5.add_trace(go.Scatterpolar(
        r=inb_norm+[inb_norm[0]],
        theta=MONTHS+[MONTHS[0]],
        fill='toself', name=t["inbound"],
        line_color=C["blue"],
        fillcolor="rgba(58,134,255,0.15)"))
    fig5.add_trace(go.Scatterpolar(
        r=dom_norm+[dom_norm[0]],
        theta=MONTHS+[MONTHS[0]],
        fill='toself', name=t["domestic"],
        line_color=C["teal"],
        fillcolor="rgba(23,177,155,0.15)"))
    fig5.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=C["grey"], family=ff),
        height=300, margin=dict(l=30,r=30,t=20,b=10),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(showticklabels=False,
                           gridcolor="rgba(42,50,53,0.5)"),
            angularaxis=dict(tickfont=dict(size=10, color=C["grey"]),
                             gridcolor="rgba(42,50,53,0.5)")),
        legend=dict(orientation="h", y=-0.1, font=dict(size=10),
                    bgcolor="rgba(0,0,0,0)"))
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
        f'<div style="font-size:.83rem;color:{txt_dark};line-height:1.65;">{txt}</div>'
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
    f'<div style="font-size:.66rem;color:#B5B8B7;margin-top:2px;">📅 Seasonality · Eng. Goda Emad</div>'
    f'</div></div>'
    f'<div style="display:flex;gap:20px;">'
    f'<a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" target="_blank" '
    f'style="font-size:.75rem;color:#B5B8B7;text-decoration:none;">🐙 GitHub</a>'
    f'<a href="https://datasaudi.sa" target="_blank" '
    f'style="font-size:.75rem;color:{C["teal"]};text-decoration:none;font-weight:600;">📊 DataSaudi</a>'
    f'</div></div>',
    unsafe_allow_html=True)
