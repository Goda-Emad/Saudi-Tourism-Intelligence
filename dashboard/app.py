import streamlit as st
import base64, os
import time

# ══════════════════════════════════════════════════════
# FIX: حل مشكلة React Error #290
# ══════════════════════════════════════════════════════
if '_react_initialized' not in st.session_state:
    st.session_state._react_initialized = True
    # تأخير بسيط لضمان تحميل React بشكل صحيح
    time.sleep(0.1)
    st.rerun()

# استيراد option_menu بطريقة آمنة
try:
    # محاولة استيراد المكتبة بشكل طبيعي
    from streamlit_option_menu import option_menu
    OPTION_MENU_AVAILABLE = True
except:
    OPTION_MENU_AVAILABLE = False
    st.warning("⚠️ مكتبة القوائم غير متوفرة، سيتم استخدام البديل المحلي")

# ══════════════════════════════════════════════════════
# بديل محلي لـ option_menu (لا يستخدم React)
# ══════════════════════════════════════════════════════
def safe_option_menu(options, icons=None, menu_title=None, default_index=0, orientation="vertical"):
    """
    بديل آمن تماماً من مشاكل React
    """
    if menu_title:
        if orientation == "vertical":
            st.sidebar.markdown(f"### {menu_title}")
            st.sidebar.markdown("---")
        else:
            st.markdown(f"### {menu_title}")
    
    selected = default_index
    
    if orientation == "vertical":
        # قائمة رأسية في sidebar
        for i, option in enumerate(options):
            icon = icons[i] if icons and i < len(icons) else "•"
            col1, col2 = st.sidebar.columns([1, 5])
            with col1:
                st.markdown(f"<h3 style='margin:0; color:{st.session_state.get('theme_color', '#C9A84C')}'>{icon}</h3>", 
                          unsafe_allow_html=True)
            with col2:
                if st.button(option, key=f"nav_{i}", use_container_width=True):
                    selected = i
            if i < len(options) - 1:
                st.sidebar.markdown("---")
    else:
        # قائمة أفقية
        cols = st.columns(len(options))
        for i, (col, option) in enumerate(zip(cols, options)):
            icon = icons[i] if icons and i < len(icons) else "•"
            with col:
                if st.button(f"{icon} {option}", key=f"nav_h_{i}", use_container_width=True):
                    selected = i
    
    return options[selected]

# ══════════════════════════════════════════════════════
# إعدادات الصفحة
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Saudi Tourism Intelligence",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════
for k, v in [("lang","EN"), ("theme","dark"), ("theme_color","#C9A84C")]:
    if k not in st.session_state:
        st.session_state[k] = v

lang  = st.session_state.lang
theme = st.session_state.theme

# ══════════════════════════════════════════════════════
# @st.cache_data — runs ONCE, never again on rerun
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
def _palette(theme: str) -> dict:
    if theme == "dark":
        return {"bg":      "#002B1E", "card":    "#003D2B", "card2":   "#004D38",
                "sidebar": "#001F16", "text":    "#FFFFFF", "sec":     "#A8D5C0",
                "gold":    "#C9A84C", "gold2":   "#E8C96A", "teal":    "#00E5A0",
                "teal2":   "#00BFA5", "green":   "#4CAF7D", "border":  "#005C3F",
                "glow":    "#00E5A033","hero_ov": "#001F16DD"}
    return     {"bg":      "#F0FAF5", "card":    "#FFFFFF", "card2":   "#E8F5EE",
                "sidebar": "#FFFFFF", "text":    "#001F16", "sec":     "#2E7D5A",
                "gold":    "#A67C00", "gold2":   "#C9A84C", "teal":    "#007A5C",
                "teal2":   "#009973", "green":   "#2E7D5A", "border":  "#B2DFCC",
                "glow":    "#00BFA518","hero_ov": "#E0F2E9DD"}

@st.cache_data(show_spinner=False)
def _css(theme: str, lang: str) -> str:
    p   = _palette(theme)
    # تحديث لون الثيم في session state
    st.session_state.theme_color = p['gold']
    
    ff  = "Tajawal" if lang == "AR" else "Sora"
    dir = "rtl"     if lang == "AR" else "ltr"
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800;900&family=IBM+Plex+Mono:wght@400;600;700&family=Tajawal:wght@300;400;700;800;900&display=swap');
*{{box-sizing:border-box;margin:0;padding:0;}}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{{
  background:{p['bg']}!important;font-family:'{ff}',sans-serif;direction:{dir};}}
section[data-testid="stSidebar"]{{
  background:{p['sidebar']}!important;border-right:1px solid {p['border']};}}
section[data-testid="stSidebar"] *{{color:{p['text']}!important;}}

/* ── TOPBAR ─────────────────────────── */
.topbar{{
  display:flex;justify-content:space-between;align-items:center;
  padding:12px 0;margin-bottom:0;
}}
.topbar-brand{{display:flex;align-items:center;gap:12px;}}
.topbar-logo{{height:42px;border-radius:8px;}}
.topbar-name{{font-size:.95rem;font-weight:800;color:{p['gold2']};}}
.topbar-sub{{font-size:.65rem;color:{p['sec']};letter-spacing:.5px;}}
.topbar-actions{{display:flex;gap:8px;align-items:center;}}
.topbar-btn{{
  background:{p['card']};border:1px solid {p['border']};
  color:{p['text']};font-size:.74rem;font-weight:600;
  padding:7px 14px;border-radius:20px;cursor:pointer;
  transition:border-color .2s,color .2s;white-space:nowrap;
}}
.topbar-btn:hover{{border-color:{p['gold']};color:{p['gold2']};}}

/* ── HERO ───────────────────────────── */
.hero{{
  position:relative;border-radius:22px;overflow:hidden;
  aspect-ratio:16/7;width:100%;margin:14px 0 26px;
  background-size:cover;background-position:center;
}}
.hero-ov{{
  position:absolute;inset:0;
  background:linear-gradient(105deg,{p['hero_ov']} 0%,{p['bg']}CC 42%,transparent 100%);
}}
.hero-body{{position:relative;z-index:2;padding:6% 5%;max-width:58%;}}
.pill{{
  display:inline-block;background:{p['gold']}20;
  border:1px solid {p['gold']}77;color:{p['gold2']};
  font-size:.6rem;font-weight:700;letter-spacing:2px;
  text-transform:uppercase;padding:5px 16px;
  border-radius:30px;margin-bottom:18px;
}}
.hero-h1{{font-size:clamp(1.6rem,3.5vw,2.8rem);font-weight:900;
  color:{p['text']};line-height:1.08;letter-spacing:-.5px;margin-bottom:4px;}}
.hero-h2{{font-size:clamp(1.6rem,3.5vw,2.8rem);font-weight:900;
  color:{p['teal']};line-height:1.08;letter-spacing:-.5px;margin-bottom:16px;}}
.hero-sub{{font-size:clamp(.75rem,1.2vw,.9rem);color:{p['sec']};
  line-height:1.65;margin-bottom:26px;}}
.hero-btn{{
  display:inline-block;
  background:linear-gradient(135deg,{p['gold']},{p['gold2']});
  color:{p['bg']}!important;font-size:.86rem;font-weight:800;
  padding:12px 28px;border-radius:30px;text-decoration:none;
  box-shadow:0 4px 20px {p['gold']}55;transition:all .25s;
}}
.hero-btn:hover{{transform:translateY(-2px);box-shadow:0 8px 32px {p['gold']}88;}}

/* ── STATS ──────────────────────────── */
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:30px;}}
.stat{{
  background:{p['card']};border:1px solid {p['border']};
  border-bottom:3px solid {p['gold']};border-radius:16px;
  padding:20px 16px;text-align:center;
  transition:transform .2s,box-shadow .2s;
}}
.stat:hover{{transform:translateY(-3px);box-shadow:0 8px 28px {p['glow']};}}
.sv{{font-size:1.7rem;font-weight:900;color:{p['gold2']};
  font-family:'IBM Plex Mono',monospace;}}
.sl{{font-size:.67rem;color:{p['sec']};font-weight:600;
  text-transform:uppercase;letter-spacing:.9px;margin-top:5px;}}

/* ── DIVIDER ────────────────────────── */
.div{{height:1px;
  background:linear-gradient(90deg,transparent,{p['gold']}66,{p['teal']}66,transparent);
  margin:24px 0;}}

/* ── SECTION HEAD ───────────────────── */
.sh h2{{font-size:1.35rem;font-weight:800;color:{p['text']};margin-bottom:4px;}}
.sh p{{font-size:.79rem;color:{p['sec']};margin-bottom:18px;}}

/* ── FEATURES ───────────────────────── */
.fg{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:28px;}}
.fc{{background:{p['card']};border:1px solid {p['border']};border-radius:14px;
  padding:20px 17px;transition:transform .2s,border-color .2s,box-shadow .2s;}}
.fc:hover{{transform:translateY(-3px);border-color:{p['gold']}88;
  box-shadow:0 6px 24px {p['gold']}22;}}
.fi{{font-size:1.55rem;margin-bottom:9px;}}
.ft{{font-size:.86rem;font-weight:700;color:{p['text']};margin-bottom:4px;}}
.fd{{font-size:.73rem;color:{p['sec']};line-height:1.5;}}

/* ── ML CARDS ───────────────────────── */
.mg{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:28px;}}
.mc{{background:{p['card']};border:1px solid {p['border']};border-radius:16px;
  padding:24px 20px;position:relative;overflow:hidden;transition:transform .2s;}}
.mc:hover{{transform:translateY(-3px);}}
.mc::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;}}
.mc1::before{{background:linear-gradient(90deg,{p['gold']},{p['gold2']});}}
.mc2::before{{background:linear-gradient(90deg,{p['teal']},{p['teal2']});}}
.mc3::before{{background:linear-gradient(90deg,{p['gold2']},{p['teal']});}}
.mg-glow{{position:absolute;top:-50px;right:-50px;width:120px;height:120px;
  border-radius:50%;opacity:.06;}}
.mn{{font-size:1rem;font-weight:800;color:{p['text']};
  font-family:'IBM Plex Mono',monospace;margin-bottom:4px;}}
.mt{{font-size:.68rem;font-weight:700;text-transform:uppercase;
  letter-spacing:1.2px;margin-bottom:10px;}}
.md{{font-size:.81rem;color:{p['sec']};line-height:1.6;}}

/* ── INSIGHTS ───────────────────────── */
.ig{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:28px;}}
.ic{{background:{p['card']};border:1px solid {p['border']};border-radius:13px;
  padding:15px 17px;display:flex;align-items:flex-start;gap:11px;
  transition:transform .2s;}}
.ic:hover{{transform:translateX(4px);}}
.ii{{font-size:1.2rem;flex-shrink:0;margin-top:1px;}}
.it{{font-size:.83rem;color:{p['text']};line-height:1.55;}}

/* ── DATA STRIP ─────────────────────── */
.ds{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:26px;}}
.db{{background:{p['card']};border:1px solid {p['border']};border-radius:9px;
  padding:8px 14px;font-size:.75rem;color:{p['text']};font-weight:600;}}
.db b{{color:{p['gold2']};}}

/* ── FOOTER ─────────────────────────── */
.footer{{background:{p['card']};border:1px solid {p['border']};
  border-top:3px solid {p['gold']};border-radius:16px;
  padding:20px 26px;display:flex;justify-content:space-between;
  align-items:center;flex-wrap:wrap;gap:12px;}}
.fb{{font-size:.88rem;font-weight:800;color:{p['gold2']};}}
.fs{{font-size:.68rem;color:{p['sec']};margin-top:2px;}}
.fl{{display:flex;gap:14px;}}
.fl a{{font-size:.77rem;color:{p['sec']};text-decoration:none;font-weight:600;}}
.fl a:hover{{color:{p['gold2']};}}
</style>"""

# ══════════════════════════════════════════════════════
# TRANSLATIONS
# ══════════════════════════════════════════════════════
TR = {
"EN": dict(
  name="Saudi Tourism Intelligence", sub="Vision 2030 · AI Analytics Platform",
  pill="🇸🇦  OFFICIAL DATA · MINISTRY OF ECONOMY & PLANNING",
  h1="Saudi Tourism", h2="Intelligence",
  hs="AI-Powered Analytics Platform · 10 Years of Official Data · 3 Production ML Models",
  hb="Explore Dashboard →",
  s1v="115.8M",s1l="Tourists 2024", s2v="1.1B",s2l="Overnight Stays",
  s3v="SAR 5,622",s3l="Avg Inbound Spend", s4v="R²=0.986",s4l="ML Accuracy",
  ftl="What's Inside", fts="8 interactive pages · Official government data · 3 production ML models",
  f1t="Executive Overview",f1d="KPIs, trends & key insights",
  f2t="Tourist Trends",   f2d="Annual & monthly patterns 2015–2024",
  f3t="Seasonality",      f3d="Peak months, Ramadan & summer effects",
  f4t="Spending Analysis",f4d="Per trip, per night, by purpose",
  f5t="Overnight Stays",  f5d="Length of stay & COVID impact",
  f6t="Demand Forecasting",f6d="Prophet ML · 2025–2026 predictions",
  f7t="Segmentation",     f7d="K-Means · High / Mid / Budget",
  f8t="Carbon Impact",    f8d="CO₂ index & sustainability metrics",
  mtl="Machine Learning Models", mts="Production-ready · Trained on 10 years of official Saudi government data",
  m1n="Prophet",          m1t="Demand Forecasting",  m1d="24-month predictions with confidence intervals",
  m2n="K-Means",          m2t="Tourist Segmentation",m2d="3 value segments · Silhouette Score 0.630",
  m3n="Gradient Boosting",m3t="Spending Prediction", m3d="R² = 0.986 · MAE: SAR 184/trip",
  itl="Key Insights",
  i1="Leisure overtook Religious as #1 purpose in 2024 — Vision 2030 milestone ✅",
  i2="Inbound avg stay jumped from 8.6 → 19.2 nights (2021→2024) · +123%",
  i3="Inbound tourists spend 4× more than Domestic (SAR 5,622 vs SAR 1,336)",
  i4="2024 all-time record: 115.9M tourists · +150% recovery from COVID low",
  ds="Data Source",dv="DataSaudi · Ministry of Economy & Planning",
  cv="Coverage",cvv="2015–2024 · 11 Datasets · 3,210 Records",
  by="Built by",
  thm_btn="☀️ Light", lng_btn="🌐 العربية",
  fc="© 2025 Saudi Tourism Intelligence · Eng. Goda Emad · All rights reserved",
),
"AR": dict(
  name="ذكاء السياحة السعودية", sub="رؤية 2030 · منصة تحليلات AI",
  pill="🇸🇦  بيانات رسمية · وزارة الاقتصاد والتخطيط",
  h1="ذكاء السياحة", h2="السعودية",
  hs="منصة تحليلات مدعومة بالذكاء الاصطناعي · 10 سنوات من البيانات الرسمية · 3 نماذج ML",
  hb="← استكشف لوحة التحكم",
  s1v="115.8M",s1l="سائح 2024", s2v="1.1B",s2l="ليالي الإقامة",
  s3v="5,622 ر",s3l="متوسط إنفاق الوافد", s4v="R²=0.986",s4l="دقة النموذج",
  ftl="ما بداخله", fts="8 صفحات تفاعلية · بيانات حكومية رسمية · 3 نماذج ML جاهزة",
  f1t="النظرة التنفيذية",  f1d="مؤشرات الأداء والاتجاهات الرئيسية",
  f2t="اتجاهات السياحة",   f2d="الأنماط السنوية والشهرية 2015–2024",
  f3t="الموسمية",           f3d="ذروة الأشهر، تأثير رمضان والصيف",
  f4t="تحليل الإنفاق",     f4d="لكل رحلة، لكل ليلة، حسب الغرض",
  f5t="ليالي الإقامة",      f5d="تطور مدة الإقامة وتأثير كوفيد",
  f6t="توقعات الطلب",       f6d="Prophet ML · توقعات 2025–2026",
  f7t="تقسيم السياح",       f7d="K-Means · عالي/متوسط/اقتصادي",
  f8t="الأثر الكربوني",     f8d="مؤشر CO₂ ومقاييس الاستدامة",
  mtl="نماذج التعلم الآلي", mts="جاهزة للإنتاج · مدرّبة على 10 سنوات من بيانات سعودية رسمية",
  m1n="Prophet",          m1t="توقع الطلب",      m1d="توقعات 24 شهرًا مع فترات الثقة",
  m2n="K-Means",          m2t="تقسيم السياح",   m2d="3 شرائح · معامل Silhouette 0.630",
  m3n="Gradient Boosting",m3t="توقع الإنفاق",   m3d="R² = 0.986 · MAE: 184 ريال/رحلة",
  itl="أبرز الاستنتاجات",
  i1="الترفيه تجاوز الديني كأول غرض سياحي في 2024 — إنجاز رؤية 2030 ✅",
  i2="متوسط إقامة الوافد: 8.6 → 19.2 ليلة (2021→2024) · +123%",
  i3="الوافدون ينفقون 4 أضعاف المحليين (5,622 مقابل 1,336 ريال)",
  i4="رقم قياسي 2024: 115.9M سائح · تعافي +150% من أدنى مستوى كوفيد",
  ds="مصدر البيانات",dv="داتا السعودية · وزارة الاقتصاد والتخطيط",
  cv="التغطية",cvv="2015–2024 · 11 مجموعة · 3,210 سجل",
  by="من تطوير",
  thm_btn="☀️ فاتح", lng_btn="🌐 English",
  fc="© 2025 ذكاء السياحة السعودية · م. جودة عماد · جميع الحقوق محفوظة",
)}

# ══════════════════════════════════════════════════════
# RENDER — CSS + data (all cached, zero re-compute)
# ══════════════════════════════════════════════════════
p  = _palette(theme)
t  = TR[lang]
st.markdown(_css(theme, lang), unsafe_allow_html=True)

hero_b64 = _img("assets/hero.png")
logo_b64 = _img("assets/logo.png")
hero_src = f"url('data:image/png;base64,{hero_b64}')" if hero_b64 \
           else f"linear-gradient(135deg,{p['bg']},{p['card']})"
logo_tag = f"<img class='topbar-logo' src='data:image/png;base64,{logo_b64}'/>" \
           if logo_b64 else "<span style='font-size:1.8rem;'>🇸🇦</span>"

# ── TOPBAR (no sidebar — cleaner home page) ───────────
thm_next = "light" if theme=="dark" else "dark"
lng_next  = "AR"    if lang=="EN"   else "EN"

c_logo, c_space, c_thm, c_lng = st.columns([3,6,1,1])
with c_logo:
    st.markdown(f"""
    <div class='topbar-brand'>
      {logo_tag}
      <div>
        <div class='topbar-name'>{t['name']}</div>
        <div class='topbar-sub'>{t['sub']}</div>
      </div>
    </div>""", unsafe_allow_html=True)
with c_thm:
    if st.button("🌙" if theme=="dark" else "☀️", use_container_width=True, key="thm"):
        st.session_state.theme = thm_next
        st.rerun()
with c_lng:
    if st.button("AR" if lang=="EN" else "EN", use_container_width=True, key="lng"):
        st.session_state.lang  = lng_next
        st.rerun()

# ── HERO ──────────────────────────────────────────────
st.markdown(f"""
<div class='hero' style='background-image:{hero_src};'>
  <div class='hero-ov'></div>
  <div class='hero-body'>
    <div class='pill'>{t['pill']}</div>
    <div class='hero-h1'>{t['h1']}</div>
    <div class='hero-h2'>{t['h2']}</div>
    <p class='hero-sub'>{t['hs']}</p>
    <a class='hero-btn' href='#'>{t['hb']}</a>
  </div>
</div>""", unsafe_allow_html=True)

# ── STATS ─────────────────────────────────────────────
st.markdown(f"""
<div class='stats'>
  <div class='stat'><div class='sv'>{t['s1v']}</div><div class='sl'>{t['s1l']}</div></div>
  <div class='stat'><div class='sv'>{t['s2v']}</div><div class='sl'>{t['s2l']}</div></div>
  <div class='stat'><div class='sv'>{t['s3v']}</div><div class='sl'>{t['s3l']}</div></div>
  <div class='stat'><div class='sv'>{t['s4v']}</div><div class='sl'>{t['s4l']}</div></div>
</div>""", unsafe_allow_html=True)

# ── FEATURES ──────────────────────────────────────────
st.markdown(f"""
<div class='sh'><h2>{t['ftl']}</h2><p>{t['fts']}</p></div>
<div class='fg'>
  <div class='fc'><div class='fi'>🏠</div><div class='ft'>{t['f1t']}</div><div class='fd'>{t['f1d']}</div></div>
  <div class='fc'><div class='fi'>📈</div><div class='ft'>{t['f2t']}</div><div class='fd'>{t['f2d']}</div></div>
  <div class='fc'><div class='fi'>📅</div><div class='ft'>{t['f3t']}</div><div class='fd'>{t['f3d']}</div></div>
  <div class='fc'><div class='fi'>💰</div><div class='ft'>{t['f4t']}</div><div class='fd'>{t['f4d']}</div></div>
  <div class='fc'><div class='fi'>🏨</div><div class='ft'>{t['f5t']}</div><div class='fd'>{t['f5d']}</div></div>
  <div class='fc'><div class='fi'>🔮</div><div class='ft'>{t['f6t']}</div><div class='fd'>{t['f6d']}</div></div>
  <div class='fc'><div class='fi'>🎯</div><div class='ft'>{t['f7t']}</div><div class='fd'>{t['f7d']}</div></div>
  <div class='fc'><div class='fi'>🌱</div><div class='ft'>{t['f8t']}</div><div class='fd'>{t['f8d']}</div></div>
</div>""", unsafe_allow_html=True)

st.markdown("<div class='div'></div>", unsafe_allow_html=True)

# ── ML MODELS ─────────────────────────────────────────
st.markdown(f"""
<div class='sh'><h2>{t['mtl']}</h2><p>{t['mts']}</p></div>
<div class='mg'>
  <div class='mc mc1'>
    <div class='mg-glow' style='background:{p["gold"]};'></div>
    <div class='mn'>🔮 {t['m1n']}</div>
    <div class='mt' style='color:{p["gold2"]};'>{t['m1t']}</div>
    <div class='md'>{t['m1d']}</div>
  </div>
  <div class='mc mc2'>
    <div class='mg-glow' style='background:{p["teal"]};'></div>
    <div class='mn'>🎯 {t['m2n']}</div>
    <div class='mt' style='color:{p["teal"]};'>{t['m2t']}</div>
    <div class='md'>{t['m2d']}</div>
  </div>
  <div class='mc mc3'>
    <div class='mg-glow' style='background:{p["gold2"]};'></div>
    <div class='mn'>💰 {t['m3n']}</div>
    <div class='mt' style='color:{p["gold2"]};'>{t['m3t']}</div>
    <div class='md'>{t['m3d']}</div>
  </div>
</div>""", unsafe_allow_html=True)

st.markdown("<div class='div'></div>", unsafe_allow_html=True)

# ── INSIGHTS ──────────────────────────────────────────
ins=[("🏖️",t["i1"],p["gold"]),("⏰",t["i2"],p["teal"]),
     ("💰",t["i3"],p["gold2"]),("🚀",t["i4"],p["teal2"])]
st.markdown(f"<div class='sh'><h2>{t['itl']}</h2></div><div class='ig'>", unsafe_allow_html=True)
for ico,txt,col in ins:
    st.markdown(f"<div class='ic' style='border-left:3px solid {col};'><div class='ii'>{ico}</div><div class='it'>{txt}</div></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='div'></div>", unsafe_allow_html=True)

# ── DATA BADGES + FOOTER ──────────────────────────────
st.markdown(f"""
<div class='ds'>
  <div class='db'><b>📦</b> {t['ds']}: {t['dv']}</div>
  <div class='db'><b>📅</b> {t['cv']}: {t['cvv']}</div>
  <div class='db'><b>🐙</b> github.com/Goda-Emad</div>
  <div class='db'><b>🐍</b> Python · Streamlit · Plotly · Prophet · Scikit-learn</div>
</div>
<div class='footer'>
  <div>
    <div class='fb'>🇸🇦 {t['name']}</div>
    <div class='fs'>{t['fc']}</div>
  </div>
  <div class='fl'>
    <a href='https://github.com/Goda-Emad/Saudi-Tourism-Intelligence' target='_blank'>🐙 GitHub</a>
    <a href='https://www.linkedin.com/in/goda-emad/' target='_blank'>💼 LinkedIn</a>
    <a href='https://datasaudi.sa' target='_blank'>📊 DataSaudi</a>
  </div>
</div>""", unsafe_allow_html=True)

# ── FIX: إذا كان هناك option_menu مستخدم في مكان آخر ──
if OPTION_MENU_AVAILABLE:
    st.sidebar.markdown("### 🧭 التنقل")
    # استخدام option_menu الأصلي إذا كان متاحاً
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=["الرئيسية", "تحليل البيانات", "النماذج", "حول"],
            icons=["house", "graph-up", "robot", "info-circle"],
            default_index=0,
            orientation="vertical"
        )
else:
    # استخدام البديل الآمن
    st.sidebar.markdown("### 🧭 التنقل")
    selected = safe_option_menu(
        options=["الرئيسية", "تحليل البيانات", "النماذج", "حول"],
        icons=["🏠", "📊", "🤖", "ℹ️"],
        menu_title=None,
        default_index=0,
        orientation="vertical"
    )
