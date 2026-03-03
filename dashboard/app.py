import streamlit as st
import base64, os

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
    bg   = "#1A1E1F" if theme == "dark" else "#F4F9F8"
    sbg  = "#0D1414" if theme == "dark" else "#FFFFFF"
    dir_ = "rtl"     if lang  == "AR"   else "ltr"
    ff   = "Tajawal" if lang  == "AR"   else "IBM Plex Sans"
    txt  = "#F4F9F8" if theme == "dark" else "#0D1414"
    return f"""<style>
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{{
  background:{bg}!important;direction:{dir_};
  font-family:'{ff}',sans-serif;color:{txt};}}
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
  s3v="5,622",  s3l="Avg Spend (SAR)",
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
       "24-month predictions · upper/lower confidence bounds","var(--ds-teal)"),
      ("🎯","K-Means","Tourist Segmentation",
       "3 value segments · Silhouette Score 0.630","var(--ds-orange)"),
      ("💰","Gradient Boosting","Spending Prediction",
       "R² = 0.986 · MAE: SAR 184 per trip","#6B9FD4")],
  ins=[("🏖️","Leisure overtook Religious as #1 purpose in 2024 — Vision 2030 milestone ✅","var(--ds-teal)"),
       ("⏰","Inbound avg stay: 8.6 → 19.2 nights (2021→2024) · +123% growth","var(--ds-orange)"),
       ("💰","Inbound spend 4× more than Domestic (SAR 5,622 vs SAR 1,336)","#6B9FD4"),
       ("🚀","2024 record: 115.9M tourists · +150% recovery from COVID low","var(--ds-teal-active)")],
  lng="AR", thm_d="🌙", thm_l="☀️",
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
  s3v="5,622",  s3l="متوسط الإنفاق (ريال)",
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
       "توقعات 24 شهرًا مع فترات الثقة العليا والدنيا","var(--ds-teal)"),
      ("🎯","K-Means","تقسيم السياح",
       "3 شرائح · معامل Silhouette 0.630","var(--ds-orange)"),
      ("💰","Gradient Boosting","توقع الإنفاق",
       "R² = 0.986 · MAE: 184 ريال/رحلة","#6B9FD4")],
  ins=[("🏖️","الترفيه تجاوز الديني كأول غرض في 2024 — إنجاز رؤية 2030 ✅","var(--ds-teal)"),
       ("⏰","متوسط إقامة الوافد: 8.6 → 19.2 ليلة (2021→2024) · +123%","var(--ds-orange)"),
       ("💰","الوافدون ينفقون 4 أضعاف المحليين (5,622 مقابل 1,336 ريال)","#6B9FD4"),
       ("🚀","رقم قياسي 2024: 115.9M سائح · تعافي +150% من أدنى كوفيد","var(--ds-teal-active)")],
  lng="EN", thm_d="🌙", thm_l="☀️",
  fc="© 2025 ذكاء السياحة السعودية · م. جودة عماد · جميع الحقوق محفوظة",
  data="داتا السعودية · وزارة الاقتصاد والتخطيط · 2015–2024",
)}

# ══════════════════════════════════════════════════════════
# INJECT CSS (all cached — zero recompute on rerun)
# ══════════════════════════════════════════════════════════
st.markdown(_load_css(),              unsafe_allow_html=True)
st.markdown(_theme_patch(theme,lang), unsafe_allow_html=True)

t = TR[lang]

# ── load images (cached bytes → b64 → src) ────────────
logo_b64 = _b64("assets/logo.jpg")
hero_b64 = _b64("assets/hero.jpg")

logo_src = f"data:image/jpeg;base64,{logo_b64}" if logo_b64 else ""
hero_bg  = (f"url('data:image/jpeg;base64,{hero_b64}')"
            if hero_b64 else "linear-gradient(135deg,#172025,#0D1414)")
logo_img = (f"<img src='{logo_src}' style='height:40px;border-radius:6px;'/>"
            if logo_src else "<span style='font-size:1.8rem;'>🇸🇦</span>")

# ══════════════════════════════════════════════════════════
# TOPBAR
# ══════════════════════════════════════════════════════════
ca, _, cb, cc = st.columns([5, 4, 0.55, 0.7])
with ca:
    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:12px;padding:12px 0 10px;'>
      {logo_img}
      <div>
        <div style='font-size:.92rem;font-weight:700;color:var(--ds-text,#F4F9F8);
             line-height:1.2;'>{t['name']}</div>
        <div style='font-size:.6rem;color:var(--ds-teal);font-weight:600;
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

# navbar border
st.markdown("<div style='height:1px;background:var(--ds-border,#2A3235);'></div>",
            unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div style='position:relative;aspect-ratio:16/6;width:100%;overflow:hidden;
            background-image:{hero_bg};background-size:cover;background-position:center;'>
  <div style='position:absolute;inset:0;
    background:linear-gradient(105deg,#0D1414F5 0%,#172025CC 38%,transparent 100%);'></div>
  <div style='position:relative;z-index:2;padding:5% 5%;max-width:55%;
              height:100%;display:flex;flex-direction:column;justify-content:center;'>
    <div class="ds-badge" style="margin-bottom:18px;">{t['pill']}</div>
    <div style='font-size:clamp(1.55rem,3vw,2.6rem);font-weight:700;
         color:var(--ds-text,#F4F9F8);line-height:1.1;margin-bottom:2px;'>
      {t['h1']}
    </div>
    <div style='font-size:clamp(1.55rem,3vw,2.6rem);font-weight:700;
         color:var(--ds-teal);line-height:1.1;margin-bottom:16px;'>
      {t['h2']}
    </div>
    <p style='font-size:clamp(.75rem,1.1vw,.88rem);color:var(--ds-grey);
         line-height:1.7;margin-bottom:26px;max-width:480px;'>
      {t['hs']}
    </p>
    <a href='#' style='display:inline-block;background:var(--ds-teal);
         color:#0D1414!important;font-size:.85rem;font-weight:700;
         padding:11px 26px;border-radius:6px;text-decoration:none;
         width:fit-content;box-shadow:0 4px 20px rgba(23,177,155,.4);'>
      {t['hb']}
    </a>
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# STATS STRIP
# ══════════════════════════════════════════════════════════
stats = [("s1v","s1l","var(--ds-teal)"),("s2v","s2l","var(--ds-teal)"),
         ("s3v","s3l","var(--ds-orange)"),("s4v","s4l","var(--ds-orange)")]
cells = "".join(f"""
  <div style='padding:26px 24px;border-right:1px solid var(--ds-border,#2A3235);'>
    <div style='font-size:1.8rem;font-weight:700;color:{col};
         font-family:var(--ds-font-mono,"IBM Plex Mono"),monospace;'>{t[vk]}</div>
    <div style='font-size:.66rem;color:var(--ds-grey);text-transform:uppercase;
         letter-spacing:.9px;font-weight:500;margin-top:5px;'>{t[lk]}</div>
  </div>""" for vk,lk,col in stats)
# remove last border-right
cells = cells.rstrip()

st.markdown(f"""
<div style='background:var(--ds-section-bg,#161B1C);
     border-top:1px solid var(--ds-border);
     border-bottom:1px solid var(--ds-border);
     display:grid;grid-template-columns:repeat(4,1fr);'>
  {cells}
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGES SECTION
# ══════════════════════════════════════════════════════════
page_cards = "".join(f"""
  <div class='ds-card'>
    <div class='ds-card-ico'>{ico}</div>
    <div class='ds-card-title'>{title}</div>
    <div class='ds-card-desc'>{desc}</div>
  </div>""" for ico,title,desc in t["f"])

st.markdown(f"""
<div style='padding:52px 40px;'>
  <div style='margin-bottom:28px;'>
    <div class='ds-badge' style='margin-bottom:10px;'>{t['pt']}</div>
    <div style='font-size:1.45rem;font-weight:700;
         color:var(--ds-text,#F4F9F8);margin-bottom:6px;'>{t['ph']}</div>
    <div style='font-size:.82rem;color:var(--ds-grey);'>{t['ps']}</div>
  </div>
  <div class='ds-card-grid cols-4'>{page_cards}</div>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='height:1px;background:var(--ds-border);margin:0 40px;'></div>",
            unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ML SECTION
# ══════════════════════════════════════════════════════════
ml_cards = "".join(f"""
  <div class='ds-ml-card'>
    <div class='ds-ml-accent' style='background:{color};'></div>
    <div style='font-size:1.5rem;margin-bottom:14px;'>{ico}</div>
    <div class='ds-ml-name'>{name}</div>
    <div class='ds-ml-type' style='color:{color};'>{mtype}</div>
    <div class='ds-ml-desc'>{desc}</div>
  </div>""" for ico,name,mtype,desc,color in t["ml"])

st.markdown(f"""
<div style='padding:52px 40px;background:var(--ds-section-bg,#161B1C);
     border-top:1px solid var(--ds-border);
     border-bottom:1px solid var(--ds-border);'>
  <div style='margin-bottom:28px;'>
    <div class='ds-badge' style='margin-bottom:10px;'>{t['mt']}</div>
    <div style='font-size:1.45rem;font-weight:700;
         color:var(--ds-text,#F4F9F8);margin-bottom:6px;'>{t['mh']}</div>
    <div style='font-size:.82rem;color:var(--ds-grey);'>{t['ms']}</div>
  </div>
  <div class='ds-card-grid cols-3'>{ml_cards}</div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# INSIGHTS
# ══════════════════════════════════════════════════════════
ins_cards = "".join(f"""
  <div class='ds-insight' style='border-left-color:{color};'>
    <div class='ds-insight-ico'>{ico}</div>
    <div class='ds-insight-txt'>{txt}</div>
  </div>""" for ico,txt,color in t["ins"])

st.markdown(f"""
<div style='padding:52px 40px;'>
  <div style='margin-bottom:28px;'>
    <div class='ds-badge' style='margin-bottom:10px;'>{t['it']}</div>
    <div style='font-size:1.45rem;font-weight:700;
         color:var(--ds-text,#F4F9F8);margin-bottom:6px;'>{t['ih']}</div>
  </div>
  <div class='ds-card-grid cols-2'>{ins_cards}</div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div style='background:var(--ds-navbar-bg,#0D1414);
     border-top:2px solid var(--ds-teal);
     padding:24px 40px;
     display:flex;justify-content:space-between;
     align-items:center;flex-wrap:wrap;gap:14px;'>
  <div style='display:flex;align-items:center;gap:14px;'>
    {logo_img}
    <div>
      <div style='font-size:.86rem;font-weight:700;
           color:var(--ds-teal);'>{t['name']}</div>
      <div style='font-size:.67rem;color:var(--ds-footer-text,#B5B8B7);margin-top:2px;'>
        {t['fc']}
      </div>
      <div style='font-size:.64rem;color:var(--ds-grey);margin-top:2px;'>
        📦 {t['data']}
      </div>
    </div>
  </div>
  <div style='display:flex;gap:20px;align-items:center;'>
    <a href='https://github.com/Goda-Emad/Saudi-Tourism-Intelligence'
       target='_blank'
       style='font-size:.76rem;color:var(--ds-footer-text);
              text-decoration:none;font-weight:500;'>🐙 GitHub</a>
    <a href='https://www.linkedin.com/in/goda-emad/'
       target='_blank'
       style='font-size:.76rem;color:var(--ds-footer-text);
              text-decoration:none;font-weight:500;'>💼 LinkedIn</a>
    <a href='https://datasaudi.sa'
       target='_blank'
       style='font-size:.76rem;color:var(--ds-teal);
              text-decoration:none;font-weight:600;'>📊 DataSaudi</a>
  </div>
</div>""", unsafe_allow_html=True)
