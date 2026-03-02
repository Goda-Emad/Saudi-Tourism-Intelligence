"""
Saudi Tourism Intelligence - Professional Dashboard
Developed by: Eng. Goda Emad
Version: 3.1.0
Features: Dark/Light Mode, Arabic/English, Responsive Design, Optimized Performance
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
    APP_VERSION = "3.1.0"
    
    # Color Palettes
    DARK_THEME = {
        'bg': '#0D1B2A',
        'card': '#132336',
        'card_hover': '#1A2F45',
        'text': '#F0F4F8',
        'text_muted': '#94A3B8',
        'border': '#2A3F55',
        'primary': '#1B5E20',
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
        'secondary': '#00ACC1',
        'accent': '#E08C00',
        'success': '#2E7D32',
        'warning': '#F57C00',
        'danger': '#C62828'
    }
    
    # Page Names
    PAGES = {
        "overview": {"EN": "🏠 Overview", "AR": "🏠 نظرة عامة"},
        "trends": {"EN": "📈 Tourist Trends", "AR": "📈 اتجاهات السياحة"},
        "seasonality": {"EN": "📅 Seasonality", "AR": "📅 الموسمية"},
        "spending": {"EN": "💰 Spending", "AR": "💰 الإنفاق"},
        "overnight": {"EN": "🏨 Overnight Stays", "AR": "🏨 ليالي الإقامة"},
        "forecast": {"EN": "🔮 Forecasting", "AR": "🔮 التوقعات"},
        "segmentation": {"EN": "🎯 Segmentation", "AR": "🎯 تجزئة السياح"},
        "carbon": {"EN": "🌱 Carbon Impact", "AR": "🌱 الأثر الكربوني"}
    }

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
        "dark_mode": "🌙 Dark Mode",
        "light_mode": "☀️ Light Mode",
        "language": "🌐 Language",
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
        "developed_by": "Developed with 🇸🇦 by"
    },
    "AR": {
        "app_title": "الذكاء السياحي السعودي",
        "app_subtitle": "منصة تحليلات سياحية مدعومة بالذكاء الاصطناعي",
        "welcome": "المنصة الرسمية للذكاء السياحي في المملكة العربية السعودية",
        "built_by": "من تطوير",
        "nav_title": "التنقل",
        "dark_mode": "🌙 الوضع الليلي",
        "light_mode": "☀️ الوضع النهاري",
        "language": "🌐 اللغة",
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
        "developed_by": "طور بـ 🇸🇦 بواسطة"
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
        """
    
    return f"""
    <style>
        /* Main app background */
        .stApp {{
            background-color: {colors['bg']};
            color: {colors['text']};
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {colors['card']};
            border-right: 1px solid {colors['border']};
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
        
        /* Buttons */
        .stButton button {{
            background-color: {colors['primary']};
            color: white;
            border: none;
            border-radius: 8px;
            transition: all 0.3s ease;
        }}
        
        .stButton button:hover {{
            background-color: {colors['secondary']};
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
        
        /* RTL Support */
        {rtl_css}
        
        /* Hero image responsive */
        .hero-image {{
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}
        
        @media (max-width: 768px) {{
            .hero-image {{
                max-width: 120px;
                margin: 0 auto;
            }}
        }}
        
        /* Headers */
        h1 {{
            color: {colors['accent']};
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        h2 {{
            color: {colors['text']};
            font-size: 1.5rem;
            font-weight: 600;
        }}
        
        /* Divider */
        hr {{
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, {colors['accent']}, transparent);
            margin: 2rem 0;
        }}
        
        /* Loading spinner */
        .stSpinner > div {{
            border-top-color: {colors['accent']} !important;
        }}
        
        /* Success/Error messages */
        .stAlert {{
            border-radius: 8px;
            border-left: 4px solid {colors['accent']};
        }}
    </style>
    """

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    # Logo
    logo_base64 = get_image_base64("assets/logo.png")
    if logo_base64:
        st.markdown(
            f"<div style='text-align:center; padding:0.5rem;'>"
            f"<img src='data:image/png;base64,{logo_base64}' style='max-width:160px; height:auto;'>"
            f"</div>",
            unsafe_allow_html=True
        )
    
    # App subtitle
    st.markdown(
        f"<div style='text-align:center; color:{colors['text_muted']}; "
        f"font-size:0.8rem; margin:1rem 0;'>"
        f"{TRANSLATIONS[st.session_state.lang]['app_subtitle']}</div>",
        unsafe_allow_html=True
    )
    
    st.divider()
    
    # Theme Toggle
    theme_label = TRANSLATIONS[st.session_state.lang]['light_mode'] if st.session_state.theme == 'dark' else TRANSLATIONS[st.session_state.lang]['dark_mode']
    if st.button(theme_label, use_container_width=True):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()
    
    # Language Toggle
    lang_label = "🇸🇦 العربية" if st.session_state.lang == "EN" else "🇬🇧 English"
    if st.button(lang_label, use_container_width=True):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"
        st.rerun()
    
    st.divider()
    
    # Navigation
    st.markdown(
        f"<div style='color:{colors['text_muted']}; font-size:0.7rem; "
        f"font-weight:600; margin-bottom:0.5rem;'>"
        f"{TRANSLATIONS[st.session_state.lang]['nav_title']}</div>",
        unsafe_allow_html=True
    )
    
    for page_id, page_names in Config.PAGES.items():
        page_name = page_names[st.session_state.lang]
        if st.button(
            page_name,
            key=f"nav_{page_id}",
            use_container_width=True,
            type="primary" if st.session_state.current_page == page_id else "secondary"
        ):
            st.session_state.current_page = page_id
            st.rerun()
    
    st.divider()
    
    # Developer info
    st.markdown(
        f"<div style='background:{colors['card']}; border:1px solid {colors['border']}; "
        f"border-radius:12px; padding:1rem; text-align:center;'>"
        f"<div style='color:{colors['text_muted']}; font-size:0.75rem;'>"
        f"{TRANSLATIONS[st.session_state.lang]['built_by']}</div>"
        f"<div style='color:{colors['accent']}; font-weight:700; margin:0.3rem 0;'>"
        f"{Config.DEV_NAME}</div>"
        f"<div style='display:flex; justify-content:center; gap:0.5rem;'>"
        f"<a href='{Config.DEV_GITHUB}' target='_blank' style='color:{colors['secondary']}; "
        f"text-decoration:none; font-size:0.75rem;'>🐙 GitHub</a>"
        f"<span style='color:{colors['border']};'>|</span>"
        f"<a href='{Config.DEV_LINKEDIN}' target='_blank' style='color:{colors['secondary']}; "
        f"text-decoration:none; font-size:0.75rem;'>💼 LinkedIn</a>"
        f"</div></div>",
        unsafe_allow_html=True
    )
    
    # Data source info
    st.markdown(
        f"<div style='color:{colors['text_muted']}; font-size:0.65rem; text-align:center; margin-top:1rem;'>"
        f"{TRANSLATIONS[st.session_state.lang]['data_source']}<br>"
        f"{TRANSLATIONS[st.session_state.lang]['last_updated']}</div>",
        unsafe_allow_html=True
    )

# ═══════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════

# Hero section with responsive image
hero_base64 = get_image_base64("assets/hero.png")

# Use columns for responsive layout
col1, col2 = st.columns([2, 1] if st.session_state.lang == 'EN' else [1, 2])

with col1:
    st.markdown(
        f"<h1>{TRANSLATIONS[st.session_state.lang]['app_title']}</h1>"
        f"<p style='color:{colors['text_muted']}; font-size:1rem; margin:1rem 0;'>"
        f"{TRANSLATIONS[st.session_state.lang]['welcome']}</p>"
        f"<div style='display:flex; gap:0.5rem; align-items:center; flex-wrap:wrap;'>"
        f"<span style='color:{colors['text_muted']};'>{TRANSLATIONS[st.session_state.lang]['built_by']}:</span>"
        f"<span style='color:{colors['accent']}; font-weight:700;'>{Config.DEV_NAME}</span>"
        f"</div>",
        unsafe_allow_html=True
    )

with col2:
    if hero_base64:
        # Responsive image sizing
        st.markdown(
            f"<div style='display:flex; justify-content:center; align-items:center; height:100%;'>"
            f"<img src='data:image/png;base64,{hero_base64}' class='hero-image' "
            f"style='max-width:180px; max-height:140px; width:auto; height:auto; border-radius:10px;'>"
            f"</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='display:flex; justify-content:center; align-items:center; height:100%;'>"
            f"<div style='font-size:4rem;'>🇸🇦</div>"
            f"</div>",
            unsafe_allow_html=True
        )

st.divider()

# Key metrics
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
    except ImportError:
        st.info(f"📄 {page_name} page is under development")
    except Exception as e:
        st.error(f"{TRANSLATIONS[st.session_state.lang]['error']}: {str(e)}")

# Load current page if not overview (overview already shown)
if st.session_state.current_page != "overview":
    st.divider()
    load_page(st.session_state.current_page)

# ═══════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════
st.divider()

footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])

with footer_col2:
    st.markdown(
        f"<div style='background:{colors['card']}; border:1px solid {colors['border']}; "
        f"border-radius:16px; padding:2rem; text-align:center; box-shadow:0 4px 12px rgba(0,0,0,0.1);'>"
        f"<div style='color:{colors['accent']}; font-weight:700; font-size:1.3rem; margin-bottom:0.5rem;'>"
        f"{Config.DEV_NAME}</div>"
        f"<div style='color:{colors['text_muted']}; font-size:0.9rem; margin-bottom:1rem;'>"
        f"{TRANSLATIONS[st.session_state.lang]['developed_by']} 🇸🇦</div>"
        f"<div style='display:flex; justify-content:center; gap:2rem; margin:1.5rem 0; flex-wrap:wrap;'>"
        f"<a href='{Config.DEV_GITHUB}' target='_blank' style='color:{colors['secondary']}; "
        f"text-decoration:none; font-size:1rem; display:flex; align-items:center; gap:0.5rem; "
        f"transition:all 0.3s ease;' onmouseover='this.style.color=\"{colors['accent']}\"' "
        f"onmouseout='this.style.color=\"{colors['secondary']}\"'>"
        f"🐙 {TRANSLATIONS[st.session_state.lang]['github']}</a>"
        f"<a href='{Config.DEV_LINKEDIN}' target='_blank' style='color:{colors['secondary']}; "
        f"text-decoration:none; font-size:1rem; display:flex; align-items:center; gap:0.5rem; "
        f"transition:all 0.3s ease;' onmouseover='this.style.color=\"{colors['accent']}\"' "
        f"onmouseout='this.style.color=\"{colors['secondary']}\"'>"
        f"💼 {TRANSLATIONS[st.session_state.lang]['linkedin']}</a>"
        f"</div>"
        f"<div style='color:{colors['text_muted']}; font-size:0.7rem;'>"
        f"{TRANSLATIONS[st.session_state.lang]['data_source']} · "
        f"{TRANSLATIONS[st.session_state.lang]['last_updated']}</div>"
        f"<div style='color:{colors['text_muted']}; font-size:0.65rem; margin-top:0.5rem;'>"
        f"{TRANSLATIONS[st.session_state.lang]['footer_text']} · v{Config.APP_VERSION}</div>"
        f"</div>",
        unsafe_allow_html=True
    )

# ═══════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    pass
