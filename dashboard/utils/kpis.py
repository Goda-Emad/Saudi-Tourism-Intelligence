# utils/kpis.py
"""
KPIs and Metrics Calculation Functions
دوال حساب المؤشرات الرئيسية
"""

import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st

# ═══════════════════════════════════════════════════════
# MAIN DATA LOADER
# ═══════════════════════════════════════════════════════
@st.cache_data
def load_all_data():
    """تحميل جميع البيانات من المجلد clean"""
    base_path = Path(__file__).parent.parent.parent / "data" / "clean"
    
    data = {}
    files = {
        'tourists': '01_Tourists_CLEAN.csv',
        'overnight': '02_Overnight_CLEAN.csv',
        'kpi': '03_KPI_CLEAN.csv',
        'expenditure': '04_Expenditure_CLEAN.csv',
        'carbon': '05_Carbon_Impact.csv'
    }
    
    for key, filename in files.items():
        file_path = base_path / filename
        if file_path.exists():
            data[key] = pd.read_csv(file_path)
        else:
            data[key] = pd.DataFrame()
            print(f"Warning: {filename} not found")
    
    return data

# ═══════════════════════════════════════════════════════
# KPI CALCULATIONS
# ═══════════════════════════════════════════════════════
def calculate_kpis(tourist_df=None, spending_df=None, overnight_df=None):
    """حساب جميع المؤشرات الرئيسية"""
    
    kpis = {}
    
    # بيانات افتراضية من business_case.pdf (لو مفيش ملفات)
    kpis['total_tourists_2024'] = 115.8  # مليون
    kpis['inbound_2024'] = 29.7  # مليون
    kpis['domestic_2024'] = 86.2  # مليون
    kpis['total_nights_2024'] = 1.1  # مليار
    kpis['avg_spend_2024'] = 5622  # ريال
    
    kpis['tourists_growth'] = 8.1  # %
    kpis['inbound_growth'] = 8.4  # %
    kpis['domestic_growth'] = 5.2  # %
    kpis['nights_growth'] = 18.2  # %
    kpis['spend_growth'] = 12.8  # %
    
    kpis['covid_drop_2020'] = -29.2  # %
    kpis['recovery_rate'] = 72.0  # %
    
    return kpis

def format_number(num, format_type='millions'):
    """تنسيق الأرقام للعرض"""
    if format_type == 'millions':
        return f"{num/1000:.1f}M" if num > 1000 else f"{num:.1f}M"
    elif format_type == 'billions':
        return f"{num:.1f}B"
    elif format_type == 'currency':
        return f"{num:,.0f} SAR"
    else:
        return f"{num:,}"

def get_yoy_growth(current, previous):
    """حساب النمو السنوي"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

def calculate_growth_rate(series):
    """حساب معدل النمو لسلسلة زمنية"""
    if len(series) < 2:
        return 0
    first = series.iloc[0]
    last = series.iloc[-1]
    if first == 0:
        return 0
    return ((last - first) / first) * 100

def get_peak_month(monthly_data):
    """الحصول على شهر الذروة"""
    if monthly_data.empty:
        return "N/A"
    max_idx = monthly_data.argmax()
    months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
              'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
    return months[max_idx] if max_idx < len(months) else "N/A"

def get_seasonal_factors(monthly_data):
    """حساب العوامل الموسمية"""
    if monthly_data.empty:
        return []
    avg = monthly_data.mean()
    return [round(x/avg, 2) for x in monthly_data]

# ═══════════════════════════════════════════════════════
# CARBON CALCULATIONS
# ═══════════════════════════════════════════════════════
def calculate_carbon_metrics(tourists, nights, transport_km=3500):
    """حساب مؤشرات الكربون"""
    # Emission factors (kg CO2 per unit)
    FLIGHT_EMISSION = 0.12  # kg per km per tourist
    HOTEL_EMISSION = 15.0   # kg per night
    LOCAL_TRANSPORT = 5.0   # kg per day
    
    flight_emissions = tourists * transport_km * FLIGHT_EMISSION / 1000  # to tons
    hotel_emissions = nights * HOTEL_EMISSION
    local_emissions = nights * LOCAL_TRANSPORT
    
    total = (flight_emissions + hotel_emissions + local_emissions) / 1e6  # to megatons
    
    return {
        'total_mt': total,
        'flight_mt': flight_emissions / 1e6,
        'hotel_mt': hotel_emissions / 1e6,
        'local_mt': local_emissions / 1e6
    }

def trees_equivalent(co2_tons):
    """تحويل الكربون إلى ما يعادل أشجار"""
    # Each tree absorbs ~20 kg CO2 per year
    trees = (co2_tons * 1000) / 20
    return int(trees)

# ═══════════════════════════════════════════════════════
# SEGMENTATION METRICS
# ═══════════════════════════════════════════════════════
def get_segment_metrics():
    """بيانات تجزئة السياح"""
    return {
        'high_value': {
            'pct': 18,
            'spend': 12500,
            'stay': 12.5,
            'frequency': 1.8,
            'color': '#F0A500'
        },
        'mid_value': {
            'pct': 37,
            'spend': 6200,
            'stay': 6.8,
            'frequency': 2.5,
            'color': '#3A86FF'
        },
        'budget': {
            'pct': 45,
            'spend': 2800,
            'stay': 3.2,
            'frequency': 4.2,
            'color': '#00C9B1'
        }
    }
