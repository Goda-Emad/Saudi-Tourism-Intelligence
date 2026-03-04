# ═══════════════════════════════════════════════════════════════════
#  Saudi Tourism Intelligence — Executive Overview
#  Author : Eng. Goda Emad   |   Design : DataSaudi
# ═══════════════════════════════════════════════════════════════════
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import base64, os, glob, re

st.set_page_config(
    page_title="Overview · Saudi Tourism Intelligence",
    page_icon="🏠", layout="wide",
    initial_sidebar_state="expanded",
)

for k, v in [("lang","EN"),("theme","dark")]:
    if k not in st.session_state:
        st.session_state[k] = v

LANG  = st.session_state.lang
THEME = st.session_state.theme

# ── Colors ───────────────────────────────────────────────────────
C = {
    "teal":"#17B19B","teal_act":"#149581","bg":"#1A1E1F",
    "sec_bg":"#161B1C","card_bg":"#1E2528","navbar":"#031414",
    "white":"#F4F9F8","grey":"#A1A6B7","foot_txt":"#B5B8B7",
    "border":"#2A3235","orange":"#F4D044","gold":"#C9A84C","blue":"#365C8D",
} if THEME=="dark" else {
    "teal":"#17B19B","teal_act":"#149581","bg":"#F0F5F4",
    "sec_bg":"#E4EDEB","card_bg":"#FFFFFF","navbar":"#172025",
    "white":"#0D1A1E","grey":"#374151","foot_txt":"#6B7280",
    "border":"#C8D8D5","orange":"#B45309","gold":"#92650A","blue":"#1D4ED8",
}
def clr(k): return C.get(k, C["teal"])
ff      = "Tajawal" if LANG=="AR" else "IBM Plex Sans"
dir_val = "rtl"     if LANG=="AR" else "ltr"

# ── Helpers ───────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def _b64(p):
    try:
        base = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base, p), "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

@st.cache_data(show_spinner=False)
def _get_pages():
    base  = os.path.dirname(os.path.abspath(__file__))
    sub   = glob.glob(os.path.join(base,"pages","[0-9]*.py"))
    same  = glob.glob(os.path.join(base,"[0-9]*.py"))
    files = sorted(sub if sub else same)
    NAME_MAP = {
        "Overview":     ("🏠  Overview",        "🏠  النظرة التنفيذية"),
        "Tourist":      ("📈  Tourist Trends",   "📈  اتجاهات السياحة"),
        "Seasonality":  ("📅  Seasonality",      "📅  الموسمية"),
        "Spending":     ("💰  Spending",         "💰  الإنفاق"),
        "Overnight":    ("🏨  Overnight Stays",  "🏨  ليالي الإقامة"),
        "Forecasting":  ("🔮  Forecasting",      "🔮  التوقعات"),
        "Segmentation": ("🎯  Segmentation",     "🎯  التقسيم"),
        "Carbon":       ("🌱  Carbon Impact",    "🌱  الأثر الكربوني"),
    }
    result = []
    for f in files:
        fname  = os.path.basename(f)
        in_sub = "/pages/" in f.replace("\\","/")
        rel    = ("pages/"+fname) if in_sub else fname
        key    = next((k for k in NAME_MAP if k.lower() in fname.lower()), None)
        if key:
            result.append((rel, NAME_MAP[key][0], NAME_MAP[key][1]))
        else:
            raw = re.sub(r"^\d+_","",fname[:-3]).replace("_"," ")
            result.append((rel, raw, raw))
    return result

logo_b64 = _b64("assets/logo.jpg")
logo_src = "data:image/jpeg;base64,"+logo_b64 if logo_b64 else ""
logo_img = ('<img src="'+logo_src+'" style="height:42px;border-radius:8px;"/>'
            if logo_src else '<span style="font-size:2rem;">🇸🇦</span>')

# ── Translations ──────────────────────────────────────────────────
TR = {
"EN":{
    "name":"Saudi Tourism Intelligence","sub":"AI ANALYTICS PLATFORM",
    "thm":"☀️  Light" if THEME=="dark" else "🌙  Dark",
    "lng":"🌐  العربية",
    "title":"🏠 Executive Overview",
    "sub_pg":"KPIs · Trends · Recovery Analysis · Vision 2030 Progress",
    # KPIs
    "k":[
        ("115.8M","Total Tourists 2024","teal","▲ +23%"),
        ("30.1M", "Inbound Tourists",   "teal","▲ +10%"),
        ("85.7M", "Domestic Tourists",  "blue","▲ +14%"),
        ("1.10B", "Overnight Stays",    "teal","▲ +41%"),
        ("19.2",  "Avg Stay (nights)",  "gold","▲ +18%"),
        ("5,622", "Avg Spend (SAR)",    "orange","▲ +8%"),
        ("98.6%", "ML Accuracy",        "green",""),
        ("0.630", "Silhouette Score",   "blue",""),
    ],
    "s1":"TOURIST VOLUME","s1h":"Annual Tourist Arrivals 2015–2024",
    "s2":"RECOVERY","s2h":"Post-COVID Recovery Index",
    "s3":"PURPOSE","s3h":"Visit Purpose Breakdown 2024",
    "s4":"NATIONALITY","s4h":"Top Inbound Nationalities 2024",
    "s5":"TREND","s5h":"Monthly Seasonality Pattern",
    "s6":"INSIGHTS","s6h":"Key Findings",
    "ins":[
        ("🚀","2024 record: 115.9M — exceeds Vision 2030 interim target of 100M","teal"),
        ("🏖️","Leisure overtook Religious tourism as #1 purpose for first time in 2024","orange"),
        ("📈","Inbound avg stay doubled: 8.6 → 19.2 nights (2021–2024) · +123%","blue"),
        ("💰","Inbound spend = 4× domestic (SAR 5,622 vs 1,336 per trip)","gold"),
    ],
},
"AR":{
    "name":"ذكاء السياحة السعودية","sub":"AI ANALYTICS PLATFORM",
    "thm":"☀️  فاتح" if THEME=="dark" else "🌙  داكن",
    "lng":"🌐  English",
    "title":"🏠 النظرة التنفيذية",
    "sub_pg":"مؤشرات الأداء · الاتجاهات · تحليل التعافي · رؤية 2030",
    "k":[
        ("115.8M","إجمالي السياح 2024","teal","▲ +23%"),
        ("30.1M", "السياح الوافدون",   "teal","▲ +10%"),
        ("85.7M", "السياح المحليون",   "blue","▲ +14%"),
        ("1.10B", "ليالي الإقامة",     "teal","▲ +41%"),
        ("19.2",  "متوسط الإقامة (ليلة)","gold","▲ +18%"),
        ("5,622", "متوسط الإنفاق (ريال)","orange","▲ +8%"),
        ("98.6%", "دقة النموذج",       "green",""),
        ("0.630", "معامل Silhouette",  "blue",""),
    ],
    "s1":"حجم السياحة","s1h":"الوصول السنوي للسياح 2015–2024",
    "s2":"التعافي","s2h":"مؤشر التعافي ما بعد كوفيد",
    "s3":"الغرض","s3h":"توزيع غرض الزيارة 2024",
    "s4":"الجنسيات","s4h":"أبرز الجنسيات الوافدة 2024",
    "s5":"الاتجاه","s5h":"النمط الموسمي الشهري",
    "s6":"الاستنتاجات","s6h":"أبرز النتائج",
    "ins":[
        ("🚀","رقم قياسي 2024: 115.9M — يتجاوز المستهدف المرحلي لرؤية 2030 (100M)","teal"),
        ("🏖️","الترفيه تجاوز الديني لأول مرة كغرض رئيسي في 2024","orange"),
        ("📈","مدة الإقامة تضاعفت: 8.6 → 19.2 ليلة (2021–2024) · +123%","blue"),
        ("💰","إنفاق الوافدين = 4× المحليين (5,622 مقابل 1,336 ريال/رحلة)","gold"),
    ],
},
}
t = TR[LANG]

# ── Data ──────────────────────────────────────────────────────────
YEARS     = list(range(2015,2025))
INBOUND   = [17.5,18.0,16.1,15.3,14.1,6.3,11.5,16.0,27.4,30.1]
DOMESTIC  = [68.2,72.0,74.0,77.0,80.5,40.0,55.0,62.0,75.0,85.7]
TOTAL     = [i+d for i,d in zip(INBOUND,DOMESTIC)]
RECOVERY  = [round(v/TOTAL[4]*100,1) for v in TOTAL]  # 2019 baseline=100%

MONTHS    = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTHLY   = [6.8,6.2,8.1,7.4,8.9,11.2,14.3,13.8,10.1,9.4,7.8,6.0]

PURPOSE_EN = ["Leisure","Religious","Business","VFR","Other"]
PURPOSE_AR = ["ترفيه","ديني","أعمال","زيارة أهل","أخرى"]
PURPOSE_V  = [38,29,14,12,7]

NAT_EN = ["GCC","Asia Pacific","Europe","Americas","Middle East","Africa"]
NAT_AR = ["دول الخليج","آسيا والمحيط الهادئ","أوروبا","الأمريكتان","الشرق الأوسط","أفريقيا"]
NAT_V  = [42,21,16,9,8,4]
NAT_C  = [C["teal"],C["blue"],C["orange"],C["gold"],C["purple"] if "purple" in C else "#8B5CF6",C["grey"]]

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
.ds-card{transition:transform .22s,box-shadow .22s,border-color .22s;}
.ds-card:hover{transform:translateY(-3px);box-shadow:0 10px 28px rgba(23,177,155,.18)!important;}
</style>
"""+
"<style>"
"html,body,[data-testid='stAppViewContainer'],[data-testid='stMain']{"
"background:"+C["bg"]+"!important;direction:"+dir_val+";font-family:'"+ff+"',sans-serif;"
"color:"+C["white"]+"!important;}"
"[data-testid='stSidebar']{background:"+C["navbar"]+"!important;border-right:1px solid "+C["border"]+"!important;}"
"[data-testid='stSidebar'] label,[data-testid='stSidebar'] span,"
"[data-testid='stSidebar'] p,[data-testid='stSidebar'] div{color:"+C["white"]+"!important;}"
"[data-testid='stSidebar'] .stButton>button{"
"background:transparent!important;border:1px solid transparent!important;"
"color:"+C["grey"]+"!important;border-radius:8px!important;"
"width:100%!important;font-size:.84rem!important;font-weight:500!important;"
"padding:9px 12px!important;margin-bottom:2px!important;transition:all .15s!important;}"
"[data-testid='stSidebar'] .stButton>button:hover{"
"background:"+C["teal"]+"22!important;border-color:"+C["teal"]+"44!important;"
"color:"+C["teal"]+"!important;}"
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
with st.sidebar:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:10px;padding:16px 4px 14px;">'
        +logo_img+
        '<div>'
        '<div style="font-size:.88rem;font-weight:700;color:'+C["white"]+';">'+t["name"]+'</div>'
        '<div style="font-size:.58rem;color:'+C["teal"]+';font-weight:600;'
        'letter-spacing:1.2px;text-transform:uppercase;">'+t["sub"]+'</div>'
        '</div></div>',
        unsafe_allow_html=True)
    st.markdown('<div style="height:1px;background:'+C["border"]+';margin-bottom:10px;"></div>',
                unsafe_allow_html=True)
    if st.button(t["thm"], key="k_thm", use_container_width=True):
        st.session_state.theme = "light" if THEME=="dark" else "dark"; st.rerun()
    if st.button(t["lng"], key="k_lng", use_container_width=True):
        st.session_state.lang  = "AR" if LANG=="EN" else "EN"; st.rerun()
    st.markdown('<div style="height:1px;background:'+C["border"]+';margin:10px 0 6px;"></div>',
                unsafe_allow_html=True)
    for rel_path, en_lbl, ar_lbl in _get_pages():
        label = ar_lbl if LANG=="AR" else en_lbl
        if st.button(label, key="nav_"+rel_path, use_container_width=True):
            try: st.switch_page(rel_path)
            except: pass
    st.markdown('<div style="height:1px;background:'+C["border"]+';margin:10px 0 8px;"></div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:.67rem;color:'+C["grey"]+';padding:0 2px;line-height:1.9;">'
        '📦 DataSaudi · 2015–2024<br>'
        '🐙 <a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" '
        'target="_blank" style="color:'+C["teal"]+';text-decoration:none;">GitHub</a>'
        '  ·  '
        '💼 <a href="https://www.linkedin.com/in/goda-emad/" '
        'target="_blank" style="color:'+C["teal"]+';text-decoration:none;">LinkedIn</a>'
        '</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════════
def sec_head(badge, h2):
    return (
        '<div style="margin-bottom:22px;">'
        '<div style="display:inline-block;background:'+C["teal"]+'15;'
        'border:1px solid '+C["teal"]+'44;color:'+C["teal"]+';'
        'font-size:.57rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;'
        'padding:4px 12px;border-radius:4px;margin-bottom:10px;">'+badge+'</div>'
        '<div style="font-size:1.3rem;font-weight:700;color:'+C["white"]+';">'+h2+'</div>'
        '</div>')

def apply_layout(fig, height=360):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=C["grey"], family=ff),
        height=height, margin=dict(l=10,r=10,t=36,b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        xaxis=dict(gridcolor="rgba(42,50,53,0.4)", linecolor="#2A3235", tickfont=dict(size=10)),
        yaxis=dict(gridcolor="rgba(42,50,53,0.4)", linecolor="#2A3235", tickfont=dict(size=10)),
    )
    return fig

def chart(fig):
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

# ════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ════════════════════════════════════════════════════════════════════
st.markdown(
    '<div style="background:'+C["navbar"]+';border-bottom:1px solid '+C["border"]+';'
    'padding:24px 40px 20px;">'
    '<div style="display:inline-block;background:'+C["teal"]+'15;border:1px solid '+C["teal"]+'44;'
    'color:'+C["teal"]+';font-size:.57rem;font-weight:700;letter-spacing:2.5px;'
    'text-transform:uppercase;padding:4px 12px;border-radius:4px;margin-bottom:10px;">'
    'EXECUTIVE OVERVIEW · KPIs</div>'
    '<div style="font-size:1.85rem;font-weight:800;color:'+C["white"]+';'
    'letter-spacing:-.5px;margin-bottom:5px;">'+t["title"]+'</div>'
    '<div style="font-size:.82rem;color:'+C["grey"]+';">'+t["sub_pg"]+'</div>'
    '</div>',
    unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# KPI GRID — 8 cards
# ════════════════════════════════════════════════════════════════════
kpi_html = '<div style="padding:28px 40px 0;"><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;">'
for val, lbl, ck, delta in t["k"]:
    arrow = ('<span style="font-size:.7rem;color:'+clr(ck)+';font-weight:700;margin-left:5px;">'+delta+'</span>'
             if delta else "")
    kpi_html += (
        '<div class="ds-card" style="background:'+C["card_bg"]+';border:1px solid '+C["border"]+';'
        'border-radius:10px;padding:20px 18px;">'
        '<div style="font-size:.62rem;color:'+C["grey"]+';text-transform:uppercase;'
        'letter-spacing:1px;font-weight:500;margin-bottom:8px;">'+lbl+'</div>'
        '<div style="display:flex;align-items:baseline;">'
        '<div style="font-size:1.75rem;font-weight:700;color:'+clr(ck)+';'
        'font-family:IBM Plex Mono,monospace;letter-spacing:-1px;">'+val+'</div>'
        +arrow+'</div></div>')
kpi_html += '</div></div>'
st.markdown(kpi_html, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# ROW 1 — Tourist Volume + Recovery
# ════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding:28px 40px 0;">'+sec_head(t["s1"],t["s1h"])+'</div>',
            unsafe_allow_html=True)
c1, c2 = st.columns([3,2], gap="large")

with c1:
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=YEARS, y=DOMESTIC, name="Domestic" if LANG=="EN" else "محليون",
        marker=dict(color=C["blue"], opacity=.85, line=dict(width=0)),
        hovertemplate="%{x}: <b>%{y}M</b><extra></extra>"))
    fig1.add_trace(go.Bar(x=YEARS, y=INBOUND, name="Inbound" if LANG=="EN" else "وافدون",
        marker=dict(color=C["teal"], opacity=.85, line=dict(width=0)),
        hovertemplate="%{x}: <b>%{y}M</b><extra></extra>"))
    fig1.add_trace(go.Scatter(x=YEARS, y=TOTAL, name="Total" if LANG=="EN" else "الإجمالي",
        line=dict(color=C["orange"], width=2.5),
        mode="lines+markers", marker=dict(size=7, color=C["orange"]),
        hovertemplate="%{x}: <b>%{y}M</b><extra></extra>"))
    fig1.add_vrect(x0=2019.5, x1=2020.5, fillcolor="rgba(239,68,68,0.1)",
                   line_width=0, annotation_text="COVID",
                   annotation_font=dict(color="#EF4444", size=10))
    apply_layout(fig1)
    fig1.update_layout(barmode="stack", bargap=0.18)
    fig1.update_yaxes(title_text="Millions")
    chart(fig1)

with c2:
    st.markdown(sec_head(t["s2"], t["s2h"]), unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=YEARS, y=RECOVERY,
        fill="tozeroy", fillcolor="rgba(23,177,155,0.15)",
        line=dict(color=C["teal"], width=2.5),
        mode="lines+markers", marker=dict(size=7, color=C["teal"]),
        hovertemplate="%{x}: <b>%{y}%</b> of 2019<extra></extra>"))
    fig2.add_hline(y=100, line_dash="dash", line_color=C["gold"],
                   annotation_text="2019 Baseline",
                   annotation_font=dict(color=C["gold"], size=10))
    apply_layout(fig2, height=300)
    fig2.update_yaxes(title_text="% of 2019 baseline")
    chart(fig2)

st.markdown('<div style="height:1px;background:'+C["border"]+';margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# ROW 2 — Purpose + Nationality
# ════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding:28px 40px 0;">'+sec_head(t["s3"],t["s3h"])+'</div>',
            unsafe_allow_html=True)
c3, c4 = st.columns([1,1], gap="large")

with c3:
    lbls = PURPOSE_AR if LANG=="AR" else PURPOSE_EN
    fig3 = go.Figure(go.Pie(
        labels=lbls, values=PURPOSE_V, hole=.52,
        marker=dict(colors=[C["teal"],C["gold"],C["blue"],C["orange"],C["grey"]],
                    line=dict(color=C["navbar"], width=2)),
        textfont=dict(size=11, color=C["white"]),
        hovertemplate="<b>%{label}</b>: %{value}% (%{percent})<extra></extra>"))
    fig3.add_annotation(text="2024",x=.5,y=.56,showarrow=False,
                        font=dict(size=11,color=C["grey"]))
    fig3.add_annotation(text="Purpose",x=.5,y=.42,showarrow=False,
                        font=dict(size=13,color=C["white"],family="IBM Plex Mono"))
    apply_layout(fig3, height=320)
    fig3.update_layout(showlegend=True, legend=dict(orientation="h",x=.05,y=-.08))
    chart(fig3)

with c4:
    st.markdown(sec_head(t["s4"], t["s4h"]), unsafe_allow_html=True)
    lbls4 = NAT_AR if LANG=="AR" else NAT_EN
    fig4 = go.Figure(go.Bar(
        x=NAT_V, y=lbls4, orientation="h",
        marker=dict(color=NAT_C, line=dict(width=0), opacity=.88),
        text=[f"{v}%" for v in NAT_V],
        textposition="outside", textfont=dict(size=11, color=C["grey"]),
        hovertemplate="<b>%{y}</b>: %{x}%<extra></extra>"))
    apply_layout(fig4, height=320)
    fig4.update_xaxes(title_text="% of inbound tourists")
    chart(fig4)

st.markdown('<div style="height:1px;background:'+C["border"]+';margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# ROW 3 — Monthly Seasonality
# ════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding:28px 40px 0;">'+sec_head(t["s5"],t["s5h"])+'</div>',
            unsafe_allow_html=True)

fig5 = go.Figure()
fig5.add_trace(go.Scatter(
    x=MONTHS, y=MONTHLY,
    fill="tozeroy", fillcolor="rgba(23,177,155,0.13)",
    line=dict(color=C["teal"], width=2.5),
    mode="lines+markers",
    marker=dict(size=8, color=[C["orange"] if v==max(MONTHLY) else C["teal"] for v in MONTHLY],
                line=dict(width=1.5, color=C["navbar"])),
    hovertemplate="<b>%{x}</b>: %{y}M tourists<extra></extra>"))

# Ramadan annotation (approx March)
fig5.add_vrect(x0="Feb", x1="Mar", fillcolor="rgba(196,154,76,0.12)",
               line_width=0, annotation_text="Ramadan",
               annotation_font=dict(color=C["gold"], size=10))
# Peak summer
fig5.add_vrect(x0="Jun", x1="Aug", fillcolor="rgba(23,177,155,0.08)",
               line_width=0, annotation_text="Peak",
               annotation_font=dict(color=C["teal"], size=10))

apply_layout(fig5, height=280)
fig5.update_yaxes(title_text="Millions")
st.markdown('<div style="padding:0 40px;">', unsafe_allow_html=True)
chart(fig5)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height:1px;background:'+C["border"]+';margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# KEY INSIGHTS
# ════════════════════════════════════════════════════════════════════
ins_html = '<div style="padding:28px 40px;">'+sec_head(t["s6"],t["s6h"])
ins_html += '<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;">'
for ico, txt, ck in t["ins"]:
    ins_html += (
        '<div style="background:'+C["card_bg"]+';border:1px solid '+C["border"]+';'
        'border-left:3px solid '+clr(ck)+';border-radius:10px;'
        'padding:16px 18px;display:flex;align-items:flex-start;gap:12px;min-height:68px;">'
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
    'align-items:center;flex-wrap:wrap;gap:12px;margin-top:16px;">'
    '<div style="display:flex;align-items:center;gap:14px;">'+logo_img+
    '<div>'
    '<div style="font-size:.88rem;font-weight:700;color:'+C["teal"]+';">'+t["name"]+'</div>'
    '<div style="font-size:.66rem;color:'+C["foot_txt"]+';margin-top:2px;">🏠 Executive Overview · Eng. Goda Emad</div>'
    '</div></div>'
    '<div style="display:flex;gap:20px;">'
    '<a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" target="_blank" '
    'style="font-size:.75rem;color:'+C["foot_txt"]+';text-decoration:none;">🐙 GitHub</a>'
    '<a href="https://datasaudi.sa" target="_blank" '
    'style="font-size:.75rem;color:'+C["teal"]+';text-decoration:none;font-weight:600;">📊 DataSaudi</a>'
    '</div></div>',
    unsafe_allow_html=True)
