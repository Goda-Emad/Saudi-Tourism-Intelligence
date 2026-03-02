"""
Saudi Tourism Intelligence - Main Application
Professional Dashboard for Tourism Analytics
Developed by: Eng. Goda Emad
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
    APP_VERSION = "2.0.0"
    
    # Color Palette
    COLORS = {
        'primary': '#1B5E20',      # Saudi Green
        'secondary': '#00838F',     # Red Sea Teal
        'accent': '#D4A017',        # Desert Gold
        'success': '#43A047',
        'warning': '#F0A500',
        'danger': '#FF5252',
        'dark': '#0D1B2A',
        'card': '#132336',
        'text': '#F0F4F8',
        'text_muted': '#94A3B8',
        'border': '#2A3F55'
    }
    
    # Page Names
    PAGES = {
        "overview": "🏠 Overview",
        "trends": "📈 Tourist Trends",
        "seasonality": "📅 Seasonality",
        "spending": "💰 Spending",
        "overnight": "🏨 Overnight Stays",
        "forecast": "🔮 Forecasting",
        "segmentation": "🎯 Segmentation",
        "carbon": "🌱 Carbon Impact"
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
        "retry": "Retry"
    },
    "AR": {
        "app_title": "الذكاء السياحي السعودي",
        "app_subtitle": "منصة تحليلات سياحية مدعومة بالذكاء الاصطناعي",
        "welcome": "المنصة الرسمية للذكاء السياحي في المملكة العربية السعودية",
        "built_by": "من تطوير",
        "nav_title": "التنقل",
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
        "retry": "إعادة المحاولة"
    }
}

# ═══════════════════════════════════════════════════════
# INITIALIZE SESSION STATE
# ═══════════════════════════════════════════════════════
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'lang': 'EN',
        'data_loaded': False,
        'current_page': 'overview',
        'tourist_data': None,
        'spending_data': None,
        'overnight_data': None,
        'carbon_data': None
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
def load_css():
    """Load custom CSS with caching"""
    css_file = Path(__file__).parent / "assets" / "style.css"
    if css_file.exists():
        with open(css_file, 'r', encoding='utf-8') as f:
            return f"<style>{f.read()}</style>"
    return ""

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
            # Try to load from utils first
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
        except Exception:
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
# APPLY CUSTOM CSS
# ═══════════════════════════════════════════════════════
st.markdown(load_css(), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    # Logo
    logo_base64 = get_image_base64("assets/logo.png")
    if logo_base64:
        st.markdown(
            f"<div style='text-align:center; padding:0.5rem;'>"
            f"<img src='data:image/png;base64,{logo_base64}' style='max-width:160px;'>"
            f"</div>",
            unsafe_allow_html=True
        )
    
    # App subtitle
    st.markdown(
        f"<div style='text-align:center; color:{Config.COLORS['text_muted']}; "
        f"font-size:0.8rem; margin-bottom:1rem;'>"
        f"{TRANSLATIONS[st.session_state.lang]['app_subtitle']}</div>",
        unsafe_allow_html=True
    )
    
    st.divider()
    
    # Language toggle
    lang_button = "🇸🇦 العربية" if st.session_state.lang == "EN" else "🇬🇧 English"
    if st.button(lang_button, use_container_width=True):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"
        st.rerun()
    
    st.divider()
    
    # Navigation
    st.markdown(
        f"<div style='color:{Config.COLORS['text_muted']}; font-size:0.7rem; "
        f"font-weight:600; margin-bottom:0.5rem;'>"
        f"{TRANSLATIONS[st.session_state.lang]['nav_title']}</div>",
        unsafe_allow_html=True
    )
    
    for page_id, page_name in Config.PAGES.items():
        if st.button(
            page_name,
            key=f"nav_{page_id}",
            use_container_width=True,
            type="secondary" if st.session_state.current_page != page_id else "primary"
        ):
            st.session_state.current_page = page_id
            st.rerun()
    
    st.divider()
    
    # Developer info
    st.markdown(
        f"<div style='background:{Config.COLORS['card']}; border:1px solid {Config.COLORS['border']}; "
        f"border-radius:12px; padding:1rem; text-align:center;'>"
        f"<div style='color:{Config.COLORS['text_muted']}; font-size:0.75rem;'>"
        f"{TRANSLATIONS[st.session_state.lang]['built_by']}</div>"
        f"<div style='color:{Config.COLORS['accent']}; font-weight:700; margin:0.3rem 0;'>"
        f"{Config.DEV_NAME}</div>"
        f"<div style='display:flex; justify-content:center; gap:0.5rem;'>"
        f"<a href='{Config.DEV_GITHUB}' target='_blank' style='color:{Config.COLORS['secondary']}; "
        f"text-decoration:none; font-size:0.75rem;'>🐙 GitHub</a>"
        f"<span style='color:{Config.COLORS['border']};'>|</span>"
        f"<a href='{Config.DEV_LINKEDIN}' target='_blank' style='color:{Config.COLORS['secondary']}; "
        f"text-decoration:none; font-size:0.75rem;'>💼 LinkedIn</a>"
        f"</div></div>",
        unsafe_allow_html=True
    )

# ═══════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════

# Hero section
hero_base64 = get_image_base64("assets/hero.png")
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(
        f"<h1 style='color:{Config.COLORS['accent']}; margin:0; font-size:2.2rem;'>"
        f"{TRANSLATIONS[st.session_state.lang]['app_title']}</h1>"
        f"<p style='color:{Config.COLORS['text_muted']}; margin:0.5rem 0;'>"
        f"{TRANSLATIONS[st.session_state.lang]['welcome']}</p>"
        f"<div style='color:{Config.COLORS['text_muted']}; font-size:0.8rem;'>"
        f"{TRANSLATIONS[st.session_state.lang]['built_by']}: "
        f"<span style='color:{Config.COLORS['accent']}; font-weight:700;'>{Config.DEV_NAME}</span></div>",
        unsafe_allow_html=True
    )

with col2:
    if hero_base64:
        st.markdown(
            f"<img src='data:image/png;base64,{hero_base64}' "
            f"style='max-width:150px; max-height:120px; border-radius:10px; float:right;'>",
            unsafe_allow_html=True
        )

# Key metrics
if st.session_state.data_loaded and hasattr(st.session_state, 'kpis'):
    kpis = st.session_state.kpis
    
    metrics = [
        ("total_tourists", f"{kpis.get('total_tourists_2024', 115.8):.1f}M", 
         f"{kpis.get('tourists_growth', 8.1):.1f}%"),
        ("inbound", f"{kpis.get('inbound_2024', 29.7):.1f}M", 
         f"{kpis.get('inbound_growth', 8.4):.1f}%"),
        ("domestic", f"{kpis.get('domestic_2024', 86.2):.1f}M", 
         f"{kpis.get('domestic_growth', 5.2):.1f}%"),
        ("overnight_stays", f"{kpis.get('total_nights_2024', 1.1):.1f}B", 
         f"{kpis.get('nights_growth', 18.2):.1f}%"),
        ("avg_spend", f"{kpis.get('avg_spend_2024', 5622):.0f} SAR", 
         f"{kpis.get('spend_growth', 12.8):.1f}%"),
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
                st.session_state.lang
            )
        elif page_name == "trends":
            from pages.tourist_trends import show_trends
            show_trends(st.session_state.tourist_data, st.session_state.lang)
        elif page_name == "seasonality":
            from pages.seasonality import show_seasonality
            show_seasonality(st.session_state.tourist_data, st.session_state.lang)
        elif page_name == "spending":
            from pages.spending import show_spending
            show_spending(st.session_state.spending_data, st.session_state.tourist_data, st.session_state.lang)
        elif page_name == "overnight":
            from pages.overnight_stays import show_overnight
            show_overnight(st.session_state.overnight_data, st.session_state.tourist_data, st.session_state.lang)
        elif page_name == "forecast":
            from pages.forecasting import show_forecast
            show_forecast(st.session_state.tourist_data, st.session_state.lang)
        elif page_name == "segmentation":
            from pages.segmentation import show_segmentation
            show_segmentation(
                st.session_state.tourist_data,
                st.session_state.spending_data,
                st.session_state.overnight_data,
                st.session_state.lang
            )
        elif page_name == "carbon":
            from pages.carbon_impact import show_carbon
            show_carbon(
                st.session_state.carbon_data,
                st.session_state.tourist_data,
                st.session_state.overnight_data,
                st.session_state.lang
            )
    except ImportError as e:
        st.info(f"📄 Page '{page_name}' is under development")
    except Exception as e:
        st.error(f"Error loading page: {str(e)}")

# Load current page
load_page(st.session_state.current_page)

# ═══════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════
st.divider()

footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])

with footer_col2:
    st.markdown(
        f"<div style='background:{Config.COLORS['card']}; border:1px solid {Config.COLORS['border']}; "
        f"border-radius:12px; padding:1.5rem; text-align:center;'>"
        f"<div style='color:{Config.COLORS['accent']}; font-weight:700; font-size:1.2rem; margin-bottom:0.5rem;'>"
        f"{Config.DEV_NAME}</div>"
        f"<div style='margin-bottom:0.8rem;'>"
        f"<a href='{Config.DEV_GITHUB}' target='_blank' style='color:{Config.COLORS['secondary']}; "
        f"text-decoration:none; margin:0 10px;'>🐙 GitHub</a>"
        f"<span style='color:{Config.COLORS['border']};'>|</span>"
        f"<a href='{Config.DEV_LINKEDIN}' target='_blank' style='color:{Config.COLORS['secondary']}; "
        f"text-decoration:none; margin:0 10px;'>💼 LinkedIn</a>"
        f"</div>"
        f"<div style='color:{Config.COLORS['text_muted']}; font-size:0.7rem;'>"
        f"{TRANSLATIONS[st.session_state.lang]['data_source']} · "
        f"{TRANSLATIONS[st.session_state.lang]['last_updated']}</div>"
        f"<div style='color:{Config.COLORS['text_muted']}; font-size:0.65rem; margin-top:0.5rem;'>"
        f"{TRANSLATIONS[st.session_state.lang]['footer_text']} · v{Config.APP_VERSION}</div>"
        f"</div>",
        unsafe_allow_html=True
    )

# ═══════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    # Already running
    pass
