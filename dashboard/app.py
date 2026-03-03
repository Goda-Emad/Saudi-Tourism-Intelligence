import streamlit as st
import plotly.graph_objects as go
import math

st.set_page_config(
    page_title="Carbon Impact · Saudi Tourism Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "lang" not in st.session_state:
    st.session_state.lang = "EN"
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

lang  = st.session_state.lang
theme = st.session_state.theme

# ══════════════════════════════════════════
# TRANSLATIONS
# ══════════════════════════════════════════
T = {
    "EN": {
        "page_title":    "🌱 Carbon Impact Index",
        "subtitle":      "CO₂ Emissions · Sustainability Metrics · Green Tourism Strategy · ESG Reporting",
        "built_by":      "Built by",
        "dark_mode":     "🌙 Dark", "light_mode": "☀️ Light", "lang_toggle": "🌐 العربية",
        "pages":         "Navigation",
        "page_overview": "🏠 Overview",   "page_trends":   "📈 Tourist Trends",
        "page_season":   "📅 Seasonality","page_spend":    "💰 Spending",
        "page_overnight":"🏨 Overnight Stays","page_forecast":"🔮 Forecasting",
        "page_segment":  "🎯 Segmentation","page_carbon":   "🌱 Carbon Impact",
        # KPIs
        "kpi_total":    "Total CO₂ 2024",
        "kpi_inbound":  "Inbound CO₂/Tourist",
        "kpi_domestic": "Domestic CO₂/Tourist",
        "kpi_growth":   "CO₂ Growth 2024",
        "kpi_trees":    "Trees to Offset 10%",
        # Sections
        "trend_title":  "Annual CO₂ Emissions Trend 2015–2024",
        "breakdown":    "CO₂ Breakdown by Tourist Type",
        "intensity":    "Carbon Intensity per Tourist",
        "reduction":    "10% Reduction Scenario — Impact Simulator",
        "benchmark":    "Global Benchmark Comparison",
        "esg_title":    "ESG Sustainability Scorecard",
        "donut_title":  "2024 Emissions Split",
        "insight_title":"Key Insights",
        # Labels
        "inbound":      "Inbound","domestic":    "Domestic","total":       "Total",
        "co2_mt":       "CO₂ (MegaTons)","co2_kg":    "CO₂ (kg/tourist)",
        "year":         "Year","reduction_lbl":"Reduction %",
        "filter_type":  "Tourist Type","all_types":  "All",
        "scenario_slider":"Reduction Scenario (%)",
        # Insights
        "i1": "2024 total CO₂: 68.17 MT — +23.2% YoY driven by inbound tourism recovery",
        "i2": "Inbound tourists emit 9.2× more CO₂ per trip than Domestic (air travel impact)",
        "i3": "A 10% reduction strategy could save 6.82 MT CO₂ — equivalent to 324,619 trees",
        "i4": "Saudi tourism CO₂/tourist (1.8 kg) is below the global average (2.4 kg) — efficient",
        # ESG
        "esg_carbon":   "Carbon Tracking",    "esg_carbon_s": "Full 10-year CO₂ dataset",
        "esg_target":   "Reduction Target",   "esg_target_s": "10% scenario modeled",
        "esg_report":   "ESG Reporting",      "esg_report_s": "Vision 2030 aligned",
        "esg_offset":   "Offset Strategy",    "esg_offset_s": "Tree planting calculator",
        "esg_bench":    "Global Benchmark",   "esg_bench_s":  "vs. Turkey, UAE, Egypt",
        "esg_score":    "ESG Score",          "esg_score_v":  "78/100",
        # Benchmark
        "country":      "Destination",
        "bm_co2":       "CO₂/Tourist (kg)",
        "bm_tourists":  "Tourists (M)",
        "bm_total":     "Total CO₂ (MT)",
        "trees_label":  "Trees needed to offset 10%",
        "saved_label":  "CO₂ saved (MT)",
    },
    "AR": {
        "page_title":    "🌱 مؤشر الأثر الكربوني",
        "subtitle":      "انبعاثات CO₂ · مقاييس الاستدامة · استراتيجية السياحة الخضراء · تقارير ESG",
        "built_by":      "من تطوير",
        "dark_mode":     "🌙 داكن","light_mode": "☀️ فاتح","lang_toggle": "🌐 English",
        "pages":         "التنقل",
        "page_overview": "🏠 نظرة عامة","page_trends":   "📈 اتجاهات السياحة",
        "page_season":   "📅 الموسمية", "page_spend":    "💰 الإنفاق",
        "page_overnight":"🏨 ليالي الإقامة","page_forecast":"🔮 التوقعات",
        "page_segment":  "🎯 تقسيم السياح","page_carbon":  "🌱 الأثر الكربوني",
        "kpi_total":    "إجمالي CO₂ 2024",
        "kpi_inbound":  "CO₂/وافد",
        "kpi_domestic": "CO₂/محلي",
        "kpi_growth":   "نمو CO₂ 2024",
        "kpi_trees":    "أشجار لتعويض 10%",
        "trend_title":  "اتجاه انبعاثات CO₂ السنوية 2015–2024",
        "breakdown":    "تفصيل CO₂ حسب نوع السائح",
        "intensity":    "كثافة الكربون لكل سائح",
        "reduction":    "سيناريو تخفيض 10% — محاكي التأثير",
        "benchmark":    "مقارنة بالمعايير العالمية",
        "esg_title":    "بطاقة تقييم الاستدامة ESG",
        "donut_title":  "توزيع انبعاثات 2024",
        "insight_title":"أبرز الاستنتاجات",
        "inbound":      "وافد","domestic":    "محلي","total":       "إجمالي",
        "co2_mt":       "CO₂ (ميجاطن)","co2_kg": "CO₂ (كجم/سائح)",
        "year":         "السنة","reduction_lbl":"نسبة التخفيض",
        "filter_type":  "نوع السائح","all_types":  "الكل",
        "scenario_slider":"سيناريو التخفيض (%)",
        "i1": "إجمالي CO₂ 2024: 68.17 ميجاطن — +23.2% مدفوعاً بتعافي الوافدين",
        "i2": "الوافدون يصدرون 9.2 ضعف CO₂ لكل رحلة مقارنة بالمحليين (تأثير الطيران)",
        "i3": "تخفيض 10% يوفر 6.82 ميجاطن CO₂ — يعادل زراعة 324,619 شجرة",
        "i4": "CO₂/سائح سعودي (1.8 كجم) أقل من المتوسط العالمي (2.4 كجم) — كفاءة عالية",
        "esg_carbon":   "تتبع الكربون",     "esg_carbon_s": "بيانات CO₂ لـ 10 سنوات كاملة",
        "esg_target":   "هدف التخفيض",      "esg_target_s": "نمذجة سيناريو 10%",
        "esg_report":   "تقارير ESG",        "esg_report_s": "متوافق مع رؤية 2030",
        "esg_offset":   "استراتيجية التعويض","esg_offset_s": "حاسبة زراعة الأشجار",
        "esg_bench":    "المعيار العالمي",   "esg_bench_s":  "مقارنة بتركيا والإمارات ومصر",
        "esg_score":    "نقاط ESG",          "esg_score_v":  "78/100",
        "country":      "الوجهة",
        "bm_co2":       "CO₂/سائح (كجم)",
        "bm_tourists":  "السياح (مليون)",
        "bm_total":     "إجمالي CO₂ (ميجاطن)",
        "trees_label":  "أشجار لتعويض 10%",
        "saved_label":  "CO₂ موفّر (ميجاطن)",
    }
}
t = T[lang]

# ══════════════════════════════════════════
# THEME
# ══════════════════════════════════════════
if theme == "dark":
    bg_main="#0A1A0F"; bg_card="#0F2318"; bg_card2="#0D1E14"
    text_primary="#E8F5E9"; text_secondary="#81C784"
    accent_green="#00E676"; accent_teal="#00BFA5"
    accent_gold="#FFD54F"; accent_blue="#40C4FF"
    accent_lime="#B2FF59"; accent_red="#FF5252"
    accent_orange="#FF9800"; border_color="#1B3A22"
    glow="#00E67622"; chart_bg="rgba(10,26,15,0)"; plotly_tmpl="plotly_dark"
else:
    bg_main="#F1F8F2"; bg_card="#FFFFFF"; bg_card2="#E8F5E9"
    text_primary="#1B3A22"; text_secondary="#388E3C"
    accent_green="#2E7D32"; accent_teal="#00695C"
    accent_gold="#F57F17"; accent_blue="#0277BD"
    accent_lime="#558B2F"; accent_red="#C62828"
    accent_orange="#E65100"; border_color="#C8E6C9"
    glow="#2E7D3218"; chart_bg="rgba(241,248,242,0)"; plotly_tmpl="plotly_white"

dir_attr = "rtl" if lang=="AR" else "ltr"
font_fam  = "Tajawal" if lang=="AR" else "Sora"

# ══════════════════════════════════════════
# DATA
# ══════════════════════════════════════════
years = list(range(2015, 2025))

# CO₂ in MegaTons
co2_inbound  = [10.52,10.55,9.42,8.96,10.24,2.42,2.22,10.63,17.40,18.99]
co2_domestic = [23.22,22.52,21.91,21.63,23.91,21.06,31.92,38.92,40.96,43.08]
co2_total    = [a+b for a,b in zip(co2_inbound, co2_domestic)]

# CO₂ intensity (kg per tourist)
intensity_inbound  = [0.585,0.585,0.585,0.585,0.585,0.585,0.638,0.639,0.640,0.639]
intensity_domestic = [0.500,0.500,0.500,0.500,0.500,0.500,0.500,0.500,0.500,0.500]

# Benchmark countries
benchmark = [
    ("Saudi Arabia", 1.80, 115.9, 68.17, accent_green),
    ("Turkey",       2.10, 49.2,  103.3, accent_blue),
    ("UAE",          3.40, 17.2,   58.5, accent_gold),
    ("Egypt",        1.50, 14.9,   22.4, accent_teal),
    ("Global Avg",   2.40, None,   None, accent_orange),
]

# ══════════════════════════════════════════
# CSS
# ══════════════════════════════════════════
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800;900&family=IBM+Plex+Mono:wght@400;600;700&family=Tajawal:wght@300;400;700;800;900&display=swap');
  html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{{
    background:{bg_main}!important;
    font-family:'{font_fam}',sans-serif;
    direction:{dir_attr};
  }}
  [data-testid="stSidebar"]{{background:{bg_card}!important;border-right:1px solid {border_color};}}
  [data-testid="stSidebar"] *{{color:{text_primary}!important;}}

  .page-header{{
    position:relative;overflow:hidden;
    background:linear-gradient(135deg,{bg_card} 0%,{bg_card2} 100%);
    border:1px solid {border_color};border-left:4px solid {accent_green};
    border-radius:20px;padding:32px 36px;margin-bottom:26px;
  }}
  .page-header::before{{
    content:'';position:absolute;top:-60px;right:-60px;
    width:220px;height:220px;border-radius:50%;
    background:radial-gradient({accent_green}18,transparent 70%);
  }}
  .page-header::after{{
    content:'🌱';position:absolute;right:28px;top:50%;
    transform:translateY(-50%);font-size:4.5rem;opacity:.07;
  }}
  .ph-tag{{
    display:inline-block;background:{accent_green}18;
    border:1px solid {accent_green}55;color:{accent_green};
    font-size:.62rem;font-weight:700;letter-spacing:1.8px;
    text-transform:uppercase;padding:4px 14px;border-radius:20px;margin-bottom:10px;
  }}
  .ph-title{{font-size:1.9rem;font-weight:900;color:{text_primary};margin:0 0 4px;letter-spacing:-.5px;}}
  .ph-sub{{font-size:.82rem;color:{accent_green};font-weight:600;letter-spacing:.5px;}}

  .kpi-row{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:26px;}}
  .kpi{{
    background:{bg_card};border:1px solid {border_color};
    border-radius:15px;padding:18px 14px;text-align:center;
    transition:transform .2s,box-shadow .2s;
  }}
  .kpi:hover{{transform:translateY(-3px);box-shadow:0 8px 28px {glow};}}
  .kpi-ico{{font-size:1.4rem;margin-bottom:6px;}}
  .kpi-val{{font-size:1.38rem;font-weight:900;line-height:1.1;font-family:'IBM Plex Mono',monospace;}}
  .kpi-lbl{{font-size:.63rem;color:{text_secondary};text-transform:uppercase;letter-spacing:.8px;font-weight:600;margin-top:4px;}}
  .kpi-sub{{font-size:.72rem;font-weight:600;margin-top:3px;font-family:'IBM Plex Mono',monospace;color:{text_secondary};}}

  .sec-title{{
    font-size:1.05rem;font-weight:800;color:{text_primary};
    margin:24px 0 14px;padding-bottom:8px;
    border-bottom:2px solid {accent_green};
  }}

  .scenario-box{{
    background:{bg_card};border:1px solid {border_color};border-radius:16px;
    padding:24px 22px;
  }}
  .sc-row{{display:flex;justify-content:space-between;align-items:center;
    padding:9px 0;border-bottom:1px solid {border_color};}}
  .sc-row:last-child{{border-bottom:none;}}
  .sc-label{{font-size:.82rem;color:{text_primary};font-weight:500;}}
  .sc-val{{font-size:.88rem;font-weight:800;font-family:'IBM Plex Mono',monospace;}}

  .esg-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:26px;}}
  .esg-card{{
    background:{bg_card};border:1px solid {border_color};border-radius:14px;
    padding:18px 16px;display:flex;align-items:flex-start;gap:12px;
    transition:transform .2s;
  }}
  .esg-card:hover{{transform:translateY(-2px);}}
  .esg-ico{{font-size:1.4rem;flex-shrink:0;}}
  .esg-title{{font-size:.85rem;font-weight:700;color:{text_primary};margin-bottom:3px;}}
  .esg-sub{{font-size:.73rem;color:{text_secondary};line-height:1.4;}}

  .bm-table{{width:100%;border-collapse:collapse;font-size:.82rem;}}
  .bm-table th{{background:{bg_card2};color:{text_secondary};padding:9px 12px;
    text-align:center;font-size:.68rem;text-transform:uppercase;
    letter-spacing:.8px;border-bottom:1px solid {border_color};}}
  .bm-table td{{padding:9px 12px;text-align:center;border-bottom:1px solid {border_color};
    font-family:'IBM Plex Mono',monospace;}}
  .bm-table tr:last-child td{{border-bottom:none;}}
  .bm-table tr:hover td{{background:{bg_card2};}}

  .insight-card{{
    background:{bg_card};border:1px solid {border_color};border-radius:12px;
    padding:14px 16px;display:flex;align-items:flex-start;gap:10px;margin-bottom:10px;
  }}
  .ins-ico{{font-size:1.2rem;flex-shrink:0;margin-top:2px;}}
  .ins-txt{{font-size:.83rem;color:{text_primary};line-height:1.55;}}

  .footer-bar{{
    background:{bg_card};border:1px solid {border_color};
    border-top:3px solid {accent_green};border-radius:16px;
    padding:16px 24px;margin-top:28px;display:flex;
    justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;
  }}
  .footer-name{{font-size:.82rem;font-weight:800;color:{accent_green};}}
  .footer-sub{{font-size:.7rem;color:{text_secondary};margin-top:2px;}}
  .footer-link a{{color:{accent_blue}!important;text-decoration:none;font-weight:600;font-size:.75rem;}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════
with st.sidebar:
    try:
        import os, base64
        base_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_dir,"assets","logo.png")
        with open(logo_path,"rb") as f:
            lb = base64.b64encode(f.read()).decode()
        st.markdown(f"<img src='data:image/png;base64,{lb}' style='width:100%;border-radius:12px;margin-bottom:6px;'/>", unsafe_allow_html=True)
    except:
        st.markdown(f"<div style='text-align:center;font-size:1.8rem;padding:8px;'>🇸🇦</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='text-align:center;margin-bottom:4px;'>
      <div style='font-size:.82rem;font-weight:800;color:{accent_green};'>Saudi Tourism Intelligence</div>
      <div style='font-size:.64rem;color:{text_secondary};'>Vision 2030 · AI Analytics Platform</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    c1,c2 = st.columns(2)
    with c1:
        if st.button(t["light_mode"] if theme=="dark" else t["dark_mode"], use_container_width=True):
            st.session_state.theme="light" if theme=="dark" else "dark"; st.rerun()
    with c2:
        if st.button(t["lang_toggle"], use_container_width=True):
            st.session_state.lang="AR" if lang=="EN" else "EN"; st.rerun()

    st.divider()
    st.markdown(f"<div style='font-size:.7rem;font-weight:700;color:{text_secondary};text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>{t['pages']}</div>", unsafe_allow_html=True)
    for pk in ["page_overview","page_trends","page_season","page_spend","page_overnight","page_forecast","page_segment","page_carbon"]:
        active = pk=="page_carbon"
        bg = f"{accent_green}22" if active else "transparent"
        fw = "700" if active else "400"
        bc = accent_green if active else "transparent"
        st.markdown(f"<div style='padding:7px 11px;border-radius:9px;background:{bg};border-left:3px solid {bc};font-size:.82rem;font-weight:{fw};color:{text_primary};margin-bottom:3px;'>{t[pk]}</div>", unsafe_allow_html=True)

    st.divider()
    tourist_filter = st.selectbox(t["filter_type"], [t["all_types"],t["inbound"],t["domestic"]])
    reduction_pct  = st.slider(t["scenario_slider"], 5, 30, 10)

    st.divider()
    st.markdown(f"""
    <div style='font-size:.7rem;color:{text_secondary};'>
      <div style='font-weight:700;color:{accent_green};margin-bottom:4px;'>{t['built_by']}</div>
      <div style='color:{text_primary};font-weight:700;margin-bottom:6px;'>Eng. Goda Emad</div>
      <a href='https://github.com/Goda-Emad/Saudi-Tourism-Intelligence' target='_blank' style='color:{accent_blue};font-weight:600;'>🐙 GitHub</a>
      &nbsp;&nbsp;
      <a href='https://www.linkedin.com/in/goda-emad/' target='_blank' style='color:{accent_blue};font-weight:600;'>💼 LinkedIn</a>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════
st.markdown(f"""
<div class='page-header'>
  <div class='ph-tag'>🌍 ESG · SUSTAINABILITY · VISION 2030</div>
  <div class='ph-title'>{t['page_title']}</div>
  <div class='ph-sub'>{t['subtitle']}</div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════
co2_saved  = round(co2_total[-1] * reduction_pct / 100, 2)
trees_need = int(co2_saved * 1e6 / 21)   # 21 kg CO2/tree/year

st.markdown(f"""
<div class='kpi-row'>
  <div class='kpi'>
    <div class='kpi-ico'>🌍</div>
    <div class='kpi-val' style='color:{accent_red};'>68.17 MT</div>
    <div class='kpi-lbl'>{t['kpi_total']}</div>
    <div class='kpi-sub'>MegaTons CO₂</div>
  </div>
  <div class='kpi'>
    <div class='kpi-ico'>✈️</div>
    <div class='kpi-val' style='color:{accent_orange};'>0.639 kg</div>
    <div class='kpi-lbl'>{t['kpi_inbound']}</div>
    <div class='kpi-sub'>per tourist</div>
  </div>
  <div class='kpi'>
    <div class='kpi-ico'>🏠</div>
    <div class='kpi-val' style='color:{accent_teal};'>0.500 kg</div>
    <div class='kpi-lbl'>{t['kpi_domestic']}</div>
    <div class='kpi-sub'>per tourist</div>
  </div>
  <div class='kpi'>
    <div class='kpi-ico'>📈</div>
    <div class='kpi-val' style='color:{accent_red};'>+23.2%</div>
    <div class='kpi-lbl'>{t['kpi_growth']}</div>
    <div class='kpi-sub'>vs 2023</div>
  </div>
  <div class='kpi'>
    <div class='kpi-ico'>🌳</div>
    <div class='kpi-val' style='color:{accent_green};'>{trees_need:,}</div>
    <div class='kpi-lbl'>{t['kpi_trees']}</div>
    <div class='kpi-sub'>{reduction_pct}% scenario</div>
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# CHART 1 — Annual Trend
# ══════════════════════════════════════════
st.markdown(f"<div class='sec-title'>📊 {t['trend_title']}</div>", unsafe_allow_html=True)

y_filter = tourist_filter
fig_trend = go.Figure()

if y_filter in [t["all_types"], t["inbound"]]:
    fig_trend.add_trace(go.Bar(
        x=years, y=co2_inbound, name=t["inbound"],
        marker_color=accent_orange, opacity=.85,
        hovertemplate="<b>%{x}</b><br>Inbound CO₂: %{y:.2f} MT<extra></extra>"
    ))
if y_filter in [t["all_types"], t["domestic"]]:
    fig_trend.add_trace(go.Bar(
        x=years, y=co2_domestic, name=t["domestic"],
        marker_color=accent_teal, opacity=.85,
        hovertemplate="<b>%{x}</b><br>Domestic CO₂: %{y:.2f} MT<extra></extra>"
    ))
if y_filter == t["all_types"]:
    fig_trend.add_trace(go.Scatter(
        x=years, y=co2_total, name=t["total"],
        line=dict(color=accent_green, width=2.5, dash="dot"),
        marker=dict(size=7), yaxis="y2"
    ))

fig_trend.add_vrect(x0=2019.5,x1=2021.5,fillcolor=accent_red,opacity=.06,
    annotation_text="COVID",annotation=dict(font_color=accent_red,font_size=10))

# Reduction forecast band
if y_filter == t["all_types"]:
    target_line = [v*(1 - reduction_pct/100) for v in co2_total]
    fig_trend.add_trace(go.Scatter(
        x=years, y=target_line, name=f"-{reduction_pct}% Target",
        line=dict(color=accent_lime, width=1.8, dash="dashdot"),
        marker=dict(size=5), yaxis="y2"
    ))

fig_trend.update_layout(
    template=plotly_tmpl, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
    height=370, barmode="stack", margin=dict(l=10,r=10,t=20,b=10),
    legend=dict(orientation="h",y=-0.12,font=dict(size=11)),
    xaxis=dict(showgrid=False, tickfont=dict(size=11)),
    yaxis=dict(showgrid=True,gridcolor=border_color,tickfont=dict(size=10),title=t["co2_mt"]),
    yaxis2=dict(overlaying="y",side="right",showgrid=False,tickfont=dict(size=10),title="Total MT"),
    font=dict(color=text_primary),
)
st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar":False})

# ══════════════════════════════════════════
# CHART 2+3 — Intensity + Donut
# ══════════════════════════════════════════
int_col, donut_col = st.columns([3,2])

with int_col:
    st.markdown(f"<div class='sec-title'>🔬 {t['intensity']}</div>", unsafe_allow_html=True)
    fig_int = go.Figure()
    fig_int.add_trace(go.Scatter(
        x=years, y=intensity_inbound,
        name=t["inbound"],
        line=dict(color=accent_orange, width=2.5),
        fill="tozeroy", fillcolor=f"{accent_orange}18",
        marker=dict(size=8, color=accent_orange, line=dict(color=bg_card,width=2)),
        text=[f"{v:.3f}" for v in intensity_inbound],
        textposition="top center", mode="lines+markers+text",
        textfont=dict(size=8, color=accent_orange)
    ))
    fig_int.add_trace(go.Scatter(
        x=years, y=intensity_domestic,
        name=t["domestic"],
        line=dict(color=accent_teal, width=2.5),
        fill="tozeroy", fillcolor=f"{accent_teal}18",
        marker=dict(size=8, color=accent_teal, line=dict(color=bg_card,width=2)),
    ))
    fig_int.add_hline(y=2.4/1000, line_dash="dash", line_color=accent_red,
        annotation_text="Global Avg", annotation_font_color=accent_red,
        annotation_font_size=10)
    fig_int.update_layout(
        template=plotly_tmpl, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=320, margin=dict(l=10,r=10,t=10,b=10),
        legend=dict(orientation="h",y=-0.15,font=dict(size=10)),
        xaxis=dict(showgrid=False,tickfont=dict(size=10)),
        yaxis=dict(showgrid=True,gridcolor=border_color,tickfont=dict(size=10),title=t["co2_kg"]),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_int, use_container_width=True, config={"displayModeBar":False})

with donut_col:
    st.markdown(f"<div class='sec-title'>🍩 {t['donut_title']}</div>", unsafe_allow_html=True)
    fig_donut = go.Figure(go.Pie(
        labels=[t["inbound"], t["domestic"]],
        values=[co2_inbound[-1], co2_domestic[-1]],
        hole=0.62,
        marker=dict(
            colors=[accent_orange, accent_teal],
            line=dict(color=bg_main, width=3)
        ),
        textfont=dict(size=11),
        hovertemplate="<b>%{label}</b><br>%{value:.2f} MT<br>%{percent}<extra></extra>"
    ))
    fig_donut.add_annotation(
        text=f"<b>68.17</b><br>MT CO₂",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=13, color=text_primary)
    )
    fig_donut.update_layout(
        template=plotly_tmpl, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=320, margin=dict(l=10,r=10,t=10,b=10),
        legend=dict(orientation="h",y=-0.08,font=dict(size=11)),
        font=dict(color=text_primary),
    )
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar":False})

# ══════════════════════════════════════════
# CHART 4 + SCENARIO BOX
# ══════════════════════════════════════════
sim_col, bench_col = st.columns([2,3])

with sim_col:
    st.markdown(f"<div class='sec-title'>🎯 {t['reduction']} (-{reduction_pct}%)</div>", unsafe_allow_html=True)
    saved_total    = round(co2_total[-1] * reduction_pct / 100, 2)
    saved_inbound  = round(co2_inbound[-1] * reduction_pct / 100, 2)
    saved_domestic = round(co2_domestic[-1] * reduction_pct / 100, 2)
    trees_total    = int(saved_total * 1e6 / 21)
    cars_off       = int(saved_total * 1e6 / 4600)   # avg car 4.6T CO2/yr

    st.markdown(f"""
    <div class='scenario-box'>
      <div class='sc-row'>
        <span class='sc-label'>📉 {t['saved_label']}</span>
        <span class='sc-val' style='color:{accent_green};'>{saved_total:.2f} MT</span>
      </div>
      <div class='sc-row'>
        <span class='sc-label'>✈️ Inbound saved</span>
        <span class='sc-val' style='color:{accent_orange};'>{saved_inbound:.2f} MT</span>
      </div>
      <div class='sc-row'>
        <span class='sc-label'>🏠 Domestic saved</span>
        <span class='sc-val' style='color:{accent_teal};'>{saved_domestic:.2f} MT</span>
      </div>
      <div class='sc-row'>
        <span class='sc-label'>🌳 {t['trees_label']}</span>
        <span class='sc-val' style='color:{accent_lime};'>{trees_total:,}</span>
      </div>
      <div class='sc-row'>
        <span class='sc-label'>🚗 Cars removed equiv.</span>
        <span class='sc-val' style='color:{accent_gold};'>{cars_off:,}</span>
      </div>
      <div class='sc-row'>
        <span class='sc-label'>📊 Remaining CO₂</span>
        <span class='sc-val' style='color:{text_secondary};'>{co2_total[-1]-saved_total:.2f} MT</span>
      </div>
    </div>""", unsafe_allow_html=True)

    # mini gauge chart
    pct_done = reduction_pct
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct_done,
        title=dict(text="Reduction Target %", font=dict(color=text_primary, size=12)),
        number=dict(suffix="%", font=dict(color=accent_green, size=28)),
        gauge=dict(
            axis=dict(range=[0,30], tickfont=dict(color=text_secondary,size=9)),
            bar=dict(color=accent_green, thickness=0.7),
            bgcolor=bg_card2,
            bordercolor=border_color,
            steps=[
                dict(range=[0,10], color=f"{accent_teal}33"),
                dict(range=[10,20],color=f"{accent_gold}33"),
                dict(range=[20,30],color=f"{accent_red}33"),
            ],
            threshold=dict(line=dict(color=accent_lime,width=3), value=10)
        )
    ))
    fig_gauge.update_layout(
        template=plotly_tmpl, paper_bgcolor=chart_bg,
        height=220, margin=dict(l=20,r=20,t=30,b=10),
        font=dict(color=text_primary)
    )
    st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar":False})

with bench_col:
    st.markdown(f"<div class='sec-title'>🌍 {t['benchmark']}</div>", unsafe_allow_html=True)

    # Benchmark bar chart
    bm_countries = [b[0] for b in benchmark if b[2]]
    bm_co2_vals  = [b[1] for b in benchmark if b[2]]
    bm_colors    = [b[4] for b in benchmark if b[2]]

    fig_bm = go.Figure()
    fig_bm.add_trace(go.Bar(
        x=bm_countries, y=bm_co2_vals,
        marker_color=bm_colors, opacity=.88,
        text=[f"{v:.2f} kg" for v in bm_co2_vals],
        textposition="outside", textfont=dict(size=11,color=text_primary)
    ))
    fig_bm.add_hline(y=2.4, line_dash="dash", line_color=accent_red, line_width=1.5,
        annotation_text="Global Avg: 2.4 kg",
        annotation_font_color=accent_red, annotation_font_size=10)
    fig_bm.add_annotation(
        x="Saudi Arabia", y=1.80,
        text="✅ Below avg!", showarrow=True, arrowhead=2,
        font=dict(size=10, color=accent_green), arrowcolor=accent_green, ay=-40
    )
    fig_bm.update_layout(
        template=plotly_tmpl, paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        height=260, margin=dict(l=10,r=10,t=30,b=10),
        xaxis=dict(showgrid=False,tickfont=dict(size=11)),
        yaxis=dict(showgrid=True,gridcolor=border_color,tickfont=dict(size=10),title=t["bm_co2"]),
        font=dict(color=text_primary), showlegend=False,
    )
    st.plotly_chart(fig_bm, use_container_width=True, config={"displayModeBar":False})

    # Benchmark Table
    table_html = f"""
    <table class='bm-table'>
      <thead><tr>
        <th>{t['country']}</th>
        <th>{t['bm_co2']}</th>
        <th>{t['bm_tourists']}</th>
        <th>{t['bm_total']}</th>
      </tr></thead>
      <tbody>"""
    for name, co2kg, tourists, total_co2, color in benchmark:
        t_str = f"{tourists:.1f}" if tourists else "—"
        c_str = f"{total_co2:.1f}" if total_co2 else "—"
        is_sa = name == "Saudi Arabia"
        row_bg = f"background:{color}15;" if is_sa else ""
        fw = "font-weight:800;" if is_sa else ""
        table_html += f"""
        <tr style='{row_bg}'>
          <td style='color:{color};{fw}font-family:Sora,sans-serif;text-align:left;padding-left:14px;'>{name}</td>
          <td style='color:{text_primary};{fw}'>{co2kg:.2f}</td>
          <td style='color:{text_secondary};'>{t_str}</td>
          <td style='color:{text_primary};{fw}'>{c_str}</td>
        </tr>"""
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)

# ══════════════════════════════════════════
# ESG SCORECARD
# ══════════════════════════════════════════
st.markdown(f"<div class='sec-title'>♻️ {t['esg_title']}</div>", unsafe_allow_html=True)

esg_items = [
    ("📊", t["esg_carbon"],  t["esg_carbon_s"],  accent_green),
    ("🎯", t["esg_target"],  t["esg_target_s"],  accent_teal),
    ("📋", t["esg_report"],  t["esg_report_s"],  accent_gold),
    ("🌳", t["esg_offset"],  t["esg_offset_s"],  accent_lime),
    ("🌍", t["esg_bench"],   t["esg_bench_s"],   accent_blue),
    ("🏆", t["esg_score"],   t["esg_score_v"],   accent_orange),
]
st.markdown("<div class='esg-grid'>", unsafe_allow_html=True)
for ico, title, sub, color in esg_items:
    st.markdown(f"""
    <div class='esg-card' style='border-left:3px solid {color};'>
      <div class='esg-ico'>{ico}</div>
      <div>
        <div class='esg-title'>{title}</div>
        <div class='esg-sub'>{sub}</div>
      </div>
    </div>""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# KEY INSIGHTS
# ══════════════════════════════════════════
st.markdown(f"<div class='sec-title'>💡 {t['insight_title']}</div>", unsafe_allow_html=True)
insights = [
    ("🌍", t["i1"], accent_red),
    ("✈️", t["i2"], accent_orange),
    ("🌳", t["i3"], accent_green),
    ("✅", t["i4"], accent_teal),
]
ins_cols = st.columns(2)
for i,(ico,txt,col) in enumerate(insights):
    with ins_cols[i%2]:
        st.markdown(f"""
        <div class='insight-card' style='border-left:3px solid {col};'>
          <div class='ins-ico'>{ico}</div>
          <div class='ins-txt'>{txt}</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════
st.markdown(f"""
<div class='footer-bar'>
  <div>
    <div class='footer-name'>Eng. Goda Emad — Saudi Tourism Intelligence</div>
    <div class='footer-sub'>Data: DataSaudi · Ministry of Economy & Planning · 2015–2024</div>
  </div>
  <div style='display:flex;gap:16px;'>
    <div class='footer-link'><a href='https://github.com/Goda-Emad/Saudi-Tourism-Intelligence' target='_blank'>🐙 GitHub</a></div>
    <div class='footer-link'><a href='https://www.linkedin.com/in/goda-emad/' target='_blank'>💼 LinkedIn</a></div>
  </div>
</div>""", unsafe_allow_html=True)
