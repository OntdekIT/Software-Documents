"""19 Wireframes en schermen: de echte schermen van MB Ontdekt, met uitleg, routes en ontwerpkeuzes."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from opmaak import (  # noqa: E402
    DATUM, DIAG, Bullets, Heading, Para, Table, bron_regel, bronnenblok, schermpad,
)
from docgen import Document, Image, Meta, Note  # noqa: E402

D = "wireframes-en-schermen"
NAV = {
 "gast": {
  "bovenbalk": [
   {
    "label": "Kaart",
    "to": "/"
   },
   {
    "label": "Heatmap",
    "to": "/heatmap"
   },
   {
    "label": "Wijken",
    "to": "/wijken"
   },
   {
    "label": "Dashboard",
    "to": "/dashboard"
   }
  ],
  "onderbalk": [
   {
    "label": "Kaart",
    "to": "/"
   },
   {
    "label": "Mijn stations",
    "to": "/my/stations"
   },
   {
    "label": "Meldingen",
    "to": "/meldingen"
   },
   {
    "label": "Inloggen",
    "to": "/auth/login"
   }
  ],
  "ontdekken": [
   {
    "label": "Heatmap",
    "to": "/heatmap"
   },
   {
    "label": "Wijken",
    "to": "/wijken"
   },
   {
    "label": "Dashboard",
    "to": "/dashboard"
   }
  ],
  "menu": [
   {
    "label": "Over ons",
    "to": "/about"
   }
  ],
  "profielmenu": []
 },
 "gebruiker": {
  "bovenbalk": [
   {
    "label": "Kaart",
    "to": "/"
   },
   {
    "label": "Heatmap",
    "to": "/heatmap"
   },
   {
    "label": "Wijken",
    "to": "/wijken"
   },
   {
    "label": "Dashboard",
    "to": "/dashboard"
   }
  ],
  "onderbalk": [
   {
    "label": "Kaart",
    "to": "/"
   },
   {
    "label": "Mijn stations",
    "to": "/my/stations"
   },
   {
    "label": "Meldingen",
    "to": "/meldingen"
   },
   {
    "label": "Profiel",
    "to": "/my/account"
   }
  ],
  "ontdekken": [
   {
    "label": "Heatmap",
    "to": "/heatmap"
   },
   {
    "label": "Wijken",
    "to": "/wijken"
   },
   {
    "label": "Dashboard",
    "to": "/dashboard"
   }
  ],
  "menu": [
   {
    "label": "Over ons",
    "to": "/about"
   }
  ],
  "profielmenu": [
   {
    "label": "Mijn stations",
    "to": "/my/stations"
   },
   {
    "label": "Meldingen",
    "to": "/meldingen"
   },
   {
    "label": "Over ons",
    "to": "/about"
   }
  ]
 },
 "beheerder": {
  "bovenbalk": [
   {
    "label": "Kaart",
    "to": "/"
   },
   {
    "label": "Heatmap",
    "to": "/heatmap"
   },
   {
    "label": "Wijken",
    "to": "/wijken"
   },
   {
    "label": "Dashboard",
    "to": "/dashboard"
   }
  ],
  "onderbalk": [
   {
    "label": "Kaart",
    "to": "/"
   },
   {
    "label": "Mijn stations",
    "to": "/my/stations"
   },
   {
    "label": "Meldingen",
    "to": "/meldingen"
   },
   {
    "label": "Profiel",
    "to": "/my/account"
   }
  ],
  "ontdekken": [
   {
    "label": "Heatmap",
    "to": "/heatmap"
   },
   {
    "label": "Wijken",
    "to": "/wijken"
   },
   {
    "label": "Dashboard",
    "to": "/dashboard"
   }
  ],
  "menu": [
   {
    "label": "Over ons",
    "to": "/about"
   },
   {
    "label": "Beheer",
    "to": "/admin"
   }
  ],
  "profielmenu": [
   {
    "label": "Mijn stations",
    "to": "/my/stations"
   },
   {
    "label": "Meldingen",
    "to": "/meldingen"
   },
   {
    "label": "Over ons",
    "to": "/about"
   },
   {
    "label": "Beheer",
    "to": "/admin"
   }
  ]
 },
 "max_bovenbalk": 4,
 "breekpunt": 1024
}
BESCHERMD = [{"pad": "/meldingen", "rollen": []}, {"pad": "/my", "rollen": []}, {"pad": "/admin", "rollen": ["SUPER_ADMIN", "ADMIN"]}]


def scherm(titel, uitleg, naam, onderschrift, hoogte=86):
    return [
        Heading(titel, 2),
        Para(uitleg),
        Image(schermpad(naam), onderschrift=onderschrift, max_hoogte_mm=hoogte, kader=True),
    ]


def document() -> Document:
    nav = NAV
    b = [
        Para("Dit document toont de schermen van MB Ontdekt zoals ze echt zijn. Het zijn geen schetsen: elk plaatje is een "
             "opname van de draaiende app (schermopnames van de draaiende app, 1440 bij 900 pixels voor desktop en 390 pixels "
             "breed voor mobiel), zodat de schermen niet afwijken van wat de code doet. Per scherm staat wat erop te zien is en "
             "wat je er doet. Daarna volgen de routestructuur en de navigatie, beide afgeleid uit de frontend-code, en de "
             "ontwerpkeuzes met de issues waar ze vandaan komen."),
        Note("Elke pagina in het menu doet iets anders: Kaart is meten per wijk en station, Heatmap het patroon over de stad, "
             "Wijken vergelijken en rangschikken, Dashboard de gezondheid van het meetnet. Dit is de afspraak uit issues #184 "
             "tot en met #187 van de frontend-repo."),
        Heading("Schermen voor iedereen (zonder account)", 1),
    ]
    b += scherm("Kaart (route /)",
                "Het hoofdscherm. De kaart vult het scherm; wijken zijn ingekleurd naar temperatuur of fijnstof (PM2.5), grijs "
                "betekent 'Geen recente data'. Linksboven staan een zoekbalk voor wijken, een knop voor je locatie, zoomknoppen, "
                "een samenvattingsstrook (gemiddelde temperatuur, PM2.5, aantal actieve stations) en de laagkeuze. Rechts staat de "
                "wijkenlijst met een kleurchip, de waarde en 'Bijgewerkt zojuist', te sorteren op A tot Z, warmst of koudst. "
                "Onderaan staat de tijdlijn: speel de afgelopen 24 uur af met afspeelknop, snelheid (1x) en een LIVE-badge. "
                "De gele stippen zijn meetstations.",
                "gast-kaart", f"Kaart, uitgelogd, desktop. Bron: opname van de draaiende app; code: src/pages/kaart.jsx; {bron_regel()}.")
    b += scherm("Wijkdetail (route /wijk/:id)",
                "Een klik op een wijk, of een gedeelde link, opent de kaart met een detailpaneel. Het toont twee kerngetallen "
                "(temperatuur en PM2.5), 'Bijgewerkt 11 min geleden' en een grafiek van de laatste 24 uur, met uitklapbare "
                "alle metingen. 'Deel' deelt de link (of kopieert hem); 'Meld mij' staat klaar maar is uitgeschakeld tot de "
                "meldingsvoorkeuren bestaan (comment in src/components/Home/RegionDetails.jsx, issue #148). Sluiten kan met de "
                "knop of Escape. Merk op: op dit scherm is in de menubalk geen item gemarkeerd, omdat '/wijk/:id' niet bij "
                "het item Kaart ('/') hoort in nav-items.js.",
                "gast-wijk-detail", f"Wijkdetail van Bouwmeester. Bron: opname; code: src/main.jsx (route wijk/:id), src/utils/nav-items.js; {bron_regel()}.")
    b += scherm("Heatmap (route /heatmap)",
                "Het patroon over de stad als doorlopend kleurvlak, geschat tussen de stations, onafhankelijk van wijkgrenzen. "
                "Rechts staat het paneel 'Patroon over de stad' met de warmste en koudste plek (met stationsnummer) en een uitleg "
                "hoeveel stations meedoen. Gebied zonder station in de buurt blijft doorzichtig. Tik op de kaart voor de "
                "geschatte waarde op dat punt.",
                "gast-heatmap", f"Heatmap. Bron: opname; code: src/pages/heatmap.jsx; {bron_regel()}.")
    b += scherm("Wijken (route /wijken)",
                "Alle wijken als rangschikking met waarde, een sparkline van 24 uur, trend, aantal stations en status. Je kunt "
                "zoeken, sorteren (A tot Z, warmst, koudst), filteren op 'Alleen wijken met data' en tot drie wijken aanvinken "
                "om ze in een lijngrafiek met het stadsgemiddelde te vergelijken. Bovenaan staan de warmste wijk, de koudste en "
                "de grootste verandering in 24 uur.",
                "gast-wijken", f"Wijken, vergelijken. Bron: opname; code: src/pages/wijken.jsx; {bron_regel()}.")
    b += scherm("Dashboard (route /dashboard)",
                "De gezondheid van het meetnet: actieve stations, uitgevallen of gestoorde stations, dekking van de laatste 24 uur, "
                "gemiddelde temperatuur en PM2.5, een grafiek van het stadsgemiddelde, de warmste en koudste wijk, een lijst van "
                "stations zonder recente meting en een uitleg waarom er soms data ontbreekt.",
                "gast-dashboard", f"Dashboard. Bron: opname; code: src/pages/network-dashboard.jsx; {bron_regel()}.")
    b += scherm("Over ons (route /about)",
                "Beschrijft wat MB Ontdekt is, de vier stappen van meetstation tot kaart en wat je in de app kunt doen.",
                "gast-over-ons", f"Over ons. Bron: opname; code: src/pages/about.jsx; {bron_regel()}.", hoogte=95)
    b += [
        Heading("Account", 1),
        Para("Inloggen, registreren en wachtwoord vergeten zijn eenvoudige kaarten in het midden van het scherm. Registreren "
             "vraagt naast naam, e-mail en wachtwoord een meetstationcode en een workshopcode; dat flow staat in de "
             "Gebruikershandleiding."),
        Image(schermpad("gast-inloggen"), onderschrift=f"Inloggen. Bron: opname; code: src/pages/auth/login.jsx; {bron_regel()}.", max_hoogte_mm=70, kader=True),
        Image(schermpad("gast-registreren"), onderschrift=f"Registreren. Bron: opname; code: src/pages/auth/register.jsx; {bron_regel()}.", max_hoogte_mm=70, kader=True),
        Heading("Schermen na inloggen", 1),
    ]
    b += scherm("Mijn stations, Meldingen en Profiel",
                "Mijn stations (/my/stations) toont je stations met een status en 'Nieuw station toevoegen'; Meldingen "
                "(/meldingen) is een placeholder met de tekst 'Meldingen komen eraan'; Profiel (/my/account) toont je "
                "accountgegevens en rol. Zonder inlog sturen deze routes naar inloggen (ProtectedRoute). Hieronder het profiel "
                "van een beheerder.",
                "beheerder-profiel", f"Profiel van een beheerder. Bron: opname; code: src/pages/my/account/profile.jsx; {bron_regel()}.", hoogte=80)
    b += [
        Heading("Beheer (alleen ADMIN of SUPER_ADMIN)", 2),
        Para("Beheer is een scherm met vier tabs: Overzicht, Gebruikers, Stations en Workshopcodes (route /admin met kinderroutes). "
             "Het overzicht toont tellers en waarschuwingen en een kaart naar de datadekking. De overige tabs tonen "
             "lijsten met acties (gebruiker bekijken, station toevoegen, workshopcode aanmaken)."),
        Image(schermpad("beheerder-overzicht"), onderschrift=f"Beheer, tab Overzicht. Bron: opname; code: src/pages/admin/admin-layout.jsx, src/utils/admin-tabs.js; {bron_regel()}.", max_hoogte_mm=90, kader=True),
        Image(schermpad("beheerder-workshopcodes"), onderschrift=f"Beheer, tab Workshopcodes (nog zonder codes). Bron: opname; code: src/pages/admin/workshop-codes/workshop-code-overview.jsx; {bron_regel()}.", max_hoogte_mm=60, kader=True),
        Heading("Mobiel", 1),
        Para("Onder 1024 pixels breedte (breekpunt DESKTOP_BREAKPOINT_PX in nav-items.js) krijgt de app een vaste onderbalk met "
             "Kaart, Mijn stations, Meldingen en Profiel (uitgelogd: Inloggen). De wijkenlijst wordt een bottom sheet, en de "
             "overige pagina's (Heatmap, Wijken, Dashboard, Over ons, Beheer) staan op de profielpagina onder 'Meer ontdekken'."),
        Image(schermpad("plaat-mobiel-kaart"), onderschrift=f"Mobiel (390 px): kaart en wijkdetail. Bron: opname met mobiele emulatie; {bron_regel()}.", max_hoogte_mm=110),
        Image(schermpad("plaat-mobiel-pagina"), onderschrift=f"Mobiel: heatmap, wijken en dashboard. Bron: opname met mobiele emulatie; {bron_regel()}.", max_hoogte_mm=100),
        Image(schermpad("plaat-mobiel-beheerder"), onderschrift=f"Mobiel, beheerder: profielpagina (met Meer ontdekken) en Beheer. Bron: opname met mobiele emulatie; {bron_regel()}.", max_hoogte_mm=110),
        Heading("Routestructuur", 1),
        Para("Het diagram laat alle pagina's zien die src/main.jsx definieert, gegroepeerd naar toegang. Doorverwijzingen uit "
             "src/utils/legacy-routes.js zijn gestippeld. De routes zijn uit de code gelezen, niet overgetypt."),
        Image(str(DIAG / D / "routes.png"), onderschrift=f"Routes en doorverwijzingen. Bron: src/main.jsx, src/utils/legacy-routes.js; {bron_regel()}.", max_hoogte_mm=100),
        Image(str(DIAG / D / "routes-beheer.png"), onderschrift=f"Routes onder /admin. Bron: src/main.jsx; {bron_regel()}.", max_hoogte_mm=80),
        Table(kop=["Beschermd pad", "Toegang"], rijen=[
            [x["pad"], ("rol " + " of ".join(x["rollen"])) if x["rollen"] else "ingelogd (elke rol)"] for x in BESCHERMD
        ], kolombreedtes=[4, 6]),
        Heading("Navigatie per apparaat en rol", 1),
        Para(f"Welke items waar staan is de menu-opbouw per rol volgens src/utils/nav-items.js, voor een gast, een gewone gebruiker en een "
             f"beheerder. De bovenbalk heeft maximaal {nav['max_bovenbalk']} items."),
        Image(str(DIAG / D / "navigatie.png"), onderschrift=f"Menu's per apparaat en rol. Bron: src/utils/nav-items.js, {bron_regel()}.", max_hoogte_mm=100),
        Heading("Ontwerpkeuzes en waar ze vandaan komen", 1),
        Table(kop=["Keuze", "Bron"], rijen=[
            ["De kaart is het hoofdscherm, volledig scherm met zwevende knoppen; wijkenlijst als zijpaneel (desktop) of bottom sheet (mobiel).", "Issue #172, PR #179"],
            ["Deelbare detailweergave per wijk op /wijk/:id met kerngetallen, 24-uursgrafiek, Deel en Meld mij.", "Issue #173, PR #180"],
            ["Tijdlijn om 24 uur af te spelen, met snelheid en LIVE-badge (in de code een 'RainViewer-achtige tijdlijn').", "Issue #174, PR #181, MapTimeline.jsx"],
            ["Onderbalk op mobiel en korte bovenbalk met profielmenu op desktop.", "Issue #175, PR #177"],
            ["Beheer als een scherm met tabs, oude routes blijven werken.", "Issue #176, PR #178"],
            ["Eén kleurenthema in amber en inkt; blauw alleen voor knoppen en acties; wijkenlijst met kleurchip en grote waarde.", "Issue #182, PR #183"],
            ["Elk menu-item een eigen pagina: Heatmap, Wijken en Dashboard krijgen eigen pagina's in plaats van doorverwijzing naar de kaart.", "Issues #184 tot #187, PR's #188 tot #191"],
        ], kolombreedtes=[8, 4]),
        Para("De issues #172 tot en met #176 vermelden dat ze 'voortgekomen uit een ontwerpreview met referenties uit RainViewer, "
             "Ventusky en Watch Duty (Appllama)' zijn. Welke referentie bij welk detail hoort staat alleen voor de tijdlijn in de "
             "code (RainViewer-achtig); issue #182 noemt 'weer- en kaartapps' als inspiratie voor de wijkenlijst. Verder is "
             "niets over de referenties vast te stellen."),
        Heading("Afwijkingen en kanttekeningen", 1),
        Bullets([
            "Op /wijk/:id is geen menu-item gemarkeerd (zie Wijkdetail); issue #187 vraagt om een herkenbare actieve pagina.",
            "De pagina Over ons beschrijft de Heatmap als 'tijdslider' en linkt naar /newheatmap en /kaart (src/pages/about.jsx regels 31 en 32); "
            "de Heatmap-pagina is sinds issue #184 een doorlopend kleurvlak zonder tijdslider, en de links werken alleen via doorverwijzing.",
            "Op mobiel heeft een bezoeker zonder account geen link naar Heatmap, Wijken, Dashboard en Over ons: de bovenbalk met die items is alleen vanaf 1024 pixels zichtbaar (lg-klassen in src/components/navbar.jsx) en 'Meer ontdekken' staat op de profielpagina, die inloggen vereist. Het diagram 'Navigatie per apparaat en rol' laat dit zien: bij gast staat bij mobiel alleen de onderbalk.",
            "De knop 'Meld mij' en de pagina Meldingen zijn bedoeld als voorlopers van FrontEnd #148 (meldingen) en doen nog niets.",
        ]),
    ]
    b += bronnenblok([
        "Schermopnames van de draaiende app op 2026-11-17 (lokale omgeving op http://localhost:3000, data van de lokale database).",
        "Routes en navigatie: src/main.jsx, src/utils/legacy-routes.js, src/utils/nav-items.js, src/utils/admin-tabs.js.",
        "Ontwerpkeuzes: issues OntdekIT/Software-FrontEnd #172 tot en met #187 en PR's #177 tot en met #191.",
        "Het profiel van de beheerder is van de lokale dev-gebruiker uit docker-compose.yml.",
    ], [
        "De meetwaarden op de schermen zijn een momentopname van de lokale database; ze zijn geen vaste waarden.",
        "Of de gekozen referenties (RainViewer, Ventusky, Watch Duty) per scherm zijn nagevolgd, is alleen vast te stellen waar de issues of code het zeggen.",
        "Het formulier 'Meetstation toevoegen' (/admin/stations/toevoegen) is niet getoond met ingevulde gegevens: het vereist een locatie en de lokale locatietabel is leeg.",
    ])
    return Document(meta=Meta("Wireframes en schermen", "De schermen van MB Ontdekt, de routes en de ontwerpkeuzes.",
                              [("Datum", DATUM)]),
                    blokken=b, voettekst="MB Ontdekt · wireframes en schermen")
