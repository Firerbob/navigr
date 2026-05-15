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
from ai_engine import get_market_briefing, get_company_briefing
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

/* Hovedbakgrunn — varm krem */
.main { background-color: #FAF6F0; }
.stApp { background-color: #FAF6F0; }

/* Sidebar — annerledes lys tone */
section[data-testid="stSidebar"] {
    background-color: #FFFBF3;
    border-right: 1px solid #E8DFC8;
}

/* Overskrifter — Fraunces serif */
h1, h2, h3 {
    font-family: 'Fraunces', Georgia, serif !important;
    color: #2C2A26 !important;
    letter-spacing: -0.02em;
}

h1 { font-weight: 500; }
h2 { font-weight: 500; }
h3 { font-weight: 500; }

/* Brødtekst — Inter */
body, p, div, span, label {
    font-family: 'Inter', system-ui, sans-serif;
    color: #2C2A26;
}

/* Knapper — terra-grønn primær */
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

/* Primary button — terra-grønn fylt */
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

/* Faner — bedre styling */
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

/* Custom kort-stiler */
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

/* Holding rad */
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

/* Selskapsnavn typografi */
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

/* Pris-tekst med monospace */
.price-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    font-variant-numeric: tabular-nums;
}

/* Pill for endring */
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

/* Term kort */
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

/* Detaljert term-visning */
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

/* Skjul Streamlit-standardelementer som forstyrrer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Selskap-knapp på rad */
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
    st.session_state.current_page = "Hjem"

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


def greeting() -> str:
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "God morgen 👋"
    if 12 <= hour < 18:
        return "God ettermiddag 👋"
    if 18 <= hour < 23:
        return "God kveld 👋"
    return "Hei 👋"


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
    # Logo og branding
    st.markdown("""
    <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 4px;'>
        <div style='font-size: 28px;'>⚓</div>
        <div style='font-family: Fraunces, serif; font-size: 28px; font-weight: 500; letter-spacing: -0.04em; color: #2C2A26;'>Navigr</div>
    </div>
    <div style='font-family: Fraunces, serif; font-style: italic; font-size: 13px; color: #7A746A; margin-bottom: 24px;'>Forstå aksjer. Naviger selv.</div>
    """, unsafe_allow_html=True)

    _page = st.session_state.current_page
    if st.button("🏠  Hjem", use_container_width=True, key="nav_home",
                 type="primary" if _page == "Hjem" else "secondary"):
        navigate_to("Hjem")
        st.rerun()

    if st.button("⚓  Ankerflåten min", use_container_width=True, key="nav_fleet",
                 type="primary" if _page == "Ankerflåten" else "secondary"):
        navigate_to("Ankerflåten")
        st.rerun()

    if st.button("🔍  Oppdag", use_container_width=True, key="nav_discover",
                 type="primary" if _page == "Oppdag" else "secondary"):
        navigate_to("Oppdag")
        st.rerun()

    if st.button("📖  Ordbok", use_container_width=True, key="nav_glossary",
                 type="primary" if _page == "Ordbok" else "secondary"):
        navigate_to("Ordbok")
        st.session_state.selected_term = None
        st.rerun()

    st.markdown("<hr style='border-color: #E8DFC8; margin: 24px 0;'>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='font-family: JetBrains Mono, monospace; font-size: 11px; color: #7A746A; text-transform: uppercase; letter-spacing: 0.06em;'>
        Ankerflåten
    </div>
    <div style='font-family: Fraunces, serif; font-size: 32px; font-weight: 500; color: #2C2A26; margin-top: 4px;'>
        {len(st.session_state.fleet)} <span style='font-size: 14px; color: #7A746A;'>selskaper</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: #E8DFC8; margin: 24px 0;'>", unsafe_allow_html=True)

    st.caption("⚠️ Generell investeringsanalyse — ikke personlig rådgivning. Historisk avkastning er ingen garanti for fremtidig utvikling.")


# ============================================================
# AI AI KORT
# ============================================================

def render_aiai_card(title: str, body: str):
    """Renderer Ai ai-kort med riktig styling."""
    html = f"""
    <div class='navigr-aiai-card'>
        <div class='navigr-aiai-badge'>Ai</div>
        <div class='navigr-aiai-title'>{title}</div>
        <div class='navigr-aiai-body'>{body}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# SIDE: HJEM
# ============================================================

def render_home():
    today = datetime.now()
    months_no = ["januar", "februar", "mars", "april", "mai", "juni",
                 "juli", "august", "september", "oktober", "november", "desember"]
    date_str = f"{today.day}. {months_no[today.month-1]} {today.year}"

    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown(f"# {greeting()}")
        st.markdown("<p style='font-family: Fraunces, serif; font-style: italic; color: #7A746A; font-size: 15px;'>Her er det som rører seg i ankerflåten din i dag</p>", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"<div style='text-align:right; color:#7A746A; font-family:JetBrains Mono, monospace; font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; padding-top:30px;'>{date_str.upper()}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Ai ai - markedsoppsummering
    with st.spinner("Henter dagens markedsoppsummering..."):
        briefing = get_market_briefing()
        render_aiai_card("Ai ai — markedet i dag", briefing)

    # Info om ankerflåten
    st.markdown("""
    <div style='background: #FFFBF3; border: 1px solid #E8DFC8; border-radius: 16px; padding: 18px 22px; margin-bottom: 20px;'>
        <span style='font-size: 20px; margin-right: 10px;'>⚓</span>
        <strong>Ankerflåten din</strong> består av selskaper du følger. Du startet med de 10 største på Oslo Børs — du kan ta opp anker fra dem du ikke vil følge, og kaste nye ankere på selskaper du blir nysgjerrig på.
    </div>
    """, unsafe_allow_html=True)

    # Vis ankerflåten
    st.markdown(f"### Ankerflåten min")
    st.caption(f"{len(st.session_state.fleet)} selskaper")

    if not st.session_state.fleet:
        st.warning("Du har ingen selskaper i ankerflåten din. Gå til **Oppdag** for å kaste anker på et selskap.")
    else:
        render_fleet_table(st.session_state.fleet, allow_remove=True)


def render_fleet_table(tickers, allow_remove=True):
    """Renderer en tabell over selskaper med kursdata."""
    _lbl = "<div style='font-family:JetBrains Mono,monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.08em;color:#7A746A;padding-bottom:4px;'>{}</div>"
    header_cols = st.columns([0.55, 2.2, 1.4, 1.2, 1.1, 1.6])
    with header_cols[0]: st.markdown(_lbl.format(""), unsafe_allow_html=True)
    with header_cols[1]: st.markdown(_lbl.format("Selskap"), unsafe_allow_html=True)
    with header_cols[2]: st.markdown(_lbl.format("Sektor"), unsafe_allow_html=True)
    with header_cols[3]: st.markdown(_lbl.format("Kurs"), unsafe_allow_html=True)
    with header_cols[4]: st.markdown(_lbl.format("Endring"), unsafe_allow_html=True)
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
                if sub_cols[0].button("Åpne", key=f"open_{ticker}_{st.session_state.current_page}", use_container_width=True):
                    navigate_to("Selskap", ticker)
                    st.rerun()
                if sub_cols[1].button("⚓×", key=f"raise_{ticker}_{st.session_state.current_page}", help="Ta opp anker", use_container_width=True):
                    raise_anchor(ticker)
                    st.toast(f"Anker tatt opp fra {ticker}", icon="⚓")
                    st.rerun()
            else:
                if st.button("⚓ Kast anker", key=f"drop_{ticker}_{st.session_state.current_page}", use_container_width=True, type="primary"):
                    drop_anchor(ticker)
                    st.toast(f"Anker kastet på {ticker}", icon="⚓")
                    st.rerun()

        st.markdown("<hr style='margin: 5px 0; border-color: #E8DFC8;'>", unsafe_allow_html=True)


# ============================================================
# SIDE: ANKERFLÅTEN
# ============================================================

def render_fleet():
    st.markdown("# ⚓ Ankerflåten min")
    st.markdown("<p style='font-family: Fraunces, serif; font-style: italic; color: #7A746A; font-size: 15px;'>Selskapene du følger akkurat nå</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.fleet:
        st.warning("Du har ingen selskaper i ankerflåten din.")
        if st.button("Gå til Oppdag", type="primary"):
            navigate_to("Oppdag")
            st.rerun()
        return

    st.caption(f"{len(st.session_state.fleet)} selskaper")
    render_fleet_table(st.session_state.fleet, allow_remove=True)


# ============================================================
# SIDE: OPPDAG
# ============================================================

def render_discover():
    st.markdown("# 🔍 Oppdag")
    st.markdown("<p style='font-family: Fraunces, serif; font-style: italic; color: #7A746A; font-size: 15px;'>Selskaper du ikke har kastet anker på ennå</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    not_in_fleet = [t for t in COMPANIES.keys() if t not in st.session_state.fleet]

    if not not_in_fleet:
        st.success("Du følger alle tilgjengelige selskaper. Flott!")
        return

    render_fleet_table(not_in_fleet, allow_remove=False)


# ============================================================
# SIDE: ORDBOK
# ============================================================

def render_glossary():
    # Hvis en term er valgt, vis detaljvisning
    if st.session_state.selected_term:
        render_term_detail(st.session_state.selected_term)
        return

    # Hovedside for ordbok
    st.markdown("""
    <div style='background: linear-gradient(135deg, #DDE5D2 0%, #F5E8D0 100%); border-radius: 24px; padding: 32px 36px; margin-bottom: 28px;'>
        <h1 style='font-family: Fraunces, serif; font-size: 32px; font-weight: 500; letter-spacing: -0.025em; color: #2C2A26; margin: 0 0 10px 0;'>
            Ordboken — <em style='color: #4F6244;'>aksje-norsk forklart.</em>
        </h1>
        <p style='font-size: 15px; color: #4A4640; line-height: 1.6; max-width: 580px; margin: 0;'>
            Her finner du de viktigste ordene, uttrykkene og forkortelsene i aksjeverden — forklart på en måte som er lett å forstå. Ingen dumme spørsmål, bare svar.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Søk
    query = st.text_input(
        "Søk",
        value=st.session_state.glossary_query,
        placeholder="🔍  Søk etter et ord eller uttrykk...",
        label_visibility="collapsed",
        key="glossary_search_input"
    )
    st.session_state.glossary_query = query

    # Nivåfilter
    levels = [
        ("all", "Alle"),
        ("basic", "Helt enkelt"),
        ("med", "Litt mer"),
        ("adv", "For de nysgjerrige"),
        ("idiom", "Uttrykk og slang"),
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

    # Resultater
    results = search_terms(query=query, level=st.session_state.glossary_level)

    if not results:
        st.markdown("""
        <div style='padding: 60px 20px; text-align: center; color: #7A746A; font-family: Fraunces, serif; font-style: italic; font-size: 16px;'>
            Vi fant ingen ord som matchet. Prøv et annet søk eller endre filteret.
        </div>
        """, unsafe_allow_html=True)
        return

    # Vis termer i grid (2 kolonner)
    for i in range(0, len(results), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(results):
                key, term = results[i + j]
                with col:
                    render_term_card(key, term)


def render_term_card(key: str, term: dict):
    """Renderer et term-kort som kan klikkes."""
    level = term["level"]
    label = LEVEL_LABELS[level]

    # Card med klikkbar knapp som dekker hele kortet
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

    if st.button(f"Les mer", key=f"term_{key}", use_container_width=True):
        st.session_state.selected_term = key
        st.rerun()


def render_term_detail(key: str):
    """Renderer detaljert visning av en term."""
    term = get_term(key)
    if not term:
        st.error("Ordet ble ikke funnet.")
        if st.button("← Tilbake til ordboken"):
            st.session_state.selected_term = None
            st.rerun()
        return

    # Tilbake-knapp
    if st.button("← Tilbake til ordboken"):
        st.session_state.selected_term = None
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    level = term["level"]
    label = LEVEL_LABELS[level]

    # Tittel og tag
    st.markdown(f"""
    <div style='background: #FFFBF3; border: 1px solid #E8DFC8; border-radius: 16px; padding: 32px 34px; margin-bottom: 20px;'>
        <div class='term-detail-title'>{term['name']}</div>
        {f"<div class='term-detail-pron'>{term['pron']}</div>" if term.get('pron') else ""}
        <span class='term-tag {level}'>{label}</span>

        <div style='border-top: 1px solid #E8DFC8; margin: 18px 0; padding-top: 18px;'></div>

        <div class='term-detail-section-label'>Hva betyr det?</div>
        <div class='term-detail-body'>{term['def']}</div>

        {f'''<div class='term-detail-section-label'>Tenk på det slik</div>
        <div class='term-detail-example-box'>"{term['example']}"</div>''' if term.get('example') else ""}

        {f'''<div class='term-detail-tip-box'><strong>💡 Tips:</strong> {term['tip']}</div>''' if term.get('tip') else ""}
    </div>
    """, unsafe_allow_html=True)

    # Relaterte ord
    if term.get("related"):
        st.markdown("<div class='term-detail-section-label'>Beslektede ord</div>", unsafe_allow_html=True)
        related_cols = st.columns(min(len(term["related"]), 4))
        for i, rel_key in enumerate(term["related"]):
            rel_term = get_term(rel_key)
            if rel_term:
                with related_cols[i % len(related_cols)]:
                    if st.button(rel_term["name"], key=f"rel_{key}_{rel_key}"):
                        st.session_state.selected_term = rel_key
                        st.rerun()


# ============================================================
# SIDE: SELSKAP
# ============================================================

def render_company():
    ticker = st.session_state.current_company
    if not ticker or ticker not in COMPANIES:
        st.error("Ingen selskap valgt.")
        return

    co = COMPANIES[ticker]
    is_anchored = ticker in st.session_state.fleet

    # Tilbake-knapp
    if st.button("← Tilbake til hjem"):
        navigate_to("Hjem")
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Header med navn og kurs
    price, change, pct = get_price_data(co["yahoo_ticker"])

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:14px;margin-bottom:12px;'>
            {render_avatar(ticker).replace("width:36px;height:36px", "width:52px;height:52px").replace("font-size:12px", "font-size:16px")}
            <div>
                <div style='font-family:JetBrains Mono,monospace;font-size:11px;text-transform:uppercase;letter-spacing:0.08em;color:#7A746A;margin-bottom:4px;'>
                    Ankerflåten / {ticker} · OSLO BØRS
                </div>
                <h1 style='margin:0;'>{co['name']}</h1>
                <div style='margin-top:8px;'>{render_sector_badge(co['sector'])}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if is_anchored:
            st.markdown("<div style='display: inline-block; background: #6B7E5C; color: #FFFBF3; padding: 6px 14px; border-radius: 100px; font-size: 12px; font-weight: 500; margin-top: 12px;'>⚓ Anker kastet</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='display: inline-block; background: #DDE5D2; color: #4F6244; padding: 6px 14px; border-radius: 100px; font-size: 12px; font-weight: 500; margin-top: 12px;'>⚓ Ikke i ankerflåten</div>", unsafe_allow_html=True)

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
            if st.button("⚓× Ta opp anker", use_container_width=True, key="toggle_anchor_company"):
                raise_anchor(ticker)
                st.toast(f"Anker tatt opp fra {ticker}", icon="⚓")
                st.rerun()
        else:
            if st.button("⚓ Kast anker", use_container_width=True, type="primary", key="toggle_anchor_company"):
                drop_anchor(ticker)
                st.toast(f"Anker kastet på {ticker}", icon="⚓")
                st.rerun()

    st.markdown("<hr style='border-color: #E8DFC8; margin: 24px 0;'>", unsafe_allow_html=True)

    # 1. OM SELSKAPET (FØR Ai ai)
    st.markdown(f"""
    <div style='background: #FFFBF3; border: 1px solid #E8DFC8; border-radius: 16px; padding: 24px 28px; margin-bottom: 20px;'>
        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 14px;'>
            <div style='width: 4px; height: 18px; background: #6B7E5C; border-radius: 2px;'></div>
            <div style='font-family: Fraunces, serif; font-size: 16px; font-weight: 500; color: #2C2A26;'>Om selskapet</div>
        </div>
        <p style='font-size: 14.5px; line-height: 1.7; color: #4A4640; margin-bottom: 18px;'>{co['about']}</p>
    </div>
    """, unsafe_allow_html=True)

    info_cols = st.columns(4)
    with info_cols[0]:
        st.markdown(f"<div style='font-family:JetBrains Mono,monospace;font-size:10px;text-transform:uppercase;letter-spacing:0.08em;color:#7A746A;margin-bottom:6px;'>Sektor</div>{render_sector_badge(co['sector'])}", unsafe_allow_html=True)
    with info_cols[1]:
        st.markdown(f"<div style='font-family: JetBrains Mono, monospace; font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em; color: #7A746A;'>Hovedkontor</div><div style='font-family: Fraunces, serif; font-size: 16px; font-weight: 500;'>{co['hq']}</div>", unsafe_allow_html=True)
    with info_cols[2]:
        st.markdown(f"<div style='font-family: JetBrains Mono, monospace; font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em; color: #7A746A;'>Grunnlagt</div><div style='font-family: Fraunces, serif; font-size: 16px; font-weight: 500;'>{co['founded']}</div>", unsafe_allow_html=True)
    with info_cols[3]:
        st.markdown(f"<div style='font-family: JetBrains Mono, monospace; font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em; color: #7A746A;'>Ansatte</div><div style='font-family: Fraunces, serif; font-size: 16px; font-weight: 500;'>{co['employees']}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. AI AI - SELSKAPSANALYSE
    with st.spinner(f"Henter dagens analyse for {ticker}..."):
        briefing = get_company_briefing(ticker, co["name"], co["sector"])
        render_aiai_card(f"Ai ai — {co['name'].split(' ')[0]}", briefing)

    # 3. FANER
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Nøkkeltall", "📈 Kursgraf", "⚖️ Faktorer", "🔄 Konkurrenter"])

    with tab1:
        render_key_metrics(ticker)

    with tab2:
        render_price_chart(co["yahoo_ticker"], ticker)

    with tab3:
        render_factors(ticker)

    with tab4:
        render_competitors(ticker)

    # Footer disclaimer
    st.markdown("""
    <div style='margin-top: 40px; padding: 18px 22px; background: #F2ECE0; border-left: 3px solid #E8DFC8; border-radius: 0 8px 8px 0; font-size: 12px; color: #7A746A; line-height: 1.6;'>
        <strong style='color: #4A4640;'>Om innholdet:</strong> Generell investeringsanalyse basert på offentlig tilgjengelig informasjon — ikke personlig rådgivning. Historisk avkastning er ingen garanti for fremtidig utvikling.
    </div>
    """, unsafe_allow_html=True)


def render_key_metrics(ticker):
    """Renderer nøkkeltall med klikkbar forklaringer fra ordboken."""
    st.markdown("<p style='color: #7A746A; font-size: 13px; margin-bottom: 16px;'>💡 Klikk på et nøkkeltall for å lese hva det betyr i ordboken.</p>", unsafe_allow_html=True)

    # Eksempeldata (i en ekte versjon ville disse kommet fra yfinance .info)
    metrics_left = [
        ("Markedsverdi", "892 mrd", "mcap"),
        ("P/E", "7,4x", "pe"),
        ("P/B", "1,8x", "pb"),
        ("EV/EBITDA", "3,2x", "evebitda"),
        ("Utbytte", "8,2 %", "utbytte"),
        ("ROE", "22,1 %", "roe"),
        ("Gjeldsgrad", "0,34", "gjeldsgrad"),
    ]

    metrics_right = [
        ("Omsetning (Q4)", "24,3 mrd USD", "omsetning"),
        ("EBITDA (Q4)", "10,8 mrd USD", "ebitda"),
        ("Netto resultat", "2,1 mrd USD", "nettoresultat"),
        ("EPS", "0,68 USD", "eps"),
        ("Mot konsensus", "+12 %", "konsensus"),
        ("Fri kontantstrøm", "4,2 mrd USD", "kontantstrom"),
    ]

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("<h3 style='font-family: Fraunces, serif; font-size: 18px; margin-bottom: 12px;'>Nøkkeltall</h3>", unsafe_allow_html=True)
        for label, value, term_key in metrics_left:
            render_metric_row(label, value, term_key)

    with col_right:
        st.markdown("<h3 style='font-family: Fraunces, serif; font-size: 18px; margin-bottom: 12px;'>Siste kvartal</h3>", unsafe_allow_html=True)
        for label, value, term_key in metrics_right:
            render_metric_row(label, value, term_key)


def render_metric_row(label: str, value: str, term_key: str):
    """Renderer en klikkbar nøkkeltall-rad."""
    cols = st.columns([3, 2])
    with cols[0]:
        if term_key in GLOSSARY:
            if st.button(f"❓ {label}", key=f"metric_{label}_{term_key}", help=f"Klikk for å lære hva {label} betyr"):
                st.session_state.selected_term = term_key
                navigate_to("Ordbok")
                st.rerun()
        else:
            st.markdown(f"<div style='padding: 8px 0; color: #7A746A;'>{label}</div>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"<div style='padding: 8px 0; text-align: right; font-family: JetBrains Mono, monospace; font-weight: 500;'>{value}</div>", unsafe_allow_html=True)


def render_price_chart(yahoo_ticker, ticker):
    """Renderer interaktiv prisgraf."""
    period = st.selectbox(
        "Periode",
        ["1mo", "3mo", "6mo", "1y", "5y"],
        index=1,
        format_func=lambda x: {"1mo": "1 måned", "3mo": "3 måneder",
                               "6mo": "6 måneder", "1y": "1 år", "5y": "5 år"}[x],
        key=f"period_{ticker}"
    )

    hist = get_price_history(yahoo_ticker, period)

    if hist is None or hist.empty:
        st.warning("Kunne ikke hente kursdata akkurat nå. Prøv igjen om litt.")
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
    """Renderer makrofaktorer og selskapsfaktorer."""
    col1, col2 = st.columns(2)

    impact_emoji = {"pos": "🟢", "neg": "🔴", "neu": "🟡"}

    with col1:
        st.markdown("<h3 style='font-family: Fraunces, serif; font-size: 18px;'>🌍 Makrofaktorer</h3>", unsafe_allow_html=True)
        st.caption("Eksterne forhold som påvirker verdsettelsen")
        for f in MACRO_FACTORS.get(ticker, []):
            st.markdown(
                f"<div style='background: #F2ECE0; padding: 14px 16px; border-radius: 12px; margin-bottom: 10px;'>"
                f"<div style='font-weight: 500;'>{impact_emoji[f['impact']]} {f['text']}</div>"
                f"<div style='color: #7A746A; font-size: 12px; margin-top: 4px;'>{f['sub']}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    with col2:
        st.markdown("<h3 style='font-family: Fraunces, serif; font-size: 18px;'>🏢 Selskapsspesifikke</h3>", unsafe_allow_html=True)
        st.caption("Interne drivere for verdsettelsen")
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
        st.info("Konkurrentdata ikke tilgjengelig for dette selskapet.")
        return

    df = pd.DataFrame(competitors)
    df.columns = ["Selskap", "Ticker", "Markedsverdi", "P/E", "Utbytte", "ROE", "Siste år", "Anbefaling"]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# ROUTER
# ============================================================

page = st.session_state.current_page

if page == "Hjem":
    render_home()
elif page == "Ankerflåten":
    render_fleet()
elif page == "Oppdag":
    render_discover()
elif page == "Ordbok":
    render_glossary()
elif page == "Selskap":
    render_company()
else:
    render_home()
