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
        "name": "Aktie",
        "pron": "/akˈsjeː/",
        "level": "basic",
        "short": "En liten del av ett bolag.",
        "def": "En aktie är en ägarandel i ett bolag. Äger du en aktie i Equinor, äger du en pytteliten del av hela bolaget. Om bolaget går bra kan din aktie bli mer värd. Om det går dåligt kan den bli mindre värd.",
        "example": "Min mamma köpte 10 aktier i Telenor på 90-talet — idag är de värda mer än dubbelt så mycket.",
        "related": ["utbytte", "bors", "mcap"],
    },
    "bors": {
        "name": "Börs",
        "pron": "/bœʂ/",
        "level": "basic",
        "short": "Marknaden där aktier köps och säljs.",
        "def": "Oslo Børs är Norges huvudbörs — en digital marknadsplats där alla bolag som är \"börsnoterade\" handlas. Allt sker elektroniskt, det är ingen som längre sitter i en ring och ropar. Börsen öppnar kl 09:00 och stänger kl 16:25 på vardagar.",
        "example": "Bolag på Oslo Børs måste följa strikta regler om öppenhet och rapportering.",
        "related": ["aksje", "osebx", "ticker"],
    },
    "utbytte": {
        "name": "Utdelning",
        "pron": "/ˈʉːtbʏtə/",
        "level": "basic",
        "short": "Pengarna ett bolag delar ut till sina ägare.",
        "def": "När ett bolag tjänar pengar kan de välja att behålla dem eller dela ut dem till aktieägarna. Det de delar ut kallas utdelning. Du kan tänka på det som hyresintäkter från aktien — utan att du behöver laga något vattenrör.",
        "example": "DNB betalade 5,80 kr i utdelning per aktie förra året. Har du 100 aktier fick du 580 kr.",
        "tip": "En hög utdelning är inte alltid bra — det kan betyda att bolaget saknar tillväxtmöjligheter att investera i.",
        "related": ["aksje", "eps", "kontantstrom"],
    },
    "osebx": {
        "name": "OSEBX",
        "pron": "/oː-eː-es-be-iks/",
        "level": "basic",
        "short": "Huvudindexet på Oslo Børs.",
        "def": "OSEBX är en samling av de mest omsatta aktierna på Oslo Børs, viktade efter storlek. När någon säger \"börsen gick upp idag\" menar de oftast OSEBX. Det är som en termometer för hela den norska aktiemarknaden.",
        "example": "OSEBX slutade upp 0,4 % idag — drivet av starka oljepriser.",
        "related": ["bors", "aksje", "sektor"],
    },
    "ticker": {
        "name": "Ticker",
        "pron": "/ˈtɪkər/",
        "level": "basic",
        "short": "Bolagets förkortning på börsen.",
        "def": "Varje börsnoterad aktie har ett kort smeknamn — kallat en ticker — som används när du handlar eller läser om bolaget. Det är som en registreringsskylt, men för aktier.",
        "example": "Equinors ticker är EQNR, Mowis är MOWI, DNBs är DNB.",
        "related": ["aksje", "bors"],
    },
    "sektor": {
        "name": "Sektor",
        "pron": "/sɛkˈtoːr/",
        "level": "basic",
        "short": "Branschen ett bolag tillhör.",
        "def": "Bolag grupperas i sektorer baserat på vad de sysslar med. Energi, finans, sjömat, teknik och industri är exempel. Bolag i samma sektor påverkas ofta av samma saker — till exempel olja för energisektorn.",
        "example": "Equinor och Aker BP är i samma sektor (energi) och påverkas båda av oljepriset.",
        "related": ["osebx", "bors"],
    },

    # ============================================
    # LITT MER (med)
    # ============================================
    "pe": {
        "name": "P/E",
        "pron": "/peː eː/",
        "level": "med",
        "short": "Hur många år med dagens vinst du betalar för en aktie.",
        "def": "P/E står för \"Price to Earnings\". Talet visar hur dyrt bolaget är prissatt i förhållande till hur mycket det tjänar. Lågt P/E (under 10) betyder ofta att aktien är billig. Högt P/E (över 25) betyder att investerare förväntar sig hög tillväxt.",
        "example": "Equinor har P/E på 7,4 — relativt billigt. Teknikbolag kan ha P/E på 50 eller mer.",
        "tip": "Lågt P/E är inte alltid bra — det kan också betyda att marknaden inte tror på bolaget.",
        "related": ["pb", "eps", "nettoresultat"],
    },
    "pb": {
        "name": "P/B",
        "pron": "/peː beː/",
        "level": "med",
        "short": "Hur mycket du betalar för en krona av bolagets tillgångar.",
        "def": "P/B står för \"Price to Book\". Det visar om aktien handlas dyrare eller billigare än bolagets bokförda värden (allt bolaget äger minus allt det är skyldigt). P/B på 1 betyder att du betalar exakt det bokförda värdet. P/B på 2 betyder att du betalar dubbelt.",
        "example": "Banker har ofta lågt P/B (runt 1,4x) eftersom de har många tillgångar. Teknikbolag har högt P/B eftersom mycket av värdet är idéer.",
        "related": ["pe", "mcap"],
    },
    "mcap": {
        "name": "Marknadsvärde",
        "pron": "",
        "level": "med",
        "short": "Vad hela bolaget är värt på börsen just nu.",
        "def": "Marknadsvärde (också kallat \"börsvärde\" eller på engelska \"market cap\") är antal aktier gånger dagens kurs. Det visar hur stort bolaget är. Equinor är Norges största börsnoterade bolag eftersom det har högst marknadsvärde.",
        "example": "Om ett bolag har 100 miljoner aktier som kostar 200 kr styck är marknadsvärdet 20 miljarder kr.",
        "related": ["aksje", "pe", "pb"],
    },
    "roe": {
        "name": "ROE",
        "pron": "/eː o eː/",
        "level": "med",
        "short": "Hur effektivt bolaget använder ägarnas pengar.",
        "def": "ROE står för \"Return on Equity\" — avkastning på eget kapital. Talet visar hur mycket bolaget tjänar för varje krona ägarna har skjutit in. Hög ROE (över 15 %) är bra. Det betyder att bolaget är duktigt på att skapa värde.",
        "example": "Equinor har ROE på 22 % — bolaget tjänar 22 öre för varje krona ägarna har placerat i det.",
        "tip": "Jämför alltid ROE inom samma sektor. Banker har lägre ROE än programvarubolag.",
        "related": ["nettoresultat", "pe", "gjeldsgrad"],
    },
    "ebitda": {
        "name": "EBITDA",
        "pron": "/eˈbitda/",
        "level": "med",
        "short": "Bolagets resultat före skatt, räntor och avskrivningar.",
        "def": "EBITDA är resultatet bolaget levererar från driften, innan du drar av skatt, räntekostnader och slitage på utrustning. Det är ett \"rent\" mått på om driften går bra, utan att redovisningsregler och finansieringskostnader blandas in.",
        "example": "Equinor levererade EBITDA på 10,8 miljarder USD i Q4 — själva driften genererar enorma pengar.",
        "tip": "EBITDA visar om kärnverksamheten är sund, men säger inte om bolaget faktiskt är lönsamt efter alla kostnader.",
        "related": ["evebitda", "nettoresultat", "omsetning"],
    },
    "evebitda": {
        "name": "EV/EBITDA",
        "pron": "/iː viː/",
        "level": "med",
        "short": "Hur dyrt bolaget är prissatt i förhållande till driftsintjäningen.",
        "def": "EV/EBITDA jämför hela bolagets värde (inklusive skulder) med vad driften tjänar. Lågt tal = billigt. Det används mycket för att jämföra bolag tvärs över sektorer eftersom det \"rensar bort\" skillnader i skuld och skatteregler.",
        "example": "Equinor handlas på EV/EBITDA 3,2x — lågt, och indikerar attraktiv prissättning.",
        "related": ["ebitda", "pe", "mcap"],
    },
    "gjeldsgrad": {
        "name": "Skuldsättning",
        "pron": "",
        "level": "med",
        "short": "Hur mycket skuld bolaget har i förhållande till eget kapital.",
        "def": "Skuldsättning visar hur mycket bolaget har lånat jämfört med ägarnas pengar. Låg skuldsättning är tryggt — bolaget klarar dåliga tider. Hög skuldsättning ger högre risk men kan ge bättre avkastning när det går bra.",
        "example": "Banker har naturligt hög skuldsättning (de är byggda kring utlåning). Teknikbolag har oftast låg.",
        "related": ["roe", "pb"],
    },
    "eps": {
        "name": "EPS",
        "pron": "/eː peː es/",
        "level": "med",
        "short": "Hur mycket bolaget tjänar per aktie.",
        "def": "EPS står för \"Earnings Per Share\". Det är bolagets vinst delat på antal aktier. Talet visar hur mycket av vinsten som tillhör varje enskild aktie du äger. Används mycket för att jämföra bolag och se utvecklingen över tid.",
        "example": "Equinor hade EPS på 0,68 USD i Q4 — det betyder 0,68 USD vinst per aktie.",
        "related": ["nettoresultat", "pe", "utbytte"],
    },
    "omsetning": {
        "name": "Omsättning",
        "pron": "",
        "level": "med",
        "short": "Hur mycket bolaget har sålt för.",
        "def": "Omsättning är totalsumman av allt bolaget har sålt under en period, innan några kostnader dragits av. Det kallas också \"intäkter\" eller \"topplinjen\" — eftersom det står överst i resultaträkningen.",
        "example": "Equinor hade omsättning på 24,3 miljarder USD i Q4 — vad de sålde olja, gas och produkter för.",
        "tip": "Stor omsättning betyder inte nödvändigtvis att bolaget tjänar pengar. Du måste dra av alla kostnader först.",
        "related": ["ebitda", "nettoresultat"],
    },
    "nettoresultat": {
        "name": "Nettoresultat",
        "pron": "",
        "level": "med",
        "short": "Det bolaget har kvar efter alla kostnader.",
        "def": "Nettoresultat är den \"rena\" vinsten — efter att allt dragits av: kostnader, räntor, skatt och slitage. Det är dessa pengar som faktiskt kan användas till utdelning, investeringar eller sparas.",
        "example": "Equinor hade nettoresultat på 2,1 miljarder USD i Q4 — pengarna som faktiskt var kvar.",
        "related": ["ebitda", "eps", "omsetning"],
    },
    "kontantstrom": {
        "name": "Fritt kassaflöde",
        "pron": "",
        "level": "med",
        "short": "Pengar bolaget har över efter alla nödvändiga investeringar.",
        "def": "Fritt kassaflöde är riktiga pengar bolaget har genererat, efter att alla investeringar är gjorda. Det är pengarna som faktiskt kan användas till utdelning, amortering av skulder eller förvärv. Många professionella anser att detta är det viktigaste talet att titta på.",
        "example": "Equinor genererade 4,2 miljarder USD i fritt kassaflöde — därför kan de betala så hög utdelning.",
        "related": ["ebitda", "utbytte", "nettoresultat"],
    },
    "konsensus": {
        "name": "Konsensus",
        "pron": "/konsɛnˈsʉs/",
        "level": "med",
        "short": "Snittet av vad analytiker förväntar sig.",
        "def": "Konsensus är genomsnittet av alla analytikers prognoser för ett bolag. När ett bolag \"slår konsensus\" betyder det att de levererade bättre siffror än förväntat — och det leder ofta till att aktien stiger.",
        "example": "Equinor slog konsensus med 12 % — vinsten var 12 % högre än analytiker väntade.",
        "tip": "Det är inte alltid sant att \"bättre än konsensus\" är bra. Om förväntningarna var låga från början kan bolaget egentligen leverera svaga siffror.",
        "related": ["eps", "nettoresultat"],
    },
    "volatilitet": {
        "name": "Volatilitet",
        "pron": "/voːlatiliˈteːt/",
        "level": "med",
        "short": "Hur mycket en aktie hoppar upp och ned.",
        "def": "Volatilitet mäter hur oförutsägbart priset på en aktie är. Hög volatilitet är som en berg-och-dalbana — spännande, men inte för de som mår illa. Låg volatilitet är som en husbilssemester — tråkigt, men förutsägbart.",
        "example": "Bitcoin har hög volatilitet. Statsobligationer har låg volatilitet. Teknikaktier är däremellan.",
        "related": ["beta"],
    },

    # ============================================
    # FOR DE NYSGJERRIGE (adv)
    # ============================================
    "beta": {
        "name": "Beta",
        "pron": "/ˈbeːta/",
        "level": "adv",
        "short": "Hur mycket en aktie rör sig jämfört med marknaden.",
        "def": "Beta mäter aktiens känslighet för marknaden. Beta 1 betyder att aktien rör sig likadant som marknaden. Beta 1,5 betyder att den rör sig 50 % mer än marknaden (både upp och ned). Beta 0,5 betyder hälften — lugnare.",
        "example": "Telenor har lågt beta (runt 0,7) — den rör sig mindre än marknadsgenomsnittet.",
        "related": ["volatilitet"],
    },
    "shorte": {
        "name": "Att shorta",
        "pron": "/ʃoːrte/",
        "level": "adv",
        "short": "Att satsa på att en aktie ska falla.",
        "def": "Att shorta är en teknik där du tjänar pengar om aktien sjunker. Du lånar aktier, säljer dem och hoppas på att köpa tillbaka dem billigare. Om du har rätt behåller du skillnaden. Om du har fel kan förlusten vara obegränsad — eftersom en aktie kan stiga oändligt.",
        "example": "Hedgefonden shortade Tesla och förlorade 1 miljard dollar när aktien fortsatte att stiga.",
        "tip": "Shorting är för proffs — för nybörjare är det bäst att hålla sig borta. Förlusterna kan bli större än investeringen.",
        "related": ["bull_bear", "volatilitet"],
    },
    "innsidehandel": {
        "name": "Insiderhandel",
        "pron": "",
        "level": "adv",
        "short": "När ledningen köper eller säljer egna aktier.",
        "def": "När toppchefer i ett bolag köper eller säljer aktier i sitt eget bolag kallas det insiderhandel. Detta måste alltid anmälas till börsen och är offentligt. Många investerare följer detta noggrant eftersom ledningen ofta vet mer än andra.",
        "example": "VD på DNB köpte 10 000 aktier igår — ett signal på att hon tror på bolaget.",
        "related": ["aksje"],
    },
    "golden_cross": {
        "name": "Golden Cross",
        "pron": "/ˈgoʊldən krɔs/",
        "level": "adv",
        "short": "Ett positivt tekniskt signal i ett diagram.",
        "def": "Golden Cross uppstår när ett kortare genomsnitt (typiskt 50 dagars snitt) korsar uppåt genom ett längre genomsnitt (typiskt 200 dagars snitt). Det tolkas som ett tecken på stärkt trend — att uppgången kan fortsätta.",
        "example": "Equinor fick Golden Cross den 23 januari och aktien har stigit jämnt sedan dess.",
        "related": ["volatilitet"],
    },
    "konsesjon": {
        "name": "Koncession",
        "pron": "/konseˈsjoːn/",
        "level": "adv",
        "short": "Offentligt tillstånd att driva en verksamhet.",
        "def": "En koncession är en licens från myndigheterna som ger ett bolag rätt att bedriva en specifik aktivitet — till exempel att producera olja, driva bank eller sälja alkohol. Koncessioner är viktiga eftersom de begränsar vem som får verka på marknaden.",
        "example": "Aker BP fick koncession för Yggdrasil-fältet efter många års handläggning.",
        "related": [],
    },

    # ============================================
    # UTTRYKK OG SLANG (idiom)
    # ============================================
    "bull_bear": {
        "name": "Bull och bear",
        "pron": "/bʊl/ /bɛr/",
        "level": "idiom",
        "short": "Optimist eller pessimist om marknaden.",
        "def": "En \"bull\" tror marknaden ska upp (som en tjur som stöter uppåt). En \"bear\" tror marknaden ska ned (som en björn som slår nedåt). \"Bull market\" = uppgångsmarknad. \"Bear market\" = nedgångsmarknad på 20 % eller mer.",
        "example": "Hon är bull på Equinor — hon tror den ska stiga vidare. Han är bear på lax just nu.",
        "related": ["shorte", "korreksjon"],
    },
    "falling_knife": {
        "name": "Never catch a falling knife",
        "pron": "",
        "level": "idiom",
        "short": "Köp inte en aktie som faller kraftigt — du kan skära dig.",
        "def": "Ett populärt uttryck som varnar för att köpa en aktie bara för att den fallit mycket. Aktien kan fortsätta att falla och du kan förlora mer. Bättre att vänta tills den stabiliserar sig innan du köper. Som att vänta tills kniven träffat golvet innan du plockar upp den.",
        "example": "Aktien föll 30 % idag — men fånga inte kniven, vänta tills vi vet att botten är nådd.",
        "tip": "Det är nästan omöjligt att träffa botten. Bättre att missa de första 10 % av en uppgång än att riskera att förlora 40 % på vägen ned.",
        "related": ["korreksjon", "volatilitet"],
    },
    "korreksjon": {
        "name": "Korrektion",
        "pron": "/korɛkˈsjoːn/",
        "level": "idiom",
        "short": "Ett fall på 10-20 % i en aktie eller marknad.",
        "def": "En korrektion är när marknaden eller en aktie faller mer än 10 % från toppen. Det är normalt och sker regelbundet — vanligtvis en gång per år. Det är inte en kris utan en \"paus\" i uppgången.",
        "example": "Efter många månaders uppgång kom en korrektion på 12 % — helt normalt.",
        "related": ["bull_bear", "volatilitet", "falling_knife"],
    },
    "blue_chip": {
        "name": "Blue chip",
        "pron": "",
        "level": "idiom",
        "short": "Stora, etablerade, trygga bolag.",
        "def": "Blue chip-bolag är de största och mest stabila aktierna på börsen — som Equinor, DNB och Telenor på Oslo Børs. Namnet kommer från poker, där blå marker är mest värda. De ger sällan explosiv tillväxt men är mer förutsägbara.",
        "example": "Hon investerar bara i blue chips för att kunna sova gott om natten.",
        "related": ["mcap", "utbytte"],
    },
    "fomo": {
        "name": "FOMO",
        "pron": "/ˈfoʊmoʊ/",
        "level": "idiom",
        "short": "Rädslan för att missa en möjlighet.",
        "def": "FOMO står för \"Fear Of Missing Out\" — rädslan för att missa något. I aktier är det känslan du får när en aktie stiger snabbt och du inte har köpt. FOMO får många att köpa på toppen — vilket ofta är misstaget.",
        "example": "Efter att alla vänner tjänade pengar på krypto köpte han av FOMO — precis innan det kraschade.",
        "tip": "FOMO är en av de farligaste känslorna i aktievärlden. Om du känner FOMO, vänta ett par dagar innan du gör något.",
        "related": ["volatilitet", "falling_knife"],
    },
    "diversifisering": {
        "name": "Diversifiering",
        "pron": "/divɛrsifisɛˈriŋ/",
        "level": "idiom",
        "short": "Lägg inte alla ägg i samma korg.",
        "def": "Att diversifiera innebär att sprida investeringarna på många olika bolag, sektorer och länder. Om ett bolag går dåligt kan andra gå bra. Det minskar risken — det är den enda \"gratislunchen\" i finansvärlden.",
        "example": "Med 10-15 olika aktier i skilda sektorer har hon en välj diversifierad portfölj.",
        "related": ["volatilitet", "sektor"],
    },
    "diamond_hands": {
        "name": "Diamond hands 💎",
        "pron": "",
        "level": "idiom",
        "short": "Att hålla aktier oavsett vad som händer.",
        "def": "Ett internetuttryck som beskriver investerare som håller kvar sina aktier även när priset faller mycket. Händer av diamant — så starka att de inte ger sig. Motsatsen är \"paper hands\" — pappershänder som släpper vid första motgång.",
        "example": "Hon har diamond hands på Tesla — har hållit aktien genom 50 % fall.",
        "tip": "Det är bra att vara långsiktig, men förväxla inte envishet med strategi. Ibland är det rätt att sälja.",
        "related": ["fomo", "bull_bear"],
    },
    "ipo": {
        "name": "IPO",
        "pron": "/aɪ piː oʊ/",
        "level": "idiom",
        "short": "När ett bolag börsnorteras för första gången.",
        "def": "IPO står för \"Initial Public Offering\" — första gångens aktieförsäljning till allmänheten. Det är då bolaget går från att vara privatägt till att handlas på börsen, och vem som helst kan köpa aktier. IPO:er omskrivs ofta mycket och kan vara spännande.",
        "example": "Spotify gjorde IPO 2018 — det var en av de största börsnoteringarna det året.",
        "tip": "Många IPO-aktier faller efter första handelsdagen. Det är ofta tryggare att vänta några månader innan du köper.",
        "related": ["aksje", "bors"],
    },
    "buyback": {
        "name": "Återköp (buyback)",
        "pron": "",
        "level": "idiom",
        "short": "När ett bolag köper egna aktier.",
        "def": "När ett bolag har överskott kan de använda pengarna till att köpa tillbaka sina egna aktier från marknaden. Då blir det färre aktier totalt och varje kvarvarande aktie blir mer värd. Det är ett sätt att ge pengar tillbaka till ägarna, alternativt till utdelning.",
        "example": "DNB köpte tillbaka 1 % av sina egna aktier förra året — ägarna har nu en större andel av bolaget.",
        "related": ["utbytte", "aksje"],
    },
}


LEVEL_LABELS = {
    "basic": "Helt enkelt",
    "med": "Lite mer",
    "adv": "För de nyfikna",
    "idiom": "Uttryck och slang",
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
