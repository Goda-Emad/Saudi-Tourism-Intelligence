# ═══════════════════════════════════════════════════════════════════
#  Saudi Tourism Intelligence — Home Page
#  Author : Eng. Goda Emad
#  Design : DataSaudi Official Design System
# ═══════════════════════════════════════════════════════════════════
import streamlit as st
import streamlit.components.v1 as components
import base64, os

st.set_page_config(
    page_title="Saudi Tourism Intelligence",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

for k, v in [("lang", "EN"), ("theme", "dark")]:
    if k not in st.session_state:
        st.session_state[k] = v

LANG  = st.session_state.lang
THEME = st.session_state.theme

# ── DataSaudi Official Colors ────────────────────────────────────
C = {
    "teal":     "#17B19B",
    "teal_act": "#149581",
    "teal_sec": "#8BAFAA",
    "bg":       "#1A1E1F",
    "sec_bg":   "#161B1C",
    "dark_bg":  "#373D44",
    "navbar":   "#031414",
    "white":    "#F4F9F8",
    "grey":     "#A1A6B7",
    "foot_txt": "#B5B8B7",
    "border":   "#2A3235",
    "orange":   "#F4D044",
    "gold":     "#C9A84C",
    "blue":     "#365C8D",
} if THEME == "dark" else {
    "teal":     "#17B19B",
    "teal_act": "#149581",
    "teal_sec": "#4A8A82",
    "bg":       "#F4F9F8",
    "sec_bg":   "#E8EFEE",
    "dark_bg":  "#DDE6E4",
    "navbar":   "#FFFFFF",
    "white":    "#0D1414",
    "grey":     "#4A5568",
    "foot_txt": "#718096",
    "border":   "#C8D8D5",
    "orange":   "#C9950A",
    "gold":     "#A67C00",
    "blue":     "#365C8D",
}

def clr(k): return C.get(k, C["teal"])

# ── Cached Helpers ───────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def _read(p):
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, p), "rb") as f:
        return f.read()

@st.cache_data(show_spinner=False)
def _b64(p):
    try:    return base64.b64encode(_read(p)).decode()
    except: return ""

@st.cache_data(show_spinner=False)
def _css():
    try:    return _read("assets/style.css").decode()
    except: return ""

# ── Translations ─────────────────────────────────────────────────
TR = {
"EN": {
    "name": "Saudi Tourism Intelligence", "sub": "AI ANALYTICS PLATFORM",
    "pill": "🇸🇦  OFFICIAL DATA · MINISTRY OF ECONOMY & PLANNING",
    "h1": "Saudi Tourism", "h2": "Intelligence",
    "hs": "AI-powered analytics on 10 years of official data. Forecasting · Segmentation · Sustainability.",
    "hb": "Explore Dashboard →",
    "stats": [
        ("115.8M","Tourists 2024","teal"),
        ("1.10B", "Overnight Stays","teal"),
        ("5,622", "Avg Spend (SAR)","orange"),
        ("0.986", "ML Accuracy R²","orange"),
    ],
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
    "data": "DataSaudi · Ministry of Economy & Planning · 2015–2024",
    "copy": "© 2025 Saudi Tourism Intelligence · Eng. Goda Emad · All rights reserved",
    "lng": "AR", "thm": "☀️" if THEME=="dark" else "🌙",
},
"AR": {
    "name": "ذكاء السياحة السعودية", "sub": "منصة تحليلات الذكاء الاصطناعي",
    "pill": "🇸🇦  بيانات رسمية · وزارة الاقتصاد والتخطيط",
    "h1": "ذكاء السياحة", "h2": "السعودية",
    "hs": "تحليلات على 10 سنوات من البيانات الرسمية. توقعات · تقسيم · استدامة.",
    "hb": "← استكشف لوحة التحكم",
    "stats": [
        ("115.8M","سائح 2024","teal"),
        ("1.10B", "ليالي الإقامة","teal"),
        ("5,622", "متوسط الإنفاق (ريال)","orange"),
        ("0.986", "دقة النموذج R²","orange"),
    ],
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
    "data": "داتا السعودية · وزارة الاقتصاد والتخطيط · 2015–2024",
    "copy": "© 2025 ذكاء السياحة السعودية · م. جودة عماد · جميع الحقوق محفوظة",
    "lng": "EN", "thm": "☀️" if THEME=="dark" else "🌙",
},
}

t        = TR[LANG]
logo_b64 = _b64("assets/logo.jpg")
hero_b64 = _b64("assets/hero.jpg")
logo_src = "data:image/jpeg;base64," + logo_b64 if logo_b64 else ""
hero_src = "data:image/jpeg;base64," + hero_b64 if hero_b64 else ""
logo_img = f'<img src="{logo_src}" style="height:40px;border-radius:6px;"/>' if logo_src else "🇸🇦"
dir_val  = "rtl" if LANG == "AR" else "ltr"
font_val = "Tajawal" if LANG == "AR" else "IBM Plex Sans"

# ════════════════════════════════════════════════════════════════════
# BUILD FULL HTML PAGE — rendered via st.components (no escape bug)
# ════════════════════════════════════════════════════════════════════

# ── Stats cells ──────────────────────────────────────────────────
stats_cells = ""
for i, (val, lbl, ck) in enumerate(t["stats"]):
    br = f'border-right:1px solid {C["border"]};' if i < 3 else ""
    stats_cells += f"""
        <div style="padding:26px 24px;{br}">
          <div style="font-size:1.8rem;font-weight:700;color:{clr(ck)};
               font-family:'IBM Plex Mono',monospace;">{val}</div>
          <div style="font-size:.66rem;color:{C['grey']};text-transform:uppercase;
               letter-spacing:.9px;font-weight:500;margin-top:5px;">{lbl}</div>
        </div>"""

# ── Page cards ───────────────────────────────────────────────────
page_cards = ""
for ico, title, desc in t["pages"]:
    page_cards += f"""
        <div class="card hover-card">
          <div style="font-size:1.5rem;margin-bottom:10px;">{ico}</div>
          <div style="font-size:.87rem;font-weight:600;color:{C['white']};
               margin-bottom:5px;">{title}</div>
          <div style="font-size:.73rem;color:{C['grey']};line-height:1.5;">{desc}</div>
        </div>"""

# ── ML cards ─────────────────────────────────────────────────────
ml_cards = ""
for ico, name, mtype, desc, ck in t["ml"]:
    ml_cards += f"""
        <div class="card" style="position:relative;overflow:hidden;">
          <div style="position:absolute;top:0;left:0;right:0;height:3px;
               background:{clr(ck)};"></div>
          <div style="font-size:1.5rem;margin-bottom:14px;">{ico}</div>
          <div style="font-size:1rem;font-weight:700;color:{C['white']};
               font-family:'IBM Plex Mono',monospace;margin-bottom:4px;">{name}</div>
          <div style="font-size:.68rem;font-weight:700;text-transform:uppercase;
               letter-spacing:1.2px;color:{clr(ck)};margin-bottom:12px;">{mtype}</div>
          <div style="font-size:.8rem;color:{C['grey']};line-height:1.6;">{desc}</div>
        </div>"""

# ── Insight cards ────────────────────────────────────────────────
ins_cards = ""
for ico, txt, ck in t["ins"]:
    ins_cards += f"""
        <div class="card" style="border-left:3px solid {clr(ck)};
             display:flex;align-items:flex-start;gap:12px;">
          <div style="font-size:1.2rem;flex-shrink:0;margin-top:2px;">{ico}</div>
          <div style="font-size:.83rem;color:{C['white']};line-height:1.6;">{txt}</div>
        </div>"""

# ── Section badge helper ─────────────────────────────────────────
def badge(label):
    return (f'<div style="display:inline-block;background:{C["teal"]}18;'
            f'border:1px solid {C["teal"]}55;color:{C["teal"]};'
            f'font-size:.6rem;font-weight:700;letter-spacing:2px;'
            f'text-transform:uppercase;padding:4px 12px;border-radius:4px;'
            f'margin-bottom:10px;">{label}</div>')

hero_style = (f'background-image:url("{hero_src}");' if hero_src else
              f'background:linear-gradient(135deg,{C["navbar"]},{C["bg"]});')

# ── Full HTML ────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="en" dir="{dir_val}">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600;700&family=Tajawal:wght@300;400;700;800&display=swap" rel="stylesheet"/>
<style>
  *{{box-sizing:border-box;margin:0;padding:0;}}
  body{{
    background:{C['bg']};color:{C['white']};
    font-family:'{font_val}',sans-serif;direction:{dir_val};
  }}
  a{{text-decoration:none;}}

  /* ── Topbar ── */
  .topbar{{
    background:{C['navbar']};
    border-bottom:1px solid {C['border']};
    padding:0 40px;height:64px;
    display:flex;align-items:center;justify-content:space-between;
  }}
  .topbar-brand{{display:flex;align-items:center;gap:12px;}}
  .brand-name{{font-size:.92rem;font-weight:700;color:{C['white']};}}
  .brand-sub{{font-size:.6rem;color:{C['teal']};font-weight:600;
    letter-spacing:1.4px;text-transform:uppercase;}}
  .topbar-btns{{display:flex;gap:8px;}}
  .topbar-btn{{
    background:{C['dark_bg']};border:1px solid {C['border']};
    color:{C['white']};font-size:.78rem;font-weight:600;
    padding:7px 16px;border-radius:6px;cursor:pointer;
    font-family:'{font_val}',sans-serif;transition:all .2s;
  }}
  .topbar-btn:hover{{border-color:{C['gold']};color:{C['gold']};}}

  /* ── Hero ── */
  .hero{{
    position:relative;aspect-ratio:16/6;width:100%;overflow:hidden;
    {hero_style}
    background-size:cover;background-position:center;
  }}
  .hero-overlay{{
    position:absolute;inset:0;
    background:linear-gradient(105deg,{C['navbar']}F5 0%,{C['dark_bg']}BB 40%,transparent 100%);
  }}
  .hero-body{{
    position:relative;z-index:2;padding:5% 5%;
    max-width:54%;height:100%;
    display:flex;flex-direction:column;justify-content:center;
  }}
  .hero-pill{{
    display:inline-block;background:{C['teal']}18;
    border:1px solid {C['teal']}66;color:{C['teal']};
    font-size:.6rem;font-weight:700;letter-spacing:2px;
    text-transform:uppercase;padding:5px 14px;
    border-radius:4px;margin-bottom:18px;
  }}
  .hero-h1{{font-size:clamp(1.55rem,3vw,2.6rem);font-weight:700;
    color:{C['white']};line-height:1.1;margin-bottom:2px;}}
  .hero-h2{{font-size:clamp(1.55rem,3vw,2.6rem);font-weight:700;
    color:{C['teal']};line-height:1.1;margin-bottom:16px;}}
  .hero-sub{{font-size:clamp(.75rem,1.1vw,.88rem);color:{C['grey']};
    line-height:1.7;margin-bottom:26px;max-width:480px;}}
  .hero-cta{{
    display:inline-block;background:{C['teal']};
    color:{C['navbar']}!important;font-size:.85rem;font-weight:700;
    padding:11px 26px;border-radius:6px;width:fit-content;
    box-shadow:0 4px 20px {C['teal']}44;transition:background .2s;
  }}
  .hero-cta:hover{{background:{C['teal_act']};}}

  /* ── Stats ── */
  .stats-strip{{
    background:{C['sec_bg']};
    border-top:1px solid {C['border']};
    border-bottom:1px solid {C['border']};
    display:grid;grid-template-columns:repeat(4,1fr);
  }}

  /* ── Section ── */
  .section{{padding:52px 40px;}}
  .section.alt{{background:{C['sec_bg']};
    border-top:1px solid {C['border']};
    border-bottom:1px solid {C['border']};}}
  .sec-head{{margin-bottom:28px;}}
  .sec-h2{{font-size:1.45rem;font-weight:700;color:{C['white']};margin-bottom:6px;}}
  .sec-sub{{font-size:.82rem;color:{C['grey']};}}
  .divider{{height:1px;background:{C['border']};margin:0 40px;}}

  /* ── Cards ── */
  .grid-4{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;}}
  .grid-3{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}}
  .grid-2{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;}}
  .card{{
    background:{C['dark_bg']};border:1px solid {C['border']};
    border-radius:8px;padding:20px 18px;
    transition:border-color .25s,transform .25s,box-shadow .25s;
  }}
  .hover-card:hover{{
    border-color:{C['teal']}55;transform:translateY(-3px);
    box-shadow:0 8px 28px {C['teal']}18;
  }}

  /* ── Footer ── */
  .footer{{
    background:{C['navbar']};border-top:2px solid {C['teal']};
    padding:24px 40px;display:flex;
    justify-content:space-between;align-items:center;
    flex-wrap:wrap;gap:14px;
  }}
  .footer-links{{display:flex;gap:22px;align-items:center;}}
  .footer-links a{{font-size:.76rem;color:{C['foot_txt']};font-weight:500;}}
  .footer-links a:hover{{color:{C['teal']};}}
  .footer-links a.primary{{color:{C['teal']};font-weight:600;}}
</style>
</head>
<body>

<!-- TOPBAR -->
<div class="topbar">
  <div class="topbar-brand">
    {logo_img}
    <div>
      <div class="brand-name">{t['name']}</div>
      <div class="brand-sub">{t['sub']}</div>
    </div>
  </div>
  <div class="topbar-btns">
    <button class="topbar-btn" onclick="window.parent.postMessage({{type:'streamlit:setComponentValue',value:'thm'}},'*')">{t['thm']}</button>
    <button class="topbar-btn" onclick="window.parent.postMessage({{type:'streamlit:setComponentValue',value:'lng'}},'*')">{t['lng']}</button>
  </div>
</div>

<!-- HERO -->
<div class="hero">
  <div class="hero-overlay"></div>
  <div class="hero-body">
    <div class="hero-pill">{t['pill']}</div>
    <div class="hero-h1">{t['h1']}</div>
    <div class="hero-h2">{t['h2']}</div>
    <p class="hero-sub">{t['hs']}</p>
    <a href="#" class="hero-cta">{t['hb']}</a>
  </div>
</div>

<!-- STATS -->
<div class="stats-strip">
  {stats_cells}
</div>

<!-- PAGES -->
<div class="section">
  <div class="sec-head">
    {badge(t['pt'])}
    <div class="sec-h2">{t['ph']}</div>
    <div class="sec-sub">{t['ps']}</div>
  </div>
  <div class="grid-4">{page_cards}</div>
</div>

<div class="divider"></div>

<!-- ML MODELS -->
<div class="section alt">
  <div class="sec-head">
    {badge(t['mt'])}
    <div class="sec-h2">{t['mh']}</div>
    <div class="sec-sub">{t['ms']}</div>
  </div>
  <div class="grid-3">{ml_cards}</div>
</div>

<!-- INSIGHTS -->
<div class="section">
  <div class="sec-head">
    {badge(t['it'])}
    <div class="sec-h2">{t['ih']}</div>
  </div>
  <div class="grid-2">{ins_cards}</div>
</div>

<!-- FOOTER -->
<div class="footer">
  <div style="display:flex;align-items:center;gap:14px;">
    {logo_img}
    <div>
      <div style="font-size:.86rem;font-weight:700;color:{C['teal']};">{t['name']}</div>
      <div style="font-size:.67rem;color:{C['foot_txt']};margin-top:2px;">{t['copy']}</div>
      <div style="font-size:.64rem;color:{C['grey']};margin-top:2px;">📦 {t['data']}</div>
    </div>
  </div>
  <div class="footer-links">
    <a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" target="_blank">🐙 GitHub</a>
    <a href="https://www.linkedin.com/in/goda-emad/" target="_blank">💼 LinkedIn</a>
    <a href="https://datasaudi.sa" target="_blank" class="primary">📊 DataSaudi</a>
  </div>
</div>

</body>
</html>"""

# ── Streamlit: hide chrome + inject Gold Slider CSS ─────────────
st.markdown("""
<style>
[data-testid="stHeader"],[data-testid="stToolbar"],footer{display:none!important;}
.block-container{padding:0!important;max-width:100%!important;}
/* ── Gold Slider ── */
[data-testid="stSlider"] [role="slider"]{background:#C9A84C!important;border-color:#C9A84C!important;}
[data-baseweb="slider"] div[data-testid="stSlider"] > div > div > div:nth-child(2) > div{background:#C9A84C!important;}
[data-baseweb="slider"] > div > div:first-child{background:#2A3235!important;}
[data-baseweb="slider"] > div > div:nth-child(2){background:#C9A84C!important;}
</style>
""", unsafe_allow_html=True)

# ── Topbar buttons via Streamlit (hidden, triggered by HTML) ─────
col_thm, col_lng = st.columns([1,1])
with col_thm:
    if st.button(t["thm"], key="k_thm", use_container_width=True):
        st.session_state.theme = "light" if THEME=="dark" else "dark"; st.rerun()
with col_lng:
    if st.button(t["lng"], key="k_lng", use_container_width=True):
        st.session_state.lang = "AR" if LANG=="EN" else "EN"; st.rerun()

# ── Render full HTML page ────────────────────────────────────────
components.html(html, height=2400, scrolling=False)
