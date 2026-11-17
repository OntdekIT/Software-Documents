"""Backlog en sprints van MB Ontdekt, uit GitHub-issues, pull requests en het project 'Sem3 2026'.
Cijfers: diagrammen/backlog/gegevens.json (GitHub-issues en projectbord)."""
import collections, json, statistics, sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _proces import schoon
from docgen import Bullets, Document, Heading, Image, Meta, Note, Para, Table

DG = Path(__file__).resolve().parent.parent / "diagrammen" / "backlog"
D = json.loads((DG / "gegevens.json").read_text(encoding="utf-8"))
KORT = {"Software-BackEnd": "BE", "Software-FrontEnd": "FE", "Software-Documents": "DOC"}
SHAS = {"backend": "e104152e572449be91d75b1d86a3bcecd6d4f5d0", "frontend": "13fc1e2f086ea4c2c52c37188294b6e3921bfebd", "documents": "2eaefc8c6823ead1882b33c09567e743b08fe3f3"}


def p(x):
    return datetime.fromisoformat(x.replace("Z", "+00:00"))


def uren(u):
    return f"{u * 60:.0f} min" if u < 1 else (f"{u:.1f} uur" if u < 48 else f"{u / 24:.0f} dagen")


def kort(t, n=62):
    t = t.replace(" \u2014 ", ": ").replace("\u2014", "-").replace("\u2013", "-")
    return t if len(t) <= n else t[: n - 3] + "..."


def document() -> Document:
    iss = D["issues"]
    prs = collections.defaultdict(list)
    for q in D["prs"]:
        for n in q["issues"]:
            prs[(q["repo"], n)].append(q)
    gemerged = lambda i: [q for q in prs.get((i["repo"], i["nummer"]), []) if q["gemerged"]]
    met_pr = [i for i in iss if gemerged(i)]
    zonder_pr_dicht = [i for i in iss if not gemerged(i) and i["state"] == "CLOSED" and i["repo"] != "Software-Documents"]
    open_gemerged = [i for i in met_pr if i["state"] == "OPEN"]
    per_repo = collections.Counter(KORT[i["repo"]] for i in iss)
    gesloten = sum(1 for i in iss if i["state"] == "CLOSED")
    snel = sum(1 for i in iss if i["gesloten"] and (p(i["gesloten"]) - p(i["aangemaakt"])).total_seconds() < 3600)
    lt = [(p(min(q["gemerged"] for q in gemerged(i))) - p(i["aangemaakt"])).total_seconds() / 3600 for i in met_pr]
    pr_n = collections.Counter(KORT[q["repo"]] for q in D["prs"])
    S = D["sprints"]
    si = D["sprint_items"]
    b = [
        Para(
            "Dit document laat zien hoe het werk aan MB Ontdekt (ClimateChecker) is georganiseerd: het GitHub-projectbord 'Sem3 2026' met epics en sprints, "
            "de issues die daaruit voortkomen en de pull requests en commits die ze oplosten. Alles komt uit GitHub (issues, pull requests, project) en is gelezen op "
            "2026-11-17. Koppelingen tussen issue en pull request zijn alleen gelegd waar ze aantoonbaar zijn: 'Closes #N' in de PR-tekst of het issuenummer in de branchnaam."
        ),
        Note(
            f"Sinds {D['sinds']} zijn {len(iss)} issues aangemaakt (backend {per_repo['BE']}, frontend {per_repo['FE']}, documenten {per_repo['DOC']}), waarvan {gesloten} gesloten. "
            f"Daar tegenover staan {len(D['prs'])} pull requests (backend {pr_n['BE']}, frontend {pr_n['FE']}). Het bord telt {D['bord_items']} items: "
            f"{D['bord_status']['Done']} Done, {D['bord_status']['Todo']} Todo, {D['bord_status']['In Progress']} In Progress, {D['bord_status']['Not Planned']} Not Planned. "
            f"Slechts {len(si)} items zijn aan een sprint gekoppeld.", kop="Kort gezegd"),
        Heading("1. Het bord en de werkwijze"),
        Para(
            "Het project 'Sem3 2026' (organisatieproject 17) is de bron van waarheid voor het werk; dat staat zo in de herkomstregel van de issues, die van losse bordkaarten (drafts) "
            "zijn omgezet naar echte issues 'tijdens het samenvoegen tot één bron van waarheid' (issues in Software-Documents, aangemaakt op 2026-10-01). Elk bord-item heeft de velden Status "
            "(Not Planned, Todo, In Progress, Done), Epic, MoSCoW, Sprint, Story Points en Categorie."
        ),
        Table(kop=["Sprint", "Start", "Duur", "Items", "Story points", "Status van de items"],
              rijen=[[s, S[s]["start"], f"{S[s]['dagen']} dagen", str(len([i for i in si if i["bord"]["sprint"] == s])),
                      str(sum(i["bord"]["punten"] or 0 for i in si if i["bord"]["sprint"] == s)),
                      ", ".join(f"{n} {k}" for k, n in sorted(collections.Counter(i["bord"]["status"] for i in si if i["bord"]["sprint"] == s).items()))]
                     for s in sorted(S)], kolombreedtes=[2, 3, 2, 1, 2, 6]),
        Para(
            "Sprint 3 begon op 2026-11-02 en duurt 40 dagen, sprint 4 begint op 2026-12-12 en duurt 35 dagen (velden Sprint in het project). "
            "Aan Sprint 1 en 2 zijn op het bord geen items gekoppeld; wat daarvoor is gedaan staat als Done-items zonder sprint."
        ),
        Heading("De epics", 2),
        Table(kop=["Epic", "Done", "Todo", "In Progress", "Not Planned", "Totaal"],
              rijen=[[e, str(v["Done"]), str(v["Todo"]), str(v["In Progress"]), str(v["Not Planned"]), str(sum(v.values()))]
                     for e, v in sorted(D["bord_epic_status"].items()) if e != "geen"]
              + [["Zonder epic", *[str(D["bord_epic_status"]["geen"][k]) for k in ("Done", "Todo", "In Progress", "Not Planned")], str(sum(D["bord_epic_status"]["geen"].values()))]],
              uitlijning=["links", "rechts", "rechts", "rechts", "rechts", "rechts"], kolombreedtes=[6, 1, 1, 2, 2, 1]),
        Para("Epics zijn alleen op de recentere items ingevuld: 73 van de 130 items hebben geen epic. De inhoud van de epics is op het bord alleen als naam vastgelegd, niet als beschrijving."),
        Heading("2. Sprint 3 en sprint 4"),
        Image(str(DG / "sprintbord.png"),
              f"Figuur 1. Items per sprint volgens het project 'Sem3 2026', amber is Must have. Bron: gh project item-list 17 op 2026-11-17.",
              breedte_mm=165, max_hoogte_mm=190),
    ]
    for s in sorted(S):
        lst = sorted([i for i in si if i["bord"]["sprint"] == s], key=lambda i: (i["bord"]["epic"] or "~", i["nummer"]))
        b += [Heading(f"{s}: {len(lst)} items", 2),
              Table(kop=["Item", "Titel", "Epic", "MoSCoW", "SP", "Status"],
                    rijen=[[f"{KORT.get(i['repo'], i['repo'])} #{i['nummer']}", kort(i["titel"], 70), i["bord"]["epic"] or "geen", i["bord"]["moscow"] or "geen",
                            str(i["bord"]["punten"] or "?"), i["bord"]["status"]] for i in lst],
                    uitlijning=["links", "links", "links", "links", "rechts", "links"], kolombreedtes=[2, 8, 4, 2, 1, 2])]
    b += [
        Para("Opvallend: bijna alle items in sprint 3 en 4 staan op Todo, ook items waarvoor al code is gemerged (zie hoofdstuk 4). Het bord is dus niet bijgewerkt met de voortgang."),
        Heading("3. Wat er is opgeleverd, met de oplossende commit"),
        Para(
            f"Voor {len(met_pr)} issues is een gemergede pull request aantoonbaar gekoppeld. De commit is de commit die de PR op de doelbranch plaatste (bij squash de squash-commit, "
            "bij een mergecommit de merge). De doorlooptijd loopt van het aanmaken van het issue tot het mergen van de eerste PR."
        ),
    ]
    for rk, rn in (("Software-BackEnd", "Backend"), ("Software-FrontEnd", "Frontend")):
        rijen = []
        for i in sorted([x for x in met_pr if x["repo"] == rk], key=lambda x: x["nummer"]):
            ps = sorted(gemerged(i), key=lambda q: q["gemerged"])
            rijen.append([f"#{i['nummer']}", kort(i["titel"], 56), ", ".join(f"#{q['nummer']}" for q in ps), ", ".join(q["commit"] for q in ps),
                          uren((p(ps[0]["gemerged"]) - p(i["aangemaakt"])).total_seconds() / 3600), i["bord"]["epic"] or "geen"])
        b += [Heading(rn, 2), Table(kop=["Issue", "Titel", "PR", "Commit", "Looptijd", "Epic"], rijen=rijen,
                                     uitlijning=["links", "links", "links", "links", "rechts", "links"], kolombreedtes=[1.4, 7, 2, 2.4, 1.8, 3])]
    b += [
        Heading("4. Afwijkingen tussen bord, issues en code", 1),
        Bullets([
            f"**Gemerged maar nog open**: {len(open_gemerged)} issues staan open of op Todo terwijl hun pull request is gemerged: "
            + ", ".join(f"{KORT[i['repo']]} #{i['nummer']}" for i in open_gemerged)
            + ". De pull requests gaan naar s3nj26_dev, terwijl de standaardbranch van beide repositories main is. GitHub sluit een issue via 'Closes #N' alleen bij een merge naar de standaardbranch; dat verklaart waarschijnlijk dat deze niet automatisch dichtgingen.",
            f"**Achteraf aangemaakt**: {snel} van de {len(iss)} issues zijn binnen een uur na aanmaken gesloten. Het gaat vooral om {len(zonder_pr_dicht)} backendissues die op 2026-09-18 zijn aangemaakt en gesloten voor werk dat in die dagen al klaar was (bijvoorbeeld #122 Security-audit, #123 JWT-sleutel uit de code gehaald), zonder koppeling aan een pull request.",
            "**Bord en issue verschillen**: in Software-Documents staan 10 open issues op Not Planned en 4 gesloten issues eveneens op Not Planned. Open en gesloten komen op het bord dus niet overeen met de status Todo of Done.",
            f"**Doorlooptijd**: voor de {len(lt)} gekoppelde issues is de mediane tijd van aanmaken tot merge {uren(statistics.median(lt))}, de langste {uren(max(lt))}. Doorlooptijden zijn kort omdat veel issues pas tegelijk met de PR zijn aangemaakt.",
        ]),
        Image(str(DG / "weekverloop.png"),
              "Figuur 2. Aangemaakte en gesloten issues per ISO-week, alle drie de repositories. Bron: gh issue list.", breedte_mm=140),
        Heading("Retroactief aangemaakte backendissues (zonder PR-koppeling)", 2),
        Table(kop=["Issue", "Titel", "Aangemaakt", "Gesloten"],
              rijen=[[f"#{i['nummer']}", kort(i["titel"], 78), i["aangemaakt"][:10], i["gesloten"][:10]] for i in sorted(zonder_pr_dicht, key=lambda x: x["nummer"])],
              kolombreedtes=[1.2, 9, 2.4, 2.4]),
        Heading("5. Openstaand werk", 1),
        Table(kop=["Item", "Titel", "Status", "Sprint"],
              rijen=[[f"{KORT[i['repo']]} #{i['nummer']}", kort(i["titel"], 78), i["bord"]["status"], i["bord"]["sprint"] or "geen"]
                     for i in sorted([x for x in iss if x["state"] == "OPEN" and x not in open_gemerged], key=lambda x: (x["repo"], x["nummer"]))],
              kolombreedtes=[2, 9, 2, 2]),
        Para("In Software-Documents staan de meeste open items rond afstemming met de opdrachtgever, hosting en overdracht. Zie ook het document Agile samenwerking."),
        Heading("Bronnen en controle"),
        Bullets([
            f"GitHub: gh issue list en gh pr list voor OntdekIT/Software-BackEnd, Software-FrontEnd en Software-Documents (issues aangemaakt vanaf {D['sinds']}); project 17 'Sem3 2026' via gh project item-list, op 2026-11-17.",
            f"Commit-SHA's van de gelezen branches: backend {SHAS['backend'][:7]}, frontend {SHAS['frontend'][:7]}, documenten {SHAS['documents'][:7]} (origin/s3nj26_dev, en origin/dev voor documenten). De commits in hoofdstuk 3 zijn de mergecommits van de PR's.",
            "**Onduidelijk**: wat de epics inhoudelijk afbakenen (alleen namen), of Sprint 1 en 2 hebben bestaan (geen items eraan gekoppeld), en wie de bordvelden bijhoudt. Story points staan op 105 van de 130 items, de schattingsmethode is niet vastgelegd. Issues van voor 2026-09-01 zijn niet opgenomen, behalve de sprint-items van het bord.",
            "**Verschil met oudere documenten**: de oudere backlogdocumenten (s3nj22 tot s3vj24) zijn niet vergeleken; dit document gaat alleen uit van de huidige GitHub-gegevens.",
        ]),
    ]
    return Document(meta=Meta(titel="Backlog en sprints", ondertitel="De backlog van MB Ontdekt: epics, sprints, issues en de commits die ze oplosten.",
                              kopregels=[("Datum", "2026-11-17"), ("Bord", "Sem3 2026")]),
                    blokken=schoon(b), bestandsnaam="Backlog en sprints", voettekst="MB Ontdekt · backlog en sprints")
