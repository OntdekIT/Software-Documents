"""Agile samenwerking rond MB Ontdekt: alleen wat in GitHub aantoonbaar is.
Bronnen: GitHub-issues, pull requests en het project 'Sem3 2026' (zie diagrammen/backlog/gegevens.json en diagrammen/versiebeheer/gegevens.json)."""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _proces import schoon
from docgen import Bullets, Document, Heading, Image, Meta, Note, Para, Table

DG = Path(__file__).resolve().parent.parent / "diagrammen"
B = json.loads((DG / "backlog" / "gegevens.json").read_text(encoding="utf-8"))
V = json.loads((DG / "versiebeheer" / "gegevens.json").read_text(encoding="utf-8"))


def st(repo, nr):
    for i in B["issues"]:
        if i["repo"] == repo and i["nummer"] == nr:
            return {"OPEN": "open", "CLOSED": "gesloten"}[i["state"]] + (f" op {i['gesloten'][:10]}" if i["gesloten"] else "")
    return "niet opgenomen"


def document() -> Document:
    D = "Software-Documents"
    reviews = sum(1 for rep in ("backend", "frontend") for q in V[rep]["prs"] if q["reviews"])
    totprs = sum(len(V[rep]["prs"]) for rep in ("backend", "frontend"))
    S = B["sprints"]
    b = [
        Para(
            "Dit document beschrijft de samenwerking rond MB Ontdekt (ClimateChecker) tussen het ontwikkelteam en de opdrachtgever, voor zover dat in GitHub aantoonbaar is: "
            "in issues, issue-comments, pull requests en het projectbord. Gesprekken, appjes en mondelinge afspraken staan daar niet in; wat daar niet in staat, "
            "wordt hier niet beweerd. Waar een afspraak alleen als plan of acceptatiecriterium bestaat, staat dat erbij."
        ),
        Note(
            "De opdrachtgever is Wil, contactpersoon bij Meet je stad Amersfoort (Documents #98: 'Wil is onze opdrachtgever'). Het team werkt met een bord, user stories, korte pull-request-rondes en CI. "
            "Dat er overleg met Wil is geweest, is niet in de repositories vast te stellen: de afspraak om de backlog te prioriteren (#98) staat nog open en een verslag ontbreekt.", kop="Kort gezegd"),
        Heading("1. Wat aantoonbaar is"),
        Table(kop=["Onderdeel", "Bewijs in GitHub", "Status"],
              rijen=[
                  ["Wil is opdrachtgever", "Documents #98 (tekst), #80 'Contactpersoon bij Meet je stad Amersfoort'", f"#98 {st(D, 98)}, #80 {st(D, 80)}"],
                  ["Contactritme drie weken", "Backend #151: 'sprintlengte van drie weken, gelijk aan het contactritme met Wil'; afgerond met het inrichten van het bord", f"#151 {st('Software-BackEnd', 151)}"],
                  ["Werkafspraken (definition of done, wie houdt de backlog bij)", "Backend #151, acceptatiecriteria en afrondingsnotitie; branching-richtlijn in het document s3nj24/Git branching strategie & richtlijnen.docx", f"#151 {st('Software-BackEnd', 151)}"],
                  ["Keuze van de codebase", "Backend #152: Wil wist niet of door te bouwen op de laatste codebase; keuze is gemaakt om op de bestaande codebase door te gaan. Terugkoppelen aan Wil staat als acceptatiecriterium, de terugkoppeling zelf is niet vast te stellen", f"#152 {st('Software-BackEnd', 152)}"],
                  ["Niet-functionele eisen afgestemd", "Documents #77: Wil hecht aan een goedkope en eenvoudige serveromgeving; vastgelegd in s3nj24/Non functional requirements.docx. Of dit met Wil is afgestemd, is niet vast te stellen", f"#77 {st(D, 77)}"],
                  ["Backlog prioriteren met Wil", "Documents #98 met acceptatiecriteria (planning sprint 3 en 4, uitvalcontrole-interval, drempels 80% en 50%, open vragen en een verslag in de repo). Geen enkel criterium is afgevinkt", f"#98 {st(D, 98)}"],
                  ["Open vragen aan Wil (e-mailadres, hostingomgeving, gebruikersdatabase, vervolgafspraak)", "Documents #82, #83, #84, #99: gesloten met de opmerking 'Wordt meegenomen in #98'. Een antwoord van Wil staat nergens", f"#82 {st(D, 82)}"],
                  ["Demo en eindoplevering aan Wil", "Documents #85", f"#85 {st(D, 85)}"],
                  ["Gebruikerstest met een stationeigenaar", "Documents #87", f"#87 {st(D, 87)}"],
                  ["Meelopen bij een workshop Meetstation bouwen", "Documents #79", f"#79 {st(D, 79)}"],
                  ["Samenwerkingscontract en rolverdeling", "Documents #101 en #102: gesloten zonder uitgewerkte inhoud ('nader in te vullen door het team')", f"#101 {st(D, 101)}, #102 {st(D, 102)}"],
              ], kolombreedtes=[4, 9, 3]),
        Heading("2. De samenwerkingscyclus"),
        Para(
            "De cyclus hieronder is opgebouwd uit wat in de repositories zichtbaar is. Amber is aantoonbaar uitgevoerd (er zijn issues, gemergede pull requests en workflows). "
            "Gestippeld is gepland maar niet als uitgevoerd vast te stellen: de afspraak met Wil over de prioriteiten en de demo."
        ),
        Image(str(DG / "agile" / "samenwerkingscyclus.png"),
              f"Figuur 1. Samenwerkingscyclus. Bron: issues Software-Documents #80, #85, #98, projectbord 'Sem3 2026', gh pr list (backend, frontend) op 2026-11-17; gegevens in diagrammen/backlog/gegevens.json en diagrammen/versiebeheer/gegevens.json.",
              breedte_mm=130, max_hoogte_mm=200),
        Heading("3. De rollen"),
        Table(kop=["Wie", "Rol", "Wat er van aantoonbaar is"],
              rijen=[
                  ["Wil, Meet je stad Amersfoort", "Opdrachtgever en contactpersoon", "Genoemd in de issues #77, #98, #151, #152. De rol als bron van prioriteiten is voorzien (#98), maar de uitkomst is niet vastgelegd."],
                  ["Ontwikkelteam (studenten)", "Bouwt de app, beheert bord, issues en pull requests", f"De {len(B['issues'])} issues sinds {B['sinds']} en de pull requests worden in de repositories door het team beheerd; de onderlinge rolverdeling is niet vastgelegd (#102 zonder inhoud)."],
                  ["Geautomatiseerde beoordelaars", "SonarCloud en een geautomatiseerde reviewer van GitHub", "SonarCloud plaatst een Quality Gate-commentaar op pull requests (bijvoorbeeld backend #205). Een geautomatiseerde review van GitHub op backend #181 meldde dat die door een quotumgrens niet kon draaien."],
              ], kolombreedtes=[3, 3, 9]),
        Para("De opdrachtgever bepaalt volgens de opzet van #98 het 'wat' en de volgorde (planning, drempelwaarden, hostingkeuze); het team bepaalt het 'hoe'. Dat laatste is een voorgenomen verdeling, geen vastgelegd resultaat."),
        Heading("4. Een ronde in de praktijk"),
        Bullets([
            "**Kiezen**: items krijgen op het bord een Epic, MoSCoW-prioriteit, story points en een Sprint. Er zijn twee sprints met items: "
            f"Sprint 3 (start {S['Sprint 3']['start']}, {S['Sprint 3']['dagen']} dagen) en Sprint 4 (start {S['Sprint 4']['start']}, {S['Sprint 4']['dagen']} dagen).",
            "**Bouwen**: per issue een branch en pull request, bijvoorbeeld feat/174-dockerfile; zie het document Versiebeheer en werkwijze.",
            "**Controleren**: bij elke pull request draaien de CI-workflows (zie het Testdocument).",
            "**Laten zien**: een demo aan Wil staat gepland (#85, open); een demo-omgeving was al eerder gevraagd in Frontend #114 ('Als opdrachtgever of demogeving wil ik een demo-omgeving').",
            "**Feedback meenemen**: niet vast te stellen. De pull requests bevatten vrijwel geen reviewcommentaar: "
            f"{reviews} van de {totprs} pull requests sinds {B['sinds']} heeft een formele review.",
        ]),
        Heading("5. Afwijkingen en tegenstrijdigheden"),
        Bullets([
            "**Sprintlengte**: de afspraak is drie weken (Backend #151). De sprints op het bord duren 40 en 35 dagen.",
            "**Contactmomenten niet vastgelegd**: #98 vraagt zelf om 'een kort verslag in deze repo'. In de gelezen bestandsstructuur van Software-Documents (origin/dev) is geen verslag of notulen van een overleg gevonden.",
            "**Bord loopt achter**: items als Backend #182, #183, #184 en #185 staan op Todo terwijl hun pull requests zijn gemerged (zie Backlog en sprints).",
            "**User stories zonder opdrachtgever**: de user stories van 2026-11-17 (Frontend #158 tot #193, Backend #196 tot #206) zijn allemaal op dezelfde dag (2026-11-17) aangemaakt. Dat ze uit gesprekken met Wil voortkomen, is niet vast te stellen.",
        ]),
        Heading("6. Wat niet aantoonbaar is"),
        Bullets([
            "Dat er daadwerkelijk contactmomenten met Wil zijn geweest, wanneer, en wat er is besloten.",
            "Een vaste ritmiek van sprintplanning, review of retrospective. In de repositories staan daarvoor geen verslagen of agenda's.",
            "Wie binnen het team welke rol heeft (scrum master, product owner namens het team).",
            "Dat de keuze van de codebase of de niet-functionele eisen aan Wil zijn teruggekoppeld.",
        ]),
        Heading("Bronnen en controle"),
        Bullets([
            "GitHub-issues van OntdekIT/Software-Documents (#75 tot #103), Software-BackEnd (#151, #152) en Software-FrontEnd (#114, #148, #150), gelezen met gh issue view op 2026-11-17.",
            "Het project 'Sem3 2026' (gh project item-list 17) voor sprintgegevens; pull requests via gh pr list.",
            "Commit-SHA's: backend e104152, frontend 13fc1e2 (origin/s3nj26_dev), documenten 2eaefc8 (origin/dev), datum 2026-11-17.",
            "**Onduidelijk**: alles buiten GitHub (gesprekken, e-mail, Trello-bord 'Ontdekstation 013' uit eerdere semesters, dat in #151 wordt genoemd maar niet is gelezen). Het bord is volgens #151 later overgezet naar GitHub Projects.",
            "**Verwijzingen naar oudere documenten** (s3nj24: Git branching strategie, Non functional requirements) zijn alleen via de issues gelezen, niet inhoudelijk getoetst.",
        ]),
    ]
    return Document(meta=Meta(titel="Agile samenwerking", ondertitel="Hoe het team en de opdrachtgever samenwerken, voor zover aantoonbaar in GitHub.",
                              kopregels=[("Datum", "2026-11-17"), ("Opdrachtgever", "Meet je stad Amersfoort")]),
                    blokken=schoon(b), bestandsnaam="Agile samenwerking", voettekst="MB Ontdekt · agile samenwerking")
