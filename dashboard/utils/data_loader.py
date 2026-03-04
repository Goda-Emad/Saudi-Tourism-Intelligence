# ═══════════════════════════════════════════════════════════════════
#  utils/data_loader.py — Saudi Tourism Intelligence
#  Author : Eng. Goda Emad
#  Merged : Original loaders + sample data + processing helpers
# ═══════════════════════════════════════════════════════════════════
import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st

# ═══════════════════════════════════════════════════════
# BASE LOADER
# ═══════════════════════════════════════════════════════
@st.cache_data
def load_csv_file(file_path):
    try:
        if Path(file_path).exists():
            return pd.read_csv(file_path)
        return pd.DataFrame()
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return pd.DataFrame()

# ═══════════════════════════════════════════════════════
# SAMPLE DATA CREATORS
# ═══════════════════════════════════════════════════════
def create_sample_tourist_data():
    years = list(range(2015, 2025))
    inbound  = [17.99,18.04,16.11,15.33,17.53, 4.14, 3.48,16.64,27.18,29.73]
    domestic = [46.45,45.04,43.82,43.26,47.81,42.11,63.83,77.84,81.92,86.16]
    return pd.DataFrame({
        'Year': years,
        'Inbound_M': inbound,
        'Domestic_M': domestic,
        'Total_M': [round(i+d,2) for i,d in zip(inbound,domestic)]
    })

def create_sample_spending_data():
    years = [2019,2020,2021,2022,2023,2024]
    ib  = [76.4,12.8,14.7,90.9,106.2,119.8]
    dom = [42.3,37.6,48.2,59.7, 68.4, 76.5]
    return pd.DataFrame({
        'Year': years,
        'Inbound_Spend_B': ib,
        'Domestic_Spend_B': dom,
        'Total_Spend_B': [round(i+d,1) for i,d in zip(ib,dom)]
    })

def create_sample_overnight_data():
    years = list(range(2015, 2025))
    ib  = [320,325,310,305,345, 82, 95,380,432,560]
    dom = [395,400,410,415,425,380,445,475,496,539]
    return pd.DataFrame({
        'Year': years,
        'Inbound_Nights_M': ib,
        'Domestic_Nights_M': dom,
        'Total_Nights_M': [i+d for i,d in zip(ib,dom)]
    })

def create_sample_carbon_data():
    years  = list(range(2015, 2025))
    carbon = [42.5,43.2,41.8,40.9,48.3,28.1,32.5,51.2,59.8,68.17]
    return pd.DataFrame({
        'Year': years,
        'Total_CO2_Mt':    carbon,
        'Inbound_CO2_Mt':  [round(c*0.58,2) for c in carbon],
        'Domestic_CO2_Mt': [round(c*0.42,2) for c in carbon]
    })

def create_sample_forecast_data():
    months = ['Jan','Feb','Mar','Apr','May','Jun',
              'Jul','Aug','Sep','Oct','Nov','Dec']
    f25 = [12307,11850,12100,11500,11200,11800,12200,12100,11600,11400,11800,12500]
    f26 = [13680,13100,13350,12700,12350,13000,13450,13350,12800,12550,13000,13800]
    data = []
    for i, month in enumerate(months):
        data.append({'Month':month,'Year':2025,'Forecast_Total':f25[i],
                     'Lower_Bound':int(f25[i]*.92),'Upper_Bound':int(f25[i]*1.08),
                     'Inbound_Pct':28,'Domestic_Pct':72})
        data.append({'Month':month,'Year':2026,'Forecast_Total':f26[i],
                     'Lower_Bound':int(f26[i]*.92),'Upper_Bound':int(f26[i]*1.08),
                     'Inbound_Pct':30,'Domestic_Pct':70})
    return pd.DataFrame(data)

def create_sample_segments_data():
    return pd.DataFrame([
        {'Segment':'High Value','Percentage':18,'Avg_Spend':12500,'Avg_Stay':12.5,
         'Frequency':1.8,'Inbound_Pct':65,'Domestic_Pct':35,
         'Religious_Pct':45,'Leisure_Pct':28,'Business_Pct':15,'VFR_Pct':8,'Other_Pct':4,
         'Winter_Pct':38,'Spring_Pct':22,'Summer_Pct':18,'Fall_Pct':22},
        {'Segment':'Mid Value','Percentage':37,'Avg_Spend':6200,'Avg_Stay':6.8,
         'Frequency':2.5,'Inbound_Pct':45,'Domestic_Pct':55,
         'Religious_Pct':38,'Leisure_Pct':32,'Business_Pct':12,'VFR_Pct':12,'Other_Pct':6,
         'Winter_Pct':28,'Spring_Pct':24,'Summer_Pct':26,'Fall_Pct':22},
        {'Segment':'Budget','Percentage':45,'Avg_Spend':2800,'Avg_Stay':3.2,
         'Frequency':4.2,'Inbound_Pct':22,'Domestic_Pct':78,
         'Religious_Pct':22,'Leisure_Pct':35,'Business_Pct':8,'VFR_Pct':25,'Other_Pct':10,
         'Winter_Pct':20,'Spring_Pct':22,'Summer_Pct':40,'Fall_Pct':18},
    ])

# ═══════════════════════════════════════════════════════
# MAIN LOADERS  (CSV first → sample fallback)
# ═══════════════════════════════════════════════════════
_BASE = Path(__file__).parent.parent.parent / "data" / "clean"

@st.cache_data
def load_tourist_data():
    df = load_csv_file(_BASE / "01_Tourists_CLEAN.csv")
    return df if not df.empty else create_sample_tourist_data()

@st.cache_data
def load_spending_data():
    df = load_csv_file(_BASE / "04_Expenditure_CLEAN.csv")
    return df if not df.empty else create_sample_spending_data()

@st.cache_data
def load_overnight_data():
    df = load_csv_file(_BASE / "02_Overnight_CLEAN.csv")
    return df if not df.empty else create_sample_overnight_data()

@st.cache_data
def load_carbon_data():
    df = load_csv_file(_BASE / "05_Carbon_Impact.csv")
    return df if not df.empty else create_sample_carbon_data()

@st.cache_data
def load_forecast_data():
    df = load_csv_file(_BASE / "06_Demand_Forecast_2025_2026.csv")
    return df if not df.empty else create_sample_forecast_data()

@st.cache_data
def load_segments_data():
    df = load_csv_file(_BASE / "07_Tourist_Segments.csv")
    return df if not df.empty else create_sample_segments_data()

@st.cache_data
def load_all_datasets():
    return {
        'tourist':  load_tourist_data(),
        'spending': load_spending_data(),
        'overnight':load_overnight_data(),
        'carbon':   load_carbon_data(),
        'forecast': load_forecast_data(),
        'segments': load_segments_data(),
    }

# ═══════════════════════════════════════════════════════
# VALIDATION & PROCESSING
# ═══════════════════════════════════════════════════════
def validate_data(df, required_columns):
    if df.empty:
        return False, "DataFrame is empty"
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        return False, f"Missing columns: {missing}"
    return True, "Data is valid"

def get_data_summary(df):
    if df.empty:
        return "No data available"
    return {'rows': len(df), 'columns': list(df.columns),
            'missing_values': df.isnull().sum().sum(),
            'data_types': df.dtypes.to_dict()}

def filter_by_year(df, year_col, start_year, end_year):
    return df[(df[year_col] >= start_year) & (df[year_col] <= end_year)]

def aggregate_monthly(df, date_col, value_col):
    df[date_col] = pd.to_datetime(df[date_col])
    return df.groupby(df[date_col].dt.to_period('M'))[value_col].sum().reset_index()
