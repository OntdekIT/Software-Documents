"""14 Architectuurbeslissingen van MB Ontdekt, zes besluiten volgens documenttypes/adr.txt."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from docgen import Bullets, Document, Heading, Image, Meta, Note, Para, Table

D = Path(__file__).resolve().parents[1] / "diagrammen" / "architectuur" / "14_architectuurbeslissingen"


def adr(nr, titel, status, datum, betreft, situatie, opties, afweging, besluit, oplevert, rekening, hangt, bewijs, extra=None):
    b = [Heading(f"ADR-{nr:04d}: {titel}"),
         Table(kop=["Nummer", "Status", "Datum", "Betreft"], rijen=[[f"ADR-{nr:04d}", status, datum, betreft]], kolombreedtes=[2, 2, 3, 5]),
         Heading("De situatie", 2), Para(situatie),
         Heading("Overwogen opties", 2), Bullets(opties),
         Heading("De afweging", 2)]
    b += [afweging] if not isinstance(afweging, list) else afweging
    b += [Heading("Het besluit", 2), Para(besluit),
          Heading("Wat het oplevert", 2), Bullets(oplevert),
          Heading("Waar moet rekening mee worden gehouden", 2), Bullets(rekening)]
    if extra:
        b += extra
    b += [Note(hangt, kop="Hangt samen met"), Para("**Bewijs:** " + bewijs)]
    return b


def document() -> Document:
    bl = [
        Para("Dit document legt zes echte besluiten van MB Ontdekt vast in de vorm van een architectuurbeslissing (ADR). Elk besluit is herleid uit issues, pull requests, de code en de gemeten gegevens; waar een alternatief of reden niet in de bronnen staat, zeggen we dat. De ADR's zijn achteraf opgeschreven (op 2026-11-17), niet op het moment van het besluit; de datum is die van de merge van de uitvoerende pull request."),
        Image(str(D / "besluiten.png"), onderschrift="Figuur 1. De zes besluiten en hun samenhang. Bron: issues en pull requests van Software-BackEnd en Software-FrontEnd (nummers in het diagram).", max_hoogte_mm=60),
        Table(kop=["Nummer", "Besluit", "Repo", "Bewijs"],
              rijen=[["ADR-0001", "Ingest-worker en snapshots in plaats van live bronaanroep", "backend", "issue 206, PR 207"],
                     ["ADR-0002", "Caffeine-cache voor andere tijdstippen", "backend", "issue 206, CacheConfig.java"],
                     ["ADR-0003", "De kaart als hoofdscherm", "frontend", "issue 172, PR 179"],
                     ["ADR-0004", "IDW voor de heatmap, in de browser", "frontend", "issue 184, PR 191"],
                     ["ADR-0005", "Gesigneerde bearer-JWT, geen cookies voor authenticatie", "backend", "PR 120, PR 187, JwtService.java"],
                     ["ADR-0006", "Squash-merges naar s3nj26_dev", "beide", "git-historie"]],
              kolombreedtes=[2, 6, 2, 4]),
    ]
    bl += adr(1, "Worker en snapshots in plaats van live bronaanroep", "Aanvaard", "2026-11-17", "Hoe de kaartgegevens aan de app komen",
        "De kaartendpoints (wijken, stations met metingen, time-lapse) riepen bij elk verzoek meetjestad.net aan. Op de lokale stack met 41.000 metingen duurde dat 1 tot 9 seconden (issue 206: time-lapse 3 tot 9 s, wijken 1 tot 2,7 s, stations 1,8 tot 2,9 s). De app hing daarmee af van de snelheid en beschikbaarheid van een externe bron en kon die bron zwaar belasten, terwijl die geen limiet publiceert.",
        ["**Live per verzoek houden** (de toenmalige situatie).",
         "**Metingen uit de lokale database lezen en per minuut cachen** (de formulering van de acceptatiecriteria in issue 206).",
         "**Een worker die periodiek ophaalt, opslaat en snapshots voorbereidt** (de gekozen oplossing in PR 207)."],
        Table(kop=["Optie", "Sterk", "Zwak"],
              rijen=[["Live per verzoek", "altijd actueel, geen nieuwe onderdelen", "1 tot 9 s, afhankelijk van de bron, belast de bron per bezoeker"],
                     ["Database plus cache", "eenvoudig, snel na de eerste aanroep", "eerste aanroep per minuut blijft duur; wie vult de database?"],
                     ["Worker plus snapshots", "antwoorden komen uit het geheugen, een enkele aanroeper van de bron, status zichtbaar", "meer onderdelen en data die minuten oud is"]],
              kolombreedtes=[3, 4, 4]),
        "De IngestWorker is de enige aanroeper van meetjestad.net. Hij haalt elke 5 minuten incrementeel metingen op, slaat ze idempotent op en bouwt daarna de snapshots opnieuw. Een verzoek voor het huidige tijdstip wordt uit de snapshot beantwoord; elk ander tijdstip uit de lokale database.",
        [ "Responstijd van 0,003 tot 0,023 seconden in plaats van 0,8 tot 2,0 (PR 207: voor 0,96 / 0,77 / 0,86 s, na 0,023 / 0,007 / 0,007 s voor wijken; ruim een factor 100).",
          "De bron wordt voorzichtig behandeld: minimale tussentijd, maximum per uur, backoff met jitter.",
          "De versheid is zichtbaar (X-Data-As-Of, /api/status, readiness DEGRADED) en een nieuw endpoint /api/snapshot geeft alles in een antwoord."],
        ["Data is zo oud als de laatste ingest (standaard maximaal ongeveer 5 minuten, bij uitval van de bron langer). PR 207 noemt dit zelf een gedragswijziging.",
         "Tijdstippen worden op de minuut naar beneden afgerond; de time-lapse kan licht afwijken van de oude route (in de proef tot ongeveer 0,5 graad in enkele wijken).",
         "De 6-uurs-sync is vervangen; de worker draait in het geheugen van een enkel proces (geen tweede instantie zonder dubbel ophalen).",
         "De frontend leest de versheidssignalen op dit moment nog niet."],
        "ADR-0002 (cache), het document Architectuur en dataflow en het document Foutafhandeling en betrouwbaarheid.",
        "issue 206 (gesloten 2026-11-17), PR 207 met de meettabel in de beschrijving, IngestWorker.java, SnapshotService.java; commit e104152. De metingen zijn uit PR 207 overgenomen, niet opnieuw uitgevoerd.",
        extra=[Image(str(D / "voor-na.png"), onderschrift="Figuur 2. Voor en na ADR-0001. Bron: beschrijving van backend PR 207; waarden overgenomen.", max_hoogte_mm=80)])
    bl += adr(2, "Caffeine-cache voor andere tijdstippen", "Aanvaard", "2026-11-17", "Beperkt cachen van berekende antwoorden",
        "De snapshots dekken alleen het huidige tijdstip en de standaard time-lapse. Een gebruiker die in de tijdlijn naar een ander moment gaat, vraagt een berekening uit de lokale database, die per verzoek duur is en bij herhaling steeds opnieuw zou lopen.",
        ["**Geen cache**: elk ander tijdstip opnieuw berekenen.",
         "**Caffeine in het geheugen** met korte levensduur en een maximum aantal items (issue 206 noemt dit als voorbeeld).",
         "**Een gedeelde cache** zoals Redis (RateLimiter.java noemt dat als vervolg voor meerdere instanties; niet gebouwd)."],
        Table(kop=["Optie", "Sterk", "Zwak"],
              rijen=[["Geen cache", "niets te beheren", "herhaalde dure berekeningen, client kan de database belasten"],
                     ["Caffeine", "geen extra onderdeel, begrensd geheugen", "per instantie, verdwijnt bij herstart"],
                     ["Gedeelde cache", "werkt over instanties heen", "extra onderdeel en beheer, nu niet nodig"]],
              kolombreedtes=[3, 4, 4]),
        "Drie Caffeine-caches (stations met metingen, wijken op tijdstip, time-lapse) met een levensduur van 60 seconden en een maximum van 120 items (20 voor de time-lapse, omdat een antwoord honderden kilobytes groot is). De sleutel is het op de minuut afgeronde tijdstip.",
        ["Een client die steeds een ander tijdstip vraagt kan het geheugen niet laten groeien: elke cache heeft een maximum.", "De waarden zijn instelbaar zonder codewijziging (map.cache.*).", "Cache-statistieken worden bijgehouden (recordStats)."],
        ["Per instantie: bij meerdere backends heeft elk een eigen cache.", "Een cachehit toont maximaal 60 seconden oude berekening bovenop de ingest-vertraging.", "Er is geen metrics-endpoint dat de hit-ratio laat zien."],
        "ADR-0001: de cache vangt op wat de snapshots niet dekken.",
        "ClimateChecker/src/main/java/.../cache/CacheConfig.java en application.properties (map.cache.ttl-seconds=60, max-entries=120, timelapse-max-entries=20); issue 206; commit e104152.")
    bl += adr(3, "De kaart als hoofdscherm", "Aanvaard, later bijgesteld", "2026-11-17", "Navigatie en eerste scherm van de app",
        "De app had aparte pagina's voor Home, Heatmap en Wijken. Een gebruiker moest tussen die pagina's wisselen om het klimaat in zijn stad te zien (issue 172: kaart als hoofdscherm, zodat niet tussen Home, Heatmap en Wijken gewisseld hoeft te worden).",
        ["**Aparte pagina's houden** (Home met samenvattingsstrook, Heatmap, Wijken).",
         "**De kaart als hoofdscherm** op de route /, volledig scherm met zwevende knoppen; wijkenlijst als zijpaneel (desktop) of bottom sheet (mobiel)."],
        Table(kop=["Optie", "Sterk", "Zwak"],
              rijen=[["Aparte pagina's", "elke pagina is eenvoudig", "wisselen kost tijd; dezelfde cijfers op meerdere plekken"],
                     ["Kaart als hoofdscherm", "direct zicht op de stad, een plek voor wijkdetails", "veel op een scherm; oude links moeten blijven werken"]],
              kolombreedtes=[3, 4, 4]),
        "De kaart is het hoofdscherm (/). Een wijk opent als /wijk/:id op dezelfde pagina met een detailsheet, zodat de kaart niet opnieuw laadt. Oude routes sturen door naar de kaart (legacy-routes.js). De issue noemt als inspiratie een ontwerpreview met referenties uit RainViewer, Ventusky en Watch Duty.",
        ["Een eerste scherm dat meteen de situatie toont, met detail zonder paginawissel.", "Bestaande links blijven werken door de doorverwijzingen."],
        ["Het besluit is bijgesteld: issue 187 vraagt dat elk menu-item iets anders doet. In de huidige code (main.jsx) zijn /heatmap, /wijken en /dashboard weer eigen pagina's; alleen de overige oude routes sturen nog door naar de kaart.",
         "De wijkdetailroute is een kinderroute van de kaart, dus de kaartpagina is groot (lazy geladen)."],
        "ADR-0004 (Heatmap als eigen pagina).",
        "frontend issue 172 en 187, PR 179 (gemerged 2026-11-17), src/main.jsx en src/utils/legacy-routes.js, commit 13fc1e2. De reden voor de bijstelling is uit issue 187 afgeleid.")
    bl += adr(4, "IDW voor de heatmap, in de browser", "Aanvaard", "2026-11-17", "Hoe het doorlopende kleurvlak wordt berekend",
        "De kaart kleurt per wijk. Voor het patroon over de stad, los van wijkgrenzen, is een doorlopend vlak nodig dat tussen de meetstations schat (issue 184).",
        ["**Wijkgemiddelden** tonen (de bestaande kaart); toont geen patroon binnen een wijk.",
         "**IDW (inverse distance weighting) in de browser** op een raster, als beeldlaag op MapLibre.",
         "**Berekenen op de server**: in de bronnen niet uitgewerkt of afgewogen; andere interpolatiemethoden worden ook niet genoemd."],
        Table(kop=["Optie", "Sterk", "Zwak"],
              rijen=[["Wijkgemiddelden", "bestaat al", "geen patroon binnen een wijk"],
                     ["IDW in de browser", "eenvoudig, pure functie met tests, geen extra API", "rekenwerk in de browser; schatting, geen meting"]],
              kolombreedtes=[3, 4, 4]),
        "Client-side IDW (macht 2) op een raster. Binnen 1 km van een station telt het kleurvlak volledig, tussen 1 en 2,5 km vervaagt het, daarbuiten blijft het leeg: er wordt niets verzonnen. Stations zonder meting van de laatste 2 uur of zonder positie doen niet mee.",
        ["Zichtbare hotspots en koele plekken; leeg gebied waar geen station is.", "De interpolatie is een pure functie (interpolation.js), getest op 0, 1 en 2 stations.", "Een klik toont de geschatte waarde en de drie dichtstbijzijnde stations."],
        ["Een schatting kan misleiden tussen verre stations; de grens van 2,5 km is een keuze, niet gemeten.", "De kleurschaal heeft een minimale breedte (3 graden, 10 microgram per kubieke meter) om kleine verschillen niet groot te laten lijken.", "Het aantal stations (43 lokaal) bepaalt hoe grof het beeld is."],
        "ADR-0003: Kaart toont per wijk, Heatmap het patroon.",
        "frontend issue 184, PR 191, src/utils/interpolation.js (FULL_COVERAGE_KM=1, MAX_COVERAGE_KM=2.5, IDW_POWER=2, uit de code overgenomen); commit 13fc1e2.")
    bl += adr(5, "Gesigneerde bearer-JWT, geen cookies voor authenticatie", "Aanvaard", "2026-09-17", "Hoe een ingelogde gebruiker zich bij elk verzoek bekendmaakt",
        "PR 120 (security-hardening) beschrijft dat de station-claim een cookiewaarde blind als gebruikers-id vertrouwde (auth-bypass en IDOR) en dat de JWT-sleutel in de code stond.",
        ["**Gebruikers-id in een cookie** (de oude, onveilige situatie).",
         "**Serversessies met sessiecookie**: in de bronnen niet afgewogen; Spring Security maakt wel een sessie aan (JSESSIONID, lokaal vastgesteld) maar authenticatie loopt er niet over.",
         "**Gesigneerde JWT in de Authorization-header** (gekozen)."],
        Table(kop=["Optie", "Sterk", "Zwak"],
              rijen=[["Id in cookie", "eenvoudig", "te vervalsen: vertrouwt de client"],
                     ["Serversessie", "intrekbaar", "toestand op de server, niet afgewogen in de bronnen"],
                     ["Bearer-JWT", "stateless, geen CSRF-risico via cookies, eenvoudig in de API en Swagger", "niet intrekbaar voor het verlopen; opslag in de browser"]],
              kolombreedtes=[3, 4, 4]),
        "De backend tekent een JWT (HS256, tien uur geldig) en leest hem uit Authorization: Bearer. Het JWT-filter kijkt niet naar cookies. De sleutel komt uit de omgeving (JWT_SECRET) en de app start buiten dev en test niet met een ontbrekende of bekende standaardsleutel (PR 187).",
        ["Een gebruiker kan niet meer als een ander optreden door een cookiewaarde aan te passen.", "Een eigen sleutel per omgeving is afgedwongen bij het opstarten.", "CSRF kan uit omdat er geen cookie-authenticatie is."],
        ["De frontend bewaart het token in localStorage: een XSS-lek kan het lezen. Een token is niet in te trekken voor het verloopt en er is geen refresh.", "Een JWT_SECRET roteren logt alle gebruikers uit.", "De README zegt dat cookies niet worden gebruikt; er wordt toch een sessiecookie gezet (zie Beveiliging)."],
        "ADR over 2FA met vertrouwd IP is hier niet opgenomen; zie het document Beveiliging.",
        "backend PR 120 (gemerged 2026-09-17) en PR 187 (2026-11-17), JwtService.java, JwtAuthenticationFilter.java, JwtSecretGuard.java, auth-provider.jsx, commit e104152. De PR 120 geeft het probleem, niet de afweging tussen opties.")
    bl += adr(6, "Squash-merges naar s3nj26_dev", "Aanvaard (afgeleid uit de praktijk)", "2026-11-17", "Hoe pull requests in de ontwikkelbranch komen",
        "Pull requests naar s3nj26_dev werden eerst met een merge-commit samengevoegd. In de recente historie staan enkelvoudige commits met de titel van de PR en het nummer erachter (bijvoorbeeld '... (#207)').",
        ["**Merge-commit**: de hele branch-historie blijft zichtbaar; de eerdere praktijk (backend PR 187, 191 en 192).",
         "**Squash-merge**: een commit per PR, met de PR-titel als bericht.",
         "**Rebase-merge**: in de bronnen niet gebruikt of besproken."],
        Table(kop=["Optie", "Sterk", "Zwak"],
              rijen=[["Merge-commit", "volledige historie", "veel losse commits, rommelige hoofdlijn"],
                     ["Squash-merge", "een leesbare lijn: een commit per PR, gemakkelijk terug te draaien", "details van tussentijdse commits gaan verloren; stacked PR's moeten opnieuw gebaseerd worden"]],
              kolombreedtes=[3, 4, 4]),
        "Pull requests naar s3nj26_dev worden gesquasht. De laatste negen backend-commits op de eerste-ouder-lijn (de PR's 197, 202 tot en met 205 en 207, met daartussen de commits van 193 tot en met 195) zijn enkelvoudige commits; de merge-commits (PR 187, 191, 192) zijn ouder. In de frontend zijn PR 195 en 196 enkelvoudige commits; PR 194 (een integratiebranch) is nog een merge-commit. Een besluit als tekst is in de repo's niet gevonden; dit is afgeleid uit de historie.",
        ["Een leesbare hoofdlijn met een commit per onderwerp, die aansluit bij het commit-prefix (feat, fix, test, docs).", "Het issue- of PR-nummer staat in de commit voor herleidbaarheid."],
        ["Gestapelde pull requests (frontend 179, dan 173, dan 174) moeten na een squash opnieuw worden gebaseerd, wat PR 179 zelf al benoemt.", "De tussenliggende commits van een branch verdwijnen uit de hoofdlijn.", "Er is geen afgedwongen regel in de repo-instellingen die we hebben kunnen lezen; het blijft een afspraak."],
        "Het document Versiebeheer en werkwijze, indien aanwezig in de set.",
        "git log --first-parent origin/s3nj26_dev in beide repo's (commit e104152 en 13fc1e2). Sinds 2026-09-18 telt de lijn in de backend 16 commits met een ouder en 8 merge-commits, in de frontend 14 en 7.")
    bl += [Heading("Bronnen en controle"),
           Bullets(["OntdekIT/Software-BackEnd, commit e104152e572449be91d75b1d86a3bcecd6d4f5d0 en OntdekIT/Software-FrontEnd, commit 13fc1e2f086ea4c2c52c37188294b6e3921bfebd (origin/s3nj26_dev).",
                    "Issues en pull requests via gh: backend 120, 182, 187, 206, 207; frontend 172, 179, 184, 187, 191.",
                    "Datum: 2026-11-17."]),
           Para("**Onduidelijk:** de afwegingen zijn achteraf uit de bronnen opgebouwd. Waar de bronnen geen alternatief noemen (serversessies, andere interpolatiemethoden, rebase-merge) is dat zo gemeld. Of het team deze besluiten zo heeft genomen, is niet vast te stellen."),
           ]
    return Document(
        meta=Meta(titel="Architectuurbeslissingen", ondertitel="Zes echte besluiten van MB Ontdekt, met bewijs uit issues, pull requests en code.",
                  kopregels=[("Systeem", "MB Ontdekt / ClimateChecker"), ("Datum", "2026-11-17"), ("Aantal", "6 ADR's")]),
        voettekst="MB Ontdekt · architectuurbeslissingen",
        blokken=bl,
    )
