"""Testdocument van MB Ontdekt / ClimateChecker, gebouwd uit echte testrapporten.

Bouw: python documentatie/bouw/build.py documentatie/documenten/15_testdocument.py --uit documentatie/pdf/Testdocument.pdf
Cijfers komen uit documentatie/diagrammen/testdocument/gegevens.json (testrapporten, workflows en gh run list).
"""
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _proces import schoon
from docgen import Bullets, Code, Document, Heading, Image, Meta, Note, Para, Spacer, Table

HIER = Path(__file__).resolve().parent
DG = HIER.parent / "diagrammen" / "testdocument"
D = json.loads((DG / "gegevens.json").read_text(encoding="utf-8"))
BE, FE = D["shas"]["backend"], D["shas"]["frontend"]
SB, SF = BE[:7], FE[:7]
K = D["backend"]["klassen"]

GEBIEDEN = {
    "api": "API en beveiliging (MockMvc)", "config": "Configuratie, JWT, CORS en rate limiting",
    "user": "Gebruikers en authenticatie", "station": "Meetstations", "measurement": "Metingen",
    "meetJestad": "Koppeling met meetjestad.net", "neighbourhood": "Wijken", "snapshot": "Snapshot en kaartendpoints",
    "ingest": "Ingest-worker (data ophalen en bewaren)", "utility": "Hulpklassen (IP, ontdubbelen, datadekking)",
    "workshop": "Workshops", "cache": "Cache", "health": "Gezondheidscontrole",
    "integration": "Integratie met echte database (Testcontainers)",
    "StationMonitorService": "Uitvalcontrole van meetstations",
}


def top(x):
    return x["pakket"].split(".")[0] or "(root)"


def som(lijst, v):
    return sum(x[v] for x in lijst)


def laag(l):
    return [x for x in K if x["laag"] == l]


def gebiedstabel(sleutel):
    rijen = []
    for x in sorted([k for k in K if top(k) == sleutel], key=lambda k: k["klasse"]):
        ex = x["voorbeelden"][0] if x["voorbeelden"] else "(overgeslagen)"
        ex = ex if len(ex) < 70 else ex[:67] + "..."
        st = f"{x['overgeslagen']} overgeslagen" if x["overgeslagen"] else "slaagt"
        rijen.append([x["klasse"], str(x["tests"]), st, ex])
    return Table(kop=["Testklasse", "Tests", "Status", "Voorbeeld van een testnaam"], rijen=rijen,
                 uitlijning=["links", "rechts", "links", "links"], kolombreedtes=[4, 1, 2, 6])


def document() -> Document:
    totaal = som(K, "tests")
    skip = som(K, "overgeslagen")
    fe = D["frontend"]["run"]["tests"]
    cy = D["frontend"]["cypress"]
    cj = D["backend"]["dekking_totaal"]
    runs = D["ci_runs"]
    b = []
    b += [
        Para(
            "Dit document beschrijft hoe de app MB Ontdekt (ClimateChecker) wordt getest, met de aantallen "
            f"en uitkomsten zoals ze echt zijn. De backend-cijfers komen uit de testrapporten (surefire) en het "
            f"JaCoCo-rapport van CI-run {D['ci_run_backend']} op commit {SB}. De frontend-cijfers komen uit een verse run "
            f"van `npm test` op commit {SF}. Wat niet vast te stellen was, staat achteraan."
        ),
        Note(
            f"Backend: {totaal} tests, {totaal - skip} geslaagd, {skip} overgeslagen, 0 mislukt. "
            f"Regeldekking {cj['line']['pct']}%. Frontend: {fe} tests, alle geslaagd, maar in geen enkele CI-workflow "
            f"aangesloten. Cypress: {sum(len(c['it']) for c in cy if not c['overgeslagen'])} actieve e2e-test, "
            f"in CI {runs['Software-FrontEnd']['E2E tests']['failure']} van {runs['Software-FrontEnd']['E2E tests']['n']} runs mislukt.",
            kop="Kort gezegd"),
        Heading("1. Teststrategie"),
        Para(
            "De app bestaat uit een Spring Boot-backend (Java 21, JUnit 5, Mockito, Spring Test, Testcontainers, JaCoCo) en een "
            "React-frontend (Vite, `node:test`, Cypress). De strategie volgt de testpiramide: veel snelle unit-tests, daarboven "
            "tests die de Spring-context en de beveiligingsketen via MockMvc op een H2-database gebruiken, daarboven "
            "integratietests op een echte MariaDB en bovenaan een end-to-end-test van het inloggen. Bronnen: "
            "`ClimateChecker/pom.xml`, `src/test/java/...`, `package.json`, `cypress/e2e/`."
        ),
        Table(kop=["Niveau", "Wat er getoetst wordt", "Gereedschap"],
              rijen=[
                  ["Unit", "Losse klassen: services, mappers, validators, filters, hulpklassen, frontend-functies", "JUnit 5 en Mockito (backend), node:test (frontend)"],
                  ["Spring-context en API", "HTTP-laag met volledige Spring Security-keten, JWT, foutafhandeling, OpenAPI-specificatie", "MockMvc op H2 (AbstractApiTest)"],
                  ["Integratie", "Flyway-migraties, JPA-mapping en queries op een echte MariaDB 11.2", "Testcontainers"],
                  ["End-to-end", "Inloggen met mailverificatie door de browser tegen de volledige stack", "Cypress, MariaDB en MailHog in CI"],
              ], kolombreedtes=[2, 6, 4]),
        Heading("2. Testsoorten en technieken", 2),
        Bullets([
            "**Normaalgeval en uitzondering**: bijvoorbeeld `ErrorHandlingApiTest` (16 tests) controleert per fout het statuscode- en berichtformaat.",
            "**Autorisatietests**: `AuthSecurityApiTest`, `StationSecurityApiTest` en `PathAliasApiTest` eisen dat muterende endpoints zonder login 401 of 403 geven.",
            "**Contracttests**: `OpenApiSpecTest` laat de test falen als de ingecheckte `docs/api/openapi.json` afwijkt van de code; `PostmanCollectionTest` controleert de Postman-collectie tegen die specificatie.",
            "**Configuratie-guards**: `JwtSecretGuardTest` en `DefaultCredentialsGuardTest` controleren dat de backend buiten dev/test niet start met standaardsleutels.",
            "**Tijd en timing** met een `MutableClock` in de ingest-tests, zodat tijdsafhankelijk gedrag deterministisch is.",
            "**Tijd- en groottebudget**: `SnapshotBudgetTest` meet een snapshot op realistische omvang (43 stations, 70 wijken).",
        ]),
        Heading("3. Testpiramide met werkelijke aantallen"),
        Image(str(DG / "testpiramide.png"),
              f"Figuur 1. Aantallen per laag. Bron: surefire-reports van CI-run {D['ci_run_backend']} (backend, commit {SB}), "
              f"`npm test` en cypress/e2e/*.cy.js (frontend, commit {SF}).",
              breedte_mm=165),
        Table(kop=["Laag", "Bestanden", "Tests", "Overgeslagen", "Mislukt"],
              rijen=[
                  ["Backend unit", str(len(laag("unit"))), str(som(laag("unit"), "tests")), "0", "0"],
                  ["Backend Spring-context en API", str(len(laag("api"))), str(som(laag("api"), "tests")), "0", "0"],
                  ["Backend integratie (Testcontainers)", str(len(laag("integratie"))), str(som(laag("integratie"), "tests")), str(som(laag("integratie"), "overgeslagen")), "0"],
                  ["Backend totaal", str(len(K)), str(totaal), str(skip), "0"],
                  ["Frontend unit (node:test)", str(len(D["frontend"]["unit_bestanden"])), str(fe), "0", str(D["frontend"]["run"]["fail"])],
                  ["Frontend e2e (Cypress)", str(len(cy)), str(sum(len(c["it"]) for c in cy)), str(sum(len(c["it"]) for c in cy if c["overgeslagen"])), "zie hoofdstuk 5"],
              ], uitlijning=["links", "rechts", "rechts", "rechts", "rechts"], kolombreedtes=[6, 2, 1, 2, 2]),
        Para(
            "De indeling van de backendklassen over de lagen is afgeleid uit de broncode: klassen die Testcontainers gebruiken zijn "
            "integratie, klassen met `@SpringBootTest` of `AbstractApiTest` zijn Spring-context/API, de rest is unit."
        ),
        Heading("Overgeslagen tests", 2),
        Para(
            f"In de CI-run zijn {skip} backendtests overgeslagen, allemaal in de map `integration`. Acht daarvan (`AuthEndpointsFeatureTest`, "
            "`UserRepositoryIntegrationTest`) staan op `@Disabled(\"Temporarily disabled due to Docker dependency issues\")`. Drie "
            "(`MeasurementIndexIntegrationTest`) hebben `@Testcontainers(disabledWithoutDocker = true)` en werden in de CI-run overgeslagen "
            "met de melding \"Docker is not available\". Op een machine met Docker draaien die laatste drie wel. De opmerking bovenin "
            "`ci.yml` zegt dat ook de Testcontainers-integratietests draaien; die bewering klopt dus niet volledig."
        ),
        Heading("Frontend unit-tests", 2),
        Table(kop=["Bestand (src/utils)", "Tests"],
              rijen=[[x["bestand"].replace("src/utils/", ""), str(x["tests"])] for x in D["frontend"]["unit_bestanden"]]
              + [["Totaal", str(fe)]],
              uitlijning=["links", "rechts"], kolombreedtes=[8, 1]),
        Para("De frontend-tests zijn gericht op zuivere logica (kleurschaal, interpolatie, statusbepaling, wijkenvergelijking, navigatie-items, SWR-cache). Componenten en schermen worden niet met unit-tests getoetst."),
        Heading("4. Testgevallen per gebied"),
        Para(
            "Per gebied staan de echte testklassen met het aantal tests en een voorbeeld van een testnaam uit het surefire-rapport. "
            "Een koppeling aan genummerde eisen (FR/UC) is niet gemaakt: in de testbronnen staan geen eis-nummers, en verzinnen zou de waarheid geweld aandoen."
        ),
    ]
    for sl in ["user", "api", "config", "station", "StationMonitorService", "measurement", "meetJestad", "ingest", "snapshot",
               "neighbourhood", "workshop", "utility", "cache", "health", "integration"]:
        kl = [k for k in K if top(k) == sl]
        if not kl:
            continue
        b += [Heading(f"{GEBIEDEN[sl]} ({som(kl, 'tests')} tests)", 2), gebiedstabel(sl)]
    b += [
        Heading("5. Continuous integration"),
        Para(
            "Beide repositories hebben GitHub Actions-workflows. Het diagram is afgeleid uit de workflowbestanden in `.github/workflows/` "
            "en de aantallen uit `gh run list` (de laatste 400 runs per repository)."
        ),
        Image(str(DG / "ci-pijplijn.png"),
              f"Figuur 2. Workflows, triggers, stappen en uitkomsten. Bron: .github/workflows/*.yml (backend {SB}, frontend {SF}) en gh run list op 2026-11-17.",
              max_hoogte_mm=215, breedte_mm=140),
    ]
    rr = []
    for repo in ("Software-BackEnd", "Software-FrontEnd"):
        for nm, s in sorted(runs[repo].items()):
            rr.append([repo.replace("Software-", ""), nm, str(s["n"]), str(s["success"]), str(s["failure"]), str(s["cancelled"]), s["laatste"][:10]])
    b += [
        Table(kop=["Repo", "Workflow", "Runs", "OK", "Mislukt", "Geannuleerd", "Laatste run"], rijen=rr,
              uitlijning=["links", "links", "rechts", "rechts", "rechts", "rechts", "links"], kolombreedtes=[2, 5, 2, 2, 2, 3, 3]),
        Para("Workflows als `Backend CI to GitHub Container Registry` en `Build and Test` (backend) bestaan niet meer in de huidige branch maar staan nog in de runhistorie."),
        Heading("Wat de pijplijn echt controleert", 2),
        Bullets([
            f"**Backend `ci.yml`**: `mvn verify` op JDK 21 bij push naar main, s3nj26 en s3nj26_dev en bij elke pull request. Slaagt in {runs['Software-BackEnd']['CI build']['success']} van {runs['Software-BackEnd']['CI build']['n']} runs. Publiceert surefire- en JaCoCo-rapporten als artefact.",
            f"**Dekkingsdrempel**: `pom.xml` zet `jacoco.minimum.coverage` op {D['backend']['jacoco_minimum']} (COVEREDRATIO) en bindt het doel `check` aan de fase `verify`.",
            f"**Backend `sonarqube.yml`**: {runs['Software-BackEnd']['Sonar Scan']['failure']} van {runs['Software-BackEnd']['Sonar Scan']['n']} runs mislukt. In het log van de laatste run staat `HTTP 403 Forbidden ... Please check the property sonar.token`, dus de scan komt niet tot analyse.",
            f"**Backend `super-linter.yml`**: {runs['Software-BackEnd']['Super-Linter']['failure']} van {runs['Software-BackEnd']['Super-Linter']['n']} runs mislukt op checkstyle-meldingen (bijvoorbeeld een ongebruikte import of een methodenaam met hoofdletter).",
            "**Frontend `npm-publish.yml` (Build and Test)**: `npm ci`, `npm run lint` en `npm run build`. Er staat geen testcommando in.",
            "**Frontend `ghcr.yml`**: lint (mag falen), build en een rooktest van de Docker-image.",
            "**Frontend `security.yml`**: gitleaks over de volledige historie en `npm audit`.",
            f"**Frontend `e2e.yml`**: start MariaDB en MailHog, bouwt de backend met `-DskipTests`, draait Cypress. Slechts {runs['Software-FrontEnd']['E2E tests']['success']} van {runs['Software-FrontEnd']['E2E tests']['n']} runs geslaagd; de laatste run faalde met `Geen verificatiecode gevonden in MailHog`.",
        ]),
        Heading("Dekking", 2),
        Para(
            f"JaCoCo meldt voor commit {SB}: regels {cj['line']['pct']}% ({cj['line']['gedekt']} van {cj['line']['gedekt'] + cj['line']['gemist']}), "
            f"instructies {cj['instruction']['pct']}%, vertakkingen {cj['branch']['pct']}%, methoden {cj['method']['pct']}%. "
            "Het pakket `features.e2e` (de testhulp-controller voor het e2e-profiel) heeft 0% dekking."
        ),
        Image(str(DG / "dekking-pakketten.png"),
              f"Figuur 3. Regeldekking per pakket (alleen pakketten met minstens 40 regels). Bron: jacoco.csv uit CI-run {D['ci_run_backend']}, commit {SB}.",
              breedte_mm=165),
        Heading("6. Uitvoeren en herhaalbaarheid"),
        Code("cd ClimateChecker\n./mvnw -B verify                 # alle backendtests plus dekkingscontrole\n"
             "./mvnw test -Dtest=OpenApiSpecTest -Dopenapi.update=true   # specificatie verversen\n\n"
             "npm ci && npm test              # frontend unit-tests (node --test \"src/**/*.test.js\")\n"
             "npx cypress run                 # e2e, vereist draaiende stack en MailHog",
             "Commando's volgens README.md, package.json en de workflows."),
        Note("Een wijziging is af als `mvn verify` slaagt (dekkingsdrempel inbegrepen) en `npm test` en `npm run lint` schoon draaien. "
             "In de huidige CI wordt alleen het eerste automatisch afgedwongen; `npm test` moet nog in een workflow.", kop="Kwaliteitsafspraak (voorstel)"),
        Heading("Bronnen en controle"),
        Bullets([
            f"Backend: OntdekIT/Software-BackEnd, origin/s3nj26_dev, commit {BE}. Testbronnen, pom.xml, workflows.",
            f"Frontend: OntdekIT/Software-FrontEnd, origin/s3nj26_dev, commit {FE}. Testbronnen, cypress, workflows, verse `npm test` (168 van 168 geslaagd).",
            f"CI-artefacten surefire-reports en jacoco-report van backend-run {D['ci_run_backend']}; workflowstatistiek via `gh run list`.",
            "Datum van verzamelen: 2026-11-17.",
            "**Onduidelijk of niet vastgesteld**: een lokale `mvn verify` is niet gedraaid (alleen JDK 24 aanwezig, Lombok 1.18.30 compileert daarop niet; het project vraagt JDK 21), daarom zijn de CI-rapporten gebruikt. De exacte oorzaak van de Cypress-fout is niet onderzocht; opvallend is wel dat `e2e.yml` de backend van branch `s3nj26` uitcheckt en niet van `s3nj26_dev`. Een koppeling naar eisen (FR/UC) bestaat niet in de testbronnen.",
            "**Oudere documenten**: de testdocumenten uit s3nj22 tot s3vj24 zijn niet vergeleken; de cijfers hier komen uitsluitend uit de huidige code en CI.",
        ]),
    ]
    return Document(meta=Meta(titel="Testdocument", ondertitel="Teststrategie, testgevallen en werkelijke resultaten van MB Ontdekt (ClimateChecker).",
                              kopregels=[("Datum", "2026-11-17"), ("Backend", SB), ("Frontend", SF)]),
                    blokken=schoon(b), bestandsnaam="Testdocument", voettekst="MB Ontdekt · testdocument")
