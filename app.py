"""
Navigr - MVP med Streamlit og Claude

Kjør med: streamlit run app.py
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from anthropic import Anthropic
from dotenv import load_dotenv

from config import COMPANIES, SECTORS, MACRO_FACTORS, COMPANY_FACTORS, COMPETITORS
from ai_engine import (
    generate_market_summary,
    generate_company_analysis,
    generate_recommendation,
    load_cache,
    save_cache,
)

load_dotenv()

st.set_page_config(
    page_title="Navigr",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@400;500;600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', system-ui, sans-serif;
}

.main .block-container {
    max-width: 1180px;
    padding-top: 2rem;
}

h1, h2, h3 {
    font-family: 'Fraunces', Georgia, serif !important;
    font-weight: 500 !important;
    letter-spacing: -0.02em;
}

.nav-brand {
    font-family: 'Fraunces', serif;
    font-size: 22px;
    font-weight: 500;
    letter-spacing: -0.03em;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 0;
}

.nav-brand-mark {
    width: 22px;
    height: 22px;
    background: #2D4A3E;
    border-radius: 5px;
    display: inline-block;
    position: relative;
}

.aiai-card {
    background: linear-gradient(135deg, #F0EEFD 0%, #E6E3FB 100%);
    border-radius: 16px;
    padding: 24px 28px;
    margin: 16px 0 24px;
}

.aiai-title {
    font-family: 'Fraunces', serif;
    font-size: 18px;
    font-weight: 500;
    color: #26215C;
    margin-bottom: 6px;
}

.aiai-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: #7F77DD;
    color: white;
    font-family: 'Fraunces', serif;
    font-weight: 600;
    margin-right: 12px;
    vertical-align: middle;
}

.aiai-body {
    font-size: 15px;
    line-height: 1.65;
    color: #26215C;
    margin-top: 12px;
}

.aiai-meta {
    font-size: 11px;
    color: #7F77DD;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.rec-bar {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 8px;
    margin: 14px 0;
}

.seg {
    padding: 14px 10px;
    border-radius: 10px;
    text-align: center;
    background: #F3F0E8;
    color: #8B8680;
    border: 1px solid #E5E0D4;
}

.seg-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 4px;
}

.seg-val {
    font-family: 'Fraunces', serif;
    font-size: 14px;
    font-weight: 500;
}

.seg.active-up { background: #E4F0E5; color: #2F6B3E; border-color: #2F6B3E; font-weight: 500; }
.seg.active-neutral { background: #F2EBD9; color: #7A6A3E; border-color: #7A6A3E; font-weight: 500; }
.seg.active-down { background: #F5E4E4; color: #9B2C2C; border-color: #9B2C2C; font-weight: 500; }

.factor-card {
    background: #F3F0E8;
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 10px;
    display: grid;
    grid-template-columns: 24px 1fr 70px;
    gap: 12px;
    align-items: center;
}

.factor-num {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 500;
    font-family: 'JetBrains Mono', monospace;
    color: #4A4744;
    border: 1px solid #E5E0D4;
}

.factor-text { font-size: 13px; line-height: 1.4; color: #1A1817; }
.factor-sub { font-size: 11px; color: #8B8680; margin-top: 2px; }

.factor-pill {
    text-align: center;
    font-size: 10px;
    padding: 3px 6px;
    border-radius: 100px;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.factor-pill.pos { background: #E4F0E5; color: #2F6B3E; }
.factor-pill.neg { background: #F5E4E4; color: #9B2C2C; }
.factor-pill.neu { background: #F2EBD9; color: #7A6A3E; }

.pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 100px;
    font-size: 12px;
    font-weight: 500;
    font-family: 'JetBrains Mono', monospace;
}

.pill-up { background: #E4F0E5; color: #2F6B3E; }
.pill-down { background: #F5E4E4; color: #9B2C2C; }
.pill-neutral { background: #F2EBD9; color: #7A6A3E; }

.disc {
    margin-top: 48px;
    padding: 20px 24px;
    background: #F3F0E8;
    border-left: 3px solid #C9C2B2;
    border-radius: 0 10px 10px 0;
    font-size: 11px;
    color: #8B8680;
    line-height: 1.6;
}

.stMetric {
    background: transparent;
    border: none;
    padding: 0;
}

div[data-testid="stMetricValue"] {
    font-family: 'Fraunces', serif !important;
    font-weight: 500 !important;
}

div[data-testid="stMetricLabel"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #8B8680 !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    padding: 12px 18px;
}

.stTabs [aria-selected="true"] {
    color: #1A1817;
    border-bottom-color: #2D4A3E;
}
</style>
"""

st.markdown(STYLE, unsafe_allow_html=True)


@st.cache_data(ttl=900)
def get_price_data(ticker: str, period: str = "3mo"):
    """Henter kursdata fra Yahoo Finance. Cached i 15 minutter."""
    yahoo_ticker = COMPANIES[ticker]["yahoo_ticker"]
    stock = yf.Ticker(yahoo_ticker)
    hist = stock.history(period=period)
    return hist


@st.cache_data(ttl=3600)
def get_company_info(ticker: str):
    """Henter selskapsinformasjon fra Yahoo Finance. Cached i 1 time."""
    yahoo_ticker = COMPANIES[ticker]["yahoo_ticker"]
    try:
        stock = yf.Ticker(yahoo_ticker)
        info = stock.info
        return info
    except Exception as e:
        return {}


def format_number(n, suffix=""):
    if n is None or pd.isna(n):
        return "—"
    if abs(n) >= 1e9:
        return f"{n/1e9:.1f} mrd{suffix}"
    if abs(n) >= 1e6:
        return f"{n/1e6:.1f} mill{suffix}"
    return f"{n:,.0f}{suffix}".replace(",", " ")


def format_pct(n):
    if n is None or pd.isna(n):
        return "—"
    return f"{n*100:.1f}%" if abs(n) < 1 else f"{n:.1f}%"


def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(data, fast=12, slow=26, signal=9):
    exp1 = data.ewm(span=fast).mean()
    exp2 = data.ewm(span=slow).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal).mean()
    return macd, signal_line


if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_ticker" not in st.session_state:
    st.session_state.selected_ticker = None


col1, col2, col3 = st.columns([2, 4, 2])
with col1:
    st.markdown(
        '<div class="nav-brand"><span class="nav-brand-mark"></span>Navigr</div>',
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        '<div style="text-align: right; font-size: 12px; color: #8B8680; padding-top: 8px;">Martin</div>',
        unsafe_allow_html=True,
    )

st.divider()


def show_home():
    months_no = ["januar", "februar", "mars", "april", "mai", "juni",
                 "juli", "august", "september", "oktober", "november", "desember"]
    today = datetime.now()
    date_str = f"{today.day}. {months_no[today.month - 1]} {today.year}"

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("# God morgen, Martin")
        st.markdown(
            '<p style="color: #8B8680; font-size: 13px; margin-top: -10px;">Her er det som rører seg i markedet i dag</p>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div style="text-align: right; padding-top: 18px; font-family: JetBrains Mono, monospace; font-size: 11px; color: #8B8680; text-transform: uppercase; letter-spacing: 0.06em;">{date_str}</div>',
            unsafe_allow_html=True,
        )

    with st.spinner("Ai ai skriver dagens markedsoppsummering..."):
        summary = generate_market_summary()

    now_str = datetime.now().strftime("%H:%M")
    st.markdown(
        f'''
        <div class="aiai-card">
            <div style="display: flex; align-items: center; margin-bottom: 4px;">
                <div class="aiai-badge">Ai</div>
                <div style="flex: 1;">
                    <div class="aiai-title">Ai ai — markedet i dag</div>
                </div>
                <div class="aiai-meta">Oppdatert {now_str}</div>
            </div>
            <div class="aiai-body">{summary}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    st.markdown("### Porteføljen din")

    portfolio_tickers = ["EQNR", "DNB", "MOWI", "AKRBP"]

    portfolio_data = []
    total_value = 0
    total_change = 0

    for ticker in portfolio_tickers:
        try:
            hist = get_price_data(ticker, period="5d")
            if len(hist) >= 2:
                last_price = hist["Close"].iloc[-1]
                prev_price = hist["Close"].iloc[-2]
                change = last_price - prev_price
                pct = (change / prev_price) * 100
                shares = COMPANIES[ticker]["shares"]
                value = last_price * shares
                portfolio_data.append({
                    "ticker": ticker,
                    "name": COMPANIES[ticker]["name"],
                    "price": last_price,
                    "change": change,
                    "pct": pct,
                    "shares": shares,
                    "value": value,
                })
                total_value += value
                total_change += change * shares
        except Exception as e:
            st.warning(f"Kunne ikke laste data for {ticker}")

    if portfolio_data:
        total_pct = (total_change / (total_value - total_change)) * 100 if total_value > total_change else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Verdi", f"{total_value:,.0f} kr".replace(",", " "))
        with col2:
            delta_color = "normal" if total_change >= 0 else "inverse"
            st.metric("I dag", f"{total_change:+,.0f} kr".replace(",", " "),
                     f"{total_pct:+.2f}%")
        with col3:
            st.metric("Posisjoner", len(portfolio_data))

        st.markdown("<br>", unsafe_allow_html=True)

        for p in portfolio_data:
            c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 0.5])
            with c1:
                st.markdown(
                    f"**{p['ticker']}**  \n<span style='color: #8B8680; font-size: 12px;'>{p['name']}</span>",
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    f"<div style='font-family: JetBrains Mono, monospace; text-align: right; padding-top: 8px;'>{p['price']:.2f}</div>",
                    unsafe_allow_html=True,
                )
            with c3:
                pill_class = "pill-up" if p["pct"] >= 0 else "pill-down"
                sign = "+" if p["pct"] >= 0 else ""
                st.markdown(
                    f"<div style='text-align: right; padding-top: 6px;'><span class='pill {pill_class}'>{sign}{p['pct']:.1f}%</span></div>",
                    unsafe_allow_html=True,
                )
            with c4:
                st.markdown(
                    f"<div style='font-family: JetBrains Mono, monospace; text-align: right; padding-top: 8px;'>{p['value']:,.0f}</div>".replace(",", " "),
                    unsafe_allow_html=True,
                )
            with c5:
                if st.button("›", key=f"go_{p['ticker']}", use_container_width=True):
                    st.session_state.page = "company"
                    st.session_state.selected_ticker = p["ticker"]
                    st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)


def show_company(ticker: str):
    co = COMPANIES[ticker]

    if st.button("← Tilbake til forsiden"):
        st.session_state.page = "home"
        st.rerun()

    try:
        hist = get_price_data(ticker, period="3mo")
        if len(hist) < 2:
            st.error("Kunne ikke laste kursdata")
            return
        current_price = hist["Close"].iloc[-1]
        prev_price = hist["Close"].iloc[-2]
        change = current_price - prev_price
        pct = (change / prev_price) * 100

        hist_1y = get_price_data(ticker, period="1y")
        year_change = ((current_price - hist_1y["Close"].iloc[0]) / hist_1y["Close"].iloc[0]) * 100 if len(hist_1y) > 0 else 0
    except Exception as e:
        st.error(f"Feil ved lasting av data: {e}")
        return

    info = get_company_info(ticker)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"# {co['name']}")
        st.markdown(
            f"<div style='color: #8B8680; font-family: JetBrains Mono, monospace; font-size: 12px; letter-spacing: 0.04em; margin-top: -10px;'>{ticker} · Oslo Børs · {co['sector']}</div>",
            unsafe_allow_html=True,
        )
    with col2:
        pill_class = "pill-up" if pct >= 0 else "pill-down"
        sign = "+" if pct >= 0 else ""
        st.markdown(
            f"""
            <div style='text-align: right;'>
                <div style='font-family: Fraunces, serif; font-size: 30px; font-weight: 500; letter-spacing: -0.02em;'>{current_price:.2f} kr</div>
                <div style='margin-top: 4px;'><span class='pill {pill_class}'>{sign}{change:.2f} ({sign}{pct:.2f}%)</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.spinner(f"Ai ai analyserer {co['name']}..."):
        analysis = generate_company_analysis(ticker, current_price, pct, year_change)
        recommendation = generate_recommendation(ticker, info, pct, year_change)

    now_str = datetime.now().strftime("%H:%M")
    st.markdown(
        f'''
        <div class="aiai-card">
            <div style="display: flex; align-items: center; margin-bottom: 4px;">
                <div class="aiai-badge">Ai</div>
                <div style="flex: 1;">
                    <div class="aiai-title">Ai ai — {co['name'].split(' ')[0]}</div>
                </div>
                <div class="aiai-meta">Oppdatert {now_str}</div>
            </div>
            <div class="aiai-body">{analysis}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    st.markdown("#### Vår analyse")

    rec = recommendation["recommendation"]
    reason = recommendation["reason"]

    segs_html = '<div class="rec-bar">'
    for key, label, val in [
        ("down", "Undervekt", "Negativt syn"),
        ("neutral", "Nøytral", "Balansert syn"),
        ("up", "Overvekt", "Positivt syn"),
    ]:
        active = " active-" + key if key == rec else ""
        check = " ✓" if key == rec else ""
        segs_html += f'<div class="seg{active}"><div class="seg-label">{label}{check}</div><div class="seg-val">{val}</div></div>'
    segs_html += "</div>"

    st.markdown(segs_html, unsafe_allow_html=True)
    st.markdown(
        f'<div style="padding: 14px 18px; background: #F3F0E8; border-radius: 10px; font-size: 13px; line-height: 1.55; color: #4A4744;"><strong style="color: #1A1817;">Begrunnelse:</strong> {reason}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Oversikt", "Teknisk analyse", "Konkurrenter", "Faktorer", "Nyheter"]
    )

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Nøkkeltall")
            market_cap = info.get("marketCap")
            pe = info.get("trailingPE")
            pb = info.get("priceToBook")
            div_yield = info.get("dividendYield", 0)
            roe = info.get("returnOnEquity")
            debt_equity = info.get("debtToEquity")

            for label, value in [
                ("Markedsverdi", format_number(market_cap, " NOK") if market_cap else "—"),
                ("P/E", f"{pe:.1f}x" if pe else "—"),
                ("P/B", f"{pb:.2f}x" if pb else "—"),
                ("Utbytte", format_pct(div_yield) if div_yield else "—"),
                ("ROE", format_pct(roe) if roe else "—"),
                ("Gjeldsgrad", f"{debt_equity:.2f}" if debt_equity else "—"),
            ]:
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f"<div style='padding: 8px 0; color: #8B8680; border-bottom: 1px solid #E5E0D4; font-size: 13px;'>{label}</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<div style='padding: 8px 0; text-align: right; font-family: JetBrains Mono, monospace; font-weight: 500; border-bottom: 1px solid #E5E0D4; font-size: 13px;'>{value}</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("##### 52-ukers intervall")
            week_high = info.get("fiftyTwoWeekHigh")
            week_low = info.get("fiftyTwoWeekLow")
            avg_volume = info.get("averageVolume")
            beta = info.get("beta")

            for label, value in [
                ("52v høy", f"{week_high:.2f} kr" if week_high else "—"),
                ("52v lav", f"{week_low:.2f} kr" if week_low else "—"),
                ("Snittvolum", f"{avg_volume:,.0f}".replace(",", " ") if avg_volume else "—"),
                ("Beta", f"{beta:.2f}" if beta else "—"),
                ("Siste år", f"{year_change:+.1f}%"),
            ]:
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f"<div style='padding: 8px 0; color: #8B8680; border-bottom: 1px solid #E5E0D4; font-size: 13px;'>{label}</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<div style='padding: 8px 0; text-align: right; font-family: JetBrains Mono, monospace; font-weight: 500; border-bottom: 1px solid #E5E0D4; font-size: 13px;'>{value}</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("##### Prisutvikling og indikatorer")

        period_map = {"1M": "1mo", "3M": "3mo", "6M": "6mo", "1A": "1y", "5A": "5y"}
        col_p, col_i = st.columns([1, 2])
        with col_p:
            period = st.radio("Periode", list(period_map.keys()), index=1, horizontal=True, key=f"period_{ticker}")
        with col_i:
            indicators = st.multiselect(
                "Indikatorer",
                ["SMA 50", "SMA 200", "Bollinger Bands"],
                default=["SMA 50", "SMA 200"],
                key=f"ind_{ticker}",
            )

        hist_ta = get_price_data(ticker, period=period_map[period])
        close = hist_ta["Close"]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist_ta.index, y=close, name=ticker,
            line=dict(color="#2D4A3E", width=2),
            fill="tozeroy",
            fillcolor="rgba(45,74,62,0.08)",
        ))

        if "SMA 50" in indicators and len(close) >= 50:
            sma50 = close.rolling(50).mean()
            fig.add_trace(go.Scatter(
                x=hist_ta.index, y=sma50, name="SMA 50",
                line=dict(color="#D4B972", width=1.5, dash="dash"),
            ))
        if "SMA 200" in indicators and len(close) >= 200:
            sma200 = close.rolling(200).mean()
            fig.add_trace(go.Scatter(
                x=hist_ta.index, y=sma200, name="SMA 200",
                line=dict(color="#9B5B2C", width=1.5, dash="dot"),
            ))
        if "Bollinger Bands" in indicators and len(close) >= 20:
            sma20 = close.rolling(20).mean()
            std20 = close.rolling(20).std()
            upper = sma20 + 2 * std20
            lower = sma20 - 2 * std20
            fig.add_trace(go.Scatter(
                x=hist_ta.index, y=upper, name="BB Upper",
                line=dict(color="rgba(127,119,221,0.4)", width=1),
            ))
            fig.add_trace(go.Scatter(
                x=hist_ta.index, y=lower, name="BB Lower",
                line=dict(color="rgba(127,119,221,0.4)", width=1),
                fill="tonexty",
                fillcolor="rgba(127,119,221,0.05)",
            ))

        fig.update_layout(
            height=400,
            margin=dict(t=20, b=20, l=20, r=20),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(family="Inter, sans-serif", size=11, color="#4A4744"),
            hovermode="x unified",
            yaxis=dict(side="right", gridcolor="#E5E0D4", tickfont=dict(family="JetBrains Mono, monospace")),
            xaxis=dict(showgrid=False, tickfont=dict(family="JetBrains Mono, monospace")),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("##### Signaler")
        rsi = calculate_rsi(close).iloc[-1] if len(close) > 14 else None
        macd, signal_line = calculate_macd(close)
        macd_val = macd.iloc[-1] if len(macd) > 0 else None
        signal_val = signal_line.iloc[-1] if len(signal_line) > 0 else None
        sma50_current = close.rolling(50).mean().iloc[-1] if len(close) >= 50 else None
        trend_bullish = current_price > sma50_current if sma50_current else None

        c1, c2, c3 = st.columns(3)

        with c1:
            if trend_bullish is not None:
                label = "Bullish" if trend_bullish else "Bearish"
                color = "#2F6B3E" if trend_bullish else "#9B2C2C"
                sub = "Pris over 50d snitt" if trend_bullish else "Pris under 50d snitt"
            else:
                label, color, sub = "—", "#8B8680", "For lite data"
            st.markdown(
                f"<div style='background: #F3F0E8; padding: 14px 16px; border-radius: 10px; border-left: 3px solid {color};'><div style='font-size: 10px; color: #8B8680; text-transform: uppercase; letter-spacing: 0.08em; font-family: JetBrains Mono, monospace;'>Trend (SMA 50)</div><div style='font-weight: 500; font-size: 14px; margin: 4px 0;'>{label}</div><div style='font-size: 11px; color: #8B8680;'>{sub}</div></div>",
                unsafe_allow_html=True,
            )

        with c2:
            if rsi is not None:
                if rsi > 70:
                    label, color = f"{rsi:.0f} — overkjøpt", "#9B2C2C"
                elif rsi < 30:
                    label, color = f"{rsi:.0f} — oversolgt", "#2F6B3E"
                else:
                    label, color = f"{rsi:.0f} — nøytral", "#7A6A3E"
                sub = "14-dagers relativ styrke"
            else:
                label, color, sub = "—", "#8B8680", "For lite data"
            st.markdown(
                f"<div style='background: #F3F0E8; padding: 14px 16px; border-radius: 10px; border-left: 3px solid {color};'><div style='font-size: 10px; color: #8B8680; text-transform: uppercase; letter-spacing: 0.08em; font-family: JetBrains Mono, monospace;'>Momentum (RSI)</div><div style='font-weight: 500; font-size: 14px; margin: 4px 0;'>{label}</div><div style='font-size: 11px; color: #8B8680;'>{sub}</div></div>",
                unsafe_allow_html=True,
            )

        with c3:
            if macd_val is not None and signal_val is not None:
                if macd_val > signal_val:
                    label, color, sub = "Positiv krysning", "#2F6B3E", "MACD over signallinje"
                else:
                    label, color, sub = "Negativ krysning", "#9B2C2C", "MACD under signallinje"
            else:
                label, color, sub = "—", "#8B8680", "For lite data"
            st.markdown(
                f"<div style='background: #F3F0E8; padding: 14px 16px; border-radius: 10px; border-left: 3px solid {color};'><div style='font-size: 10px; color: #8B8680; text-transform: uppercase; letter-spacing: 0.08em; font-family: JetBrains Mono, monospace;'>MACD</div><div style='font-weight: 500; font-size: 14px; margin: 4px 0;'>{label}</div><div style='font-size: 11px; color: #8B8680;'>{sub}</div></div>",
                unsafe_allow_html=True,
            )

    with tab3:
        st.markdown("##### Konkurrentoversikt")
        st.markdown(
            f"<p style='color: #8B8680; font-size: 12px;'>Sammenlignbare selskaper i {co['sector'].lower()}sektor.</p>",
            unsafe_allow_html=True,
        )

        comps = COMPETITORS.get(ticker, [])
        df_comps = pd.DataFrame(comps)
        if not df_comps.empty:
            st.dataframe(
                df_comps,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "name": "Selskap",
                    "ticker": "Ticker",
                    "mcap": "Markedsverdi",
                    "pe": "P/E",
                    "div": "Utbytte",
                    "roe": "ROE",
                    "year": "1 år",
                    "rec": "Analyse",
                },
            )
        st.markdown(
            "<p style='font-size: 11px; color: #8B8680; margin-top: 8px;'>Tall er hentet fra siste kvartalsrapport hvis tilgjengelig. Rader med selskapet ditt er markert.</p>",
            unsafe_allow_html=True,
        )

    with tab4:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### Makrofaktorer")
            st.markdown("<p style='color: #8B8680; font-size: 12px;'>Eksterne forhold som påvirker verdsettelsen.</p>", unsafe_allow_html=True)
            for i, f in enumerate(MACRO_FACTORS.get(ticker, []), 1):
                impact_class = {"pos": "pos", "neg": "neg", "neu": "neu"}[f["impact"]]
                impact_label = {"pos": "Positiv", "neg": "Negativ", "neu": "Nøytral"}[f["impact"]]
                st.markdown(
                    f"""
                    <div class="factor-card">
                        <div class="factor-num">{i}</div>
                        <div>
                            <div class="factor-text">{f['text']}</div>
                            <div class="factor-sub">{f['sub']}</div>
                        </div>
                        <div class="factor-pill {impact_class}">{impact_label}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with col2:
            st.markdown("##### Selskapsspesifikke")
            st.markdown("<p style='color: #8B8680; font-size: 12px;'>Interne drivere for verdsettelsen.</p>", unsafe_allow_html=True)
            for i, f in enumerate(COMPANY_FACTORS.get(ticker, []), 1):
                impact_class = {"pos": "pos", "neg": "neg", "neu": "neu"}[f["impact"]]
                impact_label = {"pos": "Positiv", "neg": "Negativ", "neu": "Nøytral"}[f["impact"]]
                st.markdown(
                    f"""
                    <div class="factor-card">
                        <div class="factor-num">{i}</div>
                        <div>
                            <div class="factor-text">{f['text']}</div>
                            <div class="factor-sub">{f['sub']}</div>
                        </div>
                        <div class="factor-pill {impact_class}">{impact_label}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with tab5:
        st.markdown("##### Nyheter og børsmeldinger")
        st.info("Nyheter integreres fra E24, DN og newsweb.oslobors.no i neste iterasjon. For MVP bruker vi statiske eksempler.")

        sample_news = [
            {"source": "E24", "title": f"{co['name']} i fokus etter ukens markedsbevegelser", "time": "2t"},
            {"source": "DN", "title": f"Analytikere diskuterer {co['name']}s posisjon i sektoren", "time": "4t"},
            {"source": "Børsmelding", "title": "Kvartalsrapport publiseres kommende uke", "time": "i går"},
            {"source": "Finansavisen", "title": f"Hva betyr sektortrendene for {ticker}?", "time": "2d"},
            {"source": "Reuters", "title": "Europeiske markeder reagerer på makroendringer", "time": "3d"},
        ]
        for n in sample_news:
            c1, c2, c3 = st.columns([1, 6, 1])
            with c1:
                st.markdown(f"<div style='font-family: JetBrains Mono, monospace; font-size: 10px; text-transform: uppercase; letter-spacing: 0.06em; color: #2D4A3E; font-weight: 500; padding-top: 6px;'>{n['source']}</div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div style='padding: 4px 0; font-size: 13px; border-bottom: 1px solid #E5E0D4; padding-bottom: 12px; margin-bottom: 12px;'>{n['title']}</div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div style='font-family: JetBrains Mono, monospace; font-size: 11px; color: #8B8680; text-align: right; padding-top: 6px;'>{n['time']}</div>", unsafe_allow_html=True)


if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "company" and st.session_state.selected_ticker:
    show_company(st.session_state.selected_ticker)


st.markdown(
    """
    <div class="disc">
        <strong style="color: #4A4744;">Om Navigr:</strong> Dette er et privat verktøy under utvikling. Innholdet baseres på offentlig tilgjengelig informasjon og utgjør ikke personlig investeringsrådgivning. Historisk avkastning er ingen garanti for fremtidig utvikling.
    </div>
    """,
    unsafe_allow_html=True,
)
