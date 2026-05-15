"""
Konfigurasjon for Navigr - selskaper, faktorer og konkurrenter.

Dette er dataene som ikke hentes fra Yahoo Finance.
Utvid dette for å legge til flere selskaper.
"""

COMPANIES = {
    "EQNR": {
        "name": "Equinor ASA",
        "yahoo_ticker": "EQNR.OL",
        "sector": "Energi",
        "shares": 315,
    },
    "DNB": {
        "name": "DNB Bank ASA",
        "yahoo_ticker": "DNB.OL",
        "sector": "Finans",
        "shares": 318,
    },
    "MOWI": {
        "name": "Mowi ASA",
        "yahoo_ticker": "MOWI.OL",
        "sector": "Sjømat",
        "shares": 300,
    },
    "AKRBP": {
        "name": "Aker BP ASA",
        "yahoo_ticker": "AKRBP.OL",
        "sector": "Energi",
        "shares": 235,
    },
}

SECTORS = {
    "Energi": ["EQNR", "AKRBP"],
    "Finans": ["DNB"],
    "Sjømat": ["MOWI"],
}

MACRO_FACTORS = {
    "EQNR": [
        {"text": "Brent oljepris", "sub": "Hver USD over 80 gir ca 0,8 mrd i EBITDA", "impact": "pos"},
        {"text": "Europeiske gasspriser", "sub": "TTF-priser styrer inntekter fra europeisk gass", "impact": "neg"},
        {"text": "Petroleumsbeskatning", "sub": "Marginalskatt på 78% — politisk risikofaktor", "impact": "neg"},
        {"text": "USD/NOK kurs", "sub": "Inntekter i USD, kostnader delvis i NOK", "impact": "pos"},
        {"text": "Energy transition-tempo", "sub": "Press mot fossil virksomhet fra ESG-investorer", "impact": "neu"},
    ],
    "DNB": [
        {"text": "Norges Banks styringsrente", "sub": "Hver 0,25 pp = ca 500 mill i nettorentemargin", "impact": "pos"},
        {"text": "Boligprisutvikling", "sub": "Påvirker kredittap og etterspørsel etter boliglån", "impact": "pos"},
        {"text": "Norsk BNP-vekst", "sub": "Bedriftssektor-utlån vokser med økonomien", "impact": "pos"},
        {"text": "Regulatorisk kapitalkrav", "sub": "Basel IV og systemrisikopåslag", "impact": "neg"},
        {"text": "Arbeidsledighet", "sub": "Lav ledighet = lave kredittap", "impact": "pos"},
    ],
    "MOWI": [
        {"text": "Lakseprisen (spot)", "sub": "Over 80 NOK/kg gir rekordmarginer", "impact": "pos"},
        {"text": "Grunnrenteskatt", "sub": "25% effektiv skatt reduserer netto resultat strukturelt", "impact": "neg"},
        {"text": "Eksport til Kina/USA", "sub": "To av tre viktigste markeder — volumfølsomme", "impact": "neu"},
        {"text": "Fôrkostnader", "sub": "Soya og fiskemel — utgjør ca 40% av kostnadene", "impact": "neg"},
        {"text": "EUR/NOK valutakurs", "sub": "Mesteparten av salget skjer i EUR og USD", "impact": "pos"},
    ],
    "AKRBP": [
        {"text": "Brent oljepris", "sub": "Break-even under $30/fat — svært robust", "impact": "pos"},
        {"text": "Petroleumsbeskatning", "sub": "78% marginalskatt — felles risiko med EQNR", "impact": "neg"},
        {"text": "USD/NOK kurs", "sub": "Inntekter i USD, investeringer delvis i NOK", "impact": "pos"},
        {"text": "Offshore riggtilgang", "sub": "Begrenset tilgang øker kostnader for Yggdrasil", "impact": "neg"},
        {"text": "Klimapolitikk (EU)", "sub": "Kan påvirke markedstilgang for norsk olje/gass", "impact": "neu"},
    ],
}

COMPANY_FACTORS = {
    "EQNR": [
        {"text": "Produksjon på norsk sokkel", "sub": "Johan Sverdrup-feltet står for ~40% av norsk produksjon", "impact": "pos"},
        {"text": "Ledig kapasitet på Troll", "sub": "Tillater fleksibel gassproduksjon etter pris", "impact": "pos"},
        {"text": "Fornybar-satsing (Hywind)", "sub": "Flyttende havvind — langsiktig vekstområde", "impact": "pos"},
        {"text": "Utbyttepolitikk", "sub": "Forpliktet til økende utbytte gjennom syklusen", "impact": "pos"},
        {"text": "Reservereplasement", "sub": "Må finne nye reserver for å opprettholde produksjon", "impact": "neg"},
    ],
    "DNB": [
        {"text": "Nettorentemargin (NIM)", "sub": "Over 1,95% i Q1 — historisk høyt", "impact": "pos"},
        {"text": "Kredittaps-rate", "sub": "Bare 0,08% — indikerer god kvalitet i porteføljen", "impact": "pos"},
        {"text": "Digital satsing (Vipps)", "sub": "DNB eier 47% av Vipps MobilePay", "impact": "pos"},
        {"text": "Kapitaldekning (CET1)", "sub": "18,3% gir stor utbyttekapasitet", "impact": "pos"},
        {"text": "Aktiv M&A-strategi", "sub": "Nylig oppkjøp av Carnegie styrker meglervirksomheten", "impact": "pos"},
    ],
    "MOWI": [
        {"text": "Biologisk produktivitet", "sub": "Dødelighet og tilvekst i sjøfasen avgjør volum", "impact": "pos"},
        {"text": "MAB-kapasitet", "sub": "Maksimalt tillatt biomasse avgjør produksjonstak", "impact": "neu"},
        {"text": "Vertikal integrasjon", "sub": "Eier kjede fra rogn til foredlet produkt", "impact": "pos"},
        {"text": "Sykdoms- og lakselusrisiko", "sub": "ISA og PD kan utløse nedslaktinger", "impact": "neg"},
        {"text": "Investering i landbasert oppdrett", "sub": "Langsiktig bet på produksjon utenfor sjø", "impact": "neu"},
    ],
    "AKRBP": [
        {"text": "Johan Sverdrup-bidrag", "sub": "Ca 70% av produksjonen, verdens billigste olje", "impact": "pos"},
        {"text": "Yggdrasil-prosjektet", "sub": "Oppstart 2027 — legger til 55 000 fat/dag", "impact": "pos"},
        {"text": "Produksjonskostnader", "sub": "Under $10/fat — laveste i sektoren", "impact": "pos"},
        {"text": "Utbyttepolitikk", "sub": "Forpliktet til kvartalsutbytte på $0,60 per aksje", "impact": "pos"},
        {"text": "Hod og Valhall oppgradering", "sub": "Forlenger levetiden av viktige felter", "impact": "pos"},
    ],
}

COMPETITORS = {
    "EQNR": [
        {"name": "Equinor (du)", "ticker": "EQNR", "mcap": "892 mrd", "pe": "7,4x", "div": "8,2%", "roe": "22,1%", "year": "+18%", "rec": "Overvekt"},
        {"name": "Shell", "ticker": "SHEL", "mcap": "2 100 mrd", "pe": "8,1x", "div": "4,5%", "roe": "16,8%", "year": "+12%", "rec": "Nøytral"},
        {"name": "BP", "ticker": "BP", "mcap": "1 100 mrd", "pe": "7,8x", "div": "5,3%", "roe": "14,2%", "year": "+8%", "rec": "Nøytral"},
        {"name": "Aker BP", "ticker": "AKRBP", "mcap": "161 mrd", "pe": "6,9x", "div": "9,1%", "roe": "24,3%", "year": "+22%", "rec": "Overvekt"},
        {"name": "TotalEnergies", "ticker": "TTE", "mcap": "1 500 mrd", "pe": "7,2x", "div": "5,8%", "roe": "19,5%", "year": "+15%", "rec": "Overvekt"},
    ],
    "DNB": [
        {"name": "DNB Bank (du)", "ticker": "DNB", "mcap": "345 mrd", "pe": "9,2x", "div": "5,8%", "roe": "15,2%", "year": "+22%", "rec": "Overvekt"},
        {"name": "Nordea Bank", "ticker": "NDA", "mcap": "420 mrd", "pe": "8,6x", "div": "6,1%", "roe": "14,8%", "year": "+15%", "rec": "Overvekt"},
        {"name": "Swedbank", "ticker": "SWED-A", "mcap": "280 mrd", "pe": "7,9x", "div": "7,2%", "roe": "16,1%", "year": "+18%", "rec": "Overvekt"},
        {"name": "SpareBank 1 SR", "ticker": "SRBNK", "mcap": "42 mrd", "pe": "8,4x", "div": "5,4%", "roe": "13,2%", "year": "+9%", "rec": "Nøytral"},
        {"name": "SEB", "ticker": "SEB-A", "mcap": "310 mrd", "pe": "9,1x", "div": "6,3%", "roe": "15,5%", "year": "+12%", "rec": "Nøytral"},
    ],
    "MOWI": [
        {"name": "Mowi (du)", "ticker": "MOWI", "mcap": "98 mrd", "pe": "14,2x", "div": "3,4%", "roe": "12,8%", "year": "−8%", "rec": "Nøytral"},
        {"name": "SalMar", "ticker": "SALM", "mcap": "71 mrd", "pe": "15,1x", "div": "2,8%", "roe": "11,4%", "year": "−12%", "rec": "Nøytral"},
        {"name": "Lerøy Seafood", "ticker": "LSG", "mcap": "28 mrd", "pe": "12,8x", "div": "4,1%", "roe": "10,2%", "year": "−5%", "rec": "Nøytral"},
        {"name": "Grieg Seafood", "ticker": "GSF", "mcap": "9 mrd", "pe": "13,5x", "div": "3,2%", "roe": "8,9%", "year": "−18%", "rec": "Undervekt"},
        {"name": "Bakkafrost", "ticker": "BAKKA", "mcap": "42 mrd", "pe": "16,3x", "div": "2,1%", "roe": "13,5%", "year": "+2%", "rec": "Nøytral"},
    ],
    "AKRBP": [
        {"name": "Aker BP (du)", "ticker": "AKRBP", "mcap": "161 mrd", "pe": "6,9x", "div": "9,1%", "roe": "24,3%", "year": "+22%", "rec": "Overvekt"},
        {"name": "Equinor", "ticker": "EQNR", "mcap": "892 mrd", "pe": "7,4x", "div": "8,2%", "roe": "22,1%", "year": "+18%", "rec": "Overvekt"},
        {"name": "Var Energi", "ticker": "VAR", "mcap": "80 mrd", "pe": "7,2x", "div": "11,2%", "roe": "26,5%", "year": "+14%", "rec": "Overvekt"},
        {"name": "DNO", "ticker": "DNO", "mcap": "12 mrd", "pe": "5,8x", "div": "7,8%", "roe": "19,2%", "year": "−3%", "rec": "Nøytral"},
        {"name": "OKEA", "ticker": "OKEA", "mcap": "3 mrd", "pe": "4,2x", "div": "14,5%", "roe": "32,1%", "year": "−8%", "rec": "Nøytral"},
    ],
}
