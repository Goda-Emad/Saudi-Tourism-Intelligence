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
        st.warning("⚠️ ملف CSS غير موجود، يتم استخدام التنسيق الافتراضي")

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
    # Logo with custom styling
    try:
        st.image("assets/logo.png", use_column_width=True)
    except:
        st.markdown("""
        <div style='text-align:center; padding: 1rem;'>
            <span style='font-size: 3rem;'>🇸🇦</span>
            <div style='color: var(--desert-gold-light); font-weight: 700;'>Saudi Tourism</div>
            <div style='color: var(--white); font-weight: 600;'>INTELLIGENCE</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='text-align:center; font-size:0.8rem; color: var(--text-secondary); margin-bottom: 1rem;'>
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
    <div style='font-size:0.7rem; font-weight:600; color: var(--text-secondary); text-transform:uppercase; margin-bottom:0.5rem;'>
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
    <div style='font-size:0.7rem; color: var(--text-secondary);'>
        <div style='margin-bottom:0.5rem;'>
            <span style='color: var(--saudi-green-light);'>📊</span> {T[st.session_state.lang]['data_source']}
        </div>
        <div>
            <span style='color: var(--saudi-green-light);'>🔄</span> {T[st.session_state.lang]['last_updated']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Developer Profile
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, rgba(27,94,32,0.2) 0%, rgba(0,131,143,0.2) 100%);
        border: 1px solid var(--border-accent);
        border-radius: 16px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        text-align: center;
    '>
        <div style='
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-bottom: 0.3rem;
        '>
            {T[st.session_state.lang]['built_by']}
        </div>
        <div style='
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--desert-gold-light);
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
                background: var(--bg-card);
                color: var(--text-primary);
                padding: 0.4rem 1rem;
                border-radius: 20px;
                font-size: 0.75rem;
                border: 1px solid var(--border-accent);
                transition: all 0.3s ease;
                display: inline-flex;
                align-items: center;
                gap: 4px;
            '>
                🐙 {T[st.session_state.lang]['github']}
            </a>
            <a href="{DEV_LINKEDIN}" target="_blank" style='
                text-decoration: none;
                background: var(--bg-card);
                color: var(--text-primary);
                padding: 0.4rem 1rem;
                border-radius: 20px;
                font-size: 0.75rem;
                border: 1px solid var(--border-accent);
                transition: all 0.3s ease;
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

# Hero Banner with Hero Image
hero_base64 = get_image_base64("assets/hero.png")

if hero_base64:
    # مع وجود الصورة
    col_hero1, col_hero2 = st.columns([2, 1])
    
    with col_hero1:
        st.markdown(f"""
        <div>
            <h1 style='margin:0; font-size:2.2rem; background: linear-gradient(135deg, var(--white), var(--desert-gold-light)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{T[st.session_state.lang]['app_title']}</h1>
            <p style='font-size:1rem; color: var(--text-secondary); max-width:600px; margin-top:0.5rem;'>
                {T[st.session_state.lang]['welcome']}
            </p>
            <div style='
                background: rgba(255,255,255,0.05);
                border-radius: 30px;
                padding: 0.5rem 1.2rem;
                border: 1px solid var(--border-accent);
                display: inline-block;
                margin-top: 0.5rem;
            '>
                <span style='color: var(--text-secondary); font-size:0.8rem;'>{T[st.session_state.lang]['built_by']}: </span>
                <span style='color: var(--desert-gold-light); font-weight:700;'>{DEV_NAME}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_hero2:
        st.markdown(f"""
        <div style='text-align: center;'>
            <img src='data:image/png;base64,{hero_base64}' style='width: 100%; max-height: 150px; object-fit: contain;'>
        </div>
        """, unsafe_allow_html=True)
else:
    # من غير الصورة
    st.markdown(f"""
    <div class='hero-banner' style='
        background: linear-gradient(135deg,
            rgba(27,94,32,0.3) 0%,
            rgba(0,131,143,0.2) 50%,
            rgba(184,134,11,0.2) 100%);
        border: 1px solid var(--border-accent);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    '>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;'>
            <div>
                <h1 style='margin:0; font-size:2.2rem; background: linear-gradient(135deg, var(--white), var(--desert-gold-light)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{T[st.session_state.lang]['app_title']}</h1>
                <p style='font-size:1rem; color: var(--text-secondary); max-width:600px; margin-top:0.5rem;'>
                    {T[st.session_state.lang]['welcome']}
                </p>
            </div>
            <div style='
                background: rgba(255,255,255,0.05);
                border-radius: 30px;
                padding: 0.5rem 1.2rem;
                border: 1px solid var(--border-accent);
            '>
                <span style='color: var(--text-secondary); font-size:0.8rem;'>{T[st.session_state.lang]['built_by']}: </span>
                <span style='color: var(--desert-gold-light); font-weight:700;'>{DEV_NAME}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Key Metrics Row (if data loaded)
if st.session_state.data_loaded:
    kpis = calculate_kpis(tourist_data, spending_data, overnight_data)
    
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
# PAGE ROUTING - FIXED IMPORTS (No numbers in filenames)
# ═══════════════════════════════════════════════════════

current_page = st.session_state.current_page

if current_page == "overview":
    # الصفحة الرئيسية - نظرة عامة
    if st.session_state.data_loaded:
        try:
            from pages.overview import show_overview
            show_overview(tourist_data, spending_data, overnight_data, carbon_data, st.session_state.lang, st.session_state.theme)
        except ImportError as e:
            st.info(f"📊 صفحة Overview جاري تجهيزها... {e}")
    else:
        st.info("📊 يرجى التأكد من وجود ملفات البيانات في المجلد data/clean/")
        
elif current_page == "trends":
    try:
        from pages.tourist_trends import show_trends
        show_trends(tourist_data, st.session_state.lang, st.session_state.theme)
    except ImportError as e:
        st.info(f"📈 صفحة Tourist Trends جاري تجهيزها... {e}")
    
elif current_page == "seasonality":
    try:
        from pages.seasonality import show_seasonality
        show_seasonality(tourist_data, st.session_state.lang, st.session_state.theme)
    except ImportError as e:
        st.info(f"📅 صفحة Seasonality جاري تجهيزها... {e}")
    
elif current_page == "spending":
    try:
        from pages.spending import show_spending
        show_spending(spending_data, tourist_data, st.session_state.lang, st.session_state.theme)
    except ImportError as e:
        st.info(f"💰 صفحة Spending جاري تجهيزها... {e}")
    
elif current_page == "overnight":
    try:
        from pages.overnight_stays import show_overnight
        show_overnight(overnight_data, tourist_data, st.session_state.lang, st.session_state.theme)
    except ImportError as e:
        st.info(f"🏨 صفحة Overnight Stays جاري تجهيزها... {e}")
    
elif current_page == "forecast":
    try:
        from pages.forecasting import show_forecast
        show_forecast(tourist_data, st.session_state.lang, st.session_state.theme)
    except ImportError as e:
        st.info(f"🔮 صفحة Forecasting جاري تجهيزها... {e}")
    
elif current_page == "segmentation":
    try:
        from pages.segmentation import show_segmentation
        show_segmentation(tourist_data, spending_data, overnight_data, st.session_state.lang, st.session_state.theme)
    except ImportError as e:
        st.info(f"🎯 صفحة Segmentation جاري تجهيزها... {e}")
    
elif current_page == "carbon":
    try:
        from pages.carbon_impact import show_carbon
        show_carbon(carbon_data, tourist_data, overnight_data, st.session_state.lang, st.session_state.theme)
    except ImportError as e:
        st.info(f"🌱 صفحة Carbon Impact جاري تجهيزها... {e}")

# ═══════════════════════════════════════════════════════
# PROFESSIONAL FOOTER WITH DEVELOPER SIGNATURE
# ═══════════════════════════════════════════════════════
st.divider()

# Signature Section
st.markdown(f"""
<div style='
    background: linear-gradient(135deg, rgba(27,94,32,0.05) 0%, rgba(0,131,143,0.05) 100%);
    border: 1px solid var(--border-accent);
    border-radius: 20px;
    padding: 2rem 1.5rem;
    margin: 2rem 0 1rem 0;
    position: relative;
    overflow: hidden;
'>
    <!-- Decorative Elements -->
    <div style='
        position: absolute;
        top: -30px; right: -30px;
        width: 150px; height: 150px;
        background: var(--saudi-green-light);
        opacity: 0.05;
        border-radius: 50%;
    '></div>
    <div style='
        position: absolute;
        bottom: -30px; left: -30px;
        width: 120px; height: 120px;
        background: var(--red-sea-teal);
        opacity: 0.05;
        border-radius: 50%;
    '></div>
    
    <!-- Main Signature Content -->
    <div style='
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        position: relative;
        z-index: 2;
    '>
        <!-- Developer Badge -->
        <div style='
            background: linear-gradient(135deg, var(--saudi-green), var(--red-sea-teal));
            padding: 0.3rem 1.2rem;
            border-radius: 30px;
            margin-bottom: 1rem;
            display: inline-block;
        '>
            <span style='
                color: white;
                font-size: 0.8rem;
                font-weight: 600;
                letter-spacing: 1px;
            '>🚀 LEAD DEVELOPER</span>
        </div>
        
        <!-- Developer Name -->
        <div style='
            font-family: "Playfair Display", serif;
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--desert-gold-light), var(--saudi-green-light));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        '>
            {DEV_NAME}
        </div>
        
        <!-- Title -->
        <div style='
            color: var(--text-secondary);
            font-size: 1rem;
            margin-bottom: 1.5rem;
        '>
            AI & Data Science Engineer · Tourism Intelligence Specialist
        </div>
        
        <!-- Social Links -->
        <div style='
            display: flex;
            gap: 1.5rem;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 2rem;
        '>
            <a href="{DEV_GITHUB}" target="_blank" style='
                text-decoration: none;
                background: var(--bg-card);
                color: var(--text-primary);
                padding: 0.6rem 1.5rem;
                border-radius: 30px;
                font-size: 0.9rem;
                border: 1px solid var(--border-accent);
                transition: all 0.3s ease;
                display: inline-flex;
                align-items: center;
                gap: 8px;
            ' onmouseover="this.style.background='var(--saudi-green)'; this.style.transform='translateY(-2px)';" 
               onmouseout="this.style.background='var(--bg-card)'; this.style.transform='translateY(0)';">
                <span style='font-size:1.2rem;'>🐙</span> GitHub Repository
            </a>
            <a href="{DEV_LINKEDIN}" target="_blank" style='
                text-decoration: none;
                background: var(--bg-card);
                color: var(--text-primary);
                padding: 0.6rem 1.5rem;
                border-radius: 30px;
                font-size: 0.9rem;
                border: 1px solid var(--border-accent);
                transition: all 0.3s ease;
                display: inline-flex;
                align-items: center;
                gap: 8px;
            ' onmouseover="this.style.background='var(--red-sea-teal)'; this.style.transform='translateY(-2px)';"
               onmouseout="this.style.background='var(--bg-card)'; this.style.transform='translateY(0)';">
                <span style='font-size:1.2rem;'>💼</span> LinkedIn Profile
            </a>
        </div>
        
        <!-- Stats -->
        <div style='
            display: flex;
            gap: 2rem;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 0.5rem;
        '>
            <div style='text-align: center;'>
                <div style='font-size: 1.3rem; font-weight: 700; color: var(--desert-gold-light);'>8</div>
                <div style='font-size: 0.7rem; color: var(--text-secondary);'>Dashboard Pages</div>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 1.3rem; font-weight: 700; color: var(--saudi-green-light);'>3</div>
                <div style='font-size: 0.7rem; color: var(--text-secondary);'>ML Models</div>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 1.3rem; font-weight: 700; color: var(--red-sea-light);'>10+</div>
                <div style='font-size: 0.7rem; color: var(--text-secondary);'>Years of Data</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer with mini logo
logo_base64 = get_image_base64("assets/logo.png")
if logo_base64:
    st.markdown(f"""
    <div style='display: flex; justify-content: center; align-items: center; gap: 10px; margin: 1rem 0;'>
        <img src='data:image/png;base64,{logo_base64}' style='height: 30px; opacity: 0.7;'>
        <span style='color: var(--text-secondary); font-size: 0.7rem;'>{T[st.session_state.lang]['footer_text']}</span>
    </div>
    """, unsafe_allow_html=True)
else:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.7rem;
            padding: 1rem 0;
        '>
            {T[st.session_state.lang]['footer_text']}<br>
            <span style='font-size:0.6rem;'>DataSaudi · Ministry of Tourism · 2015-2024</span><br>
            <span style='font-size:0.6rem; color: var(--desert-gold-light);'>Developed with 🇸🇦 by {DEV_NAME}</span>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    # تم التشغيل بالفعل
    pass
