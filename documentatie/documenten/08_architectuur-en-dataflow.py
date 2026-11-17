"""08 Architectuur en dataflow van MB Ontdekt (technische-verantwoording-recept)."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from docgen import Bullets, Document, Heading, Image, Meta, Note, Para, Table

D = Path(__file__).resolve().parents[1] / "diagrammen" / "architectuur" / "08_architectuur-en-dataflow"
BR = "(commit backend e104152, 2026-11-17)"


def document() -> Document:
    return Document(
        meta=Meta(titel="Architectuur en dataflow", ondertitel="Hoe een meting van de sensor op het scherm komt, en waarom een verzoek van de app meetjestad.net nooit aanroept.",
                  kopregels=[("Systeem", "MB Ontdekt / ClimateChecker"), ("Datum", "2026-11-17"), ("Bron", "backend-code")]),
        voettekst="MB Ontdekt · architectuur en dataflow",
        blokken=[
            Para("Dit document beschrijft de opbouw van de backend en de weg die de data aflegt. Alle diagrammen zijn uit de code afgeleid of per stap met bestand en regel onderbouwd. De containers en pakketten staan in het C4-model."),
            Heading("De kern in een alinea"),
            Note("Een achtergrondtaak (IngestWorker) haalt elke 300 seconden nieuwe metingen bij meetjestad.net, slaat ze idempotent op in MariaDB en rekent daarna alle antwoorden voor de kaart in een keer opnieuw uit (snapshots, in geheugen). De endpoints serveren die snapshots. Een verzoek van de app raakt meetjestad.net dus nooit. Gevolg: de getoonde data is zo oud als de laatste geslaagde ingest, en dat is zichtbaar via X-Data-As-Of en /api/status."),
            Heading("Dataflow"),
            Image(str(D / "dataflow.png"), onderschrift="Figuur 1. Dataflow van sensor tot scherm. Bron: IngestWorker.java, SnapshotService.java, SnapshotController.java, application.properties (waarden zijn de defaults) " + BR, max_hoogte_mm=90),
            Table(kop=["Instelling", "Default", "Betekenis"],
                  rijen=[["ingest.interval-seconds", "300", "tijd tussen runs"], ["ingest.overlap-minutes", "10", "overlap met het vorige venster"], ["ingest.max-requests-per-hour", "30", "bovengrens aanroepen naar de bron"], ["ingest.min-request-interval-seconds", "60", "minimale tussentijd"], ["ingest.backoff-initial/max-seconds", "30 / 1800", "wachttijd na een fout"], ["snapshot.now-tolerance-seconds", "300", "tot hoe ver van nu een verzoek uit de snapshot komt"], ["map.cache.ttl-seconds", "60", "Caffeine-cache voor andere tijdstippen"], ["ingest.stale-after-minutes", "30", "daarna is de readiness DEGRADED"]],
                  kolombreedtes=[4, 2, 5]),
            Heading("De ingest-run stap voor stap"),
            Para("Een run heeft vier mogelijke uitkomsten (SUCCESS, FAILURE, RATE_LIMITED, BUSY). Runs overlappen nooit (single-flight lock). Na elke run, ook een mislukte, worden de snapshots opnieuw gebouwd zodat de status klopt. De lus sterft nooit: een onverwachte fout wordt gelogd en de volgende run wordt gepland."),
            Image(str(D / "sequentie-ingest.png"), onderschrift="Figuur 2. Sequentiediagram van een ingest-run. Elke stap noemt de regel in IngestWorker.java of SnapshotService.java " + BR, max_hoogte_mm=170),
            Heading("Een kaartverzoek"),
            Para("Het controller-pad vraagt eerst of de snapshot het verzoek kan beantwoorden: dat kan als het gevraagde tijdstip binnen 300 seconden van nu ligt (of bij de standaard time-lapse van 24 uur met 24 of 25 stappen). Voor andere tijdstippen berekent de service het uit de lokale database en cachet het resultaat een minuut (Caffeine). Elk kaartantwoord krijgt de header X-Data-As-Of."),
            Image(str(D / "sequentie-kaartverzoek.png"), onderschrift="Figuur 3. Sequentiediagram van een verzoek voor het huidige tijdstip. Bron: DataFreshnessFilter.java, NeighbourhoodController.java, SnapshotService.java, NeighbourhoodService.java " + BR, max_hoogte_mm=150),
            Heading("De API in een oogopslag"),
            Para("De API heeft 37 operaties onder /api, ingedeeld in acht groepen. Het diagram is afgeleid uit docs/api/openapi.json, dat de backend zelf uit de controllers samenstelt en dat een test (OpenApiSpecTest) gelijk houdt aan de code. Een slotje betekent dat de operatie in de specificatie een bearer-JWT eist; de volledige toegangsregels staan in het beveiligingsdocument."),
            Image(str(D / "api-kaart.png"), onderschrift="Figuur 4. Operaties per groep. Bron: docs/api/openapi.json " + BR, max_hoogte_mm=110),
            Heading("Ontwerpkeuzes die de architectuur bepalen"),
            Bullets(["Een enkele aanroeper van de externe bron: gevolg van de beslissing in het ADR-document (worker en snapshots).",
                     "Flyway beheert het schema; Hibernate valideert alleen (spring.jpa.hibernate.ddl-auto=validate in application.properties). Let op: de lokale compose zet SPRING_JPA_HIBERNATE_DDL_AUTO op update.",
                     "Tijden zijn intern UTC (application.timezone=UTC); legacy-endpoints houden hun notatie dd-MM-yyyy HH:mm:ss.",
                     "Een tweede achtergrondtaak, StationMonitorService, controleert elke 5 minuten of stations uitvallen en mailt de eigenaar."]),
            Heading("Bronnen en controle"),
            Bullets(["OntdekIT/Software-BackEnd, commit e104152e572449be91d75b1d86a3bcecd6d4f5d0 (origin/s3nj26_dev), README sectie Dataflow, docs/api/openapi.json.",
                     "Datum: 2026-11-17."]),
            Para("**Onduidelijk:** de werkelijke interval en limieten in test, acceptatie en productie (de defaults gelden tenzij omgevingsvariabelen ze overschrijven; die omgevingen zijn niet toegankelijk). Het formaat van de bron meetjestad.net is niet apart gedocumenteerd; de README zegt dat de bron geen vast limiet publiceert."),
        ],
    )
