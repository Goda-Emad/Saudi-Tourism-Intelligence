# ═══════════════════════════════════════════════════════════════════
#  Saudi Tourism Intelligence — Home Page  (FINAL v7)
#  Author : Eng. Goda Emad
# ═══════════════════════════════════════════════════════════════════
import streamlit as st
import base64, os, glob, re

st.set_page_config(
    page_title="Saudi Tourism Intelligence",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded",
)

for k, v in [("lang","EN"),("theme","dark")]:
    if k not in st.session_state:
        st.session_state[k] = v

LANG  = st.session_state.lang
THEME = st.session_state.theme

# ── ML Model Accuracy (pull from model in production) ──
ML_R2        = 0.986
ML_ACCURACY  = f"{ML_R2*100:.1f}%"   # "98.6%"

# ── Colors — both themes ─────────────────────────────────────────
DARK = {
    "teal":"#17B19B","teal_act":"#149581","teal_sec":"#8BAFAA",
    "bg":"#1A1E1F","sec_bg":"#161B1C","card_bg":"#1E2528",
    "navbar":"#031414","white":"#F4F9F8","grey":"#A1A6B7",
    "foot_txt":"#B5B8B7","border":"#2A3235",
    "orange":"#F4D044","gold":"#C9A84C","blue":"#365C8D",
}
LIGHT = {
    "teal":"#17B19B","teal_act":"#149581","teal_sec":"#4A8A82",
    "bg":"#F0F5F4","sec_bg":"#E4EDEB","card_bg":"#FFFFFF",
    "navbar":"#172025","white":"#0D1A1E","grey":"#374151",
    "foot_txt":"#6B7280","border":"#C8D8D5",
    "orange":"#B45309","gold":"#92650A","blue":"#1D4ED8",
}
C = DARK if THEME=="dark" else LIGHT
def clr(k): return C.get(k, C["teal"])

# ── Cached helpers ────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def _read(p):
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, p),"rb") as f: return f.read()

@st.cache_data(show_spinner=False)
def _b64(p):
    try:    return base64.b64encode(_read(p)).decode()
    except: return ""

@st.cache_data(show_spinner=False)
def _load_css():
    try:    return "<style>"+_read("assets/style.css").decode()+"</style>"
    except: return ""

@st.cache_data(show_spinner=False)
def _get_pages():
    """Hardcoded pages list — works on Streamlit Cloud regardless of folder structure."""
    pages = [
        ("🏠  Overview",        "🏠  النظرة التنفيذية"),
        ("📈  Tourist Trends",   "📈  اتجاهات السياحة"),
        ("📅  Seasonality",      "📅  الموسمية"),
        ("💰  Spending",         "💰  الإنفاق"),
        ("🏨  Overnight Stays",  "🏨  ليالي الإقامة"),
        ("🔮  Forecasting",      "🔮  التوقعات"),
        ("🎯  Segmentation",     "🎯  التقسيم"),
        ("🌱  Carbon Impact",    "🌱  الأثر الكربوني"),
    ]
    # Try to find actual .py files to get correct path
    base   = os.path.dirname(os.path.abspath(__file__))
    in_sub = os.path.isdir(os.path.join(base, "pages"))
    PREFIX = "pages/" if in_sub else ""
    filenames = [
        "01_Overview.py","02_Tourist_Trends.py","03_Seasonality.py",
        "04_Spending.py","05_Overnight_Stays.py","06_Forecasting.py",
        "07_Segmentation.py","08_Carbon_Impact.py",
    ]
    result = []
    for i, (en, ar) in enumerate(pages):
        rel = PREFIX + filenames[i]
        result.append((rel, en, ar))
    return result

# ── Translations ──────────────────────────────────────────────────
TR = {
"EN":{
    "name":"Saudi Tourism Intelligence","sub":"AI ANALYTICS PLATFORM",
    "pill":"🇸🇦  OFFICIAL DATA · MINISTRY OF ECONOMY & PLANNING",
    "h1":"Saudi Tourism","h2":"Intelligence",
    "hs":"AI-powered analytics built on 10 years of official government data. Forecasting · Segmentation · Sustainability — all in one platform.",
    "hb":"Explore Dashboard →",
    # val, label, color_key, delta, delta_dir(up/down)
    "stats":[
        ("115.8M","Tourists 2024",       "teal",  "+23%","up"),
        ("1.10B", "Overnight Stays",     "teal",  "+41%","up"),
        ("5,622", "Avg Spend (SAR)",     "orange","+8%", "up"),
        (ML_ACCURACY, "ML Accuracy R²",      "orange","",""),
    ],
    "pt":"PLATFORM","ph":"8 Interactive Pages",
    "ps":"Comprehensive analysis covering every dimension of Saudi tourism",
    "pages":[
        ("🏠","Executive Overview","KPIs, trends & insights"),
        ("📈","Tourist Trends","Annual & monthly 2015–2024"),
        ("📅","Seasonality","Ramadan & summer peaks"),
        ("💰","Spending Analysis","Per trip, per night, by purpose"),
        ("🏨","Overnight Stays","Length of stay & COVID recovery"),
        ("🔮","Demand Forecasting","Prophet ML · 2025–2026"),
        ("🎯","Segmentation","K-Means · High / Mid / Budget"),
        ("🌱","Carbon Impact","CO₂ index & ESG sustainability"),
    ],
    "mt":"MACHINE LEARNING","mh":"3 Production ML Models",
    "ms":"Trained on 10 years of official Saudi government data",
    "ml":[
        ("🔮","Prophet","Demand Forecasting",
         "Predicts future tourist numbers using 10 years of seasonal patterns.",
         "24-month forecast · confidence bounds","teal"),
        ("🎯","K-Means","Tourist Segmentation",
         "Groups tourists into High / Mid / Budget value segments for targeted strategy.",
         "3 segments · Silhouette 0.630","orange"),
        ("💰","Gradient Boosting","Spending Prediction",
         "Predicts per-trip spending based on nationality, purpose & season.",
         "Full spend analysis · MAE SAR 184","blue"),
    ],
    "it":"KEY DISCOVERIES","ih":"Data Insights",
    "ins":[
        ("🏖️","Leisure overtook Religious as #1 purpose in 2024 — Vision 2030 ✅","teal"),
        ("⏰","Inbound avg stay: 8.6 → 19.2 nights (2021→2024) · +123%","orange"),
        ("💰","Inbound tourists spend 4× more than Domestic (SAR 5,622 vs 1,336)","blue"),
        ("🚀","2024 record: 115.9M tourists · +150% recovery from COVID low","teal_act"),
    ],
    # Vision 2030 progress bars
    "v30":[
        ("🎯 Tourist Arrivals Target",     115.9, 150.0, "M tourists by 2030",    "teal"),
        ("💰 Tourism GDP Contribution",    10.0,  10.0,  "% of GDP (achieved ✅)", "gold"),
        ("🌱 Carbon Intensity Reduction",  18.0,  30.0,  "% reduction by 2030",   "orange"),
        ("🏨 Hotel Capacity Expansion",    72.0,  100.0, "% of 500K rooms target", "blue"),
    ],
    "data":"DataSaudi · Ministry of Economy & Planning · 2015–2024",
    "copy":"© 2025 Saudi Tourism Intelligence · Eng. Goda Emad",
    "thm":"☀️  Light" if THEME=="dark" else "🌙  Dark",
    "lng":"🌐  العربية",
    "v30_title":"VISION 2030","v30_h":"Progress Toward Vision 2030 Targets",
},
"AR":{
    "name":"ذكاء السياحة السعودية","sub":"منصة تحليلات الذكاء الاصطناعي",
    "pill":"🇸🇦  بيانات رسمية · وزارة الاقتصاد والتخطيط",
    "h1":"ذكاء السياحة","h2":"السعودية",
    "hs":"تحليلات مدعومة بالذكاء الاصطناعي على 10 سنوات من البيانات الرسمية. توقعات · تقسيم · استدامة — كل شيء في منصة واحدة.",
    "hb":"← استكشف لوحة التحكم",
    "stats":[
        ("115.8M","سائح 2024",       "teal",  "+23%","up"),
        ("1.10B", "ليالي الإقامة",   "teal",  "+41%","up"),
        ("5,622", "متوسط الإنفاق",   "orange","+8%", "up"),
        (ML_ACCURACY, "دقة النموذج R²",  "orange","",""),
    ],
    "pt":"المنصة","ph":"8 صفحات تفاعلية",
    "ps":"تحليل شامل لكل أبعاد السياحة السعودية",
    "pages":[
        ("🏠","النظرة التنفيذية","مؤشرات الأداء والاتجاهات"),
        ("📈","اتجاهات السياحة","الأنماط السنوية والشهرية"),
        ("📅","الموسمية","ذروة الأشهر وتأثير رمضان"),
        ("💰","تحليل الإنفاق","لكل رحلة، لكل ليلة، حسب الغرض"),
        ("🏨","ليالي الإقامة","مدة الإقامة وتعافي كوفيد"),
        ("🔮","توقعات الطلب","Prophet ML · 2025–2026"),
        ("🎯","تقسيم السياح","K-Means · عالي/متوسط/اقتصادي"),
        ("🌱","الأثر الكربوني","مؤشر CO₂ واستدامة ESG"),
    ],
    "mt":"التعلم الآلي","mh":"3 نماذج ML جاهزة للإنتاج",
    "ms":"مدرّبة على 10 سنوات من البيانات السعودية الرسمية",
    "ml":[
        ("🔮","Prophet","توقع الطلب",
         "يتوقع أعداد السياح المستقبليين بناءً على أنماط موسمية لـ 10 سنوات.",
         "توقعات 24 شهرًا · فترات الثقة","teal"),
        ("🎯","K-Means","تقسيم السياح",
         "يصنف السياح إلى شرائح عالية / متوسطة / اقتصادية لاستراتيجية مستهدفة.",
         "3 شرائح · Silhouette 0.630","orange"),
        ("💰","Gradient Boosting","توقع الإنفاق",
         "يتوقع الإنفاق لكل رحلة بناءً على الجنسية والغرض والموسم.",
         "تحليل الإنفاق التنبؤي · MAE 184 ريال","blue"),
    ],
    "it":"الاكتشافات الرئيسية","ih":"رؤى البيانات",
    "ins":[
        ("🏖️","الترفيه تجاوز الديني كأول غرض في 2024 — إنجاز رؤية 2030 ✅","teal"),
        ("⏰","متوسط إقامة الوافد: 8.6 → 19.2 ليلة (2021→2024) · +123%","orange"),
        ("💰","الوافدون ينفقون 4 أضعاف المحليين (5,622 مقابل 1,336 ريال)","blue"),
        ("🚀","رقم قياسي 2024: 115.9M سائح · تعافي +150% من أدنى كوفيد","teal_act"),
    ],
    "v30":[
        ("🎯 مستهدف الوصول السياحي",     115.9, 150.0, "مليون سائح بحلول 2030",         "teal"),
        ("💰 مساهمة السياحة في الناتج",  10.0,  10.0,  "% من الناتج (تحقق ✅)",          "gold"),
        ("🌱 تخفيض الكثافة الكربونية",   18.0,  30.0,  "% تخفيض بحلول 2030",             "orange"),
        ("🏨 توسعة الطاقة الفندقية",     72.0,  100.0, "% من مستهدف 500 ألف غرفة",       "blue"),
    ],
    "data":"داتا السعودية · وزارة الاقتصاد والتخطيط · 2015–2024",
    "copy":"© 2025 ذكاء السياحة السعودية · م. جودة عماد",
    "thm":"☀️  فاتح" if THEME=="dark" else "🌙  داكن",
    "lng":"🌐  English",
    "v30_title":"رؤية 2030","v30_h":"التقدم نحو مستهدفات رؤية 2030",
},
}

t        = TR[LANG]
logo_b64 = _b64("assets/logo.jpg")
hero_b64 = _b64("assets/hero.jpg")
logo_src = "data:image/jpeg;base64,"+logo_b64 if logo_b64 else ""
hero_src = "data:image/jpeg;base64,"+hero_b64 if hero_b64 else ""
logo_img = ('<img src="'+logo_src+'" style="height:42px;border-radius:8px;"/>'
            if logo_src else '<span style="font-size:2rem;">🇸🇦</span>')
dir_val  = "rtl" if LANG=="AR" else "ltr"
ff       = "Tajawal" if LANG=="AR" else "IBM Plex Sans"

# ════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ════════════════════════════════════════════════════════════════════
st.markdown(_load_css(), unsafe_allow_html=True)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;600;700&family=Tajawal:wght@400;700;800&display=swap');

/* ── Hide Streamlit chrome ── */
[data-testid="stHeader"],[data-testid="stToolbar"],
[data-testid="stSidebarNav"],footer,#MainMenu{display:none!important;}
.block-container{padding:0!important;max-width:100%!important;}
section[data-testid="stMain"]>div:first-child{padding-top:0!important;}

/* ── Hero class ── */
.ds-hero{position:relative!important;width:100%!important;height:520px!important;
  overflow:hidden!important;background-size:cover!important;
  background-position:center center!important;}

/* ── Hover cards ── */
.ds-card{transition:transform .22s ease,border-color .22s,box-shadow .22s!important;cursor:pointer;}
.ds-card:hover{transform:translateY(-4px)!important;
  box-shadow:0 12px 32px rgba(23,177,155,.2)!important;}

/* ── Tooltip ── */
.ds-tooltip{position:relative;display:inline-block;}
.ds-tooltip .ds-tip{
  visibility:hidden;opacity:0;
  position:absolute;bottom:calc(100% + 8px);left:50%;
  transform:translateX(-50%);
  background:#0D1A1E;border:1px solid #17B19B44;
  color:#F4F9F8;font-size:.72rem;line-height:1.5;
  padding:8px 12px;border-radius:6px;
  width:220px;text-align:center;
  transition:opacity .2s;z-index:99;
  pointer-events:none;}
.ds-tooltip:hover .ds-tip{visibility:visible;opacity:1;}

/* ── Progress bar ── */
.ds-prog-bg{background:#2A3235;border-radius:8px;height:10px;overflow:hidden;}
.ds-prog-fill{height:100%;border-radius:8px;transition:width .8s ease;}

/* ── Sparkline SVG ── */
.ds-spark{opacity:.35;}

/* ── CTA Button — pulse on load + arrow slide on hover ── */
@keyframes ds-pulse{
  0%,100%{box-shadow:0 6px 28px rgba(23,177,155,.55);}
  50%{box-shadow:0 6px 40px rgba(23,177,155,.9),0 0 0 8px rgba(23,177,155,.12);}
}
@keyframes ds-arrow{
  0%,100%{transform:translateX(0);}
  50%{transform:translateX(5px);}
}
.ds-cta{
  animation:ds-pulse 2.6s ease-in-out infinite;
  transition:background .2s,transform .2s!important;
  color:#FFFFFF!important;
  text-decoration:none!important;
}
.ds-cta:hover{
  animation:none!important;
  transform:translateX(4px)!important;
  box-shadow:0 8px 40px rgba(23,177,155,.85)!important;
  background:#149581!important;
}
.ds-cta .ds-arrow-icon{
  display:inline-block;
  transition:transform .25s ease;
}
.ds-cta:hover .ds-arrow-icon{
  transform:translateX(6px);
}

/* ── Progress bar glow at tip ── */
.ds-prog-fill{
  position:relative;
  box-shadow:4px 0 12px currentColor;
}
.ds-prog-fill::after{
  content:'';position:absolute;
  right:-1px;top:50%;transform:translateY(-50%);
  width:10px;height:10px;border-radius:50%;
  background:inherit;
  box-shadow:0 0 8px 3px currentColor;
  opacity:.7;
}
</style>
"""+
"<style>"
"html,body,[data-testid='stAppViewContainer'],[data-testid='stMain']{"
"background:"+C["bg"]+"!important;direction:"+dir_val+";font-family:'"+ff+"',sans-serif;}"

# Sidebar
"[data-testid='stSidebar']{background:"+C["navbar"]+"!important;"
"border-right:1px solid "+C["border"]+"!important;}"
"[data-testid='stSidebar'] label,[data-testid='stSidebar'] span,"
"[data-testid='stSidebar'] p,[data-testid='stSidebar'] div{"
"color:"+C["white"]+"!important;}"

# ALL sidebar buttons base
"[data-testid='stSidebar'] .stButton>button{"
"background:transparent!important;border:1px solid transparent!important;"
"color:"+C["grey"]+"!important;border-radius:8px!important;"
"width:100%!important;font-size:.84rem!important;font-weight:500!important;"
"padding:9px 12px!important;margin-bottom:2px!important;transition:all .15s!important;}"
"[data-testid='stSidebar'] .stButton>button:hover{"
"background:"+C["teal"]+"22!important;border-color:"+C["teal"]+"44!important;"
"color:"+C["teal"]+"!important;}"

# Theme + Lang buttons — always dark filled regardless of mode
"[data-testid='stSidebar'] div:nth-child(3) .stButton>button,"
"[data-testid='stSidebar'] div:nth-child(4) .stButton>button{"
"background:#2A3235!important;border:1px solid #3A4C50!important;"
"color:#F4F9F8!important;font-weight:600!important;margin-bottom:5px!important;}"
"[data-testid='stSidebar'] div:nth-child(3) .stButton>button:hover,"
"[data-testid='stSidebar'] div:nth-child(4) .stButton>button:hover{"
"border-color:"+C["gold"]+"!important;color:"+C["gold"]+"!important;background:#2A3235!important;}"

# Gold slider
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

    # ── Navigation — hardcoded, works on Streamlit Cloud ──────────
    NAV_EN = [
        ("🏠  Overview",        "Overview.py"),
        ("📈  Tourist Trends",   "Tourist_Trends.py"),
        ("📅  Seasonality",      "Seasonality.py"),
        ("💰  Spending",         "Spending.py"),
        ("🏨  Overnight Stays",  "Overnight_Stays.py"),
        ("🔮  Forecasting",      "Forecasting.py"),
        ("🎯  Segmentation",     "Segmentation.py"),
        ("🌱  Carbon Impact",    "Carbon_Impact.py"),
    ]
    NAV_AR = [
        ("🏠  النظرة التنفيذية", "Overview.py"),
        ("📈  اتجاهات السياحة",  "Tourist_Trends.py"),
        ("📅  الموسمية",         "Seasonality.py"),
        ("💰  الإنفاق",          "Spending.py"),
        ("🏨  ليالي الإقامة",    "Overnight_Stays.py"),
        ("🔮  التوقعات",         "Forecasting.py"),
        ("🎯  التقسيم",          "Segmentation.py"),
        ("🌱  الأثر الكربوني",   "Carbon_Impact.py"),
    ]
    _nav = NAV_AR if LANG=="AR" else NAV_EN

    for label, fname in _nav:
        if st.button(label, key="nav_"+fname, use_container_width=True):
            st.switch_page("pages/" + fname)
    st.markdown('<div style="height:1px;background:'+C["border"]+';margin:10px 0;"></div>',
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
# HERO
# ════════════════════════════════════════════════════════════════════
hero_bg_val = ('url("'+hero_src+'")' if hero_src
               else "linear-gradient(135deg,"+C["navbar"]+","+C["bg"]+")")
st.markdown(
    "<style>.ds-hero{background-image:"+hero_bg_val+"!important;}</style>",
    unsafe_allow_html=True)

st.markdown(
    '<div class="ds-hero">'
    '<div style="position:absolute;inset:0;'
    'background:linear-gradient(100deg,'+C["navbar"]+'EE 0%,'+C["navbar"]+'99 38%,'
    +C["bg"]+'22 70%,transparent 100%);"></div>'
    '<div style="position:relative;z-index:2;padding:80px 52px;max-width:600px;">'
    '<div style="display:inline-flex;align-items:center;'
    'background:'+C["teal"]+'15;border:1px solid '+C["teal"]+'55;color:'+C["teal"]+';'
    'font-size:.58rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;'
    'padding:5px 14px;border-radius:4px;margin-bottom:22px;">'+t["pill"]+'</div>'
    '<div style="font-size:3.4rem;font-weight:800;color:'+C["white"]+';'
    'line-height:1.0;letter-spacing:-1.5px;margin-bottom:4px;">'+t["h1"]+'</div>'
    '<div style="font-size:3.4rem;font-weight:800;color:'+C["teal"]+';'
    'line-height:1.0;letter-spacing:-1.5px;margin-bottom:22px;">'+t["h2"]+'</div>'
    '<p style="font-size:.95rem;color:'+C["grey"]+';line-height:1.8;'
    'margin-bottom:30px;max-width:460px;">'+t["hs"]+'</p>'
    '<div id="hero-cta-placeholder"></div>'
    '</div></div>',
    unsafe_allow_html=True)

# Hero CTA — real st.button overlaid on hero
st.markdown("""
<style>
div[data-testid="stMain"] > div > div:nth-child(3){
  margin-top:-82px!important;
  padding-left:92px!important;
  position:relative!important;
  z-index:20!important;
  width:fit-content!important;
  pointer-events:auto!important;
}
div[data-testid="stMain"] > div > div:nth-child(3) button{
  background:#17B19B!important;color:#FFFFFF!important;
  font-size:.92rem!important;font-weight:700!important;
  padding:13px 28px!important;border-radius:7px!important;
  border:none!important;letter-spacing:.3px!important;
  box-shadow:0 6px 28px rgba(23,177,155,.55)!important;
  animation:ds-pulse 2.6s ease-in-out infinite!important;
}
div[data-testid="stMain"] > div > div:nth-child(3) button:hover{
  background:#149581!important;animation:none!important;
  transform:translateX(4px)!important;
}
</style>
""", unsafe_allow_html=True)

_cta = "Explore Dashboard  →" if LANG=="EN" else "←  استكشف لوحة التحكم"
if st.button(_cta, key="hero_cta"):
    st.switch_page("pages/Overview.py")



# ════════════════════════════════════════════════════════════════════
# STATS STRIP  — with delta arrows
# ════════════════════════════════════════════════════════════════════
cells = ""
for i,(val,lbl,ck,delta,ddir) in enumerate(t["stats"]):
    br = "border-right:1px solid "+C["border"]+";" if i<3 else ""
    arrow = ""
    if delta:
        a_color = "#17B19B" if ddir=="up" else "#C50A5D"
        a_icon  = "▲" if ddir=="up" else "▼"
        arrow = ('<span style="font-size:.72rem;color:'+a_color+';'
                 'font-weight:700;margin-left:6px;font-family:IBM Plex Mono,monospace;">'
                 +a_icon+' '+delta+'</span>')
    cells += (
        '<div style="padding:28px 24px;'+br+'">'
        '<div style="display:flex;align-items:baseline;gap:0;">'
        '<div style="font-size:2rem;font-weight:700;color:'+clr(ck)+';'
        'font-family:IBM Plex Mono,monospace;letter-spacing:-1px;">'+val+'</div>'
        +arrow+'</div>'
        '<div style="font-size:.64rem;color:'+C["grey"]+';text-transform:uppercase;'
        'letter-spacing:1.2px;font-weight:600;margin-top:6px;'
        'opacity:0.9;">'+lbl+'</div>'
        '</div>')
st.markdown(
    '<div style="background:'+C["sec_bg"]+';'
    'border-top:1px solid '+C["border"]+';border-bottom:1px solid '+C["border"]+';'
    'display:grid;grid-template-columns:repeat(4,1fr);">'+cells+'</div>',
    unsafe_allow_html=True)

# ── Section header helper ─────────────────────────────────────────
def sec_head(badge,h2,sub=""):
    o = ('<div style="margin-bottom:28px;">'
         '<div style="display:inline-block;background:'+C["teal"]+'15;'
         'border:1px solid '+C["teal"]+'44;color:'+C["teal"]+';'
         'font-size:.58rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;'
         'padding:4px 12px;border-radius:4px;margin-bottom:12px;">'+badge+'</div>'
         '<div style="font-size:1.5rem;font-weight:700;color:'+C["white"]+';margin-bottom:6px;">'+h2+'</div>')
    if sub: o += '<div style="font-size:.82rem;color:'+C["grey"]+';">'+sub+'</div>'
    return o+'</div>'

# ════════════════════════════════════════════════════════════════════
# PAGES — HTML cards (original design)
# ════════════════════════════════════════════════════════════════════
TXT_COL = C["white"]
page_cards = ""
for ico, title, desc in t["pages"]:
    page_cards += (
        '<div class="ds-card" style="background:'+C["card_bg"]+';'
        'border:1px solid '+C["border"]+';border-radius:10px;padding:20px 18px;">'
        '<div style="font-size:1.6rem;margin-bottom:10px;line-height:1;">'+ico+'</div>'
        '<div style="font-size:.87rem;font-weight:600;color:'+TXT_COL+';margin-bottom:5px;">'+title+'</div>'
        '<div style="font-size:.73rem;color:'+C["grey"]+';line-height:1.5;">'+desc+'</div>'
        '</div>')
st.markdown(
    '<div style="padding:52px 40px;">'+sec_head(t["pt"],t["ph"],t["ps"])+
    '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;">'+page_cards+'</div></div>',
    unsafe_allow_html=True)
st.markdown('<div style="height:1px;background:'+C["border"]+';margin:0 40px;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# ML MODELS — with tooltip + sparkline
# ════════════════════════════════════════════════════════════════════
def sparkline(color):
    # Simple SVG sparkline trend
    pts = "0,28 8,22 16,25 24,18 32,20 40,12 48,15 56,8 64,10 72,4"
    return (
        '<svg class="ds-spark" width="80" height="32" '
        'style="position:absolute;bottom:16px;right:14px;">'
        '<polyline points="'+pts+'" fill="none" stroke="'+color+'" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        '</svg>')

ml_cards = ""
for ico,name,mtype,tooltip,desc,ck in t["ml"]:
    ml_cards += (
        '<div style="background:'+C["card_bg"]+';border:1px solid '+C["border"]+';'
        'border-radius:10px;padding:26px 22px;position:relative;overflow:hidden;">'
        '<div style="position:absolute;top:0;left:0;right:0;height:3px;background:'+clr(ck)+';"></div>'
        +sparkline(clr(ck))+
        '<div style="font-size:1.5rem;margin-bottom:14px;">'+ico+'</div>'
        '<div class="ds-tooltip">'
        '<div style="font-size:1rem;font-weight:700;color:'+C["white"]+';'
        'font-family:IBM Plex Mono,monospace;margin-bottom:4px;'
        'border-bottom:1px dashed '+clr(ck)+'55;padding-bottom:3px;display:inline-block;">'
        +name+'</div>'
        '<div class="ds-tip">'+tooltip+'</div>'
        '</div>'
        '<div style="font-size:.67rem;font-weight:700;text-transform:uppercase;'
        'letter-spacing:1.2px;color:'+clr(ck)+';margin:8px 0 12px;">'+mtype+'</div>'
        '<div style="font-size:.8rem;color:'+C["grey"]+';line-height:1.6;">'+desc+'</div>'
        '</div>')
st.markdown(
    '<div style="padding:52px 40px;background:'+C["sec_bg"]+';'
    'border-top:1px solid '+C["border"]+';border-bottom:1px solid '+C["border"]+';">'+
    sec_head(t["mt"],t["mh"],t["ms"])+
    '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;">'+ml_cards+'</div></div>',
    unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# INSIGHTS
# ════════════════════════════════════════════════════════════════════
ins_cards = ""
for ico,txt,ck in t["ins"]:
    ins_cards += (
        '<div style="background:'+C["card_bg"]+';border:1px solid '+C["border"]+';'
        'border-left:3px solid '+clr(ck)+';border-radius:10px;'
        'padding:16px 18px;display:flex;align-items:flex-start;gap:12px;">'
        '<div style="font-size:1.2rem;flex-shrink:0;margin-top:2px;">'+ico+'</div>'
        '<div style="font-size:.83rem;color:'+C["white"]+';line-height:1.65;">'+txt+'</div>'
        '</div>')
st.markdown(
    '<div style="padding:52px 40px;">'+sec_head(t["it"],t["ih"])+
    '<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;">'+ins_cards+'</div></div>',
    unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# VISION 2030 PROGRESS
# ════════════════════════════════════════════════════════════════════
prog_bars = ""
for label, current, target, note, ck in t["v30"]:
    pct     = min(round(current/target*100), 100)
    col     = clr(ck)
    done    = pct >= 100
    badge   = (' <span style="color:'+col+';font-size:.8rem;">✅</span>' if done else "")
    # glow color via inline style trick — use filter
    glow    = "filter:drop-shadow(0 0 5px "+col+");" if not done else ""
    prog_bars += (
        '<div style="background:'+C["card_bg"]+';border:1px solid '+C["border"]+';'
        +(('border-color:'+col+'88;') if done else '')+
        'border-radius:10px;padding:18px 20px;">'
        '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">'
        '<div style="font-size:.84rem;font-weight:600;color:'+C["white"]+';">'+label+badge+'</div>'
        '<div style="font-size:.82rem;font-weight:700;color:'+col+';'
        'font-family:IBM Plex Mono,monospace;">'+str(pct)+'%</div>'
        '</div>'
        '<div class="ds-prog-bg">'
        '<div class="ds-prog-fill" style="width:'+str(pct)+'%;background:'+col+';'+glow+'"></div>'
        '</div>'
        '<div style="font-size:.68rem;color:'+C["grey"]+';margin-top:7px;">'+note+'</div>'
        '</div>')

st.markdown(
    '<div style="padding:52px 40px;background:'+C["sec_bg"]+';'
    'border-top:1px solid '+C["border"]+';border-bottom:1px solid '+C["border"]+';">'+
    sec_head(t["v30_title"],t["v30_h"])+
    '<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:14px;">'+prog_bars+'</div></div>',
    unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════
st.markdown(
    '<div style="background:'+C["navbar"]+';border-top:2px solid '+C["teal"]+';'
    'padding:28px 40px;display:flex;justify-content:space-between;'
    'align-items:center;flex-wrap:wrap;gap:16px;">'
    '<div style="display:flex;align-items:center;gap:14px;">'+logo_img+
    '<div>'
    '<div style="font-size:.9rem;font-weight:700;color:'+C["teal"]+';">'+t["name"]+'</div>'
    '<div style="font-size:.68rem;color:'+C["foot_txt"]+';margin-top:3px;">'+t["copy"]+'</div>'
    '<div style="font-size:.64rem;color:'+C["grey"]+';margin-top:3px;">📦 '+t["data"]+'</div>'
    '</div></div>'
    '<div style="display:flex;gap:24px;align-items:center;">'
    '<a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" target="_blank" '
    'style="font-size:.78rem;color:'+C["foot_txt"]+';text-decoration:none;font-weight:500;'
    'display:flex;align-items:center;gap:5px;">🐙 GitHub</a>'
    '<a href="https://www.linkedin.com/in/goda-emad/" target="_blank" '
    'style="font-size:.78rem;color:'+C["foot_txt"]+';text-decoration:none;font-weight:500;'
    'display:flex;align-items:center;gap:5px;">💼 LinkedIn</a>'
    '<a href="https://datasaudi.sa" target="_blank" '
    'style="font-size:.78rem;color:'+C["teal"]+';text-decoration:none;font-weight:600;'
    'display:flex;align-items:center;gap:5px;">📊 DataSaudi</a>'
    '</div></div>',
    unsafe_allow_html=True)
