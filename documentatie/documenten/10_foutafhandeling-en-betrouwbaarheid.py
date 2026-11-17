"""10 Foutafhandeling en betrouwbaarheid (technische-verantwoording-recept)."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from docgen import Bullets, Document, Heading, Image, Meta, Note, Para, Table

D = Path(__file__).resolve().parents[1] / "diagrammen" / "architectuur" / "10_foutafhandeling-en-betrouwbaarheid"
BR = "(commit backend e104152, 2026-11-17)"


def document() -> Document:
    return Document(
        meta=Meta(titel="Foutafhandeling en betrouwbaarheid", ondertitel="Hoe de backend fouten vertaalt naar antwoorden, en hoe hij blijft werken als de databron of een onderdeel uitvalt.",
                  kopregels=[("Systeem", "MB Ontdekt / ClimateChecker"), ("Datum", "2026-11-17"), ("Bron", "code en live aanroepen")]),
        voettekst="MB Ontdekt · foutafhandeling en betrouwbaarheid",
        blokken=[
            Heading("Foutantwoorden van de API"),
            Para("Een centrale GlobalExceptionHandler (@RestControllerAdvice, uit issue 199 en pull request #203) vertaalt uitzonderingen naar een vaste JSON-vorm met de velden timestamp, error, statusCode en message. De 401 (geen of ongeldig token) en 403 (onvoldoende rol) komen uit eigen handlers in de beveiligingsketen en hebben dezelfde vorm. Een vangnet zet elke onverwachte uitzondering om in een 500 met een algemene melding, zonder interne details, en logt de stack."),
            Image(str(D / "fouttoewijzing.png"), onderschrift="Figuur 1. Van uitzondering naar HTTP-status. Bron: GlobalExceptionHandler.java, RestAuthenticationEntryPoint.java, RestAccessDeniedHandler.java, RateLimitingFilter.java " + BR, max_hoogte_mm=120),
            Para("Zo ziet dat er in werkelijkheid uit (lokaal opgevraagd):"),
            Table(kop=["Verzoek", "Antwoord"],
                  rijen=[["GET /api/meetstation/99999", "404 NOT_FOUND, message Station not found"],
                         ["GET /api/neighbourhood/history?timestamp=bogus", "400 BAD_REQUEST, message Timestamp must be in ISO 8601 format"],
                         ["GET /api/users zonder token", "401 UNAUTHORIZED, message Authentication is required to access this resource"],
                         ["DELETE /api/status", "405 METHOD_NOT_ALLOWED"],
                         ["POST login met kapotte JSON", "400 BAD_REQUEST, message Malformed or unreadable request body"]],
                  kolombreedtes=[4, 6]),
            Note("De authenticatie-endpoints (/api/authentication/*) antwoorden bewust met platte tekst in plaats van JSON (de frontend toont de tekst direct). Een login met een fout wachtwoord geeft lokaal 400 met de tekst Invalid email and/or password. Dit is een uitzondering op de vaste vorm en staat zo in UserAuthenticationController.java.", kop="Uitzondering op de vaste vorm"),
            Heading("De databron valt uit: de ingest-worker"),
            Para("De backend roept meetjestad.net alleen aan vanuit de IngestWorker. Valt de bron uit (429, 5xx, time-out), dan krijgt de app daar niets van te zien behalve dat de data ouder wordt: de snapshots en de database blijven bruikbaar. De worker begrenst zichzelf (maximaal 30 verzoeken per uur, minimaal 60 seconden tussen verzoeken), laat nooit twee runs tegelijk lopen en wacht na een fout exponentieel langer, met jitter. Een Retry-After van de bron wint als die langer is. De lus zelf kan niet doodgaan: een onverwachte fout wordt gelogd en de volgende run wordt gepland. Met ingest.enabled=false doet de worker niets (kill switch)."),
            Image(str(D / "ingest-toestanden.png"), onderschrift="Figuur 2. Uitkomsten van een ingest-run. Bron: IngestWorker.java (regelnummers in het diagram), BackoffPolicy.java, application.properties " + BR, max_hoogte_mm=125),
            Table(kop=["Opeenvolgende fout", "Wachttijd (met jitter)"],
                  rijen=[["1", "15 tot 30 s"], ["2", "30 tot 60 s"], ["3", "60 tot 120 s"], ["4", "2 tot 4 min"], ["5", "4 tot 8 min"], ["6", "8 tot 16 min"], ["7 en daarna", "15 tot 30 min (plafond 1800 s)"]],
                  kolombreedtes=[3, 5]),
            Para("De tabel is berekend met de formule uit BackoffPolicy (begin 30 s, verdubbelen, plafond 1800 s, jitter tussen 50 en 100 procent) en de defaults uit application.properties. De unit tests IngestPolicyTest en IngestWorkerTest bestaan in de repo; dit document heeft de tests niet opnieuw uitgevoerd."),
            Heading("Verouderde data is geen storing"),
            Para("Worden de gegevens oud, dan blijft de app verkeer bedienen met de laatst bekende staat. De readiness-check meldt DEGRADED (HTTP 200, dus geen herstart) zodra de laatste geslaagde ingest ouder is dan 30 minuten. Alleen een databasefout maakt de readiness DOWN. Zo start een tijdelijk probleem bij de bron geen onnodige herstartlus."),
            Image(str(D / "gezondheid.png"), onderschrift="Figuur 3. Gezondheidstoestanden. Bron: application.properties (management.*), IngestHealthIndicator.java; de live readiness antwoordde op 2026-11-17 {\"status\":\"UP\"} " + BR, max_hoogte_mm=70),
            Heading("Andere betrouwbaarheidsmaatregelen"),
            Bullets(["**Idempotent opslaan**: metingen hebben de sleutel station plus tijdstip. Overlap, herstart en dubbele runs geven geen dubbelen (MeasurementIngestService).",
                     "**Atomair verwisselen**: snapshots worden buiten de lock berekend en in een keer ingewisseld (AtomicReference). Lezers zien nooit een mengsel.",
                     "**Opstarten zonder snapshot**: wordt uit de database opgebouwd, nooit uit een live aanroep. Een lege database geeft lege lijsten.",
                     "**Inhalen na stilstand** is begrensd op 168 uur (ingest.max-catch-up-hours).",
                     "**Fouten in de uitvalcontrole** worden per station gelogd en tellen mee in een samenvattende logregel; een fout bij een station stopt de rest niet (StationMonitorService).",
                     "**Mail faalt zacht**: een onbereikbare mailserver maakt de app niet DOWN (mail-health staat uit). Bij vergeten wachtwoord wordt een mislukte mail gelogd en krijgt de gebruiker toch hetzelfde antwoord.",
                     "**Frontend**: elke aanroep heeft een time-out van 15 seconden. Een bron die faalt toont de laatst bekende data uit een stale-while-revalidate-cache (sessionStorage) in plaats van een foutpagina (use-source.js en swr-cache.js)."]),
            Heading("Zwakke plekken"),
            Bullets(["**Een enkele backend-instantie**: worker, rate limiter en snapshots leven in het geheugen van een proces. Een tweede instantie zou dubbel ophalen en eigen limieten hebben. Dat is een bewuste eenvoud, maar het is geen hoge beschikbaarheid.",
                     "**Snapshot weg bij herstart**: na een herstart wordt de snapshot opnieuw uit de database gebouwd; de status van de worker (laatste fout, aantal fouten) begint weer leeg.",
                     "**Geen alarm**: er is in de repo's niets dat bij DEGRADED of een mislukte ingest een melding stuurt. De signalen zijn er (zie het document over observability), het alarmeren niet.",
                     "**Ongebruikte instelling**: station.monitor.measurement-fetch-interval-seconds wordt door StationMonitorService ingelezen maar niet meer gebruikt (het ophalen deed de oude 6-uurs-sync).",
                     "**Issue 199 staat nog open** terwijl de pull request gemerged is; de belangrijkste punten (centrale handler, 401 en 403) staan wel in de code."]),
            Heading("Bronnen en controle"),
            Bullets(["OntdekIT/Software-BackEnd, commit e104152e572449be91d75b1d86a3bcecd6d4f5d0 (origin/s3nj26_dev): exception/, ingest/, config/, application.properties, README (Dataflow).",
                     "OntdekIT/Software-FrontEnd, commit 13fc1e2f086ea4c2c52c37188294b6e3921bfebd: hooks/use-source.js, utils/swr-cache.js, utils/backend-api.jsx.",
                     "Live aanroepen op de lokale stack, 2026-11-17. Backoff-tabel in diagrammen/architectuur/10_.../backoff.json."]),
            Para("**Onduidelijk:** hoe vaak de bron in de praktijk faalt (er is geen historie van mislukte runs bewaard buiten de logs en lastError van het huidige proces) en wat een DOWN-readiness in Dokploy precies doet (de healthcheck staat volgens docs/deployment.md te configureren, maar de omgevingen zijn niet toegankelijk). De 503 bij DOWN volgt uit docs/monitoring.md en is niet live uitgelokt."),
        ],
    )
