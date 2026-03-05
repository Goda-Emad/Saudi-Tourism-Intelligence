# ═══════════════════════════════════════════════════════════════════
#  utils/kpis.py — Saudi Tourism Intelligence
#  Author : Eng. Goda Emad
#  Merged : Original KPI calculations + DataSaudi HTML components
# ═══════════════════════════════════════════════════════════════════
import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st

# ═══════════════════════════════════════════════════════
# DATA LOADER
# ═══════════════════════════════════════════════════════
@st.cache_data
def load_all_data():
    """تحميل جميع البيانات من مجلد clean"""
    base_path = Path(__file__).parent.parent.parent / "data" / "clean"
    files = {
        'tourists':    '01_Tourists_CLEAN.csv',
        'overnight':   '02_Overnight_CLEAN.csv',
        'kpi':         '03_KPI_CLEAN.csv',
        'expenditure': '04_Expenditure_CLEAN.csv',
        'carbon':      '05_Carbon_Impact.csv',
    }
    data = {}
    for key, filename in files.items():
        fp = base_path / filename
        data[key] = pd.read_csv(fp) if fp.exists() else pd.DataFrame()
    return data

# ═══════════════════════════════════════════════════════
# KPI CALCULATIONS
# ═══════════════════════════════════════════════════════
def calculate_kpis(tourist_df=None, spending_df=None, overnight_df=None):
    """حساب جميع المؤشرات الرئيسية — قيم افتراضية من business_case.pdf"""
    return {
        'total_tourists_2024': 115.8,
        'inbound_2024':         29.7,
        'domestic_2024':        86.2,
        'total_nights_2024':     1.1,
        'avg_spend_2024':      5622,
        'tourists_growth':       8.1,
        'inbound_growth':        8.4,
        'domestic_growth':       5.2,
        'nights_growth':        18.2,
        'spend_growth':         12.8,
        'covid_drop_2020':     -29.2,
        'recovery_rate':        72.0,
    }

def format_number(num, format_type='millions'):
    """تنسيق الأرقام للعرض"""
    if format_type == 'millions':
        return f"{num:.1f}M"
    elif format_type == 'billions':
        return f"{num:.1f}B"
    elif format_type == 'currency':
        return f"{num:,.0f} SAR"
    return f"{num:,}"

def get_yoy_growth(current, previous):
    """حساب النمو السنوي %"""
    if previous == 0:
        return 0
    return round(((current - previous) / previous) * 100, 1)

def calculate_growth_rate(series):
    """حساب معدل النمو الكلي لسلسلة زمنية"""
    if len(series) < 2:
        return 0
    first, last = series.iloc[0], series.iloc[-1]
    return 0 if first == 0 else round(((last - first) / first) * 100, 1)

def get_peak_month(monthly_data):
    """الحصول على شهر الذروة"""
    if isinstance(monthly_data, (list, pd.Series)) and len(monthly_data) > 0:
        months_en = ['Jan','Feb','Mar','Apr','May','Jun',
                     'Jul','Aug','Sep','Oct','Nov','Dec']
        idx = int(np.argmax(monthly_data))
        return months_en[idx] if idx < 12 else "N/A"
    return "N/A"

def get_seasonal_factors(monthly_data):
    """حساب العوامل الموسمية"""
    if not isinstance(monthly_data, (list, pd.Series)) or len(monthly_data) == 0:
        return []
    avg = np.mean(monthly_data)
    return [round(x / avg, 2) for x in monthly_data] if avg else []

# ═══════════════════════════════════════════════════════
# CARBON CALCULATIONS
# ═══════════════════════════════════════════════════════
def calculate_carbon_metrics(tourists, nights, transport_km=3500):
    """حساب مؤشرات الكربون (tonnes)"""
    FLIGHT_EMISSION = 0.12   # kg CO2 per km per tourist
    HOTEL_EMISSION  = 15.0   # kg CO2 per night
    LOCAL_TRANSPORT =  5.0   # kg CO2 per night

    flight = tourists * transport_km * FLIGHT_EMISSION / 1000   # → tonnes
    hotel  = nights  * HOTEL_EMISSION / 1000
    local  = nights  * LOCAL_TRANSPORT / 1000
    total  = flight + hotel + local

    return {
        'total_mt':  round(total  / 1e3, 3),   # megatonnes
        'flight_mt': round(flight / 1e3, 3),
        'hotel_mt':  round(hotel  / 1e3, 3),
        'local_mt':  round(local  / 1e3, 3),
    }

def trees_equivalent(co2_tons):
    """تحويل CO2 بالطن إلى عدد أشجار (كل شجرة تمتص ~21.77 kg/yr)"""
    return int(co2_tons * 1000 / 21.77)

# ═══════════════════════════════════════════════════════
# SEGMENTATION METRICS
# ═══════════════════════════════════════════════════════
def get_segment_metrics():
    """بيانات تجزئة السياح — 3 شرائح"""
    return {
        'high_value': {
            'pct': 18, 'spend': 12500, 'stay': 12.5,
            'frequency': 1.8, 'color': '#F4D044'
        },
        'mid_value': {
            'pct': 37, 'spend': 6200, 'stay': 6.8,
            'frequency': 2.5, 'color': '#17B19B'
        },
        'budget': {
            'pct': 45, 'spend': 2800, 'stay': 3.2,
            'frequency': 4.2, 'color': '#365C8D'
        },
    }

# ═══════════════════════════════════════════════════════
# HTML COMPONENTS  (DataSaudi design system)
# ═══════════════════════════════════════════════════════
def kpi_card_html(label: str, value: str, unit: str,
                  delta: str, color: str,
                  card_bg: str, border: str, grey: str) -> str:
    """HTML string لـ KPI card واحدة"""
    arrow = (f'<span style="font-size:.72rem;color:{color};'
             f'font-weight:700;margin-left:5px;">{delta}</span>'
             if delta else "")
    return (
        f'<div class="ds-card" style="background:{card_bg};border:1px solid {border};'
        f'border-radius:10px;padding:22px 20px;">'
        f'<div style="font-size:.62rem;color:{grey};text-transform:uppercase;'
        f'letter-spacing:1px;font-weight:500;margin-bottom:8px;">{label}</div>'
        f'<div style="display:flex;align-items:baseline;">'
        f'<div style="font-size:1.9rem;font-weight:700;color:{color};'
        f'font-family:IBM Plex Mono,monospace;letter-spacing:-1px;">{value}</div>'
        f'{arrow}</div>'
        f'<div style="font-size:.68rem;color:{grey};margin-top:4px;">{unit}</div>'
        f'</div>')


def render_kpi_strip(kpis: list, card_bg: str, border: str,
                     grey: str, padding: str = "28px 40px 0") -> None:
    """
    4-column KPI strip.
    kpis = [(label, value, unit, delta, color), ...]
    """
    html = (f'<div style="padding:{padding};">'
            f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;">')
    for label, value, unit, delta, color in kpis:
        html += kpi_card_html(label, value, unit, delta, color, card_bg, border, grey)
    html += '</div></div>'
    st.markdown(html, unsafe_allow_html=True)


def progress_bar_html(label: str, current: float, target: float,
                      note: str, color: str,
                      card_bg: str, border: str,
                      white: str, grey: str) -> str:
    """HTML لـ Vision 2030 progress bar"""
    pct  = min(round(current / target * 100), 100)
    done = pct >= 100
    tick = f' <span style="color:{color};font-size:.8rem;">✅</span>' if done else ""
    hi   = f"border-color:{color}88;" if done else ""
    glow = f"filter:drop-shadow(0 0 5px {color});" if not done else ""
    return (
        f'<div style="background:{card_bg};border:1px solid {border};{hi}'
        f'border-radius:10px;padding:18px 20px;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">'
        f'<div style="font-size:.84rem;font-weight:600;color:{white};">{label}{tick}</div>'
        f'<div style="font-size:.82rem;font-weight:700;color:{color};'
        f'font-family:IBM Plex Mono,monospace;">{pct}%</div>'
        f'</div>'
        f'<div style="background:#2A3235;border-radius:8px;height:10px;overflow:hidden;">'
        f'<div style="width:{pct}%;height:100%;border-radius:8px;background:{color};{glow}"></div>'
        f'</div>'
        f'<div style="font-size:.68rem;color:{grey};margin-top:7px;">{note}</div>'
        f'</div>')
