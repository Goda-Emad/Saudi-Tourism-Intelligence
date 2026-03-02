"""
Saudi Tourism Intelligence - Professional Dashboard
Developed by: Eng. Goda Emad
Version: 11.0.0
Features: Dark/Light Mode, Arabic/English, Original Colors Restored
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path
import base64

# ═══════════════════════════════════════════════════════
# PAGE CONFIG - MUST BE FIRST
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Saudi Tourism Intelligence",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════
# CONSTANTS & CONFIGURATION
# ═══════════════════════════════════════════════════════
class Config:
    """Application Configuration"""
    DEV_NAME = "Eng. Goda Emad"
    DEV_GITHUB = "https://github.com/Goda-Emad/Saudi-Tourism-Intelligence"
    DEV_LINKEDIN = "https://www.linkedin.com/in/goda-emad/"
    APP_VERSION = "11.0.0"
    
    # Color Palettes - الألوان القديمة الأصلية
    DARK_THEME = {
        'bg': '#0D1B2A',           # الخلفية الأصلية
        'card': '#132336',          # لون الكروت الأصلي
        'card_hover': '#1A2F45',    # لون الكروت عند المرور
        'text': '#F0F4F8',          # لون النص الرئيسي
        'text_muted': '#94A3B8',     # لون النص الثانوي
        'border': '#2A3F55',        # لون الحدود
        'primary': '#1B5E20',       # أخضر غامق
        'primary_light': '#2E7D32',  # أخضر فاتح
        'secondary': '#00838F',      # أزرق
        'accent': '#D4A017',         # ذهبي
        'success': '#43A047',
        'warning': '#F0A500',
        'danger': '#FF5252'
    }
    
    LIGHT_THEME = {
        'bg': '#F4F7FB',            # الخلفية الأصلية للوضع الفاتح
        'card': '#FFFFFF',           # لون الكروت الأصلي
        'card_hover': '#EDF2F7',     # لون الكروت عند المرور
        'text': '#1A2B3C',           # لون النص الرئيسي
        'text_muted': '#4A6080',      # لون النص الثانوي
        'border': '#CBD5E0',         # لون الحدود
        'primary': '#2E7D32',        # أخضر غامق
        'primary_light': '#4CAF50',   # أخضر فاتح
        'secondary': '#00ACC1',       # أزرق
        'accent': '#E08C00',          # ذهبي
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
# INITIALIZE SESSION STATE
# ═══════════════════════════════════════════════════════
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'lang': 'EN',
        'theme': 'dark',
        'data_loaded': False,
        'current_page': 'overview',
        'tourist_data': None,
        'spending_data': None,
        'overnight_data': None,
        'carbon_data': None,
        'kpis': {
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
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ═══════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════
@st.cache_data(ttl=86400)
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

@st.cache_data(ttl=3600)
def load_sample_data():
    """Load sample data for demonstration"""
    years = list(range(2015, 2025))
    inbound = [17.99, 18.04, 16.11, 15.33, 17.53, 4.14, 3.48, 16.64, 27.18, 29.73]
    domestic = [46.45, 45.04, 43.82, 43.26, 47.81, 42.11, 63.83, 77.84, 81.92, 86.16]
    
    return {
        'tourist': pd.DataFrame({
            'Year': years,
            'Inbound': inbound,
            'Domestic': domestic,
            'Total': [i+d for i,d in zip(inbound, domestic)]
        }),
        'kpis': st.session_state.kpis
    }

# ═══════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════
def load_data():
    """Load all required data"""
    with st.spinner(TRANSLATIONS[st.session_state.lang]['loading']):
        try:
            # Try to load from utils
            sys.path.append(str(Path(__file__).parent.parent))
            from utils.data_loader import load_tourist_data, load_spending_data, load_overnight_data, load_carbon_data
            from utils.kpis import calculate_kpis
            
            tourist_data = load_tourist_data()
            spending_data = load_spending_data()
            overnight_data = load_overnight_data()
            carbon_data = load_carbon_data()
            kpis = calculate_kpis(tourist_data, spending_data, overnight_data)
            
            st.session_state.tourist_data = tourist_data
            st.session_state.spending_data = spending_data
            st.session_state.overnight_data = overnight_data
            st.session_state.carbon_data = carbon_data
            st.session_state.kpis = kpis
        except Exception as e:
            # Fallback to sample data
            data = load_sample_data()
            st.session_state.tourist_data = data.get('tourist')
    
    st.session_state.data_loaded = True

# Load data if not loaded
if not st.session_state.data_loaded:
    load_data()

# ═══════════════════════════════════════════════════════
# GET COLORS BASED ON THEME
# ═══════════════════════════════════════════════════════
def get_colors():
    """Get colors based on current theme"""
    return Config.DARK_THEME if st.session_state.theme == 'dark' else Config.LIGHT_THEME

colors = get_colors()

# ═══════════════════════════════════════════════════════
# CUSTOM CSS FOR ORIGINAL COLORS
# ═══════════════════════════════════════════════════════
def get_original_css():
    """Generate custom CSS with original colors"""
    return f"""
    <style>
        /* Main app background - الأصلي */
        .stApp {{
            background-color: {colors['bg']};
            color: {colors['text']};
        }}
        
        /* Sidebar styling - الأصلي */
        [data-testid="stSidebar"] {{
            background-color: {colors['card']};
            border-right: 1px solid {colors['border']};
        }}
        
        [data-testid="stSidebar"] * {{
            color: {colors['text']};
        }}
        
        /* Metric cards - الأصلي */
        [data-testid="stMetric"] {{
            background-color: {colors['card']};
            border: 1px solid {colors['border']};
            border-radius: 12px;
            padding: 1rem;
            transition: transform 0.2s ease;
        }}
        
        [data-testid="stMetric"]:hover {{
            transform: translateY(-2px);
            background-color: {colors['card_hover']};
        }}
        
        [data-testid="stMetricLabel"] {{
            color: {colors['text_muted']} !important;
            font-size: 0.75rem !important;
        }}
        
        [data-testid="stMetricValue"] {{
            color: {colors['accent']} !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
        }}
        
        /* Navigation buttons - خضراء فقط */
        .stButton button {{
            background: {colors['primary']}20 !important;
            border: 1px solid {colors['primary']}40 !important;
            border-radius: 12px !important;
            padding: 0.8rem 1rem !important;
            margin: 0.3rem 0 !important;
            color: {colors['text']} !important;
            font-size: 0.95rem !important;
            text-align: left !important;
            width: 100% !important;
            transition: all 0.3s ease !important;
        }}
        
        .stButton button:hover {{
            background: {colors['primary']}40 !important;
            border-color: {colors['accent']} !important;
            transform: translateX(5px) !important;
        }}
        
        .stButton button[kind="primary"] {{
            background: {colors['primary']}60 !important;
            border-left: 4px solid {colors['accent']} !important;
            font-weight: 700 !important;
        }}
        
        /* Hero banner */
        .hero-banner {{
            width: 100%;
            margin-bottom: 2rem;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .hero-banner img {{
            width: 100%;
            height: 300px;
            object-fit: cover;
            object-position: center;
        }}
        
        /* Divider */
        hr {{
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, {colors['accent']}, transparent);
            margin: 2rem 0;
        }}
        
        /* RTL support */
        {f'''
        [dir="rtl"] .stButton button {{
            text-align: right !important;
        }}
        ''' if st.session_state.lang == 'AR' else ''}
    </style>
    """

# Apply CSS
st.markdown(get_original_css(), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# HERO BANNER
# ═══════════════════════════════════════════════════════
hero_base64 = get_image_base64("assets/hero.png")
if hero_base64:
    st.markdown(
        f"""
        <div class="hero-banner">
            <img src="data:image/png;base64,{hero_base64}">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"""
        <div style="
            width: 100%;
            height: 300px;
            margin-bottom: 2rem;
            background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']});
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2rem;
            font-weight: 700;
        ">
            🇸🇦 Saudi Tourism Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    # Logo
    logo_base64 = get_image_base64("assets/logo.png")
    if logo_base64:
        st.image(f"data:image/png;base64,{logo_base64}", use_column_width=True)
    else:
        st.markdown(f"<h2 style='color:{colors['accent']}; text-align:center;'>🇸🇦 STI</h2>", unsafe_allow_html=True)
    
    st.divider()
    
    # Theme and Language controls
    col1, col2 = st.columns(2)
    with col1:
        theme_icon = "☀️" if st.session_state.theme == 'dark' else "🌙"
        theme_text = "Light" if st.session_state.theme == 'dark' else "Dark"
        if st.button(f"{theme_icon} {theme_text}", key="theme_btn", use_container_width=True):
            st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
            st.rerun()
    
    with col2:
        lang_text = "🇬🇧 EN" if st.session_state.lang == 'AR' else "🇸🇦 عربي"
        if st.button(lang_text, key="lang_btn", use_container_width=True):
            st.session_state.lang = 'AR' if st.session_state.lang == 'EN' else 'EN'
            st.rerun()
    
    st.divider()
    
    # Navigation title
    st.markdown(f"<p style='color:{colors['text_muted']}; font-size:0.8rem; font-weight:600;'>{TRANSLATIONS[st.session_state.lang]['nav_title']}</p>", unsafe_allow_html=True)
    
    # Navigation buttons - خضراء فقط
    for page in Config.PAGES:
        page_name = page['en'] if st.session_state.lang == 'EN' else page['ar']
        btn_type = "primary" if st.session_state.current_page == page['id'] else "secondary"
        
        if st.button(
            page_name,
            key=f"nav_{page['id']}",
            use_container_width=True,
            type=btn_type
        ):
            st.session_state.current_page = page['id']
            st.rerun()
    
    st.divider()
    
    # Developer profile
    st.markdown(
        f"""
        <div style="
            background: {colors['card']};
            border: 1px solid {colors['border']};
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            margin-top: 1rem;
        ">
            <div style="color: {colors['accent']}; font-weight: 700; font-size: 1.1rem;">{Config.DEV_NAME}</div>
            <div style="color: {colors['text_muted']}; font-size: 0.8rem; margin: 0.5rem 0;">{TRANSLATIONS[st.session_state.lang]['developed_by']}</div>
            <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1rem;">
                <a href="{Config.DEV_GITHUB}" target="_blank" style="color: {colors['secondary']}; text-decoration: none;">🐙 GitHub</a>
                <a href="{Config.DEV_LINKEDIN}" target="_blank" style="color: {colors['secondary']}; text-decoration: none;">💼 LinkedIn</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ═══════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════

# Title
st.markdown(
    f"<h1 style='color:{colors['accent']}; text-align:center; margin-bottom:0.5rem;'>{TRANSLATIONS[st.session_state.lang]['app_title']}</h1>"
    f"<p style='color:{colors['text_muted']}; text-align:center; margin-bottom:2rem;'>{TRANSLATIONS[st.session_state.lang]['welcome']}</p>",
    unsafe_allow_html=True
)

# Key metrics
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
# PAGE ROUTING
# ═══════════════════════════════════════════════════════
def load_page(page_name):
    """Dynamically load and render page"""
    try:
        if page_name == "overview":
            from pages.overview import show_overview
            show_overview(
                st.session_state.tourist_data,
                st.session_state.spending_data,
                st.session_state.overnight_data,
                st.session_state.carbon_data,
                st.session_state.lang,
                st.session_state.theme
            )
        elif page_name == "trends":
            from pages.tourist_trends import show_trends
            show_trends(
                st.session_state.tourist_data,
                st.session_state.lang,
                st.session_state.theme
            )
        elif page_name == "seasonality":
            from pages.seasonality import show_seasonality
            show_seasonality(
                st.session_state.tourist_data,
                st.session_state.lang,
                st.session_state.theme
            )
        elif page_name == "spending":
            from pages.spending import show_spending
            show_spending(
                st.session_state.spending_data,
                st.session_state.tourist_data,
                st.session_state.lang,
                st.session_state.theme
            )
        elif page_name == "overnight":
            from pages.overnight_stays import show_overnight
            show_overnight(
                st.session_state.overnight_data,
                st.session_state.tourist_data,
                st.session_state.lang,
                st.session_state.theme
            )
        elif page_name == "forecast":
            from pages.forecasting import show_forecast
            show_forecast(
                st.session_state.tourist_data,
                st.session_state.lang,
                st.session_state.theme
            )
        elif page_name == "segmentation":
            from pages.segmentation import show_segmentation
            show_segmentation(
                st.session_state.tourist_data,
                st.session_state.spending_data,
                st.session_state.overnight_data,
                st.session_state.lang,
                st.session_state.theme
            )
        elif page_name == "carbon":
            from pages.carbon_impact import show_carbon
            show_carbon(
                st.session_state.carbon_data,
                st.session_state.tourist_data,
                st.session_state.overnight_data,
                st.session_state.lang,
                st.session_state.theme
            )
    except ImportError:
        st.info(f"📄 {page_name} - {TRANSLATIONS[st.session_state.lang]['under_development']}")

# Load current page if not overview
if st.session_state.current_page != "overview":
    load_page(st.session_state.current_page)

# ═══════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════
st.divider()

st.markdown(
    f"""
    <div style="
        text-align: center;
        padding: 2rem;
        background: {colors['card']};
        border: 1px solid {colors['border']};
        border-radius: 16px;
        margin-top: 2rem;
    ">
        <div style="color: {colors['accent']}; font-weight: 700; font-size: 1.2rem;">{Config.DEV_NAME}</div>
        <div style="color: {colors['text_muted']}; font-size: 0.8rem; margin: 0.5rem 0;">{TRANSLATIONS[st.session_state.lang]['developed_by']}</div>
        <div style="color: {colors['text_muted']}; font-size: 0.7rem;">{TRANSLATIONS[st.session_state.lang]['data_source']} · v{Config.APP_VERSION}</div>
    </div>
    """,
    unsafe_allow_html=True
)
