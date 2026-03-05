# ═══════════════════════════════════════════════════════════════════
#  Saudi Tourism Intelligence — Carbon Impact
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
    page_title="Carbon Impact · Saudi Tourism Intelligence",
    page_icon="🌱", layout="wide",
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
    "blue":"#365C8D","green":"#22C55E","red":"#EF4444","purple":"#8B5CF6",
} if THEME=="dark" else {
    "teal":"#17B19B","teal_act":"#149581","bg":"#F0F5F4",
    "sec_bg":"#E4EDEB","card_bg":"#FFFFFF","navbar":"#172025",
    "white":"#F4F9F8","grey":"#9DBFBA","foot_txt":"#9DBFBA",
    "border":"#2A3235","orange":"#E8A020","gold":"#C9A84C",
    "blue":"#5B8DC8","green":"#16A34A","red":"#DC2626","purple":"#7C3AED",
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
    "title":"🌱 Carbon Impact Index",
    "sub_pg":"CO₂ Emissions · Sustainability Metrics · ESG Reporting · Vision 2030",
    "k1":"Total CO₂ 2024","k2":"Inbound CO₂ / Tourist",
    "k3":"Domestic CO₂ / Tourist","k4":"Trees to Offset 10%",
    "s1":"EMISSIONS TREND","s1h":"Annual CO₂ Emissions 2015–2024",
    "s2":"BREAKDOWN 2024","s2h":"Inbound vs Domestic Emissions Split",
    "s3":"CARBON INTENSITY","s3h":"CO₂ Tonnes per Tourist by Year",
    "s4":"IMPACT SIMULATOR","s4h":"Reduction Scenario Calculator",
    "s5":"GLOBAL BENCHMARK","s5h":"CO₂ per Tourist — International Comparison",
    "s6":"ESG SCORECARD","s6h":"ESG Sustainability Radar",
    "s7":"KEY INSIGHTS","s7h":"Carbon Intelligence",
    "sim_lbl":"Reduction Target (%)","sim_saved":"CO₂ Saved",
    "sim_trees":"Equivalent Trees","sim_cars":"Cars Removed",
    "total":"Total","inbound":"Inbound","domestic":"Domestic",
    "v30_line":"Vision 2030 Target: 0.65 t",
    "ins":[
        ("🌍","Inbound tourists generate 4.2× more CO₂ per visit than domestic — air travel dominates","orange"),
        ("📉","Carbon intensity per tourist FELL 8% from 2022–2024 despite volume surge","teal"),
        ("🌿","Saudi Arabia 1.72 t/tourist = 2.8× the Spain benchmark — major opportunity","blue"),
        ("🎯","Vision 2030 green target: 0.65 t/tourist by 2030 — requires 62% intensity cut","gold"),
    ],
},
"AR":{
    "title":"🌱 مؤشر الأثر الكربوني",
    "sub_pg":"انبعاثات CO₂ · مقاييس الاستدامة · تقارير ESG · رؤية 2030",
    "k1":"إجمالي CO₂ 2024","k2":"CO₂ / سائح وافد",
    "k3":"CO₂ / سائح محلي","k4":"أشجار لتعويض 10%",
    "s1":"اتجاه الانبعاثات","s1h":"انبعاثات CO₂ السنوية 2015–2024",
    "s2":"التوزيع 2024","s2h":"توزيع انبعاثات الوافدين والمحليين",
    "s3":"الكثافة الكربونية","s3h":"طن CO₂ لكل سائح بالسنة",
    "s4":"محاكي التأثير","s4h":"حاسبة سيناريو التخفيض",
    "s5":"المقارنة العالمية","s5h":"CO₂ لكل سائح — مقارنة دولية",
    "s6":"بطاقة ESG","s6h":"رادار الاستدامة ESG",
    "s7":"الاستنتاجات الرئيسية","s7h":"ذكاء الكربون",
    "sim_lbl":"هدف التخفيض (%)","sim_saved":"CO₂ موفر",
    "sim_trees":"شجرة معادلة","sim_cars":"سيارة أقل",
    "total":"الإجمالي","inbound":"وافدون","domestic":"محليون",
    "v30_line":"هدف رؤية 2030: 0.65 طن",
    "ins":[
        ("🌍","الوافدون يولدون 4.2× CO₂ أكثر من المحليين لكل زيارة — السفر الجوي يهيمن","orange"),
        ("📉","انخفضت كثافة الكربون 8% من 2022–2024 رغم الارتفاع الكبير في الأعداد","teal"),
        ("🌿","1.72 طن/سائح = 2.8× معيار إسبانيا — فرصة ضخمة لإزالة الكربون","blue"),
        ("🎯","هدف رؤية 2030: 0.65 طن/سائح — يتطلب خفض 62% في الكثافة","gold"),
    ],
},
}
t = TR[LANG]

# ── Data ─────────────────────────────────────────────────────────
YEARS   = list(range(2015,2025))
IB_PER  = [1.82,1.85,1.88,1.91,1.87,0.95,1.10,1.42,1.65,1.72]
DOM_PER = [0.38,0.39,0.40,0.41,0.40,0.28,0.32,0.37,0.39,0.41]
IB_VOL  = [17.5,18.0,16.1,15.3,14.1,6.3,11.5,16.0,27.4,30.1]
DOM_VOL = [68.2,72.0,74.0,77.0,80.5,40.0,55.0,62.0,75.0,85.7]
IB_CO2  = [round(IB_VOL[i]*IB_PER[i],1)  for i in range(10)]
DOM_CO2 = [round(DOM_VOL[i]*DOM_PER[i],1) for i in range(10)]
TOT_CO2 = [round(IB_CO2[i]+DOM_CO2[i],1) for i in range(10)]

ESG_CATS_EN = ["Carbon Efficiency","Renewable Energy","Water Conservation","Waste Management","Green Cert","Community"]
ESG_CATS_AR = ["كفاءة الكربون","الطاقة المتجددة","المياه","النفايات","الشهادات الخضراء","الأثر المجتمعي"]
ESG_SCORES  = [68,42,71,55,38,80]
ESG_COLORS  = [C["teal"],C["orange"],C["blue"],C["gold"],C["green"],C["purple"]]

BM_EN   = ["Saudi Arabia","UAE","Thailand","France","Spain","Global Avg"]
BM_AR   = ["المملكة","الإمارات","تايلاند","فرنسا","إسبانيا","المتوسط العالمي"]
BM_VALS = [0.89,1.12,0.54,0.48,0.43,0.62]
BM_COLS = [C["teal"],C["orange"],C["blue"],C["gold"],C["green"],C["grey"]]

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
    ".ds-card:hover{transform:translateY(-3px);box-shadow:0 10px 28px rgba(23,177,155,.18)!important;}"
    f"html,body,[data-testid='stAppViewContainer'],[data-testid='stMain']"
    f"{{background:{C['bg']}!important;direction:{dir_val};"
    f"font-family:'{ff}',sans-serif;color:{C['white']}!important;}}"
    f"[data-baseweb='slider']>div>div:nth-child(2){{background:{C['gold']}!important;}}"
    f"[data-baseweb='slider'] [role='slider']{{background:{C['gold']}!important;"
    f"border-color:{C['gold']}!important;box-shadow:0 0 0 4px {C['gold']}22!important;}}"
    "</style>",
    unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════════
def sec_head(badge, h2):
    return (
        f'<div style="margin-bottom:22px;">'
        f'<div style="display:inline-block;background:{C["teal"]}15;'
        f'border:1px solid {C["teal"]}44;color:{C["teal"]};'
        f'font-size:.57rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;'
        f'padding:4px 12px;border-radius:4px;margin-bottom:10px;">{badge}</div>'
        f'<div style="font-size:1.3rem;font-weight:700;color:{C["white"]};">{h2}</div>'
        f'</div>')

def kpi(label, val, unit, delta, dc):
    arrow = (f'<span style="font-size:.72rem;color:{clr(dc)};font-weight:700;margin-left:5px;">{delta}</span>'
             if delta else "")
    return (
        f'<div class="ds-card" style="background:{C["card_bg"]};border:1px solid {C["border"]};'
        f'border-radius:10px;padding:22px 20px;">'
        f'<div style="font-size:.62rem;color:{C["grey"]};text-transform:uppercase;'
        f'letter-spacing:1px;font-weight:500;margin-bottom:8px;">{label}</div>'
        f'<div style="display:flex;align-items:baseline;">'
        f'<div style="font-size:1.9rem;font-weight:700;color:{clr(dc)};'
        f'font-family:IBM Plex Mono,monospace;letter-spacing:-1px;">{val}</div>'
        +arrow+f'</div>'
        f'<div style="font-size:.68rem;color:{C["grey"]};margin-top:4px;">{unit}</div>'
        f'</div>')

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
# PAGE HEADER — always light text on dark navbar
# ════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div style="background:{C["navbar"]};border-bottom:1px solid {C["border"]};'
    f'padding:24px 40px 20px;">'
    f'<div style="display:inline-block;background:{C["teal"]}15;border:1px solid {C["teal"]}44;'
    f'color:{C["teal"]};font-size:.57rem;font-weight:700;letter-spacing:2.5px;'
    f'text-transform:uppercase;padding:4px 12px;border-radius:4px;margin-bottom:10px;">'
    f'CARBON IMPACT · ESG</div>'
    f'<div style="font-size:1.85rem;font-weight:800;color:#F4F9F8;'
    f'letter-spacing:-.5px;margin-bottom:5px;">{t["title"]}</div>'
    f'<div style="font-size:.82rem;color:#A1A6B7;">{t["sub_pg"]}</div>'
    f'</div>',
    unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# KPIs
# ════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div style="padding:28px 40px 0;">'
    f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;">'
    +kpi(t["k1"],"78.0M","tonnes CO₂","▲ +12%","orange")
    +kpi(t["k2"],"1.72","t / tourist","▼ -4%","teal")
    +kpi(t["k3"],"0.41","t / tourist","▲ +5%","orange")
    +kpi(t["k4"],"35.2M","trees / year","","green")
    +'</div></div>',
    unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# ROW 1 — Emissions Trend + Donut
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:28px 40px 0;">{sec_head(t["s1"],t["s1h"])}</div>',
            unsafe_allow_html=True)

c1, c2 = st.columns([3,2], gap="large")
with c1:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=YEARS, y=TOT_CO2, name=t["total"],
        fill="tozeroy", fillcolor="rgba(23,177,155,0.12)",
        line=dict(color=C["teal"],width=2.5),
        mode="lines+markers",
        marker=dict(size=7,color=C["teal"],line=dict(width=1.5,color=C["navbar"])),
        hovertemplate="%{x}: <b>%{y}M t</b><extra></extra>"))
    fig1.add_trace(go.Scatter(
        x=YEARS, y=IB_CO2, name=t["inbound"],
        line=dict(color=C["orange"],width=2,dash="dot"),
        mode="lines+markers", marker=dict(size=6,color=C["orange"]),
        hovertemplate="%{x}: <b>%{y}M t</b><extra></extra>"))
    fig1.add_trace(go.Scatter(
        x=YEARS, y=DOM_CO2, name=t["domestic"],
        line=dict(color=C["blue"],width=2,dash="dot"),
        mode="lines+markers", marker=dict(size=6,color=C["blue"]),
        hovertemplate="%{x}: <b>%{y}M t</b><extra></extra>"))
    fig1.add_vrect(x0=2019.5,x1=2020.5,fillcolor="rgba(239,68,68,0.12)",
                   line_width=0,annotation_text="COVID-19",
                   annotation_font=dict(color=C["red"],size=10))
    apply_layout(fig1)
    fig1.update_yaxes(title_text="Million Tonnes CO₂")
    chart(fig1)

with c2:
    st.markdown(f'<div style="padding-top:0;">{sec_head(t["s2"],t["s2h"])}</div>',
                unsafe_allow_html=True)
    fig2 = go.Figure(go.Pie(
        labels=[t["inbound"],t["domestic"]],
        values=[IB_CO2[-1],DOM_CO2[-1]],
        hole=.55,
        marker=dict(colors=[C["orange"],C["blue"]],line=dict(color=C["navbar"],width=2)),
        textfont=dict(size=12,color="#F4F9F8"),
        hovertemplate="<b>%{label}</b><br>%{value}M t (%{percent})<extra></extra>"))
    fig2.add_annotation(text="2024",x=.5,y=.56,showarrow=False,
                        font=dict(size=11,color=C["grey"]))
    fig2.add_annotation(text=f"{TOT_CO2[-1]}M t",x=.5,y=.42,showarrow=False,
                        font=dict(size=17,color="#F4F9F8",family="IBM Plex Mono"))
    apply_layout(fig2,height=320)
    fig2.update_layout(showlegend=True,legend=dict(orientation="h",x=.15,y=-.06))
    chart(fig2)

st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# ROW 2 — Intensity + Simulator
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:28px 40px 0;">{sec_head(t["s3"],t["s3h"])}</div>',
            unsafe_allow_html=True)

c3, c4 = st.columns([1,1], gap="large")
with c3:
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=YEARS, y=IB_PER, name=t["inbound"],
        marker=dict(color=[C["orange"] if y!=2020 else C["red"] for y in YEARS],
                    line=dict(width=0),opacity=.85),
        hovertemplate="%{x}: <b>%{y} t</b><extra></extra>"))
    fig3.add_trace(go.Bar(
        x=YEARS, y=DOM_PER, name=t["domestic"],
        marker=dict(color=[C["blue"] if y!=2020 else C["purple"] for y in YEARS],
                    line=dict(width=0),opacity=.85),
        hovertemplate="%{x}: <b>%{y} t</b><extra></extra>"))
    fig3.add_hline(y=0.65,line_dash="dash",line_color=C["teal"],
                   annotation_text=t["v30_line"],
                   annotation_font=dict(color=C["teal"],size=10))
    apply_layout(fig3)
    fig3.update_layout(barmode="group",bargap=0.18,bargroupgap=0.06)
    fig3.update_yaxes(title_text="Tonnes CO₂ / Tourist")
    chart(fig3)

with c4:
    st.markdown(sec_head(t["s4"],t["s4h"]), unsafe_allow_html=True)
    pct = st.slider(t["sim_lbl"],5,50,10,key="sim",format="%d%%")
    saved_mt = round(TOT_CO2[-1]*pct/100, 2)
    saved_t  = saved_mt*1_000_000
    trees    = int(saved_t/21.77)
    cars     = int(saved_t/4_600)

    def sim_card(ico, lbl, val, col):
        return (
            f'<div style="background:{C["sec_bg"]};border:1px solid {C["border"]};'
            f'border-left:3px solid {col};border-radius:8px;'
            f'padding:14px 16px;margin-bottom:10px;">'
            f'<div style="font-size:.62rem;color:{C["grey"]};text-transform:uppercase;'
            f'letter-spacing:1px;margin-bottom:5px;">{ico}  {lbl}</div>'
            f'<div style="font-size:1.4rem;font-weight:700;color:{col};'
            f'font-family:IBM Plex Mono,monospace;">{val}</div>'
            f'</div>')

    st.markdown(
        sim_card("💨",t["sim_saved"],f"{saved_mt}M tonnes",C["teal"])
       +sim_card("🌳",t["sim_trees"],f"{trees:,}",C["green"])
       +sim_card("🚗",t["sim_cars"], f"{cars:,}",C["orange"]),
        unsafe_allow_html=True)

st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# ROW 3 — Benchmark + ESG Radar
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:28px 40px 0;">{sec_head(t["s5"],t["s5h"])}</div>',
            unsafe_allow_html=True)

c5, c6 = st.columns([1,1], gap="large")
with c5:
    lbls = BM_AR if LANG=="AR" else BM_EN
    fig4 = go.Figure(go.Bar(
        x=BM_VALS, y=lbls, orientation="h",
        marker=dict(color=BM_COLS,line=dict(width=0),opacity=.88),
        text=[f"{v} t" for v in BM_VALS],
        textposition="outside",
        textfont=dict(size=11,color=C["grey"]),
        hovertemplate="<b>%{y}</b>: %{x} t/tourist<extra></extra>"))
    fig4.add_vline(x=0.65,line_dash="dash",line_color=C["teal"],
                   annotation_text="2030 Target",
                   annotation_font=dict(color=C["teal"],size=10))
    apply_layout(fig4)
    fig4.update_xaxes(title_text="Tonnes CO₂ / Tourist")
    chart(fig4)

with c6:
    st.markdown(sec_head(t["s6"],t["s6h"]), unsafe_allow_html=True)
    cats = ESG_CATS_AR if LANG=="AR" else ESG_CATS_EN
    fig5 = go.Figure(go.Scatterpolar(
        r=ESG_SCORES+[ESG_SCORES[0]],
        theta=cats+[cats[0]],
        fill="toself",
        fillcolor="rgba(23,177,155,0.2)",
        line=dict(color=C["teal"],width=2),
        marker=dict(size=7,color=ESG_COLORS),
        hovertemplate="<b>%{theta}</b>: %{r}/100<extra></extra>"))
    apply_layout(fig5,height=340)
    fig5.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True,range=[0,100],
                            gridcolor="rgba(42,50,53,0.5)",tickfont=dict(size=9)),
            angularaxis=dict(gridcolor="rgba(42,50,53,0.5)",tickfont=dict(size=10))))
    chart(fig5)

st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# KEY INSIGHTS
# ════════════════════════════════════════════════════════════════════
ins_html = f'<div style="padding:28px 40px 40px;">{sec_head(t["s7"],t["s7h"])}'
ins_html += f'<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;">'
for ico, txt, ck in t["ins"]:
    ins_html += (
        f'<div style="background:{C["card_bg"]};border:1px solid {C["border"]};'
        f'border-left:3px solid {clr(ck)};border-radius:10px;'
        f'padding:16px 18px;display:flex;align-items:flex-start;gap:12px;min-height:70px;">'
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
    f'align-items:center;flex-wrap:wrap;gap:12px;margin-top:16px;">'
    f'<div style="display:flex;align-items:center;gap:14px;">{logo_img}'
    f'<div>'
    f'<div style="font-size:.88rem;font-weight:700;color:{C["teal"]};">Saudi Tourism Intelligence</div>'
    f'<div style="font-size:.66rem;color:#B5B8B7;margin-top:2px;">🌱 Carbon Impact · Eng. Goda Emad</div>'
    f'</div></div>'
    f'<div style="display:flex;gap:20px;">'
    f'<a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" target="_blank" '
    f'style="font-size:.75rem;color:#B5B8B7;text-decoration:none;">🐙 GitHub</a>'
    f'<a href="https://datasaudi.sa" target="_blank" '
    f'style="font-size:.75rem;color:{C["teal"]};text-decoration:none;font-weight:600;">📊 DataSaudi</a>'
    f'</div></div>',
    unsafe_allow_html=True)
