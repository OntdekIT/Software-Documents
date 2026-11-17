"""01 Overzicht: wat MB Ontdekt is, welk probleem het oplost en voor wie."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from opmaak import (  # noqa: E402
    DATUM, Bullets, Heading, Para, Table, bron_regel, bronnenblok, diagram,
)
from docgen import Document, Image, Meta, Note


def document() -> Document:
    b = [
        Heading("Het probleem", 1),
        Para("Ontdekstation organiseert samen met Bibliotheek Midden-Brabant workshops voor jong en oud, waarin je je "
             "talenten voor wetenschap en techniek ontdekt. Een deel daarvan is een project om temperatuur en "
             "luchtkwaliteit te meten: in een workshop bouw je zelf een meetstation. Zo'n station meet onder andere "
             "temperatuur, luchtvochtigheid en fijnstof en stuurt de metingen naar Meet je Stad."),
        Para("Elk station levert losse metingen. Om te zien hoe het klimaat per wijk verschilt en verandert, en of het "
             "meetnet nog gezond is, moeten die metingen worden samengebracht. Dat is wat MB Ontdekt doet. Data valt "
             "bovendien soms weg: issue #120 in de frontend-repo vraagt waarom de fijnstofstations wisselend data "
             "sturen, en issue #121 vraagt om inzicht in uitvalmomenten."),
        Heading("De oplossing", 1),
        Para("MB Ontdekt (in de code ook ClimateChecker of OntdekStation013) is een webapplicatie die de metingen van "
             "alle meetstations ophaalt, opslaat en overzichtelijk laat zien. Wat je als gebruiker kunt doen:"),
        Bullets([
            "**Kaart**: temperatuur of fijnstof (PM2.5) per wijk als kleurlaag, met de stations als punten, een zoekbalk, "
            "een wijkenlijst en een tijdlijn om de afgelopen 24 uur af te spelen.",
            "**Heatmap**: het patroon over de stad als doorlopend kleurvlak, met de warmste en koudste plek.",
            "**Wijken**: alle wijken rangschikken en tot drie naast elkaar vergelijken.",
            "**Dashboard**: de gezondheid van het meetnet (actieve en uitgevallen stations, dekking, stadsgemiddelde).",
            "**Mijn stations**: je eigen meetstation claimen, een naam en zichtbaarheid kiezen en de metingen bekijken.",
            "**Beheer**: gebruikers, stations en workshopcodes beheren (alleen voor beheerders).",
        ]),
        Para("De pagina 'Over ons' in de app beschrijft de keten in vier stappen: een station bouwen, het station meet, "
             "MB Ontdekt haalt de data op via de API van Meet je Stad, en de gebruiker ziet het resultaat."),
        Heading("Voor wie", 1),
        Table(kop=["Gebruiker", "Wat die doet", "Rol in de code"], rijen=[
            ["Bezoeker", "Kaart, heatmap, wijken en dashboard bekijken zonder account.", "geen account"],
            ["Stationeigenaar", "Heeft een workshop gevolgd, registreert met een stationcode en workshopcode en beheert het eigen station.", "USER"],
            ["Beheerder", "Beheert gebruikers, stations en workshopcodes en ziet kerncijfers en waarschuwingen.", "ADMIN of SUPER_ADMIN"],
        ], kolombreedtes=[2, 6, 3]),
        Para("De rollen komen uit src/domain/user-role.jsx en de route-beveiliging uit src/main.jsx. De handleiding per "
             "rol staat in het document Gebruikershandleiding."),
        Heading("Context", 1),
        Para("De app bestaat uit een webapp (React) en een backend-API (Spring Boot) met een MariaDB-database. De backend haalt "
             "periodiek metingen op bij Meet je Stad en mailt inlogcodes via een mailserver. De kaartachtergrond komt van "
             "OpenFreeMap. De plaat hieronder is afgeleid uit de code."),
        Image(diagram("overzicht", "context"), onderschrift=f"Context van MB Ontdekt. Bron: ClimateChecker/pom.xml, "
              f"src/main/resources/application.properties (meetjestad.base-url, ingest.interval-seconds, spring.datasource.url, "
              f"spring.mail.host), package.json, src/components/styles/map.json, src/domain/user-role.jsx; {bron_regel()}. "
              "Het ophaalinterval is de standaardwaarde en per omgeving instelbaar.", max_hoogte_mm=90),
        Note("MB Ontdekt maakt de metingen van de zelfgebouwde meetstations van Ontdekstation en Bibliotheek Midden-Brabant "
             "zichtbaar per wijk, en laat zien of het meetnet gezond is. Bezoekers kijken, stationeigenaren beheren hun eigen "
             "station, beheerders houden het geheel draaiend."),
        Para("Verder lezen: de Leeswijzer wijst de weg door de hele set; de Gebruikershandleiding en Wireframes en schermen "
             "tonen de app zelf; het C4-model en Architectuur en dataflow leggen de bouw uit."),
    ]
    b += bronnenblok([
        "README.md van de backend en frontend (introductie van het project).",
        "src/pages/about.jsx (de eigen beschrijving van de app in de Over ons-pagina).",
        "Issues OntdekIT/Software-FrontEnd #120 en #121 (data die wisselend binnenkomt, uitvalmomenten).",
        "src/domain/user-role.jsx en src/main.jsx (rollen en beveiligde routes).",
        "Het contextplaatje is gebaseerd op de bronbestanden in het onderschrift.",
    ], [
        "Welke bibliotheekvestigingen of aantallen deelnemers meedoen staat niet in de code of issues en wordt niet beweerd.",
        "Of Meet je Stad een vaste afspraak of SLA met het project heeft is niet vast te stellen.",
    ])
    return Document(meta=Meta("Overzicht", "Wat MB Ontdekt is en welk probleem het oplost.",
                              [("Datum", DATUM), ("Versie", "app-code " + bron_regel())]),
                    blokken=b, voettekst="MB Ontdekt · overzicht")
