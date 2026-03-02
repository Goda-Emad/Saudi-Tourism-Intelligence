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
from utils.kpis import (
    load_all_data,
    calculate_kpis,
    format_number,
    get_yoy_growth
)
from utils.charts import (
    create_trend_chart,
    create_comparison_chart,
    create_heatmap,
    create_pie_chart,
    create_radar_chart,
    create_bar_chart,
    create_line_chart,
    create_area_chart,
    create_forecast_chart,
    create_carbon_chart,
    create_segment_chart
)
from utils.data_loader import (
    load_tourist_data,
    load_spending_data,
    load_overnight_data,
    load_carbon_data
)

# ═══════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════
def get_image_base64(image_path):
    """تحويل الصورة إلى base64 لإدراجها في HTML"""
    try:
        full_path = Path(__file__).parent / image_path
        if full_path.exists():
            with open(full_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        return ""
    except:
        return ""

def resize_image_base64(base64_string, max_width=200, max_height=150):
    """إضافة CSS لتحجيم الصورة"""
    return f"""
    <style>
    .hero-image {{
        max-width: {max_width}px;
        max-height: {max_height}px;
        width: auto;
        height: auto;
        object-fit: contain;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }}
    </style>
    <img src='data:image/png;base64,{base64_string}' class='hero-image'>
    """

# ═══════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Saudi Tourism Intelligence",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════
# DEVELOPER INFO
# ═══════════════════════════════════════════════════════
DEV_NAME = "Eng. Goda Emad"
DEV_GITHUB = "https://github.com/Goda-Emad/Saudi-Tourism-Intelligence/tree/main"
DEV_LINKEDIN = "https://www.linkedin.com/in/goda-emad/"

# ═══════════════════════════════════════════════════════
# LOAD CUSTOM CSS
# ═══════════════════════════════════════════════════════
def load_css():
    """تحميل ملف CSS المخصص"""
    css_file = Path(__file__).parent / "assets" / "style.css"
    if css_file.exists():
        with open(css_file, 'r', encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        /* Fallback CSS if file not found */
        .hero-banner {
            background: linear-gradient(135deg, #1B5E20 0%, #00838F 100%);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: #132336;
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)

load_css()

# ═══════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════
if "lang" not in st.session_state:
    st.session_state.lang = "EN"
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "overview"

# ═══════════════════════════════════════════════════════
# TRANSLATIONS
# ═══════════════════════════════════════════════════════
T = {
    "EN": {
        "app_title": "Saudi Tourism Intelligence",
        "app_subtitle": "AI-Powered Tourism Analytics Platform",
        "welcome": "Welcome to the official tourism intelligence platform for Saudi Arabia. Powered by DataSaudi and Vision 2030.",
        "built_by": "Built by",
        "developer": "Eng. Goda Emad",
        "dark_mode": "🌙 Dark",
        "light_mode": "☀️ Light",
        "lang_toggle": "🌐 العربية",
        "nav_title": "Navigation",
        "overview": "🏠 Overview",
        "trends": "📈 Tourist Trends",
        "seasonality": "📅 Seasonality",
        "spending": "💰 Spending",
        "overnight": "🏨 Overnight Stays",
        "forecast": "🔮 Forecasting",
        "segmentation": "🎯 Segmentation",
        "carbon": "🌱 Carbon Impact",
        "select_page": "Select a page",
        "last_updated": "Last updated: March 2025",
        "data_source": "Data Source: DataSaudi · Ministry of Tourism",
        "key_metrics": "Key Metrics 2024",
        "total_tourists": "Total Tourists",
        "inbound": "Inbound",
        "domestic": "Domestic",
        "overnight_stays": "Overnight Stays",
        "avg_spend": "Avg Spend",
        "footer_text": "© 2025 Saudi Tourism Intelligence · All rights reserved",
        "github": "GitHub",
        "linkedin": "LinkedIn",
        "view_project": "View Project",
        "connect": "Connect",
    },
    "AR": {
        "app_title": "الذكاء السياحي السعودي",
        "app_subtitle": "منصة تحليلات سياحية مدعومة بالذكاء الاصطناعي",
        "welcome": "مرحباً بكم في المنصة الرسمية للذكاء السياحي في المملكة العربية السعودية. مدعومة من DataSaudi ورؤية 2030.",
        "built_by": "من تطوير",
        "developer": "م. جودة عماد",
        "dark_mode": "🌙 داكن",
        "light_mode": "☀️ فاتح",
        "lang_toggle": "🌐 English",
        "nav_title": "التنقل",
        "overview": "🏠 نظرة عامة",
        "trends": "📈 اتجاهات السياحة",
        "seasonality": "📅 الموسمية",
        "spending": "💰 الإنفاق",
        "overnight": "🏨 ليالي الإقامة",
        "forecast": "🔮 التوقعات",
        "segmentation": "🎯 تجزئة السياح",
        "carbon": "🌱 الأثر الكربوني",
        "select_page": "اختر الصفحة",
        "last_updated": "آخر تحديث: مارس 2025",
        "data_source": "مصدر البيانات: DataSaudi · وزارة السياحة",
        "key_metrics": "المؤشرات الرئيسية 2024",
        "total_tourists": "إجمالي السياح",
        "inbound": "وافدون",
        "domestic": "محليون",
        "overnight_stays": "ليالي الإقامة",
        "avg_spend": "متوسط الإنفاق",
        "footer_text": "© 2025 الذكاء السياحي السعودي · جميع الحقوق محفوظة",
        "github": "جيت هاب",
        "linkedin": "لينكد إن",
        "view_project": "عرض المشروع",
        "connect": "تواصل",
    }
}

# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    # Logo with proper sizing
    logo_base64 = get_image_base64("assets/logo.png")
    if logo_base64:
        st.markdown(f"""
        <div style='text-align: center; padding: 0.5rem;'>
            <img src='data:image/png;base64,{logo_base64}' style='max-width: 180px; height: auto;'>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='text-align:center; padding: 1rem;'>
            <span style='font-size: 2.5rem;'>🇸🇦</span>
            <div style='color: #D4A017; font-weight: 700; font-size: 1.2rem;'>Saudi Tourism</div>
            <div style='color: white; font-weight: 600;'>INTELLIGENCE</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='text-align:center; font-size:0.8rem; color: #94A3B8; margin-bottom: 1rem;'>
        {T[st.session_state.lang]['app_subtitle']}
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Theme and Language Toggles
    col1, col2 = st.columns(2)
    with col1:
        if st.button(T[st.session_state.lang]["dark_mode"] if st.session_state.theme == "dark" else T[st.session_state.lang]["light_mode"], use_container_width=True):
            st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
            st.rerun()
    with col2:
        if st.button(T[st.session_state.lang]["lang_toggle"], use_container_width=True):
            st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"
            st.rerun()
    
    st.divider()
    
    # Navigation
    st.markdown(f"""
    <div style='font-size:0.7rem; font-weight:600; color: #94A3B8; text-transform:uppercase; margin-bottom:0.5rem;'>
        {T[st.session_state.lang]['nav_title']}
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
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
    
    # Data info
    st.markdown(f"""
    <div style='font-size:0.7rem; color: #94A3B8;'>
        <div style='margin-bottom:0.5rem;'>
            <span style='color: #43A047;'>📊</span> {T[st.session_state.lang]['data_source']}
        </div>
        <div>
            <span style='color: #43A047;'>🔄</span> {T[st.session_state.lang]['last_updated']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Developer Profile
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, rgba(27,94,32,0.2) 0%, rgba(0,131,143,0.2) 100%);
        border: 1px solid rgba(0,131,143,0.4);
        border-radius: 16px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        text-align: center;
    '>
        <div style='
            font-size: 0.8rem;
            color: #94A3B8;
            margin-bottom: 0.3rem;
        '>
            {T[st.session_state.lang]['built_by']}
        </div>
        <div style='
            font-size: 1.1rem;
            font-weight: 700;
            color: #D4A017;
            font-family: "Playfair Display", serif;
            margin-bottom: 0.8rem;
        '>
            {DEV_NAME}
        </div>
        
        <div style='
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 0.5rem;
        '>
            <a href="{DEV_GITHUB}" target="_blank" style='
                text-decoration: none;
                background: #132336;
                color: #F0F4F8;
                padding: 0.4rem 1rem;
                border-radius: 20px;
                font-size: 0.75rem;
                border: 1px solid rgba(0,131,143,0.4);
                display: inline-flex;
                align-items: center;
                gap: 4px;
            '>
                🐙 {T[st.session_state.lang]['github']}
            </a>
            <a href="{DEV_LINKEDIN}" target="_blank" style='
                text-decoration: none;
                background: #132336;
                color: #F0F4F8;
                padding: 0.4rem 1rem;
                border-radius: 20px;
                font-size: 0.75rem;
                border: 1px solid rgba(0,131,143,0.4);
                display: inline-flex;
                align-items: center;
                gap: 4px;
            '>
                💼 {T[st.session_state.lang]['linkedin']}
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════

# Load data
@st.cache_data
def load_all_cached_data():
    """تحميل جميع البيانات مع التخزين المؤقت"""
    tourist_data = load_tourist_data()
    spending_data = load_spending_data()
    overnight_data = load_overnight_data()
    carbon_data = load_carbon_data()
    return tourist_data, spending_data, overnight_data, carbon_data

try:
    tourist_data, spending_data, overnight_data, carbon_data = load_all_cached_data()
    st.session_state.data_loaded = True
except Exception as e:
    st.error(f"⚠️ خطأ في تحميل البيانات: {str(e)}")
    st.session_state.data_loaded = False

# Hero Banner with properly sized Hero Image
hero_base64 = get_image_base64("assets/hero.png")

# Hero section with two columns
col_hero_left, col_hero_right = st.columns([3, 1])

with col_hero_left:
    st.markdown(f"""
    <div style='padding: 1rem 0;'>
        <h1 style='
            margin:0; 
            font-size:2.2rem; 
            background: linear-gradient(135deg, #FFFFFF, #D4A017);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        '>{T[st.session_state.lang]['app_title']}</h1>
        <p style='font-size:1rem; color: #94A3B8; max-width:600px; margin: 1rem 0;'>
            {T[st.session_state.lang]['welcome']}
        </p>
        <div style='
            background: rgba(255,255,255,0.05);
            border-radius: 30px;
            padding: 0.5rem 1.2rem;
            border: 1px solid rgba(0,131,143,0.4);
            display: inline-block;
        '>
            <span style='color: #94A3B8; font-size:0.8rem;'>{T[st.session_state.lang]['built_by']}: </span>
            <span style='color: #D4A017; font-weight:700;'>{DEV_NAME}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_hero_right:
    if hero_base64:
        # صورة بحجم مناسب ومضبوط
        st.markdown(f"""
        <div style='display: flex; justify-content: center; align-items: center; height: 100%; padding: 0.5rem;'>
            <img src='data:image/png;base64,{hero_base64}' 
                 style='
                    max-width: 180px;
                    max-height: 140px;
                    width: auto;
                    height: auto;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                 '>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 100%;'>
            <div style='text-align:center; padding: 1rem; background: #132336; border-radius: 12px;'>
                <span style='font-size: 3rem;'>🏝️</span>
                <p style='color: #94A3B8; margin:0;'>Saudi Tourism</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Key Metrics Row (if data loaded)
if st.session_state.data_loaded:
    kpis = calculate_kpis(tourist_data, spending_data, overnight_data)
    
    # Custom CSS for metrics
    st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background: #132336;
        border: 1px solid rgba(0,131,143,0.4);
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 0.75rem !important;
    }
    [data-testid="stMetricValue"] {
        color: #D4A017 !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label=T[st.session_state.lang]["total_tourists"],
            value=f"{kpis['total_tourists_2024']:.1f}M",
            delta=f"{kpis['tourists_growth']:.1f}%",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label=T[st.session_state.lang]["inbound"],
            value=f"{kpis['inbound_2024']:.1f}M",
            delta=f"{kpis['inbound_growth']:.1f}%",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label=T[st.session_state.lang]["domestic"],
            value=f"{kpis['domestic_2024']:.1f}M",
            delta=f"{kpis['domestic_growth']:.1f}%",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label=T[st.session_state.lang]["overnight_stays"],
            value=f"{kpis['total_nights_2024']:.1f}B",
            delta=f"{kpis['nights_growth']:.1f}%",
            delta_color="normal"
        )
    
    with col5:
        st.metric(
            label=T[st.session_state.lang]["avg_spend"],
            value=f"{kpis['avg_spend_2024']:.0f} SAR",
            delta=f"{kpis['spend_growth']:.1f}%",
            delta_color="normal"
        )
    
    st.divider()

# ═══════════════════════════════════════════════════════
# PAGE ROUTING
# ═══════════════════════════════════════════════════════

current_page = st.session_state.current_page

if current_page == "overview":
    if st.session_state.data_loaded:
        try:
            from pages.overview import show_overview
            show_overview(tourist_data, spending_data, overnight_data, carbon_data, st.session_state.lang, st.session_state.theme)
        except ImportError as e:
            st.info(f"📊 صفحة Overview جاري تجهيزها...")
    else:
        st.info("📊 يرجى التأكد من وجود ملفات البيانات في المجلد data/clean/")
        
elif current_page == "trends":
    try:
        from pages.tourist_trends import show_trends
        show_trends(tourist_data, st.session_state.lang, st.session_state.theme)
    except ImportError as e:
        st.info(f"📈 صفحة Tourist Trends جاري تجهيزها...")
    
elif current_page == "seasonality":
    try:
        from pages.seasonality import show_seasonality
        show_seasonality(tourist_data, st.session_state.lang, st.session_state.theme)
    except ImportError as e:
        st.info(f"📅 صفحة Seasonality جاري تجهيزها...")
    
elif current_page == "spending":
    try:
        from pages.spending import show_spending
        show_spending(spending_data, tourist_data, st.session_state.lang, st.session_state.theme)
    except ImportError as e:
        st.info(f"💰 صفحة Spending جاري تجهيزها...")
    
elif current_page == "overnight":
    try:
        from pages.overnight_stays import show_overnight
        show_overnight(overnight_data, tourist_data, st.session_state.lang, st.session_state.theme)
    except ImportError as e:
        st.info(f"🏨 صفحة Overnight Stays جاري تجهيزها...")
    
elif current_page == "forecast":
    try:
        from pages.forecasting import show_forecast
        show_forecast(tourist_data, st.session_state.lang, st.session_state.theme)
    except ImportError as e:
        st.info(f"🔮 صفحة Forecasting جاري تجهيزها...")
    
elif current_page == "segmentation":
    try:
        from pages.segmentation import show_segmentation
        show_segmentation(tourist_data, spending_data, overnight_data, st.session_state.lang, st.session_state.theme)
    except ImportError as e:
        st.info(f"🎯 صفحة Segmentation جاري تجهيزها...")
    
elif current_page == "carbon":
    try:
        from pages.carbon_impact import show_carbon
        show_carbon(carbon_data, tourist_data, overnight_data, st.session_state.lang, st.session_state.theme)
    except ImportError as e:
        st.info(f"🌱 صفحة Carbon Impact جاري تجهيزها...")

# ═══════════════════════════════════════════════════════
# PROFESSIONAL FOOTER
# ═══════════════════════════════════════════════════════
st.divider()

# Footer with proper links
st.markdown(f"""
<div style='
    background: linear-gradient(135deg, rgba(27,94,32,0.05) 0%, rgba(0,131,143,0.05) 100%);
    border: 1px solid rgba(0,131,143,0.3);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 2rem 0 0.5rem 0;
'>
    <!-- Navigation Links -->
    <div style='
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    '>
        <a href="#overview" style='color: #94A3B8; text-decoration: none; font-size: 0.85rem;'>Overview</a>
        <a href="#results" style='color: #94A3B8; text-decoration: none; font-size: 0.85rem;'>Results</a>
        <a href="#data" style='color: #94A3B8; text-decoration: none; font-size: 0.85rem;'>Data</a>
        <a href="#insights" style='color: #94A3B8; text-decoration: none; font-size: 0.85rem;'>Insights</a>
        <a href="#comparison" style='color: #94A3B8; text-decoration: none; font-size: 0.85rem;'>Comparison</a>
        <a href="#forecast" style='color: #94A3B8; text-decoration: none; font-size: 0.85rem;'>Forecast</a>
    </div>
    
    <!-- Developer Signature -->
    <div style='text-align: center;'>
        <div style='color: #D4A017; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;'>{DEV_NAME}</div>
        <div style='color: #94A3B8; font-size: 0.8rem; margin-bottom: 0.5rem;'>
            🐙 <a href="{DEV_GITHUB}" target="_blank" style='color: #00ACC1; text-decoration: none;'>GitHub</a> · 
            💼 <a href="{DEV_LINKEDIN}" target="_blank" style='color: #00ACC1; text-decoration: none;'>LinkedIn</a>
        </div>
        <div style='color: #94A3B8; font-size: 0.7rem;'>
            {T[st.session_state.lang]['data_source']} · {T[st.session_state.lang]['last_updated']}
        </div>
        <div style='color: #5A6F8C; font-size: 0.65rem; margin-top: 0.5rem;'>
            {T[st.session_state.lang]['footer_text']}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    pass
