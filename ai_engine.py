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


# ============================================================
# VISSTE DU? - DAGLIG FAKTA
# ============================================================

def get_did_you_know() -> str:
    """Daglig 'Visste du?'-fakta. Cachas 24 timmar."""
    cache_key = f"didyouknow_{datetime.now().strftime('%Y-%m-%d')}"
    cached = _load_cache(cache_key, max_age_hours=24)
    if cached:
        return cached

    prompt = """Du är Ai ai - en finansguide för svenska investerare.

Skriv en kort (40-70 ord) "Visste du?"-fakta på SVENSKA om något intressant från Oslo Børs, ett av de stora norska bolagen (Equinor, DNB, Aker BP, Norsk Hydro, Telenor, Yara, Mowi, Storebrand, Subsea 7, Scatec), eller ett finansiellt fenomen som påverkar norska aktier.

Variera mellan: historisk händelse, kuriosa, anekdot, statistik, eller pedagogisk poäng.

Börja med "Visste du att..." Skriv som en engagerande pedagog - lättfattlig, lite överraskande. Bara löpande text, ingen rubrik."""

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=250,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        _save_cache(cache_key, text)
        return text
    except Exception as e:
        return f"(Ai ai kunde inte generera fakta just nu: {e})"


# ============================================================
# AI AI FRÅGA - FRITEXT Q&A
# ============================================================

def ask_ai(question: str, ticker: str, name: str, sector: str,
           price=None, pct=None) -> str:
    """Fritext-Q&A om ett bolag. Ingen cache (varje fråga är unik)."""
    if not question.strip():
        return ""

    price_text = ""
    if price is not None and pct is not None:
        sign = "+" if pct > 0 else ""
        price_text = f"\nAktuell kursdata: {price:.2f} kr ({sign}{pct:.2f}% idag)"

    try:
        from config import MACRO_FACTORS, COMPANY_FACTORS
        macro = MACRO_FACTORS.get(ticker, [])
        company = COMPANY_FACTORS.get(ticker, [])
        factors_text = ""
        if macro or company:
            factors_text = "\nViktiga faktorer för bolaget:\n"
            for f in (macro + company)[:6]:
                factors_text += f"- {f['text']}: {f['sub']}\n"
    except Exception:
        factors_text = ""

    prompt = f"""Du är Ai ai - en AI-finansanalytiker för svenska investerare.

Bolag: {name} ({ticker}) på Oslo Børs i sektorn {sector}.{price_text}{factors_text}

Användarens fråga:
{question}

Svara kort (60-120 ord) på SVENSKA. Var konkret, informativ och pedagogisk. Använd faktabakgrunden ovan när relevant. Om frågan inte handlar om bolaget eller aktier, säg det vänligt och styr tillbaka."""

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()
    except Exception as e:
        return f"(Ai ai kunde inte svara just nu: {e})"


# ============================================================
# AI AI FÖRKLARAR DAGENS RÖRELSE
# ============================================================

def get_company_deepdive(ticker: str, name: str, sector: str, about: str) -> str:
    """Detaljert AI-generert deep-dive om bolaget. Cachas 30 dagar."""
    cache_key = f"deepdive_{ticker}"
    cached = _load_cache(cache_key, max_age_hours=720)
    if cached:
        return cached

    prompt = f"""Du är Ai ai - en finansguide för svenska investerare.

Skriv en detaljerad men lättfattlig "djupdykning" om {name} ({ticker}) på Oslo Børs i sektorn {sector} på SVENSKA.

Bolagsbeskrivning: {about}

Strukturera svaret med dessa rubriker (använd ## för rubrik):

## Vad gör bolaget?
2-3 meningar i klar, enkel svenska. Vad producerar eller säljer de? Vem är kunderna?

## Hur tjänar de pengar?
Förklara affärsmodellen pedagogiskt. Vilka är de viktigaste intäktskällorna? Är det cykliskt eller stabilt?

## Var är de starka?
Konkurrensfördelar och marknadsposition. Vad gör bolaget unikt?

## Vad är riskerna?
3-4 huvudrisker investerare bör känna till. Sektorrisk, regulatorisk, operationell.

## Historia i korthet
Nyckelhändelser och milstolpar — kort tidslinje.

Total ca 250-350 ord. Skriv som en kunnig vän som förklarar — engagerande, inte torrt."""

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        _save_cache(cache_key, text)
        return text
    except Exception as e:
        return f"(Ai ai kunde inte generera djupdykning: {e})"


def explain_move(ticker: str, name: str, sector: str,
                 price=None, pct=None) -> str:
    """Förklarar varför aktien rör sig som den gör idag. Cachas 1 timme."""
    cache_key = f"explain_{ticker}_{datetime.now().strftime('%Y-%m-%d-%H')}"
    cached = _load_cache(cache_key, max_age_hours=1)
    if cached:
        return cached

    price_text = ""
    if price is not None and pct is not None:
        sign = "+" if pct > 0 else ""
        price_text = f"{price:.2f} kr ({sign}{pct:.2f}% idag)"

    prompt = f"""Du är Ai ai - en AI-finansanalytiker för svenska investerare.

Bolag: {name} ({ticker}) på Oslo Børs i sektorn {sector}.
Dagens kursutveckling: {price_text}

Förklara varför aktien rör sig som den gör idag. Ta hänsyn till:
- Sektorspecifika drivkrafter (olja, ränta, valuta, råvarupriser)
- Aktuella händelser i bolaget eller branschen
- Bredare marknadssentiment

Skriv 70-110 ord på SVENSKA. Var konkret men erkänn osäkerhet där det är relevant ("kan bero på", "möjligen drivet av"). Ingen rubrik."""

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
        return f"(Ai ai kunde inte förklara just nu: {e})"
