# utils/__init__.py
"""
Saudi Tourism Intelligence - Utilities Package
"""

# استيراد الدوال من kpis
from .kpis import (
    calculate_kpis,
    format_number,
    get_yoy_growth,
    calculate_growth_rate,
    get_peak_month,
    get_seasonal_factors,
    calculate_carbon_metrics,
    trees_equivalent,
    get_segment_metrics
)

# استيراد الدوال من charts
from .charts import (
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
    create_segment_chart,
    create_sustainability_scenarios,
    create_gauge_chart
)

# استيراد الدوال من data_loader
from .data_loader import (
    load_tourist_data,
    load_spending_data,
    load_overnight_data,
    load_carbon_data,
    load_forecast_data,
    load_segments_data,
    load_all_datasets,
    get_data_summary,
    validate_data
)

# تعريف __all__ ليسهل الاستيراد
__all__ = [
    # From kpis
    'calculate_kpis',
    'format_number',
    'get_yoy_growth',
    'calculate_growth_rate',
    'get_peak_month',
    'get_seasonal_factors',
    'calculate_carbon_metrics',
    'trees_equivalent',
    'get_segment_metrics',
    
    # From charts
    'create_trend_chart',
    'create_comparison_chart',
    'create_heatmap',
    'create_pie_chart',
    'create_radar_chart',
    'create_bar_chart',
    'create_line_chart',
    'create_area_chart',
    'create_forecast_chart',
    'create_carbon_chart',
    'create_segment_chart',
    'create_sustainability_scenarios',
    'create_gauge_chart',
    
    # From data_loader
    'load_tourist_data',
    'load_spending_data',
    'load_overnight_data',
    'load_carbon_data',
    'load_forecast_data',
    'load_segments_data',
    'load_all_datasets',
    'get_data_summary',
    'validate_data'
]
