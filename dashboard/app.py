# ═══════════════════════════════════════════════════════════════════
#  Saudi Tourism Intelligence — Home (app.py)
#  Author  : Eng. Goda Emad  |  Design : DataSaudi
# ═══════════════════════════════════════════════════════════════════
import streamlit as st
import base64, os, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path: sys.path.insert(0, _HERE)

from utils.sidebar import render_sidebar
from utils.kpis    import progress_bar_html

st.set_page_config(
    page_title="Saudi Tourism Intelligence",
    page_icon="🇸🇦", layout="wide",
    initial_sidebar_state="expanded",
)
for k, v in [("lang","EN"),("theme","dark")]:
    if k not in st.session_state: st.session_state[k] = v

THEME, LANG = render_sidebar()

DARK = {
    "teal":"#17B19B","teal_act":"#149581","bg":"#1A1E1F","sec_bg":"#161B1C",
    "card_bg":"#1E2528","navbar":"#031414","white":"#F4F9F8","grey":"#A1A6B7",
    "foot_txt":"#B5B8B7","border":"#2A3235","orange":"#F4D044","gold":"#C9A84C",
    "blue":"#3A86FF","green":"#22C55E","red":"#EF4444",
}
LIGHT = {
    "teal":"#17B19B","teal_act":"#149581","bg":"#F0F5F4","sec_bg":"#E4EDEB",
    "card_bg":"#FFFFFF","navbar":"#172025","white":"#0D1A1E","grey":"#374151",
    "foot_txt":"#6B7280","border":"#C8D8D5","orange":"#B45309","gold":"#92650A",
    "blue":"#1D4ED8","green":"#16A34A","red":"#DC2626",
}
C  = DARK if THEME=="dark" else LIGHT
ff = "Tajawal" if LANG=="AR" else "IBM Plex Sans"
dr = "rtl"    if LANG=="AR" else "ltr"
txt_dark    = "#F4F9F8" if THEME=="dark" else "#0D1A1E"
footer_txt  = "#B5B8B7" if THEME=="dark" else "#6B7280"
def clr(k): return C.get(k, C["teal"])

def _b64(p):
    try:
        with open(os.path.join(_HERE, p),"rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

logo_b64 = _b64("assets/logo.jpg") or _b64("assets/logo.png")
hero_b64 = _b64("assets/hero.jpg") or _b64("assets/hero.png")
logo_src = f"data:image/jpeg;base64,{logo_b64}" if logo_b64 else ""
logo_img = (f'<img src="{logo_src}" style="height:44px;border-radius:8px;"/>'
            if logo_src else '<span style="font-size:2rem;">🇸🇦</span>')

TR = {
"EN":{
    "pill":"🇸🇦  OFFICIAL DATA · MINISTRY OF ECONOMY & PLANNING",
    "hero_title":"<span style='color:#17B19B;'>Saudi Tourism Intelligence</span>",
    "hs":"AI-powered analytics built on 10 years of official government data.\nForecasting · Segmentation · Sustainability — all in one platform.",
    "cta":"Explore Dashboard  →",
    "stats":[
        ("115.8M","TOURISTS 2024",   "teal",  "▲ +23%","up"),
        ("1.10B", "OVERNIGHT STAYS", "teal",  "▲ +41%","up"),
        ("5,622", "AVG SPEND (SAR)", "orange","▲ +8%", "up"),
        ("98.6%", "ML ACCURACY R²",  "gold",  "",      ""),
    ],
    "pt":"PLATFORM","ph":"8 Interactive Pages",
    "ps":"Comprehensive analysis covering every dimension of Saudi tourism",
    # ✅ FIX: 8 pages with correct page file names for navigation
    "pages":[
        ("🏠","Executive Overview",  "KPIs, trends & insights",         "Overview"),
        ("📈","Tourist Trends",       "Annual & monthly 2015–2024",      "Tourist_Trends"),
        ("📅","Seasonality",          "Ramadan & summer peaks",          "Seasonality"),
        ("💰","Spending Analysis",    "Per trip, per night, by purpose", "Spending"),
        ("🏨","Overnight Stays",      "Length of stay & COVID recovery", "Overnight_Stays"),
        ("🔮","Demand Forecasting",   "Prophet ML · 2025–2026",          "Forecasting"),
        ("🎯","Segmentation",         "K-Means · High / Mid / Budget",   "Segmentation"),
        ("🌱","Carbon Impact",        "CO₂ index & ESG sustainability",  "Carbon_Impact"),
    ],
    "mt":"KEY METRICS","mh":"Platform Performance",
    "ms":"Model accuracy and data quality indicators",
    # ✅ FIX: 7 datasets not 6
    "metrics":[
        ("98.6%","Prophet ML R²",      "gold", "Forecasting accuracy"),
        ("0.630","Silhouette Score",    "blue", "K-Means clustering quality"),
        ("10 yrs","Historical Data",   "teal", "2015–2024 official records"),
        ("7",    "Datasets Integrated","green","CSV files from gov. sources"),
    ],
    "it":"KEY INSIGHTS","ih":"Intelligence Summary",
    "ins":[
        ("🚀","2024 record: 115.9M tourists — exceeded Vision 2030 interim target of 100M","teal"),
        ("🏖️","Leisure overtook Religious as #1 visit purpose for the first time in 2024","orange"),
        ("📈","Inbound avg stay doubled: 8.6 → 19.2 nights (2021–2024) · +123%","blue"),
        ("💰","Inbound spend = 4× domestic · SAR 5,622 vs 1,336 per trip","gold"),
        ("🤖","Prophet model achieved 98.6% R² accuracy on 2024 holdout validation","green"),
        ("🌱","Carbon intensity fell 8% from 2022–2024 despite +42% volume surge","teal"),
    ],
    "v30_title":"VISION 2030","v30_h":"Progress Toward Vision 2030 Targets",
    "v30":[
        ("Inbound Tourists",   30.1,150.0,"30.1M of 150M target · 20%",      "teal"),
        ("Tourism GDP %",      11.5, 10.0,"11.5% — target exceeded ✅",        "green"),
        ("Hotel Capacity (k)", 550.0,650.0,"550k of 650k rooms · 85%",        "gold"),
        ("Carbon Reduction %", 18.0, 30.0,"18% of 30% target · in progress", "orange"),
    ],
    "name":"Saudi Tourism Intelligence",
    "copy":"© 2025 Saudi Tourism Intelligence · Eng. Goda Emad",
    "go_page": "Go to page →",
},
"AR":{
    "pill":"🇸🇦  بيانات رسمية · وزارة الاقتصاد والتخطيط",
    "hero_title":"<span style='color:#17B19B;'>ذكاء السياحة السعودية</span>",
    "hs":"تحليلات مدعومة بالذكاء الاصطناعي بناءً على 10 سنوات من البيانات الرسمية.\nالتوقعات · التقسيم · الاستدامة — كل شيء في منصة واحدة.",
    "cta":"←  استكشف لوحة التحكم",
    "stats":[
        ("115.8M","السياح 2024",         "teal",  "▲ +23%","up"),
        ("1.10B", "ليالي الإقامة",       "teal",  "▲ +41%","up"),
        ("5,622", "متوسط الإنفاق (ريال)","orange","▲ +8%", "up"),
        ("98.6%", "دقة النموذج R²",      "gold",  "",      ""),
    ],
    "pt":"المنصة","ph":"8 صفحات تفاعلية",
    "ps":"تحليل شامل يغطي كل أبعاد السياحة السعودية",
    "pages":[
        ("🏠","النظرة التنفيذية", "مؤشرات الأداء والاتجاهات",    "Overview"),
        ("📈","اتجاهات السياحة",  "سنوية وشهرية 2015–2024",      "Tourist_Trends"),
        ("📅","الموسمية",          "رمضان وذروة الصيف",           "Seasonality"),
        ("💰","تحليل الإنفاق",    "لكل رحلة وليلة وغرض",         "Spending"),
        ("🏨","ليالي الإقامة",    "مدة الإقامة وتعافي كوفيد",    "Overnight_Stays"),
        ("🔮","التوقعات",          "Prophet ML · 2025–2026",       "Forecasting"),
        ("🎯","التقسيم",           "K-Means · عالي/متوسط/اقتصادي","Segmentation"),
        ("🌱","الأثر الكربوني",   "مؤشر CO₂ وتقارير ESG",        "Carbon_Impact"),
    ],
    "mt":"المؤشرات الرئيسية","mh":"أداء المنصة",
    "ms":"دقة النماذج وجودة البيانات",
    "metrics":[
        ("98.6%","دقة Prophet ML",   "gold", "دقة التوقعات"),
        ("0.630","معامل Silhouette",  "blue", "جودة تجميع K-Means"),
        ("10 سنوات","بيانات تاريخية","teal", "سجلات رسمية 2015–2024"),
        ("7",    "مجموعات بيانات",   "green","ملفات CSV من مصادر حكومية"),
    ],
    "it":"الاستنتاجات الرئيسية","ih":"ملخص الذكاء",
    "ins":[
        ("🚀","رقم قياسي 2024: 115.9M سائح — تجاوز الهدف المرحلي لرؤية 2030 (100M)","teal"),
        ("🏖️","الترفيه تجاوز الديني كأول غرض للزيارة لأول مرة في 2024","orange"),
        ("📈","مدة الإقامة تضاعفت: 8.6 → 19.2 ليلة (2021–2024) · +123%","blue"),
        ("💰","إنفاق الوافدين = 4× المحليين · 5,622 مقابل 1,336 ريال/رحلة","gold"),
        ("🤖","نموذج Prophet حقق دقة 98.6% R² على بيانات التحقق لعام 2024","green"),
        ("🌱","انخفضت كثافة الكربون 8% من 2022–2024 رغم ارتفاع الأحجام بـ 42%","teal"),
    ],
    "v30_title":"رؤية 2030","v30_h":"التقدم نحو أهداف رؤية 2030",
    "v30":[
        ("السياح الوافدون",    30.1,150.0,"30.1M من هدف 150M · 20%",       "teal"),
        ("نسبة السياحة من GDP",11.5, 10.0,"11.5% — تجاوز الهدف ✅",         "green"),
        ("طاقة الفنادق (ألف)", 550.0,650.0,"550k من 650k غرفة · 85%",       "gold"),
        ("تخفيض الكربون %",    18.0, 30.0,"18% من هدف 30% · قيد التنفيذ", "orange"),
    ],
    "name":"ذكاء السياحة السعودية",
    "copy":"© 2025 ذكاء السياحة السعودية · م. جودة عماد",
    "go_page": "← انتقل للصفحة",
},
}
t = TR[LANG]

hero_bg = (f'url("data:image/jpeg;base64,{hero_b64}")' if hero_b64
           else f"linear-gradient(135deg,{C['navbar']},{C['bg']})")

# ══ GLOBAL CSS ════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;600;700&family=Tajawal:wght@400;700;800&display=swap');
[data-testid="stHeader"],[data-testid="stToolbar"],
[data-testid="stSidebarNav"],footer,#MainMenu{{display:none!important;}}
.block-container{{padding:0!important;max-width:100%!important;}}
section[data-testid="stMain"]>div:first-child{{padding-top:0!important;}}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{{
  background:{C['bg']}!important;direction:{dr};
  font-family:'{ff}',sans-serif;color:{txt_dark}!important;}}
[data-testid="stMain"] label,[data-testid="stMain"] p,
[data-testid="stMain"] span,[data-testid="stWidgetLabel"] p,
.stRadio label div p{{color:{txt_dark}!important;}}
.ds-hero{{
  position:relative;width:100%;height:520px;
  background-image:{hero_bg};background-size:cover;
  background-position:center top;overflow:hidden;}}
.ds-card{{transition:transform .22s,box-shadow .22s,border-color .22s;}}
.ds-card:hover{{
  transform:translateY(-3px);
  box-shadow:0 10px 28px rgba(23,177,155,.18)!important;
  border-color:{C['teal']}88!important;}}
@keyframes ds-pulse{{
  0%,100%{{box-shadow:0 0 0 0 rgba(23,177,155,.6);}}
  50%{{box-shadow:0 0 0 14px rgba(23,177,155,0);}}}}
.ds-cta-btn{{
  background:{C['teal']};color:#FFFFFF;
  font-size:.92rem;font-weight:700;
  padding:13px 32px;border-radius:7px;border:none;
  cursor:pointer;letter-spacing:.3px;
  box-shadow:0 6px 28px rgba(23,177,155,.55);
  animation:ds-pulse 2.6s ease-in-out infinite;
  transition:background .2s,transform .2s;
  font-family:'{ff}',sans-serif;}}
.ds-cta-btn:hover{{
  background:{C['teal_act']};
  animation:none;transform:translateX(4px);}}
.page-nav-btn{{
  display:inline-block;
  margin-top:12px;
  font-size:.72rem;font-weight:600;
  color:{C['teal']};
  background:{C['teal']}15;
  border:1px solid {C['teal']}44;
  padding:5px 12px;border-radius:5px;
  text-decoration:none;letter-spacing:.3px;
  transition:background .2s;}}
.page-nav-btn:hover{{background:{C['teal']}30;}}
</style>""", unsafe_allow_html=True)

def sec_head(badge, h2, sub=""):
    return (
        f'<div style="margin-bottom:22px;">'
        f'<div style="display:inline-block;background:{C["teal"]}15;'
        f'border:1px solid {C["teal"]}44;color:{C["teal"]};font-size:.57rem;'
        f'font-weight:700;letter-spacing:2.5px;text-transform:uppercase;'
        f'padding:4px 12px;border-radius:4px;margin-bottom:10px;">{badge}</div>'
        f'<div style="font-size:1.5rem;font-weight:700;color:{txt_dark};'
        f'margin-bottom:{"6px" if sub else "0"};">{h2}</div>'
        +(f'<div style="font-size:.82rem;color:{C["grey"]};">{sub}</div>' if sub else "")
        +'</div>')

# ══ HERO ══════════════════════════════════════════════════════════
st.markdown(
    f'<div class="ds-hero">'
    f'<div style="position:absolute;inset:0;background:linear-gradient('
    f'100deg,{C["navbar"]}EE 0%,{C["navbar"]}99 40%,{C["bg"]}22 72%,transparent 100%);"></div>'
    f'<div style="position:relative;z-index:2;padding:70px 52px;max-width:700px;">'
    f'<div style="display:inline-flex;align-items:center;background:{C["teal"]}15;'
    f'border:1px solid {C["teal"]}55;color:{C["teal"]};font-size:.58rem;font-weight:700;'
    f'letter-spacing:2.5px;text-transform:uppercase;padding:5px 14px;border-radius:4px;'
    f'margin-bottom:22px;">{t["pill"]}</div>'
    f'<div style="font-size:3.4rem;font-weight:800;color:#F4F9F8;'
    f'line-height:1.1;letter-spacing:-1.5px;margin-bottom:22px;white-space:nowrap;">'
    f'{t["hero_title"]}</div>'
    f'<p style="font-size:.95rem;color:#A1A6B7;line-height:1.8;'
    f'margin-bottom:36px;max-width:480px;">{t["hs"]}</p>'
    f'</div></div>',
    unsafe_allow_html=True)

# ✅ FIX: زرار Explore Dashboard — يستخدم st.page_link بدل onclick
st.markdown('<div style="padding:0 52px 40px;margin-top:-80px;position:relative;z-index:10;">',
            unsafe_allow_html=True)
if st.button(t["cta"], key="cta_btn",
             help="Go to Executive Overview",
             type="primary"):
    st.switch_page("pages/Overview.py")
st.markdown('</div>', unsafe_allow_html=True)

# ══ STATS STRIP ═══════════════════════════════════════════════════
cells = ""
for i,(val,lbl,ck,delta,ddir) in enumerate(t["stats"]):
    br = f"border-right:1px solid {C['border']};" if i<3 else ""
    a  = ""
    if delta:
        ac = C["teal"] if ddir=="up" else C["red"]
        a  = (f'<span style="font-size:.72rem;color:{ac};font-weight:700;'
              f'margin-left:6px;font-family:IBM Plex Mono,monospace;">{delta}</span>')
    cells += (
        f'<div style="padding:28px 24px;{br}">'
        f'<div style="display:flex;align-items:baseline;">'
        f'<div style="font-size:2rem;font-weight:700;color:{clr(ck)};'
        f'font-family:IBM Plex Mono,monospace;letter-spacing:-1px;">{val}</div>{a}</div>'
        f'<div style="font-size:.64rem;color:{C["grey"]};text-transform:uppercase;'
        f'letter-spacing:1.2px;font-weight:600;margin-top:6px;opacity:.9;">{lbl}</div>'
        f'</div>')
st.markdown(
    f'<div style="background:{C["sec_bg"]};border-top:1px solid {C["border"]};'
    f'border-bottom:1px solid {C["border"]};'
    f'display:grid;grid-template-columns:repeat(4,1fr);">{cells}</div>',
    unsafe_allow_html=True)

# ══ PAGE CARDS — clickable via st.columns + st.button ═════════════
st.markdown(
    f'<div style="padding:52px 40px 8px;">{sec_head(t["pt"],t["ph"],t["ps"])}</div>',
    unsafe_allow_html=True)

pages = t["pages"]
# Row 1: first 4 pages
cols1 = st.columns(4, gap="small")
for i, (ico, title, desc, page_file) in enumerate(pages[:4]):
    with cols1[i]:
        st.markdown(
            f'<div class="ds-card" style="background:{C["card_bg"]};'
            f'border:1px solid {C["border"]};border-radius:10px;padding:20px 18px;'
            f'min-height:130px;">'
            f'<div style="font-size:1.6rem;margin-bottom:8px;line-height:1;">{ico}</div>'
            f'<div style="font-size:.87rem;font-weight:600;color:{txt_dark};margin-bottom:4px;">{title}</div>'
            f'<div style="font-size:.73rem;color:{C["grey"]};line-height:1.5;">{desc}</div>'
            f'</div>', unsafe_allow_html=True)
        # ✅ FIX: كل كارد فيها زرار تنقل حقيقي
        if st.button(t["go_page"], key=f"pg_{page_file}", use_container_width=True):
            st.switch_page(f"pages/{page_file}.py")

st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

# Row 2: last 4 pages
cols2 = st.columns(4, gap="small")
for i, (ico, title, desc, page_file) in enumerate(pages[4:]):
    with cols2[i]:
        st.markdown(
            f'<div class="ds-card" style="background:{C["card_bg"]};'
            f'border:1px solid {C["border"]};border-radius:10px;padding:20px 18px;'
            f'min-height:130px;">'
            f'<div style="font-size:1.6rem;margin-bottom:8px;line-height:1;">{ico}</div>'
            f'<div style="font-size:.87rem;font-weight:600;color:{txt_dark};margin-bottom:4px;">{title}</div>'
            f'<div style="font-size:.73rem;color:{C["grey"]};line-height:1.5;">{desc}</div>'
            f'</div>', unsafe_allow_html=True)
        if st.button(t["go_page"], key=f"pg2_{page_file}", use_container_width=True):
            st.switch_page(f"pages/{page_file}.py")

st.markdown(f'<div style="height:1px;background:{C["border"]};margin:32px 40px 0;"></div>',
            unsafe_allow_html=True)

# ══ PLATFORM METRICS ══════════════════════════════════════════════
m_cards = ""
for val,lbl,ck,note in t["metrics"]:
    m_cards += (
        f'<div class="ds-card" style="background:{C["card_bg"]};'
        f'border:1px solid {C["border"]};border-left:3px solid {clr(ck)};'
        f'border-radius:10px;padding:22px 20px;">'
        f'<div style="font-size:2rem;font-weight:700;color:{clr(ck)};'
        f'font-family:IBM Plex Mono,monospace;letter-spacing:-1px;">{val}</div>'
        f'<div style="font-size:.84rem;font-weight:600;color:{txt_dark};margin:6px 0 4px;">{lbl}</div>'
        f'<div style="font-size:.72rem;color:{C["grey"]};">{note}</div>'
        f'</div>')
st.markdown(
    f'<div style="padding:52px 40px 40px;">{sec_head(t["mt"],t["mh"],t["ms"])}'
    f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;">'
    +m_cards+'</div></div>', unsafe_allow_html=True)
st.markdown(f'<div style="height:1px;background:{C["border"]};margin:0 40px;"></div>',
            unsafe_allow_html=True)

# ══ KEY INSIGHTS ══════════════════════════════════════════════════
ins_html = (f'<div style="padding:52px 40px 0;">{sec_head(t["it"],t["ih"])}'
            f'<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;">')
for ico,txt,ck in t["ins"]:
    ins_html += (
        f'<div style="background:{C["card_bg"]};border:1px solid {C["border"]};'
        f'border-left:3px solid {clr(ck)};border-radius:10px;'
        f'padding:16px 18px;display:flex;align-items:flex-start;gap:12px;">'
        f'<div style="font-size:1.2rem;flex-shrink:0;margin-top:2px;">{ico}</div>'
        f'<div style="font-size:.83rem;color:{txt_dark};line-height:1.65;">{txt}</div>'
        f'</div>')
ins_html += '</div></div>'
st.markdown(ins_html, unsafe_allow_html=True)
st.markdown(f'<div style="height:1px;background:{C["border"]};margin:40px 40px 0;"></div>',
            unsafe_allow_html=True)

# ══ VISION 2030 ═══════════════════════════════════════════════════
v30_html = (f'<div style="padding:52px 40px;">{sec_head(t["v30_title"],t["v30_h"])}'
            f'<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:14px;">')
for label,current,target,note,ck in t["v30"]:
    v30_html += progress_bar_html(
        label, current, target, note, clr(ck),
        C["card_bg"], C["border"], txt_dark, C["grey"])
v30_html += '</div></div>'
st.markdown(v30_html, unsafe_allow_html=True)
st.markdown(f'<div style="height:1px;background:{C["border"]};margin:0 40px;"></div>',
            unsafe_allow_html=True)

# ══ FOOTER ════════════════════════════════════════════════════════
st.markdown(
    f'<div style="background:{C["navbar"]};border-top:2px solid {C["teal"]};'
    f'padding:28px 40px;display:flex;justify-content:space-between;'
    f'align-items:center;flex-wrap:wrap;gap:16px;">'
    f'<div style="display:flex;align-items:center;gap:14px;">{logo_img}'
    f'<div><div style="font-size:.92rem;font-weight:700;color:{C["teal"]};">{t["name"]}</div>'
    f'<div style="font-size:.68rem;color:{footer_txt};margin-top:3px;">{t["copy"]}</div>'
    f'</div></div>'
    f'<div style="display:flex;gap:20px;align-items:center;">'
    f'<a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" target="_blank" '
    f'style="font-size:.78rem;color:{footer_txt};text-decoration:none;">🐙 GitHub</a>'
    f'<a href="https://www.linkedin.com/in/goda-emad/" target="_blank" '
    f'style="font-size:.78rem;color:{footer_txt};text-decoration:none;">💼 LinkedIn</a>'
    f'<a href="https://datasaudi.sa" target="_blank" '
    f'style="font-size:.78rem;color:{C["teal"]};text-decoration:none;font-weight:600;">'
    f'📊 DataSaudi</a></div></div>',
    unsafe_allow_html=True)
