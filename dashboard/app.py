# ═══════════════════════════════════════════════════════════════════
#  Saudi Tourism Intelligence — Home Page
#  Author  : Eng. Goda Emad
#  GitHub  : github.com/Goda-Emad/Saudi-Tourism-Intelligence
#  Design  : DataSaudi Official Design System
# ═══════════════════════════════════════════════════════════════════
import streamlit as st
import base64, os

st.set_page_config(
    page_title            = "Saudi Tourism Intelligence",
    page_icon             = "🇸🇦",
    layout                = "wide",
    initial_sidebar_state = "collapsed",
)

# ── Session State ────────────────────────────────────────────────
if "lang"  not in st.session_state: st.session_state.lang  = "EN"
if "theme" not in st.session_state: st.session_state.theme = "dark"
LANG  = st.session_state.lang
THEME = st.session_state.theme

# ── DataSaudi Official Color System ─────────────────────────────
DS_DARK = {
    "teal":       "#17B19B",
    "teal_act":   "#149581",
    "teal_sec":   "#8BAFAA",
    "bg":         "#1A1E1F",
    "sec_bg":     "#161B1C",
    "dark_bg":    "#373D44",
    "navbar":     "#031414",
    "white":      "#F4F9F8",
    "grey":       "#A1A6B7",
    "foot_grey":  "#B5B8B7",
    "off_white":  "#D9D9D9",
    "blue":       "#365C8D",
    "yellow":     "#FDE725",
    "purple":     "#620E8B",
    "orange":     "#F4D044",
    "pink":       "#C50A5D",
    "border":     "#2A3235",
}
DS_LIGHT = {
    **DS_DARK,
    "bg":       "#F4F9F8",
    "sec_bg":   "#E8EFEE",
    "dark_bg":  "#DDE6E4",
    "navbar":   "#FFFFFF",
    "white":    "#0D1414",
    "grey":     "#4A5568",
    "foot_grey":"#718096",
    "border":   "#C8D8D5",
}
C = DS_DARK if THEME == "dark" else DS_LIGHT

# ── Cached Helpers — run ONCE, never again ──────────────────────
@st.cache_data(show_spinner=False)
def _read(p: str) -> bytes:
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, p), "rb") as f: return f.read()

@st.cache_data(show_spinner=False)
def _b64(p: str) -> str:
    try:    return base64.b64encode(_read(p)).decode()
    except: return ""

@st.cache_data(show_spinner=False)
def _load_css() -> str:
    try:    return f"<style>{_read('assets/style.css').decode()}</style>"
    except: return ""

@st.cache_data(show_spinner=False)
def _patch(theme: str, lang: str) -> str:
    bg  = DS_DARK["bg"]      if theme=="dark" else DS_LIGHT["bg"]
    nav = DS_DARK["navbar"]  if theme=="dark" else DS_LIGHT["navbar"]
    txt = DS_DARK["white"]   if theme=="dark" else DS_LIGHT["white"]
    dir = "rtl"  if lang=="AR" else "ltr"
    ff  = "Tajawal" if lang=="AR" else "IBM Plex Sans"
    return f"""<style>
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{{
  background:{bg}!important;color:{txt};direction:{dir};
  font-family:'{ff}',sans-serif;}}
[data-testid="stSidebar"]{{background:{nav}!important;}}
[data-testid="stHeader"],[data-testid="stToolbar"],footer{{display:none!important;}}
.block-container{{padding:0!important;max-width:100%!important;}}
.stButton>button{{
  background:{DS_DARK['dark_bg'] if theme=='dark' else '#E8EFEE'}!important;
  border:1px solid {'#3A4248' if theme=='dark' else '#C8D8D5'}!important;
  color:{txt}!important;border-radius:6px!important;
  font-size:.78rem!important;font-weight:600!important;
  font-family:'{ff}',sans-serif!important;transition:all .2s!important;}}
.stButton>button:hover{{
  border-color:{DS_DARK['teal']}!important;
  color:{DS_DARK['teal']}!important;}}
</style>"""

# ── Translations ─────────────────────────────────────────────────
TR = {
"EN": dict(
    name="Saudi Tourism Intelligence", sub="AI ANALYTICS PLATFORM",
    pill="🇸🇦  OFFICIAL DATA · MINISTRY OF ECONOMY & PLANNING",
    h1="Saudi Tourism", h2="Intelligence",
    hs=("AI-powered analytics built on 10 years of official government data. "
        "Forecasting · Segmentation · Sustainability — all in one platform."),
    hb="Explore Dashboard →",
    stats=[("115.8M","Tourists 2024","teal"),("1.10B","Overnight Stays","teal"),
           ("5,622","Avg Spend (SAR)","orange"),("0.986","ML Accuracy R²","orange")],
    pt="PLATFORM", ph="8 Interactive Pages",
    ps="Comprehensive analysis covering every dimension of Saudi tourism",
    pages=[("🏠","Executive Overview","KPIs, trends & insights at a glance"),
           ("📈","Tourist Trends","Annual & monthly patterns 2015–2024"),
           ("📅","Seasonality","Peak months, Ramadan & summer effects"),
           ("💰","Spending Analysis","Per trip, per night, by purpose"),
           ("🏨","Overnight Stays","Length of stay & COVID recovery"),
           ("🔮","Demand Forecasting","Prophet ML · 2025–2026 predictions"),
           ("🎯","Segmentation","K-Means · High / Mid / Budget"),
           ("🌱","Carbon Impact","CO₂ index & ESG sustainability")],
    mt="MACHINE LEARNING", mh="3 Production ML Models",
    ms="Trained on 10 years of official Saudi government data",
    ml=[("🔮","Prophet","Demand Forecasting",
         "24-month predictions with upper/lower confidence bounds","teal"),
        ("🎯","K-Means","Tourist Segmentation",
         "3 value segments · Silhouette Score: 0.630","orange"),
        ("💰","Gradient Boosting","Spending Prediction",
         "R² = 0.986 · MAE: SAR 184 per trip","blue")],
    it="INSIGHTS", ih="Key Discoveries",
    ins=[("🏖️","Leisure overtook Religious as #1 purpose in 2024 — Vision 2030 milestone ✅","teal"),
         ("⏰","Inbound avg stay: 8.6 → 19.2 nights (2021→2024) · +123% growth","orange"),
         ("💰","Inbound tourists spend 4× more than Domestic (SAR 5,622 vs SAR 1,336)","blue"),
         ("🚀","2024 record: 115.9M tourists · +150% recovery from COVID low","teal_act")],
    data="DataSaudi · Ministry of Economy & Planning · 2015–2024",
    copy="© 2025 Saudi Tourism Intelligence · Eng. Goda Emad · All rights reserved",
    lng="AR", thm="☀️" if THEME=="dark" else "🌙",
),
"AR": dict(
    name="ذكاء السياحة السعودية", sub="منصة تحليلات الذكاء الاصطناعي",
    pill="🇸🇦  بيانات رسمية · وزارة الاقتصاد والتخطيط",
    h1="ذكاء السياحة", h2="السعودية",
    hs=("منصة تحليلات على 10 سنوات من البيانات الرسمية. "
        "توقعات · تقسيم · استدامة — كل شيء في منصة واحدة."),
    hb="← استكشف لوحة التحكم",
    stats=[("115.8M","سائح 2024","teal"),("1.10B","ليالي الإقامة","teal"),
           ("5,622","متوسط الإنفاق (ريال)","orange"),("0.986","دقة النموذج R²","orange")],
    pt="المنصة", ph="8 صفحات تفاعلية",
    ps="تحليل شامل لكل أبعاد السياحة السعودية",
    pages=[("🏠","النظرة التنفيذية","مؤشرات الأداء والاتجاهات"),
           ("📈","اتجاهات السياحة","الأنماط السنوية والشهرية 2015–2024"),
           ("📅","الموسمية","ذروة الأشهر وتأثير رمضان والصيف"),
           ("💰","تحليل الإنفاق","لكل رحلة، لكل ليلة، حسب الغرض"),
           ("🏨","ليالي الإقامة","مدة الإقامة وتعافي كوفيد"),
           ("🔮","توقعات الطلب","Prophet ML · 2025–2026"),
           ("🎯","تقسيم السياح","K-Means · عالي/متوسط/اقتصادي"),
           ("🌱","الأثر الكربوني","مؤشر CO₂ واستدامة ESG")],
    mt="التعلم الآلي", mh="3 نماذج ML جاهزة للإنتاج",
    ms="مدرّبة على 10 سنوات من البيانات السعودية الرسمية",
    ml=[("🔮","Prophet","توقع الطلب",
         "توقعات 24 شهرًا مع فترات الثقة العليا والدنيا","teal"),
        ("🎯","K-Means","تقسيم السياح",
         "3 شرائح قيمة · معامل Silhouette: 0.630","orange"),
        ("💰","Gradient Boosting","توقع الإنفاق",
         "R² = 0.986 · MAE: 184 ريال/رحلة","blue")],
    it="الاستنتاجات", ih="أبرز الاكتشافات",
    ins=[("🏖️","الترفيه تجاوز الديني كأول غرض في 2024 — إنجاز رؤية 2030 ✅","teal"),
         ("⏰","متوسط إقامة الوافد: 8.6 → 19.2 ليلة (2021→2024) · +123%","orange"),
         ("💰","الوافدون ينفقون 4 أضعاف المحليين (5,622 مقابل 1,336 ريال)","blue"),
         ("🚀","رقم قياسي 2024: 115.9M سائح · تعافي +150% من أدنى كوفيد","teal_act")],
    data="داتا السعودية · وزارة الاقتصاد والتخطيط · 2015–2024",
    copy="© 2025 ذكاء السياحة السعودية · م. جودة عماد · جميع الحقوق محفوظة",
    lng="EN", thm="☀️" if THEME=="dark" else "🌙",
),
}

# helper: color key → hex
def clr(key): return C.get(key, C["teal"])

# ════════════════════════════════════════════════════════════════════
# INJECT CSS
# ════════════════════════════════════════════════════════════════════
st.markdown(_load_css(),           unsafe_allow_html=True)
st.markdown(_patch(THEME, LANG),   unsafe_allow_html=True)

t        = TR[LANG]
logo_b64 = _b64("assets/logo.jpg")
hero_b64 = _b64("assets/hero.jpg")
logo_src = f"data:image/jpeg;base64,{logo_b64}" if logo_b64 else ""
hero_bg  = (f"url('data:image/jpeg;base64,{hero_b64}')"
            if hero_b64 else f"linear-gradient(135deg,{C['navbar']},{C['bg']})")
logo_tag = (f"<img src='{logo_src}' style='height:40px;border-radius:6px;'/>"
            if logo_src else "<span style='font-size:1.8rem;'>🇸🇦</span>")

# ════════════════════════════════════════════════════════════════════
# TOPBAR
# ════════════════════════════════════════════════════════════════════
c1, _, c2, c3 = st.columns([5, 4, 0.55, 0.65])
with c1:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;padding:12px 0 10px;">
      {logo_tag}
      <div>
        <div style="font-size:.92rem;font-weight:700;color:{C['white']};">
          {t['name']}
        </div>
        <div style="font-size:.6rem;color:{C['teal']};font-weight:600;
             letter-spacing:1.4px;text-transform:uppercase;">
          {t['sub']}
        </div>
      </div>
    </div>""", unsafe_allow_html=True)
with c2:
    if st.button(t["thm"], use_container_width=True, key="k_thm"):
        st.session_state.theme = "light" if THEME=="dark" else "dark"
        st.rerun()
with c3:
    if st.button(t["lng"], use_container_width=True, key="k_lng"):
        st.session_state.lang = "AR" if LANG=="EN" else "EN"
        st.rerun()

st.markdown(f"<div style='height:1px;background:{C['border']};'></div>",
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# HERO
# ════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="position:relative;aspect-ratio:16/6;width:100%;overflow:hidden;
            background-image:{hero_bg};background-size:cover;background-position:center;">
  <div style="position:absolute;inset:0;
    background:linear-gradient(105deg,{C['navbar']}F5 0%,{C['dark_bg']}BB 40%,transparent 100%);">
  </div>
  <div style="position:relative;z-index:2;padding:5% 5%;max-width:54%;
              height:100%;display:flex;flex-direction:column;justify-content:center;">
    <div style="display:inline-block;background:{C['teal']}18;
         border:1px solid {C['teal']}66;color:{C['teal']};
         font-size:.6rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
         padding:5px 14px;border-radius:4px;margin-bottom:18px;">
      {t['pill']}
    </div>
    <div style="font-size:clamp(1.55rem,3vw,2.6rem);font-weight:700;
         color:{C['white']};line-height:1.1;margin-bottom:2px;">
      {t['h1']}
    </div>
    <div style="font-size:clamp(1.55rem,3vw,2.6rem);font-weight:700;
         color:{C['teal']};line-height:1.1;margin-bottom:16px;">
      {t['h2']}
    </div>
    <p style="font-size:clamp(.75rem,1.1vw,.88rem);color:{C['grey']};
         line-height:1.7;margin-bottom:26px;max-width:480px;">
      {t['hs']}
    </p>
    <a href="#" style="display:inline-block;background:{C['teal']};
         color:{C['navbar']}!important;font-size:.85rem;font-weight:700;
         padding:11px 26px;border-radius:6px;text-decoration:none;
         width:fit-content;box-shadow:0 4px 20px {C['teal']}44;">
      {t['hb']}
    </a>
  </div>
</div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# STATS STRIP
# ════════════════════════════════════════════════════════════════════
cells = ""
for i, (val, lbl, color_key) in enumerate(t["stats"]):
    br = f"border-right:1px solid {C['border']};" if i < 3 else ""
    cells += f"""
    <div style="padding:26px 24px;{br}">
      <div style="font-size:1.8rem;font-weight:700;color:{clr(color_key)};
           font-family:'IBM Plex Mono',monospace;">{val}</div>
      <div style="font-size:.66rem;color:{C['grey']};text-transform:uppercase;
           letter-spacing:.9px;font-weight:500;margin-top:5px;">{lbl}</div>
    </div>"""

st.markdown(f"""
<div style="background:{C['sec_bg']};
     border-top:1px solid {C['border']};border-bottom:1px solid {C['border']};
     display:grid;grid-template-columns:repeat(4,1fr);">
  {cells}
</div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# PAGES  — 8 cards
# ════════════════════════════════════════════════════════════════════
page_cards = "".join(f"""
  <div style="background:{C['dark_bg']};border:1px solid {C['border']};
       border-radius:8px;padding:20px 18px;
       transition:border-color .25s,transform .25s,box-shadow .25s;
       position:relative;overflow:hidden;">
    <div style="position:absolute;top:0;left:0;right:0;height:2px;
         background:{C['teal']};transform:scaleX(0);transform-origin:left;
         transition:transform .3s;" class="_hover_bar"></div>
    <div style="font-size:1.5rem;margin-bottom:10px;">{ico}</div>
    <div style="font-size:.87rem;font-weight:600;color:{C['white']};
         margin-bottom:5px;">{title}</div>
    <div style="font-size:.73rem;color:{C['grey']};line-height:1.5;">{desc}</div>
  </div>""" for ico, title, desc in t["pages"])

st.markdown(f"""
<div style="padding:52px 40px;">
  <div style="margin-bottom:28px;">
    <div style="display:inline-block;background:{C['teal']}18;
         border:1px solid {C['teal']}55;color:{C['teal']};font-size:.6rem;
         font-weight:700;letter-spacing:2px;text-transform:uppercase;
         padding:4px 12px;border-radius:4px;margin-bottom:10px;">
      {t['pt']}
    </div>
    <div style="font-size:1.45rem;font-weight:700;
         color:{C['white']};margin-bottom:6px;">{t['ph']}</div>
    <div style="font-size:.82rem;color:{C['grey']};">{t['ps']}</div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;">
    {page_cards}
  </div>
</div>""", unsafe_allow_html=True)

st.markdown(f"<div style='height:1px;background:{C['border']};margin:0 40px;'></div>",
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# ML MODELS — 3 cards
# ════════════════════════════════════════════════════════════════════
ml_cards = "".join(f"""
  <div style="background:{C['dark_bg']};border:1px solid {C['border']};
       border-radius:8px;padding:26px 22px;position:relative;overflow:hidden;">
    <div style="position:absolute;top:0;left:0;right:0;height:3px;
         background:{clr(color_key)};"></div>
    <div style="font-size:1.5rem;margin-bottom:14px;">{ico}</div>
    <div style="font-size:1rem;font-weight:700;color:{C['white']};
         font-family:'IBM Plex Mono',monospace;margin-bottom:4px;">{name}</div>
    <div style="font-size:.68rem;font-weight:700;text-transform:uppercase;
         letter-spacing:1.2px;color:{clr(color_key)};margin-bottom:12px;">{mtype}</div>
    <div style="font-size:.8rem;color:{C['grey']};line-height:1.6;">{desc}</div>
  </div>""" for ico, name, mtype, desc, color_key in t["ml"])

st.markdown(f"""
<div style="padding:52px 40px;background:{C['sec_bg']};
     border-top:1px solid {C['border']};border-bottom:1px solid {C['border']};">
  <div style="margin-bottom:28px;">
    <div style="display:inline-block;background:{C['teal']}18;
         border:1px solid {C['teal']}55;color:{C['teal']};font-size:.6rem;
         font-weight:700;letter-spacing:2px;text-transform:uppercase;
         padding:4px 12px;border-radius:4px;margin-bottom:10px;">
      {t['mt']}
    </div>
    <div style="font-size:1.45rem;font-weight:700;
         color:{C['white']};margin-bottom:6px;">{t['mh']}</div>
    <div style="font-size:.82rem;color:{C['grey']};">{t['ms']}</div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;">
    {ml_cards}
  </div>
</div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# INSIGHTS — 4 cards
# ════════════════════════════════════════════════════════════════════
ins_cards = "".join(f"""
  <div style="background:{C['dark_bg']};border:1px solid {C['border']};
       border-left:3px solid {clr(color_key)};border-radius:8px;
       padding:16px 18px;display:flex;align-items:flex-start;gap:12px;">
    <div style="font-size:1.2rem;flex-shrink:0;margin-top:1px;">{ico}</div>
    <div style="font-size:.83rem;color:{C['white']};line-height:1.6;">{txt}</div>
  </div>""" for ico, txt, color_key in t["ins"])

st.markdown(f"""
<div style="padding:52px 40px;">
  <div style="margin-bottom:28px;">
    <div style="display:inline-block;background:{C['teal']}18;
         border:1px solid {C['teal']}55;color:{C['teal']};font-size:.6rem;
         font-weight:700;letter-spacing:2px;text-transform:uppercase;
         padding:4px 12px;border-radius:4px;margin-bottom:10px;">
      {t['it']}
    </div>
    <div style="font-size:1.45rem;font-weight:700;
         color:{C['white']};margin-bottom:6px;">{t['ih']}</div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;">
    {ins_cards}
  </div>
</div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="background:{C['navbar']};border-top:2px solid {C['teal']};
     padding:24px 40px;display:flex;justify-content:space-between;
     align-items:center;flex-wrap:wrap;gap:14px;">
  <div style="display:flex;align-items:center;gap:14px;">
    {logo_tag}
    <div>
      <div style="font-size:.86rem;font-weight:700;color:{C['teal']};">
        {t['name']}
      </div>
      <div style="font-size:.67rem;color:{C['foot_grey']};margin-top:2px;">
        {t['copy']}
      </div>
      <div style="font-size:.64rem;color:{C['grey']};margin-top:2px;">
        📦 {t['data']}
      </div>
    </div>
  </div>
  <div style="display:flex;gap:22px;align-items:center;">
    <a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence"
       target="_blank"
       style="font-size:.76rem;color:{C['foot_grey']};text-decoration:none;font-weight:500;">
      🐙 GitHub
    </a>
    <a href="https://www.linkedin.com/in/goda-emad/"
       target="_blank"
       style="font-size:.76rem;color:{C['foot_grey']};text-decoration:none;font-weight:500;">
      💼 LinkedIn
    </a>
    <a href="https://datasaudi.sa"
       target="_blank"
       style="font-size:.76rem;color:{C['teal']};text-decoration:none;font-weight:600;">
      📊 DataSaudi
    </a>
  </div>
</div>""", unsafe_allow_html=True)
