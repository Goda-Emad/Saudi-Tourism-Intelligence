import streamlit as st
import base64, os

st.set_page_config(
    page_title="Saudi Tourism Intelligence",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

for k, v in [("lang", "EN"), ("theme", "dark")]:
    if k not in st.session_state:
        st.session_state[k] = v

lang  = st.session_state.lang
theme = st.session_state.theme

# ══════════════════════════════════════════════════════
# DataSaudi Design System — exact CSS variables
# ══════════════════════════════════════════════════════
DS = {
    "dark": {
        "bg":          "#1A1E1F",   # --ds-background
        "section_bg":  "#161B1C",   # --ds-section-bg
        "dark_bg":     "#172025",   # --ds-dark-bg
        "navbar_bg":   "#0D1414",   # --ds-navbar-bg
        "teal":        "#17B19B",   # --ds-teal-primary
        "teal_active": "#149581",   # --ds-teal-active
        "teal_sec":    "#8BAFAA",   # --ds-teal-secondary
        "white":       "#F4F9F8",   # --ds-white
        "grey":        "#A1A6B7",   # --ds-grey-text
        "footer_txt":  "#B5B8B7",   # --ds-footer-text
        "blue":        "#365C8D",   # --ds-blue-primary
        "purple":      "#620E8B",   # --ds-purple-primary
        "orange":      "#F4D044",   # --ds-orange-primary
        "pink":        "#C50A5D",   # --ds-pink-primary
        "border":      "#2A3235",
        "glow":        "#17B19B1A",
    },
    "light": {
        "bg":          "#F4F9F8",
        "section_bg":  "#EAEFEE",
        "dark_bg":     "#DDE6E4",
        "navbar_bg":   "#FFFFFF",
        "teal":        "#17B19B",
        "teal_active": "#149581",
        "teal_sec":    "#4A8A82",
        "white":       "#0D1414",
        "grey":        "#4A5568",
        "footer_txt":  "#718096",
        "blue":        "#365C8D",
        "purple":      "#620E8B",
        "orange":      "#D4A800",
        "pink":        "#C50A5D",
        "border":      "#CBD5D3",
        "glow":        "#17B19B18",
    }
}

# ══════════════════════════════════════════════════════
# CACHED RESOURCES
# ══════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def _img(path: str) -> str:
    try:
        d = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(d, path), "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

@st.cache_data(show_spinner=False)
def _css(theme: str, lang: str) -> str:
    c   = DS[theme]
    ff  = "Tajawal" if lang == "AR" else "IBM Plex Sans"
    dir = "rtl"     if lang == "AR" else "ltr"
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Tajawal:wght@300;400;700;800&display=swap');

:root {{
  --ds-background:   {c['bg']};
  --ds-section-bg:   {c['section_bg']};
  --ds-dark-bg:      {c['dark_bg']};
  --ds-navbar-bg:    {c['navbar_bg']};
  --ds-teal-primary: {c['teal']};
  --ds-teal-active:  {c['teal_active']};
  --ds-teal-sec:     {c['teal_sec']};
  --ds-white:        {c['white']};
  --ds-grey:         {c['grey']};
  --ds-border:       {c['border']};
  --ds-glow:         {c['glow']};
  --ds-orange:       {c['orange']};
  --ds-blue:         {c['blue']};
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {{
  background: var(--ds-background) !important;
  font-family: '{ff}', sans-serif;
  direction: {dir};
  color: var(--ds-white);
}}

/* hide default streamlit chrome */
[data-testid="stHeader"],
[data-testid="stToolbar"],
footer {{ display: none !important; }}
[data-testid="stSidebar"] {{ display: none !important; }}
.block-container {{
  padding: 0 !important;
  max-width: 100% !important;
}}

/* ── NAVBAR ──────────────────────────────────────── */
.ds-nav {{
  position: sticky; top: 0; z-index: 100;
  background: var(--ds-navbar-bg);
  border-bottom: 1px solid var(--ds-border);
  padding: 0 40px;
  display: flex; align-items: center;
  justify-content: space-between;
  height: 64px;
  backdrop-filter: blur(12px);
}}
.ds-nav-brand {{ display: flex; align-items: center; gap: 12px; }}
.ds-nav-logo {{ height: 38px; border-radius: 6px; }}
.ds-nav-name {{
  font-size: .9rem; font-weight: 700;
  color: var(--ds-white); letter-spacing: .3px;
}}
.ds-nav-sub {{
  font-size: .62rem; color: var(--ds-teal-primary);
  font-weight: 600; letter-spacing: 1px; text-transform: uppercase;
}}
.ds-nav-links {{ display: flex; align-items: center; gap: 6px; }}
.ds-nav-btn {{
  background: transparent;
  border: 1px solid var(--ds-border);
  color: var(--ds-grey);
  font-size: .74rem; font-weight: 500;
  padding: 6px 16px; border-radius: 6px;
  cursor: pointer; transition: all .2s;
  font-family: '{ff}', sans-serif;
  white-space: nowrap;
}}
.ds-nav-btn:hover {{
  border-color: var(--ds-teal-primary);
  color: var(--ds-teal-primary);
}}
.ds-nav-btn.active {{
  background: var(--ds-teal-primary);
  border-color: var(--ds-teal-primary);
  color: #0D1414; font-weight: 700;
}}

/* ── HERO ─────────────────────────────────────────── */
.ds-hero {{
  position: relative;
  aspect-ratio: 16/6;
  width: 100%;
  background-size: cover;
  background-position: center;
  overflow: hidden;
}}
.ds-hero-ov {{
  position: absolute; inset: 0;
  background: linear-gradient(
    105deg,
    {c['navbar_bg']}F5 0%,
    {c['dark_bg']}CC 40%,
    transparent 100%
  );
}}
.ds-hero-body {{
  position: relative; z-index: 2;
  padding: 5% 5%;
  max-width: 55%;
  height: 100%;
  display: flex; flex-direction: column; justify-content: center;
}}
.ds-hero-tag {{
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--ds-teal-primary)18;
  border: 1px solid var(--ds-teal-primary)66;
  color: var(--ds-teal-primary);
  font-size: .6rem; font-weight: 700; letter-spacing: 2px;
  text-transform: uppercase; padding: 5px 14px;
  border-radius: 4px; margin-bottom: 20px;
}}
.ds-hero-h1 {{
  font-size: clamp(1.6rem, 3vw, 2.6rem);
  font-weight: 700; line-height: 1.15;
  color: var(--ds-white); letter-spacing: -.3px;
  margin-bottom: 12px;
}}
.ds-hero-h1 span {{ color: var(--ds-teal-primary); }}
.ds-hero-sub {{
  font-size: clamp(.78rem, 1.1vw, .88rem);
  color: var(--ds-grey); line-height: 1.7;
  margin-bottom: 28px; max-width: 520px;
}}
.ds-hero-cta {{
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--ds-teal-primary);
  color: #0D1414 !important; font-size: .84rem; font-weight: 700;
  padding: 11px 26px; border-radius: 6px;
  text-decoration: none; width: fit-content;
  transition: background .2s, transform .2s;
  box-shadow: 0 4px 20px var(--ds-teal-primary)44;
}}
.ds-hero-cta:hover {{
  background: var(--ds-teal-active);
  transform: translateY(-1px);
}}

/* ── STATS STRIP ─────────────────────────────────── */
.ds-stats {{
  background: var(--ds-section-bg);
  border-top: 1px solid var(--ds-border);
  border-bottom: 1px solid var(--ds-border);
  display: grid; grid-template-columns: repeat(4, 1fr);
  padding: 0 40px;
}}
.ds-stat {{
  padding: 28px 24px;
  border-right: 1px solid var(--ds-border);
  transition: background .2s;
}}
.ds-stat:last-child {{ border-right: none; }}
.ds-stat:hover {{ background: var(--ds-dark-bg); }}
.ds-stat-v {{
  font-size: 1.8rem; font-weight: 700;
  color: var(--ds-teal-primary);
  font-family: 'IBM Plex Mono', monospace;
  line-height: 1.1; margin-bottom: 5px;
}}
.ds-stat-l {{
  font-size: .68rem; color: var(--ds-grey);
  font-weight: 500; text-transform: uppercase;
  letter-spacing: .9px;
}}

/* ── SECTION ─────────────────────────────────────── */
.ds-section {{
  padding: 56px 40px;
}}
.ds-section.alt {{ background: var(--ds-section-bg); }}
.ds-section-head {{ margin-bottom: 32px; }}
.ds-section-tag {{
  display: inline-block;
  color: var(--ds-teal-primary);
  font-size: .65rem; font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase;
  margin-bottom: 8px;
}}
.ds-section-h2 {{
  font-size: 1.45rem; font-weight: 700;
  color: var(--ds-white); margin-bottom: 8px;
}}
.ds-section-sub {{
  font-size: .82rem; color: var(--ds-grey); line-height: 1.6;
}}

/* ── CARD GRID ───────────────────────────────────── */
.ds-grid-4 {{ display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; }}
.ds-grid-3 {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 16px; }}
.ds-grid-2 {{ display: grid; grid-template-columns: repeat(2,1fr); gap: 16px; }}

.ds-card {{
  background: var(--ds-dark-bg);
  border: 1px solid var(--ds-border);
  border-radius: 8px; padding: 22px 20px;
  transition: border-color .25s, transform .25s, box-shadow .25s;
  position: relative; overflow: hidden;
}}
.ds-card::before {{
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: var(--ds-teal-primary);
  transform: scaleX(0); transform-origin: left;
  transition: transform .3s;
}}
.ds-card:hover {{
  border-color: var(--ds-teal-primary)55;
  transform: translateY(-3px);
  box-shadow: 0 8px 32px var(--ds-glow);
}}
.ds-card:hover::before {{ transform: scaleX(1); }}

.ds-card-ico {{ font-size: 1.5rem; margin-bottom: 12px; }}
.ds-card-t {{
  font-size: .88rem; font-weight: 600;
  color: var(--ds-white); margin-bottom: 6px;
}}
.ds-card-d {{
  font-size: .74rem; color: var(--ds-grey); line-height: 1.55;
}}

/* ── ML CARDS ────────────────────────────────────── */
.ds-ml-card {{
  background: var(--ds-dark-bg);
  border: 1px solid var(--ds-border);
  border-radius: 8px; padding: 28px 24px;
  position: relative; overflow: hidden;
  transition: transform .25s, box-shadow .25s;
}}
.ds-ml-card:hover {{
  transform: translateY(-3px);
  box-shadow: 0 8px 32px var(--ds-glow);
}}
.ds-ml-accent {{
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
}}
.ds-ml-name {{
  font-size: 1rem; font-weight: 700;
  color: var(--ds-white);
  font-family: 'IBM Plex Mono', monospace;
  margin-bottom: 4px;
}}
.ds-ml-type {{
  font-size: .68rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 1.2px;
  margin-bottom: 12px;
}}
.ds-ml-desc {{
  font-size: .8rem; color: var(--ds-grey); line-height: 1.6;
}}

/* ── INSIGHT CARDS ───────────────────────────────── */
.ds-ins {{
  background: var(--ds-dark-bg);
  border: 1px solid var(--ds-border);
  border-radius: 8px; padding: 18px 20px;
  display: flex; align-items: flex-start; gap: 14px;
  transition: transform .2s;
}}
.ds-ins:hover {{ transform: translateX(4px); }}
.ds-ins-ico {{ font-size: 1.2rem; flex-shrink: 0; margin-top: 1px; }}
.ds-ins-txt {{ font-size: .83rem; color: var(--ds-white); line-height: 1.6; }}

/* ── DATA BADGES ─────────────────────────────────── */
.ds-badges {{
  display: flex; flex-wrap: wrap; gap: 10px;
  padding: 24px 40px;
  background: var(--ds-dark-bg);
  border-top: 1px solid var(--ds-border);
  border-bottom: 1px solid var(--ds-border);
}}
.ds-badge {{
  background: var(--ds-section-bg);
  border: 1px solid var(--ds-border);
  border-radius: 4px; padding: 7px 14px;
  font-size: .73rem; color: var(--ds-grey); font-weight: 500;
}}
.ds-badge b {{ color: var(--ds-teal-primary); }}

/* ── FOOTER ──────────────────────────────────────── */
.ds-footer {{
  background: var(--ds-navbar-bg);
  border-top: 1px solid var(--ds-border);
  padding: 28px 40px;
  display: flex; justify-content: space-between;
  align-items: center; flex-wrap: wrap; gap: 14px;
}}
.ds-footer-brand {{
  font-size: .84rem; font-weight: 700;
  color: var(--ds-teal-primary);
}}
.ds-footer-sub {{
  font-size: .68rem; color: {c['footer_txt']};
  margin-top: 3px;
}}
.ds-footer-links {{ display: flex; gap: 20px; }}
.ds-footer-links a {{
  font-size: .75rem; color: {c['footer_txt']};
  text-decoration: none; font-weight: 500;
  transition: color .2s;
}}
.ds-footer-links a:hover {{ color: var(--ds-teal-primary); }}

/* ── DIVIDER ─────────────────────────────────────── */
.ds-div {{
  height: 1px;
  background: var(--ds-border);
  margin: 0 40px;
}}
</style>"""

# ══════════════════════════════════════════════════════
# TRANSLATIONS
# ══════════════════════════════════════════════════════
TR = {
"EN": dict(
  name="Saudi Tourism Intelligence",
  sub="AI ANALYTICS PLATFORM",
  pill="🇸🇦  OFFICIAL DATA · MINISTRY OF ECONOMY & PLANNING",
  h1_1="Saudi Tourism", h1_2="Intelligence Platform",
  hs="AI-powered analytics built on 10 years of official government data. Forecasting, segmentation, and sustainability insights — all in one place.",
  hb="Explore Dashboard →",
  s1v="115.8M", s1l="Tourists 2024",
  s2v="1.10B",  s2l="Overnight Stays",
  s3v="5,622",  s3l="Avg Inbound Spend (SAR)",
  s4v="0.986",  s4l="ML Model R² Accuracy",
  pages_tag="PLATFORM",
  pages_h="8 Interactive Pages",
  pages_sub="Comprehensive analysis covering every dimension of Saudi tourism",
  ml_tag="MACHINE LEARNING",
  ml_h="3 Production ML Models",
  ml_sub="Trained on 10 years of official Saudi government data",
  ins_tag="INSIGHTS",
  ins_h="Key Discoveries",
  ins_sub="Data-driven findings from a decade of Saudi tourism",
  f1t="Executive Overview",   f1d="KPIs, trends & insights at a glance",
  f2t="Tourist Trends",       f2d="Annual & monthly patterns 2015–2024",
  f3t="Seasonality",          f3d="Peak months, Ramadan & summer effects",
  f4t="Spending Analysis",    f4d="Per trip, per night, by purpose",
  f5t="Overnight Stays",      f5d="Length of stay & COVID recovery",
  f6t="Demand Forecasting",   f6d="Prophet ML · 2025–2026 predictions",
  f7t="Segmentation",         f7d="K-Means · High / Mid / Budget",
  f8t="Carbon Impact",        f8d="CO₂ index & ESG sustainability",
  m1n="Prophet",           m1t="Demand Forecasting",   m1d="24-month predictions with upper/lower confidence bounds",
  m2n="K-Means",           m2t="Tourist Segmentation",  m2d="3 value segments identified · Silhouette Score: 0.630",
  m3n="Gradient Boosting", m3t="Spending Prediction",   m3d="R² = 0.986 · MAE: SAR 184 per trip",
  i1="Leisure tourism overtook Religious as the #1 purpose in 2024 — a Vision 2030 milestone ✅",
  i2="Inbound avg length of stay surged from 8.6 → 19.2 nights (2021→2024) · +123% growth",
  i3="Inbound tourists spend 4× more than Domestic per trip (SAR 5,622 vs SAR 1,336)",
  i4="2024 all-time record: 115.9M tourists · +150% recovery from the 2020 COVID low",
  ds="Data",      dv="DataSaudi · Ministry of Economy & Planning",
  cv="Coverage",  cvv="2015–2024 · 11 Datasets · 3,210 Records",
  os="License",   ov="Open Source · MIT",
  by="Built by",
  thm_d="🌙", thm_l="☀️", lng="AR",
  fc="© 2025 Saudi Tourism Intelligence · Eng. Goda Emad · All rights reserved",
),
"AR": dict(
  name="ذكاء السياحة السعودية",
  sub="منصة تحليلات الذكاء الاصطناعي",
  pill="🇸🇦  بيانات رسمية · وزارة الاقتصاد والتخطيط",
  h1_1="ذكاء السياحة", h1_2="السعودية",
  hs="منصة تحليلات مبنية على 10 سنوات من البيانات الحكومية الرسمية. توقعات وتقسيم وتحليل استدامة — كل شيء في مكان واحد.",
  hb="← استكشف لوحة التحكم",
  s1v="115.8M", s1l="سائح 2024",
  s2v="1.10B",  s2l="ليالي الإقامة",
  s3v="5,622",  s3l="متوسط إنفاق الوافد (ريال)",
  s4v="0.986",  s4l="دقة نموذج ML",
  pages_tag="المنصة",
  pages_h="8 صفحات تفاعلية",
  pages_sub="تحليل شامل يغطي كل أبعاد السياحة السعودية",
  ml_tag="التعلم الآلي",
  ml_h="3 نماذج ML جاهزة للإنتاج",
  ml_sub="مدرّبة على 10 سنوات من البيانات السعودية الرسمية",
  ins_tag="الاستنتاجات",
  ins_h="أبرز الاكتشافات",
  ins_sub="نتائج مبنية على بيانات عقد كامل من السياحة السعودية",
  f1t="النظرة التنفيذية",   f1d="مؤشرات الأداء والاتجاهات الرئيسية",
  f2t="اتجاهات السياحة",    f2d="الأنماط السنوية والشهرية 2015–2024",
  f3t="الموسمية",            f3d="ذروة الأشهر، تأثير رمضان والصيف",
  f4t="تحليل الإنفاق",      f4d="لكل رحلة، لكل ليلة، حسب الغرض",
  f5t="ليالي الإقامة",       f5d="تطور مدة الإقامة وتعافي كوفيد",
  f6t="توقعات الطلب",        f6d="Prophet ML · توقعات 2025–2026",
  f7t="تقسيم السياح",        f7d="K-Means · عالي/متوسط/اقتصادي",
  f8t="الأثر الكربوني",      f8d="مؤشر CO₂ واستدامة ESG",
  m1n="Prophet",           m1t="توقع الطلب",       m1d="توقعات 24 شهرًا مع فترات الثقة العليا والدنيا",
  m2n="K-Means",           m2t="تقسيم السياح",     m2d="3 شرائح قيمة · معامل Silhouette: 0.630",
  m3n="Gradient Boosting", m3t="توقع الإنفاق",     m3d="R² = 0.986 · MAE: 184 ريال/رحلة",
  i1="الترفيه تجاوز الديني كأول غرض سياحي في 2024 — إنجاز رؤية 2030 ✅",
  i2="متوسط إقامة الوافد قفز من 8.6 → 19.2 ليلة (2021→2024) · نمو +123%",
  i3="الوافدون ينفقون 4 أضعاف المحليين لكل رحلة (5,622 مقابل 1,336 ريال)",
  i4="رقم قياسي 2024: 115.9M سائح · تعافي +150% من أدنى مستوى كوفيد 2020",
  ds="البيانات",   dv="داتا السعودية · وزارة الاقتصاد والتخطيط",
  cv="التغطية",    cvv="2015–2024 · 11 مجموعة · 3,210 سجل",
  os="الرخصة",     ov="مفتوح المصدر · MIT",
  by="من تطوير",
  thm_d="🌙", thm_l="☀️", lng="EN",
  fc="© 2025 ذكاء السياحة السعودية · م. جودة عماد · جميع الحقوق محفوظة",
)}

# ══════════════════════════════════════════════════════
# RENDER
# ══════════════════════════════════════════════════════
c  = DS[theme]
t  = TR[lang]

st.markdown(_css(theme, lang), unsafe_allow_html=True)

hero_b64 = _img("assets/hero.png")
logo_b64 = _img("assets/logo.png")
hero_src = f"url('data:image/png;base64,{hero_b64}')" if hero_b64 \
           else f"linear-gradient(135deg,{c['dark_bg']},{c['bg']})"
logo_tag = f"<img class='ds-nav-logo' src='data:image/png;base64,{logo_b64}'/>" \
           if logo_b64 else "<span style='font-size:1.6rem;'>🇸🇦</span>"

# ── NAVBAR ────────────────────────────────────────────
thm_icon = t["thm_l"] if theme=="dark" else t["thm_d"]
nc1, nc2, nc3, nc4 = st.columns([5, 3, 0.5, 0.7])
with nc1:
    st.markdown(f"""
    <div class='ds-nav-brand'>
      {logo_tag}
      <div>
        <div class='ds-nav-name'>{t['name']}</div>
        <div class='ds-nav-sub'>{t['sub']}</div>
      </div>
    </div>""", unsafe_allow_html=True)
with nc3:
    if st.button(thm_icon, use_container_width=True, key="thm"):
        st.session_state.theme = "light" if theme=="dark" else "dark"
        st.rerun()
with nc4:
    if st.button(t["lng"], use_container_width=True, key="lng"):
        st.session_state.lang = "AR" if lang=="EN" else "EN"
        st.rerun()

st.markdown("<div style='height:2px;background:var(--ds-border);margin-bottom:0;'></div>",
            unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────
st.markdown(f"""
<div class='ds-hero' style='background-image:{hero_src};'>
  <div class='ds-hero-ov'></div>
  <div class='ds-hero-body'>
    <div class='ds-hero-tag'>{t['pill']}</div>
    <h1 class='ds-hero-h1'>{t['h1_1']}<br><span>{t['h1_2']}</span></h1>
    <p class='ds-hero-sub'>{t['hs']}</p>
    <a class='ds-hero-cta' href='#'>
      {t['hb']}
    </a>
  </div>
</div>""", unsafe_allow_html=True)

# ── STATS ─────────────────────────────────────────────
st.markdown(f"""
<div class='ds-stats'>
  <div class='ds-stat'>
    <div class='ds-stat-v'>{t['s1v']}</div>
    <div class='ds-stat-l'>{t['s1l']}</div>
  </div>
  <div class='ds-stat'>
    <div class='ds-stat-v'>{t['s2v']}</div>
    <div class='ds-stat-l'>{t['s2l']}</div>
  </div>
  <div class='ds-stat'>
    <div class='ds-stat-v'>{t['s3v']}</div>
    <div class='ds-stat-l'>{t['s3l']}</div>
  </div>
  <div class='ds-stat'>
    <div class='ds-stat-v'>{t['s4v']}</div>
    <div class='ds-stat-l'>{t['s4l']}</div>
  </div>
</div>""", unsafe_allow_html=True)

# ── PAGES SECTION ─────────────────────────────────────
feats = [
    ("🏠","f1t","f1d"),("📈","f2t","f2d"),("📅","f3t","f3d"),("💰","f4t","f4d"),
    ("🏨","f5t","f5d"),("🔮","f6t","f6d"),("🎯","f7t","f7d"),("🌱","f8t","f8d"),
]
cards_html = "".join(f"""
  <div class='ds-card'>
    <div class='ds-card-ico'>{ico}</div>
    <div class='ds-card-t'>{t[tk]}</div>
    <div class='ds-card-d'>{t[dk]}</div>
  </div>""" for ico,tk,dk in feats)

st.markdown(f"""
<div class='ds-section'>
  <div class='ds-section-head'>
    <div class='ds-section-tag'>{t['pages_tag']}</div>
    <div class='ds-section-h2'>{t['pages_h']}</div>
    <div class='ds-section-sub'>{t['pages_sub']}</div>
  </div>
  <div class='ds-grid-4'>{cards_html}</div>
</div>""", unsafe_allow_html=True)

st.markdown("<div class='ds-div'></div>", unsafe_allow_html=True)

# ── ML SECTION ────────────────────────────────────────
ml_items = [
    ("m1n","m1t","m1d", c["teal"],   "🔮"),
    ("m2n","m2t","m2d", c["orange"], "🎯"),
    ("m3n","m3t","m3d", c["blue"],   "💰"),
]
ml_html = "".join(f"""
  <div class='ds-ml-card'>
    <div class='ds-ml-accent' style='background:{color};'></div>
    <div style='margin-bottom:16px;font-size:1.6rem;'>{ico}</div>
    <div class='ds-ml-name'>{t[nk]}</div>
    <div class='ds-ml-type' style='color:{color};'>{t[tk]}</div>
    <div class='ds-ml-desc'>{t[dk]}</div>
  </div>""" for nk,tk,dk,color,ico in ml_items)

st.markdown(f"""
<div class='ds-section alt'>
  <div class='ds-section-head'>
    <div class='ds-section-tag'>{t['ml_tag']}</div>
    <div class='ds-section-h2'>{t['ml_h']}</div>
    <div class='ds-section-sub'>{t['ml_sub']}</div>
  </div>
  <div class='ds-grid-3'>{ml_html}</div>
</div>""", unsafe_allow_html=True)

st.markdown("<div class='ds-div'></div>", unsafe_allow_html=True)

# ── INSIGHTS SECTION ──────────────────────────────────
ins_colors = [c["teal"], c["orange"], c["blue"], c["teal_active"]]
ins_icons  = ["🏖️","⏰","💰","🚀"]
ins_keys   = ["i1","i2","i3","i4"]
ins_html   = "".join(f"""
  <div class='ds-ins' style='border-left:2px solid {col};'>
    <div class='ds-ins-ico'>{ico}</div>
    <div class='ds-ins-txt'>{t[key]}</div>
  </div>""" for ico,col,key in zip(ins_icons,ins_colors,ins_keys))

st.markdown(f"""
<div class='ds-section'>
  <div class='ds-section-head'>
    <div class='ds-section-tag'>{t['ins_tag']}</div>
    <div class='ds-section-h2'>{t['ins_h']}</div>
    <div class='ds-section-sub'>{t['ins_sub']}</div>
  </div>
  <div class='ds-grid-2'>{ins_html}</div>
</div>""", unsafe_allow_html=True)

# ── DATA BADGES ───────────────────────────────────────
st.markdown(f"""
<div class='ds-badges'>
  <div class='ds-badge'><b>📦</b> {t['ds']}: {t['dv']}</div>
  <div class='ds-badge'><b>📅</b> {t['cv']}: {t['cvv']}</div>
  <div class='ds-badge'><b>🐙</b> github.com/Goda-Emad</div>
  <div class='ds-badge'><b>🔑</b> {t['os']}: {t['ov']}</div>
  <div class='ds-badge'><b>🐍</b> Python · Streamlit · Plotly · Prophet · Scikit-learn</div>
</div>""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────
st.markdown(f"""
<div class='ds-footer'>
  <div>
    <div class='ds-footer-brand'>🇸🇦 {t['name']}</div>
    <div class='ds-footer-sub'>{t['fc']}</div>
  </div>
  <div class='ds-footer-links'>
    <a href='https://github.com/Goda-Emad/Saudi-Tourism-Intelligence' target='_blank'>🐙 GitHub</a>
    <a href='https://www.linkedin.com/in/goda-emad/' target='_blank'>💼 LinkedIn</a>
    <a href='https://datasaudi.sa' target='_blank'>📊 DataSaudi</a>
  </div>
</div>""", unsafe_allow_html=True)
