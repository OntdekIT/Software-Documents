"""20 Gebruikershandleiding: stap voor stap per rol (bezoeker, stationeigenaar, beheerder)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from opmaak import (  # noqa: E402
    DATUM, DIAG, SCHERMEN, Bullets, Heading, Para, Table, bron_regel, bronnenblok, schermpad,
)
from docgen import Document, Image, Meta, Note  # noqa: E402


def flow(naam: str) -> str:
    return str(SCHERMEN / "flow" / f"{naam}.png")


def stap(nr, tekst):
    return f"**{nr}.** {tekst}"


def document() -> Document:
    b = [
        Para("Deze handleiding legt stap voor stap uit hoe je MB Ontdekt gebruikt, per rol. De stappen zijn zelf doorlopen in de "
             "draaiende app op 2026-11-17 (schermopnames in de lokale omgeving), en de plaatjes zijn de echte schermen daarvan. "
             "Voor een overzicht van alle schermen en routes: zie Wireframes en schermen."),
        Table(kop=["Rol", "Wat je kunt", "Heb je nodig"], rijen=[
            ["Bezoeker", "Kaart, heatmap, wijken en dashboard bekijken.", "Niets, geen account."],
            ["Stationeigenaar", "Alles van de bezoeker, plus je eigen stations beheren.", "Een account, een stationcode en een workshopcode."],
            ["Beheerder", "Alles van de stationeigenaar, plus gebruikers, stations en workshopcodes beheren.", "Een account met de rol ADMIN of SUPER_ADMIN."],
        ], kolombreedtes=[3, 6, 5]),
        Heading("Bezoeker", 1),
        Heading("De kaart gebruiken", 2),
        Bullets([
            stap(1, "Open de app. De kaart (route /) is het startscherm. Wijken zijn ingekleurd; grijs betekent 'Geen recente data'."),
            stap(2, "Kies linksboven de laag: Temperatuur of Fijnstof (PM2.5). De legenda linksonder volgt de keuze."),
            stap(3, "Zoek een wijk in de zoekbalk, of kies er een uit de lijst rechts. Sorteer de lijst op A tot Z, Warmst of Koudst."),
            stap(4, "Klik een wijk. Het detailpaneel toont temperatuur, PM2.5, hoe lang geleden de wijk is bijgewerkt en een grafiek van 24 uur. "
                    "Met 'Deel' kopieer je de link (/wijk/:id), met 'Sluiten' of Escape sluit je het paneel."),
            stap(5, "Speel de afgelopen 24 uur af met de afspeelknop onderaan. Het chip kiest de snelheid en 'LIVE' brengt je terug naar nu."),
        ]),
        Image(schermpad("gast-kaart"), onderschrift=f"Kaart met wijkenlijst en tijdlijn. Bron: opname van de draaiende app; {bron_regel()}.", max_hoogte_mm=85, kader=True),
        Image(schermpad("gast-wijk-detail"), onderschrift=f"Wijkdetail. Bron: opname; {bron_regel()}.", max_hoogte_mm=85, kader=True),
        Heading("Heatmap, Wijken en Dashboard", 2),
        Bullets([
            "**Heatmap** (menu, Heatmap): het patroon over de stad. Rechts staan de warmste en koudste plek. Tik op de kaart voor een schatting op dat punt.",
            "**Wijken** (menu, Wijken): zoek een wijk, sorteer, vink tot drie wijken aan en vergelijk ze met het stadsgemiddelde.",
            "**Dashboard** (menu, Dashboard): zie of het meetnet gezond is, met actieve en uitgevallen stations en een uitleg waarom er soms data ontbreekt.",
        ]),
        Image(schermpad("plaat-mobiel-pagina"), onderschrift=f"Dezelfde pagina's op mobiel (390 px). Bron: opname met mobiele emulatie; {bron_regel()}.", max_hoogte_mm=85),
        Para("Op mobiel staat onderaan een balk met Kaart, Mijn stations, Meldingen en Inloggen of Profiel. Heatmap, Wijken en Dashboard "
             "vind je dan op de profielpagina onder 'Meer ontdekken'. Let op: uitgelogd heeft de mobiele app geen link naar die pagina's (de profielpagina vraagt een account); je opent ze dan via het adres (/heatmap, /wijken, /dashboard) of logt eerst in."),
        Heading("Een account maken", 1),
        Para("Een account maak je met een meetstationcode en een workshopcode. Die krijg je tijdens de workshop van Ontdekstation en "
             "Bibliotheek Midden-Brabant: de workshopcode wordt door een beheerder aangemaakt en is tijdelijk geldig, de stationcode "
             "staat op je meetstation (de naam in de app is 'Meetstation Code'). Zonder geldige codes lukt registreren niet."),
        Bullets([
            stap(1, "Kies Login (of Inloggen) en dan 'Registreer hier', of ga naar /auth/register."),
            stap(2, "Vul voornaam, achternaam, e-mailadres, wachtwoord (twee keer), de meetstationcode en de workshopcode in. Het wachtwoord moet 8 tot 128 tekens lang zijn "
                    "en minstens een hoofdletter en een cijfer bevatten."),
            stap(3, "Kies Registreren. Je krijgt een e-mail met een code en het scherm 'Email bevestigen'."),
            stap(4, "Vul de code uit de e-mail in en kies 'Code verifiëren'. Daarna ben je ingelogd."),
        ]),
        Image(flow("05-registreren-ingevuld"), onderschrift=f"Registreren met een stationcode en een workshopcode. Bron: opname; {bron_regel()}.", max_hoogte_mm=80, kader=True),
        Image(flow("07-mailhog-code"), onderschrift=f"De e-mail met de code, hier gezien in MailHog (de lokale mailbak). Bron: opname; {bron_regel()}.", max_hoogte_mm=70, kader=True),
        Note("Je ziet foutmeldingen zoals 'Ongeldige workshopcode', 'Ongeldige stationcode' of 'Station is al geclaimd' als een van de codes niet klopt. "
             "Een workshopcode verloopt na de gekozen geldigheidsduur (15 minuten tot 1 week), vraag dan een nieuwe aan de beheerder.", kop="Als het niet lukt"),
        Heading("Stationeigenaar", 1),
        Heading("Inloggen met een code", 2),
        Bullets([
            stap(1, "Ga naar Inloggen, vul e-mailadres en wachtwoord in en kies 'Inloggen'."),
            stap(2, "Op een nog onbekend netwerkadres stuurt de app je een code per e-mail. Vul die in en kies 'Code verifiëren'. Op een vertrouwd adres "
                    "ben je direct ingelogd (de backend slaat de mailcode dan over)."),
            stap(3, "Je komt op Mijn stations. Ben je het wachtwoord vergeten, kies 'Wachtwoord vergeten?' op het inlogscherm (het formulier is getoond, het herstelproces is niet doorlopen)."),
        ]),
        Image(flow("06-code-invullen"), onderschrift=f"Het scherm 'Email bevestigen', na registreren of inloggen. Bron: opname; {bron_regel()}.", max_hoogte_mm=65, kader=True),
        Heading("Je station claimen", 2),
        Para("Na het bevestigen van je registratie opent de claim-wizard op stap 2 van 4, omdat het stationnummer uit je registratie bekend is. "
             "Wil je later een extra station toevoegen, dan kies je op Mijn stations 'Nieuw station toevoegen' en begin je bij stap 1."),
        Bullets([
            stap(1, "Stap 1, Meetstation zoeken: vul de workshopcode en het stationnummer in en kies 'Volgende'. Is het station bezet of de code onjuist, dan meldt de app dat."),
            stap(2, "Stap 2, Meetstation privacy: kies Onzichtbaar (de data telt wel mee in de wijk) of Zichtbaar (iedereen kan het station bekijken)."),
            stap(3, "Stap 3, Meetstation naam: geef je station een naam."),
            stap(4, "Stap 4, Meetstation gegevens: controleer nummer, naam en zichtbaarheid en kies 'Claimen'. De melding 'Meetstation succesvol geclaimd' bevestigt het."),
        ]),
        Image(flow("14-claim2-stap1"), onderschrift=f"Claim-wizard, stap 1. Bron: opname; {bron_regel()}.", max_hoogte_mm=60, kader=True),
        Image(flow("17-claim2-stap4"), onderschrift=f"Claim-wizard, stap 4, controleren en Claimen. Bron: opname; {bron_regel()}.", max_hoogte_mm=60, kader=True),
        Image(flow("18-mijn-stations-twee"), onderschrift=f"Mijn stations na het claimen van een tweede station; het nieuwe station heet 'Station op het dak'. Bron: opname; {bron_regel()}.", max_hoogte_mm=75, kader=True),
        Note("Bij het eerste station, direct na registreren, werkte de claim-wizard in onze opname niet zoals bedoeld: de registratie koppelt het "
             "station al aan je account, en de wizard toonde daarna na 'Claimen' de melding 'Meetstation claimen is mislukt'. De gekozen naam en zichtbaarheid "
             "werden daardoor niet opgeslagen; het station behield zijn oorspronkelijke naam en bleef Onzichtbaar. Pas ze daarna aan via het potlood op Mijn stations "
             "(zie 'Een station bewerken'). Zie het onderdeel 'Wat de code echt doet' hieronder.", kop="Let op"),
        Heading("Een station bekijken en bewerken", 2),
        Bullets([
            stap(1, "Op Mijn stations toont elke kaart de status (Offline of een recente meting) en twee knoppen: de 'i' opent de stationsdetails, het potlood bewerkt het station."),
            stap(2, "De details tonen temperatuur, luchtvochtigheid en fijnstof (min, gemiddelde, max), een periodekeuze (24u, 7d, 30d, 3 mnd of eigen datums), een vergelijking met het netwerk en een CSV-export."),
            stap(3, "Bij bewerken kun je de naam en de zichtbaarheid wijzigen en kiezen voor 'Opslaan'."),
        ]),
        Image(flow("25-station-bewerken"), onderschrift=f"Station bewerken. Bron: opname; {bron_regel()}.", max_hoogte_mm=75, kader=True),
        Heading("Profiel en Meldingen", 2),
        Para("Op Profiel zie je je naam, e-mailadres en rol, en kun je ze bijwerken. Meldingen is nog een placeholder ('Meldingen komen eraan'): "
             "er worden nog geen waarschuwingen verstuurd."),
        Image(schermpad("plaat-mobiel-beheerder"), onderschrift=f"Mobiel: profielpagina en Beheer. Bron: opname met mobiele emulatie; {bron_regel()}.", max_hoogte_mm=80),
        Heading("Beheerder", 1),
        Para("Beheerders (rol ADMIN of SUPER_ADMIN) zien in het profielmenu rechtsboven (desktop) of op de profielpagina (mobiel) het item Beheer. "
             "Beheer heeft vier tabs: Overzicht, Gebruikers, Stations en Workshopcodes."),
        Heading("Een workshopcode aanmaken", 2),
        Bullets([
            stap(1, "Ga naar Beheer, tab Workshopcodes, en kies 'Workshopcode aanmaken'."),
            stap(2, "Kies de geldigheidsduur (15 min tot 1 week) en kies 'Workshopcode aanmaken'. De code is een willekeurig getal."),
            stap(3, "De code staat daarna in de lijst met een label zoals 'Verloopt binnen 24 uur' en de vervaldatum. Met de prullenbak verwijder je hem. Met 'toon verlopen codes' zie je ook verlopen codes."),
            stap(4, "Geef de code (en de stationcode) aan de deelnemer van de workshop."),
        ]),
        Image(flow("01-workshopcode-aanmaken"), onderschrift=f"Een workshopcode aanmaken. Bron: opname; {bron_regel()}.", max_hoogte_mm=60, kader=True),
        Image(flow("23-beheer-workshopcodes-met-code"), onderschrift=f"De aangemaakte code in de lijst. Bron: opname; {bron_regel()}.", max_hoogte_mm=50, kader=True),
        Heading("Gebruikers en stations bekijken", 2),
        Bullets([
            stap(1, "Tab Gebruikers: een lijst met naam, e-mailadres en rol. De pijl opent de gebruikerspagina met de gekoppelde stations; daar staan knoppen om te bewerken en te verwijderen."),
            stap(2, "Tab Stations: alle meetstations met actief, publiek en database-tag, en 'Voeg Meetstation Toe'."),
            stap(3, "Tab Overzicht: tellers (gebruikers, stations, stations zonder recente meting, actieve en verlopen workshopcodes, fijnstofdekking), 'Aandacht nodig' en een kaart naar Datadekking."),
        ]),
        Image(flow("22-beheer-gebruiker-detail"), onderschrift=f"Een gebruiker met de gekoppelde stations. Bron: opname; {bron_regel()}.", max_hoogte_mm=60, kader=True),
        Image(schermpad("beheerder-datadekking"), onderschrift=f"Datadekking fijnstof (vanuit het Overzicht). Bron: opname; {bron_regel()}.", max_hoogte_mm=75, kader=True),
        Note("Een meetstation toevoegen via 'Voeg Meetstation Toe' lukt in de huidige versie niet (zie hieronder). Stations komen daarom nu via de gegevensbron en de database binnen, niet via dit formulier.", kop="Let op"),
        Heading("Wat de code echt doet", 1),
        Para("Het diagram is afgeleid uit de code: elke stap heeft een bronbestand en regel (zie Bronnen en controle). De streepjesstap is een "
             "gevonden afwijking tussen bedoeling en gedrag."),
        Image(str(DIAG / "gebruikershandleiding" / "stroom.png"), onderschrift=f"Van bezoeker tot stationeigenaar. Bron: zie de tabel bij Bronnen en controle; {bron_regel()}.", max_hoogte_mm=140),
        Heading("Bekende afwijkingen die je kunt tegenkomen", 2),
        Bullets([
            "**Claim-wizard na registreren:** de wizard probeert een station te claimen dat de registratie al aan je koppelde. Het systeem weigert (station al geclaimd) en toont 'Meetstation claimen is mislukt'. Naam en zichtbaarheid pas je daarna aan via bewerken.",
            "**Stationnummer blijft onthouden:** na die mislukte claim blijft het stationnummer in je browser (localStorage 'stationId') staan; de wizard start dan weer op stap 2 tot je opnieuw inlogt, want inloggen wist het nummer.",
            "**Meetstation toevoegen (beheer):** het formulier vereist een locatie, maar de locatiekeuzelijst is leeg op een database zonder locaties; en POST /api/meetstation/add faalde in onze test met 'Column hum_error cannot be null' (de foutvlaggen worden niet gevuld) en meldt dan ten onrechte 409 'Resource already exists'.",
            "**Mobiel uitgelogd:** de onderbalk heeft alleen Kaart, Mijn stations, Meldingen en Inloggen, en de bovenbalk met Heatmap, Wijken, Dashboard en Over ons is alleen vanaf 1024 pixels breed zichtbaar. Zonder account bereik je die pagina's op een telefoon alleen via het adres.",
            "**Registreren met stationcode 0:** alle bestaande stations in de lokale database hebben registratiecode 0. Registreren met die code geeft de misleidende melding 'Email is al in gebruik' (een fout over meerdere gevonden stations wordt zo vertaald).",
        ]),
    ]
    bron_tabel = Table(kop=["Stap in het diagram", "Bestand", "Regel"], rijen=[
        ["1 Workshopcode aanmaken", "WorkshopController.java", "45"],
        ["2 Registratieformulier", "src/pages/auth/register.jsx", "33"],
        ["3 Controle en koppeling", "UserAuthenticationController.java", "91"],
        ["4 Mail met code", "UserAuthenticationController.java", "107"],
        ["5 Code invullen", "src/components/auth/verify-email.jsx", "26"],
        ["6 Wizard stap 2", "src/pages/my/stations/claim-station.jsx", "38"],
        ["7 Claimen", "src/pages/my/stations/claim-station.jsx", "149"],
        ["Weigering", "StationService.java", "78"],
    ], kolombreedtes=[4, 6, 1])
    b += bronnenblok([
        "Zelf doorlopen in de app op 2026-11-17: workshopcode aanmaken, registreren, code uit MailHog, claimen (twee keer), station bekijken en bewerken, beheerpagina's bekijken.",
        "Doorlopen in een schone testomgeving met testgegevens. Twee teststations (990001, 990002) zijn daarvoor direct in de testdatabase gezet, omdat het toevoegformulier en POST /api/meetstation/add niet werken.",
        "Code: UserAuthenticationController.java (register, login, verify), StationController.java (availability, claim), StationService.java, claim-station.jsx, verify-email.jsx, register.jsx, login.jsx, my-stations-overview.jsx.",
        "Stroomdiagram: de bestanden en regelnummers uit de tabel hieronder, volgens de commits hierboven.",
    ], [
        "Het herstelproces van een vergeten wachtwoord is niet doorlopen, alleen het formulier is gezien.",
        "Gebruiker bewerken of verwijderen en een workshopcode verwijderen zijn niet uitgevoerd, alleen bekeken.",
        "Of bij het claimen een andere gebruiker dan de registrerende kan optreden (bijvoorbeeld een bestaand account dat een extra station claimt) is alleen via de tweede claim getest.",
        "De doelgroep 'stationeigenaar' is een rol USER in de code; de term 'deelnemer van de workshop' komt uit de README en de Over ons-pagina.",
    ])
    # De bronnen-tabel van het stroomdiagram direct na het onderdeel 'Bronnen en controle'.
    idx = next(i for i, x in enumerate(b) if getattr(x, "tekst", "") == "Gebruikte bronnen")
    b.insert(idx, bron_tabel)
    return Document(meta=Meta("Gebruikershandleiding", "MB Ontdekt stap voor stap, per rol.", [("Datum", DATUM)]),
                    blokken=b, voettekst="MB Ontdekt · gebruikershandleiding")
