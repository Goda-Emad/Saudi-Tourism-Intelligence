# ═══════════════════════════════════════════════════════════════════
#  Saudi Tourism Intelligence — Home Page  (FINAL)
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

# ── Colors ───────────────────────────────────────────────────────
C = {
    "teal":"#17B19B","teal_act":"#149581","bg":"#1A1E1F",
    "sec_bg":"#161B1C","card_bg":"#1E2528","navbar":"#031414",
    "white":"#F4F9F8","grey":"#A1A6B7","foot_txt":"#B5B8B7",
    "border":"#2A3235","orange":"#F4D044","gold":"#C9A84C","blue":"#365C8D",
} if THEME=="dark" else {
    "teal":"#17B19B","teal_act":"#149581","bg":"#F4F9F8",
    "sec_bg":"#E8EFEE","card_bg":"#FFFFFF","navbar":"#1A2628",
    "white":"#F4F9F8","grey":"#8BAFAA","foot_txt":"#8BAFAA",
    "border":"#2A3235","orange":"#C9950A","gold":"#A67C00","blue":"#365C8D",
}
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

# ── Auto-discover pages ───────────────────────────────────────────
@st.cache_data(show_spinner=False)
def _get_pages():
    base      = os.path.dirname(os.path.abspath(__file__))
    pages_dir = os.path.join(base, "pages")
    files     = sorted(glob.glob(os.path.join(pages_dir, "*.py")))
    result    = []
    for f in files:
        fname = os.path.basename(f)                         # 01_🏠_Overview.py
        rel   = "pages/" + fname                            # relative to app.py
        label = re.sub(r"^\d+_", "", fname[:-3])            # 🏠_Overview
        label = label.replace("_", " ")                     # 🏠 Overview
        result.append((rel, label))
    return result

# ── Translations ──────────────────────────────────────────────────
TR = {
"EN":{
    "name":"Saudi Tourism Intelligence","sub":"AI ANALYTICS PLATFORM",
    "pill":"🇸🇦  OFFICIAL DATA · MINISTRY OF ECONOMY & PLANNING",
    "h1":"Saudi Tourism","h2":"Intelligence",
    "hs":"AI-powered analytics built on 10 years of official government data. Forecasting · Segmentation · Sustainability — all in one platform.",
    "hb":"Explore Dashboard →",
    "stats":[("115.8M","Tourists 2024","teal"),("1.10B","Overnight Stays","teal"),
             ("5,622","Avg Spend (SAR)","orange"),("0.986","ML Accuracy R²","orange")],
    "pt":"PLATFORM","ph":"8 Interactive Pages",
    "ps":"Comprehensive analysis covering every dimension of Saudi tourism",
    "pages":[("🏠","Executive Overview","KPIs, trends & insights"),
             ("📈","Tourist Trends","Annual & monthly 2015–2024"),
             ("📅","Seasonality","Ramadan & summer peaks"),
             ("💰","Spending Analysis","Per trip, per night, by purpose"),
             ("🏨","Overnight Stays","Length of stay & COVID recovery"),
             ("🔮","Demand Forecasting","Prophet ML · 2025–2026"),
             ("🎯","Segmentation","K-Means · High / Mid / Budget"),
             ("🌱","Carbon Impact","CO₂ index & ESG sustainability")],
    "mt":"MACHINE LEARNING","mh":"3 Production ML Models",
    "ms":"Trained on 10 years of official Saudi government data",
    "ml":[("🔮","Prophet","Demand Forecasting","24-month predictions with confidence bounds","teal"),
          ("🎯","K-Means","Tourist Segmentation","3 segments · Silhouette Score 0.630","orange"),
          ("💰","Gradient Boosting","Spending Prediction","R²=0.986 · MAE: SAR 184/trip","blue")],
    "it":"INSIGHTS","ih":"Key Discoveries",
    "ins":[("🏖️","Leisure overtook Religious as #1 purpose in 2024 — Vision 2030 ✅","teal"),
           ("⏰","Inbound avg stay: 8.6 → 19.2 nights (2021→2024) · +123%","orange"),
           ("💰","Inbound tourists spend 4× more than Domestic (SAR 5,622 vs 1,336)","blue"),
           ("🚀","2024 record: 115.9M tourists · +150% recovery from COVID low","teal_act")],
    "data":"DataSaudi · Ministry of Economy & Planning · 2015–2024",
    "copy":"© 2025 Saudi Tourism Intelligence · Eng. Goda Emad",
    "thm":"☀️  Light" if THEME=="dark" else "🌙  Dark",
    "lng":"🌐  العربية",
},
"AR":{
    "name":"ذكاء السياحة السعودية","sub":"منصة تحليلات الذكاء الاصطناعي",
    "pill":"🇸🇦  بيانات رسمية · وزارة الاقتصاد والتخطيط",
    "h1":"ذكاء السياحة","h2":"السعودية",
    "hs":"تحليلات مدعومة بالذكاء الاصطناعي على 10 سنوات من البيانات الرسمية. توقعات · تقسيم · استدامة — كل شيء في منصة واحدة.",
    "hb":"← استكشف لوحة التحكم",
    "stats":[("115.8M","سائح 2024","teal"),("1.10B","ليالي الإقامة","teal"),
             ("5,622","متوسط الإنفاق","orange"),("0.986","دقة النموذج R²","orange")],
    "pt":"المنصة","ph":"8 صفحات تفاعلية",
    "ps":"تحليل شامل لكل أبعاد السياحة السعودية",
    "pages":[("🏠","النظرة التنفيذية","مؤشرات الأداء والاتجاهات"),
             ("📈","اتجاهات السياحة","الأنماط السنوية والشهرية"),
             ("📅","الموسمية","ذروة الأشهر وتأثير رمضان"),
             ("💰","تحليل الإنفاق","لكل رحلة، لكل ليلة، حسب الغرض"),
             ("🏨","ليالي الإقامة","مدة الإقامة وتعافي كوفيد"),
             ("🔮","توقعات الطلب","Prophet ML · 2025–2026"),
             ("🎯","تقسيم السياح","K-Means · عالي/متوسط/اقتصادي"),
             ("🌱","الأثر الكربوني","مؤشر CO₂ واستدامة ESG")],
    "mt":"التعلم الآلي","mh":"3 نماذج ML جاهزة للإنتاج",
    "ms":"مدرّبة على 10 سنوات من البيانات السعودية الرسمية",
    "ml":[("🔮","Prophet","توقع الطلب","توقعات 24 شهرًا مع فترات الثقة","teal"),
          ("🎯","K-Means","تقسيم السياح","3 شرائح · معامل Silhouette 0.630","orange"),
          ("💰","Gradient Boosting","توقع الإنفاق","R²=0.986 · MAE: 184 ريال/رحلة","blue")],
    "it":"الاستنتاجات","ih":"أبرز الاكتشافات",
    "ins":[("🏖️","الترفيه تجاوز الديني كأول غرض في 2024 — إنجاز رؤية 2030 ✅","teal"),
           ("⏰","متوسط إقامة الوافد: 8.6 → 19.2 ليلة (2021→2024) · +123%","orange"),
           ("💰","الوافدون ينفقون 4 أضعاف المحليين (5,622 مقابل 1,336 ريال)","blue"),
           ("🚀","رقم قياسي 2024: 115.9M سائح · تعافي +150% من أدنى كوفيد","teal_act")],
    "data":"داتا السعودية · وزارة الاقتصاد والتخطيط · 2015–2024",
    "copy":"© 2025 ذكاء السياحة السعودية · م. جودة عماد",
    "thm":"☀️  فاتح" if THEME=="dark" else "🌙  داكن",
    "lng":"🌐  English",
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
st.markdown(
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700"
    "&family=IBM+Plex+Mono:wght@400;600&family=Tajawal:wght@400;700;800&display=swap');"

    "[data-testid='stHeader'],[data-testid='stToolbar'],"
    "[data-testid='stSidebarNav'],footer,#MainMenu{display:none!important;}"
    ".block-container{padding:0!important;max-width:100%!important;}"
    "section[data-testid='stMain']>div:first-child{padding-top:0!important;}"

    "html,body,[data-testid='stAppViewContainer'],[data-testid='stMain']{"
    "background:"+C["bg"]+"!important;direction:"+dir_val+";font-family:'"+ff+"',sans-serif;}"

    # sidebar background — dark navbar in dark, light grey in light
    "[data-testid='stSidebar']{"
    "background:"+C["navbar"]+"!important;"
    "border-right:1px solid "+C["border"]+"!important;}"

    # ALL sidebar text visible in both modes
    "[data-testid='stSidebar'] label,"
    "[data-testid='stSidebar'] span,"
    "[data-testid='stSidebar'] p,"
    "[data-testid='stSidebar'] div{"
    "color:"+C["white"]+"!important;}"

    # Nav buttons — page links
    "[data-testid='stSidebar'] .stButton>button{"
    "background:transparent!important;"
    "border:1px solid transparent!important;"
    "color:"+C["grey"]+"!important;"
    "border-radius:8px!important;width:100%!important;"
    "font-size:.84rem!important;font-weight:500!important;"
    "padding:9px 12px!important;margin-bottom:2px!important;"
    "transition:all .15s!important;}"
    "[data-testid='stSidebar'] .stButton>button:hover{"
    "background:"+C["teal"]+"22!important;"
    "border-color:"+C["teal"]+"44!important;"
    "color:"+C["teal"]+"!important;}"

    # Theme + Lang buttons — first 2 styled as filled
    "[data-testid='stSidebar'] div[data-testid='stVerticalBlock']"
    ">div:nth-child(3) .stButton>button,"
    "[data-testid='stSidebar'] div[data-testid='stVerticalBlock']"
    ">div:nth-child(4) .stButton>button{"
    "background:"+C["card_bg"]+"!important;"
    "border:1px solid "+C["border"]+"!important;"
    "color:"+C["white"]+"!important;"
    "font-weight:600!important;margin-bottom:5px!important;}"
    "[data-testid='stSidebar'] div[data-testid='stVerticalBlock']"
    ">div:nth-child(3) .stButton>button:hover,"
    "[data-testid='stSidebar'] div[data-testid='stVerticalBlock']"
    ">div:nth-child(4) .stButton>button:hover{"
    "border-color:"+C["gold"]+"!important;"
    "color:"+C["gold"]+"!important;}"

    # Gold slider
    "[data-baseweb='slider']>div>div:nth-child(2){background:"+C["gold"]+"!important;}"
    "[data-baseweb='slider'] [role='slider']{"
    "background:"+C["gold"]+"!important;border-color:"+C["gold"]+"!important;"
    "box-shadow:0 0 0 4px "+C["gold"]+"22!important;}"
    "</style>",
    unsafe_allow_html=True,
)

# ════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Brand
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

    # Theme + Lang
    if st.button(t["thm"], key="k_thm", use_container_width=True):
        st.session_state.theme = "light" if THEME=="dark" else "dark"; st.rerun()
    if st.button(t["lng"], key="k_lng", use_container_width=True):
        st.session_state.lang  = "AR" if LANG=="EN" else "EN"; st.rerun()

    st.markdown('<div style="height:1px;background:'+C["border"]+';margin:10px 0 6px;"></div>',
                unsafe_allow_html=True)

    # ── Nav: st.switch_page via buttons — works on Streamlit Cloud ──
    pages = _get_pages()
    for rel_path, label in pages:
        if st.button(label, key="nav_"+rel_path, use_container_width=True):
            st.switch_page(rel_path)

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
        '</div>',
        unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# HERO
# ════════════════════════════════════════════════════════════════════
hero_bg = ('url("'+hero_src+'")' if hero_src
           else "linear-gradient(135deg,"+C["navbar"]+","+C["bg"]+")")

# inject hero CSS separately so height isn't eaten by Streamlit wrappers
st.markdown(
    "<style>"
    ".ds-hero{"
    "position:relative!important;width:100%!important;height:520px!important;"
    "overflow:hidden!important;"
    "background-image:"+hero_bg+"!important;"
    "background-size:cover!important;background-position:center center!important;}"
    "[data-testid='stMarkdownContainer']:has(.ds-hero){"
    "padding:0!important;margin:0!important;}"
    "</style>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="ds-hero">'

    '<div style="position:absolute;inset:0;'
    'background:linear-gradient(100deg,'
    +C["navbar"]+'EE 0%,'+C["navbar"]+'99 38%,'+C["bg"]+'33 70%,transparent 100%);"></div>'

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
    'margin-bottom:32px;max-width:460px;">'+t["hs"]+'</p>'

    '<a href="#" style="display:inline-flex;align-items:center;gap:8px;'
    'background:'+C["teal"]+';color:#031414!important;'
    'font-size:.9rem;font-weight:700;padding:13px 30px;border-radius:7px;'
    'text-decoration:none;box-shadow:0 6px 28px '+C["teal"]+'55;">'+t["hb"]+'</a>'
    '</div></div>',
    unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# STATS
# ════════════════════════════════════════════════════════════════════
cells = ""
for i,(val,lbl,ck) in enumerate(t["stats"]):
    br = "border-right:1px solid "+C["border"]+";" if i<3 else ""
    cells += (
        '<div style="padding:28px 24px;'+br+'">'
        '<div style="font-size:2rem;font-weight:700;color:'+clr(ck)+';'
        'font-family:IBM Plex Mono,monospace;letter-spacing:-1px;">'+val+'</div>'
        '<div style="font-size:.64rem;color:'+C["grey"]+';text-transform:uppercase;'
        'letter-spacing:1px;font-weight:500;margin-top:6px;">'+lbl+'</div>'
        '</div>')
st.markdown(
    '<div style="background:'+C["sec_bg"]+';'
    'border-top:1px solid '+C["border"]+';border-bottom:1px solid '+C["border"]+';'
    'display:grid;grid-template-columns:repeat(4,1fr);">'+cells+'</div>',
    unsafe_allow_html=True)

# ── Section header helper ─────────────────────────────────────────
def sec_head(badge, h2, sub=""):
    o = ('<div style="margin-bottom:28px;">'
         '<div style="display:inline-block;background:'+C["teal"]+'15;'
         'border:1px solid '+C["teal"]+'44;color:'+C["teal"]+';'
         'font-size:.58rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;'
         'padding:4px 12px;border-radius:4px;margin-bottom:12px;">'+badge+'</div>'
         '<div style="font-size:1.5rem;font-weight:700;color:'+C["white"]+';margin-bottom:6px;">'+h2+'</div>')
    if sub: o += '<div style="font-size:.82rem;color:'+C["grey"]+';">'+sub+'</div>'
    return o+'</div>'

# ════════════════════════════════════════════════════════════════════
# PAGES
# ════════════════════════════════════════════════════════════════════
page_cards = ""
for ico,title,desc in t["pages"]:
    page_cards += (
        '<div style="background:'+C["card_bg"]+';border:1px solid '+C["border"]+';'
        'border-radius:10px;padding:20px 18px;">'
        '<div style="font-size:1.5rem;margin-bottom:10px;">'+ico+'</div>'
        '<div style="font-size:.87rem;font-weight:600;color:'+C["white"]+';margin-bottom:5px;">'+title+'</div>'
        '<div style="font-size:.73rem;color:'+C["grey"]+';line-height:1.5;">'+desc+'</div>'
        '</div>')
st.markdown(
    '<div style="padding:52px 40px;">'+sec_head(t["pt"],t["ph"],t["ps"])+
    '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;">'+page_cards+'</div></div>',
    unsafe_allow_html=True)
st.markdown('<div style="height:1px;background:'+C["border"]+';margin:0 40px;"></div>',unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# ML MODELS
# ════════════════════════════════════════════════════════════════════
ml_cards = ""
for ico,name,mtype,desc,ck in t["ml"]:
    ml_cards += (
        '<div style="background:'+C["card_bg"]+';border:1px solid '+C["border"]+';'
        'border-radius:10px;padding:26px 22px;position:relative;overflow:hidden;">'
        '<div style="position:absolute;top:0;left:0;right:0;height:3px;background:'+clr(ck)+';"></div>'
        '<div style="font-size:1.5rem;margin-bottom:14px;">'+ico+'</div>'
        '<div style="font-size:1rem;font-weight:700;color:'+C["white"]+';'
        'font-family:IBM Plex Mono,monospace;margin-bottom:4px;">'+name+'</div>'
        '<div style="font-size:.67rem;font-weight:700;text-transform:uppercase;'
        'letter-spacing:1.2px;color:'+clr(ck)+';margin-bottom:12px;">'+mtype+'</div>'
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
# FOOTER
# ════════════════════════════════════════════════════════════════════
st.markdown(
    '<div style="background:'+C["navbar"]+';border-top:2px solid '+C["teal"]+';'
    'padding:22px 40px;display:flex;justify-content:space-between;'
    'align-items:center;flex-wrap:wrap;gap:12px;">'
    '<div style="display:flex;align-items:center;gap:14px;">'+logo_img+
    '<div>'
    '<div style="font-size:.88rem;font-weight:700;color:'+C["teal"]+';">'+t["name"]+'</div>'
    '<div style="font-size:.66rem;color:'+C["foot_txt"]+';margin-top:2px;">'+t["copy"]+'</div>'
    '<div style="font-size:.63rem;color:'+C["grey"]+';margin-top:2px;">📦 '+t["data"]+'</div>'
    '</div></div>'
    '<div style="display:flex;gap:20px;align-items:center;">'
    '<a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" target="_blank" '
    'style="font-size:.75rem;color:'+C["foot_txt"]+';text-decoration:none;">🐙 GitHub</a>'
    '<a href="https://www.linkedin.com/in/goda-emad/" target="_blank" '
    'style="font-size:.75rem;color:'+C["foot_txt"]+';text-decoration:none;">💼 LinkedIn</a>'
    '<a href="https://datasaudi.sa" target="_blank" '
    'style="font-size:.75rem;color:'+C["teal"]+';text-decoration:none;font-weight:600;">📊 DataSaudi</a>'
    '</div></div>',
    unsafe_allow_html=True)
