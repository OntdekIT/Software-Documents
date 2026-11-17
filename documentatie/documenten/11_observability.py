"""11 Observability van MB Ontdekt (technische-verantwoording-recept)."""
from pathlib import Path
import json, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from docgen import Bullets, Code, Document, Heading, Image, Meta, Note, Para, Table

D = Path(__file__).resolve().parents[1] / "diagrammen" / "architectuur" / "11_observability"
BR = "(commit backend e104152, frontend 13fc1e2, 2026-11-17)"
F = json.loads((D / "data.json").read_text())


def document() -> Document:
    ing = F["status_voorbeeld"]["ingest"]
    voorbeeld = json.dumps({"dataAsOf": F["status_voorbeeld"]["dataAsOf"], "ingest": {k: ing[k] for k in ("enabled", "lastSuccessAt", "lastError", "consecutiveFailures", "lastStoredCount", "stale", "staleAfterMinutes")}, "snapshot": F["status_voorbeeld"]["snapshot"]}, indent=1)
    rijen = [[k, str(v.get("info", 0)), str(v.get("warn", 0)), str(v.get("error", 0))] for k, v in F["logregels_per_pakket"].items()]
    return Document(
        meta=Meta(titel="Observability", ondertitel="Welke signalen MB Ontdekt afgeeft over zijn eigen gezondheid, en wie ze kan lezen.",
                  kopregels=[("Systeem", "MB Ontdekt / ClimateChecker"), ("Datum", "2026-11-17"), ("Bron", "code en live status")]),
        voettekst="MB Ontdekt · observability",
        blokken=[
            Para("Observability is hier: kun je van buiten zien of de data vers is en of de achtergrondtaken werken? Het antwoord in een zin: de backend geeft goede signalen af (status, versheidsheader, health-endpoints, logs en mail), maar in de repo's leest en alarmeert niets ze, en de frontend gebruikt ze nog niet."),
            Image(str(D / "signalen.png"), onderschrift="Figuur 1. Signalen: bronnen, kanalen en lezers. Bron: IngestWorker.java, IngestState, SnapshotController.java, DataFreshnessFilter.java, StationMonitorService.java, application.properties, Dockerfile " + BR, max_hoogte_mm=120),
            Heading("De kanalen"),
            Table(kop=["Kanaal", "Wat het zegt", "Toegang"],
                  rijen=[["GET /api/status", "laatste geslaagde en laatste mislukte ingest, aantal opeenvolgende fouten, volgende poging, aantal opgeslagen metingen, stale-vlag, snapshotversie", "publiek, JSON"],
                         ["Header X-Data-As-Of", "tijdstip van de laatste geslaagde ingest, op alle kaart-, station-, wijk-, meting-, snapshot- en statusantwoorden; via CORS leesbaar voor browsers", "publiek"],
                         ["/actuator/health/readiness", "UP, DEGRADED (data ouder dan 30 min, HTTP 200) of DOWN (database weg)", "publiek, zonder details"],
                         ["/actuator/health/liveness", "het proces leeft; controleert de database niet", "publiek"],
                         ["Docker HEALTHCHECK", "roept de readiness elke 30 s aan (start-period 60 s)", "binnen de container"],
                         ["Logs op stdout", "zie hieronder", "containerlogs"],
                         ["E-mail aan de eigenaar", "bij uitval van een station (een station zonder meting in 24 uur) en bij sensor- of locatiefouten", "alleen de eigenaar"]],
                  kolombreedtes=[3, 6, 2]),
            Para("Alleen health is als actuator-endpoint blootgesteld (management.endpoints.web.exposure.include=health). Er zijn geen metrics-endpoints (geen Prometheus of Micrometer-exporter in de afhankelijkheden die hier zijn nagelopen) en geen tracing."),
            Heading("Een echt statusantwoord"),
            Code(voorbeeld, onderschrift="Antwoord van GET /api/status op de lokale stack op 2026-11-17 (ingekort)."),
            Heading("Uitvalcontrole van stations"),
            Para("De StationMonitorService draait elke 300 seconden (station.monitor.downtime-check-interval-seconds). Voor elk station kijkt hij in de lokale database naar de metingen van de laatste 24 uur. Is er geen enkele meting, dan wordt het station inactief gezet en krijgt de eigenaar een e-mail. Ontbreken temperatuur, vochtigheid, fijnstof of een eigen GPS-positie, dan krijgt het station een foutvlag (tempError, humError, stofError, locError) en volgt een mail bij een omslag van de status. Die vlaggen verschijnen weer in de API. Het ophalen van metingen doet deze service niet meer; dat is de taak van de IngestWorker."),
            Heading("Logging"),
            Para("De code logt via SLF4J (Lombok @Slf4j). In de huidige bronnen staan geen System.out-aanroepen meer (pull request #193 verving ze). Er is geen eigen logconfiguratie (geen logback-bestand in resources), dus de standaard van Spring Boot geldt: tekst naar stdout. Foutlogs bevatten korte meldingen: de worker bewaart alleen klasse en melding (maximaal 200 tekens), geen volledige URL met parameters."),
            Table(kop=["Pakket", "info", "warn", "error"], rijen=rijen, kolombreedtes=[5, 1, 1, 1], uitlijning=["links", "rechts", "rechts", "rechts"]),
            Para("Tabel: aantal log-aanroepen in de broncode per niveau, geteld in de broncode. De pakketten ingest en snapshot loggen elke run (gestart, geslaagd met aantallen, mislukt met aantal opeenvolgende fouten en wachttijd, snapshot gebouwd met bouwtijd en grootte)."),
            Heading("Wat ontbreekt"),
            Bullets(["**Geen alarmering**: niets in de repo's stuurt een melding bij DEGRADED, een stale-vlag of een rij mislukte runs. docs/monitoring.md raadt aan een externe monitor te laten pollen (Beszel, Uptime Kuma of een uptime-check); of dat is ingericht is niet vast te stellen.",
                     "**De frontend leest de signalen niet**: er is in src/ geen gebruik van X-Data-As-Of, /api/status of /api/snapshot. De app toont dus niet dat de data oud is, ook al kan de backend dat melden. Dit is nagegaan in src/ op de genoemde commit.",
                     "**Geen metrics**: bijvoorbeeld responstijden, cache-treffers (de caches nemen wel statistieken op, recordStats) of ingest-duur zijn alleen in logs zichtbaar.",
                     "**Geen centrale logopslag**: logs leven in de container. Hoe lang ze bewaard blijven hangt van Dokploy af en is niet vast te stellen.",
                     "**Statusendpoint is publiek**: /api/status toont de laatste foutmelding (maximaal 200 tekens, zonder URL). Dat is bewust beperkt, maar het is een openbare bron."]),
            Heading("Bronnen en controle"),
            Bullets(["OntdekIT/Software-BackEnd, commit e104152e572449be91d75b1d86a3bcecd6d4f5d0: snapshot/, ingest/, features/station/StationMonitorService.java, application.properties, Dockerfile, docs/monitoring.md.",
                     "OntdekIT/Software-FrontEnd, commit 13fc1e2f086ea4c2c52c37188294b6e3921bfebd: src/ (zoekopdracht naar de signalen).",
                     "Lokale stack: GET /api/status op 2026-11-17."]),
            Para("**Onduidelijk:** welke monitor of alarmering in de echte omgevingen draait, hoe lang logs bewaard worden en of de healthcheck van Dokploy is ingesteld."),
        ],
    )
