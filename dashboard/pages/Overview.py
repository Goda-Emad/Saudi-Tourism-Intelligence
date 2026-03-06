# ═══════════════════════════════════════════════════════════════════
#  Saudi Tourism Intelligence — Executive Overview
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
    page_title="Overview · Saudi Tourism Intelligence",
    page_icon="🏠", layout="wide",
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
    "blue":  "#4D9FFF",   # Inbound tourists — vivid sky blue
    "gold":  "#D4A843",   # Total / KPIs — warm gold
    "green": "#2ECC71",   # Growth ▲ — emerald
    "red":   "#FF4757",   # Decline / COVID ▼ — vivid red
    "orange":"#FF7F3F",   # Revenue / VFR — vivid orange
    "purple":"#C67FFF",   # Segmentation — soft violet
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
}

def clr(k): return C.get(k, C["teal"])
ff       = "Tajawal" if LANG=="AR" else "IBM Plex Sans"
dir_val  = "rtl"     if LANG=="AR" else "ltr"
txt_dark = "#F4F9F8" if THEME=="dark" else "#0D1A1E"

def rgba(hex_color, alpha=0.15):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"

# ── Logo ─────────────────────────────────────────────────────────
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

# ── Translations ─────────────────────────────────────────────────
TR = {
"EN":{
    "title":"🏠 Executive Overview",
    "sub_pg":"KPIs · Trends · Recovery Analysis · Vision 2030 Progress",
    "k":[
        ("115.8M","Total Tourists 2024",   "teal",  "▲ +13.1%"),
        ("30.1M", "Inbound Tourists",      "blue",  "▲ +9.9%"),
        ("85.7M", "Domestic Tourists",     "teal",  "▲ +14.3%"),
        ("1.10B", "Overnight Stays",       "gold",  "▲ +18.5%"),
        ("19.2",  "Avg Stay (nights)",     "gold",  "▲ +23%"),
        ("5,622", "Avg Spend (SAR)",       "orange","▲ +8%"),
        ("98.6%", "ML Accuracy",           "green", ""),
        ("0.630", "Silhouette Score",      "purple",""),
    ],
    "s1":"TOURIST VOLUME","s1h":"Annual Tourist Arrivals 2015–2024",
    "s2":"RECOVERY","s2h":"Post-COVID Recovery Index (Base: 2019 = 100%)",
    "s3":"PURPOSE","s3h":"Visit Purpose Breakdown 2024",
    "s4":"NATIONALITY","s4h":"Top Inbound Nationalities 2024",
    "s5":"TREND","s5h":"Monthly Seasonality Pattern (2024)",
    "s6":"INSIGHTS","s6h":"Key Findings",
    "dom":"Domestic","inb":"Inbound","tot":"Total",
    "ramadan":"Ramadan","peak":"Peak Season",
    "recovery_lbl":"2019 Baseline (100%)",
    "ins":[
        ("🚀","2024 record: 115.8M — exceeds Vision 2030 interim target of 100M","teal"),
        ("🏖️","Leisure overtook Religious tourism as #1 purpose for first time in 2024","orange"),
        ("📈","Inbound avg stay doubled: 8.6 → 19.2 nights (2021–2024) · +123%","blue"),
        ("💰","Inbound spend = 4× domestic (SAR 5,622 vs 1,336 per trip)","gold"),
    ],
},
"AR":{
    "title":"🏠 النظرة التنفيذية",
    "sub_pg":"مؤشرات الأداء · الاتجاهات · تحليل التعافي · رؤية 2030",
    "k":[
        ("115.8M","إجمالي السياح 2024",    "teal",  "▲ +13.1%"),
        ("30.1M", "السياح الوافدون",       "blue",  "▲ +9.9%"),
        ("85.7M", "السياح المحليون",       "teal",  "▲ +14.3%"),
        ("1.10B", "ليالي الإقامة",         "gold",  "▲ +18.5%"),
        ("19.2",  "متوسط الإقامة (ليلة)", "gold",  "▲ +23%"),
        ("5,622", "متوسط الإنفاق (ريال)", "orange","▲ +8%"),
        ("98.6%", "دقة النموذج",          "green", ""),
        ("0.630", "معامل Silhouette",      "purple",""),
    ],
    "s1":"حجم السياحة","s1h":"الوصول السنوي للسياح 2015–2024",
    "s2":"التعافي","s2h":"مؤشر التعافي ما بعد كوفيد (الأساس: 2019 = 100%)",
    "s3":"الغرض","s3h":"توزيع غرض الزيارة 2024",
    "s4":"الجنسيات","s4h":"أبرز الجنسيات الوافدة 2024",
    "s5":"الاتجاه","s5h":"النمط الموسمي الشهري (2024)",
    "s6":"الاستنتاجات","s6h":"أبرز النتائج",
    "dom":"محليون","inb":"وافدون","tot":"الإجمالي",
    "ramadan":"رمضان","peak":"موسم الذروة",
    "recovery_lbl":"الأساس 2019 (100%)",
    "ins":[
        ("🚀","رقم قياسي 2024: 115.8M — يتجاوز المستهدف المرحلي لرؤية 2030 (100M)","teal"),
        ("🏖️","الترفيه تجاوز الديني لأول مرة كغرض رئيسي في 2024","orange"),
        ("📈","مدة الإقامة تضاعفت: 8.6 → 19.2 ليلة (2021–2024) · +123%","blue"),
        ("💰","إنفاق الوافدين = 4× المحليين (5,622 مقابل 1,336 ريال/رحلة)","gold"),
    ],
},
}
t = TR[LANG]

# ── Data ─────────────────────────────────────────────────────────
YEARS    = list(range(2015,2025))
INBOUND  = [17.5,18.0,16.1,15.3,14.1,6.3,11.5,16.0,27.4,30.1]
DOMESTIC = [68.2,72.0,74.0,77.0,80.5,40.0,55.0,62.0,75.0,85.7]
TOTAL    = [i+d for i,d in zip(INBOUND,DOMESTIC)]
RECOVERY = [round(v/TOTAL[4]*100,1) for v in TOTAL]

MONTHS_EN = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTHS_AR = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
MONTHS    = MONTHS_AR if LANG=="AR" else MONTHS_EN
MONTHLY   = [7.16,6.53,8.53,7.79,9.37,11.79,15.05,14.53,10.63,9.90,8.21,6.32]

PURPOSE_EN = ["Leisure","Religious","Business","VFR","Other"]
PURPOSE_AR = ["ترفيه","ديني","أعمال","زيارة أهل","أخرى"]
PURPOSE_V  = [38,29,14,12,7]
# Purpose donut uses new high-contrast palette
PURPOSE_C  = [C["teal"], C["red"], C["blue"], C["orange"], C["grey"]]

NAT_EN = ["GCC","Asia Pacific","Europe","Americas","Middle East","Africa"]
NAT_AR = ["دول الخليج","آسيا والمحيط الهادئ","أوروبا","الأمريكتان","الشرق الأوسط","أفريقيا"]
NAT_V  = [42,21,16,9,8,4]
NAT_C  = [C["teal"],C["blue"],C["orange"],C["gold"],C["purple"],C["grey"]]

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

# ── helpers ──────────────────────────────────────────────────────
def sec_head(badge, h2):
    return (
        f'<div style="margin-bottom:22px;">'
        f'<div style="display:inline-block;background:{C["teal"]}15;'
        f'border:1px solid {C["teal"]}44;color:{C["teal"]};'
        f'font-size:.57rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;'
        f'padding:4px 12px;border-radius:4px;margin-bottom:10px;">{badge}</div>'
        f'<div style="font-size:1.3rem;font-weight:700;color:{txt_dark};">{h2}</div>'
        f'</div>')

def apply_layout(fig, height=360):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=C["grey"], family=ff),
        height=height, margin=dict(l=10,r=10,t=36,b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
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
    f'<div style="display:inline-block;background:{C["teal"]}15;border:1px solid {C["teal"]}44;'
    f'color:{C["teal"]};font-size:.57rem;font-weight:700;letter-spacing:2.5px;'
    f'text-transform:uppercase;padding:4px 12px;border-radius:4px;margin-bottom:10px;">'
    f'EXECUTIVE OVERVIEW · KPIs</div>'
    f'<div style="font-size:1.85rem;font-weight:800;color:#F4F9F8;'
    f'letter-spacing:-.5px;margin-bottom:5px;">{t["title"]}</div>'
    f'<div style="font-size:.82rem;color:#A1A6B7;">{t["sub_pg"]}</div>'
    f'</div>',
    unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# KPI GRID — 8 cards (2 rows × 4)
# ════════════════════════════════════════════════════════════════════
kpi_html = (f'<div style="padding:28px 40px 0;">'
            f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;">')
for val, lbl, ck, delta in t["k"]:
    arrow = (f'<span style="font-size:.7rem;color:{clr(ck)};font-weight:700;'
             f'margin-left:5px;">{delta}</span>' if delta else "")
    kpi_html += (
        f'<div class="ds-card" style="background:{C["card_bg"]};border:1px solid {C["border"]};'
        f'border-top:3px solid {clr(ck)};border-radius:10px;padding:20px 18px;">'
        f'<div style="font-size:.62rem;color:{C["grey"]};text-transform:uppercase;'
        f'letter-spacing:1px;font-weight:500;margin-bottom:8px;">{lbl}</div>'
        f'<div style="display:flex;align-items:baseline;">'
        f'<div style="font-size:1.75rem;font-weight:700;color:{clr(ck)};'
        f'font-family:IBM Plex Mono,monospace;letter-spacing:-1px;">{val}</div>'
        +arrow+f'</div></div>')
kpi_html += '</div></div>'
st.markdown(kpi_html, unsafe_allow_html=True)

st.markdown(f'<div style="height:1px;background:{C["border"]};margin:20px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# ROW 1 — Tourist Volume + Recovery
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:28px 40px 0;">{sec_head(t["s1"],t["s1h"])}</div>',
            unsafe_allow_html=True)

st.markdown('<div style="padding:0 40px;">', unsafe_allow_html=True)
c1, c2 = st.columns([3,2], gap="large")

with c1:
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=YEARS, y=DOMESTIC, name=t["dom"],
        marker=dict(color=C["teal"], opacity=.85, line=dict(width=0)),
        hovertemplate="%{x}: <b>%{y}M</b><extra></extra>"))
    fig1.add_trace(go.Bar(
        x=YEARS, y=INBOUND, name=t["inb"],
        marker=dict(color=C["blue"], opacity=.85, line=dict(width=0)),
        hovertemplate="%{x}: <b>%{y}M</b><extra></extra>"))
    fig1.add_trace(go.Scatter(
        x=YEARS, y=TOTAL, name=t["tot"],
        line=dict(color=C["gold"], width=2.5),
        mode="lines+markers",
        marker=dict(size=7, color=C["gold"],
                    line=dict(width=1.5, color=C["bg"])),
        hovertemplate="%{x}: <b>%{y}M</b><extra></extra>"))
    fig1.add_vrect(x0=2019.5, x1=2020.5,
        fillcolor=rgba(C["red"],0.10), line_width=0,
        annotation_text="COVID",
        annotation_font=dict(color=C["red"], size=10))
    apply_layout(fig1)
    fig1.update_layout(barmode="stack", bargap=0.18,
                       legend=dict(orientation="h", y=-0.14))
    fig1.update_yaxes(title_text="Millions")
    chart(fig1)

with c2:
    st.markdown(sec_head(t["s2"],t["s2h"]), unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=YEARS, y=RECOVERY,
        fill="tozeroy", fillcolor=rgba(C["teal"],0.13),
        line=dict(color=C["teal"], width=2.5),
        mode="lines+markers",
        marker=dict(size=7, color=C["teal"],
                    line=dict(width=1.5, color=C["bg"])),
        hovertemplate="%{x}: <b>%{y}%</b> of 2019<extra></extra>"))
    fig2.add_hline(y=100, line_dash="dash", line_color=C["gold"],
                   annotation_text=t["recovery_lbl"],
                   annotation_font=dict(color=C["gold"], size=10))
    fig2.add_annotation(x=2024, y=RECOVERY[-1],
        text=f"✅ {RECOVERY[-1]}%", showarrow=True, arrowhead=2,
        font=dict(size=10, color=C["teal"]), arrowcolor=C["teal"], ay=-40,
        bgcolor=C["card_bg"], bordercolor=C["teal"], borderwidth=1, borderpad=3)
    apply_layout(fig2, height=300)
    fig2.update_yaxes(title_text="% of 2019 baseline")
    chart(fig2)

st.markdown('</div>', unsafe_allow_html=True)
divider()

# ════════════════════════════════════════════════════════════════════
# ROW 2 — Purpose Donut + Nationality
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:28px 40px 0;">{sec_head(t["s3"],t["s3h"])}</div>',
            unsafe_allow_html=True)

st.markdown('<div style="padding:0 40px;">', unsafe_allow_html=True)
c3, c4 = st.columns([1,1], gap="large")

with c3:
    lbls = PURPOSE_AR if LANG=="AR" else PURPOSE_EN
    fig3 = go.Figure(go.Pie(
        labels=lbls, values=PURPOSE_V, hole=.52,
        marker=dict(colors=PURPOSE_C,
                    line=dict(color=C["bg"], width=3)),
        textfont=dict(size=11, color="#F4F9F8"),
        hovertemplate="<b>%{label}</b>: %{value}% (%{percent})<extra></extra>"))
    fig3.add_annotation(text="2024", x=.5, y=.56, showarrow=False,
                        font=dict(size=11, color=C["grey"]))
    fig3.add_annotation(
        text="Purpose" if LANG=="EN" else "الغرض",
        x=.5, y=.42, showarrow=False,
        font=dict(size=13, color=txt_dark, family="IBM Plex Mono"))
    apply_layout(fig3, height=320)
    fig3.update_layout(showlegend=True,
                       legend=dict(orientation="h", x=.05, y=-.08,
                                   font=dict(color=txt_dark)))
    chart(fig3)

with c4:
    st.markdown(sec_head(t["s4"],t["s4h"]), unsafe_allow_html=True)
    lbls4 = NAT_AR if LANG=="AR" else NAT_EN
    fig4 = go.Figure(go.Bar(
        x=NAT_V, y=lbls4, orientation="h",
        marker=dict(color=NAT_C, line=dict(width=0), opacity=.90),
        text=[f"{v}%" for v in NAT_V],
        textposition="outside",
        textfont=dict(size=11, color=txt_dark),
        hovertemplate="<b>%{y}</b>: %{x}%<extra></extra>"))
    apply_layout(fig4, height=320)
    fig4.update_xaxes(title_text="% of inbound tourists")
    fig4.update_yaxes(tickfont=dict(size=11, color=C["grey"]))
    chart(fig4)

st.markdown('</div>', unsafe_allow_html=True)
divider()

# ════════════════════════════════════════════════════════════════════
# ROW 3 — Monthly Seasonality
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:28px 40px 0;">{sec_head(t["s5"],t["s5h"])}</div>',
            unsafe_allow_html=True)

fig5 = go.Figure()
fig5.add_trace(go.Scatter(
    x=MONTHS, y=MONTHLY,
    fill="tozeroy", fillcolor=rgba(C["teal"],0.13),
    line=dict(color=C["teal"], width=2.5),
    mode="lines+markers",
    marker=dict(
        size=8,
        color=[C["orange"] if v==max(MONTHLY) else
               C["red"]    if v==min(MONTHLY) else C["teal"] for v in MONTHLY],
        line=dict(width=1.5, color=C["bg"])),
    hovertemplate="<b>%{x}</b>: %{y:.2f}M tourists<extra></extra>"))

fig5.add_vrect(x0=MONTHS[1], x1=MONTHS[2],
    fillcolor=rgba(C["gold"],0.10), line_width=0,
    annotation_text=t["ramadan"],
    annotation_font=dict(color=C["gold"], size=10))
fig5.add_vrect(x0=MONTHS[5], x1=MONTHS[7],
    fillcolor=rgba(C["teal"],0.08), line_width=0,
    annotation_text=t["peak"],
    annotation_font=dict(color=C["teal"], size=10))

apply_layout(fig5, height=280)
fig5.update_yaxes(title_text="Millions")
st.markdown('<div style="padding:0 40px;">', unsafe_allow_html=True)
chart(fig5)
st.markdown('</div>', unsafe_allow_html=True)
divider()

# ════════════════════════════════════════════════════════════════════
# KEY INSIGHTS
# ════════════════════════════════════════════════════════════════════
ins_html = (f'<div style="padding:28px 40px 40px;">{sec_head(t["s6"],t["s6h"])}'
            f'<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;">')
for ico, txt_i, ck in t["ins"]:
    ins_html += (
        f'<div style="background:{C["card_bg"]};border:1px solid {C["border"]};'
        f'border-left:3px solid {clr(ck)};border-radius:10px;'
        f'padding:16px 18px;display:flex;align-items:flex-start;gap:12px;">'
        f'<div style="font-size:1.2rem;flex-shrink:0;margin-top:2px;">{ico}</div>'
        f'<div style="font-size:.83rem;color:{txt_dark};line-height:1.65;">{txt_i}</div>'
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
    f'<div style="font-size:.66rem;color:{C["foot_txt"]};margin-top:2px;">🏠 Executive Overview · Eng. Goda Emad</div>'
    f'</div></div>'
    f'<div style="display:flex;gap:20px;">'
    f'<a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" target="_blank" '
    f'style="font-size:.75rem;color:{C["foot_txt"]};text-decoration:none;">🐙 GitHub</a>'
    f'<a href="https://datasaudi.sa" target="_blank" '
    f'style="font-size:.75rem;color:{C["teal"]};text-decoration:none;font-weight:600;">📊 DataSaudi</a>'
    f'</div></div>',
    unsafe_allow_html=True)
