"""Versiebeheer en werkwijze van MB Ontdekt, uit git en GitHub. Cijfers: diagrammen/versiebeheer/gegevens.json."""
import json, statistics, sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _proces import schoon
from docgen import Bullets, Document, Heading, Image, Meta, Note, Para, Table

DG = Path(__file__).resolve().parent.parent / "diagrammen" / "versiebeheer"
D = json.loads((DG / "gegevens.json").read_text(encoding="utf-8"))
BE, FE = D["backend"], D["frontend"]
SB, SF = BE["sha"], FE["sha"]


def p(x):
    return datetime.fromisoformat(x.replace("Z", "+00:00"))


def stat(r):
    m = [q for q in r["prs"] if q["state"] == "MERGED"]
    uren = [(p(q["mergedAt"]) - p(q["createdAt"])).total_seconds() / 3600 for q in m]
    return {"n": len(m), "squash": sum(1 for q in m if q["ouders"] == 1), "merge": sum(1 for q in m if q["ouders"] == 2),
            "med": statistics.median(uren), "max": max(uren), "gesloten": sum(1 for q in r["prs"] if q["state"] == "CLOSED"),
            "review": sum(1 for q in r["prs"] if q["reviews"]), "concept": sum(1 for q in r["prs"] if q["isDraft"])}


def uren(u):
    return f"{u * 60:.0f} minuten" if u < 1 else (f"{u:.1f} uur" if u < 48 else f"{u / 24:.0f} dagen")


def conv(r):
    t = r["commit_types"]
    n = r["commits_zonder_merges"]
    return n, n - t.get("geen prefix", 0)


def document() -> Document:
    sb, sf = stat(BE), stat(FE)
    nb, cb = conv(BE)
    nf, cf = conv(FE)
    b = [
        Para(
            "Dit document beschrijft hoe de code van MB Ontdekt (ClimateChecker) wordt beheerd, zoals dat uit git en GitHub blijkt: "
            "welke branches er zijn, hoe wijzigingen via pull requests binnenkomen, hoe commits eruitzien en wat daar in de praktijk van klopt. "
            f"Alle cijfers gelden voor de periode vanaf {D['sinds']} (start van het huidige semester) tot 2026-11-17, "
            f"tenzij anders vermeld. Gelezen op backend-commit {SB[:7]} en frontend-commit {SF[:7]}."
        ),
        Heading("1. Repositories en branches"),
        Para("Er zijn drie repositories in de organisatie OntdekIT: Software-BackEnd (Spring Boot), Software-FrontEnd (React) en Software-Documents (documentatie). De backend en frontend hebben dezelfde branchstructuur."),
        Table(kop=["Branch", "Rol (zoals uit de code en PR's blijkt)", "Staat op 2026-11-17"],
              rijen=[
                  ["main", "Hoofdbranch van de repository. PR 'back to main for new semester' (#119 backend, #129 frontend) bracht het werk van het vorige team terug.", f"backend {BE['tips']['main']['sha']}, frontend {FE['tips']['main']['sha']}"],
                  ["s3nj26", "Semestertak voor dit semester. Beveiligings- en CI-fixes van september gingen hierheen. Releasetags van de frontend worden alleen op main en s3nj26 gemaakt (ghcr.yml).", f"{BE['tips']['s3nj26']['vooruit_op_main']} (backend) en {FE['tips']['s3nj26']['vooruit_op_main']} (frontend) commits voor op main"],
                  ["s3nj26_dev", "Integratiebranch. Alle feature-PR's sinds oktober gaan hierheen. De backend-workflow Deploy draait op pushes naar deze branch.", f"{BE['tips']['s3nj26_dev']['vooruit_op_main']} (backend) en {FE['tips']['s3nj26_dev']['vooruit_op_main']} (frontend) commits voor op main"],
                  ["feature-branches", "Eén branch per issue of taak, benoemd met prefix en issuenummer, bijvoorbeeld feat/174-dockerfile, fix/198-api-security, test/183-jacoco-coverage.", f"{BE['remote_branches']} (backend) en {FE['remote_branches']} (frontend) remote branches in totaal"],
              ], kolombreedtes=[2, 7, 4]),
        Para(
            f"Opvallend is dat main en s3nj26 ver achterlopen op s3nj26_dev: er is sinds de septemberfixes geen promotie naar s3nj26 of main geweest. "
            "De werkelijke branchstroom is daarom: feature-branch naar s3nj26_dev, en in september nog rechtstreeks naar s3nj26."
        ),
        Image(str(DG / "branching-backend.png"),
              f"Figuur 1. Backend: gemergede pull requests per type branch naar doelbranch. Label: aantal (squash of rebase + mergecommit). Tussen haakjes bij een branch: commits voor op main. Bron: gh pr list en git cat-file op Software-BackEnd, commit {SB[:7]}.",
              breedte_mm=165),
        Image(str(DG / "branching-frontend.png"),
              f"Figuur 2. Frontend, zelfde opbouw. De extra doelbranch integration/kaart-en-navigatie bundelde vier kaart-PR's, die daarna als een PR (#194) naar s3nj26_dev gingen. Bron: Software-FrontEnd, commit {SF[:7]}.",
              breedte_mm=165),
        Heading("2. Het pull-requestverloop"),
        Para("Wijzigingen komen via een pull request binnen. Dat blijkt uit de PR-lijst: bijna alle wijzigingen sinds september staan als PR, met de commit of de branchnaam die naar een issue verwijst."),
        Bullets([
            "Een issue op het GitHub-projectbord beschrijft de wens (vaak als user story, 'Als gebruiker wil ik ...', met label userstories).",
            "Een branch met prefix en issuenummer wordt aangemaakt en de PR verwijst naar het issue (zichtbaar als 'Closes #N' in de PR-tekst, zoals #205 in de backend).",
            "Bij elke PR draaien de workflows: backend CI build, Super-Linter en Sonar Scan; frontend Build and Test, Security checks, container-build en E2E tests (zie het Testdocument).",
            "De PR wordt gemerged naar s3nj26_dev, meestal als squash-commit met het PR-nummer achter de titel, bijvoorbeeld 'feat: ... (#201) (#205)'.",
            "Een push naar s3nj26_dev activeert in de backend de Deploy-workflow (image bouwen en publiceren).",
        ]),
        Table(kop=["Meting", "Backend", "Frontend"],
              rijen=[
                  ["PR's gemerged", str(sb["n"]), str(sf["n"])],
                  ["Daarvan squash of rebase (een ouder)", str(sb["squash"]), str(sf["squash"])],
                  ["Daarvan mergecommit (twee ouders)", str(sb["merge"]), str(sf["merge"])],
                  ["Gesloten zonder merge", str(sb["gesloten"]), str(sf["gesloten"])],
                  ["Mediane doorlooptijd (aanmaken tot merge)", uren(sb["med"]), uren(sf["med"])],
                  ["Langste doorlooptijd", uren(sb["max"]), uren(sf["max"])],
                  ["PR's met een formele review", str(sb["review"]), str(sf["review"])],
                  ["PR's als concept (draft) aangemaakt", str(sb["concept"]), str(sf["concept"])],
              ], uitlijning=["links", "rechts", "rechts"], kolombreedtes=[6, 2, 2]),
        Image(str(DG / "doorlooptijd.png"),
              f"Figuur 3. Doorlooptijd van gemergede PR's, backend en frontend samen. Bron: gh pr list (createdAt en mergedAt).",
              breedte_mm=150),
        Para(
            "De korte doorlooptijden komen doordat veel PR's binnen enkele minuten na het aanmaken zijn gemerged, vaak in series op dezelfde dag "
            "(op 2026-09-18 veertien backend-PR's, op 2026-11-17 zestien backend- en vierentwintig frontend-PR's). Er staan weinig formele reviews tegenover. "
            "Op de backend-PR #181 staan twee reviews (een van een geautomatiseerde reviewer van GitHub die niet kon draaien en een inhoudelijke). "
            "Een deel van de PR's heeft een geautomatiseerd commentaar van SonarCloud."
        ),
        Heading("3. Merge-strategie"),
        Para(
            f"De repository-instellingen staan alle drie de methoden toe (squash, mergecommit, rebase) en 'branch verwijderen na merge' staat uit (bron: gh api repos). "
            f"Gevolg: {BE['remote_branches']} remote branches in de backend en {FE['remote_branches']} in de frontend, waarvan git er respectievelijk {BE['niet_gemerged_volgens_git']} en {FE['niet_gemerged_volgens_git']} "
            "als 'niet gemerged in s3nj26_dev' toont. Dat zijn grotendeels branches die via squash zijn gemerged: git herkent de inhoud dan niet als gemerged, dus de lijst zegt niets over echt openstaand werk."
        ),
        Heading("4. Commitberichten"),
        Para(
            f"De afspraak is conventionele commits (feat, fix, test, refactor, docs, chore, style, ci, perf). Van de commits op s3nj26_dev sinds {D['sinds']} (zonder mergecommits) heeft "
            f"{cb} van {nb} backendcommits en {cf} van {nf} frontendcommits zo'n prefix. De overige commits hebben een gewone zin als bericht, bijvoorbeeld 'removed unused Mockito import'. "
            "Veel commitberichten bevatten het PR-nummer."
        ),
        Image(str(DG / "commitsoorten.png"),
              f"Figuur 4. Commits per prefix. Bron: git log origin/s3nj26_dev --no-merges sinds {D['sinds']}, backend {SB[:7]}, frontend {SF[:7]}.", breedte_mm=165),
        Heading("5. Releases en tags"),
        Para(
            "In beide repositories bestaan tags voor mijlpalen van eerdere groepen (bijvoorbeeld s3vj26-final, s3vj25-final). Daarnaast verhoogt de frontend-workflow ghcr.yml bij een push naar main of s3nj26 automatisch het patchnummer van de semver-tag "
            "(workflowtekst, regel 59 tot 114). Voor de backend is er een CHANGELOG.md volgens Keep a Changelog, maar die zegt zelf dat hij pas laat in het project is ingezet. De meest recente semver-tag in de frontend is 1.0.19 (2026-09-17, de dag van de s3nj26-pushes); in de backend is de laatste semver-tag 1.0.3 (2026-02-23) en de laatste tag overall s3vj26-final (2026-05-18). Sinds 2026-09-17 zijn dus geen nieuwe versietags gemaakt."
        ),
        Heading("6. Hulpmiddelen in de repository"),
        Bullets([
            "Issue-templates voor bug, feature en standaardissue (backend: drie, frontend: bug en feature).",
            "Geen CONTRIBUTING.md, geen pull-request-template en geen CODEOWNERS in de gelezen commits.",
            "Branchbescherming is niet uit te lezen: de API geeft 404 op de beveiligings-endpoint voor alle branches. Issue #75 in Software-Documents meldt wel dat die repository zonder review niet te mergen was.",
        ]),
        Note(
            "De werkwijze op papier (issue, branch, PR, CI, merge) wordt in de praktijk gevolgd. Wat afwijkt: nauwelijks formele reviews, branches blijven staan, "
            "main en s3nj26 zijn niet bijgewerkt sinds de septemberfixes, en in de backend volgt een kwart van de commits (13 van 52) de commitconventie niet.",
            kop="Kort gezegd"),
        Heading("Bronnen en controle"),
        Bullets([
            f"git log, git rev-list, git cat-file op verse clones van origin/s3nj26_dev: Software-BackEnd {SB}, Software-FrontEnd {SF}.",
            "gh pr list en gh api repos/OntdekIT/<repo> (instellingen) op 2026-11-17.",
            "Of de merge een squash was, is afgeleid uit het aantal ouders van de mergecommit (een ouder: squash of rebase, twee: mergecommit); het onderscheid tussen squash en rebase is niet gemaakt.",
            "Onduidelijk: of main en s3nj26 bewust zijn blijven staan, wie reviewt (alleen formele reviews zijn telbaar, mondelinge niet), en of branchbescherming aan staat.",
            "Auteursnamen in git zijn niet eenduidig (dezelfde persoon commit onder meerdere namen), daarom zijn er geen cijfers per persoon opgenomen.",
        ]),
    ]
    return Document(meta=Meta(titel="Versiebeheer en werkwijze", ondertitel="Branches, pull requests en commits van MB Ontdekt, zoals ze in git en GitHub echt zijn.",
                              kopregels=[("Datum", "2026-11-17"), ("Backend", SB[:7]), ("Frontend", SF[:7])]),
                    blokken=schoon(b), bestandsnaam="Versiebeheer en werkwijze", voettekst="MB Ontdekt · versiebeheer")
