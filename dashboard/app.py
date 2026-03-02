import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path
import base64

# إضافة المسار الرئيسي للمشروع
sys.path.append(str(Path(__file__).parent.parent))

# استيراد الدوال المساعدة
from utils.kpis import calculate_kpis
from utils.data_loader import (
    load_tourist_data,
    load_spending_data,
    load_overnight_data,
    load_carbon_data
)

# ═══════════════════════════════════════════════════════
# PAGE CONFIG - MUST BE FIRST STREAMLIT COMMAND
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Saudi Tourism Intelligence",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════
# CONSTANTS & CONFIG
# ═══════════════════════════════════════════════════════
DEV_NAME = "Eng. Goda Emad"
DEV_GITHUB = "https://github.com/Goda-Emad/Saudi-Tourism-Intelligence/tree/main"
DEV_LINKEDIN = "https://www.linkedin.com/in/goda-emad/"

# ألوان ثابتة
COLORS = {
    'green': '#1B5E20',
    'green_light': '#43A047',
    'gold': '#D4A017',
    'teal': '#00838F',
    'teal_light': '#00ACC1',
    'bg_card': '#132336',
    'text_primary': '#F0F4F8',
    'text_secondary': '#94A3B8',
    'border': '#2A3F55'
}

# ═══════════════════════════════════════════════════════
# CACHED FUNCTIONS (لتسريع التحميل)
# ═══════════════════════════════════════════════════════
@st.cache_data(ttl=3600)  # تخزين مؤقت لمدة ساعة
def load_all_cached_data():
    """تحميل جميع البيانات مع التخزين المؤقت"""
    tourist_data = load_tourist_data()
    spending_data = load_spending_data()
    overnight_data = load_overnight_data()
    carbon_data = load_carbon_data()
    return tourist_data, spending_data, overnight_data, carbon_data

@st.cache_data(ttl=86400)  # تخزين مؤقت لمدة يوم
def get_image_base64(image_path):
    """تحويل الصورة إلى base64"""
    try:
        full_path = Path(__file__).parent / image_path
        if full_path.exists():
            with open(full_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        return ""
    except:
        return ""

# ═══════════════════════════════════════════════════════
# LOAD CUSTOM CSS (مع التخزين المؤقت)
# ═══════════════════════════════════════════════════════
@st.cache_data(ttl=86400)
def load_css():
    """تحميل ملف CSS المخصص"""
    css_file = Path(__file__).parent / "assets" / "style.css"
    if css_file.exists():
        with open(css_file, 'r', encoding='utf-8') as f:
            return f"<style>{f.read()}</style>"
    return ""

# تطبيق CSS
st.markdown(load_css(), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════
if "lang" not in st.session_state:
    st.session_state.lang = "EN"
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "overview"

# ═══════════════════════════════════════════════════════
# TRANSLATIONS (مبسطة)
# ═══════════════════════════════════════════════════════
T = {
    "EN": {
        "app_title": "Saudi Tourism Intelligence",
        "app_subtitle": "AI-Powered Tourism Analytics",
        "welcome": "Official tourism intelligence platform for Saudi Arabia. Powered by DataSaudi and Vision 2030.",
        "built_by": "Built by",
        "nav_title": "Navigation",
        "overview": "🏠 Overview",
        "trends": "📈 Tourist Trends",
        "seasonality": "📅 Seasonality",
        "spending": "💰 Spending",
        "overnight": "🏨 Overnight Stays",
        "forecast": "🔮 Forecasting",
        "segmentation": "🎯 Segmentation",
        "carbon": "🌱 Carbon Impact",
        "data_source": "DataSaudi · Ministry of Tourism",
        "last_updated": "March 2025",
        "key_metrics": "Key Metrics 2024",
        "total_tourists": "Total Tourists",
        "inbound": "Inbound",
        "domestic": "Domestic",
        "overnight_stays": "Overnight Stays",
        "avg_spend": "Avg Spend",
        "footer_text": "© 2025 Saudi Tourism Intelligence",
        "github": "GitHub",
        "linkedin": "LinkedIn",
    },
    "AR": {
        "app_title": "الذكاء السياحي السعودي",
        "app_subtitle": "منصة تحليلات سياحية",
        "welcome": "المنصة الرسمية للذكاء السياحي في السعودية. مدعومة من DataSaudi ورؤية 2030.",
        "built_by": "من تطوير",
        "nav_title": "التنقل",
        "overview": "🏠 نظرة عامة",
        "trends": "📈 اتجاهات السياحة",
        "seasonality": "📅 الموسمية",
        "spending": "💰 الإنفاق",
        "overnight": "🏨 ليالي الإقامة",
        "forecast": "🔮 التوقعات",
        "segmentation": "🎯 تجزئة السياح",
        "carbon": "🌱 الأثر الكربوني",
        "data_source": "DataSaudi · وزارة السياحة",
        "last_updated": "مارس 2025",
        "key_metrics": "المؤشرات الرئيسية 2024",
        "total_tourists": "إجمالي السياح",
        "inbound": "وافدون",
        "domestic": "محليون",
        "overnight_stays": "ليالي الإقامة",
        "avg_spend": "متوسط الإنفاق",
        "footer_text": "© 2025 الذكاء السياحي السعودي",
        "github": "جيت هاب",
        "linkedin": "لينكد إن",
    }
}

# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    # Logo
    logo_base64 = get_image_base64("assets/logo.png")
    if logo_base64:
        st.markdown(f"""
        <div style='text-align: center; padding: 0.5rem;'>
            <img src='data:image/png;base64,{logo_base64}' style='max-width: 160px; height: auto;'>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='text-align:center; padding: 1rem;'>
            <div style='color: {COLORS['gold']}; font-weight: 700;'>Saudi Tourism</div>
            <div style='color: {COLORS['text_primary']};'>INTELLIGENCE</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"<div style='text-align:center; color:{COLORS['text_secondary']}; font-size:0.8rem; margin-bottom:1rem;'>{T[st.session_state.lang]['app_subtitle']}</div>", unsafe_allow_html=True)
    
    st.divider()
    
    # Language Toggle (مبسط)
    if st.button("🌐 العربية" if st.session_state.lang == "EN" else "🌐 English", use_container_width=True):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"
        st.rerun()
    
    st.divider()
    
    # Navigation
    st.markdown(f"<div style='color:{COLORS['text_secondary']}; font-size:0.7rem; font-weight:600; margin-bottom:0.5rem;'>{T[st.session_state.lang]['nav_title']}</div>", unsafe_allow_html=True)
    
    pages = {
        "overview": T[st.session_state.lang]["overview"],
        "trends": T[st.session_state.lang]["trends"],
        "seasonality": T[st.session_state.lang]["seasonality"],
        "spending": T[st.session_state.lang]["spending"],
        "overnight": T[st.session_state.lang]["overnight"],
        "forecast": T[st.session_state.lang]["forecast"],
        "segmentation": T[st.session_state.lang]["segmentation"],
        "carbon": T[st.session_state.lang]["carbon"],
    }
    
    for page_key, page_name in pages.items():
        if st.button(page_name, key=f"nav_{page_key}", use_container_width=True):
            st.session_state.current_page = page_key
            st.rerun()
    
    st.divider()
    
    # Developer Info (مبسط)
    st.markdown(f"""
    <div style='background: {COLORS['bg_card']}; border:1px solid {COLORS['border']}; border-radius:12px; padding:1rem; text-align:center;'>
        <div style='color:{COLORS['text_secondary']}; font-size:0.75rem;'>{T[st.session_state.lang]['built_by']}</div>
        <div style='color:{COLORS['gold']}; font-weight:700; margin:0.3rem 0;'>{DEV_NAME}</div>
        <div style='display:flex; justify-content:center; gap:0.5rem;'>
            <a href="{DEV_GITHUB}" target="_blank" style='color:{COLORS['teal_light']}; text-decoration:none; font-size:0.75rem;'>🐙 GitHub</a>
            <span style='color:{COLORS['border']};'>|</span>
            <a href="{DEV_LINKEDIN}" target="_blank" style='color:{COLORS['teal_light']}; text-decoration:none; font-size:0.75rem;'>💼 LinkedIn</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════

# Load data
try:
    tourist_data, spending_data, overnight_data, carbon_data = load_all_cached_data()
    st.session_state.data_loaded = True
except Exception as e:
    st.error(f"⚠️ خطأ في تحميل البيانات")
    st.session_state.data_loaded = False

# Hero Section
hero_base64 = get_image_base64("assets/hero.png")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"""
    <h1 style='color:{COLORS['gold']}; margin:0; font-size:2.2rem;'>{T[st.session_state.lang]['app_title']}</h1>
    <p style='color:{COLORS['text_secondary']}; margin:0.5rem 0;'>{T[st.session_state.lang]['welcome']}</p>
    <div style='color:{COLORS['text_secondary']}; font-size:0.8rem;'>{T[st.session_state.lang]['built_by']}: <span style='color:{COLORS['gold']}; font-weight:700;'>{DEV_NAME}</span></div>
    """, unsafe_allow_html=True)

with col2:
    if hero_base64:
        st.markdown(f"<img src='data:image/png;base64,{hero_base64}' style='max-width:150px; max-height:120px; border-radius:10px;'>", unsafe_allow_html=True)

# Key Metrics
if st.session_state.data_loaded:
    kpis = calculate_kpis(tourist_data, spending_data, overnight_data)
    
    metrics = [
        (T[st.session_state.lang]["total_tourists"], f"{kpis['total_tourists_2024']:.1f}M", f"{kpis['tourists_growth']:.1f}%"),
        (T[st.session_state.lang]["inbound"], f"{kpis['inbound_2024']:.1f}M", f"{kpis['inbound_growth']:.1f}%"),
        (T[st.session_state.lang]["domestic"], f"{kpis['domestic_2024']:.1f}M", f"{kpis['domestic_growth']:.1f}%"),
        (T[st.session_state.lang]["overnight_stays"], f"{kpis['total_nights_2024']:.1f}B", f"{kpis['nights_growth']:.1f}%"),
        (T[st.session_state.lang]["avg_spend"], f"{kpis['avg_spend_2024']:.0f} SAR", f"{kpis['spend_growth']:.1f}%"),
    ]
    
    cols = st.columns(5)
    for i, (label, value, delta) in enumerate(metrics):
        with cols[i]:
            st.metric(label=label, value=value, delta=delta)

# ═══════════════════════════════════════════════════════
# PAGE ROUTING
# ═══════════════════════════════════════════════════════
current_page = st.session_state.current_page

if current_page != "overview":
    st.divider()

try:
    if current_page == "overview" and st.session_state.data_loaded:
        from pages.overview import show_overview
        show_overview(tourist_data, spending_data, overnight_data, carbon_data, st.session_state.lang)
    elif current_page == "trends":
        from pages.tourist_trends import show_trends
        show_trends(tourist_data, st.session_state.lang)
    elif current_page == "seasonality":
        from pages.seasonality import show_seasonality
        show_seasonality(tourist_data, st.session_state.lang)
    elif current_page == "spending":
        from pages.spending import show_spending
        show_spending(spending_data, tourist_data, st.session_state.lang)
    elif current_page == "overnight":
        from pages.overnight_stays import show_overnight
        show_overnight(overnight_data, tourist_data, st.session_state.lang)
    elif current_page == "forecast":
        from pages.forecasting import show_forecast
        show_forecast(tourist_data, st.session_state.lang)
    elif current_page == "segmentation":
        from pages.segmentation import show_segmentation
        show_segmentation(tourist_data, spending_data, overnight_data, st.session_state.lang)
    elif current_page == "carbon":
        from pages.carbon_impact import show_carbon
        show_carbon(carbon_data, tourist_data, overnight_data, st.session_state.lang)
except ImportError:
    st.info(f"صفحة {current_page} قيد التطوير")

# ═══════════════════════════════════════════════════════
# FOOTER (مبسط وسريع)
# ═══════════════════════════════════════════════════════
st.divider()

st.markdown(f"""
<div style='background:{COLORS['bg_card']}; border:1px solid {COLORS['border']}; border-radius:12px; padding:1.5rem; margin-top:1rem; text-align:center;'>
    <div style='color:{COLORS['gold']}; font-weight:700; font-size:1.2rem; margin-bottom:0.5rem;'>{DEV_NAME}</div>
    <div style='margin-bottom:0.8rem;'>
        <a href="{DEV_GITHUB}" target="_blank" style='color:{COLORS['teal_light']}; text-decoration:none; margin:0 10px;'>🐙 GitHub</a>
        <span style='color:{COLORS['border']};'>|</span>
        <a href="{DEV_LINKEDIN}" target="_blank" style='color:{COLORS['teal_light']}; text-decoration:none; margin:0 10px;'>💼 LinkedIn</a>
    </div>
    <div style='color:{COLORS['text_secondary']}; font-size:0.7rem;'>{T[st.session_state.lang]['data_source']} · {T[st.session_state.lang]['last_updated']}</div>
    <div style='color:{COLORS['text_secondary']}; font-size:0.65rem; margin-top:0.5rem;'>{T[st.session_state.lang]['footer_text']}</div>
</div>
""", unsafe_allow_html=True)
