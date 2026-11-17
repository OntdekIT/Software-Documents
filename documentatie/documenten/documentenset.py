"""De vaste lijst van de 21 documenten van de set. Eenmaal vastgelegd, door de leeswijzer
(tabel en diagram) gedeeld. De titel is de PDF-bestandsnaam zonder nummer, zoals de andere
documenten hem gebruiken."""

# (nr, titel, groep, voor wie, wat je erin vindt)
SET = [
    (1, "Overzicht", "Begin hier", "iedereen", "Wat MB Ontdekt is, welk probleem het oplost en voor wie, met een contextplaatje."),
    (2, "Leeswijzer", "Begin hier", "iedereen", "Dit document: de indeling van de set en leesroutes per lezer."),
    (3, "Analysedocument", "Wat en waarom", "opdrachtgever, team, beoordelaar", "De wensen van de opdrachtgever als eisen en use cases."),
    (4, "Prioritering", "Wat en waarom", "opdrachtgever, team", "Welke wensen eerst komen en waarom."),
    (5, "Domeinmodel", "Wat en waarom", "team, beoordelaar", "De begrippen van het domein en hoe ze samenhangen."),
    (6, "Woordenlijst", "Wat en waarom", "iedereen", "Uitleg van de vaktermen en afkortingen."),
    (7, "C4-model", "Hoe het gebouwd is", "team, beoordelaar", "De architectuur in vier zoomniveaus."),
    (8, "Architectuur en dataflow", "Hoe het gebouwd is", "team, beoordelaar", "Hoe gegevens van meetstation tot scherm stromen."),
    (9, "Beveiliging", "Hoe het gebouwd is", "team, beheerder, beoordelaar", "Hoe de app inloggen, rechten en gegevens beschermt."),
    (10, "Foutafhandeling en betrouwbaarheid", "Hoe het gebouwd is", "team, beheerder", "Wat er gebeurt als iets uitvalt of ontbreekt."),
    (11, "Observability", "Hoe het gebouwd is", "team, beheerder", "Hoe je ziet of het systeem gezond is."),
    (12, "Deployment en omgevingen", "Hoe het gebouwd is", "team, beheerder", "Hoe de app draait en wordt uitgerold."),
    (13, "Backups en AVG", "Hoe het gebouwd is", "beheerder, beoordelaar", "Back-ups en omgang met persoonsgegevens."),
    (14, "Architectuurbeslissingen", "Hoe het gebouwd is", "team, beoordelaar", "De belangrijke keuzes met afwegingen (ADR-set)."),
    (21, "API-document", "Hoe het gebouwd is", "ontwikkelaars", "De endpoints van de backend-API."),
    (15, "Testdocument", "Kwaliteit en werkwijze", "team, beoordelaar", "Teststrategie, testgevallen en resultaten."),
    (16, "Versiebeheer en werkwijze", "Kwaliteit en werkwijze", "team", "Branches, pull requests en afspraken."),
    (17, "Backlog en sprints", "Kwaliteit en werkwijze", "team, opdrachtgever", "De backlog in epics en sprints."),
    (18, "Agile samenwerking", "Kwaliteit en werkwijze", "team, opdrachtgever", "Hoe in korte rondes met de opdrachtgever is gewerkt."),
    (19, "Wireframes en schermen", "Gebruik", "ontwerpers, team, beoordelaar", "De schermen van de app met uitleg en de routestructuur."),
    (20, "Gebruikershandleiding", "Gebruik", "bezoekers, stationeigenaren, beheerders", "Stap voor stap gebruik per rol."),
]

LEESROUTES = [
    ("Nieuw in het team", [1, 6, 5, 7, 8, 12, 16]),
    ("Opdrachtgever", [1, 3, 4, 17, 18, 19, 20]),
    ("Beoordelaar", [1, 3, 14, 7, 9, 15, 16]),
    ("Beheerder", [1, 20, 12, 13, 11, 10, 9]),
    ("Gebruiker van de app", [1, 20, 19]),
]


def genummerd(nr, titel):
    return f"{nr:02d} {titel}"
