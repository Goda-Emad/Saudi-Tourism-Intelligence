# 🇸🇦 Saudi Tourism Intelligence

<div align="center">

![Saudi Tourism Intelligence](https://img.shields.io/badge/Saudi%20Tourism-Intelligence-17B19B?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0tMiAxNWwtNS01IDEuNDEtMS40MUwxMCAxNC4xN2w3LjU5LTcuNTlMMTkgOGwtOSA5eiIvPjwvc3ZnPg==)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Prophet](https://img.shields.io/badge/Prophet%20ML-17B19B?style=for-the-badge)

**AI-powered analytics platform built on 10 years of official Saudi government tourism data**

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Open%20App-17B19B?style=for-the-badge)](https://saudi-tourism-intelligence-zyayphbqpoqx623bg5neme.streamlit.app/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Goda%20Emad-0077B5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/goda-emad/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/Goda-Emad/Saudi-Tourism-Intelligence)

</div>

---

## 📌 Overview

**Saudi Tourism Intelligence** is a comprehensive, interactive analytics dashboard that transforms 10 years (2015–2024) of official Saudi government tourism data into actionable intelligence. Built with Python and Streamlit, it combines statistical analysis, machine learning forecasting, and ESG sustainability metrics — all in one platform.

> 🏆 Achieved **98.6% R²** accuracy using Prophet ML on 2024 holdout validation data.

---

## 🌐 Live Application

| Link | Description |
|------|-------------|
| 🚀 [**Live App**](https://saudi-tourism-intelligence-zyayphbqpoqx623bg5neme.streamlit.app/) | Interactive Streamlit dashboard |
| 💼 [**LinkedIn**](https://www.linkedin.com/in/goda-emad/) | Author profile |
| 🐙 [**GitHub**](https://github.com/Goda-Emad/Saudi-Tourism-Intelligence) | Source code repository |

---

## ✨ Key Features

| Feature | Details |
|---------|---------|
| 📊 **8 Interactive Pages** | Full coverage of every tourism dimension |
| 🤖 **Prophet ML Forecasting** | 98.6% R² · 2025–2026 demand predictions |
| 🎯 **K-Means Segmentation** | Silhouette Score: 0.630 · High/Mid/Budget clusters |
| 🌱 **Carbon Impact** | CO₂ index & ESG sustainability tracking |
| 🌐 **Bilingual** | Full Arabic 🇸🇦 & English 🇬🇧 support |
| 🌙 **Dark / Light Mode** | Fully themed UI |
| 📅 **10 Years of Data** | 2015–2024 official government records |
| 📁 **7 Datasets** | CSV files from Ministry of Economy & Planning |

---

## 📈 Dashboard Pages

```
📱 Saudi Tourism Intelligence
├── 🏠  Executive Overview      → KPIs, trends & strategic insights
├── 📈  Tourist Trends          → Annual & monthly analysis 2015–2024
├── 📅  Seasonality             → Ramadan & summer peak detection
├── 💰  Spending Analysis       → Per trip, per night, by purpose
├── 🏨  Overnight Stays         → Length of stay & COVID-19 recovery
├── 🔮  Demand Forecasting      → Prophet ML · 2025–2026 predictions
├── 🎯  Segmentation            → K-Means tourist clustering
└── 🌱  Carbon Impact           → CO₂ index & ESG sustainability
```

---

## 📊 Key Statistics (2024)

| Metric | Value | YoY Change |
|--------|-------|-----------|
| 🌍 Total Tourists | **115.8M** | ▲ +23% |
| 🌙 Overnight Stays | **1.10B** | ▲ +41% |
| 💰 Avg Spend (SAR) | **5,622** | ▲ +8% |
| ✈️ Inbound Tourists | **29.7M** | ▲ +8.4% |
| 🏠 Domestic Tourists | **86.2M** | ▲ +5.2% |
| 🤖 ML Accuracy R² | **98.6%** | — |

---

## 🏗️ Project Structure

```
dashboard/
├── app.py                    # 🏠 Home page & hero section
├── assets/
│   ├── logo.jpg              # Platform logo
│   └── hero.jpg              # Hero background image
├── pages/
│   ├── Overview.py           # Executive overview
│   ├── Tourist_Trends.py     # Tourist trends analysis
│   ├── Seasonality.py        # Seasonality patterns
│   ├── Spending.py           # Spending analysis
│   ├── Overnight_Stays.py    # Overnight stays
│   ├── Forecasting.py        # ML demand forecasting
│   ├── Segmentation.py       # Tourist segmentation
│   └── Carbon_Impact.py      # Carbon & ESG
└── utils/
    ├── __init__.py
    ├── sidebar.py            # Shared navigation sidebar
    ├── kpis.py               # KPI & progress bar components
    ├── charts.py             # Reusable chart helpers
    └── data_loader.py        # Data loading utilities
```

---

## 🛠️ Tech Stack

| Technology | Usage |
|-----------|-------|
| **Python 3.10+** | Core language |
| **Streamlit** | Web application framework |
| **Plotly** | Interactive charts & heatmaps |
| **Prophet (Meta)** | Time-series ML forecasting |
| **scikit-learn** | K-Means clustering & segmentation |
| **Pandas / NumPy** | Data processing & analysis |

---

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.10+
pip
```

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Goda-Emad/Saudi-Tourism-Intelligence.git
cd Saudi-Tourism-Intelligence/dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
streamlit run app.py
```

### Dependencies (`requirements.txt`)
```
streamlit
plotly
pandas
numpy
prophet
scikit-learn
```

---

## 🎯 Vision 2030 Alignment

This platform tracks Saudi Arabia's progress toward **Vision 2030** tourism targets:

| Target | Current | Goal | Progress |
|--------|---------|------|---------|
| Inbound Tourists | 30.1M | 150M | 20% |
| Tourism GDP % | 11.5% | 10% | ✅ Exceeded |
| Hotel Capacity | 550K rooms | 650K | 85% |
| Carbon Reduction | 18% | 30% | In Progress |

---

## 🔮 ML Forecasting Highlights

- **Model:** Facebook Prophet with yearly & weekly seasonality
- **Training Data:** 2015–2023 (9 years)
- **Validation:** 2024 holdout test set
- **Accuracy:** R² = **0.986** · MAPE < 4%
- **Forecast Horizon:** 2025–2026 with confidence intervals

---

## 👩‍💻 Author

<div align="center">

**Eng. Goda Emad**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/goda-emad/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](https://github.com/Goda-Emad/Saudi-Tourism-Intelligence)

*Data Scientist & Analytics Engineer*
*Design: DataSaudi*

</div>

---

## 📄 License

This project uses official data from the **Ministry of Economy & Planning, Saudi Arabia**.
All analytics, visualizations, and ML models are original work by Eng. Goda Emad.

---

<div align="center">

**© 2025 Saudi Tourism Intelligence · Eng. Goda Emad**

[![Live App](https://img.shields.io/badge/🚀%20Try%20the%20Live%20App-17B19B?style=for-the-badge)](https://saudi-tourism-intelligence-zyayphbqpoqx623bg5neme.streamlit.app/)

*Built with ❤️ for Saudi Vision 2030*

</div>
