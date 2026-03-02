# Data Dictionary
## Saudi Tourism Intelligence Project
**Source:** DataSaudi — Ministry of Economy & Planning
**URL:** datasaudi.sa/en/sector/tourism

---

## 01_Tourists_CLEAN.csv
| Column | Type | Description |
|--------|------|-------------|
| Period | object | Year (2015-2024) or Month (2015-01) |
| Trip Purpose | object | Religious / Leisure / Business / VFR / Other |
| Type of tourist | object | Inbound / Domestic |
| Tourists | float64 | Number of tourists (thousands) |
| Frequency | object | Annual / Monthly |

---

## 02_Overnight_CLEAN.csv
| Column | Type | Description |
|--------|------|-------------|
| Period | object | Year or Month |
| Type of tourist | object | Inbound / Domestic |
| Overnight Stays | float64 | Number of overnight stays (thousands) |
| Frequency | object | Annual / Monthly |

---

## 03_KPI_CLEAN.csv
| Column | Type | Description |
|--------|------|-------------|
| Month | object | Format: YYYY-MM (2015-01 to 2024-12) |
| Type of tourist | object | Inbound / Domestic |
| Average Length of Stay | float64 | Average nights per trip |
| Average Spending per Trip | float64 | Average SAR spent per trip |
| Average Spending per Night | float64 | Average SAR spent per night |

---

## 04_Expenditure_CLEAN.csv
| Column | Type | Description |
|--------|------|-------------|
| Year | int64 | Year (2014-2022) |
| Trip Purpose | object | Religious / Leisure / Business / VFR / Other |
| Type of tourist | object | Inbound / Domestic |
| Expenditure_Billions_SAR | float64 | Total expenditure in Billions SAR |

---

## 05_Carbon_Impact.csv
| Column | Type | Description |
|--------|------|-------------|
| Period | int64 | Year (2015-2024) |
| Type of tourist | object | Inbound / Domestic |
| Overnight Stays | float64 | Overnight stays (thousands) |
| Carbon_kg | float64 | Carbon emissions in kg CO2 |
| Carbon_MegaTons | float64 | Carbon emissions in MegaTons CO2 |

---

## 06_Demand_Forecast_2025_2026.csv
| Column | Type | Description |
|--------|------|-------------|
| Month | object | Format: YYYY-MM |
| Forecast | float64 | Predicted tourists (thousands) |
| Lower | float64 | Lower confidence interval |
| Upper | float64 | Upper confidence interval |

---

## 07_Tourist_Segments.csv
| Column | Type | Description |
|--------|------|-------------|
| Period | int64 | Year |
| Type of tourist | object | Inbound / Domestic |
| Cluster | int64 | Cluster ID (0-2) |
| Segment | object | High-Value / Mid-Value / Budget |

---

## 08_Spending_Predictions.csv
| Column | Type | Description |
|--------|------|-------------|
| Year | int64 | 2025 or 2026 |
| Month_Num | int64 | Month number (1-12) |
| Type | object | Inbound / Domestic |
| Predicted_Spending | float64 | Predicted SAR spending per trip |

---

## Key Metrics (2024)
- Total Tourists: 115.8M
- Inbound: 29.7M | Domestic: 86.2M
- Overnight Stays: 1.1B nights
- Avg Spending Inbound: SAR 5,622 per trip
- Carbon Impact: 68.17 MegaTons CO2
