"""
Ai ai-motoren for Navigr - genererer markedsoppsummering,
selskapsanalyse og anbefalinger med Claude.

Bruker lokal cache for å unngå unødige API-kall.
Cachen fornyes hver 24. time.
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta

from anthropic import Anthropic

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

MODEL = "claude-sonnet-4-5"

client = Anthropic()


def load_cache(key: str, max_age_hours: int = 24):
    """Laster cached svar hvis det finnes og ikke er for gammelt."""
    cache_file = CACHE_DIR / f"{key}.json"
    if not cache_file.exists():
        return None
    try:
        data = json.loads(cache_file.read_text())
        cached_time = datetime.fromisoformat(data["timestamp"])
        if datetime.now() - cached_time < timedelta(hours=max_age_hours):
            return data["content"]
    except Exception:
        return None
    return None


def save_cache(key: str, content):
    """Lagrer svar til cache."""
    cache_file = CACHE_DIR / f"{key}.json"
    cache_file.write_text(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "content": content,
    }, ensure_ascii=False, indent=2))


def generate_market_summary() -> str:
    """Genererer daglig markedsoppsummering for Oslo Børs."""
    today = datetime.now().strftime("%Y-%m-%d")
    cache_key = f"market_{today}"

    cached = load_cache(cache_key, max_age_hours=12)
    if cached:
        return cached

    prompt = """Du er Ai ai - en AI-finansassistent som gir daglige markedsoppsummeringer for Oslo Børs til norske investorer.

Skriv en kort (80-120 ord), informativ oppsummering på norsk som dekker:
- Hovedindeksen (OSEBX) sin generelle utvikling i dag
- De viktigste sektorene som beveger seg (positivt eller negativt)
- Minst ett eller to nøkkelselskaper med konkret prisendring
- En makrofaktor som påvirker dagens handel (olje, rente, valuta, etc.)
- Eventuelle viktige hendelser (rapporter, utbytter, oppkjøp)

Skriv som erfaren finansjournalist - informativ, presis, ikke sensasjonell. Ikke bruk overskrift. Bare løpende tekst.

Siden dette er en demo og du ikke har sanntidsdata, bruk realistiske norske markedsdata fra 2025. Det er viktig at teksten gir en naturlig sammenheng og konsistens. Dette er en demo, så brukeren forstår at det ikke er ekte sanntidsdata."""

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        save_cache(cache_key, text)
        return text
    except Exception as e:
        return f"(Ai ai kunne ikke generere oppsummering: {e})"


def generate_company_analysis(ticker: str, current_price: float, day_change_pct: float, year_change_pct: float) -> str:
    """Genererer selskapsspesifikk Ai ai-analyse."""
    today = datetime.now().strftime("%Y-%m-%d")
    cache_key = f"company_{ticker}_{today}"

    cached = load_cache(cache_key, max_age_hours=12)
    if cached:
        return cached

    from config import COMPANIES, MACRO_FACTORS, COMPANY_FACTORS

    co = COMPANIES.get(ticker, {})
    macro = MACRO_FACTORS.get(ticker, [])
    company = COMPANY_FACTORS.get(ticker, [])

    factors_text = "\n".join([
        f"- {f['text']}: {f['sub']} (impact: {f['impact']})"
        for f in macro + company
    ])

    prompt = f"""Du er Ai ai - en AI-finansanalytiker som gir kortfattede selskapsoppdateringer til norske investorer.

Generer en kort (60-100 ord) analyse på norsk for {co.get('name', ticker)} ({ticker}) basert på følgende:

Dagens kurs: {current_price:.2f} kr
Dagens endring: {day_change_pct:+.1f}%
Siste 12 måneder: {year_change_pct:+.1f}%
Sektor: {co.get('sector', 'N/A')}

Viktige faktorer å vurdere:
{factors_text}

Oppsummeringen skal:
- Forklare hva som skjer med selskapet akkurat nå (dagens bevegelse)
- Nevne én eller to konkrete drivere (positive eller negative)
- Identifisere én hovedrisiko
- Ha en informativ, rolig tone - ikke sensasjonell

Ikke bruk overskrift. Bare løpende tekst. Skriv som om dette var i dag."""

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        save_cache(cache_key, text)
        return text
    except Exception as e:
        return f"(Ai ai kunne ikke generere analyse: {e})"


def generate_recommendation(ticker: str, info: dict, day_change_pct: float, year_change_pct: float) -> dict:
    """Genererer anbefaling (undervekt/nøytral/overvekt) med begrunnelse."""
    today = datetime.now().strftime("%Y-%m-%d")
    cache_key = f"rec_{ticker}_{today}"

    cached = load_cache(cache_key, max_age_hours=24)
    if cached:
        return cached

    from config import COMPANIES

    co = COMPANIES.get(ticker, {})

    pe = info.get("trailingPE", "N/A")
    pb = info.get("priceToBook", "N/A")
    div_yield = info.get("dividendYield", 0) * 100 if info.get("dividendYield") else 0
    roe = info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else 0
    market_cap = info.get("marketCap", 0) / 1e9

    prompt = f"""Du er Ai ai - en AI-analytiker som vurderer aksjer på Oslo Børs.

Gi en anbefaling for {co.get('name', ticker)} ({ticker}) basert på følgende data:

Sektor: {co.get('sector', 'N/A')}
Markedsverdi: {market_cap:.0f} mrd NOK
P/E: {pe if isinstance(pe, (int, float)) else 'N/A'}
P/B: {pb if isinstance(pb, (int, float)) else 'N/A'}
Utbytte: {div_yield:.1f}%
ROE: {roe:.1f}%
Siste 12 måneder: {year_change_pct:+.1f}%

Ikke ta hensyn til brukerens spesifikke situasjon - dette er generell investeringsanalyse, ikke personlig rådgivning.

Svar kun med et JSON-objekt i dette eksakte formatet (uten markdown-formatering, kun ren JSON):

{{"recommendation": "up" | "neutral" | "down", "reason": "60-100 ord begrunnelse på norsk som dekker verdsettelse, inntjeningskvalitet og hovedrisiko"}}

"up" = overvekt (positivt syn)
"neutral" = nøytral (balansert syn)
"down" = undervekt (negativt syn)"""

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()

        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        result = json.loads(text)

        if result.get("recommendation") not in ["up", "neutral", "down"]:
            result["recommendation"] = "neutral"

        save_cache(cache_key, result)
        return result
    except Exception as e:
        return {
            "recommendation": "neutral",
            "reason": f"Anbefaling ikke tilgjengelig ({e}). Bruker fallback.",
        }
