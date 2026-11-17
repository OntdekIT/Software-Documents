"""12 Deployment en omgevingen (technische-verantwoording-recept)."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from docgen import Bullets, Document, Heading, Image, Meta, Note, Para, Table

D = Path(__file__).resolve().parents[1] / "diagrammen" / "architectuur" / "12_deployment-en-omgevingen"
BR = "(commit backend e104152, frontend 13fc1e2, 2026-11-17)"


def document() -> Document:
    return Document(
        meta=Meta(titel="Deployment en omgevingen", ondertitel="Hoe een wijziging van een commit naar een draaiende omgeving gaat, en wat daarvan in de praktijk werkt.",
                  kopregels=[("Systeem", "MB Ontdekt / ClimateChecker"), ("Datum", "2026-11-17"), ("Bron", "workflows, compose, GitHub")]),
        voettekst="MB Ontdekt · deployment en omgevingen",
        blokken=[
            Note("Ontwerp: een keer bouwen, daarna promoveren. Het image wordt eenmalig gebouwd en getagd met de commit (sha-1a2b3c4). Naar test, acceptatie of productie gaat exact hetzelfde image als extra tag. Alleen de omgevingsvariabelen verschillen. Werkelijkheid op 2026-11-17: de pijplijn bouwt en tagt wel, maar de laatste stap, de Dokploy-webhook, wordt overgeslagen omdat het secret niet is ingesteld. Er is dus nog geen geautomatiseerde uitrol naar een omgeving.", kop="Kort gezegd"),
            Heading("Wat er bij een push gebeurt"),
            Para("Een push naar s3nj26_dev start in de backend-repo twee workflows. ci.yml draait alle tests (mvn verify op JDK 21, inclusief de Testcontainers-integratietests). deploy.yml bouwt het Docker-image, publiceert het als ghcr.io/ontdekit/climatechecker-backend:sha-<commit> en zet de vlottende tag test erop. De deploy-job wacht niet op CI: ze lopen parallel, dus een rode CI blokkeert de test-tag niet. Daarna roept de workflow de Dokploy-webhook van de omgeving aan, als het bijbehorende secret bestaat."),
            Image(str(D / "pijplijn.png"), onderschrift="Figuur 1. De pijplijn. Bron: .github/workflows/deploy.yml en ci.yml (backend), ghcr.yml (frontend); beide als YAML uitgelezen " + BR, max_hoogte_mm=105),
            Heading("Wat vast te stellen was over de uitrol"),
            Table(kop=["Waarneming", "Bewijs"],
                  rijen=[["Laatste deploy-run (id 44190061175, commit e104152) slaagde", "gh run view: conclusie success"],
                         ["De webhookstap schreef: No Dokploy webhook secret for 'test', skipping deploy.", "log van de stap Trigger Dokploy deploy; WEBHOOK_TEST was leeg"],
                         ["In de GitHub-omgeving test staan 0 secrets; alleen de omgeving test bestaat", "gh api repos/OntdekIT/Software-BackEnd/environments en .../test/secrets"],
                         ["Een run blijft groen zonder webhook", "ontwerp van deploy.yml (exit 0), bewust zo opgezet"]],
                  kolombreedtes=[6, 5]),
            Para("Gevolg: de beschrijving die vaak wordt gegeven, 'een push naar s3nj26_dev rolt uit naar test via Dokploy', klopt voor het bouwen en publiceren van het image, maar niet voor de uitrol zelf. Zolang de webhook niet is gekoppeld, moet iemand in Dokploy handmatig herstarten of de webhook alsnog instellen. Het ontwerp daarvoor staat in docs/deployment.md."),
            Heading("De omgevingen"),
            Image(str(D / "omgevingen.png"), onderschrift="Figuur 2. Promoveren door te hertaggen. Bron: deploy.yml (workflow_dispatch, opties test, acceptance, production), docs/deployment.md " + BR, max_hoogte_mm=65),
            Table(kop=["Omgeving", "Trigger", "Image-tag", "Goedkeuring volgens docs"],
                  rijen=[["Lokaal", "docker compose", "lokaal gebouwd", "nee"], ["Test", "push naar s3nj26_dev", "test", "nee"], ["Acceptatie", "handmatig", "acceptance", "aanbevolen"], ["Productie", "handmatig", "production", "verplicht (reviewer)"]],
                  kolombreedtes=[2, 3, 2, 3]),
            Para("Promoveren gaat via Actions, workflow Deploy, Run workflow, met de omgeving en de source_tag van een eerder geteste commit. Terugdraaien is dezelfde handeling met de tag van de vorige goede versie. Flyway-migraties worden niet teruggedraaid."),
            Heading("De containers in test, acceptatie en productie"),
            Para("docker-compose-prod.yml is het sjabloon voor alle drie. Het bevat geen geheimen: JWT_SECRET, TRUSTED_IP_PEPPER, FRONTEND_HOST en CORS_ALLOWED_ORIGINS zijn verplicht (compose weigert te starten zonder). De database publiceert geen poort, gebruikt een benoemd volume en heeft een healthcheck; de backend wacht op een gezonde database en de frontend op een gezonde backend."),
            Image(str(D / "compose-prod.png"), onderschrift="Figuur 3. Services in docker-compose-prod.yml. Bron: ClimateChecker/docker-compose-prod.yml (uitgelezen) " + BR, max_hoogte_mm=70),
            Heading("Het image"),
            Bullets(["Multi-stage Dockerfile: Maven met Java 21 bouwt de jar (tests worden daar overgeslagen, die draaien in CI), de runtime is eclipse-temurin:21-jre.",
                     "De app draait als niet-root gebruiker app, poort 8082, heap als percentage (MaxRAMPercentage=75).",
                     "HEALTHCHECK op /actuator/health/readiness (30 s interval, 60 s opstarttijd, wat Flyway-migraties de ruimte geeft).",
                     "Frontend: nginx 1.27-alpine met SPA-fallback en beveiligingsheaders; VITE_BACKEND_API_URL wordt bij het bouwen in de bundel gebakken. Een frontend-image hoort dus bij precies een backend-URL, waardoor drie omgevingen drie frontend-builds vragen."]),
            Heading("Frontend en de verschillen met het ontwerp"),
            Bullets(["De frontend-workflow ghcr.yml publiceert alleen een image en een semver-tag bij een push naar main of s3nj26, niet bij een push naar s3nj26_dev. Er is dus geen frontend-image voor de testomgeving vanuit de ontwikkelbranch.",
                     "**Mogelijk het verkeerde frontend-image**: ghcr.yml bouwt met docker build -t climatechecker-frontend . zonder --target. De laatste stage in de Dockerfile is dev (Vite-ontwikkelserver op poort 5173, vandaar ook docker run -p 3000:5173 in de test), niet release (nginx). Daarmee is het gepubliceerde image waarschijnlijk de ontwikkelserver, zonder VITE_BACKEND_API_URL als build-argument. Dit is uit de bestanden afgeleid en niet door het image te starten bevestigd.",
                     "De E2E-workflow (Cypress) van de frontend faalde op de laatste run voor commit 13fc1e2; de reden is niet onderzocht.",
                     "De commentaar in ci.yml noemt een workflow ghcr.yml in de backend-repo; die bestaat daar niet (de image-stap zit in deploy.yml).",
                     "docker-compose-prod.yml zet SPRING_PROFILES_ACTIVE op docker als standaard, maar er is geen application-docker.properties; het profiel doet niets.",
                     "De lokale compose (/OntdekIT/docker-compose.yml) zet SPRING_JPA_HIBERNATE_DDL_AUTO op update; het prod-sjabloon zet validate."]),
            Heading("Waar op te letten"),
            Bullets(["**Productie en acceptatie bestaan nog niet als GitHub-omgeving**: alleen test staat in de repo-instellingen. Een eerste run naar production maakt de omgeving zonder verplichte reviewer aan, tenzij die eerst wordt ingesteld.",
                     "**De deploy loopt parallel aan CI**: een kapotte build kan de test-tag krijgen. Promoveer alleen tags met een groene CI.",
                     "**De webhook-URL is een geheim** en hoort alleen in de GitHub-omgeving te staan, nooit in de repo."]),
            Heading("Bronnen en controle"),
            Bullets(["OntdekIT/Software-BackEnd, commit e104152e572449be91d75b1d86a3bcecd6d4f5d0: .github/workflows/deploy.yml en ci.yml, ClimateChecker/Dockerfile en docker-compose-prod.yml, docs/deployment.md.",
                     "OntdekIT/Software-FrontEnd, commit 13fc1e2f086ea4c2c52c37188294b6e3921bfebd: Dockerfile, nginx.conf, .github/workflows/ghcr.yml en e2e.yml.",
                     "GitHub via gh (alleen lezen): deploy-run 44190061175, omgevingen en secrets van de backend-repo, op 2026-11-17."]),
            Para("**Onduidelijk:** de inrichting van Dokploy zelf (projecten, domeinen, healthchecks, backups per omgeving), of acceptatie en productie bestaan, en welke frontend-URL bij welke omgeving hoort. Die zijn niet te lezen uit de repo's."),
        ],
    )
