"""
Navigr - Aksjeinformasjon for Oslo Børs
MVP med ankerflåte-konsept

Brukerne starter med 10 selskaper som ankerflåte. De kan kaste anker
(legge til) og ta opp anker (fjerne) som de vil. Ingen aksjebeholdninger
eller verdiberegninger - dette er en lærings- og analyse-app.
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

from config import COMPANIES, INITIAL_FLEET, MACRO_FACTORS, COMPANY_FACTORS, COMPETITORS
from ai_engine import get_market_briefing, get_company_briefing


# ============================================================
# SIDEOPPSETT
# ============================================================

st.set_page_config(
    page_title="Navigr",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Tilpasset CSS for varmere palett
st.markdown("""
<style>
    .main { background-color: #FAF6F0; }
    .stApp { background-color: #FAF6F0; }
    h1, h2, h3 { color: #2C2A26; }
    .stButton button {
        background-color: #6B7E5C;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
    }
    .stButton button:hover {
        background-color: #4F6244;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE - HUSKER ANKERFLÅTEN
# ============================================================

if "fleet" not in st.session_state:
    st.session_state.fleet = list(INITIAL_FLEET)

if "current_page" not in st.session_state:
    st.session_state.current_page = "Hjem"

if "current_company" not in st.session_state:
    st.session_state.current_company = None


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


def drop_anchor(ticker):
    """Kast anker - legger til selskap i flåten."""
    if ticker not in st.session_state.fleet:
        st.session_state.fleet.append(ticker)


def raise_anchor(ticker):
    """Ta opp anker - fjerner selskap fra flåten."""
    if ticker in st.session_state.fleet:
        st.session_state.fleet.remove(ticker)


def navigate_to(page, company=None):
    """Naviger mellom sider."""
    st.session_state.current_page = page
    if company:
        st.session_state.current_company = company


def format_price(price):
    """Formaterer pris med norsk konvensjon."""
    if price is None:
        return "—"
    return f"{price:,.2f}".replace(",", " ").replace(".", ",")


def format_pct(pct):
    """Formaterer prosent med fortegn."""
    if pct is None:
        return "—"
    sign = "+" if pct > 0 else ""
    return f"{sign}{pct:.2f} %"


# ============================================================
# SIDEMENY
# ============================================================

with st.sidebar:
    st.markdown("## ⚓ Navigr")
    st.markdown("*Forstå aksjer. Naviger selv.*")
    st.markdown("---")

    if st.button("🏠 Hjem", use_container_width=True):
        navigate_to("Hjem")
        st.rerun()

    if st.button("⚓ Ankerflåten min", use_container_width=True):
        navigate_to("Ankerflåten")
        st.rerun()

    if st.button("🔍 Oppdag", use_container_width=True):
        navigate_to("Oppdag")
        st.rerun()

    st.markdown("---")
    st.caption(f"**{len(st.session_state.fleet)}** selskaper i flåten")
    st.markdown("---")
    st.caption("⚠️ Generell investeringsanalyse — ikke personlig rådgivning.")


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
        st.markdown("# God morgen 👋")
        st.markdown("*Her er det som rører seg i ankerflåten din i dag*")
    with col_b:
        st.markdown(f"<div style='text-align:right; color:#7A746A; font-family:monospace; padding-top:30px;'>{date_str.upper()}</div>",
                    unsafe_allow_html=True)

    # Ai ai - markedsoppsummering
    st.markdown("---")
    with st.container():
        st.markdown("### 🧭 Ai ai — markedet i dag")
        with st.spinner("Henter dagens markedsoppsummering..."):
            briefing = get_market_briefing()
            st.markdown(briefing)

    st.markdown("---")

    # Info om ankerflåten
    st.info(
        "**Ankerflåten din** består av selskaper du følger. Du startet med de 10 største på Oslo Børs — "
        "du kan ta opp anker fra dem du ikke vil følge, og kaste nye ankere på selskaper du blir nysgjerrig på."
    )

    # Vis ankerflåten
    st.markdown(f"### ⚓ Ankerflåten min ({len(st.session_state.fleet)} selskaper)")

    if not st.session_state.fleet:
        st.warning("Du har ingen selskaper i ankerflåten din. Gå til **Oppdag** for å kaste anker på et selskap.")
    else:
        render_fleet_table(st.session_state.fleet)


def render_fleet_table(tickers):
    """Renderer en tabell over selskaper med kursdata."""
    header_cols = st.columns([0.5, 2.5, 1.5, 1.5, 1, 1.2])
    header_cols[0].markdown("**⚓**")
    header_cols[1].markdown("**Selskap**")
    header_cols[2].markdown("**Sektor**")
    header_cols[3].markdown("**Kurs**")
    header_cols[4].markdown("**Endring**")
    header_cols[5].markdown("**Handling**")

    st.markdown("<hr style='margin:5px 0; border-color:#E8DFC8;'>", unsafe_allow_html=True)

    for ticker in tickers:
        co = COMPANIES[ticker]
        price, change, pct = get_price_data(co["yahoo_ticker"])

        cols = st.columns([0.5, 2.5, 1.5, 1.5, 1, 1.2])
        cols[0].markdown("⚓")
        cols[1].markdown(f"**{ticker}**  \n*{co['name']}*")
        cols[2].markdown(f"<span style='color:#7A746A;font-size:13px;'>{co['sector']}</span>", unsafe_allow_html=True)
        cols[3].markdown(f"`{format_price(price)} kr`" if price else "—")

        if pct is not None:
            color = "#2F6B3E" if pct > 0 else "#8A1F1F" if pct < 0 else "#6B5B2C"
            cols[4].markdown(
                f"<span style='color:{color};font-weight:500;'>{format_pct(pct)}</span>",
                unsafe_allow_html=True
            )
        else:
            cols[4].markdown("—")

        sub_cols = cols[5].columns(2)
        if sub_cols[0].button("Åpne", key=f"open_{ticker}", use_container_width=True):
            navigate_to("Selskap", ticker)
            st.rerun()
        if sub_cols[1].button("⚓×", key=f"raise_{ticker}", help="Ta opp anker", use_container_width=True):
            raise_anchor(ticker)
            st.toast(f"Anker tatt opp fra {ticker}", icon="⚓")
            st.rerun()


# ============================================================
# SIDE: ANKERFLÅTEN
# ============================================================

def render_fleet():
    st.markdown("# ⚓ Ankerflåten min")
    st.markdown("*Selskapene du følger akkurat nå*")
    st.markdown("---")

    if not st.session_state.fleet:
        st.warning("Du har ingen selskaper i ankerflåten din.")
        if st.button("Gå til Oppdag"):
            navigate_to("Oppdag")
            st.rerun()
        return

    st.markdown(f"### {len(st.session_state.fleet)} selskaper")
    render_fleet_table(st.session_state.fleet)


# ============================================================
# SIDE: OPPDAG
# ============================================================

def render_discover():
    st.markdown("# 🔍 Oppdag")
    st.markdown("*Selskaper du ikke har kastet anker på ennå*")
    st.markdown("---")

    not_in_fleet = [t for t in COMPANIES.keys() if t not in st.session_state.fleet]

    if not not_in_fleet:
        st.success("Du følger alle tilgjengelige selskaper. Flott!")
        return

    header_cols = st.columns([0.5, 2.5, 1.5, 1.5, 1, 1.2])
    header_cols[0].markdown("**⚓**")
    header_cols[1].markdown("**Selskap**")
    header_cols[2].markdown("**Sektor**")
    header_cols[3].markdown("**Kurs**")
    header_cols[4].markdown("**Endring**")
    header_cols[5].markdown("**Handling**")

    st.markdown("<hr style='margin:5px 0; border-color:#E8DFC8;'>", unsafe_allow_html=True)

    for ticker in not_in_fleet:
        co = COMPANIES[ticker]
        price, change, pct = get_price_data(co["yahoo_ticker"])

        cols = st.columns([0.5, 2.5, 1.5, 1.5, 1, 1.2])
        cols[0].markdown("<span style='opacity:0.3;'>⚓</span>", unsafe_allow_html=True)
        cols[1].markdown(f"**{ticker}**  \n*{co['name']}*")
        cols[2].markdown(f"<span style='color:#7A746A;font-size:13px;'>{co['sector']}</span>", unsafe_allow_html=True)
        cols[3].markdown(f"`{format_price(price)} kr`" if price else "—")

        if pct is not None:
            color = "#2F6B3E" if pct > 0 else "#8A1F1F" if pct < 0 else "#6B5B2C"
            cols[4].markdown(
                f"<span style='color:{color};font-weight:500;'>{format_pct(pct)}</span>",
                unsafe_allow_html=True
            )
        else:
            cols[4].markdown("—")

        if cols[5].button("⚓ Kast anker", key=f"drop_{ticker}", use_container_width=True):
            drop_anchor(ticker)
            st.toast(f"Anker kastet på {ticker}", icon="⚓")
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

    # Header med navn og kurs
    price, change, pct = get_price_data(co["yahoo_ticker"])

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown(f"# {co['name']}")
        st.markdown(f"**{ticker}** · Oslo Børs · {co['sector']}")
        if is_anchored:
            st.markdown("⚓ *Anker kastet — i ankerflåten din*")
        else:
            st.markdown("*Ikke i ankerflåten din*")

    with col_right:
        if price:
            st.markdown(f"### {format_price(price)} kr")
            if pct is not None:
                color = "#2F6B3E" if pct > 0 else "#8A1F1F" if pct < 0 else "#6B5B2C"
                st.markdown(
                    f"<span style='color:{color};font-size:18px;font-weight:500;'>{format_pct(pct)}</span>",
                    unsafe_allow_html=True
                )

        if is_anchored:
            if st.button("⚓× Ta opp anker", use_container_width=True):
                raise_anchor(ticker)
                st.toast(f"Anker tatt opp fra {ticker}", icon="⚓")
                st.rerun()
        else:
            if st.button("⚓ Kast anker", use_container_width=True, type="primary"):
                drop_anchor(ticker)
                st.toast(f"Anker kastet på {ticker}", icon="⚓")
                st.rerun()

    st.markdown("---")

    # 1. OM SELSKAPET (kommer FØR Ai ai)
    st.markdown("### 📋 Om selskapet")
    st.markdown(co["about"])

    info_cols = st.columns(4)
    info_cols[0].metric("Sektor", co["sector"])
    info_cols[1].metric("Hovedkontor", co["hq"])
    info_cols[2].metric("Grunnlagt", co["founded"])
    info_cols[3].metric("Ansatte", co["employees"])

    st.markdown("---")

    # 2. AI AI - SELSKAPSANALYSE
    st.markdown(f"### 🧭 Ai ai — {co['name'].split(' ')[0]}")
    with st.spinner("Henter dagens analyse..."):
        briefing = get_company_briefing(ticker, co["name"], co["sector"])
        st.markdown(briefing)

    st.markdown("---")

    # 3. FANER
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Kursgraf", "⚖️ Faktorer", "🔄 Konkurrenter", "ℹ️ Mer info"])

    with tab1:
        render_price_chart(co["yahoo_ticker"], ticker)

    with tab2:
        render_factors(ticker)

    with tab3:
        render_competitors(ticker)

    with tab4:
        st.markdown(f"**Selskap:** {co['name']}")
        st.markdown(f"**Ticker:** {ticker}")
        st.markdown(f"**Yahoo Finance ticker:** {co['yahoo_ticker']}")
        st.markdown(f"**Sektor:** {co['sector']}")
        st.markdown(f"**Hovedkontor:** {co['hq']}")
        st.markdown(f"**Grunnlagt:** {co['founded']}")
        st.markdown(f"**Antall ansatte:** {co['employees']}")


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
    impact_label = {"pos": "Positiv", "neg": "Negativ", "neu": "Nøytral"}

    with col1:
        st.markdown("#### 🌍 Makrofaktorer")
        st.caption("Eksterne forhold som påvirker verdsettelsen")
        for f in MACRO_FACTORS.get(ticker, []):
            with st.container():
                st.markdown(f"{impact_emoji[f['impact']]} **{f['text']}**  \n"
                            f"<small style='color:#7A746A;'>{f['sub']}</small>",
                            unsafe_allow_html=True)
                st.markdown("")

    with col2:
        st.markdown("#### 🏢 Selskapsspesifikke")
        st.caption("Interne drivere for verdsettelsen")
        for f in COMPANY_FACTORS.get(ticker, []):
            with st.container():
                st.markdown(f"{impact_emoji[f['impact']]} **{f['text']}**  \n"
                            f"<small style='color:#7A746A;'>{f['sub']}</small>",
                            unsafe_allow_html=True)
                st.markdown("")


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
elif page == "Selskap":
    render_company()
else:
    render_home()
