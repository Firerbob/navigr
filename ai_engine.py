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
            data_text = "\n\nAktuella kursdata hämtade just nu:\n" + "\n".join(lines)

    prompt = f"""Du är Ai ai - en AI-finansassistent som ger dagliga marknadssammanfattningar för Oslo Børs till svenska investerare.{data_text}

Skriv en kort (80-120 ord), informativ sammanfattning på svenska som täcker:
- Vilka bolag och sektorer som stiger eller faller mest idag (använd siffrorna ovan)
- En makrofaktor som sannolikt påverkar dagens rörelser (olja, ränta, valuta, etc.)
- Eventuella mönster tvärs över sektorerna

Skriv som en erfaren finansjournalist - informativ, precis, inte sensationell.
Använd inte rubrik. Bara löpande text.
{"Basera analysen på kursdata angivna ovan — detta är riktiga siffror." if data_text else "Inga kursdata tillgängliga — ge en allmän kommentar om Oslo Børs idag."}"""

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
        return f"(Ai ai kunde inte generera marknadssammanfattning just nu: {e})"


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
        price_text = f"\n\nAktuella kursdata: {price:.2f} kr  ({sign}{pct:.2f}% idag)"

    try:
        from config import MACRO_FACTORS, COMPANY_FACTORS
        macro = MACRO_FACTORS.get(ticker, [])
        company = COMPANY_FACTORS.get(ticker, [])
        factors_text = ""
        if macro or company:
            factors_text = "\n\nViktiga faktorer att beakta:\n"
            for f in (macro + company)[:6]:
                factors_text += f"- {f['text']}: {f['sub']} (effekt: {f['impact']})\n"
    except Exception:
        factors_text = ""

    grounded = "Basera analysen på kursdata angivna ovan — detta är riktiga siffror." if price_text else ""

    prompt = f"""Du är Ai ai - en AI-finansanalytiker som ger kortfattade bolagsuppdateringar till svenska investerare.

Generera en kort (70-110 ord) analys på svenska för {name} ({ticker}) som handlas på Oslo Børs i sektorn {sector}.{price_text}{factors_text}

Sammanfattningen ska:
- Kommentera dagens kursutveckling konkret (använd siffrorna ovan)
- Nämna en eller två sannolika drivkrafter bakom rörelsen
- Identifiera en huvudrisk som användaren bör vara medveten om
- Ha en informativ, lugn ton - inte sensationell

Använd inte rubrik. Bara löpande text. {grounded}"""

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
        return f"(Ai ai kunde inte generera analys för {ticker} just nu: {e})"
