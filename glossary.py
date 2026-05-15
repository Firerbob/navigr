"""
Ordbok for Navigr - aksje-begreper forklart på vanlig norsk.

Fire nivåer:
- basic: Helt enkelt (grunnbegreper)
- med: Litt mer (nøkkeltall)
- adv: For de nysgjerrige (avansert)
- idiom: Uttrykk og slang
"""

GLOSSARY = {
    # ============================================
    # HELT ENKELT (basic)
    # ============================================
    "aksje": {
        "name": "Aksje",
        "pron": "/akˈsjeː/",
        "level": "basic",
        "short": "En liten bit av et selskap.",
        "def": "En aksje er en eierandel i et selskap. Eier du én aksje i Equinor, eier du en bittebitte del av hele selskapet. Hvis selskapet går bra, kan aksjen din bli mer verdt. Hvis det går dårlig, kan den bli mindre verdt.",
        "example": "Min mor kjøpte 10 aksjer i Telenor på 90-tallet — i dag er de verdt mer enn det dobbelte.",
        "related": ["utbytte", "bors", "mcap"],
    },
    "bors": {
        "name": "Børs",
        "pron": "/bœʂ/",
        "level": "basic",
        "short": "Markedet hvor aksjer kjøpes og selges.",
        "def": "Oslo Børs er Norges hovedbørs — en digital markedsplass hvor alle selskaper som er \"børsnotert\" handles. Alt skjer elektronisk, det er ingen som lenger sitter i en sirkel og roper. Børsen åpner kl 09:00 og stenger kl 16:25 på hverdager.",
        "example": "Selskaper på Oslo Børs må følge strenge regler for åpenhet og rapportering.",
        "related": ["aksje", "osebx", "ticker"],
    },
    "utbytte": {
        "name": "Utbytte",
        "pron": "/ˈʉːtbʏtə/",
        "level": "basic",
        "short": "Pengene et selskap deler ut til eierne sine.",
        "def": "Når et selskap tjener penger, kan de velge å beholde pengene eller dele ut til aksjeeierne. Det de deler ut kalles utbytte. Du kan tenke på det som leieinntekt fra aksjen — uten at du må reparere noe vannrør.",
        "example": "DNB betalte 5,80 kr i utbytte per aksje i fjor. Har du 100 aksjer, fikk du 580 kr.",
        "tip": "Et høyt utbytte er ikke alltid bra — det kan bety at selskapet ikke har vekstmuligheter å investere i.",
        "related": ["aksje", "eps", "kontantstrom"],
    },
    "osebx": {
        "name": "OSEBX",
        "pron": "/oː-eː-es-be-iks/",
        "level": "basic",
        "short": "Hovedindeksen på Oslo Børs.",
        "def": "OSEBX er en samling av de mest omsatte aksjene på Oslo Børs, vektet etter størrelse. Når noen sier \"børsen gikk opp i dag\", mener de oftest OSEBX. Det er som en temperaturmåler for hele det norske aksjemarkedet.",
        "example": "OSEBX endte opp 0,4 % i dag — drevet av sterke oljepriser.",
        "related": ["bors", "aksje", "sektor"],
    },
    "ticker": {
        "name": "Ticker",
        "pron": "/ˈtɪkər/",
        "level": "basic",
        "short": "Selskapets forkortelse på børsen.",
        "def": "Hver børsnotert aksje har et kort kallenavn — kalt en ticker — som brukes når du handler eller leser om selskapet. Det er som et nummerskilt, men for aksjer.",
        "example": "Equinors ticker er EQNR, Mowis er MOWI, DNBs er DNB.",
        "related": ["aksje", "bors"],
    },
    "sektor": {
        "name": "Sektor",
        "pron": "/sɛkˈtoːr/",
        "level": "basic",
        "short": "Bransjen et selskap tilhører.",
        "def": "Selskaper grupperes i sektorer basert på hva de driver med. Energi, finans, sjømat, teknologi og industri er eksempler. Selskaper i samme sektor påvirkes ofte av de samme tingene — for eksempel olje for energisektoren.",
        "example": "Equinor og Aker BP er i samme sektor (energi), og påvirkes begge av oljeprisen.",
        "related": ["osebx", "bors"],
    },

    # ============================================
    # LITT MER (med)
    # ============================================
    "pe": {
        "name": "P/E",
        "pron": "/peː eː/",
        "level": "med",
        "short": "Hvor mange år med dagens overskudd du betaler for én aksje.",
        "def": "P/E står for \"Price to Earnings\". Tallet viser hvor dyrt selskapet er priset i forhold til hvor mye det tjener. Lavt P/E (under 10) betyr ofte at aksjen er billig. Høyt P/E (over 25) betyr at investorer forventer mye vekst.",
        "example": "Equinor har P/E på 7,4 — relativt billig. Tech-selskaper kan ha P/E på 50 eller mer.",
        "tip": "Lavt P/E er ikke alltid bra — det kan også bety at markedet ikke tror på selskapet.",
        "related": ["pb", "eps", "nettoresultat"],
    },
    "pb": {
        "name": "P/B",
        "pron": "/peː beː/",
        "level": "med",
        "short": "Hvor mye du betaler for én krone av selskapets eiendeler.",
        "def": "P/B står for \"Price to Book\". Det viser om aksjen handles dyrere eller billigere enn selskapets bokførte verdier (alt selskapet eier minus alt det skylder). P/B på 1 betyr at du betaler nøyaktig den bokførte verdien. P/B på 2 betyr at du betaler dobbelt.",
        "example": "Banker har ofte lav P/B (rundt 1,4x) fordi de har mye eiendeler. Tech-selskaper har høy P/B fordi mye av verdien er ideer.",
        "related": ["pe", "mcap"],
    },
    "mcap": {
        "name": "Markedsverdi",
        "pron": "",
        "level": "med",
        "short": "Hva hele selskapet er verdt på børsen akkurat nå.",
        "def": "Markedsverdi (også kalt \"børsverdi\" eller på engelsk \"market cap\") er antall aksjer ganger dagens kurs. Det viser hvor stort selskapet er. Equinor er Norges største børsnoterte selskap fordi det har høyest markedsverdi.",
        "example": "Hvis et selskap har 100 millioner aksjer som koster 200 kr stykket, er markedsverdien 20 milliarder kr.",
        "related": ["aksje", "pe", "pb"],
    },
    "roe": {
        "name": "ROE",
        "pron": "/eː o eː/",
        "level": "med",
        "short": "Hvor effektivt selskapet bruker eiernes penger.",
        "def": "ROE står for \"Return on Equity\" — avkastning på egenkapital. Tallet viser hvor mye selskapet tjener for hver krone eierne har skutt inn. Høy ROE (over 15 %) er bra. Det betyr at selskapet er flinkt til å skape verdi.",
        "example": "Equinor har ROE på 22 % — selskapet tjener 22 øre for hver krone eierne har plassert i det.",
        "tip": "Sammenlign alltid ROE innen samme sektor. Banker har lavere ROE enn programvareselskaper.",
        "related": ["nettoresultat", "pe", "gjeldsgrad"],
    },
    "ebitda": {
        "name": "EBITDA",
        "pron": "/eˈbitda/",
        "level": "med",
        "short": "Selskapets resultat før skatt, renter og avskrivninger.",
        "def": "EBITDA er resultatet selskapet leverer fra driften, før du trekker fra skatt, rentekostnader, og slitasje på utstyr. Det er et \"rent\" mål på om driften går bra, uten at regnskapsregler og finansieringskostnader rotes inn.",
        "example": "Equinor leverte EBITDA på 10,8 milliarder USD i Q4 — selve driften gir massive penger.",
        "tip": "EBITDA viser om kjernevirksomheten er sunn, men sier ikke om selskapet faktisk er lønnsomt etter alle kostnader.",
        "related": ["evebitda", "nettoresultat", "omsetning"],
    },
    "evebitda": {
        "name": "EV/EBITDA",
        "pron": "/iː viː/",
        "level": "med",
        "short": "Hvor dyrt selskapet er priset i forhold til driftsinntjeningen.",
        "def": "EV/EBITDA sammenligner hele selskapets verdi (inkludert gjeld) med hva driften tjener. Lavt tall = billig. Det brukes mye for å sammenligne selskaper på tvers av sektorer fordi det \"renser bort\" forskjeller i gjeld og skatteregler.",
        "example": "Equinor handler på EV/EBITDA 3,2x — lavt, og indikerer attraktiv prising.",
        "related": ["ebitda", "pe", "mcap"],
    },
    "gjeldsgrad": {
        "name": "Gjeldsgrad",
        "pron": "",
        "level": "med",
        "short": "Hvor mye gjeld selskapet har i forhold til egenkapital.",
        "def": "Gjeldsgrad viser hvor mye selskapet har lånt sammenlignet med eiernes penger. Lav gjeldsgrad er trygt — selskapet kan tåle dårlige tider. Høy gjeldsgrad gir høyere risiko, men kan gi bedre avkastning når det går bra.",
        "example": "Banker har naturlig høy gjeldsgrad (de er bygget rundt utlån). Tech-selskaper har gjerne lav.",
        "related": ["roe", "pb"],
    },
    "eps": {
        "name": "EPS",
        "pron": "/eː peː es/",
        "level": "med",
        "short": "Hvor mye selskapet tjener per aksje.",
        "def": "EPS står for \"Earnings Per Share\". Det er selskapets overskudd delt på antall aksjer. Tallet viser hvor mye av overskuddet som tilhører hver enkelt aksje du eier. Brukes mye for å sammenligne selskaper og se utvikling over tid.",
        "example": "Equinor hadde EPS på 0,68 USD i Q4 — det betyr 0,68 USD overskudd per aksje.",
        "related": ["nettoresultat", "pe", "utbytte"],
    },
    "omsetning": {
        "name": "Omsetning",
        "pron": "",
        "level": "med",
        "short": "Hvor mye selskapet har solgt for.",
        "def": "Omsetning er totalsummen av alt selskapet har solgt i en periode, før noen kostnader er trukket fra. Det kalles også \"inntekter\" eller \"topplinjen\" — fordi det står øverst i resultatregnskapet.",
        "example": "Equinor hadde omsetning på 24,3 milliarder USD i Q4 — hva de solgte olje, gass og produkter for.",
        "tip": "Stor omsetning betyr ikke nødvendigvis at selskapet tjener penger. Du må trekke fra alle kostnadene først.",
        "related": ["ebitda", "nettoresultat"],
    },
    "nettoresultat": {
        "name": "Nettoresultat",
        "pron": "",
        "level": "med",
        "short": "Det selskapet sitter igjen med etter alle kostnader.",
        "def": "Nettoresultat er det \"rene\" overskuddet — etter at alt er trukket fra: kostnader, renter, skatt, og slitasje. Det er disse pengene som faktisk kan brukes til utbytte, investeringer eller spares.",
        "example": "Equinor hadde nettoresultat på 2,1 milliarder USD i Q4 — pengene som faktisk var igjen.",
        "related": ["ebitda", "eps", "omsetning"],
    },
    "kontantstrom": {
        "name": "Fri kontantstrøm",
        "pron": "",
        "level": "med",
        "short": "Penger selskapet har til overs etter alle nødvendige investeringer.",
        "def": "Fri kontantstrøm er ekte penger selskapet har generert, etter at alle investeringer er gjort. Det er pengene som faktisk kan brukes til utbytte, nedbetaling av gjeld eller oppkjøp. Mange profesjonelle mener dette er det viktigste tallet å se på.",
        "example": "Equinor genererte 4,2 milliarder USD i fri kontantstrøm — derfor kan de betale så høyt utbytte.",
        "related": ["ebitda", "utbytte", "nettoresultat"],
    },
    "konsensus": {
        "name": "Konsensus",
        "pron": "/konsɛnˈsʉs/",
        "level": "med",
        "short": "Snittet av hva analytikere forventer.",
        "def": "Konsensus er gjennomsnittet av alle analytikernes prognoser for et selskap. Når et selskap \"slår konsensus\", betyr det at de leverte bedre tall enn forventet — og det fører ofte til at aksjen stiger.",
        "example": "Equinor slo konsensus med 12 % — overskuddet var 12 % høyere enn analytikere ventet.",
        "tip": "Det er ikke alltid sant at \"bedre enn konsensus\" er bra. Hvis forventningene var lave til å begynne med, kan selskapet egentlig levere svake tall.",
        "related": ["eps", "nettoresultat"],
    },
    "volatilitet": {
        "name": "Volatilitet",
        "pron": "/voːlatiliˈteːt/",
        "level": "med",
        "short": "Hvor mye en aksje hopper opp og ned.",
        "def": "Volatilitet måler hvor uforutsigbar prisen på en aksje er. Høy volatilitet er som rusjekjøring — spennende, men ikke for de som blir kvalme. Lav volatilitet er som bobiltur — kjedelig, men forutsigbart.",
        "example": "Bitcoin har høy volatilitet. Statsobligasjoner har lav volatilitet. Tech-aksjer er imellom.",
        "related": ["beta"],
    },

    # ============================================
    # FOR DE NYSGJERRIGE (adv)
    # ============================================
    "beta": {
        "name": "Beta",
        "pron": "/ˈbeːta/",
        "level": "adv",
        "short": "Hvor mye en aksje beveger seg sammenlignet med markedet.",
        "def": "Beta måler aksjens følsomhet for markedet. Beta 1 betyr at aksjen beveger seg likt med markedet. Beta 1,5 betyr at den beveger seg 50 % mer enn markedet (både opp og ned). Beta 0,5 betyr halvparten — roligere.",
        "example": "Telenor har lav beta (rundt 0,7) — den beveger seg mindre enn markedssnittet.",
        "related": ["volatilitet"],
    },
    "shorte": {
        "name": "Å shorte",
        "pron": "/ʃoːrte/",
        "level": "adv",
        "short": "Å satse på at en aksje skal falle.",
        "def": "Å shorte er en teknikk hvor du tjener penger hvis aksjen synker. Du låner aksjer, selger dem, og håper å kjøpe dem tilbake billigere. Hvis du har rett, beholder du differansen. Hvis du tar feil, kan tapet være ubegrenset — fordi en aksje kan stige uendelig.",
        "example": "Hedgefondet shortet Tesla og tapte 1 milliard dollar da aksjen fortsatte å stige.",
        "tip": "Shorting er for proffe — for nybegynnere er det best å holde seg unna. Tapene kan bli større enn investeringen.",
        "related": ["bull_bear", "volatilitet"],
    },
    "innsidehandel": {
        "name": "Innsidehandel",
        "pron": "",
        "level": "adv",
        "short": "Når ledelsen kjøper eller selger egne aksjer.",
        "def": "Når toppledere i et selskap kjøper eller selger aksjer i sitt eget selskap, kalles det innsidehandel. Dette må alltid meldes til børsen og er offentlig. Mange investorer følger med på dette fordi ledelsen ofte vet mer enn andre.",
        "example": "CEO i DNB kjøpte 10 000 aksjer i går — et signal på at hun har tro på selskapet.",
        "related": ["aksje"],
    },
    "golden_cross": {
        "name": "Golden Cross",
        "pron": "/ˈgoʊldən krɔs/",
        "level": "adv",
        "short": "Et positivt teknisk signal i en graf.",
        "def": "Golden Cross oppstår når et kortere gjennomsnitt (typisk 50 dagers snitt) krysser oppover gjennom et lengre gjennomsnitt (typisk 200 dagers snitt). Det tolkes som et tegn på styrket trend — at oppturen kan fortsette.",
        "example": "Equinor fikk Golden Cross 23. januar, og aksjen har steget jevnt siden da.",
        "related": ["volatilitet"],
    },
    "konsesjon": {
        "name": "Konsesjon",
        "pron": "/konseˈsjoːn/",
        "level": "adv",
        "short": "Offentlig tillatelse til å drive en virksomhet.",
        "def": "En konsesjon er en lisens fra myndighetene som gir et selskap rett til å drive en spesifikk aktivitet — for eksempel å produsere olje, drive bank eller selge alkohol. Konsesjoner er viktige fordi de begrenser hvem som kan operere i markedet.",
        "example": "Aker BP fikk konsesjon for Yggdrasil-feltet etter mange års saksbehandling.",
        "related": [],
    },

    # ============================================
    # UTTRYKK OG SLANG (idiom)
    # ============================================
    "bull_bear": {
        "name": "Bull og bear",
        "pron": "/bʊl/ /bɛr/",
        "level": "idiom",
        "short": "Optimist eller pessimist om markedet.",
        "def": "En \"bull\" tror markedet skal opp (som en okse som stanger oppover). En \"bear\" tror markedet skal ned (som en bjørn som slår nedover). \"Bull market\" = oppgangsmarked. \"Bear market\" = nedgangsmarked på 20 % eller mer.",
        "example": "Hun er bull på Equinor — hun tror den skal stige videre. Han er bear på laks akkurat nå.",
        "related": ["shorte", "korreksjon"],
    },
    "falling_knife": {
        "name": "Never catch a falling knife",
        "pron": "",
        "level": "idiom",
        "short": "Ikke kjøp en aksje som er i kraftig fall — du kan kutte deg.",
        "def": "Et populært uttrykk som advarer mot å kjøpe en aksje bare fordi den har falt mye. Aksjen kan fortsette å falle, og du kan tape mer. Bedre å vente til den stabiliserer seg før du kjøper. Som å vente til kniven har truffet bakken før du plukker den opp.",
        "example": "Aksjen falt 30 % i dag — men ikke fang kniven, vent til vi vet at bunnen er nådd.",
        "tip": "Det er nesten umulig å treffe bunnen. Bedre å gå glipp av de første 10 % av en oppgang enn å risikere å tape 40 % på vei ned.",
        "related": ["korreksjon", "volatilitet"],
    },
    "korreksjon": {
        "name": "Korreksjon",
        "pron": "/korɛkˈsjoːn/",
        "level": "idiom",
        "short": "Et fall på 10-20 % i en aksje eller marked.",
        "def": "En korreksjon er når markedet eller en aksje faller mer enn 10 % fra toppen. Det er normalt og skjer regelmessig — som regel én gang i året. Det er ikke en krise, men en \"pause\" i oppgangen.",
        "example": "Etter mange måneder med oppgang kom en korreksjon på 12 % — helt normalt.",
        "related": ["bull_bear", "volatilitet", "falling_knife"],
    },
    "blue_chip": {
        "name": "Blue chip",
        "pron": "",
        "level": "idiom",
        "short": "Store, etablerte, trygge selskaper.",
        "def": "Blue chip-selskaper er de største og mest stabile aksjene på børsen — som Equinor, DNB og Telenor på Oslo Børs. Navnet kommer fra poker, hvor blå chips er mest verdt. De gir sjelden eksplosiv vekst, men er mer forutsigbare.",
        "example": "Hun investerer kun i blue chips fordi hun vil sove godt om natten.",
        "related": ["mcap", "utbytte"],
    },
    "fomo": {
        "name": "FOMO",
        "pron": "/ˈfoʊmoʊ/",
        "level": "idiom",
        "short": "Frykten for å gå glipp av en mulighet.",
        "def": "FOMO står for \"Fear Of Missing Out\" — frykten for å gå glipp av noe. I aksjer er det den følelsen du får når en aksje stiger raskt og du ikke har kjøpt. FOMO får mange til å kjøpe på toppen — som ofte er feilen.",
        "example": "Etter at alle vennene tjente penger på krypto, kjøpte han i FOMO — like før det krasjet.",
        "tip": "FOMO er en av de farligste følelsene i aksjeverden. Hvis du føler FOMO, vent et par dager før du gjør noe.",
        "related": ["volatilitet", "falling_knife"],
    },
    "diversifisering": {
        "name": "Diversifisering",
        "pron": "/divɛrsifisɛˈriŋ/",
        "level": "idiom",
        "short": "Ikke legg alle eggene i én kurv.",
        "def": "Å diversifisere betyr å spre investeringene dine på mange forskjellige selskaper, sektorer og land. Hvis ett selskap går dårlig, kan andre gå bra. Det reduserer risikoen — det er den eneste \"gratis-lunsjen\" i finansverden.",
        "example": "Med 10-15 ulike aksjer i forskjellige sektorer har hun en godt diversifisert portefølje.",
        "related": ["volatilitet", "sektor"],
    },
    "diamond_hands": {
        "name": "Diamond hands 💎",
        "pron": "",
        "level": "idiom",
        "short": "Å holde på aksjer uansett hva som skjer.",
        "def": "Et internett-uttrykk som beskriver investorer som holder på aksjene sine selv når prisen faller mye. Hender av diamant — så sterke at de ikke gir slipp. Det motsatte er \"paper hands\" — papir-hender som slipper ved første motgang.",
        "example": "Hun har diamond hands på Tesla — har holdt aksjen gjennom 50 % fall.",
        "tip": "Det er bra å være langsiktig, men ikke forveksle stahet med strategi. Noen ganger er det riktig å selge.",
        "related": ["fomo", "bull_bear"],
    },
    "ipo": {
        "name": "IPO",
        "pron": "/aɪ piː oʊ/",
        "level": "idiom",
        "short": "Når et selskap blir børsnotert for første gang.",
        "def": "IPO står for \"Initial Public Offering\" — første gangs aksjesalg til publikum. Det er da selskapet går fra å være privateid til å handles på børsen, og hvem som helst kan kjøpe aksjer. IPO-er blir ofte mye omtalt og kan være spennende.",
        "example": "Spotify gjorde IPO i 2018 — det var en av de største børsnoteringene det året.",
        "tip": "Mange IPO-aksjer faller etter første handelsdag. Det er ofte tryggere å vente noen måneder før du kjøper.",
        "related": ["aksje", "bors"],
    },
    "buyback": {
        "name": "Tilbakekjøp (buyback)",
        "pron": "",
        "level": "idiom",
        "short": "Når et selskap kjøper egne aksjer.",
        "def": "Når et selskap har overskudd, kan de bruke pengene til å kjøpe tilbake sine egne aksjer fra markedet. Da blir det færre aksjer totalt, og hver gjenværende aksje blir mer verdt. Det er en måte å gi penger tilbake til eierne på, alternativt til utbytte.",
        "example": "DNB kjøpte tilbake 1 % av sine egne aksjer i fjor — eierne sitter nå med en større andel av selskapet.",
        "related": ["utbytte", "aksje"],
    },
}


LEVEL_LABELS = {
    "basic": "Helt enkelt",
    "med": "Litt mer",
    "adv": "For de nysgjerrige",
    "idiom": "Uttrykk og slang",
}

LEVEL_COLORS = {
    "basic": ("#DDE5D2", "#4F6244"),   # terra-soft, terra-2
    "med": ("#F5E8D0", "#6B5B2C"),     # honey-soft, neutral
    "adv": ("#F4E5E2", "#C4847C"),     # rose-soft, rose
    "idiom": ("#E8E5F4", "#5A4A8C"),   # lilla-soft, lilla
}


def search_terms(query: str = "", level: str = "all") -> list:
    """Søker i ordboken og returnerer matchende termer.

    Args:
        query: Søketekst (tom = ingen filter)
        level: Filter etter nivå ("all", "basic", "med", "adv", "idiom")

    Returns:
        Liste med (key, term_dict) tupler
    """
    results = []
    query_lower = query.lower().strip()

    for key, term in GLOSSARY.items():
        # Filter på nivå
        if level != "all" and term["level"] != level:
            continue

        # Filter på søketekst
        if query_lower:
            haystack = (
                term["name"].lower() + " " +
                term["short"].lower() + " " +
                term["def"].lower()
            )
            if query_lower not in haystack:
                continue

        results.append((key, term))

    return results


def get_term(key: str) -> dict | None:
    """Henter en spesifikk term fra ordboken."""
    return GLOSSARY.get(key)
