# ═══════════════════════════════════════════════════════════════════
#  Saudi Tourism Intelligence — Home Page
#  Author : Eng. Goda Emad
# ═══════════════════════════════════════════════════════════════════
import streamlit as st
import base64, os
from utils.sidebar import render_sidebar

# 1. إعدادات الصفحة (يجب أن تكون أول سطر)
st.set_page_config(
    page_title="Saudi Tourism Intelligence",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. استدعاء القائمة الجانبية الموحدة وجلب المتغيرات
THEME, LANG = render_sidebar()

# ── ML Model Accuracy ──
ML_R2 = 0.986
ML_ACCURACY = f"{ML_R2*100:.1f}%"

# ── Colors ─────────────────────────────────────────
DARK = {
    "teal":"#17B19B", "teal_act":"#149581", "teal_sec":"#8BAFAA",
    "bg":"#1A1E1F", "sec_bg":"#161B1C", "card_bg":"#1E2528",
    "navbar":"#031414", "white":"#F4F9F8", "grey":"#A1A6B7",
    "foot_txt":"#B5B8B7", "border":"#2A3235",
    "orange":"#F4D044", "gold":"#C9A84C", "blue":"#365C8D",
}
LIGHT = {
    "teal":"#17B19B", "teal_act":"#149581", "teal_sec":"#4A8A82",
    "bg":"#F0F5F4", "sec_bg":"#E4EDEB", "card_bg":"#FFFFFF",
    "navbar":"#172025", "white":"#0D1A1E", "grey":"#374151",
    "foot_txt":"#6B7280", "border":"#C8D8D5",
    "orange":"#B45309", "gold":"#92650A", "blue":"#1D4ED8",
}
C = DARK if THEME == "dark" else LIGHT
def clr(k): return C.get(k, C["teal"])

# ── Cached helpers ────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def _b64(path):
    try:
        base = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base, path), "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

# ── Translations ──────────────────────────────────────────────────
TR = {
    "EN": {
        "pill": "🇸🇦 OFFICIAL DATA · MINISTRY OF ECONOMY & PLANNING",
        "h1": "Saudi Tourism", "h2": "Intelligence",
        "hs": "AI-powered analytics built on 10 years of official government data. Forecasting · Segmentation · Sustainability — all in one platform.",
        "stats": [
            ("115.8M", "Tourists 2024", "teal", "+23%", "up"),
            ("1.10B", "Overnight Stays", "teal", "+41%", "up"),
            ("5,622", "Avg Spend (SAR)", "orange", "+8%", "up"),
            (ML_ACCURACY, "ML Accuracy R²", "orange", "", ""),
        ],
        "pt": "PLATFORM", "ph": "8 Interactive Pages",
        "ps": "Comprehensive analysis covering every dimension of Saudi tourism",
        "pages": [
            ("🏠", "Executive Overview", "KPIs, trends & insights"),
            ("📈", "Tourist Trends", "Annual & monthly 2015–2024"),
            ("📅", "Seasonality", "Ramadan & summer peaks"),
            ("💰", "Spending Analysis", "Per trip, per night, by purpose"),
            ("🏨", "Overnight Stays", "Length of stay & COVID recovery"),
            ("🔮", "Demand Forecasting", "Prophet ML · 2025–2026"),
            ("🎯", "Segmentation", "K-Means · High / Mid / Budget"),
            ("🌱", "Carbon Impact", "CO₂ index & ESG sustainability"),
        ],
        "mt": "MACHINE LEARNING", "mh": "3 Production ML Models",
        "ms": "Trained on 10 years of official Saudi government data",
        "ml": [
            ("🔮", "Prophet", "Demand Forecasting", "Predicts future tourist numbers...", "24-month forecast · confidence bounds", "teal"),
            ("🎯", "K-Means", "Tourist Segmentation", "Groups tourists into High / Mid...", "3 segments · Silhouette 0.630", "orange"),
            ("💰", "Gradient Boosting", "Spending Prediction", "Predicts per-trip spending...", "Full spend analysis · MAE SAR 184", "blue"),
        ],
        "it": "KEY DISCOVERIES", "ih": "Data Insights",
        "ins": [
            ("🏖️", "Leisure overtook Religious as #1 purpose in 2024 — Vision 2030 ✅", "teal"),
            ("⏰", "Inbound avg stay: 8.6 → 19.2 nights (2021→2024) · +123%", "orange"),
            ("💰", "Inbound tourists spend 4× more than Domestic", "blue"),
            ("🚀", "2024 record: 115.9M tourists · +150% recovery", "teal_act"),
        ],
        "v30": [
            ("🎯 Tourist Arrivals Target", 115.9, 150.0, "M tourists by 2030", "teal"),
            ("💰 Tourism GDP Contribution", 10.0, 10.0, "% of GDP (achieved ✅)", "gold"),
            ("🌱 Carbon Intensity Reduction", 18.0, 30.0, "% reduction by 2030", "orange"),
            ("🏨 Hotel Capacity Expansion", 72.0, 100.0, "% of 500K rooms target", "blue"),
        ],
        "v30_title": "VISION 2030", "v30_h": "Progress Toward Vision 2030 Targets",
        "name": "Saudi Tourism Intelligence", "copy": "© 2025 Saudi Tourism Intelligence", "data": "DataSaudi · 2015–2024",
    },
    "AR": {
        "pill": "🇸🇦 بيانات رسمية · وزارة الاقتصاد والتخطيط",
        "h1": "ذكاء السياحة", "h2": "السعودية",
        "hs": "تحليلات مدعومة بالذكاء الاصطناعي على 10 سنوات من البيانات الرسمية. توقعات · تقسيم · استدامة — كل شيء في منصة واحدة.",
        "stats": [
            ("115.8M", "سائح 2024", "teal", "+23%", "up"),
            ("1.10B", "ليالي الإقامة", "teal", "+41%", "up"),
            ("5,622", "متوسط الإنفاق", "orange", "+8%", "up"),
            (ML_ACCURACY, "دقة النموذج R²", "orange", "", ""),
        ],
        "pt": "المنصة", "ph": "8 صفحات تفاعلية",
        "ps": "تحليل شامل لكل أبعاد السياحة السعودية",
        "pages": [
            ("🏠", "النظرة التنفيذية", "مؤشرات الأداء والاتجاهات"),
            ("📈", "اتجاهات السياحة", "الأنماط السنوية والشهرية"),
            ("📅", "الموسمية", "ذروة الأشهر وتأثير رمضان"),
            ("💰", "تحليل الإنفاق", "لكل رحلة، لكل ليلة، حسب الغرض"),
            ("🏨", "ليالي الإقامة", "مدة الإقامة وتعافي كوفيد"),
            ("🔮", "توقعات الطلب", "Prophet ML · 2025–2026"),
            ("🎯", "تقسيم السياح", "K-Means · عالي/متوسط/اقتصادي"),
            ("🌱", "الأثر الكربوني", "مؤشر CO₂ واستدامة ESG"),
        ],
        "mt": "التعلم الآلي", "mh": "3 نماذج ML جاهزة للإنتاج",
        "ms": "مدرّبة على 10 سنوات من البيانات السعودية الرسمية",
        "ml": [
            ("🔮", "Prophet", "توقع الطلب", "يتوقع أعداد السياح المستقبليين...", "توقعات 24 شهرًا · فترات الثقة", "teal"),
            ("🎯", "K-Means", "تقسيم السياح", "يصنف السياح لاستراتيجية مستهدفة...", "3 شرائح · Silhouette 0.630", "orange"),
            ("💰", "Gradient Boosting", "توقع الإنفاق", "يتوقع الإنفاق لكل رحلة...", "تحليل الإنفاق التنبؤي · MAE 184", "blue"),
        ],
        "it": "الاكتشافات الرئيسية", "ih": "رؤى البيانات",
        "ins": [
            ("🏖️", "الترفيه تجاوز الديني كأول غرض في 2024 ✅", "teal"),
            ("⏰", "متوسط إقامة الوافد: 8.6 → 19.2 ليلة · +123%", "orange"),
            ("💰", "الوافدون ينفقون 4 أضعاف المحليين", "blue"),
            ("🚀", "رقم قياسي 2024: 115.9M سائح", "teal_act"),
        ],
        "v30": [
            ("🎯 مستهدف الوصول السياحي", 115.9, 150.0, "مليون سائح بحلول 2030", "teal"),
            ("💰 مساهمة السياحة في الناتج", 10.0, 10.0, "% من الناتج (تحقق ✅)", "gold"),
            ("🌱 تخفيض الكثافة الكربونية", 18.0, 30.0, "% تخفيض بحلول 2030", "orange"),
            ("🏨 توسعة الطاقة الفندقية", 72.0, 100.0, "% من مستهدف 500 ألف غرفة", "blue"),
        ],
        "v30_title": "رؤية 2030", "v30_h": "التقدم نحو مستهدفات رؤية 2030",
        "name": "ذكاء السياحة السعودية", "copy": "© 2025 ذكاء السياحة السعودية", "data": "داتا السعودية · 2015–2024",
    }
}

t = TR[LANG]
hero_b64 = _b64("assets/hero.jpg")
hero_src = f"data:image/jpeg;base64,{hero_b64}" if hero_b64 else ""
logo_b64 = _b64("assets/logo.png")
logo_src = f"data:image/png;base64,{logo_b64}" if logo_b64 else ""

dir_val = "rtl" if LANG == "AR" else "ltr"
ff = "Tajawal" if LANG == "AR" else "IBM Plex Sans"

# ════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ════════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;600;700&family=Tajawal:wght@400;700;800&display=swap');

/* Main Settings */
html, body, [data-testid='stAppViewContainer'], [data-testid='stMain'] {{
    background: {C["bg"]} !important;
    direction: {dir_val};
    font-family: '{ff}', sans-serif;
}}

/* Hide Streamlit chrome */
[data-testid="stHeader"], [data-testid="stToolbar"], footer, #MainMenu {{ display: none !important; }}
.block-container {{ padding: 0 !important; max-width: 100% !important; }}
section[data-testid="stMain"] > div:first-child {{ padding-top: 0 !important; }}

/* Hero class */
.ds-hero {{
    position: relative !important; width: 100% !important; height: 520px !important;
    overflow: hidden !important; background-size: cover !important;
    background-position: center center !important;
    background-image: {'url("' + hero_src + '")' if hero_src else 'linear-gradient(135deg,'+C["navbar"]+','+C["bg"]+')'} !important;
}}

/* Hover cards & Elements */
.ds-card {{ transition: transform .22s ease, border-color .22s, box-shadow .22s !important; cursor: pointer; }}
.ds-card:hover {{ transform: translateY(-4px) !important; box-shadow: 0 12px 32px rgba(23,177,155,.2) !important; }}
.ds-prog-bg {{ background: {C["border"]}; border-radius: 8px; height: 10px; overflow: hidden; }}
.ds-prog-fill {{ height: 100%; border-radius: 8px; transition: width .8s ease; position: relative; box-shadow: 4px 0 12px currentColor; }}
.ds-prog-fill::after {{
    content: ''; position: absolute; right: -1px; top: 50%; transform: translateY(-50%);
    width: 10px; height: 10px; border-radius: 50%; background: inherit;
    box-shadow: 0 0 8px 3px currentColor; opacity: .7;
}}
.ds-spark {{ opacity: .35; }}

/* Tooltips */
.ds-tooltip {{ position: relative; display: inline-block; }}
.ds-tooltip .ds-tip {{
    visibility: hidden; opacity: 0; position: absolute; bottom: calc(100% + 8px); left: 50%;
    transform: translateX(-50%); background: #0D1A1E; border: 1px solid #17B19B44;
    color: #F4F9F8; font-size: .72rem; line-height: 1.5; padding: 8px 12px;
    border-radius: 6px; width: 220px; text-align: center; transition: opacity .2s; z-index: 99;
}}
.ds-tooltip:hover .ds-tip {{ visibility: visible; opacity: 1; }}

/* CTA Button Animation */
@keyframes ds-pulse {{
  0%, 100% {{ box-shadow: 0 6px 28px rgba(23,177,155,.55); }}
  50% {{ box-shadow: 0 6px 40px rgba(23,177,155,.9), 0 0 0 8px rgba(23,177,155,.12); }}
}}
div[data-testid="stMain"] > div > div:nth-child(2) {{
  margin-top: -82px !important; padding-left: 92px !important; position: relative !important;
  z-index: 20 !important; width: fit-content !important; pointer-events: auto !important;
}}
div[data-testid="stMain"] > div > div:nth-child(2) button {{
  background: #17B19B !important; color: #FFFFFF !important; font-size: .92rem !important;
  font-weight: 700 !important; padding: 13px 28px !important; border-radius: 7px !important;
  border: none !important; animation: ds-pulse 2.6s ease-in-out infinite !important;
}}
div[data-testid="stMain"] > div > div:nth-child(2) button:hover {{
  background: #149581 !important; animation: none !important; transform: translateX(4px) !important;
}}
</style>
""", unsafe_allow_html=True)

def sec_head(badge, h2, sub=""):
    return f"""
    <div style="margin-bottom:28px;">
        <div style="display:inline-block;background:{C['teal']}15;border:1px solid {C['teal']}44;color:{C['teal']};font-size:.58rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;padding:4px 12px;border-radius:4px;margin-bottom:12px;">{badge}</div>
        <div style="font-size:1.5rem;font-weight:700;color:{C['white']};margin-bottom:6px;">{h2}</div>
        {f'<div style="font-size:.82rem;color:{C["grey"]};">{sub}</div>' if sub else ''}
    </div>
    """

# ════════════════════════════════════════════════════════════════════
# HERO SECTION
# ════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="ds-hero">
    <div style="position:absolute;inset:0;background:linear-gradient(100deg,{C['navbar']}EE 0%,{C['navbar']}99 38%,{C['bg']}22 70%,transparent 100%);"></div>
    <div style="position:relative;z-index:2;padding:80px 52px;max-width:600px;">
        <div style="display:inline-flex;align-items:center;background:{C['teal']}15;border:1px solid {C['teal']}55;color:{C['teal']};font-size:.58rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;padding:5px 14px;border-radius:4px;margin-bottom:22px;">{t['pill']}</div>
        <div style="font-size:3.4rem;font-weight:800;color:{C['white']};line-height:1.0;letter-spacing:-1.5px;margin-bottom:4px;">{t['h1']}</div>
        <div style="font-size:3.4rem;font-weight:800;color:{C['teal']};line-height:1.0;letter-spacing:-1.5px;margin-bottom:22px;">{t['h2']}</div>
        <p style="font-size:.95rem;color:{C['grey']};line-height:1.8;margin-bottom:30px;max-width:460px;">{t['hs']}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Button
if st.button("Explore Dashboard  →" if LANG=="EN" else "←  استكشف لوحة التحكم", key="hero_cta"):
    st.switch_page("pages/Tourist_Trends.py")

# ════════════════════════════════════════════════════════════════════
# STATS STRIP
# ════════════════════════════════════════════════════════════════════
cells = "".join([f"""
    <div style="padding:28px 24px; {'border-right:1px solid '+C['border'] if i<3 else ''}">
        <div style="display:flex;align-items:baseline;gap:0;">
            <div style="font-size:2rem;font-weight:700;color:{clr(ck)};font-family:IBM Plex Mono,monospace;letter-spacing:-1px;">{val}</div>
            {f'<span style="font-size:.72rem;color:{"#17B19B" if ddir=="up" else "#C50A5D"};font-weight:700;margin-left:6px;font-family:IBM Plex Mono,monospace;">{"▲" if ddir=="up" else "▼"} {delta}</span>' if delta else ""}
        </div>
        <div style="font-size:.64rem;color:{C['grey']};text-transform:uppercase;letter-spacing:1.2px;font-weight:600;margin-top:6px;opacity:0.9;">{lbl}</div>
    </div>
""" for i, (val, lbl, ck, delta, ddir) in enumerate(t["stats"])])

st.markdown(f'<div style="background:{C["sec_bg"]};border-top:1px solid {C["border"]};border-bottom:1px solid {C["border"]};display:grid;grid-template-columns:repeat(4,1fr);">{cells}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# CARDS SECTION (Pages, ML, Insights, Vision)
# ════════════════════════════════════════════════════════════════════
# Pages Cards
page_cards = "".join([f"""
    <div class="ds-card" style="background:{C['card_bg']};border:1px solid {C['border']};border-radius:10px;padding:20px 18px;">
        <div style="font-size:1.6rem;margin-bottom:10px;line-height:1;">{ico}</div>
        <div style="font-size:.87rem;font-weight:600;color:{C['white']};margin-bottom:5px;">{title}</div>
        <div style="font-size:.73rem;color:{C['grey']};line-height:1.5;">{desc}</div>
    </div>
""" for ico, title, desc in t["pages"]])

st.markdown(f'<div style="padding:52px 40px;">{sec_head(t["pt"], t["ph"], t["ps"])}<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;">{page_cards}</div></div>', unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div style="background:{C['navbar']};border-top:2px solid {C['teal']};padding:28px 40px;display:flex;justify-content:space-between;align-items:center;">
    <div style="display:flex;align-items:center;gap:14px;">
        <img src="{logo_src}" style="height:42px;border-radius:8px;" onerror="this.style.display='none'"/>
        <div>
            <div style="font-size:.9rem;font-weight:700;color:{C['teal']};">{t['name']}</div>
            <div style="font-size:.68rem;color:{C['foot_txt']};margin-top:3px;">{t['copy']}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
