"""
Saudi Tourism Intelligence - Professional Dashboard
Developed by: Eng. Goda Emad
Version: 7.0.0
Features: Dark/Light Mode, Arabic/English, Responsive Design, Green Navigation Cards in Slider
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
    APP_VERSION = "7.0.0"
    
    # Color Palettes
    DARK_THEME = {
        'bg': '#0D1B2A',
        'card': '#132336',
        'card_hover': '#1A2F45',
        'text': '#F0F4F8',
        'text_muted': '#94A3B8',
        'border': '#2A3F55',
        'primary': '#1B5E20',
        'primary_hover': '#2E7D32',
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
        'primary_hover': '#1B5E20',
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
        'kpis': {}
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
            
            return {
                'tourist': tourist_data,
                'spending': spending_data,
                'overnight': overnight_data,
                'carbon': carbon_data,
                'kpis': kpis
            }
        except Exception as e:
            # Fallback to sample data
            return load_sample_data()

# Load data if not loaded
if not st.session_state.data_loaded:
    data = load_data()
    st.session_state.tourist_data = data.get('tourist')
    st.session_state.spending_data = data.get('spending')
    st.session_state.overnight_data = data.get('overnight')
    st.session_state.carbon_data = data.get('carbon')
    st.session_state.kpis = data.get('kpis', {})
    st.session_state.data_loaded = True

# ═══════════════════════════════════════════════════════
# GET CURRENT THEME COLORS
# ═══════════════════════════════════════════════════════
def get_colors():
    """Get colors based on current theme"""
    return Config.DARK_THEME if st.session_state.theme == 'dark' else Config.LIGHT_THEME

colors = get_colors()

# ═══════════════════════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════════════════════
def get_custom_css():
    """Generate custom CSS based on theme"""
    rtl_css = ""
    if st.session_state.lang == 'AR':
        rtl_css = """
        [dir="rtl"] .stMarkdown {
            text-align: right;
        }
        
        [data-testid="column"] {
            direction: rtl;
        }
        """
    
    return f"""
    <style>
        /* Main app background */
        .stApp {{
            background-color: {colors['bg']};
            color: {colors['text']};
        }}
        
        /* Metric cards */
        [data-testid="stMetric"] {{
            background-color: {colors['card']};
            border: 1px solid {colors['border']};
            border-radius: 12px;
            padding: 1rem;
            transition: transform 0.3s ease;
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
        
        /* Top bar with logo and controls */
        .top-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
            margin-bottom: 1rem;
            border-bottom: 1px solid {colors['border']};
        }}
        
        .logo-container {{
            max-width: 200px;
        }}
        
        .logo-container img {{
            max-width: 100%;
            height: auto;
        }}
        
        .controls-container {{
            display: flex;
            gap: 0.5rem;
        }}
        
        .control-btn {{
            background: {colors['card']};
            border: 1px solid {colors['border']};
            border-radius: 30px;
            padding: 0.5rem 1.2rem;
            color: {colors['text']};
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .control-btn:hover {{
            border-color: {colors['primary']};
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        /* Hero image - FULL WIDTH */
        .hero-section {{
            width: 100%;
            margin: 1rem 0 2rem 0;
        }}
        
        .hero-image-container {{
            width: 100%;
            background: linear-gradient(135deg, {colors['primary']}15, {colors['secondary']}15);
            border-radius: 24px;
            padding: 2rem;
            text-align: center;
            border: 1px solid {colors['border']};
        }}
        
        .hero-image {{
            max-width: 100%;
            max-height: 350px;
            width: auto;
            height: auto;
            border-radius: 20px;
            box-shadow: 0 12px 32px rgba(0,0,0,0.2);
        }}
        
        /* Title under hero */
        .main-title {{
            text-align: center;
            margin: 2rem 0 1rem 0;
        }}
        
        .main-title h1 {{
            color: {colors['accent']};
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        .main-title p {{
            color: {colors['text_muted']};
            font-size: 1.1rem;
            max-width: 800px;
            margin: 0 auto;
        }}
        
        /* Slider container - مربعات خضراء */
        .slider-section {{
            background: {colors['card']};
            border: 1px solid {colors['border']};
            border-radius: 24px;
            padding: 1.5rem;
            margin: 1rem 0 2rem 0;
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        }}
        
        .slider-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid {colors['border']};
        }}
        
        .slider-header h3 {{
            color: {colors['text']};
            font-size: 1.1rem;
            font-weight: 600;
            margin: 0;
        }}
        
        .nav-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 0.8rem;
        }}
        
        .nav-card {{
            background: linear-gradient(135deg, {colors['primary']}15, {colors['primary']}05);
            border: 1px solid {colors['primary']}30;
            border-radius: 12px;
            padding: 0.8rem;
            text-align: center;
            color: {colors['text']};
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .nav-card:hover {{
            background: linear-gradient(135deg, {colors['primary']}30, {colors['primary']}20);
            border-color: {colors['accent']};
            transform: translateY(-3px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        }}
        
        .nav-card.active {{
            background: linear-gradient(135deg, {colors['primary']}50, {colors['secondary']}30);
            border-left: 4px solid {colors['primary']};
            border-color: {colors['primary']};
            font-weight: 600;
        }}
        
        /* Profile card */
        .profile-card {{
            background: linear-gradient(135deg, {colors['primary']}15, {colors['secondary']}15);
            border: 1px solid {colors['border']};
            border-radius: 20px;
            padding: 1.5rem;
            margin: 1rem 0;
            text-align: center;
        }}
        
        .profile-name {{
            color: {colors['accent']};
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
            background: {colors['card']};
            color: {colors['secondary']};
            text-decoration: none;
            font-size: 0.85rem;
            padding: 0.4rem 1rem;
            border-radius: 30px;
            border: 1px solid {colors['border']};
            transition: all 0.3s ease;
        }}
        
        .profile-link:hover {{
            color: {colors['accent']};
            border-color: {colors['accent']};
            transform: translateY(-2px);
        }}
        
        /* Footer */
        .footer {{
            background: {colors['card']};
            border: 1px solid {colors['border']};
            border-radius: 20px;
            padding: 2rem;
            margin-top: 3rem;
            text-align: center;
        }}
        
        /* RTL Support */
        {rtl_css}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .hero-image {{
                max-height: 200px;
            }}
            
            .hero-image-container {{
                padding: 1rem;
            }}
            
            .main-title h1 {{
                font-size: 1.8rem;
            }}
            
            .nav-grid {{
                grid-template-columns: 1fr;
            }}
            
            .controls-container {{
                flex-direction: column;
            }}
        }}
    </style>
    """

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# TOP BAR WITH LOGO AND CONTROLS
# ═══════════════════════════════════════════════════════
st.markdown("<div class='top-bar'>", unsafe_allow_html=True)

col_logo, col_controls = st.columns([1, 1])

with col_logo:
    logo_base64 = get_image_base64("assets/logo.png")
    if logo_base64:
        st.markdown(
            f"<div class='logo-container'><img src='data:image/png;base64,{logo_base64}'></div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(f"<h2 style='color:{colors['accent']};'>🇸🇦 STI</h2>", unsafe_allow_html=True)

with col_controls:
    st.markdown("<div class='controls-container'>", unsafe_allow_html=True)
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

st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# HERO IMAGE - FULL WIDTH
# ═══════════════════════════════════════════════════════
hero_base64 = get_image_base64("assets/hero.png")
if hero_base64:
    st.markdown(
        f"<div class='hero-section'>"
        f"<div class='hero-image-container'>"
        f"<img src='data:image/png;base64,{hero_base64}' class='hero-image'>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True
    )

# ═══════════════════════════════════════════════════════
# MAIN TITLE UNDER HERO
# ═══════════════════════════════════════════════════════
st.markdown(
    f"<div class='main-title'>"
    f"<h1>{TRANSLATIONS[st.session_state.lang]['app_title']}</h1>"
    f"<p>{TRANSLATIONS[st.session_state.lang]['welcome']}</p>"
    f"</div>",
    unsafe_allow_html=True
)

# ═══════════════════════════════════════════════════════
# SLIDER SECTION WITH GREEN NAVIGATION CARDS
# ═══════════════════════════════════════════════════════
st.markdown("<div class='slider-section'>", unsafe_allow_html=True)

# Slider header with title and controls
st.markdown(
    f"<div class='slider-header'>"
    f"<h3>{TRANSLATIONS[st.session_state.lang]['nav_title']}</h3>"
    f"</div>",
    unsafe_allow_html=True
)

# Navigation grid
st.markdown("<div class='nav-grid'>", unsafe_allow_html=True)

nav_cols = st.columns(4)  # 4 columns for 8 pages (2 rows)

for idx, page in enumerate(Config.PAGES):
    col_idx = idx % 4
    with nav_cols[col_idx]:
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

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# PROFILE CARD
# ═══════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════
# KEY METRICS
# ═══════════════════════════════════════════════════════
if st.session_state.data_loaded and st.session_state.kpis:
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
        if page_name == "overview" and st.session_state.data_loaded:
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
        else:
            st.info(f"📄 {page_name} - {TRANSLATIONS[st.session_state.lang]['under_development']}")
    except ImportError:
        st.info(f"📄 {page_name} - {TRANSLATIONS[st.session_state.lang]['under_development']}")
    except Exception as e:
        st.error(f"{TRANSLATIONS[st.session_state.lang]['error']}: {str(e)}")

# Load current page
load_page(st.session_state.current_page)

# ═══════════════════════════════════════════════════════
# FOOTER
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

# ═══════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    pass
