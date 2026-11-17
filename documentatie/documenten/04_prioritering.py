"""04 Prioritering: MoSCoW en volgorde, gebaseerd op het echte bord Sem3 2026."""
import json, os
from docgen import Document, Meta, Heading, Para, Bullets, Table, Note, Image

HIER = os.path.dirname(os.path.abspath(__file__))
DG = os.path.join(HIER, "..", "diagrammen", "prioritering")
S = json.load(open(os.path.join(DG, "stats.json")))
M = S["moscow_status"]
NL = {"Done": "klaar", "In Progress": "bezig", "Todo": "te doen", "Not Planned": "niet gepland"}
VOLG = {"Must have": 0, "Should have": 1, "Could have": 2, "Won't have": 3}
KORT = {"BackEnd": "BE", "FrontEnd": "FE", "Documents": "Doc"}


def ref(i):
    return f"{KORT.get(i['repo'], i['repo'])} #{i['nummer']}"


def sprint_tabel(naam):
    rijen = sorted([i for i in S["items_mc"] if i["sprint"] == naam], key=lambda i: (VOLG[i["moscow"]], i["nummer"]))
    return Table(["Item", "Titel", "MoSCoW", "Punten", "Status"],
                 [[ref(i), i["titel"][:80], i["moscow"], str(i["sp"] or "-"), NL[i["status"]]] for i in rijen],
                 kolombreedtes=[1.4, 6, 1.8, 1, 1.5])


def tel(m, *st):
    return sum(M[m].get(s, 0) for s in st)


def document():
    sp = S["sprints"]
    b = [
        Para("Niet alles kan tegelijk. Dit document beschrijft hoe het team de backlog van MB Ontdekt ordent: de MoSCoW-indeling op het "
             f"projectbord Sem3 2026, wat daar werkelijk in staat ({S['totaal_items']} items) en welke volgorde dat oplevert. "
             "Alle cijfers zijn uit het bord berekend."),
        Heading("De methode: MoSCoW"),
        Para("Het bord gebruikt de velden MoSCoW (Must, Should, Could, Won't have), Epic, Sprint, Story points en Status. "
             f"Van de {S['totaal_items']} items hebben {S['met_moscow']} een MoSCoW-klasse en een epic: dat is de oorspronkelijke backlog. "
             f"De overige {S['zonder_moscow']} items (waarvan {S['zonder_status'].get('Done', 0)} klaar) zijn later toegevoegd of waren al afgerond werk, zoals de "
             "security-audit en de UX-user stories, en hebben geen MoSCoW-klasse."),
        Table(["Klasse", "Betekenis (standaard)", "Aantal en status op het bord", "Voorbeeld van het bord"], [
            ["Must have", "Zonder dit is de oplevering mislukt.", f"{sum(M['Must have'].values())} items: {tel('Must have','Done')} klaar, {tel('Must have','Todo')} te doen, {tel('Must have','Not Planned')} niet gepland", "BE #174 Applicatie containeriseren met Docker (klaar)"],
            ["Should have", "Belangrijk, maar de oplevering is niet kapot zonder.", f"{sum(M['Should have'].values())} items: {tel('Should have','Done')} klaar, {tel('Should have','In Progress')} bezig, {tel('Should have','Todo')} te doen, {tel('Should have','Not Planned')} niet gepland", "BE #169 Healthcheck en monitoring (klaar)"],
            ["Could have", "Fijn als er tijd is.", f"{sum(M['Could have'].values())} items: {tel('Could have','Done')} klaar, {tel('Could have','In Progress')} bezig, {tel('Could have','Todo')} te doen, {tel('Could have','Not Planned')} niet gepland", "FE #150 'Over ons' pagina invullen (klaar)"],
            ["Won't have", "Nu bewust niet.", f"{sum(M[chr(87)+'on'+chr(39)+'t have'].values())} item, niet gepland", "FE #111 Enquete voor meetstation-eigenaren (niet gepland)"],
        ], kolombreedtes=[1.5, 3, 4.5, 4]),
        Image(os.path.join(DG, "moscow-status.png"),
              "MoSCoW-klasse en status. Bron: GitHub Project 17 (Sem3 2026) van OntdekIT, opgehaald op 2026-11-17, " + str(S["met_moscow"]) + " items met MoSCoW. Berekend uit het bord.",
              breedte_mm=165),
        Para("De betekenis in de tweede kolom is de gangbare MoSCoW-definitie, niet een tekst uit het project: het team heeft de klassen op het bord niet "
             "zelf omschreven."),
        Heading("De weegfactoren"),
        Para("In de repo's, de issues en het bord is nergens vastgelegd welke vragen de MoSCoW-klasse bepaalden. Dat is een onduidelijkheid, geen conclusie. "
             "Wat het bord wel laat zien zijn de velden waarmee gewogen kan worden:"),
        Bullets([
            f"**Story points** (1, 2, 3, 5 of 8) in de volgorde van de Fibonacci-reeks op een deel van de items. Totaal over de items met MoSCoW: {S['totaal_sp_mc']} punten.",
            "**Epic**: tien thema's, van DevOps, hosting en OTAP tot Notificaties.",
            "**Sprint**: Sprint 3 en Sprint 4 zijn gevuld (zie hieronder).",
            "**Afhankelijkheid met de opdrachtgever.** Issue Documents #98 noemt de afspraak met de opdrachtgever waarin de planning voor sprint 3 en 4 wordt doorgenomen "
            "met als uitgangspunt: eerst de datasynchronisatie (de hoofdvraag), dan de rest. Dat issue staat nog open.",
        ]),
        Note(f"Van de {S['met_moscow']} items met MoSCoW is {S['totaal_sp_mc']} punten werk. Daarvan is nog {sum(S['sp_open_moscow'].values())} punten open (te doen of bezig), "
             f"waarvan {S['sp_open_moscow']['Must have']} punten Must have. Het zwaarst weegt op het bord dus de Must-klasse, maar dat is een uitkomst van de tellingen, "
             "geen vastgelegde regel.", kop="Wat de cijfers zeggen"),
        Table(["Klasse", "Items", "Punten totaal", "Punten nog open"],
              [[k, str(sum(M[k].values())), str(S["sp_moscow"][k]), str(S["sp_open_moscow"][k])] for k in ["Must have", "Should have", "Could have", "Won't have"]],
              kolombreedtes=[2, 1, 1.5, 1.5], uitlijning=["links", "rechts", "rechts", "rechts"]),
        Heading("De prioriteitenvolgorde"),
        Para("De volgorde in tijd staat in het veld Sprint. Sprint 3 begint op " + sp["Sprint 3"]["start"] + f" en duurt {sp['Sprint 3']['dagen']} dagen, "
             "Sprint 4 begint op " + sp["Sprint 4"]["start"] + f" en duurt {sp['Sprint 4']['dagen']} dagen. Per sprint staan de items hieronder op MoSCoW-klasse. Doc #75 (Sprint 3, klaar) heeft geen MoSCoW-klasse en staat daarom niet in de tabel."),
        Heading("Sprint 3", 2), sprint_tabel("Sprint 3"),
        Heading("Sprint 4", 2), sprint_tabel("Sprint 4"),
        Heading("De epics in volgorde van belang", 2),
        Para("Het diagram ordent de epics op het aantal Must-items en daarna op punten. Deze volgorde is berekend, niet door het team vastgesteld."),
        Image(os.path.join(DG, "epics-status.png"),
              "Epics en status. Bron: GitHub Project 17 (Sem3 2026), opgehaald op 2026-11-17. Berekend uit het bord.", breedte_mm=165),
        Heading("Waar bord en werkelijkheid verschillen"),
        Bullets([
            f"**Werk buiten de prioritering.** {S['zonder_moscow']} items hebben geen MoSCoW en geen epic; {S['zonder_status'].get('Done', 0)} daarvan zijn klaar. "
            "Het meeste is uitgevoerd zonder dat het langs de MoSCoW-indeling is gegaan.",
            "**Open issues met samengevoegde PR.** FrontEnd #158 tot #164 en BackEnd #196 en #198 tot #201 staan op Todo, terwijl de bijbehorende PR's zijn samengevoegd "
            "(FrontEnd #165 tot #171, BackEnd #197 en #202 tot #205).",
            "**Zwaar gewicht, weinig gepland.** Van de Must-items zijn er 2 op Niet gepland gezet (BE #173 Acceptatie- en productieomgeving, Doc #100 GitHub-toegang).",
            "**Sprint-veld grotendeels leeg.** Maar 21 van de " + str(S["totaal_items"]) + " items heeft een sprint.",
        ]),
        Para("Dit sluit aan op de documenten Analysedocument (wat er is gebouwd en bewezen) en Backlog en sprints."),
        Heading("Bronnen en controle"),
        Bullets([
            "Bord: GitHub Project 17 (Sem3 2026) van OntdekIT, opgehaald met gh project item-list op 2026-11-17 en bewaard in diagrammen/prioritering/bord-sem3-2026.json.",
            "Issues en PR's: gh issue list en gh pr list voor OntdekIT/Software-BackEnd, Software-FrontEnd en Software-Documents, 2026-11-17. Backend origin/s3nj26_dev e104152e572449be91d75b1d86a3bcecd6d4f5d0, frontend origin/s3nj26_dev 13fc1e2f086ea4c2c52c37188294b6e3921bfebd (voor de PR-verwijzingen).",
            "Alle cijfers en diagrammen zijn berekend uit het bord. Datum: 2026-11-17.",
        ]),
        Para("**Onduidelijk gebleven:** de weegfactoren achter de MoSCoW-klassen, wie ze heeft toegekend en of de opdrachtgever ze heeft bevestigd (issue Documents #98 is nog open). "
             "Het veld Sprint is bij de meeste items niet ingevuld, dus voor die items is de volgorde niet vast te stellen."),
    ]
    return Document(meta=Meta("Prioritering", "Hoe bepaald wordt wat eerst wordt gebouwd.", [("Datum", "2026-11-17"), ("Bron", "bord Sem3 2026")]),
                    blokken=b, voettekst="MB Ontdekt - ClimateChecker - prioritering")
