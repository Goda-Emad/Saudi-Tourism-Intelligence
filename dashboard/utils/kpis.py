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
        'carbon': load_carbon_data()
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
