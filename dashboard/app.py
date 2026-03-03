# ═══════════════════════════════════════════════════════════════════
#  Saudi Tourism Intelligence — Home Page
#  Author : Eng. Goda Emad
#  Design : DataSaudi Official Design System
# ═══════════════════════════════════════════════════════════════════
import streamlit as st
import base64, os

st.set_page_config(
    page_title="Saudi Tourism Intelligence",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

for k, v in [("lang","EN"),("theme","dark")]:
    if k not in st.session_state:
        st.session_state[k] = v

LANG  = st.session_state.lang
THEME = st.session_state.theme

# ── DataSaudi Official Colors ────────────────────────────────────
C = {
    "teal":     "#17B19B", "teal_act": "#149581", "teal_sec": "#8BAFAA",
    "bg":       "#1A1E1F", "sec_bg":   "#161B1C", "dark_bg":  "#373D44",
    "navbar":   "#031414", "white":    "#F4F9F8", "grey":     "#A1A6B7",
    "foot_txt": "#B5B8B7", "border":   "#2A3235", "orange":   "#F4D044",
    "gold":     "#C9A84C", "blue":     "#365C8D",
} if THEME == "dark" else {
    "teal":     "#17B19B", "teal_act": "#149581", "teal_sec": "#4A8A82",
    "bg":       "#F4F9F8", "sec_bg":   "#E8EFEE", "dark_bg":  "#DDE6E4",
    "navbar":   "#FFFFFF", "white":    "#0D1414", "grey":     "#4A5568",
    "foot_txt": "#718096", "border":   "#C8D8D5", "orange":   "#C9950A",
    "gold":     "#A67C00", "blue":     "#365C8D",
}

def clr(k): return C.get(k, C["teal"])

@st.cache_data(show_spinner=False)
def _read(p):
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, p), "rb") as f: return f.read()

@st.cache_data(show_spinner=False)
def _b64(p):
    try:    return base64.b64encode(_read(p)).decode()
    except: return ""

@st.cache_data(show_spinner=False)
def _load_css():
    try:    return "<style>" + _read("assets/style.css").decode() + "</style>"
    except: return ""

# ── Translations ─────────────────────────────────────────────────
TR = {
"EN": {
    "name":"Saudi Tourism Intelligence", "sub":"AI ANALYTICS PLATFORM",
    "pill":"🇸🇦  OFFICIAL DATA · MINISTRY OF ECONOMY & PLANNING",
    "h1":"Saudi Tourism", "h2":"Intelligence",
    "hs":"AI-powered analytics built on 10 years of official government data. Forecasting · Segmentation · Sustainability — all in one platform.",
    "hb":"Explore Dashboard →",
    "stats":[("115.8M","Tourists 2024","teal"),("1.10B","Overnight Stays","teal"),
             ("5,622","Avg Spend (SAR)","orange"),("0.986","ML Accuracy R²","orange")],
    "pt":"PLATFORM", "ph":"8 Interactive Pages",
    "ps":"Comprehensive analysis covering every dimension of Saudi tourism",
    "pages":[
        ("🏠","Executive Overview","KPIs, trends & insights"),
        ("📈","Tourist Trends","Annual & monthly patterns 2015–2024"),
        ("📅","Seasonality","Peak months, Ramadan & summer effects"),
        ("💰","Spending Analysis","Per trip, per night, by purpose"),
        ("🏨","Overnight Stays","Length of stay & COVID recovery"),
        ("🔮","Demand Forecasting","Prophet ML · 2025–2026 predictions"),
        ("🎯","Segmentation","K-Means · High / Mid / Budget"),
        ("🌱","Carbon Impact","CO₂ index & ESG sustainability"),
    ],
    "mt":"MACHINE LEARNING", "mh":"3 Production ML Models",
    "ms":"Trained on 10 years of official Saudi government data",
    "ml":[
        ("🔮","Prophet","Demand Forecasting","24-month predictions with confidence bounds","teal"),
        ("🎯","K-Means","Tourist Segmentation","3 value segments · Silhouette Score: 0.630","orange"),
        ("💰","Gradient Boosting","Spending Prediction","R² = 0.986 · MAE: SAR 184 per trip","blue"),
    ],
    "it":"INSIGHTS", "ih":"Key Discoveries",
    "ins":[
        ("🏖️","Leisure overtook Religious as #1 purpose in 2024 — Vision 2030 milestone ✅","teal"),
        ("⏰","Inbound avg stay: 8.6 → 19.2 nights (2021→2024) · +123% growth","orange"),
        ("💰","Inbound tourists spend 4× more than Domestic (SAR 5,622 vs SAR 1,336)","blue"),
        ("🚀","2024 record: 115.9M tourists · +150% recovery from COVID low","teal_act"),
    ],
    "data":"DataSaudi · Ministry of Economy & Planning · 2015–2024",
    "copy":"© 2025 Saudi Tourism Intelligence · Eng. Goda Emad · All rights reserved",
    "lng":"AR", "thm":"☀️" if THEME=="dark" else "🌙",
},
"AR": {
    "name":"ذكاء السياحة السعودية", "sub":"منصة تحليلات الذكاء الاصطناعي",
    "pill":"🇸🇦  بيانات رسمية · وزارة الاقتصاد والتخطيط",
    "h1":"ذكاء السياحة", "h2":"السعودية",
    "hs":"تحليلات مدعومة بالذكاء الاصطناعي على 10 سنوات من البيانات الرسمية. توقعات · تقسيم · استدامة — كل شيء في منصة واحدة.",
    "hb":"← استكشف لوحة التحكم",
    "stats":[("115.8M","سائح 2024","teal"),("1.10B","ليالي الإقامة","teal"),
             ("5,622","متوسط الإنفاق (ريال)","orange"),("0.986","دقة النموذج R²","orange")],
    "pt":"المنصة", "ph":"8 صفحات تفاعلية",
    "ps":"تحليل شامل لكل أبعاد السياحة السعودية",
    "pages":[
        ("🏠","النظرة التنفيذية","مؤشرات الأداء والاتجاهات"),
        ("📈","اتجاهات السياحة","الأنماط السنوية والشهرية 2015–2024"),
        ("📅","الموسمية","ذروة الأشهر وتأثير رمضان والصيف"),
        ("💰","تحليل الإنفاق","لكل رحلة، لكل ليلة، حسب الغرض"),
        ("🏨","ليالي الإقامة","مدة الإقامة وتعافي كوفيد"),
        ("🔮","توقعات الطلب","Prophet ML · 2025–2026"),
        ("🎯","تقسيم السياح","K-Means · عالي/متوسط/اقتصادي"),
        ("🌱","الأثر الكربوني","مؤشر CO₂ واستدامة ESG"),
    ],
    "mt":"التعلم الآلي", "mh":"3 نماذج ML جاهزة للإنتاج",
    "ms":"مدرّبة على 10 سنوات من البيانات السعودية الرسمية",
    "ml":[
        ("🔮","Prophet","توقع الطلب","توقعات 24 شهرًا مع فترات الثقة","teal"),
        ("🎯","K-Means","تقسيم السياح","3 شرائح · معامل Silhouette: 0.630","orange"),
        ("💰","Gradient Boosting","توقع الإنفاق","R² = 0.986 · MAE: 184 ريال/رحلة","blue"),
    ],
    "it":"الاستنتاجات", "ih":"أبرز الاكتشافات",
    "ins":[
        ("🏖️","الترفيه تجاوز الديني كأول غرض في 2024 — إنجاز رؤية 2030 ✅","teal"),
        ("⏰","متوسط إقامة الوافد: 8.6 → 19.2 ليلة (2021→2024) · +123%","orange"),
        ("💰","الوافدون ينفقون 4 أضعاف المحليين (5,622 مقابل 1,336 ريال)","blue"),
        ("🚀","رقم قياسي 2024: 115.9M سائح · تعافي +150% من أدنى كوفيد","teal_act"),
    ],
    "data":"داتا السعودية · وزارة الاقتصاد والتخطيط · 2015–2024",
    "copy":"© 2025 ذكاء السياحة السعودية · م. جودة عماد · جميع الحقوق محفوظة",
    "lng":"EN", "thm":"☀️" if THEME=="dark" else "🌙",
},
}

t        = TR[LANG]
logo_b64 = _b64("assets/logo.jpg")
hero_b64 = _b64("assets/hero.jpg")
logo_src = "data:image/jpeg;base64," + logo_b64 if logo_b64 else ""
hero_src = "data:image/jpeg;base64," + hero_b64 if hero_b64 else ""
logo_img = ('<img src="' + logo_src + '" style="height:38px;border-radius:6px;"/>'
            if logo_src else "🇸🇦")
dir_val  = "rtl" if LANG == "AR" else "ltr"
ff       = "Tajawal" if LANG == "AR" else "IBM Plex Sans"

# ════════════════════════════════════════════════════════════════════
# GLOBAL CSS  (injected once — hides all Streamlit chrome)
# ════════════════════════════════════════════════════════════════════
st.markdown(_load_css(), unsafe_allow_html=True)

st.markdown("""
<style>
/* ── Hide all Streamlit chrome ── */
[data-testid="stHeader"],[data-testid="stToolbar"],
[data-testid="stSidebarNav"],footer,
#MainMenu {display:none!important;}
[data-testid="stSidebar"]{display:none!important;}
.block-container{padding:0!important;max-width:100%!important;}
section[data-testid="stMain"] > div:first-child{padding:0!important;}

/* ── Topbar buttons ── */
.stButton > button {
  background: #373D44 !important;
  border: 1px solid #2A3235 !important;
  color: #F4F9F8 !important;
  border-radius: 6px !important;
  font-size: .78rem !important;
  font-weight: 600 !important;
  transition: border-color .2s, color .2s !important;
  padding: 6px 18px !important;
}
.stButton > button:hover {
  border-color: #C9A84C !important;
  color: #C9A84C !important;
}

/* ── Gold Slider ── */
[data-baseweb="slider"] > div > div:nth-child(2) {background:#C9A84C!important;}
[data-baseweb="slider"] [role="slider"] {
  background:#C9A84C!important;
  border-color:#C9A84C!important;
  box-shadow:0 0 0 4px #C9A84C22!important;
}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# HTML BUILDER — uses double quotes only inside style attrs
# ════════════════════════════════════════════════════════════════════
def pill(label, color=None):
    color = color or C["teal"]
    return (
        '<span style="display:inline-block;'
        'background:' + color + '18;'
        'border:1px solid ' + color + '66;'
        'color:' + color + ';'
        'font-size:.6rem;font-weight:700;letter-spacing:2px;'
        'text-transform:uppercase;padding:4px 12px;'
        'border-radius:4px;margin-bottom:10px;">'
        + label + '</span>'
    )

def card(content, extra_style=""):
    return (
        '<div style="background:' + C["dark_bg"] + ';'
        'border:1px solid ' + C["border"] + ';'
        'border-radius:8px;padding:20px 18px;'
        'transition:border-color .25s,transform .25s,box-shadow .25s;'
        + extra_style + '">' + content + '</div>'
    )

def sec_head(badge_txt, h2, sub=""):
    return (
        '<div style="margin-bottom:28px;">'
        + pill(badge_txt) +
        '<div style="font-size:1.45rem;font-weight:700;color:' + C["white"] + ';margin-bottom:6px;">'
        + h2 + '</div>'
        + ('<div style="font-size:.82rem;color:' + C["grey"] + ';">' + sub + '</div>' if sub else '')
        + '</div>'
    )

# ── TOPBAR ────────────────────────────────────────────────────────
cb, _, ct, cl = st.columns([5, 4, 0.6, 0.7])
with cb:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:12px;padding:11px 0;">'
        + logo_img +
        '<div>'
        '<div style="font-size:.92rem;font-weight:700;color:' + C["white"] + ';">' + t["name"] + '</div>'
        '<div style="font-size:.6rem;color:' + C["teal"] + ';font-weight:600;'
        'letter-spacing:1.4px;text-transform:uppercase;">' + t["sub"] + '</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )
with ct:
    if st.button(t["thm"], key="k_thm", use_container_width=True):
        st.session_state.theme = "light" if THEME=="dark" else "dark"; st.rerun()
with cl:
    if st.button(t["lng"], key="k_lng", use_container_width=True):
        st.session_state.lang = "AR" if LANG=="EN" else "EN"; st.rerun()

st.markdown('<div style="height:1px;background:' + C["border"] + ';"></div>', unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────
hero_bg = ('url("' + hero_src + '")') if hero_src else ('linear-gradient(135deg,' + C["navbar"] + ',' + C["bg"] + ')')

st.markdown(
    '<div style="position:relative;aspect-ratio:16/6;width:100%;overflow:hidden;'
    'background-image:' + hero_bg + ';background-size:cover;background-position:center;">'

    '<div style="position:absolute;inset:0;'
    'background:linear-gradient(105deg,' + C["navbar"] + 'F2 0%,' + C["dark_bg"] + '99 45%,transparent 100%);"></div>'

    '<div style="position:relative;z-index:2;padding:5% 5%;max-width:52%;height:100%;'
    'display:flex;flex-direction:column;justify-content:center;">'

    + pill(t["pill"]) +

    '<div style="font-size:clamp(2rem,3.5vw,3.2rem);font-weight:800;'
    'color:' + C["white"] + ';line-height:1.05;margin-bottom:4px;letter-spacing:-.5px;">' + t["h1"] + '</div>'

    '<div style="font-size:clamp(2rem,3.5vw,3.2rem);font-weight:800;'
    'color:' + C["teal"] + ';line-height:1.05;margin-bottom:20px;letter-spacing:-.5px;">' + t["h2"] + '</div>'

    '<p style="font-size:clamp(.78rem,1.1vw,.92rem);color:' + C["grey"] + ';'
    'line-height:1.75;margin-bottom:28px;max-width:460px;">' + t["hs"] + '</p>'

    '<a href="#" style="display:inline-flex;align-items:center;gap:8px;'
    'background:' + C["teal"] + ';color:' + C["navbar"] + '!important;'
    'font-size:.88rem;font-weight:700;padding:12px 28px;border-radius:6px;'
    'text-decoration:none;width:fit-content;'
    'box-shadow:0 4px 24px ' + C["teal"] + '55;transition:background .2s,transform .2s;">'
    + t["hb"] + '</a>'

    '</div></div>',
    unsafe_allow_html=True,
)

# ── STATS STRIP ───────────────────────────────────────────────────
cells = ""
for i, (val, lbl, ck) in enumerate(t["stats"]):
    br = 'border-right:1px solid ' + C["border"] + ';' if i < 3 else ''
    cells += (
        '<div style="padding:28px 24px;' + br + '">'
        '<div style="font-size:2rem;font-weight:700;color:' + clr(ck) + ';'
        'font-family:IBM Plex Mono,monospace;">' + val + '</div>'
        '<div style="font-size:.66rem;color:' + C["grey"] + ';text-transform:uppercase;'
        'letter-spacing:.9px;font-weight:500;margin-top:6px;">' + lbl + '</div>'
        '</div>'
    )
st.markdown(
    '<div style="background:' + C["sec_bg"] + ';'
    'border-top:1px solid ' + C["border"] + ';border-bottom:1px solid ' + C["border"] + ';'
    'display:grid;grid-template-columns:repeat(4,1fr);">'
    + cells + '</div>',
    unsafe_allow_html=True,
)

# ── PAGES SECTION ─────────────────────────────────────────────────
page_cards = ""
for ico, title, desc in t["pages"]:
    page_cards += card(
        '<div style="font-size:1.5rem;margin-bottom:10px;">' + ico + '</div>'
        '<div style="font-size:.87rem;font-weight:600;color:' + C["white"] + ';margin-bottom:5px;">' + title + '</div>'
        '<div style="font-size:.73rem;color:' + C["grey"] + ';line-height:1.5;">' + desc + '</div>'
    )

st.markdown(
    '<div style="padding:52px 40px;">'
    + sec_head(t["pt"], t["ph"], t["ps"]) +
    '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;">'
    + page_cards + '</div></div>',
    unsafe_allow_html=True,
)
st.markdown('<div style="height:1px;background:' + C["border"] + ';margin:0 40px;"></div>', unsafe_allow_html=True)

# ── ML MODELS ─────────────────────────────────────────────────────
ml_cards = ""
for ico, name, mtype, desc, ck in t["ml"]:
    ml_cards += card(
        '<div style="position:absolute;top:0;left:0;right:0;height:3px;background:' + clr(ck) + ';"></div>'
        '<div style="font-size:1.5rem;margin-bottom:14px;">' + ico + '</div>'
        '<div style="font-size:1rem;font-weight:700;color:' + C["white"] + ';'
        'font-family:IBM Plex Mono,monospace;margin-bottom:4px;">' + name + '</div>'
        '<div style="font-size:.68rem;font-weight:700;text-transform:uppercase;'
        'letter-spacing:1.2px;color:' + clr(ck) + ';margin-bottom:12px;">' + mtype + '</div>'
        '<div style="font-size:.8rem;color:' + C["grey"] + ';line-height:1.6;">' + desc + '</div>',
        extra_style="position:relative;overflow:hidden;padding:26px 22px;"
    )

st.markdown(
    '<div style="padding:52px 40px;background:' + C["sec_bg"] + ';'
    'border-top:1px solid ' + C["border"] + ';border-bottom:1px solid ' + C["border"] + ';">'
    + sec_head(t["mt"], t["mh"], t["ms"]) +
    '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;">'
    + ml_cards + '</div></div>',
    unsafe_allow_html=True,
)

# ── INSIGHTS ──────────────────────────────────────────────────────
ins_cards = ""
for ico, txt, ck in t["ins"]:
    ins_cards += (
        '<div style="background:' + C["dark_bg"] + ';border:1px solid ' + C["border"] + ';'
        'border-left:3px solid ' + clr(ck) + ';border-radius:8px;'
        'padding:16px 18px;display:flex;align-items:flex-start;gap:12px;">'
        '<div style="font-size:1.2rem;flex-shrink:0;margin-top:2px;">' + ico + '</div>'
        '<div style="font-size:.83rem;color:' + C["white"] + ';line-height:1.6;">' + txt + '</div>'
        '</div>'
    )

st.markdown(
    '<div style="padding:52px 40px;">'
    + sec_head(t["it"], t["ih"]) +
    '<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;">'
    + ins_cards + '</div></div>',
    unsafe_allow_html=True,
)

# ── FOOTER ────────────────────────────────────────────────────────
st.markdown(
    '<div style="background:' + C["navbar"] + ';border-top:2px solid ' + C["teal"] + ';'
    'padding:24px 40px;display:flex;justify-content:space-between;'
    'align-items:center;flex-wrap:wrap;gap:14px;">'

    '<div style="display:flex;align-items:center;gap:14px;">'
    + logo_img +
    '<div>'
    '<div style="font-size:.88rem;font-weight:700;color:' + C["teal"] + ';">' + t["name"] + '</div>'
    '<div style="font-size:.67rem;color:' + C["foot_txt"] + ';margin-top:2px;">' + t["copy"] + '</div>'
    '<div style="font-size:.64rem;color:' + C["grey"] + ';margin-top:2px;">📦 ' + t["data"] + '</div>'
    '</div></div>'

    '<div style="display:flex;gap:22px;align-items:center;">'
    '<a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" target="_blank" '
    'style="font-size:.76rem;color:' + C["foot_txt"] + ';text-decoration:none;font-weight:500;">🐙 GitHub</a>'
    '<a href="https://www.linkedin.com/in/goda-emad/" target="_blank" '
    'style="font-size:.76rem;color:' + C["foot_txt"] + ';text-decoration:none;font-weight:500;">💼 LinkedIn</a>'
    '<a href="https://datasaudi.sa" target="_blank" '
    'style="font-size:.76rem;color:' + C["teal"] + ';text-decoration:none;font-weight:600;">📊 DataSaudi</a>'
    '</div></div>',
    unsafe_allow_html=True,
)
