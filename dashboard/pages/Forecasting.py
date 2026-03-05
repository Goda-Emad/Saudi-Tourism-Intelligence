# ═══════════════════════════════════════════════════════════════════
#  Saudi Tourism Intelligence — Demand Forecasting
#  Author : Eng. Goda Emad   |   Design : DataSaudi
#  Model  : Facebook Prophet · Trained on 2015–2024 (120 months)
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
    page_title="Forecasting · Saudi Tourism Intelligence",
    page_icon="🔮", layout="wide",
    initial_sidebar_state="expanded",
)
for k, v in [("lang","EN"),("theme","dark")]:
    if k not in st.session_state: st.session_state[k] = v

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
    # ✅ FIX: light mode text colors corrected
    "white":"#0D1A1E","grey":"#374151","foot_txt":"#6B7280",
    "border":"#C8D8D5","orange":"#B45309","gold":"#92650A",
    "blue":"#1565C0","green":"#16A34A","red":"#DC2626","purple":"#6A1B9A",
}
def clr(k): return C.get(k, C["teal"])
ff      = "Tajawal" if LANG=="AR" else "IBM Plex Sans"
dir_val = "rtl"     if LANG=="AR" else "ltr"
txt_col = C["white"]

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

# ── Data (defined early — needed for KPI labels) ─────────────────
MONTHS_EN = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTHS_AR = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
MONTHS    = MONTHS_AR if LANG=="AR" else MONTHS_EN

F25 = [12307,10628,10812,10074,8964,11238,11832,11124,9846,9561,11710,10798]
F26 = [13680,11797,11963,11180,9927,12458,13063,12290,10831,10550,12905,11897]
L25 = [10664,9022, 9146, 8509, 7237,9536, 10251,9507, 8016, 7914, 10088,9203]
U25 = [13969,12301,12422,11662,10622,12807,13522,12770,11391,11131,13380,12477]
L26 = [11938,10188,10328,9532, 8349,10700,11361,10799,9094, 8863,11223,10321]
U26 = [15330,13355,13516,12805,11695,14131,14719,13899,12415,12190,14546,13537]

HIST_YRS = list(range(2015,2025))
HIST_TOT = [64.4,63.1,59.9,58.6,65.3,46.2,67.3,94.5,109.1,115.9]

TOT25 = round(sum(F25)/1000, 2)   # 128.89M
TOT26 = round(sum(F26)/1000, 2)   # 142.54M
YOY   = round((TOT26-TOT25)/TOT25*100, 1)   # +10.6%
# ✅ FIX: correct pct vs 2024
PCT_2024 = round((TOT25-115.9)/115.9*100, 1)  # +11.2%

SEASONAL = [9.8,8.4,8.6,7.9,7.1,9.2,11.4,11.0,8.6,8.2,9.6,9.5]

SC_YEARS = [2024,2025,2026,2027,2028,2029,2030]
SC_BASE  = [115.9, TOT25, TOT26, 158.2, 175.6, 194.9, 216.4]   # ✅ FIX: 2027 corrected
SC_OPT   = [115.9, 133.3, 153.3, 176.3, 202.8, 233.2, 268.2]
SC_PES   = [115.9, 122.9, 130.2, 138.1, 146.4, 155.2, 164.5]
SC_TARG  = [None,  None,  None,  None,  None,  None,  150.0]

M25 = [f"2025-{str(i+1).zfill(2)}" for i in range(12)]
M26 = [f"2026-{str(i+1).zfill(2)}" for i in range(12)]

# ── Translations ─────────────────────────────────────────────────
TR = {
"EN":{
    "title":"🔮 Demand Forecasting 2025–2026",
    "sub_pg":"Prophet ML Model · Monthly Predictions · Confidence Intervals · Vision 2030",
    "s_filter":"Forecast Year","both":"2025 & 2026",
    "kpi_peak25":"Peak Month 2025","kpi_peak26":"Peak Month 2026",
    "kpi_tot25":"Total Forecast 2025","kpi_tot26":"Total Forecast 2026",
    "kpi_yoy":"YoY Growth 2026","kpi_acc":"Model Accuracy R²",
    "s1":"FORECAST","s1h":"Monthly Forecast 2025–2026 with 95% Confidence Intervals",
    "s2":"HISTORICAL VS FORECAST","s2h":"Actual Tourists 2015–2024 + Prophet Projections",
    "s3":"VISION 2030","s3h":"Progress Tracker — Road to 150M Tourists",
    "s4":"SEASONAL DECOMP","s4h":"Monthly Seasonality Pattern (2015–2024 Average)",
    "s5":"SCENARIO ANALYSIS","s5h":"Optimistic / Base / Pessimistic Scenarios 2025–2030",
    "s6":"MONTHLY TABLE","s6h":"Full Forecast Breakdown by Month",
    "s7":"KEY INSIGHTS","s7h":"Forecasting Intelligence",
    "hist":"Historical","fcast":"Forecast","upper":"Upper 95%","lower":"Lower 95%",
    "total":"Total","inbound":"Inbound","domestic":"Domestic",
    "target":"Target","actual":"Actual","progress":"Progress to Target",
    "month":"Month","tourists_k":"Tourists (K)","tourists_m":"Tourists (M)",
    "optimistic":"Optimistic (+15%/yr)","base":"Base Case (+11%/yr)","pessimistic":"Pessimistic (+6%/yr)",
    "yr2024":"2024 Actual","yr2025":"2025 Forecast","yr2026":"2026 Forecast","yr2030":"2030 Target",
    "vision_note":"Vision 2030 Target: 150 Million Tourists",
    "ins":[
        ("🏆","Jan 2026 is peak month at 13,680K tourists — highest ever forecasted","purple"),
        ("📈",f"2026 forecast shows +{YOY}% growth over 2025, on track with Vision 2030","blue"),
        ("📅","Consistent seasonal pattern: Jan & Jul peaks, May trough — matches 10yr history","teal"),
        ("🎯","At current growth, Saudi Arabia will reach 150M tourist target by 2029","gold"),
        ("🤖","Prophet R²=98.6% on 2024 holdout — multiplicative seasonality captures peaks well","green"),
        ("⚠️","COVID-19 dip (2020) treated as anomaly in training — excluded from seasonality","red"),
    ],
},
"AR":{
    "title":"🔮 توقعات الطلب 2025–2026",
    "sub_pg":"نموذج Prophet · توقعات شهرية · فترات الثقة · رؤية 2030",
    "s_filter":"سنة التوقع","both":"2025 و 2026",
    "kpi_peak25":"ذروة 2025","kpi_peak26":"ذروة 2026",
    "kpi_tot25":"إجمالي توقعات 2025","kpi_tot26":"إجمالي توقعات 2026",
    "kpi_yoy":"نمو سنوي 2026","kpi_acc":"دقة النموذج R²",
    "s1":"التوقعات","s1h":"التوقعات الشهرية 2025–2026 مع فترات الثقة 95%",
    "s2":"التاريخي مقابل التوقع","s2h":"السياح الفعليون 2015–2024 + توقعات Prophet",
    "s3":"رؤية 2030","s3h":"متتبع التقدم — الطريق إلى 150M سائح",
    "s4":"التحليل الموسمي","s4h":"النمط الشهري الموسمي (متوسط 2015–2024)",
    "s5":"تحليل السيناريوهات","s5h":"سيناريوهات متفائل / أساسي / متشائم 2025–2030",
    "s6":"الجدول الشهري","s6h":"تفاصيل التوقعات الكاملة شهرياً",
    "s7":"الاستنتاجات الرئيسية","s7h":"ذكاء التوقعات",
    "hist":"تاريخي","fcast":"توقع","upper":"الحد الأعلى 95%","lower":"الحد الأدنى 95%",
    "total":"إجمالي","inbound":"وافد","domestic":"محلي",
    "target":"الهدف","actual":"الفعلي","progress":"التقدم نحو الهدف",
    "month":"الشهر","tourists_k":"السياح (ألف)","tourists_m":"السياح (مليون)",
    "optimistic":"متفائل (+15%/سنة)","base":"أساسي (+11%/سنة)","pessimistic":"متشائم (+6%/سنة)",
    "yr2024":"فعلي 2024","yr2025":"توقع 2025","yr2026":"توقع 2026","yr2030":"هدف 2030",
    "vision_note":"هدف رؤية 2030: 150 مليون سائح",
    "ins":[
        ("🏆","يناير 2026 هو الذروة المتوقعة بـ 13,680K سائح — أعلى توقع في التاريخ","purple"),
        ("📈",f"توقعات 2026 تظهر +{YOY}% نمواً عن 2025، متوافق مع مسار رؤية 2030","blue"),
        ("📅","النمط الموسمي ثابت: ذروة يناير ويوليو، انخفاض مايو — كالتاريخي","teal"),
        ("🎯","بالمعدل الحالي، ستصل السعودية لهدف 150M سائح بحلول 2029","gold"),
        ("🤖","Prophet حقق R²=98.6% على بيانات التحقق 2024 — الموسمية الضربية تلتقط الذرى","green"),
        ("⚠️","انخفاض كوفيد 2020 عومل كشذوذ في التدريب — مستبعد من حسابات الموسمية","red"),
    ],
},
}
t = TR[LANG]

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
    ".ds-card:hover{transform:translateY(-3px);box-shadow:0 10px 28px rgba(23,177,155,.18)!important;}"
    +f"html,body,[data-testid='stAppViewContainer'],[data-testid='stMain']"
    f"{{background:{C['bg']}!important;direction:{dir_val};"
    f"font-family:'{ff}',sans-serif;color:{txt_col}!important;}}"
    f"[data-testid='stMain'] label,[data-testid='stMain'] p,"
    f"[data-testid='stMain'] span,[data-testid='stWidgetLabel'] p,"
    f".stRadio label div p{{color:{txt_col}!important;}}"
    f".ftable{{width:100%;border-collapse:collapse;font-size:.82rem;}}"
    f".ftable th{{background:{C['sec_bg']};color:{C['grey']};padding:9px 12px;text-align:center;"
    f"font-size:.7rem;text-transform:uppercase;letter-spacing:.8px;border-bottom:1px solid {C['border']};}}"
    f".ftable td{{padding:8px 12px;text-align:center;border-bottom:1px solid {C['border']};"
    f"font-family:IBM Plex Mono,monospace;font-size:.8rem;color:{txt_col};}}"
    f".ftable tr:last-child td{{border-bottom:none;}}"
    f".ftable tr:hover td{{background:{C['sec_bg']};}}"
    "</style>",
    unsafe_allow_html=True)

# ── helpers ──────────────────────────────────────────────────────
def sec_head(badge, h2):
    return (
        f'<div style="margin-bottom:18px;">'
        f'<div style="display:inline-block;background:{C["teal"]}15;'
        f'border:1px solid {C["teal"]}44;color:{C["teal"]};'
        f'font-size:.57rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;'
        f'padding:4px 12px;border-radius:4px;margin-bottom:10px;">{badge}</div>'
        f'<div style="font-size:1.25rem;font-weight:700;color:{txt_col};">{h2}</div>'
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

def apply_layout(fig, height=360):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=C["grey"],family=ff),
        height=height,margin=dict(l=10,r=10,t=36,b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=11),
                    orientation="h",y=-0.14),
        xaxis=dict(gridcolor="rgba(42,50,53,0.4)",linecolor=C["border"],
                   tickfont=dict(size=10),showgrid=False),
        yaxis=dict(gridcolor="rgba(42,50,53,0.4)",linecolor=C["border"],
                   tickfont=dict(size=10)))
    return fig

def chart(fig):
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

# ════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div style="background:{C["navbar"]};border-bottom:1px solid {C["border"]};'
    f'padding:24px 40px 20px;">'
    f'<div style="display:inline-block;background:{C["purple"]}22;border:1px solid {C["purple"]}55;'
    f'color:{C["purple"]};font-size:.57rem;font-weight:700;letter-spacing:2.5px;'
    f'text-transform:uppercase;padding:4px 12px;border-radius:4px;margin-bottom:10px;">'
    f'DEMAND FORECASTING · PROPHET ML</div>'
    f'<div style="font-size:1.85rem;font-weight:800;color:#F4F9F8;'
    f'letter-spacing:-.5px;margin-bottom:5px;">{t["title"]}</div>'
    f'<div style="font-size:.82rem;color:#A1A6B7;">{t["sub_pg"]}</div>'
    f'</div>',
    unsafe_allow_html=True)

badge_s = (f'background:{C["sec_bg"]};border:1px solid {C["border"]};'
           f'border-radius:20px;padding:5px 14px;font-size:.75rem;font-weight:600;')
st.markdown(
    f'<div style="padding:16px 40px 0;display:flex;gap:8px;flex-wrap:wrap;">'
    f'<span style="{badge_s}color:{C["purple"]};">🔮 Facebook Prophet</span>'
    f'<span style="{badge_s}color:{C["green"]};">✅ R² = 98.6%</span>'
    f'<span style="{badge_s}color:{C["teal"]};">📊 MAE = 284K tourists</span>'
    f'<span style="{badge_s}color:{C["gold"]};">📅 120 months training</span>'
    f'<span style="{badge_s}color:{C["blue"]};">🔄 Multiplicative seasonality</span>'
    f'</div>',
    unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# KPI STRIP  ✅ FIX: +8.5% → correct value
# ════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div style="padding:24px 40px 0;">'
    f'<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:12px;">'
    +kpi_card("📅",t["kpi_peak25"],"Jan 2025","12,307K tourists","blue")
    +kpi_card("📅",t["kpi_peak26"],"Jan 2026","13,680K tourists","purple")
    +kpi_card("🌍",t["kpi_tot25"],f"{TOT25:.1f}M",f"+{PCT_2024}% vs 2024","teal")
    +kpi_card("🌍",t["kpi_tot26"],f"{TOT26:.1f}M",f"+{YOY}% vs 2025","gold")
    +kpi_card("📈",t["kpi_yoy"],f"+{YOY}%","2026 vs 2025","green")
    +kpi_card("🤖",t["kpi_acc"],"98.6%","R² holdout 2024","purple")
    +'</div></div>',
    unsafe_allow_html=True)

st.markdown(f'<div style="height:1px;background:{C["border"]};margin:24px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# FILTER
# ════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding:20px 40px 0;">',unsafe_allow_html=True)
year_filter = st.radio(t["s_filter"],[t["both"],"2025","2026"],
                       horizontal=True,key="yr_filter")
st.markdown('</div>',unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# CHART 1 — Main Forecast
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:20px 40px 0;">{sec_head(t["s1"],t["s1h"])}</div>',
            unsafe_allow_html=True)
st.markdown('<div style="padding:0 40px;">',unsafe_allow_html=True)
fig1 = go.Figure()

if year_filter in [t["both"],"2025"]:
    fig1.add_trace(go.Scatter(
        x=M25+M25[::-1],y=U25+L25[::-1],
        fill='toself',fillcolor=rgba(C["blue"],0.15),
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=True,name="95% CI 2025",hoverinfo='skip'))
    fig1.add_trace(go.Scatter(
        x=M25,y=F25,name="2025",
        line=dict(color=C["blue"],width=2.5,dash='dot'),
        marker=dict(size=7,color=C["blue"],line=dict(color=C["bg"],width=2)),
        hovertemplate="<b>%{x}</b><br>Forecast: <b>%{y:,.0f}K</b><extra></extra>"))

if year_filter in [t["both"],"2026"]:
    fig1.add_trace(go.Scatter(
        x=M26+M26[::-1],y=U26+L26[::-1],
        fill='toself',fillcolor=rgba(C["purple"],0.15),
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=True,name="95% CI 2026",hoverinfo='skip'))
    fig1.add_trace(go.Scatter(
        x=M26,y=F26,name="2026",
        line=dict(color=C["purple"],width=2.5),
        marker=dict(size=7,color=C["purple"],line=dict(color=C["bg"],width=2)),
        hovertemplate="<b>%{x}</b><br>Forecast: <b>%{y:,.0f}K</b><extra></extra>"))

# ✅ FIX: annotations only when year is in filter
if year_filter in [t["both"],"2026"]:
    fig1.add_annotation(x="2026-01",y=13680,
        text="🏆 Peak: 13,680K",showarrow=True,arrowhead=2,
        font=dict(size=10,color=C["gold"]),arrowcolor=C["gold"],ay=-40,
        bgcolor=C["card_bg"],bordercolor=C["gold"],borderwidth=1,borderpad=4)
if year_filter in [t["both"],"2025"]:
    fig1.add_annotation(x="2025-05",y=8964,
        text="⬇ Low: 8,964K",showarrow=True,arrowhead=2,
        font=dict(size=10,color=C["red"]),arrowcolor=C["red"],ay=45,
        bgcolor=C["card_bg"],bordercolor=C["red"],borderwidth=1,borderpad=4)

apply_layout(fig1,height=400)
fig1.update_layout(xaxis=dict(showgrid=False,tickangle=45,tickfont=dict(size=9)))
fig1.update_yaxes(title_text=t["tourists_k"])
chart(fig1)
st.markdown('</div>',unsafe_allow_html=True)
st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# CHARTS 2+3 — Historical vs Forecast | Vision 2030
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:28px 40px 0;">{sec_head(t["s2"],t["s2h"])}</div>',
            unsafe_allow_html=True)
st.markdown('<div style="padding:0 40px;">',unsafe_allow_html=True)
c1,c2 = st.columns([3,2],gap="large")

with c1:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=HIST_YRS,y=HIST_TOT,name=t["hist"],
        fill="tozeroy",fillcolor=rgba(C["teal"],0.12),
        line=dict(color=C["teal"],width=2.5),
        marker=dict(size=7,color=C["teal"],line=dict(color=C["bg"],width=1.5)),
        hovertemplate="%{x}: <b>%{y}M</b><extra></extra>"))
    fig2.add_trace(go.Scatter(
        x=[2024,2025,2026],y=[115.9,TOT25,TOT26],name=t["fcast"],
        line=dict(color=C["purple"],width=2.5,dash='dash'),
        marker=dict(size=9,symbol='diamond',color=C["purple"],
                    line=dict(color=C["bg"],width=2)),
        hovertemplate="%{x}: <b>%{y:.1f}M</b><extra></extra>"))
    fig2.add_vrect(x0=2019.5,x1=2021.5,
        fillcolor=rgba(C["red"],0.08),line_width=0,
        annotation_text="COVID",annotation_font=dict(color=C["red"],size=10))
    fig2.add_vrect(x0=2024.5,x1=2026.5,
        fillcolor=rgba(C["purple"],0.06),line_width=0,
        annotation_text="Forecast Zone",
        annotation_font=dict(color=C["purple"],size=10))
    fig2.add_hline(y=150,line_dash="dash",line_color=C["gold"],
                   annotation_text="2030 Target: 150M",
                   annotation_font=dict(color=C["gold"],size=10))
    apply_layout(fig2,height=340)
    fig2.update_layout(xaxis=dict(showgrid=False,tickfont=dict(size=10)))
    fig2.update_yaxes(title_text=t["tourists_m"])
    chart(fig2)

with c2:
    st.markdown(sec_head(t["s3"],t["s3h"]),unsafe_allow_html=True)
    for lbl,val,col in [(t["yr2024"],115.9,C["teal"]),
                        (t["yr2025"],TOT25,C["blue"]),
                        (t["yr2026"],TOT26,C["purple"]),
                        (t["yr2030"],150.0,C["gold"])]:
        pct = min(val/150*100,100)
        st.markdown(
            f'<div style="margin-bottom:16px;">'
            f'<div style="display:flex;justify-content:space-between;margin-bottom:5px;">'
            f'<span style="font-size:.82rem;font-weight:600;color:{txt_col};">{lbl}</span>'
            f'<span style="font-size:.82rem;font-weight:700;color:{col};'
            f'font-family:IBM Plex Mono,monospace;">{val:.1f}M / 150M</span>'
            f'</div>'
            f'<div style="background:{C["sec_bg"]};border-radius:6px;height:10px;overflow:hidden;">'
            f'<div style="width:{pct:.1f}%;height:100%;background:{col};'
            f'border-radius:6px;transition:width .5s;"></div></div>'
            f'<div style="font-size:.7rem;color:{C["grey"]};text-align:right;margin-top:3px;">'
            f'{pct:.1f}% {t["progress"]}</div>'
            f'</div>',
            unsafe_allow_html=True)
    st.markdown(
        f'<div style="background:{C["sec_bg"]};border:1px solid {C["border"]};'
        f'border-left:3px solid {C["gold"]};border-radius:8px;padding:12px 14px;margin-top:8px;">'
        f'<div style="font-size:.78rem;font-weight:700;color:{C["gold"]};margin-bottom:4px;">'
        f'🎯 {t["vision_note"]}</div>'
        f'<div style="font-size:.74rem;color:{C["grey"]};">'
        f'At +11%/yr growth rate, target achievable by <b style="color:{C["teal"]};">2029</b></div>'
        f'</div>',
        unsafe_allow_html=True)

st.markdown('</div>',unsafe_allow_html=True)
st.markdown(f'<div style="height:1px;background:{C["border"]};margin:16px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# CHARTS 4+5 — Seasonal | Scenarios
# ════════════════════════════════════════════════════════════════════
st.markdown('<div style="padding:28px 40px 0;">',unsafe_allow_html=True)
c3,c4 = st.columns([1,1],gap="large")

with c3:
    st.markdown(sec_head(t["s4"],t["s4h"]),unsafe_allow_html=True)
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=MONTHS,y=SEASONAL,
        marker=dict(
            color=[C["gold"] if v==max(SEASONAL)
                   else C["red"] if v==min(SEASONAL)
                   else C["teal"] for v in SEASONAL],
            line=dict(width=0),opacity=.88),
        text=[f"{v}%" for v in SEASONAL],
        textposition="outside",textfont=dict(size=9,color=C["grey"]),
        hovertemplate="<b>%{x}</b>: %{y}% of annual<extra></extra>"))
    fig3.add_hline(y=100/12,line_dash="dash",line_color=C["blue"],
                   annotation_text="Average (8.3%)",
                   annotation_font=dict(color=C["blue"],size=9))
    apply_layout(fig3,height=320)
    fig3.update_yaxes(title_text="% of Annual Total")
    chart(fig3)

with c4:
    st.markdown(sec_head(t["s5"],t["s5h"]),unsafe_allow_html=True)
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=SC_YEARS,y=SC_OPT,name=t["optimistic"],
        line=dict(color=C["green"],width=2,dash='dot'),
        fill='tonexty',fillcolor=rgba(C["green"],0.06),
        marker=dict(size=6,color=C["green"]),
        hovertemplate="%{x}: <b>%{y:.1f}M</b><extra></extra>"))
    fig4.add_trace(go.Scatter(
        x=SC_YEARS,y=SC_BASE,name=t["base"],
        line=dict(color=C["teal"],width=3),
        marker=dict(size=7,color=C["teal"],line=dict(color=C["bg"],width=1.5)),
        hovertemplate="%{x}: <b>%{y:.1f}M</b><extra></extra>"))
    fig4.add_trace(go.Scatter(
        x=SC_YEARS,y=SC_PES,name=t["pessimistic"],
        line=dict(color=C["orange"],width=2,dash='dot'),
        marker=dict(size=6,color=C["orange"]),
        hovertemplate="%{x}: <b>%{y:.1f}M</b><extra></extra>"))
    fig4.add_trace(go.Scatter(
        x=SC_YEARS,y=SC_TARG,name="2030 Target",
        mode="markers",
        marker=dict(size=14,symbol='star',color=C["gold"],
                    line=dict(color=C["bg"],width=2)),
        hovertemplate="<b>2030 Target: 150M</b><extra></extra>"))
    fig4.add_hline(y=150,line_dash="dash",line_color=C["gold"],
                   annotation_text="150M Target",
                   annotation_font=dict(color=C["gold"],size=9))
    apply_layout(fig4,height=320)
    fig4.update_yaxes(title_text=t["tourists_m"])
    chart(fig4)

st.markdown('</div>',unsafe_allow_html=True)
st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# MONTHLY TABLE
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:28px 40px 0;">{sec_head(t["s6"],t["s6h"])}</div>',
            unsafe_allow_html=True)

tbl = (f'<div style="padding:0 40px 24px;overflow-x:auto;">'
       f'<table class="ftable"><thead><tr>'
       f'<th>{t["month"]}</th>'
       f'<th style="color:{C["blue"]};">2025 {t["fcast"]}</th>'
       f'<th>2025 {t["lower"]}</th><th>2025 {t["upper"]}</th>'
       f'<th style="color:{C["purple"]};">2026 {t["fcast"]}</th>'
       f'<th>2026 {t["lower"]}</th><th>2026 {t["upper"]}</th>'
       f'<th>YoY</th>'
       f'</tr></thead><tbody>')

for i,m in enumerate(MONTHS):
    yoy  = round((F26[i]-F25[i])/F25[i]*100,1)
    ycol = C["green"] if yoy>0 else C["red"]
    p25  = F25[i]==max(F25)
    p26  = F26[i]==max(F26)
    rbg  = f'style="background:{C["sec_bg"]};"' if (p25 or p26) else ""
    tbl += (f'<tr {rbg}>'
            f'<td style="font-weight:600;color:{txt_col};">{m}</td>'
            f'<td style="color:{C["blue"]};font-weight:{"800" if p25 else "400"};">{F25[i]:,}</td>'
            f'<td style="color:{C["grey"]};">{L25[i]:,}</td>'
            f'<td style="color:{C["grey"]};">{U25[i]:,}</td>'
            f'<td style="color:{C["purple"]};font-weight:{"800" if p26 else "400"};">{F26[i]:,}</td>'
            f'<td style="color:{C["grey"]};">{L26[i]:,}</td>'
            f'<td style="color:{C["grey"]};">{U26[i]:,}</td>'
            f'<td style="color:{ycol};font-weight:700;">+{yoy}%</td>'
            f'</tr>')

s25 = sum(F25); s26 = sum(F26)
tyoy = round((s26-s25)/s25*100,1)
tbl += (f'<tr style="background:{C["sec_bg"]};border-top:2px solid {C["purple"]};">'
        f'<td style="font-weight:800;color:{txt_col};">TOTAL</td>'
        f'<td style="color:{C["blue"]};font-weight:800;">{s25:,}</td>'
        f'<td style="color:{C["grey"]};">—</td><td style="color:{C["grey"]};">—</td>'
        f'<td style="color:{C["purple"]};font-weight:800;">{s26:,}</td>'
        f'<td style="color:{C["grey"]};">—</td><td style="color:{C["grey"]};">—</td>'
        f'<td style="color:{C["green"]};font-weight:800;">+{tyoy}%</td>'
        f'</tr></tbody></table></div>')

st.markdown(tbl,unsafe_allow_html=True)
st.markdown(f'<div style="height:1px;background:{C["border"]};margin:0 40px;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# KEY INSIGHTS
# ════════════════════════════════════════════════════════════════════
ins_html = f'<div style="padding:28px 40px 40px;">{sec_head(t["s7"],t["s7h"])}'
ins_html += '<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;">'
for ico,txt_i,ck in t["ins"]:
    ins_html += (
        f'<div style="background:{C["card_bg"]};border:1px solid {C["border"]};'
        f'border-left:3px solid {clr(ck)};border-radius:10px;'
        f'padding:16px 18px;display:flex;align-items:flex-start;gap:12px;">'
        f'<div style="font-size:1.2rem;flex-shrink:0;margin-top:2px;">{ico}</div>'
        f'<div style="font-size:.83rem;color:{txt_col};line-height:1.65;">{txt_i}</div>'
        f'</div>')
ins_html += '</div></div>'
st.markdown(ins_html,unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div style="background:{C["navbar"]};border-top:2px solid {C["teal"]};'
    f'padding:22px 40px;display:flex;justify-content:space-between;'
    f'align-items:center;flex-wrap:wrap;gap:12px;">'
    f'<div style="display:flex;align-items:center;gap:14px;">{logo_img}'
    f'<div><div style="font-size:.88rem;font-weight:700;color:{C["teal"]};">Saudi Tourism Intelligence</div>'
    f'<div style="font-size:.66rem;color:{C["foot_txt"]};margin-top:2px;">🔮 Forecasting · Eng. Goda Emad</div>'
    f'</div></div>'
    f'<div style="display:flex;gap:20px;">'
    f'<a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" target="_blank" '
    f'style="font-size:.75rem;color:{C["foot_txt"]};text-decoration:none;">🐙 GitHub</a>'
    f'<a href="https://datasaudi.sa" target="_blank" '
    f'style="font-size:.75rem;color:{C["teal"]};text-decoration:none;font-weight:600;">📊 DataSaudi</a>'
    f'</div></div>',
    unsafe_allow_html=True)
