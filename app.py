"""
Navigr - Aksjeinformasjon for Oslo Børs
MVP med ankerflåte-konsept og ordbok.

Brukerne starter med 10 selskaper som ankerflåte. De kan kaste anker
(legge til) og ta opp anker (fjerne) som de vil. Ordboken forklarer
nøkkeltall og finansbegreper på vanlig norsk.
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

from config import COMPANIES, INITIAL_FLEET, MACRO_FACTORS, COMPANY_FACTORS, COMPETITORS
from ai_engine import get_market_briefing, get_company_briefing, get_did_you_know, ask_ai, explain_move, get_company_deepdive
from glossary import GLOSSARY, LEVEL_LABELS, LEVEL_COLORS, search_terms, get_term

SECTOR_COLORS = {
    "Energi":          {"bg": "#FEF3C7", "text": "#92400E", "border": "#F59E0B"},
    "Finans":          {"bg": "#DBEAFE", "text": "#1E40AF", "border": "#3B82F6"},
    "Industri":        {"bg": "#F1F5F9", "text": "#334155", "border": "#94A3B8"},
    "Sjømat":          {"bg": "#CCFBF1", "text": "#0F766E", "border": "#14B8A6"},
    "Telekom":         {"bg": "#EDE9FE", "text": "#5B21B6", "border": "#8B5CF6"},
    "Fornybar energi": {"bg": "#DCFCE7", "text": "#166534", "border": "#22C55E"},
}


# ============================================================
# SIDEOPPSETT
# ============================================================

st.set_page_config(
    page_title="Navigr",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
/* Importer Fraunces og Inter for bedre typografi */
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* Huvudbakgrund — varm kräm */
.main { background-color: #FAF6F0; }
.stApp { background-color: #FAF6F0; }

/* Sidebar — annorlunda ljus ton */
section[data-testid="stSidebar"] {
    background-color: #FFFBF3;
    border-right: 1px solid #E8DFC8;
}

/* Rubriker — Fraunces serif */
h1, h2, h3 {
    font-family: 'Fraunces', Georgia, serif !important;
    color: #2C2A26 !important;
    letter-spacing: -0.02em;
}

h1 { font-weight: 500; }
h2 { font-weight: 500; }
h3 { font-weight: 500; }

/* Brödtext — Inter */
body, p, div, span, label {
    font-family: 'Inter', system-ui, sans-serif;
    color: #2C2A26;
}

/* Knappar — terra-grön primär */
.stButton button {
    background-color: #FFFBF3;
    color: #2C2A26;
    border: 1px solid #E8DFC8;
    border-radius: 8px;
    padding: 8px 16px;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    transition: all 0.15s;
}
.stButton button:hover {
    background-color: #F2ECE0;
    border-color: #6B7E5C;
    color: #2C2A26;
}

/* Primary button — terra-grön fylld */
.stButton button[kind="primary"] {
    background-color: #6B7E5C;
    color: #FFFBF3;
    border: 1px solid #6B7E5C;
}
.stButton button[kind="primary"]:hover {
    background-color: #4F6244;
    border-color: #4F6244;
    color: #FFFBF3;
}

/* Flikar — bättre styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    border-bottom: 1px solid #E8DFC8;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: #7A746A;
    border: none;
    padding: 12px 20px;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #2C2A26;
    border-bottom: 2px solid #6B7E5C;
}

/* Anpassade kortstilar */
.navigr-card {
    background: #FFFBF3;
    border: 1px solid #E8DFC8;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
}

.navigr-aiai-card {
    background: linear-gradient(135deg, #F0EEFD 0%, #E6E3FB 100%);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 20px;
    position: relative;
}
.navigr-aiai-badge {
    display: inline-block;
    background: #7F77DD;
    color: white;
    padding: 6px 12px;
    border-radius: 10px;
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 13px;
    margin-bottom: 12px;
}
.navigr-aiai-title {
    font-family: 'Fraunces', serif;
    font-size: 19px;
    font-weight: 500;
    color: #26215C;
    margin-bottom: 12px;
}
.navigr-aiai-body {
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    line-height: 1.65;
    color: #26215C;
}

/* Holding-rad */
.holding-row {
    display: grid;
    grid-template-columns: 40px 2fr 1fr 100px 100px 200px;
    gap: 14px;
    padding: 14px 16px;
    align-items: center;
    border-bottom: 1px solid #E8DFC8;
    transition: background 0.15s;
}
.holding-row:hover { background-color: #F2ECE0; }
.anchor-icon {
    width: 32px; height: 32px;
    border-radius: 50%;
    background: #6B7E5C;
    color: #FFFBF3;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
}
.anchor-icon.empty {
    background: #DDE5D2;
    color: #6B7E5C;
}

/* Bolagsnamn typografi */
.tick-name {
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: 16px;
    color: #2C2A26;
}
.tick-sub {
    font-size: 12px;
    color: #7A746A;
    margin-top: 2px;
}

/* Kurs-text med monospace */
.price-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    font-variant-numeric: tabular-nums;
}

/* Pill för förändring */
.pill {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 100px;
    font-size: 12px;
    font-weight: 500;
    font-family: 'JetBrains Mono', monospace;
}
.pill.up { background: #DCEBDD; color: #2F6B3E; }
.pill.down { background: #F0DBDB; color: #8A1F1F; }
.pill.neutral { background: #F2EBD9; color: #6B5B2C; }

/* Term-kort */
.term-card {
    background: #FFFBF3;
    border: 1px solid #E8DFC8;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 12px;
    transition: all 0.2s;
}
.term-card:hover {
    border-color: #6B7E5C;
    box-shadow: 0 4px 12px rgba(44, 42, 38, 0.06);
}
.term-name {
    font-family: 'Fraunces', serif;
    font-size: 20px;
    font-weight: 500;
    color: #2C2A26;
    margin-bottom: 6px;
}
.term-tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 100px;
    font-size: 10px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 8px;
}
.term-tag.basic { background: #DDE5D2; color: #4F6244; }
.term-tag.med { background: #F5E8D0; color: #6B5B2C; }
.term-tag.adv { background: #F4E5E2; color: #C4847C; }
.term-tag.idiom { background: #E8E5F4; color: #5A4A8C; }
.term-short {
    font-size: 14px;
    line-height: 1.55;
    color: #4A4640;
    margin-bottom: 8px;
}
.term-example {
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-size: 13px;
    color: #7A746A;
    border-top: 1px dashed #E8DFC8;
    padding-top: 10px;
    margin-top: 8px;
}

/* Detaljerad term-visning */
.term-detail-title {
    font-family: 'Fraunces', serif;
    font-size: 32px;
    font-weight: 500;
    color: #2C2A26;
    letter-spacing: -0.02em;
    margin-bottom: 8px;
}
.term-detail-pron {
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-size: 13px;
    color: #7A746A;
    margin-bottom: 10px;
}
.term-detail-section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #7A746A;
    margin-bottom: 8px;
}
.term-detail-body {
    font-size: 15px;
    line-height: 1.65;
    color: #4A4640;
    margin-bottom: 18px;
}
.term-detail-example-box {
    background: #F2ECE0;
    border-left: 3px solid #6B7E5C;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-size: 14px;
    color: #4A4640;
    margin-bottom: 18px;
}
.term-detail-tip-box {
    background: #F5E8D0;
    border-radius: 12px;
    padding: 14px 18px;
    font-size: 13.5px;
    color: #6B5B2C;
    margin-bottom: 18px;
}

/* Dölj Streamlit-standardelement som stör */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Bolag-knapp på rad */
.row-button {
    background: #FFFBF3 !important;
    border: 1px solid #E8DFC8 !important;
    color: #4A4640 !important;
    border-radius: 6px !important;
    padding: 6px 12px !important;
    font-size: 12px !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "fleet" not in st.session_state:
    st.session_state.fleet = list(INITIAL_FLEET)

if "current_page" not in st.session_state:
    st.session_state.current_page = "Hem"

if "current_company" not in st.session_state:
    st.session_state.current_company = None

if "selected_term" not in st.session_state:
    st.session_state.selected_term = None

if "glossary_query" not in st.session_state:
    st.session_state.glossary_query = ""

if "glossary_level" not in st.session_state:
    st.session_state.glossary_level = "all"


# ============================================================
# HJELPEFUNKSJONER
# ============================================================

@st.cache_data(ttl=300)
def get_price_data(ticker, period="3mo"):
    """Henter kursdata fra Yahoo Finance med 5 min cache."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        if hist.empty:
            return None, None, None
        current = hist["Close"].iloc[-1]
        prev = hist["Close"].iloc[-2] if len(hist) > 1 else current
        change = current - prev
        pct = (change / prev * 100) if prev else 0
        return current, change, pct
    except Exception:
        return None, None, None


@st.cache_data(ttl=300)
def get_price_history(ticker, period="3mo"):
    """Henter prishistorikk for graf."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        return hist if not hist.empty else None
    except Exception:
        return None


@st.cache_data(ttl=3600)
def get_fundamentals(yahoo_ticker):
    """Henter nøkkeltall fra Yahoo Finance (cache 1 time)."""
    try:
        return yf.Ticker(yahoo_ticker).info or {}
    except Exception:
        return {}


@st.cache_data(ttl=3600)
def get_insider_transactions(yahoo_ticker):
    try:
        df = yf.Ticker(yahoo_ticker).insider_transactions
        return df if df is not None and not df.empty else None
    except Exception:
        return None


@st.cache_data(ttl=3600)
def get_dividends_history(yahoo_ticker):
    try:
        divs = yf.Ticker(yahoo_ticker).dividends
        return divs if divs is not None and not divs.empty else None
    except Exception:
        return None


@st.cache_data(ttl=3600)
def get_earnings_dates_data(yahoo_ticker):
    try:
        df = yf.Ticker(yahoo_ticker).earnings_dates
        return df if df is not None and not df.empty else None
    except Exception:
        return None


@st.cache_data(ttl=1800)
def get_news(yahoo_ticker):
    try:
        news = yf.Ticker(yahoo_ticker).news
        return news if news else []
    except Exception:
        return []


@st.cache_data(ttl=3600)
def get_recommendations(yahoo_ticker):
    try:
        df = yf.Ticker(yahoo_ticker).recommendations
        return df if df is not None and not df.empty else None
    except Exception:
        return None


def _fmt_mrd(val, currency=""):
    if val is None:
        return "—"
    mrd = val / 1_000_000_000
    s = f"{mrd:,.1f}".replace(",", " ").replace(".", ",")
    return f"{s} mrd {currency}".strip()


def _fmt_x(val):
    if val is None or val != val:
        return "—"
    return f"{val:.1f}x".replace(".", ",")


def _fmt_pct(val):
    if val is None or val != val:
        return "—"
    return f"{val * 100:.1f} %".replace(".", ",")


def _fmt_ratio(val):
    if val is None or val != val:
        return "—"
    return f"{val:.2f}".replace(".", ",")


def greeting() -> str:
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "God morgon, Maria 👋"
    if 12 <= hour < 18:
        return "God eftermiddag, Maria 👋"
    if 18 <= hour < 23:
        return "God kväll, Maria 👋"
    return "Hej, Maria 👋"


def render_avatar(ticker: str) -> str:
    co = COMPANIES[ticker]
    sc = SECTOR_COLORS.get(co.get("sector", ""), {"bg": "#E8DFC8", "text": "#4A4640", "border": "#C8B896"})
    initials = co.get("logo", ticker[:2])
    return (
        f"<div style='width:36px;height:36px;border-radius:50%;"
        f"background:{sc['bg']};border:1.5px solid {sc['border']};"
        f"color:{sc['text']};display:flex;align-items:center;justify-content:center;"
        f"font-family:Fraunces,serif;font-weight:500;font-size:12px;"
        f"letter-spacing:-0.02em;flex-shrink:0;'>{initials}</div>"
    )


def render_sector_badge(sector: str) -> str:
    sc = SECTOR_COLORS.get(sector, {"bg": "#E8DFC8", "text": "#4A4640", "border": "#C8B896"})
    return (
        f"<span style='display:inline-block;background:{sc['bg']};color:{sc['text']};"
        f"border:1px solid {sc['border']};padding:2px 9px;border-radius:100px;"
        f"font-size:11px;font-weight:500;white-space:nowrap;'>{sector}</span>"
    )


def drop_anchor(ticker):
    if ticker not in st.session_state.fleet:
        st.session_state.fleet.append(ticker)


def raise_anchor(ticker):
    if ticker in st.session_state.fleet:
        st.session_state.fleet.remove(ticker)


def navigate_to(page, company=None):
    st.session_state.current_page = page
    if company:
        st.session_state.current_company = company


def format_price(price):
    if price is None:
        return "—"
    return f"{price:,.2f}".replace(",", " ").replace(".", ",")


def format_pct(pct):
    if pct is None:
        return "—"
    sign = "+" if pct > 0 else ""
    return f"{sign}{pct:.2f} %"


def pill_class(pct):
    if pct is None:
        return "neutral"
    return "up" if pct > 0 else "down" if pct < 0 else "neutral"


# ============================================================
# SIDEMENY
# ============================================================

with st.sidebar:
    # Logotyp och varumärke
    st.markdown("""
    <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 4px;'>
        <div style='font-size: 28px;'>⚓</div>
        <div style='font-family: Fraunces, serif; font-size: 28px; font-weight: 500; letter-spacing: -0.04em; color: #2C2A26;'>Navigr</div>
    </div>
    <div style='font-family: Fraunces, serif; font-style: italic; font-size: 13px; color: #7A746A; margin-bottom: 24px;'>Förstå aktier. Navigera själv.</div>
    """, unsafe_allow_html=True)

    _page = st.session_state.current_page
    if st.button("🏠  Hem", use_container_width=True, key="nav_home",
                 type="primary" if _page == "Hem" else "secondary"):
        navigate_to("Hem")
        st.rerun()

    if st.button("⚓  Min Ankrarflottan", use_container_width=True, key="nav_fleet",
                 type="primary" if _page == "Ankrarflottan" else "secondary"):
        navigate_to("Ankrarflottan")
        st.rerun()

    if st.button("🔍  Utforska", use_container_width=True, key="nav_discover",
                 type="primary" if _page == "Utforska" else "secondary"):
        navigate_to("Utforska")
        st.rerun()

    if st.button("📖  Ordbok", use_container_width=True, key="nav_glossary",
                 type="primary" if _page == "Ordbok" else "secondary"):
        navigate_to("Ordbok")
        st.session_state.selected_term = None
        st.rerun()

    st.markdown("<hr style='border-color: #E8DFC8; margin: 24px 0;'>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='font-family: JetBrains Mono, monospace; font-size: 11px; color: #7A746A; text-transform: uppercase; letter-spacing: 0.06em;'>
        Ankrarflottan
    </div>
    <div style='font-family: Fraunces, serif; font-size: 32px; font-weight: 500; color: #2C2A26; margin-top: 4px;'>
        {len(st.session_state.fleet)} <span style='font-size: 14px; color: #7A746A;'>bolag</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: #E8DFC8; margin: 24px 0;'>", unsafe_allow_html=True)

    st.caption("⚠️ Allmän investeringsanalys — inte personlig rådgivning. Historisk avkastning är ingen garanti för framtida utveckling.")


# ============================================================
# AI AI KORT
# ============================================================

def render_aiai_card(title: str, body: str):
    """Renderer Ai ai-kort med korrekt styling."""
    html = f"""
    <div class='navigr-aiai-card'>
        <div class='navigr-aiai-badge'>Ai</div>
        <div class='navigr-aiai-title'>{title}</div>
        <div class='navigr-aiai-body'>{body}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# SIDA: HEM
# ============================================================

def render_home():
    today = datetime.now()
    months_sv = ["januari", "februari", "mars", "april", "maj", "juni",
                 "juli", "augusti", "september", "oktober", "november", "december"]
    date_str = f"{today.day}. {months_sv[today.month-1]} {today.year}"

    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown(f"# {greeting()}")
        st.markdown("<p style='font-family: Fraunces, serif; font-style: italic; color: #7A746A; font-size: 15px;'>Här är vad som rör sig i din Ankrarflottan idag</p>", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"<div style='text-align:right; color:#7A746A; font-family:JetBrains Mono, monospace; font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; padding-top:30px;'>{date_str.upper()}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Ai ai - marknadssammanfattning med riktiga kursdata
    with st.spinner("Hämtar dagens marknadssammanfattning..."):
        market_data = []
        for t in st.session_state.fleet:
            co = COMPANIES[t]
            p, _, pct_val = get_price_data(co["yahoo_ticker"])
            market_data.append({"ticker": t, "name": co["name"], "sector": co["sector"], "price": p, "pct": pct_val})
        briefing = get_market_briefing(market_data)
        render_aiai_card("Ai ai — marknaden idag", briefing)

    # Dagens stigande och fallande
    render_top_movers(market_data)

    # Visste du? - daglig fakta
    with st.spinner("Hämtar dagens fakta..."):
        fact = get_did_you_know()
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #F5E8D0 0%, #DDE5D2 100%); border-radius: 16px; padding: 22px 26px; margin-bottom: 20px;'>
        <div style='display: inline-block; background: #6B5B2C; color: #FFFBF3; padding: 4px 11px; border-radius: 100px; font-family: Fraunces, serif; font-weight: 600; font-size: 12px; margin-bottom: 12px;'>💡 Visste du?</div>
        <div style='font-family: Inter, sans-serif; font-size: 15px; line-height: 1.65; color: #4A4640;'>{fact}</div>
    </div>
    """, unsafe_allow_html=True)

    # Info om Ankrarflottan
    st.markdown("""
    <div style='background: #FFFBF3; border: 1px solid #E8DFC8; border-radius: 16px; padding: 18px 22px; margin-bottom: 20px;'>
        <span style='font-size: 20px; margin-right: 10px;'>⚓</span>
        <strong>Din Ankrarflottan</strong> består av bolag du följer. Du startade med de 10 största på Oslo Børs — du kan ta upp ankaret från de du inte vill följa, och kasta ankare på bolag du blir nyfiken på.
    </div>
    """, unsafe_allow_html=True)

    # Visa Ankrarflottan
    st.markdown(f"### Min Ankrarflottan")
    st.caption(f"{len(st.session_state.fleet)} bolag")

    if not st.session_state.fleet:
        st.warning("Du har inga bolag i din Ankrarflottan. Gå till **Utforska** för att kasta ankare på ett bolag.")
    else:
        render_fleet_table(st.session_state.fleet, allow_remove=True)


def render_top_movers(market_data):
    """Visar dagens topp 3 stigande och topp 3 fallande."""
    valid = [d for d in market_data if d.get("pct") is not None]
    if not valid:
        return
    sorted_data = sorted(valid, key=lambda x: x["pct"], reverse=True)
    winners = sorted_data[:3]
    losers = sorted(sorted_data[-3:], key=lambda x: x["pct"])

    st.markdown("### Dagens rörelser i din flotta")
    cols = st.columns(2)

    def _card(d, color_bg, color_text):
        sign = "+" if d["pct"] > 0 else ""
        return (
            f"<div style='display:flex;align-items:center;justify-content:space-between;"
            f"background:#FFFBF3;border:1px solid #E8DFC8;border-radius:10px;"
            f"padding:10px 14px;margin-bottom:6px;'>"
            f"<div><div style='font-family:Fraunces,serif;font-weight:500;font-size:14px;'>{d['ticker']}</div>"
            f"<div style='font-size:11px;color:#7A746A;'>{d['name']}</div></div>"
            f"<div style='background:{color_bg};color:{color_text};padding:4px 10px;"
            f"border-radius:100px;font-family:JetBrains Mono,monospace;font-size:12px;font-weight:500;'>"
            f"{sign}{d['pct']:.2f}%</div></div>"
        )

    with cols[0]:
        st.markdown("<div style='font-family:JetBrains Mono,monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.08em;color:#2F6B3E;margin-bottom:8px;'>📈 Stigande</div>", unsafe_allow_html=True)
        for d in winners:
            st.markdown(_card(d, "#DCEBDD", "#2F6B3E"), unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div style='font-family:JetBrains Mono,monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.08em;color:#8A1F1F;margin-bottom:8px;'>📉 Fallande</div>", unsafe_allow_html=True)
        for d in losers:
            st.markdown(_card(d, "#F0DBDB", "#8A1F1F"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


def render_fleet_table(tickers, allow_remove=True):
    """Renderer en tabell över bolag med kursdata."""
    _lbl = "<div style='font-family:JetBrains Mono,monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.08em;color:#7A746A;padding-bottom:4px;'>{}</div>"
    header_cols = st.columns([0.55, 2.2, 1.4, 1.2, 1.1, 1.6])
    with header_cols[0]: st.markdown(_lbl.format(""), unsafe_allow_html=True)
    with header_cols[1]: st.markdown(_lbl.format("Bolag"), unsafe_allow_html=True)
    with header_cols[2]: st.markdown(_lbl.format("Sektor"), unsafe_allow_html=True)
    with header_cols[3]: st.markdown(_lbl.format("Kurs"), unsafe_allow_html=True)
    with header_cols[4]: st.markdown(_lbl.format("Förändring"), unsafe_allow_html=True)
    with header_cols[5]: st.markdown(_lbl.format("&nbsp;"), unsafe_allow_html=True)

    st.markdown("<hr style='margin: 5px 0; border-color: #E8DFC8;'>", unsafe_allow_html=True)

    for ticker in tickers:
        co = COMPANIES[ticker]
        price, change, pct = get_price_data(co["yahoo_ticker"])
        cls = pill_class(pct)
        is_anchored = ticker in st.session_state.fleet

        cols = st.columns([0.55, 2.2, 1.4, 1.2, 1.1, 1.6])

        with cols[0]:
            st.markdown(render_avatar(ticker), unsafe_allow_html=True)

        with cols[1]:
            st.markdown(
                f"<div class='tick-name'>{ticker}</div>"
                f"<div class='tick-sub'>{co['name']}</div>",
                unsafe_allow_html=True,
            )

        with cols[2]:
            st.markdown(render_sector_badge(co["sector"]), unsafe_allow_html=True)

        with cols[3]:
            st.markdown(f"<div class='price-text'>{format_price(price)} kr</div>", unsafe_allow_html=True)

        with cols[4]:
            if pct is not None:
                st.markdown(f"<span class='pill {cls}'>{format_pct(pct)}</span>", unsafe_allow_html=True)
            else:
                st.markdown("—")

        with cols[5]:
            if allow_remove and is_anchored:
                sub_cols = st.columns(2)
                if sub_cols[0].button("Öppna", key=f"open_{ticker}_{st.session_state.current_page}", use_container_width=True):
                    navigate_to("Bolag", ticker)
                    st.rerun()
                if sub_cols[1].button("⚓×", key=f"raise_{ticker}_{st.session_state.current_page}", help="Ta upp ankaret", use_container_width=True):
                    raise_anchor(ticker)
                    st.toast(f"Ankaret taget upp från {ticker}", icon="⚓")
                    st.rerun()
            else:
                if st.button("⚓ Kasta ankare", key=f"drop_{ticker}_{st.session_state.current_page}", use_container_width=True, type="primary"):
                    drop_anchor(ticker)
                    st.toast(f"Ankare kastat på {ticker}", icon="⚓")
                    st.rerun()

        st.markdown("<hr style='margin: 5px 0; border-color: #E8DFC8;'>", unsafe_allow_html=True)


# ============================================================
# SIDA: ANKRARFLOTTAN
# ============================================================

def render_fleet():
    st.markdown("# ⚓ Min Ankrarflottan")
    st.markdown("<p style='font-family: Fraunces, serif; font-style: italic; color: #7A746A; font-size: 15px;'>Bolagen du följer just nu</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.fleet:
        st.warning("Du har inga bolag i din Ankrarflottan.")
        if st.button("Gå till Utforska", type="primary"):
            navigate_to("Utforska")
            st.rerun()
        return

    st.caption(f"{len(st.session_state.fleet)} bolag")
    render_fleet_table(st.session_state.fleet, allow_remove=True)


# ============================================================
# SIDA: UTFORSKA
# ============================================================

def render_discover():
    st.markdown("# 🔍 Utforska")
    st.markdown("<p style='font-family: Fraunces, serif; font-style: italic; color: #7A746A; font-size: 15px;'>Bolag du inte har kastat ankare på än</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    not_in_fleet = [t for t in COMPANIES.keys() if t not in st.session_state.fleet]

    if not not_in_fleet:
        st.success("Du följer alla tillgängliga bolag. Bra jobbat!")
        return

    render_fleet_table(not_in_fleet, allow_remove=False)


# ============================================================
# SIDA: ORDBOK
# ============================================================

def render_glossary():
    # Om en term är vald, visa detaljvy
    if st.session_state.selected_term:
        render_term_detail(st.session_state.selected_term)
        return

    # Huvudsida för ordbok
    st.markdown("""
    <div style='background: linear-gradient(135deg, #DDE5D2 0%, #F5E8D0 100%); border-radius: 24px; padding: 32px 36px; margin-bottom: 28px;'>
        <h1 style='font-family: Fraunces, serif; font-size: 32px; font-weight: 500; letter-spacing: -0.025em; color: #2C2A26; margin: 0 0 10px 0;'>
            Ordboken — <em style='color: #4F6244;'>aktie-svenska förklarat.</em>
        </h1>
        <p style='font-size: 15px; color: #4A4640; line-height: 1.6; max-width: 580px; margin: 0;'>
            Här hittar du de viktigaste orden, uttrycken och förkortningarna i aktievärlden — förklarade på ett sätt som är lätt att förstå. Inga dumma frågor, bara svar.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sök
    query = st.text_input(
        "Sök",
        value=st.session_state.glossary_query,
        placeholder="🔍  Sök efter ett ord eller uttryck...",
        label_visibility="collapsed",
        key="glossary_search_input"
    )
    st.session_state.glossary_query = query

    # Nivåfilter
    levels = [
        ("all", "Alla"),
        ("basic", "Helt enkelt"),
        ("med", "Lite mer"),
        ("adv", "För de nyfikna"),
        ("idiom", "Uttryck och slang"),
    ]
    cols = st.columns(len(levels))
    for i, (level_key, level_label) in enumerate(levels):
        with cols[i]:
            is_active = st.session_state.glossary_level == level_key
            btn_type = "primary" if is_active else "secondary"
            if st.button(level_label, key=f"filter_{level_key}", use_container_width=True, type=btn_type):
                st.session_state.glossary_level = level_key
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Resultat
    results = search_terms(query=query, level=st.session_state.glossary_level)

    if not results:
        st.markdown("""
        <div style='padding: 60px 20px; text-align: center; color: #7A746A; font-family: Fraunces, serif; font-style: italic; font-size: 16px;'>
            Vi hittade inga ord som matchade. Prova en annan sökning eller ändra filtret.
        </div>
        """, unsafe_allow_html=True)
        return

    # Visa termer i grid (2 kolumner)
    for i in range(0, len(results), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(results):
                key, term = results[i + j]
                with col:
                    render_term_card(key, term)


def render_term_card(key: str, term: dict):
    """Renderer ett term-kort som kan klickas."""
    level = term["level"]
    label = LEVEL_LABELS[level]

    # Kort med klickbar knapp som täcker hela kortet
    st.markdown(f"""
    <div class='term-card'>
        <div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;'>
            <div class='term-name'>{term['name']}</div>
            <span class='term-tag {level}'>{label}</span>
        </div>
        <div class='term-short'>{term['short']}</div>
        {f"<div class='term-example'>\"{term['example']}\"</div>" if term.get('example') else ""}
    </div>
    """, unsafe_allow_html=True)

    if st.button(f"Läs mer", key=f"term_{key}", use_container_width=True):
        st.session_state.selected_term = key
        st.rerun()


def render_term_detail(key: str):
    """Renderer detaljerad visning av en term."""
    term = get_term(key)
    if not term:
        st.error("Ordet hittades inte.")
        if st.button("← Tillbaka till ordboken"):
            st.session_state.selected_term = None
            st.rerun()
        return

    # Tillbaka-knapp
    if st.button("← Tillbaka till ordboken"):
        st.session_state.selected_term = None
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    level = term["level"]
    label = LEVEL_LABELS[level]

    # Titel och tagg
    st.markdown(f"""
    <div style='background: #FFFBF3; border: 1px solid #E8DFC8; border-radius: 16px; padding: 32px 34px; margin-bottom: 20px;'>
        <div class='term-detail-title'>{term['name']}</div>
        {f"<div class='term-detail-pron'>{term['pron']}</div>" if term.get('pron') else ""}
        <span class='term-tag {level}'>{label}</span>

        <div style='border-top: 1px solid #E8DFC8; margin: 18px 0; padding-top: 18px;'></div>

        <div class='term-detail-section-label'>Vad betyder det?</div>
        <div class='term-detail-body'>{term['def']}</div>

        {f'''<div class='term-detail-section-label'>Tänk på det så här</div>
        <div class='term-detail-example-box'>"{term['example']}"</div>''' if term.get('example') else ""}

        {f'''<div class='term-detail-tip-box'><strong>💡 Tips:</strong> {term['tip']}</div>''' if term.get('tip') else ""}
    </div>
    """, unsafe_allow_html=True)

    # Relaterade ord
    if term.get("related"):
        st.markdown("<div class='term-detail-section-label'>Besläktade ord</div>", unsafe_allow_html=True)
        related_cols = st.columns(min(len(term["related"]), 4))
        for i, rel_key in enumerate(term["related"]):
            rel_term = get_term(rel_key)
            if rel_term:
                with related_cols[i % len(related_cols)]:
                    if st.button(rel_term["name"], key=f"rel_{key}_{rel_key}"):
                        st.session_state.selected_term = rel_key
                        st.rerun()


# ============================================================
# SIDA: BOLAG
# ============================================================

def render_company():
    ticker = st.session_state.current_company
    if not ticker or ticker not in COMPANIES:
        st.error("Inget bolag valt.")
        return

    co = COMPANIES[ticker]
    is_anchored = ticker in st.session_state.fleet

    # Tillbaka-knapp
    if st.button("← Tillbaka till hem"):
        navigate_to("Hem")
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Header med namn och kurs
    price, change, pct = get_price_data(co["yahoo_ticker"])

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:14px;margin-bottom:12px;'>
            {render_avatar(ticker).replace("width:36px;height:36px", "width:52px;height:52px").replace("font-size:12px", "font-size:16px")}
            <div>
                <div style='font-family:JetBrains Mono,monospace;font-size:11px;text-transform:uppercase;letter-spacing:0.08em;color:#7A746A;margin-bottom:4px;'>
                    Ankrarflottan / {ticker} · OSLO BØRS
                </div>
                <h1 style='margin:0;'>{co['name']}</h1>
                <div style='margin-top:8px;'>{render_sector_badge(co['sector'])}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if is_anchored:
            st.markdown("<div style='display: inline-block; background: #6B7E5C; color: #FFFBF3; padding: 6px 14px; border-radius: 100px; font-size: 12px; font-weight: 500; margin-top: 12px;'>⚓ Ankare kastat</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='display: inline-block; background: #DDE5D2; color: #4F6244; padding: 6px 14px; border-radius: 100px; font-size: 12px; font-weight: 500; margin-top: 12px;'>⚓ Inte i Ankrarflottan</div>", unsafe_allow_html=True)

    with col_right:
        if price:
            cls = pill_class(pct)
            st.markdown(f"""
            <div style='text-align: right;'>
                <div style='font-family: Fraunces, serif; font-size: 32px; font-weight: 500; letter-spacing: -0.02em; color: #2C2A26;'>{format_price(price)} kr</div>
                <div style='margin-top: 6px;'><span class='pill {cls}'>{format_pct(pct)}</span></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if is_anchored:
            if st.button("⚓× Ta upp ankaret", use_container_width=True, key="toggle_anchor_company"):
                raise_anchor(ticker)
                st.toast(f"Ankaret taget upp från {ticker}", icon="⚓")
                st.rerun()
        else:
            if st.button("⚓ Kasta ankare", use_container_width=True, type="primary", key="toggle_anchor_company"):
                drop_anchor(ticker)
                st.toast(f"Ankare kastat på {ticker}", icon="⚓")
                st.rerun()

    st.markdown("<hr style='border-color: #E8DFC8; margin: 24px 0;'>", unsafe_allow_html=True)

    # 1. OM BOLAGET (FÖRE Ai ai)
    st.markdown(f"""
    <div style='background: #FFFBF3; border: 1px solid #E8DFC8; border-radius: 16px; padding: 24px 28px; margin-bottom: 20px;'>
        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 14px;'>
            <div style='width: 4px; height: 18px; background: #6B7E5C; border-radius: 2px;'></div>
            <div style='font-family: Fraunces, serif; font-size: 16px; font-weight: 500; color: #2C2A26;'>Om bolaget</div>
        </div>
        <p style='font-size: 14.5px; line-height: 1.7; color: #4A4640; margin-bottom: 18px;'>{co['about']}</p>
    </div>
    """, unsafe_allow_html=True)

    info_cols = st.columns(4)
    with info_cols[0]:
        st.markdown(f"<div style='font-family:JetBrains Mono,monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.08em;color:#7A746A;margin-bottom:6px;'>Sektor</div>{render_sector_badge(co['sector'])}", unsafe_allow_html=True)
    with info_cols[1]:
        st.markdown(f"<div style='font-family: JetBrains Mono, monospace; font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em; color: #7A746A;'>Huvudkontor</div><div style='font-family: Fraunces, serif; font-size: 16px; font-weight: 500;'>{co['hq']}</div>", unsafe_allow_html=True)
    with info_cols[2]:
        st.markdown(f"<div style='font-family: JetBrains Mono, monospace; font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em; color: #7A746A;'>Grundat</div><div style='font-family: Fraunces, serif; font-size: 16px; font-weight: 500;'>{co['founded']}</div>", unsafe_allow_html=True)
    with info_cols[3]:
        st.markdown(f"<div style='font-family: JetBrains Mono, monospace; font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em; color: #7A746A;'>Anställda</div><div style='font-family: Fraunces, serif; font-size: 16px; font-weight: 500;'>{co['employees']}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. AI AI - BOLAGSANALYS med riktiga kursdata
    with st.spinner(f"Hämtar dagens analys för {ticker}..."):
        briefing = get_company_briefing(ticker, co["name"], co["sector"], price, pct)
        render_aiai_card(f"Ai ai — {co['name'].split(' ')[0]}", briefing)

    # "Varför?" - förklarar dagens rörelse
    if pct is not None:
        exp_col1, exp_col2 = st.columns([1, 5])
        with exp_col1:
            if st.button("🤔 Varför?", key=f"explain_{ticker}", help="Låt Ai ai förklara dagens kursrörelse"):
                st.session_state[f"show_explain_{ticker}"] = True
        if st.session_state.get(f"show_explain_{ticker}"):
            with st.spinner("Ai ai funderar..."):
                explanation = explain_move(ticker, co["name"], co["sector"], price, pct)
            render_aiai_card(f"Varför rör sig {ticker} idag?", explanation)

    # FLIKAR
    tab_labels = [
        "ℹ️ Djupdykning", "📰 Nyheter", "📊 Nyckeltal", "📈 Kursgraf",
        "⚖️ Faktorer", "🔄 Konkurrenter", "💎 Insider & analytiker",
        "📅 Tidslinje", "💬 Fråga Ai ai"
    ]
    tabs = st.tabs(tab_labels)

    with tabs[0]:
        render_deepdive(ticker, co)
    with tabs[1]:
        render_news(ticker, co)
    with tabs[2]:
        render_key_metrics(ticker)
    with tabs[3]:
        render_price_chart(co["yahoo_ticker"], ticker)
    with tabs[4]:
        render_factors(ticker)
    with tabs[5]:
        render_competitors(ticker)
    with tabs[6]:
        render_insider_analyst(ticker, co)
    with tabs[7]:
        render_timeline(ticker, co)
    with tabs[8]:
        render_ask_ai(ticker, co, price, pct)

    # Footer disclaimer
    st.markdown("""
    <div style='margin-top: 40px; padding: 18px 22px; background: #F2ECE0; border-left: 3px solid #E8DFC8; border-radius: 0 8px 8px 0; font-size: 12px; color: #7A746A; line-height: 1.6;'>
        <strong style='color: #4A4640;'>Om innehållet:</strong> Allmän investeringsanalys baserad på offentligt tillgänglig information — inte personlig rådgivning. Historisk avkastning är ingen garanti för framtida utveckling.
    </div>
    """, unsafe_allow_html=True)


def render_key_metrics(ticker):
    """Renderer nyckeltal med riktiga data från yfinance."""
    co = COMPANIES[ticker]
    with st.spinner("Hämtar nyckeltal..."):
        info = get_fundamentals(co["yahoo_ticker"])

    currency = info.get("currency", "")
    st.markdown("<p style='color: #7A746A; font-size: 13px; margin-bottom: 16px;'>💡 Klicka på ett nyckeltal för att läsa vad det betyder i ordboken.</p>", unsafe_allow_html=True)

    metrics_left = [
        ("Marknadsvärde",  _fmt_mrd(info.get("marketCap"), currency),          "mcap"),
        ("P/E",            _fmt_x(info.get("trailingPE")),                      "pe"),
        ("P/B",            _fmt_x(info.get("priceToBook")),                     "pb"),
        ("EV/EBITDA",      _fmt_x(info.get("enterpriseToEbitda")),              "evebitda"),
        ("Utdelning",      _fmt_pct(info.get("dividendYield")),                 "utbytte"),
        ("ROE",            _fmt_pct(info.get("returnOnEquity")),                "roe"),
        ("Skuldsättning",  _fmt_ratio(info.get("debtToEquity")),                "gjeldsgrad"),
    ]

    metrics_right = [
        ("Omsättning (TTM)",       _fmt_mrd(info.get("totalRevenue"), currency),      "omsetning"),
        ("EBITDA (TTM)",           _fmt_mrd(info.get("ebitda"), currency),            "ebitda"),
        ("Nettoresultat (TTM)",    _fmt_mrd(info.get("netIncomeToCommon"), currency), "nettoresultat"),
        ("EPS (TTM)",              f"{info.get('trailingEps', '—')} {currency}" if info.get("trailingEps") else "—", "eps"),
        ("52-veckors högsta",      f"{info.get('fiftyTwoWeekHigh', '—')} {currency}" if info.get("fiftyTwoWeekHigh") else "—", "konsensus"),
        ("Fritt kassaflöde",       _fmt_mrd(info.get("freeCashflow"), currency),      "kontantstrom"),
    ]

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("<h3 style='font-family: Fraunces, serif; font-size: 18px; margin-bottom: 12px;'>Nyckeltal</h3>", unsafe_allow_html=True)
        for label, value, term_key in metrics_left:
            render_metric_row(label, value, term_key)

    with col_right:
        st.markdown("<h3 style='font-family: Fraunces, serif; font-size: 18px; margin-bottom: 12px;'>Senaste 12 månader (TTM)</h3>", unsafe_allow_html=True)
        for label, value, term_key in metrics_right:
            render_metric_row(label, value, term_key)


def render_metric_row(label: str, value: str, term_key: str):
    """Renderer en klickbar nyckeltal-rad."""
    cols = st.columns([3, 2])
    with cols[0]:
        if term_key in GLOSSARY:
            if st.button(f"❓ {label}", key=f"metric_{label}_{term_key}", help=f"Klicka för att lära dig vad {label} betyder"):
                st.session_state.selected_term = term_key
                navigate_to("Ordbok")
                st.rerun()
        else:
            st.markdown(f"<div style='padding: 8px 0; color: #7A746A;'>{label}</div>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"<div style='padding: 8px 0; text-align: right; font-family: JetBrains Mono, monospace; font-weight: 500;'>{value}</div>", unsafe_allow_html=True)


def render_price_chart(yahoo_ticker, ticker):
    """Renderer interaktiv kursgraf."""
    period = st.selectbox(
        "Period",
        ["1mo", "3mo", "6mo", "1y", "5y"],
        index=1,
        format_func=lambda x: {"1mo": "1 månad", "3mo": "3 månader",
                               "6mo": "6 månader", "1y": "1 år", "5y": "5 år"}[x],
        key=f"period_{ticker}"
    )

    hist = get_price_history(yahoo_ticker, period)

    if hist is None or hist.empty:
        st.warning("Kunde inte hämta kursdata just nu. Försök igen om en stund.")
        return

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist["Close"],
        mode="lines",
        name=ticker,
        line=dict(color="#6B7E5C", width=2),
        fill="tozeroy",
        fillcolor="rgba(107, 126, 92, 0.08)",
    ))

    fig.update_layout(
        template="simple_white",
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
        plot_bgcolor="#FFFBF3",
        paper_bgcolor="#FFFBF3",
        font=dict(family="Inter, sans-serif"),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#E8DFC8", title="Kurs (NOK)"),
    )

    st.plotly_chart(fig, use_container_width=True)


def render_factors(ticker):
    """Renderer makrofaktorer och bolagsfaktorer."""
    col1, col2 = st.columns(2)

    impact_emoji = {"pos": "🟢", "neg": "🔴", "neu": "🟡"}

    with col1:
        st.markdown("<h3 style='font-family: Fraunces, serif; font-size: 18px;'>🌍 Makrofaktorer</h3>", unsafe_allow_html=True)
        st.caption("Externa förhållanden som påverkar värderingen")
        for f in MACRO_FACTORS.get(ticker, []):
            st.markdown(
                f"<div style='background: #F2ECE0; padding: 14px 16px; border-radius: 12px; margin-bottom: 10px;'>"
                f"<div style='font-weight: 500;'>{impact_emoji[f['impact']]} {f['text']}</div>"
                f"<div style='color: #7A746A; font-size: 12px; margin-top: 4px;'>{f['sub']}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    with col2:
        st.markdown("<h3 style='font-family: Fraunces, serif; font-size: 18px;'>🏢 Bolagsspecifika</h3>", unsafe_allow_html=True)
        st.caption("Interna drivkrafter för värderingen")
        for f in COMPANY_FACTORS.get(ticker, []):
            st.markdown(
                f"<div style='background: #F2ECE0; padding: 14px 16px; border-radius: 12px; margin-bottom: 10px;'>"
                f"<div style='font-weight: 500;'>{impact_emoji[f['impact']]} {f['text']}</div>"
                f"<div style='color: #7A746A; font-size: 12px; margin-top: 4px;'>{f['sub']}</div>"
                f"</div>",
                unsafe_allow_html=True
            )


def render_competitors(ticker):
    """Renderer konkurrenttabell."""
    competitors = COMPETITORS.get(ticker, [])
    if not competitors:
        st.info("Konkurrentdata inte tillgängligt för detta bolag.")
        return

    df = pd.DataFrame(competitors)
    df.columns = ["Bolag", "Ticker", "Marknadsvärde", "P/E", "Utdelning", "ROE", "Senaste år", "Rekommendation"]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )


def render_deepdive(ticker, co):
    """Djupdykning om bolaget med logo, AI-genererad detaljerad text."""
    domain = co.get("domain", "")
    logo_url = f"https://logo.clearbit.com/{domain}" if domain else None

    col_logo, col_meta = st.columns([1, 3])
    with col_logo:
        if logo_url:
            st.markdown(
                f"<div style='background:#FFFBF3;border:1px solid #E8DFC8;border-radius:16px;"
                f"padding:24px;display:flex;align-items:center;justify-content:center;min-height:140px;'>"
                f"<img src='{logo_url}' style='max-width:100%;max-height:100px;' alt='{co['name']} logo' "
                f"onerror=\"this.style.display='none'\"></div>",
                unsafe_allow_html=True,
            )
    with col_meta:
        st.markdown(f"""
        <div style='padding:8px 0;'>
            <h2 style='margin:0 0 8px 0;font-family:Fraunces,serif;font-size:26px;'>{co['name']}</h2>
            <div style='display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;'>
                {render_sector_badge(co['sector'])}
                <span style='background:#F2ECE0;color:#4A4640;padding:2px 9px;border-radius:100px;font-size:11px;font-weight:500;'>📍 {co['hq']}</span>
                <span style='background:#F2ECE0;color:#4A4640;padding:2px 9px;border-radius:100px;font-size:11px;font-weight:500;'>📅 Grundat {co['founded']}</span>
                <span style='background:#F2ECE0;color:#4A4640;padding:2px 9px;border-radius:100px;font-size:11px;font-weight:500;'>👥 {co['employees']} anställda</span>
            </div>
            {f'<a href="https://{domain}" target="_blank" style="color:#6B7E5C;text-decoration:none;font-size:13px;">🔗 {domain}</a>' if domain else ''}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: #E8DFC8; margin: 24px 0;'>", unsafe_allow_html=True)

    with st.spinner(f"Ai ai förbereder en djupdykning om {co['name']}..."):
        text = get_company_deepdive(ticker, co["name"], co["sector"], co["about"])
    st.markdown(text)


def render_news(ticker, co):
    """Nyhetsström från Yahoo Finance."""
    st.markdown("<h3 style='font-family: Fraunces, serif; font-size: 20px; margin-bottom: 6px;'>📰 Senaste nyheter</h3>", unsafe_allow_html=True)
    st.caption(f"Artiklar och nyheter om {co['name']} från olika källor")

    news = get_news(co["yahoo_ticker"])
    if not news:
        st.info("Inga nyheter tillgängliga just nu för detta bolag.")
        return

    for item in news[:15]:
        content = item.get("content", item)
        title = content.get("title", "")
        if not title:
            continue
        publisher = content.get("provider", {}).get("displayName") if isinstance(content.get("provider"), dict) else content.get("publisher", "")
        link = content.get("canonicalUrl", {}).get("url") if isinstance(content.get("canonicalUrl"), dict) else content.get("link", "")
        if not link:
            link = content.get("clickThroughUrl", {}).get("url", "") if isinstance(content.get("clickThroughUrl"), dict) else ""
        pub_date = content.get("pubDate") or content.get("displayTime") or ""
        if pub_date:
            try:
                from datetime import datetime as _dt
                pub_date = _dt.fromisoformat(pub_date.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
            except Exception:
                pass
        thumb = ""
        thumbnail = content.get("thumbnail")
        if isinstance(thumbnail, dict):
            resolutions = thumbnail.get("resolutions", [])
            if resolutions:
                thumb = resolutions[0].get("url", "")
            else:
                thumb = thumbnail.get("originalUrl", "")

        thumb_html = f"<img src='{thumb}' style='width:100px;height:80px;object-fit:cover;border-radius:8px;flex-shrink:0;' onerror=\"this.style.display='none'\">" if thumb else ""

        st.markdown(f"""
        <a href='{link}' target='_blank' style='text-decoration:none;color:inherit;'>
        <div style='display:flex;gap:14px;background:#FFFBF3;border:1px solid #E8DFC8;border-radius:12px;padding:14px 16px;margin-bottom:10px;transition:all 0.15s;'
             onmouseover="this.style.borderColor='#6B7E5C'" onmouseout="this.style.borderColor='#E8DFC8'">
            {thumb_html}
            <div style='flex:1;'>
                <div style='font-family:Fraunces,serif;font-weight:500;font-size:15px;color:#2C2A26;margin-bottom:6px;line-height:1.35;'>{title}</div>
                <div style='display:flex;gap:10px;font-size:11px;color:#7A746A;font-family:JetBrains Mono,monospace;'>
                    <span>{publisher or '—'}</span>
                    {f"<span>· {pub_date}</span>" if pub_date else ""}
                </div>
            </div>
        </div>
        </a>
        """, unsafe_allow_html=True)


def render_insider_analyst(ticker, co):
    """Visar insiderhandel och analytikerrekommendationer."""
    yt = co["yahoo_ticker"]
    info = get_fundamentals(yt)

    # ANALYTIKER
    st.markdown("<h3 style='font-family: Fraunces, serif; font-size: 20px; margin-bottom: 6px;'>🎯 Analytikermål</h3>", unsafe_allow_html=True)
    st.caption("Vad professionella analytiker tycker om aktien")

    rec = info.get("recommendationKey", "—")
    rec_label = {
        "strong_buy": "Stark köp", "buy": "Köp", "hold": "Behåll",
        "sell": "Sälj", "strong_sell": "Stark sälj", "underperform": "Undervikt",
    }.get(rec, rec.capitalize() if isinstance(rec, str) else "—")
    n_analysts = info.get("numberOfAnalystOpinions", "—")
    target_mean = info.get("targetMeanPrice")
    target_high = info.get("targetHighPrice")
    target_low = info.get("targetLowPrice")
    currency = info.get("currency", "")

    a_cols = st.columns(4)
    with a_cols[0]:
        st.markdown(f"<div style='font-family:JetBrains Mono,monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.08em;color:#7A746A;'>Konsensus</div><div style='font-family:Fraunces,serif;font-size:22px;font-weight:500;margin-top:4px;'>{rec_label}</div>", unsafe_allow_html=True)
    with a_cols[1]:
        st.markdown(f"<div style='font-family:JetBrains Mono,monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.08em;color:#7A746A;'>Analytiker</div><div style='font-family:Fraunces,serif;font-size:22px;font-weight:500;margin-top:4px;'>{n_analysts}</div>", unsafe_allow_html=True)
    with a_cols[2]:
        tm = f"{target_mean:.0f} {currency}" if target_mean else "—"
        st.markdown(f"<div style='font-family:JetBrains Mono,monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.08em;color:#7A746A;'>Median kursmål</div><div style='font-family:Fraunces,serif;font-size:22px;font-weight:500;margin-top:4px;'>{tm}</div>", unsafe_allow_html=True)
    with a_cols[3]:
        rng = f"{target_low:.0f}–{target_high:.0f}" if target_low and target_high else "—"
        st.markdown(f"<div style='font-family:JetBrains Mono,monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.08em;color:#7A746A;'>Spann</div><div style='font-family:Fraunces,serif;font-size:22px;font-weight:500;margin-top:4px;'>{rng}</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color: #E8DFC8; margin: 28px 0;'>", unsafe_allow_html=True)

    # INSIDERHANDEL
    st.markdown("<h3 style='font-family: Fraunces, serif; font-size: 20px; margin-bottom: 6px;'>💎 Insiderhandel</h3>", unsafe_allow_html=True)
    st.caption("När ledning och styrelse handlar egna aktier — ett signalvärde")

    df = get_insider_transactions(yt)
    if df is None or df.empty:
        st.info("Ingen insiderdata tillgänglig för detta bolag.")
    else:
        show = df.head(10).copy()
        show.columns = [str(c) for c in show.columns]
        st.dataframe(show, use_container_width=True, hide_index=True)


def render_timeline(ticker, co):
    """Visar tidslinje med utdelningar och rapporter."""
    yt = co["yahoo_ticker"]

    st.markdown("<h3 style='font-family: Fraunces, serif; font-size: 20px; margin-bottom: 6px;'>📅 Kommande rapporter</h3>", unsafe_allow_html=True)
    st.caption("Datum då bolaget rapporterar sina resultat")

    ed = get_earnings_dates_data(yt)
    if ed is None or ed.empty:
        st.info("Ingen rapportkalender tillgänglig.")
    else:
        show = ed.head(8).copy()
        show.index = show.index.strftime("%Y-%m-%d")
        show.columns = [str(c) for c in show.columns]
        st.dataframe(show, use_container_width=True)

    st.markdown("<hr style='border-color: #E8DFC8; margin: 28px 0;'>", unsafe_allow_html=True)

    st.markdown("<h3 style='font-family: Fraunces, serif; font-size: 20px; margin-bottom: 6px;'>💰 Utdelningshistorik</h3>", unsafe_allow_html=True)
    st.caption("Utdelningar bolaget har betalat ut över tid")

    divs = get_dividends_history(yt)
    if divs is None or len(divs) == 0:
        st.info("Ingen utdelningshistorik tillgänglig.")
    else:
        recent = divs.tail(20)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=recent.index, y=recent.values,
            marker=dict(color="#6B7E5C"),
            hovertemplate="%{x|%Y-%m-%d}<br>%{y:.2f} kr<extra></extra>",
        ))
        fig.update_layout(
            template="simple_white", height=320,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor="#FFFBF3", paper_bgcolor="#FFFBF3",
            font=dict(family="Inter, sans-serif"),
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(gridcolor="#E8DFC8", title="Utdelning per aktie"),
        )
        st.plotly_chart(fig, use_container_width=True)


def render_ask_ai(ticker, co, price, pct):
    """Fritext-Q&A med Ai ai."""
    st.markdown("<h3 style='font-family: Fraunces, serif; font-size: 20px; margin-bottom: 6px;'>💬 Fråga Ai ai</h3>", unsafe_allow_html=True)
    st.caption(f"Ställ valfri fråga om {co['name']} — Ai ai svarar på svenska")

    examples = [
        f"Vad är största risken med {co['name'].split(' ')[0]}?",
        "Hur tjänar bolaget pengar?",
        "Är aktien dyr eller billig just nu?",
        "Vilka är de viktigaste konkurrenterna?",
    ]
    ex_cols = st.columns(len(examples))
    for i, ex in enumerate(examples):
        with ex_cols[i]:
            if st.button(ex, key=f"ex_{ticker}_{i}", use_container_width=True):
                st.session_state[f"q_{ticker}"] = ex

    question = st.text_area(
        "Din fråga",
        value=st.session_state.get(f"q_{ticker}", ""),
        placeholder=f"T.ex. 'Varför har {ticker} stigit så mycket i år?'",
        key=f"qinput_{ticker}",
        height=80,
        label_visibility="collapsed",
    )

    if st.button("Skicka fråga", type="primary", key=f"send_{ticker}"):
        if question.strip():
            with st.spinner("Ai ai funderar..."):
                answer = ask_ai(question, ticker, co["name"], co["sector"], price, pct)
            st.session_state[f"a_{ticker}"] = (question, answer)
            st.session_state[f"q_{ticker}"] = ""

    saved = st.session_state.get(f"a_{ticker}")
    if saved:
        q, a = saved
        st.markdown(f"""
        <div style='background:#F2ECE0;border-left:3px solid #6B7E5C;border-radius:0 8px 8px 0;padding:14px 18px;margin-top:18px;margin-bottom:10px;font-family:Fraunces,serif;font-style:italic;font-size:14px;color:#4A4640;'>
            Du frågade: "{q}"
        </div>
        """, unsafe_allow_html=True)
        render_aiai_card("Ai ai svarar", a)


# ============================================================
# ROUTER
# ============================================================

page = st.session_state.current_page

if page == "Hem":
    render_home()
elif page == "Ankrarflottan":
    render_fleet()
elif page == "Utforska":
    render_discover()
elif page == "Ordbok":
    render_glossary()
elif page == "Bolag":
    render_company()
else:
    render_home()
