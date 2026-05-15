# Navigr MVP

En Streamlit-app som gir AI-drevet analyse av børsnoterte selskaper på Oslo Børs.

## Funksjoner

- Ai ai-markedsoppsummering på forsiden, oppdateres daglig
- Ai ai-analyse per selskap med Claude Sonnet
- Automatisk anbefaling: undervekt / nøytral / overvekt
- Live kursdata fra Yahoo Finance
- Teknisk analyse: SMA 50, SMA 200, Bollinger Bands, RSI, MACD
- Konkurrentoversikt med 5 sammenlignbare selskaper per selskap
- 5 makrofaktorer og 5 selskapsspesifikke faktorer per selskap
- Fire selskaper i MVP: Equinor, DNB, Mowi, Aker BP

## Forutsetninger

1. Python 3.10 eller nyere installert
2. Anthropic API-nøkkel (med kreditt på kontoen)

## Installasjon — Mac

Åpne Terminal (Cmd+Space, skriv "terminal", enter).

```bash
# 1. Gå til mappen der du har lagret filene
cd ~/Downloads/navigr-streamlit

# 2. Opprett virtuelt miljø
python3 -m venv venv

# 3. Aktiver miljøet
source venv/bin/activate

# 4. Installer pakker
pip install -r requirements.txt

# 5. Kopier .env.example til .env
cp .env.example .env

# 6. Åpne .env og legg inn API-nøkkelen din
open .env
# (Bytt ut sk-ant-din-api-nokkel-her med din ekte nøkkel, lagre filen)

# 7. Kjør appen
streamlit run app.py
```

## Installasjon — Windows

Åpne Command Prompt (trykk Windows-tast, skriv "cmd", enter).

```cmd
REM 1. Gå til mappen der du har lagret filene
cd %USERPROFILE%\Downloads\navigr-streamlit

REM 2. Opprett virtuelt miljø
python -m venv venv

REM 3. Aktiver miljøet
venv\Scripts\activate

REM 4. Installer pakker
pip install -r requirements.txt

REM 5. Kopier .env.example til .env
copy .env.example .env

REM 6. Åpne .env og legg inn API-nøkkelen din
notepad .env
REM (Bytt ut sk-ant-din-api-nokkel-her med din ekte nøkkel, lagre filen)

REM 7. Kjør appen
streamlit run app.py
```

Etter siste kommando åpner Streamlit automatisk nettleseren din på `http://localhost:8501`.

## Slik får du Anthropic API-nøkkel

1. Gå til https://console.anthropic.com
2. Opprett konto
3. Legg til kredittkort under "Plans & Billing"
4. Kjøp 10 USD i kreditt (holder i ukevis for MVP-testing)
5. Gå til "API Keys" og klikk "Create Key"
6. Gi nøkkelen et navn (f.eks. "Navigr MVP")
7. Kopier nøkkelen som starter med `sk-ant-...`
8. Lim inn i `.env`-filen

## Prosjektstruktur

```
navigr-streamlit/
├── app.py              # Hovedapp (Streamlit)
├── config.py           # Selskapsdata, faktorer, konkurrenter
├── ai_engine.py        # Claude-integrasjon (Ai ai)
├── requirements.txt    # Python-avhengigheter
├── .env.example        # Mal for miljøvariabler
├── .env                # Din faktiske API-nøkkel (opprett selv)
├── .gitignore          # Hindrer at .env blir delt
├── cache/              # Cached AI-svar (opprettes automatisk)
└── README.md           # Denne filen
```

## Caching

Appen cacher AI-svar i `cache/`-mappen for å unngå unødige API-kall:
- Markedsoppsummering: 12 timer
- Selskapsanalyse: 12 timer  
- Anbefaling: 24 timer
- Kursdata fra Yahoo Finance: 15 minutter

Du kan slette `cache/`-mappen når som helst for å tvinge nye AI-kall.

## Kostnader

Forventet månedskostnad med 4 selskaper og daglig oppdatering:
- Markedsoppsummering: 1 kall/dag = ~5 kr/mnd
- Selskapsanalyse: 4 kall/dag = ~20 kr/mnd
- Anbefaling: 4 kall/dag = ~25 kr/mnd
- **Totalt: ~50 kr/mnd**

Yahoo Finance og Streamlit er gratis.

## Legg til nye selskaper

Åpne `config.py` og legg til selskapet i:
1. `COMPANIES` — selskapsinformasjon og Yahoo-ticker
2. `MACRO_FACTORS` — 5 makrofaktorer
3. `COMPANY_FACTORS` — 5 selskapsspesifikke faktorer
4. `COMPETITORS` — 5 konkurrenter

Deretter starter du appen på nytt.

## Deploy til Streamlit Cloud (gratis)

Når du er klar for å dele med testbrukere:

1. Lag en konto på https://share.streamlit.io
2. Push koden til et privat GitHub-repo (uten `.env`-filen!)
3. Koble repoet til Streamlit Cloud
4. Legg inn `ANTHROPIC_API_KEY` som secret under app settings
5. Du får en URL som `navigr-mvp.streamlit.app` du kan dele

## Feilsøking

**"No module named 'streamlit'"**
Virtuelt miljø er ikke aktivert. Kjør `source venv/bin/activate` (Mac) eller `venv\Scripts\activate` (Windows).

**"ANTHROPIC_API_KEY not found"**
`.env`-filen mangler eller API-nøkkelen er ikke lagt inn riktig.

**"No data found for ticker"**
Yahoo Finance kan være ustabil. Vent litt og prøv igjen.

**"insufficient_quota"**
Anthropic-kontoen er tom for kreditt. Legg til mer under "Plans & Billing".

## Disclaimer

Navigr er et verktøy for informasjon og analyse. Innholdet baseres på offentlig tilgjengelig informasjon og utgjør ikke personlig investeringsrådgivning. Historisk avkastning er ingen garanti for fremtidig utvikling.
