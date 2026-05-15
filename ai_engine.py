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

MODEL = "claude-sonnet-4-5"

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

def get_market_briefing() -> str:
    """Henter daglig markedsoppsummering for Oslo Børs.

    Cacher resultatet i 12 timer for å unngå unødige API-kall.
    """
    today = datetime.now().strftime("%Y-%m-%d-%H")
    # Cache key bare på dato (ikke time) — fornyes hver 12 time
    date_key = datetime.now().strftime("%Y-%m-%d")
    half_day = "morning" if datetime.now().hour < 12 else "afternoon"
    cache_key = f"market_{date_key}_{half_day}"

    cached = _load_cache(cache_key, max_age_hours=12)
    if cached:
        return cached

    prompt = """Du er Ai ai - en AI-finansassistent som gir daglige markedsoppsummeringer for Oslo Børs til norske investorer.

Skriv en kort (80-120 ord), informativ oppsummering på norsk som dekker:
- Hovedindeksen (OSEBX) sin generelle utvikling i dag
- De viktigste sektorene som beveger seg (positivt eller negativt)
- Minst ett eller to nøkkelselskaper med konkret prisendring
- En makrofaktor som påvirker dagens handel (olje, rente, valuta, etc.)
- Eventuelle viktige hendelser (rapporter, utbytter, oppkjøp)

Skriv som erfaren finansjournalist - informativ, presis, ikke sensasjonell.
Ikke bruk overskrift. Bare løpende tekst.

Siden dette er en demo og du ikke har sanntidsdata, bruk realistiske markedsdata for en typisk handelsdag på Oslo Børs. Det er viktig at teksten gir naturlig sammenheng. Brukeren forstår at dette er demo og ikke ekte sanntidsdata."""

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

def get_company_briefing(ticker: str, name: str, sector: str) -> str:
    """Henter dagens analyse for et spesifikt selskap.

    Cacher resultatet i 12 timer per selskap.
    """
    date_key = datetime.now().strftime("%Y-%m-%d")
    half_day = "morning" if datetime.now().hour < 12 else "afternoon"
    cache_key = f"company_{ticker}_{date_key}_{half_day}"

    cached = _load_cache(cache_key, max_age_hours=12)
    if cached:
        return cached

    # Hent ekstra kontekst fra config hvis tilgjengelig
    try:
        from config import MACRO_FACTORS, COMPANY_FACTORS
        macro = MACRO_FACTORS.get(ticker, [])
        company = COMPANY_FACTORS.get(ticker, [])

        factors_text = ""
        if macro or company:
            factors_text = "\n\nViktige faktorer å hensynta:\n"
            for f in (macro + company)[:6]:  # max 6 faktorer for å holde prompten kompakt
                factors_text += f"- {f['text']}: {f['sub']} (effekt: {f['impact']})\n"
    except Exception:
        factors_text = ""

    prompt = f"""Du er Ai ai - en AI-finansanalytiker som gir kortfattede selskapsoppdateringer til norske investorer.

Generer en kort (70-110 ord) analyse på norsk for {name} ({ticker}) som handles på Oslo Børs i sektoren {sector}.{factors_text}

Oppsummeringen skal:
- Forklare hva som rører seg rundt selskapet akkurat nå
- Nevne én eller to konkrete drivere (kvartalsrapport, sektor-trend, makro)
- Identifisere én hovedrisiko brukeren bør være oppmerksom på
- Ha en informativ, rolig tone - ikke sensasjonell

Ikke bruk overskrift. Bare løpende tekst. Skriv som om dette er en oppdatering for i dag.

Siden dette er en demo bruk realistiske data for selskapet. Brukeren forstår at dette ikke er sanntidsdata."""

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
