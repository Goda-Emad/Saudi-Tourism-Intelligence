# utils/data_loader.py
"""
Data Loading Functions
دوال تحميل البيانات
"""

import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st

# ═══════════════════════════════════════════════════════
# BASE LOADER
# ═══════════════════════════════════════════════════════
@st.cache_data
def load_csv_file(file_path):
    """تحميل ملف CSV مع معالجة الأخطاء"""
    try:
        if Path(file_path).exists():
            return pd.read_csv(file_path)
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return pd.DataFrame()

# ═══════════════════════════════════════════════════════
# MAIN DATA LOADERS
# ═══════════════════════════════════════════════════════
@st.cache_data
def load_tourist_data():
    """تحميل بيانات السياح"""
    base_path = Path(__file__).parent.parent.parent / "data" / "clean"
    file_path = base_path / "01_Tourists_CLEAN.csv"
    
    df = load_csv_file(file_path)
    
    # إذا الملف مش موجود، نرجع بيانات افتراضية
    if df.empty:
        df = create_sample_tourist_data()
    
    return df

@st.cache_data
def load_spending_data():
    """تحميل بيانات الإنفاق"""
    base_path = Path(__file__).parent.parent.parent / "data" / "clean"
    file_path = base_path / "04_Expenditure_CLEAN.csv"
    
    df = load_csv_file(file_path)
    
    if df.empty:
        df = create_sample_spending_data()
    
    return df

@st.cache_data
def load_overnight_data():
    """تحميل بيانات الإقامة"""
    base_path = Path(__file__).parent.parent.parent / "data" / "clean"
    file_path = base_path / "02_Overnight_CLEAN.csv"
    
    df = load_csv_file(file_path)
    
    if df.empty:
        df = create_sample_overnight_data()
    
    return df

@st.cache_data
def load_carbon_data():
    """تحميل بيانات الكربون"""
    base_path = Path(__file__).parent.parent.parent / "data" / "clean"
    file_path = base_path / "05_Carbon_Impact.csv"
    
    df = load_csv_file(file_path)
    
    if df.empty:
        df = create_sample_carbon_data()
    
    return df

@st.cache_data
def load_forecast_data():
    """تحميل بيانات التوقعات 2025-2026"""
    base_path = Path(__file__).parent.parent.parent / "data" / "clean"
    file_path = base_path / "06_Demand_Forecast_2025_2026.csv"
    
    df = load_csv_file(file_path)
    
    if df.empty:
        df = create_sample_forecast_data()
    
    return df

@st.cache_data
def load_segments_data():
    """تحميل بيانات تجزئة السياح"""
    base_path = Path(__file__).parent.parent.parent / "data" / "clean"
    file_path = base_path / "07_Tourist_Segments.csv"
    
    df = load_csv_file(file_path)
    
    if df.empty:
        df = create_sample_segments_data()
    
    return df

# ═══════════════════════════════════════════════════════
# SAMPLE DATA CREATORS (للتجربة)
# ═══════════════════════════════════════════════════════
def create_sample_tourist_data():
    """إنشاء بيانات سياحية تجريبية"""
    years = list(range(2015, 2025))
    inbound = [17.99, 18.04, 16.11, 15.33, 17.53, 4.14, 3.48, 16.64, 27.18, 29.73]
    domestic = [46.45, 45.04, 43.82, 43.26, 47.81, 42.11, 63.83, 77.84, 81.92, 86.16]
    
    df = pd.DataFrame({
        'Year': years,
        'Inbound_M': inbound,
        'Domestic_M': domestic,
        'Total_M': [i + d for i, d in zip(inbound, domestic)]
    })
    
    return df

def create_sample_spending_data():
    """إنشاء بيانات إنفاق تجريبية"""
    years = [2019, 2020, 2021, 2022, 2023, 2024]
    inbound_spend = [76.4, 12.8, 14.7, 90.9, 106.2, 119.8]
    domestic_spend = [42.3, 37.6, 48.2, 59.7, 68.4, 76.5]
    
    df = pd.DataFrame({
        'Year': years,
        'Inbound_Spend_B': inbound_spend,
        'Domestic_Spend_B': domestic_spend,
        'Total_Spend_B': [i + d for i, d in zip(inbound_spend, domestic_spend)]
    })
    
    return df

def create_sample_overnight_data():
    """إنشاء بيانات إقامة تجريبية"""
    years = list(range(2015, 2025))
    inbound_nights = [320, 325, 310, 305, 345, 82, 95, 380, 432, 560]
    domestic_nights = [395, 400, 410, 415, 425, 380, 445, 475, 496, 539]
    
    df = pd.DataFrame({
        'Year': years,
        'Inbound_Nights_M': inbound_nights,
        'Domestic_Nights_M': domestic_nights,
        'Total_Nights_M': [i + d for i, d in zip(inbound_nights, domestic_nights)]
    })
    
    return df

def create_sample_carbon_data():
    """إنشاء بيانات كربون تجريبية"""
    years = list(range(2015, 2025))
    carbon = [42.5, 43.2, 41.8, 40.9, 48.3, 28.1, 32.5, 51.2, 59.8, 68.17]
    
    df = pd.DataFrame({
        'Year': years,
        'Total_CO2_Mt': carbon,
        'Inbound_CO2_Mt': [c * 0.58 for c in carbon],
        'Domestic_CO2_Mt': [c * 0.42 for c in carbon]
    })
    
    return df

def create_sample_forecast_data():
    """إنشاء بيانات توقعات تجريبية (من business_case.pdf)"""
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # 2025 forecast (thousands)
    forecast_2025 = [12307, 11850, 12100, 11500, 11200, 11800,
                     12200, 12100, 11600, 11400, 11800, 12500]
    
    # 2026 forecast (thousands)
    forecast_2026 = [13680, 13100, 13350, 12700, 12350, 13000,
                     13450, 13350, 12800, 12550, 13000, 13800]
    
    # Confidence intervals
    lower_2025 = [int(f * 0.92) for f in forecast_2025]
    upper_2025 = [int(f * 1.08) for f in forecast_2025]
    lower_2026 = [int(f * 0.92) for f in forecast_2026]
    upper_2026 = [int(f * 1.08) for f in forecast_2026]
    
    # Create dataframe
    data = []
    for i, month in enumerate(months):
        # 2025
        data.append({
            'Month': month,
            'Year': 2025,
            'Forecast_Total': forecast_2025[i],
            'Lower_Bound': lower_2025[i],
            'Upper_Bound': upper_2025[i],
            'Inbound_Pct': 28,
            'Domestic_Pct': 72
        })
        # 2026
        data.append({
            'Month': month,
            'Year': 2026,
            'Forecast_Total': forecast_2026[i],
            'Lower_Bound': lower_2026[i],
            'Upper_Bound': upper_2026[i],
            'Inbound_Pct': 30,
            'Domestic_Pct': 70
        })
    
    return pd.DataFrame(data)

def create_sample_segments_data():
    """إنشاء بيانات تجزئة السياح تجريبية"""
    
    segments = [
        {
            'Segment': 'High Value',
            'Percentage': 18,
            'Avg_Spend': 12500,
            'Avg_Stay': 12.5,
            'Frequency': 1.8,
            'Inbound_Pct': 65,
            'Domestic_Pct': 35,
            'Religious_Pct': 45,
            'Leisure_Pct': 28,
            'Business_Pct': 15,
            'VFR_Pct': 8,
            'Other_Pct': 4,
            'Winter_Pct': 38,
            'Spring_Pct': 22,
            'Summer_Pct': 18,
            'Fall_Pct': 22
        },
        {
            'Segment': 'Mid Value',
            'Percentage': 37,
            'Avg_Spend': 6200,
            'Avg_Stay': 6.8,
            'Frequency': 2.5,
            'Inbound_Pct': 45,
            'Domestic_Pct': 55,
            'Religious_Pct': 38,
            'Leisure_Pct': 32,
            'Business_Pct': 12,
            'VFR_Pct': 12,
            'Other_Pct': 6,
            'Winter_Pct': 28,
            'Spring_Pct': 24,
            'Summer_Pct': 26,
            'Fall_Pct': 22
        },
        {
            'Segment': 'Budget',
            'Percentage': 45,
            'Avg_Spend': 2800,
            'Avg_Stay': 3.2,
            'Frequency': 4.2,
            'Inbound_Pct': 22,
            'Domestic_Pct': 78,
            'Religious_Pct': 22,
            'Leisure_Pct': 35,
            'Business_Pct': 8,
            'VFR_Pct': 25,
            'Other_Pct': 10,
            'Winter_Pct': 20,
            'Spring_Pct': 22,
            'Summer_Pct': 40,
            'Fall_Pct': 18
        }
    ]
    
    return pd.DataFrame(segments)

# ═══════════════════════════════════════════════════════
# BULK LOADER
# ═══════════════════════════════════════════════════════
@st.cache_data
def load_all_datasets():
    """تحميل جميع مجموعات البيانات"""
    return {
        'tourist': load_tourist_data(),
        'spending': load_spending_data(),
        'overnight': load_overnight_data(),
        'carbon': load_carbon_data(),
        'forecast': load_forecast_data(),
        'segments': load_segments_data()
    }

# ═══════════════════════════════════════════════════════
# DATA VALIDATION
# ═══════════════════════════════════════════════════════
def validate_data(df, required_columns):
    """التحقق من صحة البيانات"""
    if df.empty:
        return False, "DataFrame is empty"
    
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        return False, f"Missing columns: {missing}"
    
    return True, "Data is valid"

def get_data_summary(df):
    """الحصول على ملخص البيانات"""
    if df.empty:
        return "No data available"
    
    summary = {
        'rows': len(df),
        'columns': list(df.columns),
        'missing_values': df.isnull().sum().sum(),
        'data_types': df.dtypes.to_dict()
    }
    
    return summary

# ═══════════════════════════════════════════════════════
# DATA PROCESSING
# ═══════════════════════════════════════════════════════
def filter_by_year(df, year_col, start_year, end_year):
    """تصفية البيانات حسب السنة"""
    return df[(df[year_col] >= start_year) & (df[year_col] <= end_year)]

def aggregate_monthly(df, date_col, value_col):
    """تجميع البيانات الشهرية"""
    df[date_col] = pd.to_datetime(df[date_col])
    return df.groupby(df[date_col].dt.to_period('M'))[value_col].sum().reset_index()
