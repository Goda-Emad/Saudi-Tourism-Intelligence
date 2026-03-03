import streamlit as st
import base64
import os

st.set_page_config(
    page_title="Saudi Tourism Intelligence",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── session state ──────────────────────────────────────
for k, v in [("lang","EN"), ("theme","dark")]:
    if k not in st.session_state:
        st.session_state[k] = v

lang  = st.session_state.lang
theme = st.session_state.theme

# ══════════════════════════════════════════════════════════
# CACHED HELPERS — runs ONCE, never re-runs on rerun
# ══════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def _read_bytes(rel: str) -> bytes:
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, rel), "rb") as f:
        return f.read()

@st.cache_data(show_spinner=False)
def _b64(rel: str) -> str:
    try:    return base64.b64encode(_read_bytes(rel)).decode()
    except: return ""

@st.cache_data(show_spinner=False)
def _load_css() -> str:
    """Load style.css once — injected as-is, zero rebuild."""
    try:    return f"<style>{_read_bytes('assets/style.css').decode()}</style>"
    except: return ""

@st.cache_data(show_spinner=False)
def _theme_patch(theme: str, lang: str) -> str:
    """Tiny patch on top of style.css for theme + direction."""
    bg   = "#0D1B2A" if theme == "dark" else "#F4F7FB"
    sbg  = "#132336" if theme == "dark" else "#FFFFFF"
    dir_ = "rtl"     if lang  == "AR"   else "ltr"
    ff   = "Tajawal" if lang  == "AR"   else "Sora"
    txt  = "#F0F4F8" if theme == "dark" else "#1A2B3C"
    return f"""<style>
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{{
  background:{bg}!important;direction:{dir_};
  font-family:'{ff}',sans-serif;color:{txt}!important;}}
[data-testid="stSidebar"]{{background:{sbg}!important;}}
[data-testid="stHeader"],[data-testid="stToolbar"],footer{{display:none!important;}}
.block-container{{padding:0!important;max-width:100%!important;}}
</style>"""

# ══════════════════════════════════════════════════════════
# TRANSLATIONS
# ══════════════════════════════════════════════════════════
TR = {
"EN": dict(
  name="Saudi Tourism Intelligence", sub="AI ANALYTICS PLATFORM",
  pill="🇸🇦  OFFICIAL DATA · MINISTRY OF ECONOMY & PLANNING",
  h1="Saudi Tourism", h2="Intelligence",
  hs="AI-powered analytics built on 10 years of official government data. Forecasting · Segmentation · Sustainability — all in one platform.",
  hb="Explore Dashboard →",
  s1v="115.8M", s1l="Tourists 2024",
  s2v="1.10B",  s2l="Overnight Stays",
  s3v="SAR 5,622",  s3l="Avg Spend",
  s4v="0.986",  s4l="ML Accuracy R²",
  pt="PLATFORM", ph="8 Interactive Pages",
  ps="Comprehensive analysis covering every dimension of Saudi tourism",
  mt="MACHINE LEARNING", mh="3 Production ML Models",
  ms="Trained on 10 years of official Saudi government data",
  it="INSIGHTS", ih="Key Discoveries",
  f=[("🏠","Executive Overview","KPIs, trends & insights at a glance"),
     ("📈","Tourist Trends","Annual & monthly patterns 2015–2024"),
     ("📅","Seasonality","Peak months, Ramadan & summer effects"),
     ("💰","Spending Analysis","Per trip, per night, by purpose"),
     ("🏨","Overnight Stays","Length of stay & COVID recovery"),
     ("🔮","Demand Forecasting","Prophet ML · 2025–2026 predictions"),
     ("🎯","Segmentation","K-Means · High / Mid / Budget"),
     ("🌱","Carbon Impact","CO₂ index & ESG sustainability")],
  ml=[("🔮","Prophet","Demand Forecasting",
       "24-month predictions · upper/lower confidence bounds","#00C9B1"),
      ("🎯","K-Means","Tourist Segmentation",
       "3 value segments · Silhouette Score 0.630","#F0A500"),
      ("💰","Gradient Boosting","Spending Prediction",
       "R² = 0.986 · MAE: SAR 184 per trip","#3A86FF")],
  ins=[("🏖️","Leisure overtook Religious as #1 purpose in 2024 — Vision 2030 milestone ✅","#00C9B1"),
       ("⏰","Inbound avg stay: 8.6 → 19.2 nights (2021→2024) · +123% growth","#F0A500"),
       ("💰","Inbound spend 4× more than Domestic (SAR 5,622 vs SAR 1,336)","#3A86FF"),
       ("🚀","2024 record: 115.9M tourists · +150% recovery from COVID low","#00C9B1")],
  lng="AR", thm_d="🌙 Dark", thm_l="☀️ Light",
  fc="© 2025 Saudi Tourism Intelligence · Eng. Goda Emad · All rights reserved",
  data="DataSaudi · Ministry of Economy & Planning · 2015–2024",
),
"AR": dict(
  name="ذكاء السياحة السعودية", sub="منصة تحليلات الذكاء الاصطناعي",
  pill="🇸🇦  بيانات رسمية · وزارة الاقتصاد والتخطيط",
  h1="ذكاء السياحة", h2="السعودية",
  hs="منصة تحليلات على 10 سنوات من البيانات الرسمية. توقعات · تقسيم · استدامة — كل شيء في منصة واحدة.",
  hb="← استكشف لوحة التحكم",
  s1v="115.8M", s1l="سائح 2024",
  s2v="1.10B",  s2l="ليالي الإقامة",
  s3v="٥،٦٢٢ ر",  s3l="متوسط الإنفاق",
  s4v="0.986",  s4l="دقة النموذج R²",
  pt="المنصة", ph="8 صفحات تفاعلية",
  ps="تحليل شامل لكل أبعاد السياحة السعودية",
  mt="التعلم الآلي", mh="3 نماذج ML جاهزة للإنتاج",
  ms="مدرّبة على 10 سنوات من البيانات السعودية الرسمية",
  it="الاستنتاجات", ih="أبرز الاكتشافات",
  f=[("🏠","النظرة التنفيذية","مؤشرات الأداء والاتجاهات"),
     ("📈","اتجاهات السياحة","الأنماط السنوية والشهرية 2015–2024"),
     ("📅","الموسمية","ذروة الأشهر وتأثير رمضان والصيف"),
     ("💰","تحليل الإنفاق","لكل رحلة، لكل ليلة، حسب الغرض"),
     ("🏨","ليالي الإقامة","مدة الإقامة وتعافي كوفيد"),
     ("🔮","توقعات الطلب","Prophet ML · 2025–2026"),
     ("🎯","تقسيم السياح","K-Means · عالي/متوسط/اقتصادي"),
     ("🌱","الأثر الكربوني","مؤشر CO₂ واستدامة ESG")],
  ml=[("🔮","Prophet","توقع الطلب",
       "توقعات 24 شهرًا مع فترات الثقة","#00C9B1"),
      ("🎯","K-Means","تقسيم السياح",
       "3 شرائح · معامل Silhouette 0.630","#F0A500"),
      ("💰","Gradient Boosting","توقع الإنفاق",
       "R² = 0.986 · MAE: ١٨٤ ريال/رحلة","#3A86FF")],
  ins=[("🏖️","الترفيه تجاوز الديني كأول غرض في 2024 — إنجاز رؤية 2030 ✅","#00C9B1"),
       ("⏰","متوسط إقامة الوافد: ٨.٦ ← ١٩.٢ ليلة (٢٠٢١←٢٠٢٤) · +١٢٣٪","#F0A500"),
       ("💰","الوافدون ينفقون ٤ أضعاف المحليين (٥،٦٢٢ مقابل ١،٣٣٦ ريال)","#3A86FF"),
       ("🚀","رقم قياسي ٢٠٢٤: ١١٥.٩م سائح · تعافي +١٥٠٪ من أدنى كوفيد","#00C9B1")],
  lng="EN", thm_d="🌙 ليلي", thm_l="☀️ نهاري",
  fc="© ٢٠٢٥ ذكاء السياحة السعودية · م. جودة عماد · جميع الحقوق محفوظة",
  data="داتا السعودية · وزارة الاقتصاد والتخطيط · ٢٠١٥–٢٠٢٤",
)}

# ══════════════════════════════════════════════════════════
# INJECT CSS (all cached — zero recompute on rerun)
# ══════════════════════════════════════════════════════════
st.markdown(_load_css(),              unsafe_allow_html=True)
st.markdown(_theme_patch(theme,lang), unsafe_allow_html=True)

t = TR[lang]

# ── load images (cached bytes → b64 → src) ────────────
logo_b64 = _b64("assets/logo.png")
hero_b64 = _b64("assets/hero.png")
logo_src = f"data:image/png;base64,{logo_b64}" if logo_b64 else ""
hero_bg  = (f"url('data:image/png;base64,{hero_b64}')"
            if hero_b64 else "linear-gradient(135deg,#1B5E20,#0D1B2A)")
logo_img = (f"<img src='{logo_src}' style='height:45px;border-radius:8px;'/>"
            if logo_src else "<span style='font-size:2rem;'>🇸🇦</span>")

# ══════════════════════════════════════════════════════════
# TOPBAR
# ══════════════════════════════════════════════════════════
ca, _, cb, cc = st.columns([5, 4, 0.6, 0.8])
with ca:
    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:14px;padding:12px 0 10px;'>
      {logo_img}
      <div>
        <div style='font-size:.95rem;font-weight:700;color:{'#F0F4F8' if theme=='dark' else '#1A2B3C'};
             line-height:1.2;'>{t['name']}</div>
        <div style='font-size:.6rem;color:#00C9B1;font-weight:600;
             letter-spacing:1.4px;text-transform:uppercase;'>{t['sub']}</div>
      </div>
    </div>""", unsafe_allow_html=True)
with cb:
    if st.button(t["thm_l"] if theme=="dark" else t["thm_d"],
                 use_container_width=True, key="thm"):
        st.session_state.theme = "light" if theme=="dark" else "dark"
        st.rerun()
with cc:
    if st.button(t["lng"], use_container_width=True, key="lng"):
        st.session_state.lang = "AR" if lang=="EN" else "EN"
        st.rerun()

st.markdown("<div style='height:1px;background:#2A3F55;'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div style='position:relative;aspect-ratio:16/5;width:100%;overflow:hidden;
            background-image:{hero_bg};background-size:cover;background-position:center;'>
  <div style='position:absolute;inset:0;
    background:linear-gradient(105deg,{'#0D1B2AF5' if theme=='dark' else '#F4F7FBF5'} 0%,{'#132336CC' if theme=='dark' else '#FFFFFFCC'} 38%,transparent 100%);'></div>
  <div style='position:relative;z-index:2;padding:4% 5%;max-width:55%;
              height:100%;display:flex;flex-direction:column;justify-content:center;'>
    <div style='display:inline-block;background:#1B5E2022;border:1px solid #00C9B166;
                color:#00C9B1;font-size:0.65rem;font-weight:700;padding:5px 14px;
                border-radius:20px;margin-bottom:18px;width:fit-content;'>
      {t['pill']}
    </div>
    <div style='font-size:clamp(1.6rem,3.2vw,2.8rem);font-weight:700;
         color:{'#F0F4F8' if theme=='dark' else '#1A2B3C'};line-height:1.1;margin-bottom:2px;'>
      {t['h1']}
    </div>
    <div style='font-size:clamp(1.6rem,3.2vw,2.8rem);font-weight:700;
         color:#00C9B1;line-height:1.1;margin-bottom:16px;'>
      {t['h2']}
    </div>
    <p style='font-size:clamp(.75rem,1.1vw,.9rem);color:#94A3B8;
         line-height:1.7;margin-bottom:26px;max-width:500px;'>
      {t['hs']}
    </p>
    <a href='#' style='display:inline-block;background:#00C9B1;
         color:{'#0D1B2A' if theme=='dark' else '#FFFFFF'}!important;font-size:.85rem;font-weight:700;
         padding:12px 28px;border-radius:30px;text-decoration:none;
         width:fit-content;box-shadow:0 4px 20px #00C9B166;'>
      {t['hb']}
    </a>
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# STATS STRIP
# ══════════════════════════════════════════════════════════
stats = [
    ("s1v","s1l","#00C9B1"),
    ("s2v","s2l","#00C9B1"),
    ("s3v","s3l","#F0A500"),
    ("s4v","s4l","#3A86FF")
]

cells = ""
for vk, lk, col in stats:
    cells += f"""
    <div style='padding:24px 20px;border-right:1px solid #2A3F55;'>
        <div style='font-size:1.8rem;font-weight:700;color:{col};
             font-family:IBM Plex Mono,monospace;'>{t[vk]}</div>
        <div style='font-size:.66rem;color:#94A3B8;text-transform:uppercase;
             letter-spacing:.9px;margin-top:5px;'>{t[lk]}</div>
    </div>"""

st.markdown(f"""
<div style='background:{'#132336' if theme=='dark' else '#EDF2F7'};
     border-top:1px solid #2A3F55;border-bottom:1px solid #2A3F55;
     display:grid;grid-template-columns:repeat(4,1fr);'>
  {cells}
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGES SECTION
# ══════════════════════════════════════════════════════════
page_cards = ""
for ico, title, desc in t["f"]:
    page_cards += f"""
    <div style='background:{'#132336' if theme=='dark' else '#FFFFFF'};
                border:1px solid #2A3F55;border-radius:12px;padding:20px 16px;
                transition:transform 0.2s;cursor:default;'>
        <div style='font-size:1.6rem;margin-bottom:12px;'>{ico}</div>
        <div style='font-size:.9rem;font-weight:700;color:{'#F0F4F8' if theme=='dark' else '#1A2B3C'};margin-bottom:6px;'>{title}</div>
        <div style='font-size:.75rem;color:#94A3B8;line-height:1.5;'>{desc}</div>
    </div>"""

st.markdown(f"""
<div style='padding:48px 40px;'>
  <div style='margin-bottom:28px;'>
    <div style='display:inline-block;background:#1B5E2022;border:1px solid #00C9B166;
                color:#00C9B1;font-size:0.65rem;font-weight:700;padding:5px 14px;
                border-radius:20px;margin-bottom:10px;'>{t['pt']}</div>
    <div style='font-size:1.5rem;font-weight:700;color:{'#F0F4F8' if theme=='dark' else '#1A2B3C'};margin-bottom:6px;'>{t['ph']}</div>
    <div style='font-size:.82rem;color:#94A3B8;'>{t['ps']}</div>
  </div>
  <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:16px;'>{page_cards}</div>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='height:1px;background:#2A3F55;margin:0 40px;'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ML SECTION
# ══════════════════════════════════════════════════════════
ml_cards = ""
for ico, name, mtype, desc, color in t["ml"]:
    ml_cards += f"""
    <div style='background:{'#132336' if theme=='dark' else '#FFFFFF'};
                border:1px solid #2A3F55;border-radius:16px;padding:24px 20px;
                position:relative;overflow:hidden;'>
        <div style='position:absolute;top:0;left:0;right:0;height:3px;background:{color};'></div>
        <div style='font-size:1.5rem;margin-bottom:14px;'>{ico}</div>
        <div style='font-size:1.1rem;font-weight:700;color:{'#F0F4F8' if theme=='dark' else '#1A2B3C'};margin-bottom:3px;'>{name}</div>
        <div style='font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;color:{color};'>{mtype}</div>
        <div style='font-size:.8rem;color:#94A3B8;line-height:1.6;'>{desc}</div>
    </div>"""

st.markdown(f"""
<div style='padding:48px 40px;background:{'#132336' if theme=='dark' else '#EDF2F7'};
     border-top:1px solid #2A3F55;border-bottom:1px solid #2A3F55;'>
  <div style='margin-bottom:28px;'>
    <div style='display:inline-block;background:#1B5E2022;border:1px solid #00C9B166;
                color:#00C9B1;font-size:0.65rem;font-weight:700;padding:5px 14px;
                border-radius:20px;margin-bottom:10px;'>{t['mt']}</div>
    <div style='font-size:1.5rem;font-weight:700;color:{'#F0F4F8' if theme=='dark' else '#1A2B3C'};margin-bottom:6px;'>{t['mh']}</div>
    <div style='font-size:.82rem;color:#94A3B8;'>{t['ms']}</div>
  </div>
  <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:20px;'>{ml_cards}</div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# INSIGHTS
# ══════════════════════════════════════════════════════════
ins_cards = ""
for ico, txt, color in t["ins"]:
    ins_cards += f"""
    <div style='background:{'#132336' if theme=='dark' else '#FFFFFF'};
                border:1px solid #2A3F55;border-radius:12px;padding:16px 18px;
                display:flex;align-items:flex-start;gap:12px;
                border-left:3px solid {color};'>
        <div style='font-size:1.2rem;'>{ico}</div>
        <div style='font-size:.83rem;color:{'#F0F4F8' if theme=='dark' else '#1A2B3C'};line-height:1.55;'>{txt}</div>
    </div>"""

st.markdown(f"""
<div style='padding:48px 40px;'>
  <div style='margin-bottom:28px;'>
    <div style='display:inline-block;background:#1B5E2022;border:1px solid #00C9B166;
                color:#00C9B1;font-size:0.65rem;font-weight:700;padding:5px 14px;
                border-radius:20px;margin-bottom:10px;'>{t['it']}</div>
    <div style='font-size:1.5rem;font-weight:700;color:{'#F0F4F8' if theme=='dark' else '#1A2B3C'};margin-bottom:6px;'>{t['ih']}</div>
  </div>
  <div style='display:grid;grid-template-columns:repeat(2,1fr);gap:16px;'>{ins_cards}</div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div style='background:{'#132336' if theme=='dark' else '#EDF2F7'};
     border-top:2px solid #00C9B1;
     padding:24px 40px;
     display:flex;justify-content:space-between;
     align-items:center;flex-wrap:wrap;gap:14px;'>
  <div style='display:flex;align-items:center;gap:14px;'>
    {logo_img}
    <div>
      <div style='font-size:.86rem;font-weight:700;
           color:#00C9B1;'>{t['name']}</div>
      <div style='font-size:.67rem;color:#94A3B8;margin-top:2px;'>
        {t['fc']}
      </div>
      <div style='font-size:.64rem;color:#94A3B8;margin-top:2px;'>
        📦 {t['data']}
      </div>
    </div>
  </div>
  <div style='display:flex;gap:20px;align-items:center;'>
    <a href='https://github.com/Goda-Emad/Saudi-Tourism-Intelligence'
       target='_blank'
       style='font-size:.76rem;color:#94A3B8;
              text-decoration:none;'>🐙 GitHub</a>
    <a href='https://www.linkedin.com/in/goda-emad/'
       target='_blank'
       style='font-size:.76rem;color:#94A3B8;
              text-decoration:none;'>💼 LinkedIn</a>
    <a href='https://datasaudi.sa'
       target='_blank'
       style='font-size:.76rem;color:#00C9B1;
              text-decoration:none;font-weight:600;'>📊 DataSaudi</a>
  </div>
</div>""", unsafe_allow_html=True)
