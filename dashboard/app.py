import streamlit as st
import base64, os

st.set_page_config(
    page_title="Saudi Tourism Intelligence",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "lang" not in st.session_state:
    st.session_state.lang = "EN"
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

lang  = st.session_state.lang
theme = st.session_state.theme

# ══════════════════════════════════════════
# TRANSLATIONS
# ══════════════════════════════════════════
T = {
    "EN": {
        "nav_title":     "Saudi Tourism Intelligence",
        "nav_sub":       "Vision 2030 · AI Analytics Platform",
        "hero_tag":      "🇸🇦  OFFICIAL DATA · MINISTRY OF ECONOMY & PLANNING",
        "hero_title_1":  "Saudi Tourism",
        "hero_title_2":  "Intelligence",
        "hero_sub":      "AI-Powered Analytics Platform · 10 Years of Data · 3 Production ML Models",
        "hero_btn":      "Explore Dashboard →",
        "stat1_v":"115.8M",  "stat1_l":"Tourists 2024",
        "stat2_v":"1.1B",    "stat2_l":"Overnight Stays",
        "stat3_v":"SAR 5,622","stat3_l":"Avg Inbound Spend",
        "stat4_v":"R²=0.986","stat4_l":"ML Accuracy",
        "feat_title": "What's Inside",
        "feat_sub":   "8 interactive pages · Official government data · 3 production ML models",
        "f1t":"Executive Overview",   "f1d":"KPIs, trends & key insights",
        "f2t":"Tourist Trends",       "f2d":"Annual & monthly patterns 2015–2024",
        "f3t":"Seasonality",          "f3d":"Peak months, Ramadan & summer effects",
        "f4t":"Spending Analysis",    "f4d":"Per trip, per night, by purpose",
        "f5t":"Overnight Stays",      "f5d":"Length of stay & COVID impact",
        "f6t":"Demand Forecasting",   "f6d":"Prophet ML · 2025–2026 predictions",
        "f7t":"Segmentation",         "f7d":"K-Means · High / Mid / Budget",
        "f8t":"Carbon Impact",        "f8d":"CO₂ index & sustainability metrics",
        "ml_title":  "Machine Learning Models",
        "ml_sub":    "Production-ready · Trained on 10 years of official Saudi data",
        "m1n":"Prophet",          "m1t":"Demand Forecasting",  "m1d":"24-month predictions with confidence intervals",
        "m2n":"K-Means",          "m2t":"Tourist Segmentation","m2d":"3 value segments · Silhouette Score 0.630",
        "m3n":"Gradient Boosting","m3t":"Spending Prediction", "m3d":"R² = 0.986 · MAE: SAR 184/trip",
        "ins_title": "Key Insights",
        "i1":"Leisure overtook Religious as #1 purpose in 2024 — Vision 2030 milestone ✅",
        "i2":"Inbound avg stay jumped from 8.6 → 19.2 nights (2021→2024) · +123%",
        "i3":"Inbound tourists spend 4× more than Domestic (SAR 5,622 vs SAR 1,336)",
        "i4":"2024 all-time record: 115.9M tourists · +150% recovery from COVID low",
        "data_src":"Data Source","data_val":"DataSaudi · Ministry of Economy & Planning",
        "coverage":"Coverage","cov_val":"2015–2024 · 11 Datasets · 3,210 Records",
        "built_by":"Built by","open_src":"Open Source",
        "lang_btn":"🌐 العربية","dark_btn":"🌙 Dark","light_btn":"☀️ Light",
        "nav_lbl":"Navigation",
        "p1":"🏠 Overview","p2":"📈 Tourist Trends","p3":"📅 Seasonality","p4":"💰 Spending",
        "p5":"🏨 Overnight Stays","p6":"🔮 Forecasting","p7":"🎯 Segmentation","p8":"🌱 Carbon Impact",
        "footer":"© 2025 Saudi Tourism Intelligence · Eng. Goda Emad · All rights reserved",
    },
    "AR": {
        "nav_title":     "ذكاء السياحة السعودية",
        "nav_sub":       "رؤية 2030 · منصة تحليلات ذكاء اصطناعي",
        "hero_tag":      "🇸🇦  بيانات رسمية · وزارة الاقتصاد والتخطيط",
        "hero_title_1":  "ذكاء السياحة",
        "hero_title_2":  "السعودية",
        "hero_sub":      "منصة تحليلات مدعومة بالذكاء الاصطناعي · 10 سنوات من البيانات · 3 نماذج ML",
        "hero_btn":      "← استكشف لوحة التحكم",
        "stat1_v":"115.8M","stat1_l":"سائح 2024",
        "stat2_v":"1.1B",  "stat2_l":"ليالي الإقامة",
        "stat3_v":"5,622 ر","stat3_l":"متوسط إنفاق الوافد",
        "stat4_v":"R²=0.986","stat4_l":"دقة النموذج",
        "feat_title":"ما بداخله",
        "feat_sub":"8 صفحات تفاعلية · بيانات حكومية رسمية · 3 نماذج ML جاهزة",
        "f1t":"النظرة التنفيذية",   "f1d":"مؤشرات الأداء والاتجاهات",
        "f2t":"اتجاهات السياحة",    "f2d":"الأنماط السنوية والشهرية 2015–2024",
        "f3t":"الموسمية",           "f3d":"ذروة الأشهر، تأثير رمضان والصيف",
        "f4t":"تحليل الإنفاق",     "f4d":"لكل رحلة، لكل ليلة، حسب الغرض",
        "f5t":"ليالي الإقامة",      "f5d":"تطور مدة الإقامة وتأثير كوفيد",
        "f6t":"توقعات الطلب",       "f6d":"Prophet ML · توقعات 2025–2026",
        "f7t":"تقسيم السياح",       "f7d":"K-Means · عالي/متوسط/اقتصادي",
        "f8t":"الأثر الكربوني",     "f8d":"مؤشر CO₂ ومقاييس الاستدامة",
        "ml_title":"نماذج التعلم الآلي",
        "ml_sub":"جاهزة للإنتاج · مدرّبة على 10 سنوات من بيانات سعودية رسمية",
        "m1n":"Prophet",          "m1t":"توقع الطلب",      "m1d":"توقعات 24 شهرًا مع فترات الثقة",
        "m2n":"K-Means",          "m2t":"تقسيم السياح",   "m2d":"3 شرائح · معامل Silhouette 0.630",
        "m3n":"Gradient Boosting","m3t":"توقع الإنفاق",   "m3d":"R² = 0.986 · MAE: 184 ريال/رحلة",
        "ins_title":"أبرز الاستنتاجات",
        "i1":"الترفيه تجاوز الديني كأول غرض في 2024 — إنجاز رؤية 2030 ✅",
        "i2":"متوسط إقامة الوافد: 8.6 → 19.2 ليلة (2021→2024) · +123%",
        "i3":"الوافدون ينفقون 4 أضعاف المحليين (5,622 مقابل 1,336 ريال)",
        "i4":"رقم قياسي 2024: 115.9M سائح · تعافي +150% من أدنى مستوى كوفيد",
        "data_src":"مصدر البيانات","data_val":"داتا السعودية · وزارة الاقتصاد والتخطيط",
        "coverage":"التغطية","cov_val":"2015–2024 · 11 مجموعة · 3,210 سجل",
        "built_by":"من تطوير","open_src":"مفتوح المصدر",
        "lang_btn":"🌐 English","dark_btn":"🌙 داكن","light_btn":"☀️ فاتح",
        "nav_lbl":"التنقل",
        "p1":"🏠 نظرة عامة","p2":"📈 اتجاهات السياحة","p3":"📅 الموسمية","p4":"💰 الإنفاق",
        "p5":"🏨 ليالي الإقامة","p6":"🔮 التوقعات","p7":"🎯 تقسيم السياح","p8":"🌱 الأثر الكربوني",
        "footer":"© 2025 ذكاء السياحة السعودية · م. جودة عماد · جميع الحقوق محفوظة",
    }
}
t = T[lang]

# ══════════════════════════════════════════
# THEME — extracted from logo & hero palette
# ══════════════════════════════════════════
if theme == "dark":
    BG_MAIN   = "#002B1E"   # deepest green (logo bg)
    BG_CARD   = "#003D2B"   # card green
    BG_CARD2  = "#004D35"   # lighter card
    BG_SIDEBAR= "#001F16"   # sidebar dark
    TXT_PRI   = "#FFFFFF"
    TXT_SEC   = "#A8D5C0"
    GOLD      = "#C9A84C"   # from logo text
    GOLD2     = "#E8C96A"   # lighter gold
    TEAL      = "#00E5A0"   # glow from logo
    TEAL2     = "#00BFA5"
    GREEN_LT  = "#4CAF7D"
    BORDER    = "#005C3F"
    GLOW      = "#00E5A033"
    HERO_OVL  = "#001F16CC"
    CHART_BG  = "rgba(0,43,30,0)"
else:
    BG_MAIN   = "#F0FAF5"
    BG_CARD   = "#FFFFFF"
    BG_CARD2  = "#E8F5EE"
    BG_SIDEBAR= "#FFFFFF"
    TXT_PRI   = "#001F16"
    TXT_SEC   = "#2E7D5A"
    GOLD      = "#A67C00"
    GOLD2     = "#C9A84C"
    TEAL      = "#007A5C"
    TEAL2     = "#009973"
    GREEN_LT  = "#2E7D5A"
    BORDER    = "#B2DFCC"
    GLOW      = "#00BFA518"
    HERO_OVL  = "#E8F5EECC"
    CHART_BG  = "rgba(240,250,245,0)"

dir_attr = "rtl" if lang=="AR" else "ltr"
font_fam  = "Tajawal" if lang=="AR" else "Sora"

# ══════════════════════════════════════════
# LOAD IMAGES
# ══════════════════════════════════════════
def img_to_b64(path):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full = os.path.join(base_dir, path)
        with open(full, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

hero_b64 = img_to_b64("assets/hero.png")
logo_b64 = img_to_b64("assets/logo.png")

hero_css_bg = f"url('data:image/png;base64,{hero_b64}')" if hero_b64 else "none"
logo_html   = f"<img src='data:image/png;base64,{logo_b64}' style='width:100%;border-radius:12px;margin-bottom:6px;' />" if logo_b64 else "<div style='text-align:center;font-size:2rem;'>🇸🇦</div>"

# ══════════════════════════════════════════
# CSS
# ══════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800;900&family=IBM+Plex+Mono:wght@400;600;700&family=Tajawal:wght@300;400;700;800;900&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {{
  background: {BG_MAIN} !important;
  font-family: '{font_fam}', sans-serif;
  direction: {dir_attr};
}}

[data-testid="stSidebar"] {{
  background: {BG_SIDEBAR} !important;
  border-right: 1px solid {BORDER};
}}
[data-testid="stSidebar"] * {{ color: {TXT_PRI} !important; }}

/* ─── HERO ─────────────────────────────── */
.hero {{
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  min-height: 440px;
  display: flex;
  align-items: center;
  margin-bottom: 28px;
  background-image: {hero_css_bg};
  background-size: cover;
  background-position: center top;
}}
.hero-overlay {{
  position: absolute; inset: 0;
  background: linear-gradient(
    100deg,
    {HERO_OVL} 0%,
    {BG_MAIN}BB 45%,
    transparent 100%
  );
}}
.hero-body {{
  position: relative; z-index: 2;
  padding: 52px 56px;
  max-width: 660px;
}}
.hero-pill {{
  display: inline-block;
  background: {GOLD}22;
  border: 1px solid {GOLD}88;
  color: {GOLD2};
  font-size: 0.64rem;
  font-weight: 700;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  padding: 5px 16px;
  border-radius: 30px;
  margin-bottom: 20px;
}}
.hero-h1 {{
  font-size: 3rem;
  font-weight: 900;
  color: {TXT_PRI};
  line-height: 1.08;
  margin: 0 0 6px 0;
  letter-spacing: -0.5px;
}}
.hero-h1 .gold {{ color: {GOLD2}; }}
.hero-h2 {{
  font-size: 3rem;
  font-weight: 900;
  color: {TEAL};
  line-height: 1.08;
  margin: 0 0 18px 0;
  letter-spacing: -0.5px;
}}
.hero-sub {{
  font-size: 0.9rem;
  color: {TXT_SEC};
  line-height: 1.65;
  margin-bottom: 28px;
}}
.hero-btn {{
  display: inline-block;
  background: linear-gradient(135deg, {GOLD}, {GOLD2});
  color: {BG_MAIN} !important;
  font-size: 0.88rem;
  font-weight: 800;
  padding: 13px 30px;
  border-radius: 30px;
  text-decoration: none;
  letter-spacing: 0.3px;
  box-shadow: 0 4px 20px {GOLD}55;
  transition: all 0.25s;
}}
.hero-btn:hover {{
  transform: translateY(-2px);
  box-shadow: 0 8px 32px {GOLD}88;
}}

/* ─── STAT BAR ─────────────────────────── */
.stats {{
  display: grid;
  grid-template-columns: repeat(4,1fr);
  gap: 14px;
  margin-bottom: 32px;
}}
.stat {{
  background: {BG_CARD};
  border: 1px solid {BORDER};
  border-bottom: 3px solid {GOLD};
  border-radius: 16px;
  padding: 22px 16px;
  text-align: center;
  transition: transform .2s, box-shadow .2s;
}}
.stat:hover {{
  transform: translateY(-3px);
  box-shadow: 0 8px 28px {GLOW};
}}
.stat-v {{
  font-size: 1.75rem;
  font-weight: 900;
  color: {GOLD2};
  font-family: 'IBM Plex Mono', monospace;
  line-height: 1.1;
}}
.stat-l {{
  font-size: 0.68rem;
  color: {TXT_SEC};
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.9px;
  margin-top: 5px;
}}

/* ─── SECTION HEADER ───────────────────── */
.sec-head {{
  margin: 0 0 20px 0;
}}
.sec-head h2 {{
  font-size: 1.45rem;
  font-weight: 800;
  color: {TXT_PRI};
  margin: 0 0 5px 0;
}}
.sec-head p {{
  font-size: 0.8rem;
  color: {TXT_SEC};
  margin: 0;
}}

/* ─── DIVIDER ──────────────────────────── */
.divider {{
  height: 1px;
  background: linear-gradient(90deg,
    transparent, {GOLD}66, {TEAL}66, transparent);
  margin: 28px 0;
}}

/* ─── FEATURE GRID ─────────────────────── */
.feat-grid {{
  display: grid;
  grid-template-columns: repeat(4,1fr);
  gap: 14px;
  margin-bottom: 32px;
}}
.feat {{
  background: {BG_CARD};
  border: 1px solid {BORDER};
  border-radius: 14px;
  padding: 20px 18px;
  transition: transform .2s, border-color .2s, box-shadow .2s;
}}
.feat:hover {{
  transform: translateY(-3px);
  border-color: {GOLD}88;
  box-shadow: 0 6px 24px {GOLD}22;
}}
.feat-ico {{ font-size: 1.6rem; margin-bottom: 10px; }}
.feat-t {{
  font-size: 0.87rem;
  font-weight: 700;
  color: {TXT_PRI};
  margin-bottom: 5px;
}}
.feat-d {{
  font-size: 0.74rem;
  color: {TXT_SEC};
  line-height: 1.5;
}}

/* ─── ML CARDS ─────────────────────────── */
.ml-grid {{
  display: grid;
  grid-template-columns: repeat(3,1fr);
  gap: 16px;
  margin-bottom: 32px;
}}
.ml-card {{
  background: {BG_CARD};
  border: 1px solid {BORDER};
  border-radius: 16px;
  padding: 26px 22px;
  position: relative;
  overflow: hidden;
  transition: transform .2s;
}}
.ml-card:hover {{ transform: translateY(-3px); }}
.ml-card::before {{
  content:'';
  position:absolute; top:0; left:0; right:0; height:3px;
}}
.ml-1::before {{ background: linear-gradient(90deg,{GOLD},{GOLD2}); }}
.ml-2::before {{ background: linear-gradient(90deg,{TEAL},{TEAL2}); }}
.ml-3::before {{ background: linear-gradient(90deg,{GOLD2},{TEAL}); }}
.ml-glow {{
  position:absolute; top:-50px; right:-50px;
  width:130px; height:130px;
  border-radius:50%; opacity:.07;
}}
.ml-name {{
  font-size: 1.05rem;
  font-weight: 800;
  color: {TXT_PRI};
  font-family: 'IBM Plex Mono', monospace;
  margin-bottom: 4px;
}}
.ml-type {{
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  margin-bottom: 12px;
}}
.ml-desc {{
  font-size: 0.82rem;
  color: {TXT_SEC};
  line-height: 1.6;
}}

/* ─── INSIGHT GRID ─────────────────────── */
.ins-grid {{
  display: grid;
  grid-template-columns: repeat(2,1fr);
  gap: 12px;
  margin-bottom: 32px;
}}
.ins-card {{
  background: {BG_CARD};
  border: 1px solid {BORDER};
  border-radius: 13px;
  padding: 16px 18px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  transition: transform .2s;
}}
.ins-card:hover {{ transform: translateX(4px); }}
.ins-ico {{ font-size: 1.25rem; flex-shrink:0; margin-top:1px; }}
.ins-txt {{
  font-size: 0.84rem;
  color: {TXT_PRI};
  line-height: 1.55;
}}

/* ─── DATA STRIP ───────────────────────── */
.data-strip {{
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 28px;
}}
.dbadge {{
  background: {BG_CARD};
  border: 1px solid {BORDER};
  border-radius: 10px;
  padding: 9px 16px;
  font-size: 0.77rem;
  color: {TXT_PRI};
  font-weight: 600;
}}
.dbadge b {{ color: {GOLD2}; }}

/* ─── FOOTER ───────────────────────────── */
.footer {{
  background: {BG_CARD};
  border: 1px solid {BORDER};
  border-top: 3px solid {GOLD};
  border-radius: 16px;
  padding: 22px 28px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}}
.footer-brand {{
  font-size: 0.9rem;
  font-weight: 800;
  color: {GOLD2};
}}
.footer-sub {{
  font-size: 0.7rem;
  color: {TXT_SEC};
  margin-top: 3px;
}}
.footer-links {{ display:flex; gap:14px; }}
.flink {{
  font-size: 0.78rem;
  color: {TXT_SEC};
  text-decoration: none;
  font-weight: 600;
}}
.flink:hover {{ color:{GOLD2}; }}

/* ─── SIDEBAR BUTTONS ──────────────────── */
.stButton button {{
  background: {BG_CARD2} !important;
  border: 1px solid {BORDER} !important;
  color: {TXT_PRI} !important;
  border-radius: 10px !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
}}
.stButton button:hover {{
  border-color: {GOLD} !important;
  color: {GOLD2} !important;
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════
with st.sidebar:
    st.markdown(logo_html, unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align:center;margin-bottom:4px;'>
      <div style='font-size:0.82rem;font-weight:800;color:{GOLD2};'>{t['nav_title']}</div>
      <div style='font-size:0.64rem;color:{TXT_SEC};letter-spacing:.5px;'>{t['nav_sub']}</div>
    </div>""", unsafe_allow_html=True)

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button(t["light_btn"] if theme=="dark" else t["dark_btn"], use_container_width=True):
            st.session_state.theme = "light" if theme=="dark" else "dark"
            st.rerun()
    with c2:
        if st.button(t["lang_btn"], use_container_width=True):
            st.session_state.lang = "AR" if lang=="EN" else "EN"
            st.rerun()

    st.divider()
    st.markdown(f"<div style='font-size:.7rem;font-weight:700;color:{TXT_SEC};text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>{t['nav_lbl']}</div>", unsafe_allow_html=True)

    pages     = ["p1","p2","p3","p4","p5","p6","p7","p8"]
    pg_colors = [TEAL, TEAL, GOLD, GOLD, TEAL2, GOLD2, TEAL, GREEN_LT]
    for pk, pc in zip(pages, pg_colors):
        st.markdown(f"""
        <div style='padding:8px 12px;border-radius:10px;
             background:{pc}12;border-left:3px solid {pc}66;
             font-size:.82rem;color:{TXT_PRI};margin-bottom:4px;
             font-weight:500;'>
          {t[pk]}
        </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown(f"""
    <div style='background:{BG_CARD2};border:1px solid {BORDER};
         border-radius:12px;padding:14px;'>
      <div style='font-size:.67rem;font-weight:700;color:{TXT_SEC};
           text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;'>
        {t['built_by']}
      </div>
      <div style='font-size:.9rem;font-weight:800;color:{GOLD2};margin-bottom:9px;'>
        Eng. Goda Emad
      </div>
      <div style='display:flex;gap:8px;'>
        <a href='https://github.com/Goda-Emad/Saudi-Tourism-Intelligence'
           target='_blank'
           style='background:{BORDER};color:{TXT_PRI};font-size:.71rem;
                  font-weight:700;padding:5px 10px;border-radius:8px;
                  text-decoration:none;'>🐙 GitHub</a>
        <a href='https://www.linkedin.com/in/goda-emad/'
           target='_blank'
           style='background:{TEAL}22;color:{TEAL};font-size:.71rem;
                  font-weight:700;padding:5px 10px;border-radius:8px;
                  text-decoration:none;'>💼 LinkedIn</a>
      </div>
    </div>
    <div style='margin-top:8px;font-size:.65rem;color:{TXT_SEC};text-align:center;'>
      {t['data_src']}: {t['data_val']}
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# HERO
# ══════════════════════════════════════════
st.markdown(f"""
<div class='hero'>
  <div class='hero-overlay'></div>
  <div class='hero-body'>
    <div class='hero-pill'>{t['hero_tag']}</div>
    <div class='hero-h1'>{t['hero_title_1']}</div>
    <div class='hero-h2'>{t['hero_title_2']}</div>
    <p class='hero-sub'>{t['hero_sub']}</p>
    <a class='hero-btn' href='#'>{t['hero_btn']}</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# STATS
# ══════════════════════════════════════════
st.markdown(f"""
<div class='stats'>
  <div class='stat'><div class='stat-v'>{t['stat1_v']}</div><div class='stat-l'>{t['stat1_l']}</div></div>
  <div class='stat'><div class='stat-v'>{t['stat2_v']}</div><div class='stat-l'>{t['stat2_l']}</div></div>
  <div class='stat'><div class='stat-v'>{t['stat3_v']}</div><div class='stat-l'>{t['stat3_l']}</div></div>
  <div class='stat'><div class='stat-v'>{t['stat4_v']}</div><div class='stat-l'>{t['stat4_l']}</div></div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# FEATURES
# ══════════════════════════════════════════
st.markdown(f"""
<div class='sec-head'><h2>{t['feat_title']}</h2><p>{t['feat_sub']}</p></div>
<div class='feat-grid'>
  <div class='feat'><div class='feat-ico'>🏠</div><div class='feat-t'>{t['f1t']}</div><div class='feat-d'>{t['f1d']}</div></div>
  <div class='feat'><div class='feat-ico'>📈</div><div class='feat-t'>{t['f2t']}</div><div class='feat-d'>{t['f2d']}</div></div>
  <div class='feat'><div class='feat-ico'>📅</div><div class='feat-t'>{t['f3t']}</div><div class='feat-d'>{t['f3d']}</div></div>
  <div class='feat'><div class='feat-ico'>💰</div><div class='feat-t'>{t['f4t']}</div><div class='feat-d'>{t['f4d']}</div></div>
  <div class='feat'><div class='feat-ico'>🏨</div><div class='feat-t'>{t['f5t']}</div><div class='feat-d'>{t['f5d']}</div></div>
  <div class='feat'><div class='feat-ico'>🔮</div><div class='feat-t'>{t['f6t']}</div><div class='feat-d'>{t['f6d']}</div></div>
  <div class='feat'><div class='feat-ico'>🎯</div><div class='feat-t'>{t['f7t']}</div><div class='feat-d'>{t['f7d']}</div></div>
  <div class='feat'><div class='feat-ico'>🌱</div><div class='feat-t'>{t['f8t']}</div><div class='feat-d'>{t['f8d']}</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# ML MODELS
# ══════════════════════════════════════════
st.markdown(f"""
<div class='sec-head'><h2>{t['ml_title']}</h2><p>{t['ml_sub']}</p></div>
<div class='ml-grid'>
  <div class='ml-card ml-1'>
    <div class='ml-glow' style='background:{GOLD};'></div>
    <div class='ml-name'>🔮 {t['m1n']}</div>
    <div class='ml-type' style='color:{GOLD2};'>{t['m1t']}</div>
    <div class='ml-desc'>{t['m1d']}</div>
  </div>
  <div class='ml-card ml-2'>
    <div class='ml-glow' style='background:{TEAL};'></div>
    <div class='ml-name'>🎯 {t['m2n']}</div>
    <div class='ml-type' style='color:{TEAL};'>{t['m2t']}</div>
    <div class='ml-desc'>{t['m2d']}</div>
  </div>
  <div class='ml-card ml-3'>
    <div class='ml-glow' style='background:{GOLD2};'></div>
    <div class='ml-name'>💰 {t['m3n']}</div>
    <div class='ml-type' style='color:{GOLD2};'>{t['m3t']}</div>
    <div class='ml-desc'>{t['m3d']}</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# KEY INSIGHTS
# ══════════════════════════════════════════
ins = [
    ("🏖️", t["i1"], GOLD),
    ("⏰", t["i2"], TEAL),
    ("💰", t["i3"], GOLD2),
    ("🚀", t["i4"], TEAL2),
]
st.markdown(f"<div class='sec-head'><h2>{t['ins_title']}</h2></div>", unsafe_allow_html=True)
st.markdown("<div class='ins-grid'>", unsafe_allow_html=True)
for ico, txt, col in ins:
    st.markdown(f"""
    <div class='ins-card' style='border-left:3px solid {col};'>
      <div class='ins-ico'>{ico}</div>
      <div class='ins-txt'>{txt}</div>
    </div>""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# DATA BADGES
# ══════════════════════════════════════════
st.markdown(f"""
<div class='data-strip'>
  <div class='dbadge'><b>📦</b> {t['data_src']}: {t['data_val']}</div>
  <div class='dbadge'><b>📅</b> {t['coverage']}: {t['cov_val']}</div>
  <div class='dbadge'><b>🐙</b> {t['open_src']}: github.com/Goda-Emad</div>
  <div class='dbadge'><b>🐍</b> Python · Streamlit · Plotly · Prophet · Scikit-learn</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════
st.markdown(f"""
<div class='footer'>
  <div>
    <div class='footer-brand'>🇸🇦 {t['nav_title']}</div>
    <div class='footer-sub'>{t['footer']}</div>
  </div>
  <div class='footer-links'>
    <a class='flink' href='https://github.com/Goda-Emad/Saudi-Tourism-Intelligence' target='_blank'>🐙 GitHub</a>
    <a class='flink' href='https://www.linkedin.com/in/goda-emad/' target='_blank'>💼 LinkedIn</a>
    <a class='flink' href='https://datasaudi.sa' target='_blank'>📊 DataSaudi</a>
  </div>
</div>
""", unsafe_allow_html=True)
