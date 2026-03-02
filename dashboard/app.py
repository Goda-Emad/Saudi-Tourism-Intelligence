import streamlit as st

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

T = {
    "EN": {
        "nav_title":      "Saudi Tourism Intelligence",
        "nav_sub":        "Vision 2030 · AI Analytics Platform",
        "hero_tag":       "🇸🇦 OFFICIAL DATA · MINISTRY OF ECONOMY & PLANNING",
        "hero_title":     "Saudi Tourism\nIntelligence",
        "hero_subtitle":  "AI-Powered Analytics Platform · 10 Years of Data · 3 ML Models",
        "hero_btn":       "Explore Dashboard →",
        "stat1_val":      "115.8M",  "stat1_lbl": "Tourists 2024",
        "stat2_val":      "1.1B",    "stat2_lbl": "Overnight Stays",
        "stat3_val":      "SAR 5,622","stat3_lbl": "Avg Inbound Spend",
        "stat4_val":      "R²=0.986","stat4_lbl": "ML Model Accuracy",
        "features_title": "What's Inside",
        "features_sub":   "8 interactive pages · Real government data · 3 production ML models",
        "f1_title": "Tourist Trends",     "f1_desc": "Annual & monthly patterns 2015–2024",
        "f2_title": "Seasonality",        "f2_desc": "Peak months, Ramadan & summer effects",
        "f3_title": "Spending Analysis",  "f3_desc": "Per trip, per night, by purpose breakdown",
        "f4_title": "Overnight Stays",    "f4_desc": "Length of stay evolution & COVID impact",
        "f5_title": "Demand Forecasting", "f5_desc": "Prophet ML · 2025–2026 predictions",
        "f6_title": "Segmentation",       "f6_desc": "K-Means · High / Mid / Budget segments",
        "f7_title": "Carbon Impact",      "f7_desc": "CO₂ index & sustainability metrics",
        "f8_title": "Executive Overview", "f8_desc": "KPIs, trends & key insights at a glance",
        "models_title":   "Machine Learning Models",
        "m1_name": "Prophet", "m1_type": "Demand Forecasting",
        "m1_desc": "24-month predictions with confidence intervals",
        "m2_name": "K-Means", "m2_type": "Tourist Segmentation",
        "m2_desc": "3 value segments · Silhouette Score 0.630",
        "m3_name": "Gradient Boosting", "m3_type": "Spending Prediction",
        "m3_desc": "R² = 0.986 · MAE: SAR 184/trip",
        "insights_title": "Key Insights",
        "i1": "Leisure tourism overtook Religious as #1 purpose in 2024 — Vision 2030 milestone ✅",
        "i2": "Inbound avg stay: 8.6 nights (2021) → 19.2 nights (2024) · +123% growth",
        "i3": "Inbound tourists spend 4× more than Domestic (SAR 5,622 vs SAR 1,336)",
        "i4": "2024 all-time record: 115.9M tourists · +150% recovery from COVID low",
        "built_by":   "Built by",
        "data_src":   "Data Source",
        "data_val":   "DataSaudi · Ministry of Economy & Planning",
        "coverage":   "Coverage",
        "coverage_v": "2015 – 2024 · 11 Datasets · 3,210 Records",
        "open_src":   "Open Source",
        "lang_toggle":"🌐 العربية",
        "dark_mode":  "🌙 Dark",
        "light_mode": "☀️ Light",
        "pages":      "Navigation",
        "p1": "🏠 Overview",      "p2": "📈 Tourist Trends",
        "p3": "📅 Seasonality",   "p4": "💰 Spending",
        "p5": "🏨 Overnight Stays","p6": "🔮 Forecasting",
        "p7": "🎯 Segmentation",  "p8": "🌱 Carbon Impact",
        "footer_copy": "© 2025 Saudi Tourism Intelligence · Eng. Goda Emad · All rights reserved",
    },
    "AR": {
        "nav_title":      "ذكاء السياحة السعودية",
        "nav_sub":        "رؤية 2030 · منصة تحليلات الذكاء الاصطناعي",
        "hero_tag":       "🇸🇦 بيانات رسمية · وزارة الاقتصاد والتخطيط",
        "hero_title":     "ذكاء السياحة\nالسعودية",
        "hero_subtitle":  "منصة تحليلات مدعومة بالذكاء الاصطناعي · 10 سنوات من البيانات · 3 نماذج ML",
        "hero_btn":       "استكشف لوحة التحكم ←",
        "stat1_val":      "115.8M",   "stat1_lbl": "سائح 2024",
        "stat2_val":      "1.1B",     "stat2_lbl": "ليالي الإقامة",
        "stat3_val":      "5,622 ر",  "stat3_lbl": "متوسط إنفاق الوافد",
        "stat4_val":      "R²=0.986", "stat4_lbl": "دقة النموذج",
        "features_title": "ما بداخله",
        "features_sub":   "8 صفحات تفاعلية · بيانات حكومية حقيقية · 3 نماذج ML جاهزة للإنتاج",
        "f1_title": "اتجاهات السياحة",    "f1_desc": "الأنماط السنوية والشهرية 2015–2024",
        "f2_title": "الموسمية",            "f2_desc": "ذروة الأشهر، تأثير رمضان والصيف",
        "f3_title": "تحليل الإنفاق",      "f3_desc": "لكل رحلة، لكل ليلة، حسب الغرض",
        "f4_title": "ليالي الإقامة",       "f4_desc": "تطور مدة الإقامة وتأثير كوفيد",
        "f5_title": "توقعات الطلب",        "f5_desc": "Prophet ML · توقعات 2025–2026",
        "f6_title": "تقسيم السياح",        "f6_desc": "K-Means · شرائح عالي/متوسط/اقتصادي",
        "f7_title": "الأثر الكربوني",      "f7_desc": "مؤشر CO₂ ومقاييس الاستدامة",
        "f8_title": "النظرة التنفيذية",    "f8_desc": "مؤشرات الأداء والاتجاهات بلمحة واحدة",
        "models_title":   "نماذج التعلم الآلي",
        "m1_name": "Prophet",         "m1_type": "توقع الطلب",
        "m1_desc": "توقعات 24 شهرًا مع فترات الثقة",
        "m2_name": "K-Means",         "m2_type": "تقسيم السياح",
        "m2_desc": "3 شرائح · معامل Silhouette 0.630",
        "m3_name": "Gradient Boosting","m3_type": "توقع الإنفاق",
        "m3_desc": "R² = 0.986 · MAE: 184 ريال/رحلة",
        "insights_title": "أبرز الاستنتاجات",
        "i1": "الترفيه تجاوز الديني كأول غرض سياحي في 2024 — إنجاز رؤية 2030 ✅",
        "i2": "متوسط إقامة الوافد: 8.6 ليلة (2021) → 19.2 ليلة (2024) · نمو +123%",
        "i3": "الوافدون ينفقون 4 أضعاف المحليين (5,622 مقابل 1,336 ريال)",
        "i4": "رقم قياسي 2024: 115.9M سائح · تعافي +150% من أدنى مستوى كوفيد",
        "built_by":   "من تطوير",
        "data_src":   "مصدر البيانات",
        "data_val":   "داتا السعودية · وزارة الاقتصاد والتخطيط",
        "coverage":   "التغطية",
        "coverage_v": "2015 – 2024 · 11 مجموعة بيانات · 3,210 سجل",
        "open_src":   "مفتوح المصدر",
        "lang_toggle":"🌐 English",
        "dark_mode":  "🌙 داكن",
        "light_mode": "☀️ فاتح",
        "pages":      "التنقل",
        "p1": "🏠 نظرة عامة",       "p2": "📈 اتجاهات السياحة",
        "p3": "📅 الموسمية",         "p4": "💰 الإنفاق",
        "p5": "🏨 ليالي الإقامة",    "p6": "🔮 التوقعات",
        "p7": "🎯 تقسيم السياح",     "p8": "🌱 الأثر الكربوني",
        "footer_copy": "© 2025 ذكاء السياحة السعودية · م. جودة عماد · جميع الحقوق محفوظة",
    }
}
t = T[lang]

# ═══════════════════════════════════════
# THEME PALETTE
# ═══════════════════════════════════════
if theme == "dark":
    bg_main        = "#0A1A0F"
    bg_card        = "#0F2318"
    bg_card2       = "#0D1E14"
    bg_hero        = "#081510"
    text_primary   = "#E8F5E9"
    text_secondary = "#81C784"
    accent_green   = "#00E676"
    accent_teal    = "#00BFA5"
    accent_gold    = "#FFD54F"
    accent_blue    = "#40C4FF"
    accent_lime    = "#B2FF59"
    accent_red     = "#FF5252"
    border_color   = "#1B3A22"
    glow_green     = "#00E67633"
    chart_bg       = "rgba(10,26,15,0)"
    plotly_tmpl    = "plotly_dark"
else:
    bg_main        = "#F1F8F2"
    bg_card        = "#FFFFFF"
    bg_card2       = "#E8F5E9"
    bg_hero        = "#E0F2E9"
    text_primary   = "#1B3A22"
    text_secondary = "#388E3C"
    accent_green   = "#2E7D32"
    accent_teal    = "#00695C"
    accent_gold    = "#F57F17"
    accent_blue    = "#0277BD"
    accent_lime    = "#558B2F"
    accent_red     = "#C62828"
    border_color   = "#C8E6C9"
    glow_green     = "#2E7D3218"
    chart_bg       = "rgba(241,248,242,0)"
    plotly_tmpl    = "plotly_white"

dir_attr = 'rtl' if lang == "AR" else 'ltr'
font_family = 'Tajawal' if lang == "AR" else 'Sora'

# ═══════════════════════════════════════
# CSS
# ═══════════════════════════════════════
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800;900&family=IBM+Plex+Mono:wght@400;600;700&family=Tajawal:wght@300;400;700;800;900&display=swap');

  * {{ box-sizing: border-box; }}

  html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
    background-color: {bg_main} !important;
    font-family: '{font_family}', sans-serif;
    direction: {dir_attr};
  }}

  [data-testid="stSidebar"] {{
    background: {bg_card} !important;
    border-right: 1px solid {border_color};
  }}
  [data-testid="stSidebar"] * {{ color: {text_primary} !important; }}

  /* ── HERO ─────────────────────────────── */
  .hero-wrap {{
    position: relative;
    border-radius: 24px;
    overflow: hidden;
    margin-bottom: 32px;
    min-height: 420px;
    display: flex;
    align-items: center;
  }}
  .hero-img {{
    position: absolute;
    inset: 0;
    width: 100%; height: 100%;
    object-fit: cover;
    opacity: 0.30;
    border-radius: 24px;
  }}
  .hero-overlay {{
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg,
      {bg_hero}EE 0%,
      {bg_card}99 50%,
      transparent 100%);
    border-radius: 24px;
  }}
  .hero-content {{
    position: relative;
    z-index: 2;
    padding: 48px 52px;
    max-width: 680px;
  }}
  .hero-tag {{
    display: inline-block;
    background: {accent_green}22;
    border: 1px solid {accent_green}66;
    color: {accent_green};
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 18px;
  }}
  .hero-title {{
    font-size: 3.2rem;
    font-weight: 900;
    color: {text_primary};
    line-height: 1.1;
    margin: 0 0 14px 0;
    letter-spacing: -1px;
  }}
  .hero-title span {{ color: {accent_green}; }}
  .hero-sub {{
    font-size: 1rem;
    color: {text_secondary};
    font-weight: 400;
    margin-bottom: 28px;
    line-height: 1.6;
  }}
  .hero-btn {{
    display: inline-block;
    background: linear-gradient(135deg, {accent_green}, {accent_teal});
    color: #000 !important;
    font-size: 0.88rem;
    font-weight: 800;
    padding: 12px 28px;
    border-radius: 30px;
    text-decoration: none;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 24px {accent_green}44;
    transition: transform 0.2s, box-shadow 0.2s;
  }}
  .hero-btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 32px {accent_green}66;
  }}

  /* ── STAT BAR ─────────────────────────── */
  .stat-bar {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 32px;
  }}
  .stat-card {{
    background: {bg_card};
    border: 1px solid {border_color};
    border-bottom: 3px solid {accent_green};
    border-radius: 14px;
    padding: 20px 16px;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
  }}
  .stat-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 8px 28px {glow_green};
  }}
  .stat-val {{
    font-size: 1.7rem;
    font-weight: 900;
    color: {accent_green};
    font-family: 'IBM Plex Mono', monospace;
    line-height: 1.1;
  }}
  .stat-lbl {{
    font-size: 0.7rem;
    color: {text_secondary};
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 5px;
  }}

  /* ── SECTION TITLE ────────────────────── */
  .sec-title {{
    font-size: 1.4rem;
    font-weight: 800;
    color: {text_primary};
    margin: 0 0 6px 0;
  }}
  .sec-sub {{
    font-size: 0.82rem;
    color: {text_secondary};
    margin-bottom: 20px;
  }}

  /* ── FEATURE CARDS ───────────────────── */
  .feat-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 32px;
  }}
  .feat-card {{
    background: {bg_card};
    border: 1px solid {border_color};
    border-radius: 14px;
    padding: 20px 16px;
    transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
    cursor: default;
  }}
  .feat-card:hover {{
    transform: translateY(-3px);
    border-color: {accent_green}88;
    box-shadow: 0 6px 24px {glow_green};
  }}
  .feat-icon {{ font-size: 1.6rem; margin-bottom: 10px; }}
  .feat-title {{
    font-size: 0.88rem;
    font-weight: 700;
    color: {text_primary};
    margin-bottom: 6px;
  }}
  .feat-desc {{
    font-size: 0.75rem;
    color: {text_secondary};
    line-height: 1.5;
  }}

  /* ── ML MODEL CARDS ──────────────────── */
  .model-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 32px;
  }}
  .model-card {{
    background: {bg_card};
    border: 1px solid {border_color};
    border-radius: 16px;
    padding: 24px 20px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
  }}
  .model-card:hover {{ transform: translateY(-3px); }}
  .model-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
  }}
  .model-card-1::before {{ background: linear-gradient(90deg, {accent_green}, {accent_teal}); }}
  .model-card-2::before {{ background: linear-gradient(90deg, {accent_teal}, {accent_blue}); }}
  .model-card-3::before {{ background: linear-gradient(90deg, {accent_gold}, {accent_green}); }}
  .model-glow {{
    position: absolute;
    top: -40px; right: -40px;
    width: 120px; height: 120px;
    border-radius: 50%;
    opacity: 0.06;
  }}
  .model-name {{
    font-size: 1.1rem;
    font-weight: 800;
    color: {text_primary};
    margin-bottom: 3px;
    font-family: 'IBM Plex Mono', monospace;
  }}
  .model-type {{
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
  }}
  .model-desc {{
    font-size: 0.82rem;
    color: {text_secondary};
    line-height: 1.6;
  }}

  /* ── INSIGHTS ────────────────────────── */
  .insight-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin-bottom: 32px;
  }}
  .insight-card {{
    background: {bg_card};
    border: 1px solid {border_color};
    border-radius: 12px;
    padding: 16px 18px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    transition: transform 0.2s;
  }}
  .insight-card:hover {{ transform: translateX(4px); }}
  .insight-icon {{ font-size: 1.2rem; flex-shrink: 0; margin-top: 2px; }}
  .insight-text {{ font-size: 0.85rem; color: {text_primary}; line-height: 1.55; }}

  /* ── FOOTER ──────────────────────────── */
  .footer {{
    background: {bg_card};
    border: 1px solid {border_color};
    border-top: 3px solid {accent_green};
    border-radius: 16px;
    padding: 24px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 14px;
    margin-top: 16px;
  }}
  .footer-brand {{
    font-size: 0.88rem;
    font-weight: 800;
    color: {accent_green};
  }}
  .footer-sub {{
    font-size: 0.72rem;
    color: {text_secondary};
    margin-top: 3px;
  }}
  .footer-links {{ display: flex; gap: 16px; align-items: center; }}
  .footer-link {{
    font-size: 0.78rem;
    color: {text_secondary};
    text-decoration: none;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .footer-link:hover {{ color: {accent_green}; }}

  /* ── DATA BADGE ──────────────────────── */
  .data-badge {{
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 32px;
  }}
  .badge {{
    background: {bg_card};
    border: 1px solid {border_color};
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 0.78rem;
    color: {text_primary};
    font-weight: 600;
  }}
  .badge span {{
    color: {accent_green};
    font-weight: 700;
    margin-right: 4px;
  }}

  /* ── DIVIDER ─────────────────────────── */
  .green-divider {{
    height: 1px;
    background: linear-gradient(90deg, {accent_green}00, {accent_green}88, {accent_green}00);
    margin: 24px 0;
  }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════
with st.sidebar:
    try:
        st.image("assets/logo.png", use_column_width=True)
    except:
        st.markdown(f"<div style='text-align:center;font-size:2rem;padding:12px 0;'>🇸🇦</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='text-align:center;margin-bottom:4px;'>
      <div style='font-size:0.85rem;font-weight:800;color:{accent_green};'>{t['nav_title']}</div>
      <div style='font-size:0.65rem;color:{text_secondary};letter-spacing:0.5px;'>{t['nav_sub']}</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    # Theme + Language
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button(t["light_mode"] if theme=="dark" else t["dark_mode"],
                     use_container_width=True, key="theme_btn"):
            st.session_state.theme = "light" if theme=="dark" else "dark"
            st.rerun()
    with col_b:
        if st.button(t["lang_toggle"], use_container_width=True, key="lang_btn"):
            st.session_state.lang = "AR" if lang=="EN" else "EN"
            st.rerun()

    st.divider()

    # Navigation
    st.markdown(f"<div style='font-size:0.7rem;font-weight:700;color:{text_secondary};text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>{t['pages']}</div>", unsafe_allow_html=True)
    nav_pages = ["p1","p2","p3","p4","p5","p6","p7","p8"]
    nav_icons_color = [accent_teal, accent_blue, accent_gold, accent_gold,
                       accent_blue, accent_lime, accent_green, accent_green]
    for p, color in zip(nav_pages, nav_icons_color):
        st.markdown(f"""
        <div style='padding:8px 12px;border-radius:10px;background:{color}11;
             border-left:3px solid {color}55;font-size:0.83rem;
             color:{text_primary};margin-bottom:4px;font-weight:500;'>
          {t[p]}
        </div>""", unsafe_allow_html=True)

    st.divider()

    # Built by
    st.markdown(f"""
    <div style='background:{bg_card2};border:1px solid {border_color};border-radius:12px;padding:14px;'>
      <div style='font-size:0.68rem;font-weight:700;color:{text_secondary};text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;'>{t['built_by']}</div>
      <div style='font-size:0.88rem;font-weight:800;color:{accent_green};margin-bottom:8px;'>Eng. Goda Emad</div>
      <div style='display:flex;gap:8px;'>
        <a href='https://github.com/Goda-Emad/Saudi-Tourism-Intelligence' target='_blank'
           style='background:{border_color};color:{text_primary};font-size:0.72rem;font-weight:700;padding:5px 10px;border-radius:8px;text-decoration:none;'>🐙 GitHub</a>
        <a href='https://www.linkedin.com/in/goda-emad/' target='_blank'
           style='background:{accent_blue}22;color:{accent_blue};font-size:0.72rem;font-weight:700;padding:5px 10px;border-radius:8px;text-decoration:none;'>💼 LinkedIn</a>
      </div>
    </div>
    <div style='margin-top:10px;font-size:0.68rem;color:{text_secondary};text-align:center;'>
      {t['data_src']}: {t['data_val']}
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════
# HERO SECTION
# ═══════════════════════════════════════
try:
    import base64
    with open("assets/hero.png", "rb") as f:
        hero_b64 = base64.b64encode(f.read()).decode()
    hero_src = f"data:image/png;base64,{hero_b64}"
    hero_img_tag = f"<img src='{hero_src}' class='hero-img' />"
except:
    hero_img_tag = ""

title_parts = t['hero_title'].split('\n')
title_html = title_parts[0] + (f"<br><span>{title_parts[1]}</span>" if len(title_parts)>1 else "")

st.markdown(f"""
<div class='hero-wrap'>
  {hero_img_tag}
  <div class='hero-overlay'></div>
  <div class='hero-content'>
    <div class='hero-tag'>{t['hero_tag']}</div>
    <h1 class='hero-title'>{title_html}</h1>
    <p class='hero-sub'>{t['hero_subtitle']}</p>
    <a href='#features' class='hero-btn'>{t['hero_btn']}</a>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════
# STAT BAR
# ═══════════════════════════════════════
st.markdown(f"""
<div class='stat-bar'>
  <div class='stat-card'>
    <div class='stat-val'>{t['stat1_val']}</div>
    <div class='stat-lbl'>{t['stat1_lbl']}</div>
  </div>
  <div class='stat-card'>
    <div class='stat-val'>{t['stat2_val']}</div>
    <div class='stat-lbl'>{t['stat2_lbl']}</div>
  </div>
  <div class='stat-card'>
    <div class='stat-val'>{t['stat3_val']}</div>
    <div class='stat-lbl'>{t['stat3_lbl']}</div>
  </div>
  <div class='stat-card'>
    <div class='stat-val'>{t['stat4_val']}</div>
    <div class='stat-lbl'>{t['stat4_lbl']}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════
# FEATURES GRID
# ═══════════════════════════════════════
st.markdown(f"""
<div id='features'>
  <div class='sec-title'>{t['features_title']}</div>
  <div class='sec-sub'>{t['features_sub']}</div>
</div>
<div class='feat-grid'>
  <div class='feat-card'><div class='feat-icon'>🏠</div><div class='feat-title'>{t['f8_title']}</div><div class='feat-desc'>{t['f8_desc']}</div></div>
  <div class='feat-card'><div class='feat-icon'>📈</div><div class='feat-title'>{t['f1_title']}</div><div class='feat-desc'>{t['f1_desc']}</div></div>
  <div class='feat-card'><div class='feat-icon'>📅</div><div class='feat-title'>{t['f2_title']}</div><div class='feat-desc'>{t['f2_desc']}</div></div>
  <div class='feat-card'><div class='feat-icon'>💰</div><div class='feat-title'>{t['f3_title']}</div><div class='feat-desc'>{t['f3_desc']}</div></div>
  <div class='feat-card'><div class='feat-icon'>🏨</div><div class='feat-title'>{t['f4_title']}</div><div class='feat-desc'>{t['f4_desc']}</div></div>
  <div class='feat-card'><div class='feat-icon'>🔮</div><div class='feat-title'>{t['f5_title']}</div><div class='feat-desc'>{t['f5_desc']}</div></div>
  <div class='feat-card'><div class='feat-icon'>🎯</div><div class='feat-title'>{t['f6_title']}</div><div class='feat-desc'>{t['f6_desc']}</div></div>
  <div class='feat-card'><div class='feat-icon'>🌱</div><div class='feat-title'>{t['f7_title']}</div><div class='feat-desc'>{t['f7_desc']}</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════
# ML MODELS
# ═══════════════════════════════════════
st.markdown(f"""
<div class='sec-title'>{t['models_title']}</div>
<div class='sec-sub' style='margin-bottom:16px;'>Production-ready · Trained on official Saudi government data</div>
<div class='model-grid'>
  <div class='model-card model-card-1'>
    <div class='model-glow' style='background:{accent_green};'></div>
    <div class='model-name'>🔮 {t['m1_name']}</div>
    <div class='model-type' style='color:{accent_green};'>{t['m1_type']}</div>
    <div class='model-desc'>{t['m1_desc']}</div>
  </div>
  <div class='model-card model-card-2'>
    <div class='model-glow' style='background:{accent_teal};'></div>
    <div class='model-name'>🎯 {t['m2_name']}</div>
    <div class='model-type' style='color:{accent_teal};'>{t['m2_type']}</div>
    <div class='model-desc'>{t['m2_desc']}</div>
  </div>
  <div class='model-card model-card-3'>
    <div class='model-glow' style='background:{accent_gold};'></div>
    <div class='model-name'>💰 {t['m3_name']}</div>
    <div class='model-type' style='color:{accent_gold};'>{t['m3_type']}</div>
    <div class='model-desc'>{t['m3_desc']}</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════
# KEY INSIGHTS
# ═══════════════════════════════════════
icons  = ["🏖️","⏰","💰","🚀"]
colors = [accent_green, accent_teal, accent_gold, accent_blue]
ins_keys = ["i1","i2","i3","i4"]

st.markdown(f"<div class='sec-title'>{t['insights_title']}</div><div class='sec-sub' style='margin-bottom:16px;'>Discovered from 10 years of official Saudi tourism data</div>", unsafe_allow_html=True)

st.markdown(f"<div class='insight-grid'>", unsafe_allow_html=True)
for icon, color, key in zip(icons, colors, ins_keys):
    st.markdown(f"""
    <div class='insight-card' style='border-left:3px solid {color};'>
      <div class='insight-icon'>{icon}</div>
      <div class='insight-text'>{t[key]}</div>
    </div>""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════
# DATA BADGES
# ═══════════════════════════════════════
st.markdown(f"""
<div class='data-badge'>
  <div class='badge'><span>📦</span>{t['data_src']}: {t['data_val']}</div>
  <div class='badge'><span>📅</span>{t['coverage']}: {t['coverage_v']}</div>
  <div class='badge'><span>🐙</span>{t['open_src']}: github.com/Goda-Emad</div>
  <div class='badge'><span>🐍</span>Stack: Python · Streamlit · Plotly · Prophet · Scikit-learn</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════
st.markdown(f"""
<div class='footer'>
  <div>
    <div class='footer-brand'>🇸🇦 {t['nav_title']}</div>
    <div class='footer-sub'>{t['footer_copy']}</div>
  </div>
  <div class='footer-links'>
    <a class='footer-link' href='https://github.com/Goda-Emad/Saudi-Tourism-Intelligence' target='_blank'>
      🐙 GitHub
    </a>
    <a class='footer-link' href='https://www.linkedin.com/in/goda-emad/' target='_blank'>
      💼 LinkedIn
    </a>
    <a class='footer-link' href='https://datasaudi.sa' target='_blank'>
      📊 DataSaudi
    </a>
  </div>
</div>
""", unsafe_allow_html=True)
