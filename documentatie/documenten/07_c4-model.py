"""07 C4-model van MB Ontdekt, volgens documenttypes/c4-model.txt."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from docgen import Bullets, Document, Heading, Image, Meta, Note, Para, Table

D = Path(__file__).resolve().parents[1] / "diagrammen" / "architectuur" / "07_c4-model"
BR = "(commit backend e104152, frontend 13fc1e2, 2026-11-17)"


def document() -> Document:
    return Document(
        meta=Meta(titel="C4-model", ondertitel="De architectuur van MB Ontdekt in vier zoomniveaus: context, containers, componenten en code.",
                  kopregels=[("Systeem", "MB Ontdekt / ClimateChecker"), ("Datum", "2026-11-17"), ("Bron", "echte code en compose")]),
        voettekst="MB Ontdekt · C4-model",
        blokken=[
            Para("Het C4-model beschrijft een systeem in vier zoomniveaus, van ver weg naar dichtbij. Alle diagrammen in dit document zijn afgeleid uit de echte bronnen: rollen uit de code, containers uit docker-compose.yml, componenten uit de Java-pakketten en de imports. Elk onderschrift noemt de bron en de commit."),
            Heading("Niveau 1: Context"),
            Para("MB Ontdekt toont temperatuur en fijnstof uit het meetnet van meetstations. Drie soorten gebruikers werken ermee: een **bezoeker** zonder account bekijkt kaart, heatmap, wijken en dashboard (die endpoints zijn publiek). Een **meetstation-eigenaar** (rol USER) registreert zich met een workshop- en stationcode en beheert zijn stations. Een **beheerder** (ADMIN of SUPER_ADMIN) beheert gebruikers, workshopcodes, stations en de datadekking. De metingen komen van **meetjestad.net**; mail gaat via een SMTP-server (lokaal MailHog). De browser laadt de kaartachtergrond van OpenFreeMap en pictogrammen van de jsDelivr-CDN."),
            Image(str(D / "c4-niveau1-context.png"), onderschrift="Figuur 1. Contextdiagram. Bron: UserRole.java, application.properties (meetjestad.base-url, spring.mail.*), newmap.jsx (tegelstijl), index.html (CDN) " + BR + ".", max_hoogte_mm=140),
            Note("Het bestand src/utils/open-meteo.jsx (weerdienst Open-Meteo) wordt door geen enkel ander bestand geimporteerd. Open-Meteo is daarom geen extern systeem in gebruik en staat niet in het diagram. Dit is nagegaan in de broncode op de genoemde commit.", kop="Bewust weggelaten"),
            Heading("Niveau 2: Containers"),
            Para("De lokale stack draait vier containers in een compose-netwerk: de frontend (nginx met de gebouwde bestanden), de backend (Spring Boot), de database (MariaDB) en MailHog. De React-app zelf draait in de browser en praat rechtstreeks met de backend (REST, JSON, bearer-JWT). Alleen de backend benadert meetjestad.net en de database. De backend wacht met starten tot de database gezond is (depends_on service_healthy)."),
            Image(str(D / "c4-niveau2-containers.png"), onderschrift="Figuur 2. Containerdiagram. Bron: docker-compose.yml (lokale stack), ClimateChecker/pom.xml, Dockerfile van de frontend " + BR + ".", max_hoogte_mm=110),
            Table(kop=["Container", "Technologie", "Hostpoort"],
                  rijen=[["frontend", "nginx 1.27-alpine (gebouwde React-app)", "3000"], ["backend-api", "Spring Boot 3.3.5, Java 21", "8082"], ["mariaDB", "MariaDB 11.2", "3307"], ["mailhog", "MailHog v1.0.1", "1025 (SMTP), 8025 (web)"]],
                  kolombreedtes=[2, 5, 3]),
            Heading("Niveau 3: Componenten"),
            Heading("Backend", 2),
            Para("De backend is opgedeeld in pakketten per functie (features/*) plus de pakketten ingest, snapshot, cache, config, exception en utility. Het diagram toont de functionele pakketten en het aantal imports ertussen. De dwarsverbanden (config, exception, utility, cache) zijn weggelaten omdat bijna alles ze gebruikt. Twee pakketparen hangen wederzijds van elkaar af: station en measurement (10 en 7 imports) en neighbourhood en snapshot (2 en 7). Dat is een bekende zwakte: de pakketgrenzen zijn niet strikt gelaagd."),
            Image(str(D / "c4-niveau3-backend.png"), onderschrift="Figuur 3. Backendcomponenten. Bron: alle .java-bestanden onder ClimateChecker/src/main/java, import-telling in de broncode " + BR + ".", max_hoogte_mm=120),
            Heading("Frontend", 2),
            Para("De React-app heeft mappen voor pagina's (een per route), herbruikbare componenten, pure logica in utils (onder andere de IDW-interpolatie van de heatmap en de kleurschaal), hooks, de auth-provider en loaders. Alle backendverkeer loopt via utils/backend-api (axios met 15 seconden time-out)."),
            Image(str(D / "c4-niveau3-frontend.png"), onderschrift="Figuur 4. Frontendonderdelen. Bron: src/ van de frontend, import-telling in de broncode (commit frontend 13fc1e2, 2026-11-17).", max_hoogte_mm=110),
            Heading("Niveau 4: Code"),
            Para("Op dit niveau tekenen we geen diagram. De code zelf is de bron: per component staat in de README van de backend (sectie Dataflow) en in de OpenAPI-specificatie (docs/api/openapi.json) wat het doet. Kernklassen zijn IngestWorker (ingest), SnapshotService (snapshot), SecurityConfiguration en JwtAuthenticationFilter (config), StationMonitorService (station) en GlobalExceptionHandler (exception)."),
            Heading("Bronnen en controle"),
            Bullets(["Backend: OntdekIT/Software-BackEnd, commit e104152e572449be91d75b1d86a3bcecd6d4f5d0 (origin/s3nj26_dev).",
                     "Frontend: OntdekIT/Software-FrontEnd, commit 13fc1e2f086ea4c2c52c37188294b6e3921bfebd (origin/s3nj26_dev).",
                     "Containers: docker-compose.yml van de lokale stack, uitgelezen met docker compose-formaat (YAML).",
                     "Datum: 2026-11-17."]),
            Para("**Onduidelijk of niet vastgesteld:** hoe de frontend in test, acceptatie en productie wordt geserveerd (de compose hierboven is de lokale stack). De hostpoorten gelden alleen lokaal."),
        ],
    )
