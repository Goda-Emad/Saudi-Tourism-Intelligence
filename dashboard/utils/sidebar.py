# ═══════════════════════════════════════════════════════════════════
#  utils/sidebar.py — Shared Sidebar for ALL pages
#  Author : Eng. Goda Emad
# ═══════════════════════════════════════════════════════════════════
import streamlit as st
import base64, os

def render_sidebar():
    """Call this at the top of every page to get the shared sidebar."""

    if "theme" not in st.session_state: st.session_state.theme = "dark"
    if "lang"  not in st.session_state: st.session_state.lang  = "EN"

    THEME = st.session_state.theme
    LANG  = st.session_state.lang

    TEAL   = "#17B19B"
    GOLD   = "#C9A84C"
    NAV_BG = "#031414" if THEME == "dark" else "#172025"
    WHITE  = "#F4F9F8" if THEME == "dark" else "#0D1A1E"
    GREY   = "#A1A6B7" if THEME == "dark" else "#374151"
    BORDER = "#2A3235" if THEME == "dark" else "#C8D8D5"
    FF     = "Tajawal" if LANG  == "AR"   else "IBM Plex Sans"

    def _logo():
        try:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            for p in ["assets/logo.jpg", "assets/logo.png"]:
                fp = os.path.join(base, p)
                if os.path.exists(fp):
                    with open(fp, "rb") as f:
                        d = base64.b64encode(f.read()).decode()
                    ext = "png" if p.endswith("png") else "jpeg"
                    return f"data:image/{ext};base64,{d}"
        except: pass
        return ""

    logo_src = _logo()
    logo_img = (f'<img src="{logo_src}" style="height:42px;border-radius:8px;"/>'
                if logo_src else '<span style="font-size:2rem;">🇸🇦</span>')

    NAV = [
        ("🏠  Overview",        "🏠  النظرة التنفيذية", "pages/Overview.py"),
        ("📈  Tourist Trends",   "📈  اتجاهات السياحة",  "pages/Tourist_Trends.py"),
        ("📅  Seasonality",      "📅  الموسمية",         "pages/Seasonality.py"),
        ("💰  Spending",         "💰  الإنفاق",          "pages/Spending.py"),
        ("🏨  Overnight Stays",  "🏨  ليالي الإقامة",    "pages/Overnight_Stays.py"),
        ("🔮  Forecasting",      "🔮  التوقعات",         "pages/Forecasting.py"),
        ("🎯  Segmentation",     "🎯  التقسيم",          "pages/Segmentation.py"),
        ("🌱  Carbon Impact",    "🌱  الأثر الكربوني",   "pages/Carbon_Impact.py"),
    ]

    st.markdown(
        "<style>"
        f"@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=Tajawal:wght@400;700;800&display=swap');"
        f"[data-testid='stSidebar']{{background:{NAV_BG}!important;border-right:1px solid {BORDER}!important;}}"
        f"[data-testid='stSidebarNav']{{display:none!important;}}"
        f"[data-testid='stSidebar'] div,[data-testid='stSidebar'] span,"
        f"[data-testid='stSidebar'] p,[data-testid='stSidebar'] label{{color:{WHITE}!important;font-family:'{FF}',sans-serif!important;}}"
        "[data-testid='stSidebar'] .stButton>button{"
        f"background:transparent!important;border:1px solid transparent!important;"
        f"color:{GREY}!important;border-radius:8px!important;"
        "width:100%!important;font-size:.84rem!important;font-weight:500!important;"
        "padding:9px 12px!important;margin-bottom:2px!important;transition:all .18s!important;}"
        "[data-testid='stSidebar'] .stButton>button:hover{"
        f"background:{TEAL}22!important;color:{TEAL}!important;border-color:{TEAL}44!important;}}"
        "[data-testid='stSidebar'] div:nth-child(3) .stButton>button,"
        "[data-testid='stSidebar'] div:nth-child(4) .stButton>button{"
        "background:#2A3235!important;border:1px solid #3A4C50!important;"
        "color:#F4F9F8!important;font-weight:600!important;margin-bottom:5px!important;}"
        "[data-testid='stSidebar'] div:nth-child(3) .stButton>button:hover,"
        "[data-testid='stSidebar'] div:nth-child(4) .stButton>button:hover{"
        f"border-color:{GOLD}!important;color:{GOLD}!important;}}"
        "</style>",
        unsafe_allow_html=True)

    with st.sidebar:
        # Brand
        name = "Saudi Tourism Intelligence" if LANG == "EN" else "ذكاء السياحة السعودية"
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;padding:16px 4px 14px;">'
            f'{logo_img}'
            f'<div>'
            f'<div style="font-size:.88rem;font-weight:700;color:{WHITE};">{name}</div>'
            f'<div style="font-size:.58rem;color:{TEAL};font-weight:600;'
            f'letter-spacing:1.2px;text-transform:uppercase;">AI ANALYTICS PLATFORM</div>'
            f'</div></div>',
            unsafe_allow_html=True)

        st.markdown(f'<div style="height:1px;background:{BORDER};margin-bottom:10px;"></div>',
                    unsafe_allow_html=True)

        # Theme toggle
        thm_lbl = ("☀️  Light" if THEME == "dark" else "🌙  Dark")
        if st.button(thm_lbl, key="sb_thm", use_container_width=True):
            st.session_state.theme = "light" if THEME == "dark" else "dark"
            st.rerun()

        # Language toggle
        lng_lbl = ("🌐  العربية" if LANG == "EN" else "🌐  English")
        if st.button(lng_lbl, key="sb_lng", use_container_width=True):
            st.session_state.lang = "AR" if LANG == "EN" else "EN"
            st.rerun()

        st.markdown(f'<div style="height:1px;background:{BORDER};margin:10px 0 4px;"></div>',
                    unsafe_allow_html=True)

        # ✅ Home button — teal colored, returns to app.py from any page
        home_lbl = "🏡  الرئيسية" if LANG == "AR" else "🏡  Home"
        st.markdown(
            f'<style>.home-wrap .stButton>button{{'
            f'background:{TEAL}20!important;border:1px solid {TEAL}66!important;'
            f'color:{TEAL}!important;font-weight:700!important;margin-bottom:6px!important;}}'
            f'.home-wrap .stButton>button:hover{{'
            f'background:{TEAL}40!important;border-color:{TEAL}!important;}}'
            f'</style>',
            unsafe_allow_html=True)
        st.markdown('<div class="home-wrap">', unsafe_allow_html=True)
        if st.button(home_lbl, key="sb_nav_home", use_container_width=True):
            st.switch_page("app.py")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f'<div style="height:1px;background:{BORDER};margin:4px 0 6px;"></div>',
                    unsafe_allow_html=True)

        # Page navigation
        for en_lbl, ar_lbl, fpath in NAV:
            label = ar_lbl if LANG == "AR" else en_lbl
            key = "sb_nav_" + os.path.basename(fpath)
            if st.button(label, key=key, use_container_width=True):
                st.switch_page(fpath)

        st.markdown(f'<div style="height:1px;background:{BORDER};margin:10px 0 8px;"></div>',
                    unsafe_allow_html=True)

        # Footer
        st.markdown(
            f'<div style="font-size:.67rem;color:{GREY};padding:0 2px;line-height:1.9;">'
            f'📦 DataSaudi · 2015–2024<br>'
            f'🐙 <a href="https://github.com/Goda-Emad/Saudi-Tourism-Intelligence" '
            f'target="_blank" style="color:{TEAL};text-decoration:none;">GitHub</a>'
            f'  ·  '
            f'💼 <a href="https://www.linkedin.com/in/goda-emad/" '
            f'target="_blank" style="color:{TEAL};text-decoration:none;">LinkedIn</a>'
            f'</div>',
            unsafe_allow_html=True)

    return st.session_state.theme, st.session_state.lang
