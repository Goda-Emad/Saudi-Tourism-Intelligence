"""
Saudi Tourism Intelligence - Professional Dashboard
Developed by: Eng. Goda Emad
Version: 8.0.0
Features: Dark/Light Mode, Arabic/English, Optimized Performance, Green Navigation in Slider
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path
import base64
import time

# ═══════════════════════════════════════════════════════
# PAGE CONFIG - MUST BE FIRST
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Saudi Tourism Intelligence",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="collapsed"  # لتسريع التحميل
)

# ═══════════════════════════════════════════════════════
# CONSTANTS & CONFIGURATION
# ═══════════════════════════════════════════════════════
class Config:
    """Application Configuration"""
    DEV_NAME = "Eng. Goda Emad"
    DEV_GITHUB = "https://github.com/Goda-Emad/Saudi-Tourism-Intelligence"
    DEV_LINKEDIN = "https://www.linkedin.com/in/goda-emad/"
    APP_VERSION = "8.0.0"
    
    # Color Palettes
    DARK_THEME = {
        'bg': '#0D1B2A',
        'card': '#132336',
        'card_hover': '#1A2F45',
        'text': '#F0F4F8',
        'text_muted': '#94A3B8',
        'border': '#2A3F55',
        'primary': '#1B5E20',
        'primary_light': '#2E7D32',
        'primary_dark': '#0A3A0A',
        'secondary': '#00838F',
        'accent': '#D4A017',
        'success': '#43A047',
        'warning': '#F0A500',
        'danger': '#FF5252'
    }
    
    LIGHT_THEME = {
        'bg': '#F5F9FF',
        'card': '#FFFFFF',
        'card_hover': '#F0F4F8',
        'text': '#1A2B3C',
        'text_muted': '#4A6080',
        'border': '#CBD5E0',
        'primary': '#2E7D32',
        'primary_light': '#4CAF50',
        'primary_dark': '#1B5E20',
        'secondary': '#00ACC1',
        'accent': '#E08C00',
        'success': '#2E7D32',
        'warning': '#F57C00',
        'danger': '#C62828'
    }
    
    # Page Names
    PAGES = [
        {"id": "overview", "en": "📊 Overview", "ar": "📊 نظرة عامة"},
        {"id": "trends", "en": "📈 Tourist Trends", "ar": "📈 اتجاهات السياحة"},
        {"id": "seasonality", "en": "📅 Seasonality", "ar": "📅 الموسمية"},
        {"id": "spending", "en": "💰 Spending", "ar": "💰 الإنفاق"},
        {"id": "overnight", "en": "🏨 Overnight Stays", "ar": "🏨 ليالي الإقامة"},
        {"id": "forecast", "en": "🔮 Forecasting", "ar": "🔮 التوقعات"},
        {"id": "segmentation", "en": "🎯 Segmentation", "ar": "🎯 تجزئة السياح"},
        {"id": "carbon", "en": "🌱 Carbon Impact", "ar": "🌱 الأثر الكربوني"}
    ]

# ═══════════════════════════════════════════════════════
# TRANSLATIONS
# ═══════════════════════════════════════════════════════
TRANSLATIONS = {
    "EN": {
        "app_title": "Saudi Tourism Intelligence",
        "app_subtitle": "AI-Powered Tourism Analytics Platform",
        "welcome": "Official tourism intelligence platform for Saudi Arabia. Powered by DataSaudi and Vision 2030.",
        "built_by": "Built by",
        "nav_title": "NAVIGATION",
        "dark_mode": "🌙 Dark",
        "light_mode": "☀️ Light",
        "language": "🌐 EN/AR",
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
        "loading": "Loading...",
        "error": "An error occurred",
        "retry": "Retry",
        "developed_by": "Developed with 🇸🇦 by",
        "under_development": "Page under development"
    },
    "AR": {
        "app_title": "الذكاء السياحي السعودي",
        "app_subtitle": "منصة تحليلات سياحية مدعومة بالذكاء الاصطناعي",
        "welcome": "المنصة الرسمية للذكاء السياحي في المملكة العربية السعودية",
        "built_by": "من تطوير",
        "nav_title": "التنقل",
        "dark_mode": "🌙 ليلي",
        "light_mode": "☀️ نهاري",
        "language": "🇸🇦 عربي/EN",
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
        "loading": "جاري التحميل...",
        "error": "حدث خطأ",
        "retry": "إعادة المحاولة",
        "developed_by": "طور بـ 🇸🇦 بواسطة",
        "under_development": "الصفحة قيد التطوير"
    }
}

# ═══════════════════════════════════════════════════════
# INITIALIZE SESSION STATE (مبسط وسريع)
# ═══════════════════════════════════════════════════════
if "lang" not in st.session_state:
    st.session_state.lang = "EN"
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "overview"
if "kpis" not in st.session_state:
    st.session_state.kpis = {
        'total_tourists_2024': 115.8,
        'inbound_2024': 29.7,
        'domestic_2024': 86.2,
        'total_nights_2024': 1.1,
        'avg_spend_2024': 5622,
        'tourists_growth': 8.1,
        'inbound_growth': 8.4,
        'domestic_growth': 5.2,
        'nights_growth': 18.2,
        'spend_growth': 12.8
    }

# ═══════════════════════════════════════════════════════
# CACHED UTILITY FUNCTIONS (للسرعة)
# ═══════════════════════════════════════════════════════
@st.cache_data(ttl=86400, show_spinner=False)
def get_image_base64(image_path):
    """Convert image to base64 with caching"""
    try:
        full_path = Path(__file__).parent / image_path
        if full_path.exists():
            with open(full_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    except Exception:
        pass
    return None

@st.cache_data(ttl=86400, show_spinner=False)
def get_custom_css(theme_colors, lang):
    """Generate custom CSS based on theme and language"""
    
    rtl_css = ""
    if lang == 'AR':
        rtl_css = """
        [dir="rtl"] .stMarkdown { text-align: right; }
        [data-testid="column"] { direction: rtl; }
        """
    
    return f"""
    <style>
        /* Fast loading optimizations */
        .stApp {{ background-color: {theme_colors['bg']}; color: {theme_colors['text']}; }}
        
        /* Metric cards - fast transitions */
        [data-testid="stMetric"] {{
            background-color: {theme_colors['card']};
            border: 1px solid {theme_colors['border']};
            border-radius: 12px;
            padding: 1rem;
            transition: transform 0.2s ease;
        }}
        
        [data-testid="stMetric"]:hover {{
            transform: translateY(-2px);
            background-color: {theme_colors['card_hover']};
        }}
        
        [data-testid="stMetricLabel"] {{
            color: {theme_colors['text_muted']} !important;
            font-size: 0.75rem !important;
        }}
        
        [data-testid="stMetricValue"] {{
            color: {theme_colors['accent']} !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
        }}
        
        /* Main Slider Container - أخضر */
        .main-slider {{
            background: linear-gradient(135deg, {theme_colors['primary']}15, {theme_colors['primary']}05);
            border: 2px solid {theme_colors['primary']}40;
            border-radius: 30px;
            padding: 1.5rem;
            margin: 1rem 0 2rem 0;
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        }}
        
        /* Logo inside slider - في أعلى السلايدر */
        .slider-logo {{
            text-align: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid {theme_colors['primary']}30;
        }}
        
        .slider-logo img {{
            max-width: 200px;
            height: auto;
        }}
        
        /* Controls inside slider */
        .slider-controls {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 1.5rem 0;
            padding: 0.5rem;
        }}
        
        .control-btn {{
            background: {theme_colors['card']};
            border: 1px solid {theme_colors['primary']}40;
            border-radius: 30px;
            padding: 0.6rem 1.5rem;
            color: {theme_colors['text']};
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s ease;
            flex: 1;
            text-align: center;
        }}
        
        .control-btn:hover {{
            border-color: {theme_colors['primary']};
            background: {theme_colors['primary']}20;
            transform: translateY(-2px);
        }}
        
        /* Navigation Title */
        .nav-title {{
            color: {theme_colors['text']};
            font-size: 1rem;
            font-weight: 600;
            margin: 1rem 0;
            padding-left: 0.5rem;
        }}
        
        /* Navigation Grid - أزرار خضراء */
        .nav-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.8rem;
            margin: 1rem 0;
        }}
        
        /* أزرار التنقل الخضراء */
        .nav-btn {{
            background: linear-gradient(135deg, {theme_colors['primary']}20, {theme_colors['primary_dark']}30);
            border: 2px solid {theme_colors['primary']}40;
            border-radius: 16px;
            padding: 1rem 0.5rem;
            color: {theme_colors['text']};
            font-size: 0.9rem;
            font-weight: 500;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        .nav-btn:hover {{
            background: linear-gradient(135deg, {theme_colors['primary']}40, {theme_colors['primary']}30);
            border-color: {theme_colors['accent']};
            transform: translateY(-3px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        }}
        
        .nav-btn.active {{
            background: linear-gradient(135deg, {theme_colors['primary']}60, {theme_colors['primary']}40);
            border-color: {theme_colors['accent']};
            border-left: 4px solid {theme_colors['accent']};
            font-weight: 700;
        }}
        
        /* Profile Card داخل السلايدر */
        .profile-card {{
            background: linear-gradient(135deg, {theme_colors['primary']}20, {theme_colors['secondary']}20);
            border: 1px solid {theme_colors['border']};
            border-radius: 20px;
            padding: 1.5rem;
            margin: 1.5rem 0 0.5rem 0;
            text-align: center;
        }}
        
        .profile-name {{
            color: {theme_colors['accent']};
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
        }}
        
        .profile-links {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 1rem 0;
        }}
        
        .profile-link {{
            background: {theme_colors['card']};
            color: {theme_colors['secondary']};
            text-decoration: none;
            font-size: 0.85rem;
            padding: 0.4rem 1rem;
            border-radius: 30px;
            border: 1px solid {theme_colors['border']};
            transition: all 0.2s ease;
        }}
        
        .profile-link:hover {{
            color: {theme_colors['accent']};
            border-color: {theme_colors['accent']};
            transform: translateY(-2px);
        }}
        
        /* Hero Image - عرض كامل */
        .hero-container {{
            width: 100vw;
            position: relative;
            left: 50%;
            right: 50%;
            margin-left: -50vw;
            margin-right: -50vw;
            margin-bottom: 2rem;
            background: linear-gradient(135deg, {theme_colors['primary']}10, {theme_colors['secondary']}10);
            padding: 2rem 0;
        }}
        
        .hero-image {{
            width: 100%;
            max-height: 400px;
            object-fit: cover;
            object-position: center;
        }}
        
        /* Title under hero */
        .hero-title {{
            text-align: center;
            margin: 2rem 0;
            padding: 0 1rem;
        }}
        
        .hero-title h1 {{
            color: {theme_colors['accent']};
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        .hero-title p {{
            color: {theme_colors['text_muted']};
            font-size: 1.1rem;
            max-width: 800px;
            margin: 0 auto;
        }}
        
        /* Footer */
        .footer {{
            background: {theme_colors['card']};
            border: 1px solid {theme_colors['border']};
            border-radius: 20px;
            padding: 2rem;
            margin-top: 3rem;
            text-align: center;
        }}
        
        /* RTL Support */
        {rtl_css}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .hero-title h1 {{ font-size: 1.8rem; }}
            .nav-grid {{ grid-template-columns: 1fr; }}
            .slider-controls {{ flex-direction: column; }}
        }}
    </style>
    """

# ═══════════════════════════════════════════════════════
# GET COLORS BASED ON THEME
# ═══════════════════════════════════════════════════════
colors = Config.DARK_THEME if st.session_state.theme == 'dark' else Config.LIGHT_THEME

# ═══════════════════════════════════════════════════════
# APPLY CUSTOM CSS (مسكّت مؤقتاً)
# ═══════════════════════════════════════════════════════
st.markdown(get_custom_css(colors, st.session_state.lang), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# HERO IMAGE - FULL WIDTH (أول حاجة)
# ═══════════════════════════════════════════════════════
hero_base64 = get_image_base64("assets/hero.png")
if hero_base64:
    st.markdown(
        f"<div class='hero-container'>"
        f"<img src='data:image/png;base64,{hero_base64}' class='hero-image'>"
        f"</div>",
        unsafe_allow_html=True
    )

# ═══════════════════════════════════════════════════════
# TITLE UNDER HERO
# ═══════════════════════════════════════════════════════
st.markdown(
    f"<div class='hero-title'>"
    f"<h1>{TRANSLATIONS[st.session_state.lang]['app_title']}</h1>"
    f"<p>{TRANSLATIONS[st.session_state.lang]['welcome']}</p>"
    f"</div>",
    unsafe_allow_html=True
)

# ═══════════════════════════════════════════════════════
# MAIN SLIDER - كل حاجة جواه
# ═══════════════════════════════════════════════════════
with st.container():
    st.markdown("<div class='main-slider'>", unsafe_allow_html=True)
    
    # 1. اللوجو في أعلى السلايدر
    logo_base64 = get_image_base64("assets/logo.png")
    if logo_base64:
        st.markdown(
            f"<div class='slider-logo'><img src='data:image/png;base64,{logo_base64}'></div>",
            unsafe_allow_html=True
        )
    
    # 2. أزرار التحكم (ترجمة + Dark/Light)
    st.markdown("<div class='slider-controls'>", unsafe_allow_html=True)
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        theme_icon = "☀️" if st.session_state.theme == 'dark' else "🌙"
        theme_text = TRANSLATIONS[st.session_state.lang]['light_mode' if st.session_state.theme == 'dark' else 'dark_mode']
        if st.button(f"{theme_icon} {theme_text}", key="theme_btn", use_container_width=True):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()
    
    with col_btn2:
        lang_text = "🇬🇧 EN" if st.session_state.lang == 'AR' else "🇸🇦 عربي"
        if st.button(lang_text, key="lang_btn", use_container_width=True):
            st.session_state.lang = 'AR' if st.session_state.lang == 'EN' else 'EN'
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 3. عنوان NAVIGATION
    st.markdown(f"<div class='nav-title'>{TRANSLATIONS[st.session_state.lang]['nav_title']}</div>", unsafe_allow_html=True)
    
    # 4. أزرار التنقل الخضراء (شبكة 2 عمود)
    st.markdown("<div class='nav-grid'>", unsafe_allow_html=True)
    
    # تقسيم الأزرار إلى مجموعتين للعرض بشكل أفضل
    for i in range(0, len(Config.PAGES), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(Config.PAGES):
                page = Config.PAGES[i + j]
                with cols[j]:
                    page_name = page['en'] if st.session_state.lang == 'EN' else page['ar']
                    active_class = "active" if st.session_state.current_page == page['id'] else ""
                    
                    # نستخدم button عادي مع CSS مخصص
                    if st.button(
                        page_name,
                        key=f"nav_{page['id']}",
                        use_container_width=True
                    ):
                        st.session_state.current_page = page['id']
                        st.rerun()
                    
                    # إضافة class للزر النشط
                    if st.session_state.current_page == page['id']:
                        st.markdown(f"""
                        <style>
                            div[data-testid="stButton"]:has(button[key="nav_{page['id']}"]) button {{
                                background: linear-gradient(135deg, {colors['primary']}60, {colors['primary']}40) !important;
                                border-color: {colors['accent']} !important;
                                border-left: 4px solid {colors['accent']} !important;
                                font-weight: 700 !important;
                            }}
                        </style>
                        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 5. اسمي وحساباتي داخل السلايدر
    st.markdown(
        f"<div class='profile-card'>"
        f"<div class='profile-name'>{Config.DEV_NAME}</div>"
        f"<div style='color:{colors['text_muted']}; font-size:0.8rem; margin-bottom:1rem;'>"
        f"{TRANSLATIONS[st.session_state.lang]['developed_by']}</div>"
        f"<div class='profile-links'>"
        f"<a href='{Config.DEV_GITHUB}' target='_blank' class='profile-link'>🐙 GitHub</a>"
        f"<a href='{Config.DEV_LINKEDIN}' target='_blank' class='profile-link'>💼 LinkedIn</a>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True
    )
    
    st.markdown("</div>", unsafe_allow_html=True)  # Close main-slider

# ═══════════════════════════════════════════════════════
# KEY METRICS (بعد السلايدر)
# ═══════════════════════════════════════════════════════
if st.session_state.data_loaded:
    kpis = st.session_state.kpis
    
    metrics = [
        ("total_tourists", f"{kpis.get('total_tourists_2024', 115.8):.1f}M", 
         f"{kpis.get('tourists_growth', 8.1):+.1f}%"),
        ("inbound", f"{kpis.get('inbound_2024', 29.7):.1f}M", 
         f"{kpis.get('inbound_growth', 8.4):+.1f}%"),
        ("domestic", f"{kpis.get('domestic_2024', 86.2):.1f}M", 
         f"{kpis.get('domestic_growth', 5.2):+.1f}%"),
        ("overnight_stays", f"{kpis.get('total_nights_2024', 1.1):.1f}B", 
         f"{kpis.get('nights_growth', 18.2):+.1f}%"),
        ("avg_spend", f"{kpis.get('avg_spend_2024', 5622):,.0f} SAR", 
         f"{kpis.get('spend_growth', 12.8):+.1f}%"),
    ]
    
    cols = st.columns(5)
    for i, (key, value, delta) in enumerate(metrics):
        with cols[i]:
            st.metric(
                label=TRANSLATIONS[st.session_state.lang][key],
                value=value,
                delta=delta
            )

st.divider()

# ═══════════════════════════════════════════════════════
# PAGE ROUTING (سريع)
# ═══════════════════════════════════════════════════════
def load_page(page_name):
    """Dynamically load and render page"""
    try:
        if page_name == "overview":
            from pages.overview import show_overview
            show_overview(None, None, None, None, st.session_state.lang, st.session_state.theme)
        elif page_name == "trends":
            from pages.tourist_trends import show_trends
            show_trends(None, st.session_state.lang, st.session_state.theme)
        elif page_name == "seasonality":
            from pages.seasonality import show_seasonality
            show_seasonality(None, st.session_state.lang, st.session_state.theme)
        elif page_name == "spending":
            from pages.spending import show_spending
            show_spending(None, None, st.session_state.lang, st.session_state.theme)
        elif page_name == "overnight":
            from pages.overnight_stays import show_overnight
            show_overnight(None, None, st.session_state.lang, st.session_state.theme)
        elif page_name == "forecast":
            from pages.forecasting import show_forecast
            show_forecast(None, st.session_state.lang, st.session_state.theme)
        elif page_name == "segmentation":
            from pages.segmentation import show_segmentation
            show_segmentation(None, None, None, st.session_state.lang, st.session_state.theme)
        elif page_name == "carbon":
            from pages.carbon_impact import show_carbon
            show_carbon(None, None, None, st.session_state.lang, st.session_state.theme)
    except ImportError:
        st.info(f"📄 {page_name} - {TRANSLATIONS[st.session_state.lang]['under_development']}")

# Load current page if not overview
if st.session_state.current_page != "overview":
    load_page(st.session_state.current_page)

# ═══════════════════════════════════════════════════════
# FOOTER (سريع)
# ═══════════════════════════════════════════════════════
st.divider()

st.markdown(
    f"<div class='footer'>"
    f"<div style='color:{colors['accent']}; font-weight:700; font-size:1.3rem;'>{Config.DEV_NAME}</div>"
    f"<div style='color:{colors['text_muted']}; margin:0.5rem 0 1rem 0;'>{TRANSLATIONS[st.session_state.lang]['developed_by']}</div>"
    f"<div style='display:flex; justify-content:center; gap:2rem; margin:1rem 0;'>"
    f"<a href='{Config.DEV_GITHUB}' target='_blank' style='color:{colors['secondary']}; text-decoration:none;'>🐙 GitHub</a>"
    f"<a href='{Config.DEV_LINKEDIN}' target='_blank' style='color:{colors['secondary']}; text-decoration:none;'>💼 LinkedIn</a>"
    f"</div>"
    f"<div style='color:{colors['text_muted']}; font-size:0.7rem;'>{TRANSLATIONS[st.session_state.lang]['data_source']} · v{Config.APP_VERSION}</div>"
    f"</div>",
    unsafe_allow_html=True
)
