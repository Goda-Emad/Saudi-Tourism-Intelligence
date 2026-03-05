# ═══════════════════════════════════════════════════════════════════
#  Saudi Tourism Intelligence — Segmentation
#  Author : Eng. Goda Emad   |   Design : DataSaudi
# ═══════════════════════════════════════════════════════════════════
import streamlit as st
import plotly.graph_objects as go
import random, base64, os, sys

# ── Path setup ───────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in [_HERE, _ROOT]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="Tourist Segmentation · Saudi Tourism Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

for k, v in [("lang", "EN"), ("theme", "dark")]:
    if k not in st.session_state:
        st.session_state[k] = v

THEME, LANG = render_sidebar()

# ── Colors ───────────────────────────────────────────────────────
C = {
    "teal":"#17B19B","teal_act":"#149581","bg":"#1A1E1F",
    "sec_bg":"#161B1C","card_bg":"#1E2528","navbar":"#031414",
    "white":"#F4F9F8","grey":"#A1A6B7","foot_txt":"#B5B8B7",
    "border":"#2A3235","orange":"#F4D044","gold":"#C9A84C",
    "blue":"#3A86FF","green":"#22C55E","red":"#EF4444","purple":"#BB86FC",
} if THEME == "dark" else {
    "teal":"#17B19B","teal_act":"#149581","bg":"#F0F5F4",
    "sec_bg":"#E4EDEB","card_bg":"#FFFFFF","navbar":"#172025",
    "white":"#F4F9F8","grey":"#9DBFBA","foot_txt":"#9DBFBA",
    "border":"#2A3235","orange":"#E8A020","gold":"#C9A84C",
    "blue":"#1565C0","green":"#16A34A","red":"#DC2626","purple":"#6A1B9A",
}

def clr(k): return C.get(k, C["teal"])
ff      = "Tajawal" if LANG == "AR" else "IBM Plex Sans"
dir_val = "rtl"     if LANG == "AR" else "ltr"

# Shorthand color aliases (used in charts/cards)
bg_main        = C["bg"]
bg_card        = C["card_bg"]
bg_card2       = C["sec_bg"]
text_primary   = C["white"]
text_secondary = C["grey"]
accent_teal    = C["teal"]
accent_gold    = C["gold"]
accent_blue    = C["blue"]
accent_green   = C["green"]
accent_red     = C["red"]
accent_purple  = C["purple"]
border_color   = C["border"]
chart_bg       = "rgba(0,0,0,0)"
plotly_template = "plotly_dark" if THEME == "dark" else "plotly_white"

# ── Logo ─────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def _b64(p):
    try:
        with open(os.path.join(_ROOT, p), "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

logo_b64 = _b64("assets/logo.jpg")
logo_src = "data:image/jpeg;base64," + logo_b64 if logo_b64 else ""
logo_img = (f'<img src="{logo_src}" style="height:42px;border-radius:8px;"/>'
            if logo_src else '<span style="font-size:2rem;">🇸🇦</span>')

# ── Translations ─────────────────────────────────────────────────
TR = {
"EN": {
    "page_title":"🎯 Tourist Segmentation",
    "subtitle":"K-Means Clustering · 3 Segments · Spending & Stay Behavior · Strategic Insights",
    "seg_high":"High-Value","seg_mid":"Mid-Value","seg_budget":"Budget",
    "kpi_segments":"Total Segments","kpi_silhouette":"Silhouette Score",
    "kpi_high_spend":"High-Value Avg Spend","kpi_budget_size":"Budget Segment Size",
    "kpi_algo":"Algorithm",
    "segment_overview":"Segment Overview & Profiles",
    "scatter_title":"Spending vs Length of Stay — Cluster Map",
    "radar_title":"Segment Comparison — Radar Chart",
    "size_title":"Segment Size Distribution",
    "timeline_title":"Segment Evolution Over Time",
    "strategy_title":"Business Strategy by Segment",
    "k_choice":"K Selection (Silhouette)",
    "features_used":"Features Used",
    "tourists":"Tourists","avg_trip":"Avg Spend/Trip","avg_night":"Avg Spend/Night",
    "avg_los":"Avg Length of Stay","type":"Tourist Type","years":"Years Active",
    "nights":"nights","sar":"SAR","millions":"M",
    "insight_title":"Key Insights",
    "i1":"High-Value segment emerged after 2022 — Inbound tourists now stay 17+ nights",
    "i2":"Budget segment (Domestic) is 3x larger but generates 4x less revenue per trip",
    "i3":"Inbound transitioned from Mid-Value to High-Value segment post-pandemic",
    "i4":"Targeting High-Value segment = 4.4x more revenue with same tourist count",
    "strategy_high":"Focus: Luxury experiences, long-stay packages, premium hospitality",
    "strategy_mid":"Focus: Group tours, cultural experiences, mid-range accommodation",
    "strategy_budget":"Focus: Domestic destinations, family packages, affordable activities",
},
"AR": {
    "page_title":"🎯 تقسيم السياح",
    "subtitle":"تجميع K-Means · 3 شرائح · سلوك الإنفاق والإقامة · استنتاجات استراتيجية",
    "seg_high":"عالي القيمة","seg_mid":"متوسط القيمة","seg_budget":"اقتصادي",
    "kpi_segments":"إجمالي الشرائح","kpi_silhouette":"نتيجة Silhouette",
    "kpi_high_spend":"إنفاق عالي القيمة","kpi_budget_size":"حجم الشريحة الاقتصادية",
    "kpi_algo":"الخوارزمية",
    "segment_overview":"نظرة عامة على الشرائح وملفاتها",
    "scatter_title":"الإنفاق مقابل مدة الإقامة — خريطة المجموعات",
    "radar_title":"مقارنة الشرائح — مخطط رادار",
    "size_title":"توزيع أحجام الشرائح",
    "timeline_title":"تطور الشرائح عبر الزمن",
    "strategy_title":"الاستراتيجية التجارية لكل شريحة",
    "k_choice":"اختيار K (Silhouette)",
    "features_used":"الميزات المستخدمة",
    "tourists":"السياح","avg_trip":"متوسط إنفاق/رحلة","avg_night":"متوسط إنفاق/ليلة",
    "avg_los":"متوسط مدة الإقامة","type":"نوع السائح","years":"سنوات النشاط",
    "nights":"ليالي","sar":"ريال","millions":"م",
    "insight_title":"أبرز الاستنتاجات",
    "i1":"شريحة عالي القيمة ظهرت بعد 2022 — الوافدون يقيمون الآن 17+ ليلة",
    "i2":"الشريحة الاقتصادية (المحلية) أكبر 3 مرات لكنها تولد إيرادات أقل 4 مرات لكل رحلة",
    "i3":"الوافدون انتقلوا من متوسط القيمة إلى عالي القيمة بعد الجائحة",
    "i4":"استهداف شريحة عالي القيمة = إيرادات أكثر 4.4x بنفس عدد السياح",
    "strategy_high":"التركيز: تجارب فاخرة، باقات إقامة طويلة، ضيافة متميزة",
    "strategy_mid":"التركيز: جولات جماعية، تجارب ثقافية، إقامة متوسطة",
    "strategy_budget":"التركيز: وجهات محلية، باقات عائلية، أنشطة بأسعار مناسبة",
},
}
t = TR[LANG]

# ── Data ─────────────────────────────────────────────────────────
segments = {
    "high": {
        "name": t["seg_high"], "color": accent_gold, "emoji": "💎",
        "tourists": 24514, "avg_trip": 5512, "avg_night": 510,
        "avg_los": 17.1, "type": "Inbound", "years": "2022–2024",
        "revenue_index": 100,
    },
    "mid": {
        "name": t["seg_mid"], "color": accent_blue, "emoji": "🌟",
        "tourists": 13232, "avg_trip": 4791, "avg_night": 430,
        "avg_los": 9.2, "type": "Inbound", "years": "2015–2021",
        "revenue_index": 87,
    },
    "budget": {
        "name": t["seg_budget"], "color": accent_teal, "emoji": "🏠",
        "tourists": 57822, "avg_trip": 1242, "avg_night": 220,
        "avg_los": 5.4, "type": "Domestic", "years": "2015–2024",
        "revenue_index": 23,
    },
}

k_values    = [2, 3, 4, 5]
silhouettes = [0.568, 0.630, 0.644, 0.573]

random.seed(42)
scatter_data = {
    "high":   [(random.gauss(17, 1.5), random.gauss(5512, 300)) for _ in range(30)],
    "mid":    [(random.gauss(9,  1.2), random.gauss(4791, 280)) for _ in range(25)],
    "budget": [(random.gauss(5.4, 0.8),random.gauss(1242, 150)) for _ in range(60)],
}

timeline_years = list(range(2015, 2025))
high_count   = [0,0,0,0,0,0,0,1,1,1]
mid_count    = [1,1,1,1,1,1,1,0,0,0]

# ════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ════════════════════════════════════════════════════════════════════
st.markdown(
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700"
    "&family=IBM+Plex+Mono:wght@400;600;700&family=Tajawal:wght@400;700;800&display=swap');"
    "[data-testid='stHeader'],[data-testid='stToolbar'],"
    "[data-testid='stSidebarNav'],footer,#MainMenu{display:none!important;}"
    ".block-container{padding:0!important;max-width:100%!important;}"
    "section[data-testid='stMain']>div:first-child{padding-top:0!important;}"
    ".ds-card{transition:transform .22s,box-shadow .22s,border-color .22s;}"
    ".ds-card:hover{transform:translateY(-3px);"
    "box-shadow:0 10px 28px rgba(23,177,155,.18)!important;}"
    f"html,body,[data-testid='stAppViewContainer'],[data-testid='stMain']"
    f"{{background:{C['bg']}!important;direction:{dir_val};"
    f"font-family:'{ff}',sans-serif;color:{C['white']}!important;}}"
    ".seg-card{background:var(--card-bg);border-radius:16px;padding:20px 18px;"
    "height:100%;transition:transform .2s,box-shadow .2s;}"
    ".seg-card:hover{transform:translateY(-3px);box-shadow:0 8px 24px rgba(0,0,0,.2);}"
    ".revenue-bar{height:8px;border-radius:4px;margin:4px 0;}"
    ".seg-row{display:flex;justify-content:space-between;padding:6px 0;"
    f"border-bottom:1px solid {C['border']};}} "
    ".seg-row:last-child{border-bottom:none;}"
    ".strategy-card{border-radius:14px;padding:18px;height:100%;}"
    ".insight-card{border-radius:12px;padding:14px 16px;"
    "display:flex;align-items:flex-start;gap:10px;margin-bottom:10px;}"
    "</style>",
    unsafe_allow_html=True)

# ── Helpers ──────────────────────────────────────────────────────
def sec_head(badge, h2):
    return (
        f'<div style="margin-bottom:18px;">'
        f'<div style="display:inline-block;background:{C["teal"]}15;'
        f'border:1px solid {C["teal"]}44;color:{C["teal"]};'
        f'font-size:.57rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;'
        f'padding:4px 12px;border-radius:4px;margin-bottom:10px;">{badge}</div>'
        f'<div style="font-size:1.25rem;font-weight:700;color:{C["white"]};">{h2}</div>'
        f'</div>')

def kpi_card(ico, lbl, val, sub, ck):
    return (
        f'<div class="ds-card" style="background:{C["card_bg"]};border:1px solid {C["border"]};'
        f'border-top:3px solid {clr(ck)};border-radius:10px;padding:20px 16px;text-align:center;">'
        f'<div style="font-size:1.4rem;margin-bottom:6px;">{ico}</div>'
        f'<div style="font-size:1.45rem;font-weight:800;color:{clr(ck)};'
        f'font-family:IBM Plex Mono,monospace;letter-spacing:-1px;line-height:1.1;">{val}</div>'
        f'<div style="font-size:.62rem;color:{C["grey"]};text-transform:uppercase;'
        f'letter-spacing:.8px;font-weight:600;margin:6px 0 4px;">{lbl}</div>'
        f'<div style="font-size:.72rem;color:{C["grey"]};font-family:IBM Plex Mono,monospace;">{sub}</div>'
        f'</div>')

def apply_layout(fig, height=340):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=C["grey"], family=ff),
        height=height, margin=dict(l=10,r=10,t=36,b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11),
                    orientation="h", y=-0.14),
        xaxis=dict(gridcolor="rgba(42,50,53,0.4)", linecolor="#2A3235",
                   tickfont=dict(size=10), showgrid=False),
        yaxis=dict(gridcolor="rgba(42,50,53,0.4)", linecolor="#2A3235",
                   tickfont=dict(size=10)),
    )
    return fig

def chart(fig):
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div style="background:{C["navbar"]};border-bottom:1px solid {C["border"]};'
    f'padding:24px 40px 20px;">'
    f'<div style="display:inline-block;background:{C["purple"]}22;border:1px solid {C["purple"]}55;'
    f'color:{C["purple"]};font-size:.57rem;font-weight:700;letter-spacing:2.5px;'
    f'text-transform:uppercase;padding:4px 12px;border-radius:4px;margin-bottom:10px;">'
    f'SEGMENTATION · K-MEANS CLUSTERING</div>'
    f'<div style="font-size:1.85rem;font-weight:800;color:#F4F9F8;'
    f'letter-spacing:-.5px;margin-bottom:5px;">{t["page_title"]}</div>'
    f'<div style="font-size:.82rem;color:#A1A6B7;">{t["subtitle"]}</div>'
    f'</div>',
    unsafe_allow_html=True)

# ── Model badges ─────────────────────────────────────────────────
badge_style = (f'display:inline-block;background:{C["sec_bg"]};border:1px solid {C["border"]};'
               f'border-radius:20px;padding:5px 14px;font-size:.78rem;color:{C["white"]};'
               f'font-weight:600;margin:4px;')
st.markdown(
    f'<div style="padding:16px 40px 0;">'
    f'<span style="{badge_style}">🤖 {t["kpi_algo"]}: K-Means (k=3)</span>'
    f'<span style="{badge_style}">📊 Silhouette: 0.630</span>'
    f'<span style="{badge_style}">📐 Scaler: StandardScaler</span>'
    f'<span style="{badge_style}">🗂️ {t["features_used"]}: 5 features</span>'
    f'<span style="{badge_style}">📅 Data: 2015–2024</span>'
    f'</div>',
    unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# KPI STRIP
# ════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div style="padding:20px 40px 0;">'
    f'<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;">'
    + kpi_card("🎯", t["kpi_segments"],   "3",          "K-Means",      "teal")
    + kpi_card("📊", t["kpi_silhouette"], "0.630",      "k=3 selected", "gold")
    + kpi_card("💎", t["kpi_high_spend"], "SAR 5,512",  "/trip avg",    "gold")
    + kpi_card("🏠", t["kpi_budget_size"],"57,822K",    "Tourists",     "blue")
    + kpi_card("⚡", "Revenue Ratio",     "4.4×",       "High vs Budget","purple")
    + '</div></div>',
    unsafe_allow_html=True)

st.markdown(f'<div style="height:1px;background:{C["border"]};margin:20px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# SEGMENT PROFILE CARDS
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:24px 40px 0;">{sec_head("SEGMENT PROFILES", t["segment_overview"])}</div>',
            unsafe_allow_html=True)

st.markdown('<div style="padding:0 40px;">', unsafe_allow_html=True)
seg_cols = st.columns(3)
for col, (key, seg) in zip(seg_cols, segments.items()):
    with col:
        rev_pct = seg["revenue_index"]
        st.markdown(
            f'<div class="ds-card" style="background:{C["card_bg"]};border:1px solid {C["border"]};'
            f'border-top:3px solid {seg["color"]};border-radius:16px;padding:20px 18px;">'
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;">'
            f'<span style="font-size:1.8rem;">{seg["emoji"]}</span>'
            f'<span style="font-size:1.05rem;font-weight:800;color:{seg["color"]};">{seg["name"]}</span>'
            f'</div>'
            f'<div style="margin-bottom:10px;">'
            f'<div style="font-size:.7rem;color:{C["grey"]};margin-bottom:4px;">Revenue Index</div>'
            f'<div style="background:{C["sec_bg"]};height:8px;border-radius:4px;">'
            f'<div style="width:{rev_pct}%;background:{seg["color"]};height:8px;border-radius:4px;"></div>'
            f'</div>'
            f'<div style="font-size:.72rem;color:{seg["color"]};font-weight:700;">{rev_pct}/100</div>'
            f'</div>'
            f'<div class="seg-row"><span style="font-size:.75rem;color:{C["grey"]};">{t["tourists"]}</span>'
            f'<span style="font-size:.8rem;font-weight:700;font-family:IBM Plex Mono,monospace;color:{seg["color"]};">{seg["tourists"]:,}K</span></div>'
            f'<div class="seg-row"><span style="font-size:.75rem;color:{C["grey"]};">{t["avg_trip"]}</span>'
            f'<span style="font-size:.8rem;font-weight:700;font-family:IBM Plex Mono,monospace;">SAR {seg["avg_trip"]:,}</span></div>'
            f'<div class="seg-row"><span style="font-size:.75rem;color:{C["grey"]};">{t["avg_night"]}</span>'
            f'<span style="font-size:.8rem;font-weight:700;font-family:IBM Plex Mono,monospace;">SAR {seg["avg_night"]:,}</span></div>'
            f'<div class="seg-row"><span style="font-size:.75rem;color:{C["grey"]};">{t["avg_los"]}</span>'
            f'<span style="font-size:.8rem;font-weight:700;font-family:IBM Plex Mono,monospace;">{seg["avg_los"]} {t["nights"]}</span></div>'
            f'<div class="seg-row"><span style="font-size:.75rem;color:{C["grey"]};">{t["type"]}</span>'
            f'<span style="font-size:.8rem;font-weight:700;font-family:IBM Plex Mono,monospace;">{seg["type"]}</span></div>'
            f'<div class="seg-row"><span style="font-size:.75rem;color:{C["grey"]};">{t["years"]}</span>'
            f'<span style="font-size:.8rem;font-weight:700;font-family:IBM Plex Mono,monospace;">{seg["years"]}</span></div>'
            f'</div>',
            unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# CHARTS: Scatter + Radar
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:24px 40px 0;">{sec_head("CLUSTER MAP", t["scatter_title"])}</div>',
            unsafe_allow_html=True)

st.markdown('<div style="padding:0 40px;">', unsafe_allow_html=True)
scatter_col, radar_col = st.columns([3, 2], gap="large")

with scatter_col:
    fig_scatter = go.Figure()
    seg_colors_map = {"high": accent_gold, "mid": accent_blue, "budget": accent_teal}
    seg_names_map  = {"high": t["seg_high"], "mid": t["seg_mid"], "budget": t["seg_budget"]}
    for key, points in scatter_data.items():
        fig_scatter.add_trace(go.Scatter(
            x=[p[0] for p in points], y=[p[1] for p in points],
            mode='markers', name=seg_names_map[key],
            marker=dict(color=seg_colors_map[key], size=10, opacity=0.75,
                        line=dict(color=bg_card, width=1.5)),
            hovertemplate=f"<b>{seg_names_map[key]}</b><br>LOS: %{{x:.1f}} nights<br>Spend: SAR %{{y:,.0f}}<extra></extra>"
        ))
    centroids = [
        (17.1, 5512, accent_gold, t["seg_high"]),
        (9.2,  4791, accent_blue, t["seg_mid"]),
        (5.4,  1242, accent_teal, t["seg_budget"]),
    ]
    for cx, cy, cc, cn in centroids:
        fig_scatter.add_trace(go.Scatter(
            x=[cx], y=[cy], mode='markers',
            marker=dict(color=cc, size=18, symbol='star',
                        line=dict(color=bg_card, width=2)),
            showlegend=False,
            hovertemplate=f"<b>{cn} Centroid</b><br>LOS: {cx} nights<br>Spend: SAR {cy:,}<extra></extra>"
        ))
    apply_layout(fig_scatter, height=360)
    fig_scatter.update_layout(
        xaxis=dict(title=f"{t['avg_los']} (Nights)", showgrid=True,
                   gridcolor="rgba(42,50,53,0.4)", tickfont=dict(size=10)),
        yaxis=dict(title=f"{t['avg_trip']} (SAR)", showgrid=True,
                   gridcolor="rgba(42,50,53,0.4)", tickfont=dict(size=10),
                   tickprefix="SAR "),
    )
    chart(fig_scatter)

with radar_col:
    st.markdown(sec_head("RADAR", t["radar_title"]), unsafe_allow_html=True)
    categories  = ["Volume","Spend/Trip","Spend/Night","LOS","Revenue Index"]
    high_vals   = [100*24514/57822, 100,  100,  100,  100]
    mid_vals    = [100*13232/57822,  87,   84, 100*9.2/17.1, 87]
    budget_vals = [100,              23,   43, 100*5.4/17.1, 23]

    fig_radar = go.Figure()
    for name, vals, color in [
        (t["seg_high"],   high_vals,   accent_gold),
        (t["seg_mid"],    mid_vals,    accent_blue),
        (t["seg_budget"], budget_vals, accent_teal),
    ]:
        fig_radar.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=categories + [categories[0]],
            fill='toself', name=name,
            line_color=color, fillcolor=f"{color}25"
        ))
    fig_radar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=C["grey"], family=ff),
        height=360, margin=dict(l=30,r=30,t=20,b=10),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(showticklabels=False, gridcolor="rgba(42,50,53,0.5)"),
            angularaxis=dict(tickfont=dict(size=10, color=C["grey"]),
                             gridcolor="rgba(42,50,53,0.5)")),
        legend=dict(orientation="h", y=-0.1, font=dict(size=10), bgcolor="rgba(0,0,0,0)"))
    chart(fig_radar)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# CHARTS: Size Pie + Timeline
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:24px 40px 0;">', unsafe_allow_html=True)
size_col, timeline_col = st.columns([1, 2], gap="large")

with size_col:
    st.markdown(sec_head("SIZE", t["size_title"]), unsafe_allow_html=True)
    fig_size = go.Figure(go.Pie(
        labels=[t["seg_high"], t["seg_mid"], t["seg_budget"]],
        values=[24514, 13232, 57822],
        hole=0.55,
        marker=dict(colors=[accent_gold, accent_blue, accent_teal],
                    line=dict(color=bg_main, width=2)),
        textfont=dict(size=10),
        hovertemplate="<b>%{label}</b><br>%{value:,}K tourists<br>%{percent}<extra></extra>"
    ))
    fig_size.add_annotation(text="<b>95.6M</b><br>Total", x=0.5, y=0.5,
        showarrow=False, font=dict(size=12, color=C["white"]))
    apply_layout(fig_size, height=280)
    fig_size.update_layout(showlegend=True,
        legend=dict(orientation="v", font=dict(size=10)))
    chart(fig_size)

with timeline_col:
    st.markdown(sec_head("EVOLUTION", t["timeline_title"]), unsafe_allow_html=True)
    inbound_total  = [17990,18040,16110,15330,17530,4140,3480,16640,27180,29730]
    domestic_total = [46450,45040,43820,43260,47810,42110,63830,77840,81920,86160]

    fig_tl = go.Figure()
    fig_tl.add_trace(go.Bar(
        x=timeline_years,
        y=[v * (1 if m else 0) for v, m in zip(inbound_total, mid_count)],
        name=t["seg_mid"], marker_color=accent_blue, opacity=0.85))
    fig_tl.add_trace(go.Bar(
        x=timeline_years,
        y=[v * h for v, h in zip(inbound_total, high_count)],
        name=t["seg_high"], marker_color=accent_gold, opacity=0.88))
    fig_tl.add_trace(go.Bar(
        x=timeline_years, y=domestic_total,
        name=t["seg_budget"], marker_color=accent_teal, opacity=0.85))
    fig_tl.add_annotation(
        x=2022, y=17000,
        text="Transition:\nMid → High Value",
        showarrow=True, arrowhead=2,
        font=dict(size=9, color=accent_gold),
        arrowcolor=accent_gold, ay=-50)
    apply_layout(fig_tl, height=280)
    fig_tl.update_layout(
        barmode='stack',
        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor="rgba(42,50,53,0.4)",
                   tickfont=dict(size=10), title="K Tourists"),
    )
    chart(fig_tl)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# Silhouette + Strategy
# ════════════════════════════════════════════════════════════════════
st.markdown(f'<div style="padding:24px 40px 0;">', unsafe_allow_html=True)
sil_col, strategy_col = st.columns([1, 2], gap="large")

with sil_col:
    st.markdown(sec_head("MODEL", t["k_choice"]), unsafe_allow_html=True)
    sil_colors = [C["gold"] if k == 3 else C["teal"] for k in k_values]
    fig_sil = go.Figure(go.Bar(
        x=[f"k={k}" for k in k_values], y=silhouettes,
        marker_color=sil_colors, opacity=0.88,
        text=[f"{s:.3f}" for s in silhouettes],
        textposition='outside', textfont=dict(size=11, color=C["white"])
    ))
    fig_sil.add_annotation(x="k=3", y=0.630,
        text="✅ Selected", showarrow=False,
        font=dict(size=10, color=accent_gold), yshift=28)
    apply_layout(fig_sil, height=260)
    fig_sil.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, tickfont=dict(size=12)),
        yaxis=dict(showgrid=True, gridcolor="rgba(42,50,53,0.4)",
                   tickfont=dict(size=10), title="Silhouette Score", range=[0.5, 0.7]),
    )
    chart(fig_sil)

with strategy_col:
    st.markdown(sec_head("STRATEGY", t["strategy_title"]), unsafe_allow_html=True)
    strat_cols = st.columns(3)
    strategies = [
        (t["seg_high"],   "💎", "gold",   t["strategy_high"],   "SAR 5,512/trip", "+85% Revenue"),
        (t["seg_mid"],    "🌟", "blue",   t["strategy_mid"],    "SAR 4,791/trip", "+48% Revenue"),
        (t["seg_budget"], "🏠", "teal",   t["strategy_budget"], "SAR 1,242/trip", "Volume Play"),
    ]
    for col, (name, emoji, ck, strategy, spend, tag) in zip(strat_cols, strategies):
        with col:
            st.markdown(
                f'<div class="ds-card" style="background:{C["card_bg"]};border:1px solid {C["border"]};'
                f'border-top:3px solid {clr(ck)};border-radius:14px;padding:18px;">'
                f'<div style="font-size:2rem;margin-bottom:8px;">{emoji}</div>'
                f'<div style="font-size:.95rem;font-weight:800;color:{clr(ck)};margin-bottom:8px;">{name}</div>'
                f'<div style="display:flex;gap:6px;margin-bottom:10px;flex-wrap:wrap;">'
                f'<span style="background:{clr(ck)}22;border:1px solid {clr(ck)}44;border-radius:12px;'
                f'padding:3px 8px;font-size:.7rem;color:{clr(ck)};font-weight:700;">{spend}</span>'
                f'<span style="background:{C["sec_bg"]};border:1px solid {C["border"]};border-radius:12px;'
                f'padding:3px 8px;font-size:.7rem;color:{C["grey"]};font-weight:600;">{tag}</span>'
                f'</div>'
                f'<div style="font-size:.8rem;color:{C["grey"]};line-height:1.5;">{strategy}</div>'
                f'</div>',
                unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown(f'<div style="height:1px;background:{C["border"]};margin:8px 40px 0;"></div>',
            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# KEY INSIGHTS
# ════════════════════════════════════════════════════════════════════
insights = [
    ("💎", t["i1"], "gold"),
    ("🏠", t["i2"], "teal"),
    ("🔄", t["i3"], "blue"),
    ("💰", t["i4"], "purple"),
]
ins_html = f'<div style="padding:24px 40px 40px;">{sec_head("INSIGHTS", t["insight_title"])}'
ins_html += f'<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;">'
for ico, txt, ck in insights:
    ins_html += (
        f'<div style="background:{C["card_bg"]};border:1px solid {C["border"]};'
        f'border-left:3px solid {clr(ck)};border-radius:12px;'
        f'padding:14px 16px;display:flex;align-items:flex-start;gap:10px;">'
        f'<div style="font-size:1.2rem;flex-shrink:0;margin-top:2px;">{ico}</div>'
        f'<div style="font-size:.83rem;color:{C["white"]};line-height:1.65;">{txt}</div>'
        f'</div>')
ins_html += '</div></div>'
st.markdown(ins_html, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════
st.markdown(
    f'<div style="background:{C["navbar"]};border-top:2px solid {C["teal"]};'
    f'padding:22px 40px;display:flex;justify-content:space-between;'
    f'align-items:center;flex-wrap:wrap;gap:12px;">'
    f'<div style="display:flex;align-items:center;gap:14px;">{logo_img}'
    f'<div>'
    f'<div style="font-size:.88rem;font-weight:700;color:{C["teal"]};">Saudi Tourism Intelligence</div>'
    f'<div style="font-size:.66rem;color:#B5B8B7;margin-top:2px;">🎯 Segmentation · Eng. Goda Emad</div>'
    f'</div></div>'
    f'<div style="display:flex;gap:20px;">'
    f'<a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" target="_blank" '
    f'style="font-size:.75rem;color:#B5B8B7;text-decoration:none;">🐙 GitHub</a>'
    f'<a href="https://datasaudi.sa" target="_blank" '
    f'style="font-size:.75rem;color:{C["teal"]};text-decoration:none;font-weight:600;">📊 DataSaudi</a>'
    f'</div></div>',
    unsafe_allow_html=True)
