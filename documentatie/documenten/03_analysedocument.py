"""03 Analysedocument: wat ClimateChecker moet doen, met bewijs per eis."""
import os, sys
from collections import Counter
from docgen import Document, Meta, Heading, Para, Bullets, Table, Note, Image

HIER = os.path.dirname(os.path.abspath(__file__))
DG = os.path.join(HIER, "..", "diagrammen", "analysedocument")
sys.path.insert(0, DG)
import eisen  # noqa: E402

FR, NFR, UC = eisen.FR, eisen.NFR, eisen.UC


def tabel_fr(onderwerp):
    return Table(["Code", "Wens", "Bewijs", "Status"],
                 [[c, w, b, s] for c, o, w, b, s in FR if o == onderwerp], kolombreedtes=[1.1, 5, 4, 2])


def document():
    onderwerpen = []
    for e in FR:
        if e[1] not in onderwerpen:
            onderwerpen.append(e[1])
    tel = Counter(e[4] for e in FR)
    teln = Counter(e[4] for e in NFR)
    b = [
        Para("Dit document beschrijft wat ClimateChecker (MB Ontdekt) moet doen, niet hoe het gebouwd is. Elke wens heeft een code: FR is een functionele wens, "
             "NFR een kwaliteitseis, UC een use case. Bij elke wens staat het bewijs: het issue of de pull request, en het bestand of de route waarin ze in de code "
             "terug te vinden is. De status zegt of de wens op de dev-branch (origin/s3nj26_dev) gerealiseerd is. Wat niet te bewijzen was, staat als open of deels."),
        Para(f"Totaal: {len(FR)} functionele wensen ({tel['gerealiseerd']} gerealiseerd, {tel['deels']} deels, {tel['open']} open, {tel['niet gepland']} niet gepland) en "
             f"{len(NFR)} kwaliteitseisen ({teln['gerealiseerd']} gerealiseerd, {teln['deels']} deels, {teln['open']} open)."),
        Image(os.path.join(DG, "status.png"),
              "Eisen per onderwerp en status. Bron: de eisenlijst in dit document, getoetst aan de code. Backend e104152, frontend 13fc1e2.", breedte_mm=140),
        Heading("Het probleem en het doel"),
        Para("Ontdekstation013 organiseert met Bibliotheek Midden-Brabant workshops waarin deelnemers een meetstation voor temperatuur en luchtkwaliteit bouwen. "
             "De stations sturen hun data naar Meet je stad. MB Ontdekt haalt die data op en toont ze overzichtelijk (bron: README van de backend). Het doel van de app is:"),
        Bullets([
            "Bezoekers zien in een oogopslag hoe warm het is in Tilburg en waar de luchtkwaliteit slecht is, per wijk.",
            "Eigenaren van een station zien hun station en horen het als het uitvalt.",
            "Beheerders beheren gebruikers, workshopcodes en stations en zien of de data betrouwbaar is.",
            "De data komt uit een eigen database, zodat de app snel blijft en niet afhangt van meetjestad.net (BE #206).",
        ]),
        Heading("Wat wel en niet in scope is"),
        Table(["Wel", "Niet (bord: niet gepland of Won't have)"], [
            ["Kaart, wijken, heatmap, dashboard met data uit meetjestad.net", "Een enquete voor meetstation-eigenaren (FE #111)"],
            ["Accounts met workshopcode, e-mailverificatie en rollen", "Notificatievoorkeuren in het profiel (FE #148)"],
            ["Uitvaldetectie en mail aan de eigenaar", "Een eigen e-mailserver in beheer (BE #179; onderzoek in PR #192)"],
            ["Beheer van gebruikers, workshops en stations", "Schaalbaarheid en clustering (Doc #93)"],
            ["Docker-uitrol, healthchecks, CI", "Een volledige acceptatie- en productieomgeving (BE #173)"],
        ], kolombreedtes=[5, 5]),
        Heading("De belangrijkste wensen, per onderwerp"),
    ]
    for o in onderwerpen:
        b += [Heading(o, 2), tabel_fr(o)]
    b += [
        Note("De knop Meld mij in de wijkdetails bestaat al, maar is uitgeschakeld in afwachting van meldingsvoorkeuren (FR-26, niet gepland). "
             "De uitvalmail (FR-23) gaat nu rechtstreeks naar de eigenaar van het station zonder instelbare voorkeur.", kop="Beperking"),
        Heading("Kwaliteitseisen (niet-functioneel)"),
        Table(["Code", "Eis", "Bewijs", "Status"], [[c, f"**{o}.** {w}", bw, s] for c, o, w, bw, s in NFR], kolombreedtes=[1.1, 5, 4, 2]),
        Heading("Belangrijkste gebruikssituaties"),
        Para("Het diagram toont de actoren en de dertien use cases. De use cases staan in de tabel met de wensen waaruit ze zijn opgebouwd."),
        Image(os.path.join(DG, "use-cases.png"),
              "Use-casediagram. Bron: eisen.py (use cases en actoren), de routes in src/main.jsx van de frontend en de controllers van de backend, e104152 en 13fc1e2.",
              breedte_mm=95, max_hoogte_mm=205),
        Table(["Use case", "Waar het over gaat", "Actoren", "Wensen"],
              [[f"{c} {n}", o, ", ".join(a), f] for c, n, a, o, f, _ in UC], kolombreedtes=[3, 4.5, 2, 2.5]),
        Heading("Verschillen met de oude analysedocumenten"),
        Bullets([
            "Het Analysedocument iteratie 4 (s3nj24) noemt een profielpagina waar een gebruiker ook zijn adres kan wijzigen. In de code bewaart een gebruiker alleen voornaam, "
            "achternaam, e-mail, wachtwoord, rol en workshopcode (tabel user; UpdateMyAccountRequest). Een adres bestaat niet.",
            "Issue BE #206 beschrijft dat de kaartendpoints metingen eerst live bij meetjestad.net lazen. Nu lezen ze uit de eigen database die de ingest-worker vult (PR #207). "
            "Een codecommentaar in utility/MeasurementDeduplicator.java zegt nog dat de backend metingen niet bewaart; dat is verouderd.",
        ]),
        Para("Verdere uitleg van de begrippen staat in de Woordenlijst, de structuur van de gegevens in het Domeinmodel, de volgorde van het werk in Prioritering en de endpoints in het API-document."),
        Heading("Bronnen en controle"),
        Bullets([
            "Backend: OntdekIT/Software-BackEnd, commit e104152e572449be91d75b1d86a3bcecd6d4f5d0 (origin/s3nj26_dev). Frontend: OntdekIT/Software-FrontEnd, commit 13fc1e2f086ea4c2c52c37188294b6e3921bfebd (origin/s3nj26_dev).",
            "Issues en pull requests: gh issue list en gh pr list voor Software-BackEnd, Software-FrontEnd en Software-Documents (ook gesloten), opgehaald op 2026-11-17. Bord Sem3 2026 (project 17).",
            "Code: controllers, SecurityConfiguration, StationMonitorService, IngestWorker, OverviewCalculator en de routes in src/main.jsx. Snelheid van NFR-01 is eenmalig lokaal gemeten op de draaiende stack (http://localhost:8082).",
            "Het bewijs per wens staat in de tabellen van dit document; de diagrammen zijn daaruit afgeleid. Datum: 2026-11-17.",
        ]),
        Para("**Onduidelijk gebleven:** of de wensen door de opdrachtgever zijn bevestigd (issue Documents #98 staat open); de productiesnelheid van de endpoints; "
             "of de toegankelijkheidseisen (WCAG AA) gehaald worden; en of er in het oude semester-document wensen stonden die inmiddels zijn vervallen, omdat die documenten als Word-bestand niet volledig zijn nagelopen."),
    ]
    return Document(meta=Meta("Analysedocument", "Wat het systeem moet doen, in gewone taal.", [("Datum", "2026-11-17"), ("Bron", "backend e104152, frontend 13fc1e2")]),
                    blokken=b, voettekst="MB Ontdekt - ClimateChecker - analyse")
