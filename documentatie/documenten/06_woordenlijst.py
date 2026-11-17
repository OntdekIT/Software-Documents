"""06 Woordenlijst: begrippen uit de code en de issues van ClimateChecker."""
from docgen import Document, Meta, Heading, Para, Table, Note, Bullets

SHA_BE, SHA_FE = "e104152", "13fc1e2"
KB = [3, 8, 4]
KOP = ["Term", "Uitleg", "Bron"]

THEMAS = [
    ("Het meetnet", [
        ["Actueel", "Een meting telt als actueel als ze hoogstens 120 minuten oud is. Dit is instelbaar (snapshot.recency-minutes).", "snapshot/SnapshotProperties.java"],
        ["Dekking", "Het deel van de uur-meetmomenten waarop een station iets heeft gemeten. In de snapshot is dat het percentage uren (van de laatste 24) per station met minstens een meting. De aparte dekkingsberekening voor fijnstof telt per uur of dag of een station PM-waarden leverde.", "snapshot/OverviewCalculator.java, utility/DataCoverageLogic.java"],
        ["Fijnstof (PM2.5, PM10)", "Zeer kleine stofdeeltjes in de lucht. PM2.5 is kleiner dan 2,5 micrometer, PM10 kleiner dan 10 micrometer. De app toont ze naast temperatuur.", "measurement/Measurement.java"],
        ["Laatst bekende positie", "Heeft een meting geen geldige GPS-positie, dan krijgt ze de laatst bekende positie van het station. De meting is dan als overgenomen gemarkeerd (location_inherited).", "features/measurement/Measurement.java, issue BackEnd #185"],
        ["Late meting", "Een station heeft nog wel een meting, maar die is ouder dan de actualiteitsgrens, zodat er geen actuele waarde is. Reden late_meting in de snapshot.", "snapshot/OverviewCalculator.java"],
        ["Meetstation (station)", "Een fysiek apparaat dat temperatuur, vochtigheid en fijnstof meldt. Heeft een id, een registratiecode, een optionele eigenaar en vlaggen voor storingen.", "features/station/Station.java"],
        ["Meting", "Een regel met tijdstip, positie en de gemeten waarden van een station.", "features/measurement/Measurement.java"],
        ["Netwerkgat", "Een uur of dag waarin minder dan de helft van de stations die fijnstof kunnen meten, een PM-waarde leverde. Wijst eerder op een probleem in bron, koppeling of synchronisatie dan op een enkele sensor.", "utility/DataCoverageLogic.java (NETWORK_GAP_THRESHOLD 0,5)"],
        ["Sensorfout", "Een station stuurt recent wel metingen, maar zonder bruikbare temperatuur of PM2.5. Reden sensorfout in de snapshot. Het station heeft daarbij vaak een storingsvlag.", "snapshot/OverviewCalculator.java"],
        ["Storingsvlag", "Vier markeringen per station: temperatuur (temp_error), vochtigheid (hum_error), fijnstof (stof_error) en locatie (loc_error). Ze veranderen wanneer een waardesoort verdwijnt of terugkomt.", "features/station/StationMonitorService.java"],
        ["Uitval", "Een station dat in de laatste 24 uur niets meldde. Het station wordt op niet actief gezet en de eigenaar krijgt een bericht. In de snapshot is de reden uitval.", "features/station/StationMonitorService.java, snapshot/OverviewCalculator.java"],
        ["Wijk", "Een gebied in Tilburg met een naam en een grens. In de database heet de tabel region, in de code Neighbourhood. De waarde van een wijk is het gemiddelde van de stations binnen de grens.", "features/neighbourhood/"],
        ["Wijkgrens", "De hoekpunten (breedte en lengte) die samen de omtrek van een wijk vormen. Een meting hoort bij een wijk als haar positie binnen die omtrek valt.", "features/neighbourhood/NeighbourhoodCoords.java, GpsTriangulation.java"],
    ]),
    ("Gegevens binnenhalen en tonen", [
        ["Backoff", "Na een fout wacht de ingest-worker steeds langer voor een nieuwe poging: eerst 30 seconden, verdubbelend tot maximaal 30 minuten, met een beetje willekeur (jitter).", "ingest/BackoffPolicy.java, IngestProperties.java"],
        ["Dubbele meting", "Twee metingen van hetzelfde station op hetzelfde tijdstip. Ze worden samengevoegd tot een record; de meest complete wint.", "utility/MeasurementDeduplicator.java"],
        ["Eerlijk gebruik", "De afspraak dat de app de bron niet overbelast: minimaal 60 seconden tussen verzoeken en maximaal 30 verzoeken per uur.", "ingest/RequestLimiter.java, IngestProperties.java"],
        ["Heatmap", "Een kaart die temperatuur of PM2.5 als doorlopend kleurvlak toont, geinterpoleerd tussen de stations, los van wijkgrenzen.", "issue FrontEnd #184, pages/heatmap.jsx"],
        ["Ingest-worker", "De achtergrondtaak in de backend die elke 5 minuten nieuwe metingen bij meetjestad.net ophaalt en opslaat. Het is de enige plek die de externe bron aanroept.", "ingest/IngestWorker.java"],
        ["Inhaalperiode", "Na een lange stilstand haalt de worker hooguit 168 uur (zeven dagen) aan metingen in. De eerste keer op een lege database is het venster 24 uur.", "ingest/IngestProperties.java"],
        ["meetjestad.net", "De externe site van het netwerk Meet je stad waar de metingen vandaan komen.", "features/meetjestad/MeetJeStadService.java, application.properties"],
        ["Nagestuurde meting", "Een meting die later binnenkomt dan haar eigen tijdstip. De ingest laat daarom elk venster 10 minuten overlappen met het vorige.", "ingest/IngestProperties.java, issue BackEnd #175"],
        ["Snapshot", "Een voorberekend overzicht van het hele netwerk (stadsgemiddelde, wijken, stations, netwerkstatus, heatmappunten) dat na elke geslaagde ingest wordt ververst en aan de kaart wordt geleverd via /api/snapshot.", "snapshot/SnapshotService.java, issue BackEnd #206"],
        ["Tijdlijn (timelapse)", "De afspeelbare weergave van de afgelopen 24 uur op de kaart, uit 2 tot 48 stappen.", "issue FrontEnd #174, NeighbourhoodTimelapseResponse.java"],
        ["X-Data-As-Of", "Antwoordheader met het moment van de laatste geslaagde ingest, zodat de kaart kan tonen hoe vers de data is.", "snapshot/DataFreshnessFilter.java"],
    ]),
    ("Accounts en toegang", [
        ["Beheerder, superbeheerder", "De rollen ADMIN en SUPER_ADMIN. Beheerders beheren gebruikers, workshopcodes en stations. Alleen een superbeheerder mag een andere beheerder verwijderen of terugzetten naar gebruiker.", "features/user/UserRole.java, UserController.java"],
        ["Claimen", "Een station aan een gebruiker koppelen. Dat kan alleen voor een station dat nog geen eigenaar heeft.", "features/station/StationService.java"],
        ["JWT", "Het inlogtoken dat de backend uitgeeft na de e-mailverificatie. Het gaat mee als Authorization: Bearer.", "config/JwtService.java"],
        ["Overdragen", "De eigenaar (of een beheerder) geeft een station aan een andere gebruiker.", "features/station/endpoint/StationController.java, issue BackEnd #143"],
        ["Rate limiting", "Een begrenzing op het aantal verzoeken per minuut per IP-adres (standaard 20). Inloggen en wachtwoord herstellen hebben een eigen limiet van 5 pogingen per minuut.", "config/ratelimit/RateLimitingFilter.java, utility/RateLimiter.java"],
        ["Registratiecode", "Een unieke code per station (registration_code).", "features/station/Station.java"],
        ["Verificatiecode", "De cijfercode die per e-mail wordt gestuurd om in te loggen (type VERIFY_AUTH) of een wachtwoord te herstellen (type PASSWORD_RESET).", "features/user/authentication/TokenType.java"],
        ["Vertrouwd IP (trusted IP)", "Een IP-adres waarvandaan een gebruiker eerder heeft ingelogd. Vanaf zo'n adres vervalt de e-mailstap. Het adres wordt niet leesbaar bewaard maar als HMAC-hash met een geheime pepper.", "features/user/authentication/trustedip/TrustedIpService.java"],
        ["Workshop", "Een bouwworkshop waarin deelnemers een meetstation maken. In de app is dat een record met een code en een verloopdatum.", "features/workshop/Workshop.java"],
        ["Workshopcode", "De code uit een workshop waarmee iemand zich registreert en zijn station koppelt. Een code verloopt op een vastgestelde datum.", "features/workshop/Workshop.java, issue FrontEnd #162"],
    ]),
    ("Techniek en werkwijze", [
        ["Actuator, liveness en readiness", "De gezondheidscontroles van de backend. Liveness zegt of het proces draait, readiness of het klaar is voor verkeer (database en ingest in orde).", "docs/monitoring.md, application.properties"],
        ["Epic", "Een thema op het projectbord waaronder meerdere user stories vallen, bijvoorbeeld Datakwaliteit en betrouwbaarheid.", "bord Sem3 2026 (project 17)"],
        ["Flyway", "Het hulpmiddel dat de databasewijzigingen als genummerde migraties (V1_0_0 tot V1_3_0) uitvoert.", "db/migration/"],
        ["MoSCoW", "Indeling van wensen in Must, Should, Could en Won't have.", "bord Sem3 2026"],
        ["OTAP", "Ontwikkel-, test-, acceptatie- en productieomgeving.", "issues BackEnd #172 en #173"],
        ["Story points", "De schatting van de omvang van een taak op het bord (1, 2, 3, 5 of 8).", "bord Sem3 2026"],
        ["User story", "Een wens in de vorm Als gebruiker wil ik, zodat ik, met acceptatiecriteria.", "issues met het label userstories"],
    ]),
]


def document():
    b = [Para("Dit zijn de begrippen uit de andere documenten, kort uitgelegd. Elk begrip komt uit de code of uit de issues van het project; "
              "de derde kolom zegt waar. Binnen een thema staan ze op alfabet. Waarden zoals 120 minuten zijn de standaardwaarden uit de configuratie en "
              "kunnen per omgeving anders staan.")]
    for t, rijen in THEMAS:
        rijen = sorted(rijen, key=lambda r: r[0].lower())
        b.append(Heading(t))
        # In stukken van 6 rijen, zodat een tabel nooit als geheel naar de volgende pagina springt.
        for i in range(0, len(rijen), 6):
            b.append(Table(KOP, rijen[i:i + 6], kolombreedtes=KB))
    b += [
        Heading("Bronnen en controle"),
        Bullets([
            f"Backend: OntdekIT/Software-BackEnd, commit e104152e572449be91d75b1d86a3bcecd6d4f5d0 (origin/s3nj26_dev). Gelezen: de bestanden die in de derde kolom staan, application.properties en docs/monitoring.md.",
            "Frontend: OntdekIT/Software-FrontEnd, commit 13fc1e2f086ea4c2c52c37188294b6e3921bfebd (origin/s3nj26_dev), voor de heatmap en de pagina's.",
            "Issues en bord: GitHub-issues in beide repo's en het bord Sem3 2026 (project 17) van OntdekIT, opgehaald op 2026-11-17.",
            "Datum van dit document: 2026-11-17.",
        ]),
        Para("**Onduidelijk gebleven:** het begrip hotspot en coolspot uit issue FrontEnd #184 is alleen in een testbestand (utils/interpolation.test.js) teruggevonden, "
             "niet in de schermen, daarom staat het hier niet. De term ingest-worker komt alleen in de code en in PR BackEnd #207 voor, niet in een user story."),
    ]
    return Document(meta=Meta("Woordenlijst", "De begrippen uit de documenten, kort uitgelegd.", [("Datum", "2026-11-17"), ("Bron", f"backend {SHA_BE}, frontend {SHA_FE}")]),
                    blokken=b, voettekst="MB Ontdekt - ClimateChecker - woordenlijst")
