# ═══════════════════════════════════════════════════════════════════
#  Saudi Tourism Intelligence — Carbon Impact Page
#  Author : Eng. Goda Emad
#  Design : DataSaudi Official Design System
# ═══════════════════════════════════════════════════════════════════
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Carbon Impact · Saudi Tourism Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

for k, v in [("lang","EN"),("theme","dark")]:
    if k not in st.session_state:
        st.session_state[k] = v

LANG  = st.session_state.lang
THEME = st.session_state.theme

# ── Colors (same system as app.py) ───────────────────────────────
C = {
    "teal":"#17B19B","teal_act":"#149581","bg":"#1A1E1F",
    "sec_bg":"#161B1C","card_bg":"#1E2528","navbar":"#031414",
    "white":"#F4F9F8","grey":"#A1A6B7","foot_txt":"#B5B8B7",
    "border":"#2A3235","orange":"#F4D044","gold":"#C9A84C","blue":"#365C8D",
    "green":"#22C55E","red":"#EF4444","purple":"#8B5CF6",
} if THEME=="dark" else {
    "teal":"#17B19B","teal_act":"#149581","bg":"#F0F5F4",
    "sec_bg":"#E4EDEB","card_bg":"#FFFFFF","navbar":"#172025",
    "white":"#F4F9F8","grey":"#9DBFBA","foot_txt":"#9DBFBA",
    "border":"#2A3235","orange":"#E8A020","gold":"#C9A84C","blue":"#5B8DC8",
    "green":"#16A34A","red":"#DC2626","purple":"#7C3AED",
}

PLOT_BG  = "rgba(0,0,0,0)"
GRID_CLR = C["border"]
FONT_CLR = C["grey"]
ff       = "Tajawal" if LANG=="AR" else "IBM Plex Sans"
dir_val  = "rtl"    if LANG=="AR" else "ltr"

def clr(k): return C.get(k, C["teal"])

# ── Data ──────────────────────────────────────────────────────────
YEARS = list(range(2015, 2025))

# CO₂ tonnes per tourist (estimated from transport + hotel energy)
INBOUND_CO2_PER = [1.82,1.85,1.88,1.91,1.87,0.95,1.10,1.42,1.65,1.72]  # COVID dip 2020
DOMESTIC_CO2_PER= [0.38,0.39,0.40,0.41,0.40,0.28,0.32,0.37,0.39,0.41]

# Tourist volumes (millions)
INBOUND  = [17.5,18.0,16.1,15.3,14.1, 6.3,11.5,16.0,27.4,30.1]
DOMESTIC = [68.2,72.0,74.0,77.0,80.5,40.0,55.0,62.0,75.0,85.7]

# Total CO₂ (million tonnes)
TOTAL_CO2 = [
    round(INBOUND[i]*INBOUND_CO2_PER[i] + DOMESTIC[i]*DOMESTIC_CO2_PER[i], 1)
    for i in range(10)
]
INBOUND_CO2  = [round(INBOUND[i]*INBOUND_CO2_PER[i],1)  for i in range(10)]
DOMESTIC_CO2 = [round(DOMESTIC[i]*DOMESTIC_CO2_PER[i],1) for i in range(10)]

# ESG Scores (0–100)
ESG = {
    "EN": ["Carbon Efficiency","Renewable Energy","Water Conservation","Waste Management","Green Certification","Community Impact"],
    "AR": ["كفاءة الكربون","الطاقة المتجددة","الحفاظ على المياه","إدارة النفايات","الشهادات الخضراء","الأثر المجتمعي"],
    "scores": [68, 42, 71, 55, 38, 80],
    "colors": ["#17B19B","#F4D044","#365C8D","#C9A84C","#22C55E","#8B5CF6"],
}

# Global benchmarks (CO₂ tonnes/tourist)
BENCHMARKS = {
    "EN":   ["Saudi Arabia","UAE","Thailand","France","Spain","Global Avg"],
    "AR":   ["المملكة العربية السعودية","الإمارات","تايلاند","فرنسا","إسبانيا","المتوسط العالمي"],
    "vals": [0.89, 1.12, 0.54, 0.48, 0.43, 0.62],
    "cols": ["#17B19B","#F4D044","#365C8D","#C9A84C","#22C55E","#A1A6B7"],
}

# ── Translations ──────────────────────────────────────────────────
TR = {
"EN":{
    "title":"🌱 Carbon Impact Index",
    "sub":"CO₂ Emissions · Sustainability Metrics · ESG Reporting · Vision 2030 Green Goals",
    "thm":"☀️ Light" if THEME=="dark" else "🌙 Dark",
    "lng":"🌐 العربية",
    # KPIs
    "k1_lbl":"Total CO₂ 2024","k1_val":"78.0M","k1_unit":"tonnes","k1_d":"▲+12%","k1_dc":"orange",
    "k2_lbl":"Inbound CO₂/Tourist","k2_val":"1.72","k2_unit":"t/tourist","k2_d":"▼-4%","k2_dc":"teal",
    "k3_lbl":"Domestic CO₂/Tourist","k3_val":"0.41","k3_unit":"t/tourist","k3_d":"▲+5%","k3_dc":"orange",
    "k4_lbl":"Trees to Offset 10%","k4_val":"35.2M","k4_unit":"trees/year","k4_d":"","k4_dc":"green",
    # Section titles
    "s1":"EMISSIONS TREND","s1h":"Annual CO₂ Emissions 2015–2024",
    "s2":"BREAKDOWN","s2h":"Inbound vs Domestic Emissions",
    "s3":"INTENSITY","s3h":"Carbon Intensity per Tourist (tonnes)",
    "s4":"SIMULATOR","s4h":"10% Reduction Scenario — Impact Simulator",
    "s5":"BENCHMARKS","s5h":"Global Benchmark Comparison",
    "s6":"ESG SCORECARD","s6h":"ESG Sustainability Scorecard",
    "s7":"KEY INSIGHTS","s7h":"Carbon Intelligence",
    # Simulator
    "sim_label":"Adjust Reduction Target (%)",
    "sim_saved":"CO₂ Saved",
    "sim_trees":"Equivalent Trees",
    "sim_cars" :"Cars Removed",
    # Insights
    "ins":[
        ("🌍","Inbound tourists generate 4.2× more CO₂ per visit than domestic — air travel dominates","orange"),
        ("📉","Carbon intensity per tourist FELL 8% from 2022–2024 despite volume surge — efficiency gains","teal"),
        ("🌿","Saudi Arabia's 1.72 t/tourist is 2.8× the Spain benchmark — major decarbonization opportunity","blue"),
        ("🎯","Vision 2030 green tourism target: reach 0.65 t/tourist by 2030 — requires 62% intensity cut","gold"),
    ],
},
"AR":{
    "title":"🌱 مؤشر الأثر الكربوني",
    "sub":"انبعاثات CO₂ · مقاييس الاستدامة · تقارير ESG · أهداف رؤية 2030 الخضراء",
    "thm":"☀️ فاتح" if THEME=="dark" else "🌙 داكن",
    "lng":"🌐 English",
    "k1_lbl":"إجمالي CO₂ 2024","k1_val":"78.0M","k1_unit":"طن","k1_d":"▲+12%","k1_dc":"orange",
    "k2_lbl":"CO₂/سائح وافد","k2_val":"1.72","k2_unit":"طن/سائح","k2_d":"▼-4%","k2_dc":"teal",
    "k3_lbl":"CO₂/سائح محلي","k3_val":"0.41","k3_unit":"طن/سائح","k3_d":"▲+5%","k3_dc":"orange",
    "k4_lbl":"أشجار لتعويض 10%","k4_val":"35.2M","k4_unit":"شجرة/سنة","k4_d":"","k4_dc":"green",
    "s1":"اتجاه الانبعاثات","s1h":"انبعاثات CO₂ السنوية 2015–2024",
    "s2":"التوزيع","s2h":"انبعاثات الوافدين مقابل المحليين",
    "s3":"الكثافة","s3h":"الكثافة الكربونية لكل سائح (طن)",
    "s4":"المحاكي","s4h":"سيناريو تخفيض 10% — محاكي التأثير",
    "s5":"المقارنة العالمية","s5h":"مقارنة بالمعايير العالمية",
    "s6":"بطاقة ESG","s6h":"بطاقة أداء الاستدامة ESG",
    "s7":"الاستنتاجات الرئيسية","s7h":"ذكاء الكربون",
    "sim_label":"اضبط هدف التخفيض (%)",
    "sim_saved":"CO₂ موفر",
    "sim_trees":"شجرة معادلة",
    "sim_cars" :"سيارة أقل",
    "ins":[
        ("🌍","الوافدون يولدون 4.2 ضعف CO₂ مقارنة بالمحليين لكل زيارة — السفر الجوي يهيمن","orange"),
        ("📉","انخفضت كثافة الكربون لكل سائح 8% من 2022–2024 رغم ارتفاع الأعداد","teal"),
        ("🌿","1.72 طن/سائح = 2.8 ضعف معيار إسبانيا — فرصة ضخمة لإزالة الكربون","blue"),
        ("🎯","هدف رؤية 2030: الوصول لـ 0.65 طن/سائح — يتطلب خفض 62% في الكثافة","gold"),
    ],
},
}
t = TR[LANG]

# ════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;600;700&family=Tajawal:wght@400;700;800&display=swap');
[data-testid="stHeader"],[data-testid="stToolbar"],
[data-testid="stSidebarNav"],footer,#MainMenu{display:none!important;}
.block-container{padding:0!important;max-width:100%!important;}
section[data-testid="stMain"]>div:first-child{padding-top:0!important;}
.ds-card{transition:transform .22s,box-shadow .22s,border-color .22s;cursor:default;}
.ds-card:hover{transform:translateY(-3px);box-shadow:0 10px 30px rgba(23,177,155,.18);}
</style>
"""+
"<style>"
"html,body,[data-testid='stAppViewContainer'],[data-testid='stMain']{"
"background:"+C["bg"]+"!important;direction:"+dir_val+";font-family:'"+ff+"',sans-serif;}"
"[data-testid='stSidebar']{background:"+C["navbar"]+"!important;border-right:1px solid "+C["border"]+"!important;}"
"[data-testid='stSidebar'] label,[data-testid='stSidebar'] span,"
"[data-testid='stSidebar'] p,[data-testid='stSidebar'] div{color:"+C["white"]+"!important;}"
"[data-testid='stSidebar'] .stButton>button{"
"background:transparent!important;border:1px solid transparent!important;"
"color:"+C["grey"]+"!important;border-radius:8px!important;"
"width:100%!important;font-size:.84rem!important;font-weight:500!important;"
"padding:9px 12px!important;margin-bottom:2px!important;transition:all .15s!important;}"
"[data-testid='stSidebar'] .stButton>button:hover{"
"background:"+C["teal"]+"22!important;border-color:"+C["teal"]+"44!important;color:"+C["teal"]+"!important;}"
"[data-testid='stSidebar'] div:nth-child(3) .stButton>button,"
"[data-testid='stSidebar'] div:nth-child(4) .stButton>button{"
"background:#2A3235!important;border:1px solid #3A4C50!important;"
"color:#F4F9F8!important;font-weight:600!important;margin-bottom:5px!important;}"
"[data-testid='stSidebar'] div:nth-child(3) .stButton>button:hover,"
"[data-testid='stSidebar'] div:nth-child(4) .stButton>button:hover{"
"border-color:"+C["gold"]+"!important;color:"+C["gold"]+"!important;background:#2A3235!important;}"
"[data-baseweb='slider']>div>div:nth-child(2){background:"+C["gold"]+"!important;}"
"[data-baseweb='slider'] [role='slider']{"
"background:"+C["gold"]+"!important;border-color:"+C["gold"]+"!important;"
"box-shadow:0 0 0 4px "+C["gold"]+"22!important;}"
"</style>",
unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════
import glob, re, os, base64

@st.cache_data(show_spinner=False)
def _b64(p):
    try:
        base = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base,p),"rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

@st.cache_data(show_spinner=False)
def _get_pages():
    base  = os.path.dirname(os.path.abspath(__file__))
    files = sorted(glob.glob(os.path.join(base,"pages","*.py")))
    return [("pages/"+os.path.basename(f),
             re.sub(r"^\d+_","",os.path.basename(f)[:-3]).replace("_"," "))
            for f in files]

logo_b64 = _b64("assets/logo.jpg")
logo_src = "data:image/jpeg;base64,"+logo_b64 if logo_b64 else ""
logo_img = ('<img src="'+logo_src+'" style="height:38px;border-radius:7px;"/>'
            if logo_src else "🇸🇦")

with st.sidebar:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:10px;padding:16px 4px 14px;">'
        +logo_img+
        '<div>'
        '<div style="font-size:.85rem;font-weight:700;color:'+C["white"]+';">Saudi Tourism Intelligence</div>'
        '<div style="font-size:.57rem;color:'+C["teal"]+';font-weight:600;letter-spacing:1.2px;text-transform:uppercase;">AI ANALYTICS PLATFORM</div>'
        '</div></div>', unsafe_allow_html=True)
    st.markdown('<div style="height:1px;background:'+C["border"]+';margin-bottom:10px;"></div>', unsafe_allow_html=True)
    if st.button(t["thm"], key="k_thm", use_container_width=True):
        st.session_state.theme = "light" if THEME=="dark" else "dark"; st.rerun()
    if st.button(t["lng"], key="k_lng", use_container_width=True):
        st.session_state.lang  = "AR" if LANG=="EN" else "EN"; st.rerun()
    st.markdown('<div style="height:1px;background:'+C["border"]+';margin:10px 0 6px;"></div>', unsafe_allow_html=True)
    for rel, label in _get_pages():
        active = "Carbon" in rel or "carbon" in rel
        if st.button(("🌱 " if active else "")+label,
                     key="nav_"+rel, use_container_width=True):
            st.switch_page(rel)
    st.markdown('<div style="height:1px;background:'+C["border"]+';margin:10px 0 8px;"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:.66rem;color:'+C["grey"]+';padding:0 2px;line-height:1.9;">'
        '📦 DataSaudi · 2015–2024<br>'
        '🐙 <a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" '
        'target="_blank" style="color:'+C["teal"]+';text-decoration:none;">GitHub</a>'
        '  ·  '
        '💼 <a href="https://www.linkedin.com/in/goda-emad/" '
        'target="_blank" style="color:'+C["teal"]+';text-decoration:none;">LinkedIn</a>'
        '</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ════════════════════════════════════════════════════════════════════
st.markdown(
    '<div style="background:'+C["navbar"]+';border-bottom:1px solid '+C["border"]+';'
    'padding:24px 40px 20px;">'
    '<div style="display:inline-block;background:'+C["teal"]+'15;border:1px solid '+C["teal"]+'44;'
    'color:'+C["teal"]+';font-size:.58rem;font-weight:700;letter-spacing:2.5px;'
    'text-transform:uppercase;padding:4px 12px;border-radius:4px;margin-bottom:10px;">CARBON IMPACT · ESG</div>'
    '<div style="font-size:1.9rem;font-weight:800;color:'+C["white"]+';letter-spacing:-.5px;margin-bottom:5px;">'+t["title"]+'</div>'
    '<div style="font-size:.82rem;color:'+C["grey"]+';">'+t["sub"]+'</div>'
    '</div>',
    unsafe_allow_html=True)

# ── helper: section header ────────────────────────────────────────
def sec_head(badge, h2):
    return (
        '<div style="margin-bottom:22px;">'
        '<div style="display:inline-block;background:'+C["teal"]+'15;border:1px solid '+C["teal"]+'44;'
        'color:'+C["teal"]+';font-size:.57rem;font-weight:700;letter-spacing:2.5px;'
        'text-transform:uppercase;padding:4px 12px;border-radius:4px;margin-bottom:10px;">'+badge+'</div>'
        '<div style="font-size:1.3rem;font-weight:700;color:'+C["white"]+';">'+h2+'</div>'
        '</div>')

def kpi_card(label, val, unit, delta, dc):
    darrow = ('<span style="font-size:.72rem;color:'+clr(dc)+';font-weight:700;margin-left:5px;">'+delta+'</span>'
              if delta else "")
    return (
        '<div class="ds-card" style="background:'+C["card_bg"]+';border:1px solid '+C["border"]+';'
        'border-radius:10px;padding:22px 20px;">'
        '<div style="font-size:.65rem;color:'+C["grey"]+';text-transform:uppercase;'
        'letter-spacing:1px;font-weight:500;margin-bottom:8px;">'+label+'</div>'
        '<div style="display:flex;align-items:baseline;gap:0;">'
        '<div style="font-size:1.9rem;font-weight:700;color:'+clr(dc)+';'
        'font-family:IBM Plex Mono,monospace;letter-spacing:-1px;">'+val+'</div>'
        +darrow+
        '</div>'
        '<div style="font-size:.7rem;color:'+C["grey"]+';margin-top:4px;">'+unit+'</div>'
        '</div>')

# ════════════════════════════════════════════════════════════════════
# KPIs
# ════════════════════════════════════════════════════════════════════
st.markdown(
    '<div style="padding:28px 40px 0;">'
    '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;">'
    +kpi_card(t["k1_lbl"],t["k1_val"],t["k1_unit"],t["k1_d"],t["k1_dc"])
    +kpi_card(t["k2_lbl"],t["k2_val"],t["k2_unit"],t["k2_d"],t["k2_dc"])
    +kpi_card(t["k3_lbl"],t["k3_val"],t["k3_unit"],t["k3_d"],t["k3_dc"])
    +kpi_card(t["k4_lbl"],t["k4_val"],t["k4_unit"],t["k4_d"],t["k4_dc"])
    +'</div></div>',
    unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# CHART HELPERS
# ════════════════════════════════════════════════════════════════════
def apply_layout(fig, title="", height=380):
    fig.update_layout(
        title=dict(text=title, font=dict(size=13, color=FONT_CLR, family=ff)),
        paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_CLR, family=ff),
        height=height, margin=dict(l=10,r=10,t=40,b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        xaxis=dict(gridcolor=GRID_CLR+"55", linecolor=GRID_CLR, tickfont=dict(size=10)),
        yaxis=dict(gridcolor=GRID_CLR+"55", linecolor=GRID_CLR, tickfont=dict(size=10)),
    )
    return fig

def chart_container(fig):
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

# ════════════════════════════════════════════════════════════════════
# ROW 1 — Trend + Breakdown
# ════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding:28px 40px 0;">'+sec_head(t["s1"],t["s1h"])+'</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns([3,2], gap="large")

with col1:
    st.markdown('<div style="padding:0 0 0 40px;">', unsafe_allow_html=True)
    fig = go.Figure()
    # Area fill total
    fig.add_trace(go.Scatter(
        x=YEARS, y=TOTAL_CO2, name="Total CO₂" if LANG=="EN" else "إجمالي CO₂",
        fill="tozeroy", fillcolor=C["teal"]+"22",
        line=dict(color=C["teal"], width=2.5),
        mode="lines+markers",
        marker=dict(size=7, color=C["teal"], line=dict(width=1.5, color=C["navbar"])),
        hovertemplate="%{x}: <b>%{y}M t</b><extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=YEARS, y=INBOUND_CO2, name="Inbound" if LANG=="EN" else "وافدون",
        line=dict(color=C["orange"], width=2, dash="dot"),
        mode="lines+markers",
        marker=dict(size=6, color=C["orange"]),
        hovertemplate="%{x}: <b>%{y}M t</b><extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=YEARS, y=DOMESTIC_CO2, name="Domestic" if LANG=="EN" else "محليون",
        line=dict(color=C["blue"], width=2, dash="dot"),
        mode="lines+markers",
        marker=dict(size=6, color=C["blue"]),
        hovertemplate="%{x}: <b>%{y}M t</b><extra></extra>",
    ))
    # COVID annotation
    fig.add_vrect(x0=2019.5, x1=2020.5, fillcolor=C["red"]+"22",
                  line_width=0, annotation_text="COVID-19",
                  annotation_font=dict(color=C["red"], size=10))
    apply_layout(fig, height=360)
    fig.update_yaxes(title_text="Million Tonnes CO₂" if LANG=="EN" else "مليون طن CO₂")
    chart_container(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div style="padding:0 40px 0 0;">', unsafe_allow_html=True)
    st.markdown(sec_head(t["s2"], t["s2h"]), unsafe_allow_html=True)
    fig2 = go.Figure(go.Pie(
        labels=(["Inbound","Domestic"] if LANG=="EN" else ["وافدون","محليون"]),
        values=[INBOUND_CO2[-1], DOMESTIC_CO2[-1]],
        hole=.55,
        marker=dict(colors=[C["orange"], C["blue"]],
                    line=dict(color=C["navbar"], width=2)),
        textfont=dict(size=12, color=C["white"]),
        hovertemplate="<b>%{label}</b><br>%{value}M t (%{percent})<extra></extra>",
    ))
    fig2.add_annotation(text="2024", x=.5, y=.55, showarrow=False,
                        font=dict(size=11, color=C["grey"]))
    fig2.add_annotation(text=f"{TOTAL_CO2[-1]}M t", x=.5, y=.4, showarrow=False,
                        font=dict(size=18, color=C["white"], family="IBM Plex Mono"))
    apply_layout(fig2, height=320)
    fig2.update_layout(showlegend=True,
                       legend=dict(orientation="h", x=.15, y=-.08))
    chart_container(fig2)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height:1px;background:'+C["border"]+';margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# ROW 2 — Intensity + Simulator
# ════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding:28px 40px 0;">'+sec_head(t["s3"],t["s3h"])+'</div>',
            unsafe_allow_html=True)

col3, col4 = st.columns([1,1], gap="large")

with col3:
    st.markdown('<div style="padding:0 0 0 40px;">', unsafe_allow_html=True)
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=YEARS, y=INBOUND_CO2_PER,
        name="Inbound" if LANG=="EN" else "وافدون",
        marker=dict(color=[C["orange"] if y!=2020 else C["red"] for y in YEARS],
                    line=dict(width=0), opacity=.85),
        hovertemplate="%{x}: <b>%{y} t</b><extra></extra>",
    ))
    fig3.add_trace(go.Bar(
        x=YEARS, y=DOMESTIC_CO2_PER,
        name="Domestic" if LANG=="EN" else "محليون",
        marker=dict(color=[C["blue"] if y!=2020 else C["purple"] for y in YEARS],
                    line=dict(width=0), opacity=.85),
        hovertemplate="%{x}: <b>%{y} t</b><extra></extra>",
    ))
    # Vision 2030 target line
    fig3.add_hline(y=0.65, line_dash="dash", line_color=C["teal"],
                   annotation_text="Vision 2030 Target: 0.65",
                   annotation_font=dict(color=C["teal"], size=10))
    apply_layout(fig3, height=340)
    fig3.update_layout(barmode="group", bargap=0.18, bargroupgap=0.06)
    fig3.update_yaxes(title_text="Tonnes CO₂ / Tourist" if LANG=="EN" else "طن CO₂ / سائح")
    chart_container(fig3)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div style="padding:0 40px 0 0;">', unsafe_allow_html=True)
    st.markdown(sec_head(t["s4"], t["s4h"]), unsafe_allow_html=True)

    reduction_pct = st.slider(t["sim_label"], 5, 50, 10,
                              key="carbon_sim", format="%d%%")

    base_total   = TOTAL_CO2[-1]
    saved_mt     = round(base_total * reduction_pct / 100, 2)
    saved_t      = saved_mt * 1_000_000
    trees_needed = int(saved_t / 21.77)          # avg tree absorbs 21.77 kg CO₂/yr
    cars_removed = int(saved_t / 4_600)          # avg car emits 4.6t/yr

    def sim_card(icon, label, value, color):
        return (
            '<div style="background:'+C["sec_bg"]+';border:1px solid '+C["border"]+';'
            'border-left:3px solid '+color+';border-radius:8px;'
            'padding:14px 16px;margin-bottom:10px;">'
            '<div style="font-size:.65rem;color:'+C["grey"]+';text-transform:uppercase;'
            'letter-spacing:1px;margin-bottom:5px;">'+icon+' '+label+'</div>'
            '<div style="font-size:1.4rem;font-weight:700;color:'+color+';'
            'font-family:IBM Plex Mono,monospace;">'+value+'</div>'
            '</div>')

    st.markdown(
        sim_card("💨", t["sim_saved"], f"{saved_mt}M tonnes", C["teal"])
       +sim_card("🌳", t["sim_trees"], f"{trees_needed:,}", C["green"])
       +sim_card("🚗", t["sim_cars"],  f"{cars_removed:,}", C["orange"]),
        unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height:1px;background:'+C["border"]+';margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# ROW 3 — Benchmarks + ESG Radar
# ════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding:28px 40px 0;">'+sec_head(t["s5"],t["s5h"])+'</div>',
            unsafe_allow_html=True)

col5, col6 = st.columns([1,1], gap="large")

with col5:
    st.markdown('<div style="padding:0 0 0 40px;">', unsafe_allow_html=True)
    labels = BENCHMARKS["AR"] if LANG=="AR" else BENCHMARKS["EN"]
    fig4 = go.Figure(go.Bar(
        x=BENCHMARKS["vals"], y=labels,
        orientation="h",
        marker=dict(color=BENCHMARKS["cols"], line=dict(width=0), opacity=.88),
        text=[f"{v} t" for v in BENCHMARKS["vals"]],
        textposition="outside",
        textfont=dict(size=11, color=FONT_CLR),
        hovertemplate="<b>%{y}</b>: %{x} t/tourist<extra></extra>",
    ))
    # Saudi highlight
    fig4.add_vline(x=0.65, line_dash="dash", line_color=C["teal"],
                   annotation_text="2030 Target",
                   annotation_font=dict(color=C["teal"], size=10))
    apply_layout(fig4, height=340)
    fig4.update_yaxes(tickfont=dict(size=11))
    fig4.update_xaxes(title_text="Tonnes CO₂ / Tourist" if LANG=="EN" else "طن CO₂ / سائح")
    chart_container(fig4)
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div style="padding:0 40px 0 0;">', unsafe_allow_html=True)
    st.markdown(sec_head(t["s6"], t["s6h"]), unsafe_allow_html=True)
    cats = ESG["AR"] if LANG=="AR" else ESG["EN"]
    fig5 = go.Figure(go.Scatterpolar(
        r=ESG["scores"]+[ESG["scores"][0]],
        theta=cats+[cats[0]],
        fill="toself",
        fillcolor=C["teal"]+"33",
        line=dict(color=C["teal"], width=2),
        marker=dict(size=7, color=ESG["colors"]),
        hovertemplate="<b>%{theta}</b>: %{r}/100<extra></extra>",
    ))
    apply_layout(fig5, height=340)
    fig5.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0,100],
                           gridcolor=GRID_CLR, tickfont=dict(size=9)),
            angularaxis=dict(gridcolor=GRID_CLR, tickfont=dict(size=10)),
        ))
    chart_container(fig5)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height:1px;background:'+C["border"]+';margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# INSIGHTS
# ════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding:28px 40px;">'+sec_head(t["s7"],t["s7h"]), unsafe_allow_html=True)

ins_html = '<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:0;">'
for ico, txt, ck in t["ins"]:
    ins_html += (
        '<div style="background:'+C["card_bg"]+';border:1px solid '+C["border"]+';'
        'border-left:3px solid '+clr(ck)+';border-radius:10px;'
        'padding:16px 18px;display:flex;align-items:flex-start;gap:12px;">'
        '<div style="font-size:1.2rem;flex-shrink:0;margin-top:2px;">'+ico+'</div>'
        '<div style="font-size:.83rem;color:'+C["white"]+';line-height:1.65;">'+txt+'</div>'
        '</div>')
ins_html += '</div></div>'
st.markdown(ins_html, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════
st.markdown(
    '<div style="background:'+C["navbar"]+';border-top:2px solid '+C["teal"]+';'
    'padding:22px 40px;display:flex;justify-content:space-between;'
    'align-items:center;flex-wrap:wrap;gap:12px;margin-top:20px;">'
    '<div style="font-size:.75rem;color:'+C["foot_txt"]+';">🌱 Carbon Impact · Saudi Tourism Intelligence · Eng. Goda Emad</div>'
    '<div style="display:flex;gap:20px;">'
    '<a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" target="_blank" '
    'style="font-size:.73rem;color:'+C["foot_txt"]+';text-decoration:none;">🐙 GitHub</a>'
    '<a href="https://datasaudi.sa" target="_blank" '
    'style="font-size:.73rem;color:'+C["teal"]+';text-decoration:none;font-weight:600;">📊 DataSaudi</a>'
    '</div></div>',
    unsafe_allow_html=True)
