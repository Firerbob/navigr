"""
Ai ai-motoren for Navigr - genererer markedsoppsummering og selskapsanalyse
med Claude.

Bruker lokal cache for å unngå unødige API-kall. Cachen fornyes etter 12 timer.
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta

from dotenv import load_dotenv
from anthropic import Anthropic

# Last inn API-nøkkel fra .env
load_dotenv()

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

MODEL = "claude-sonnet-4-6"

# Initialiser Anthropic-klienten (henter API-nøkkel fra .env automatisk)
client = Anthropic()


# ============================================================
# CACHE-HJELPERE
# ============================================================

def _load_cache(key: str, max_age_hours: int = 12):
    """Laster cached svar hvis det finnes og ikke er for gammelt."""
    cache_file = CACHE_DIR / f"{key}.json"
    if not cache_file.exists():
        return None
    try:
        data = json.loads(cache_file.read_text(encoding="utf-8"))
        cached_time = datetime.fromisoformat(data["timestamp"])
        if datetime.now() - cached_time < timedelta(hours=max_age_hours):
            return data["content"]
    except Exception:
        return None
    return None


def _save_cache(key: str, content: str):
    """Lagrer svar til cache."""
    cache_file = CACHE_DIR / f"{key}.json"
    cache_file.write_text(
        json.dumps({
            "timestamp": datetime.now().isoformat(),
            "content": content,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


# ============================================================
# MARKEDSOPPSUMMERING (Ai ai på forsiden)
# ============================================================

def get_market_briefing(market_data: list | None = None) -> str:
    """Henter daglig markedsoppsummering for Oslo Børs.

    market_data: liste med dicts {ticker, name, sector, price, pct} — ekte kursdata fra yfinance.
    Cacher resultatet i 1 time.
    """
    cache_key = f"market_{datetime.now().strftime('%Y-%m-%d-%H')}"

    cached = _load_cache(cache_key, max_age_hours=1)
    if cached:
        return cached

    data_text = ""
    if market_data:
        lines = []
        for d in market_data:
            if d["price"] is not None and d["pct"] is not None:
                sign = "+" if d["pct"] > 0 else ""
                lines.append(
                    f"- {d['ticker']} ({d['name']}, {d['sector']}): "
                    f"{d['price']:.2f} kr  {sign}{d['pct']:.2f}% i dag"
                )
        if lines:
            data_text = "\n\nAktuelle kursdata hentet akkurat nå:\n" + "\n".join(lines)

    prompt = f"""Du er Ai ai - en AI-finansassistent som gir daglige markedsoppsummeringer for Oslo Børs til norske investorer.{data_text}

Skriv en kort (80-120 ord), informativ oppsummering på norsk som dekker:
- Hvilke selskaper og sektorer som stiger eller faller mest i dag (bruk tallene over)
- En makrofaktor som sannsynlig påvirker dagens bevegelser (olje, rente, valuta, etc.)
- Eventuelle mønstre på tvers av sektorene

Skriv som erfaren finansjournalist - informativ, presis, ikke sensasjonell.
Ikke bruk overskrift. Bare løpende tekst.
{"Basér analysen på kursdata oppgitt over — dette er ekte tall." if data_text else "Ingen kursdata tilgjengelig — gi en generell kommentar om Oslo Børs i dag."}"""

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        _save_cache(cache_key, text)
        return text
    except Exception as e:
        return f"(Ai ai kunne ikke generere markedsoppsummering akkurat nå: {e})"


# ============================================================
# SELSKAPSANALYSE (Ai ai på selskapssiden)
# ============================================================

def get_company_briefing(
    ticker: str,
    name: str,
    sector: str,
    price: float | None = None,
    pct: float | None = None,
) -> str:
    """Henter dagens analyse for et spesifikt selskap.

    price/pct: ekte kursdata fra yfinance.
    Cacher resultatet i 1 time per selskap.
    """
    cache_key = f"company_{ticker}_{datetime.now().strftime('%Y-%m-%d-%H')}"

    cached = _load_cache(cache_key, max_age_hours=1)
    if cached:
        return cached

    price_text = ""
    if price is not None and pct is not None:
        sign = "+" if pct > 0 else ""
        price_text = f"\n\nAktuelle kursdata: {price:.2f} kr  ({sign}{pct:.2f}% i dag)"

    try:
        from config import MACRO_FACTORS, COMPANY_FACTORS
        macro = MACRO_FACTORS.get(ticker, [])
        company = COMPANY_FACTORS.get(ticker, [])
        factors_text = ""
        if macro or company:
            factors_text = "\n\nViktige faktorer å hensynta:\n"
            for f in (macro + company)[:6]:
                factors_text += f"- {f['text']}: {f['sub']} (effekt: {f['impact']})\n"
    except Exception:
        factors_text = ""

    grounded = "Basér analysen på kursdata oppgitt over — dette er ekte tall." if price_text else ""

    prompt = f"""Du er Ai ai - en AI-finansanalytiker som gir kortfattede selskapsoppdateringer til norske investorer.

Generer en kort (70-110 ord) analyse på norsk for {name} ({ticker}) som handles på Oslo Børs i sektoren {sector}.{price_text}{factors_text}

Oppsummeringen skal:
- Kommentere dagens kursutvikling konkret (bruk tallene over)
- Nevne én eller to sannsynlige drivere bak bevegelsen
- Identifisere én hovedrisiko brukeren bør være oppmerksom på
- Ha en informativ, rolig tone - ikke sensasjonell

Ikke bruk overskrift. Bare løpende tekst. {grounded}"""

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        _save_cache(cache_key, text)
        return text
    except Exception as e:
        return f"(Ai ai kunne ikke generere analyse for {ticker} akkurat nå: {e})"
