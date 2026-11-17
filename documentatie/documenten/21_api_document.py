"""21 API-document: endpointtabel en API-kaart, afgeleid uit de OpenAPI-specificatie."""
import json, os
from docgen import Document, Meta, Heading, Para, Bullets, Table, Note, Code, Image

HIER = os.path.dirname(os.path.abspath(__file__))
DG = os.path.join(HIER, "..", "diagrammen", "api-document")
E = json.load(open(os.path.join(DG, "endpoints.json")))
SHA = E["backend_sha"][:7]
def _compact(o, diep=0):
    """Boven niveau 2 een regel per sleutel, daaronder alles op een regel."""
    if diep >= 2 or not isinstance(o, (dict, list)):
        return json.dumps(o, ensure_ascii=False)
    pad = "  " * (diep + 1)
    if isinstance(o, dict):
        return "{\n" + ",\n".join(f'{pad}"{k}": {_compact(v, diep + 1)}' for k, v in o.items()) + "\n" + "  " * diep + "}"
    return "[\n" + ",\n".join(pad + _compact(v, diep + 1) for v in o) + "\n" + "  " * diep + "]"


SNAP = _compact(json.load(open(os.path.join(DG, "snapshot-voorbeeld.json"))))
TOEG = {"openbaar": "openbaar", "ingelogd": "ingelogd", "beheerder": "beheerder"}


def tabel(groep):
    rijen = []
    for e in E["endpoints"]:
        if e["groep"] != groep:
            continue
        rijen.append([f"**{e['methode']}** {e['pad']}", e["samenvatting"], TOEG[e["toegang"]],
                      ", ".join(e["parameters"]) or "-", ", ".join(e["statuscodes"])])
    return Table(["Endpoint", "Wat het doet", "Toegang", "Parameters", "Codes"], rijen,
                 kolombreedtes=[4.2, 3.4, 1.6, 3.6, 1.5])


def document():
    groepen = []
    for e in E["endpoints"]:
        if e["groep"] not in groepen:
            groepen.append(e["groep"])
    b = [
        Para(f"Dit document beschrijft de REST-API van de ClimateChecker-backend ({len(E['endpoints'])} endpoints). "
             "Het is afgeleid uit docs/api/openapi.json van de backend en vergeleken met de live OpenAPI-specificatie "
             "van de draaiende backend (/v3/api-docs). De kolom Toegang is niet uit de specificatie gehaald maar uit de "
             "echte toegangsregels in SecurityConfiguration.java, omdat de specificatie alleen bearerAuth kent."),
        Note("De API-beschrijving komt uit de code (springdoc). Dit document geeft de stand van 2026-11-17: de specificatie in de repo "
             "en de code zijn leidend, niet dit document.", kop="Let op"),
        Heading("De API-kaart"),
        Image(os.path.join(DG, "api-kaart.png"),
              f"API-kaart. Bron: docs/api/openapi.json en config/SecurityConfiguration.java, backend {E['backend_sha']} (origin/s3nj26_dev).",
              breedte_mm=165),
        Heading("Algemene afspraken"),
        Bullets([
            "**Basispad en formaat.** Alle paden beginnen met /api. De API praat JSON, behalve het PDF-endpoint /api/meetstation/measurements/{id}.",
            "**Inloggen in twee stappen.** POST /api/authentication/login stuurt een code per e-mail, POST /api/authentication/verify "
            "levert een JWT op. Een IP-adres dat eerder via verify is gebruikt wordt onthouden (alleen als HMAC-hash) en slaat de mailstap over "
            "(UserAuthenticationController.java, trustedip/TrustedIpService.java). Het token gaat mee als Authorization: Bearer.",
            "**Rollen.** Openbaar, ingelogd (elke gebruiker) of beheerder (ADMIN of SUPER_ADMIN). Een niet toegestane rol geeft 403, geen of ongeldig token geeft 401.",
            "**Foutantwoord.** Elke fout heeft dezelfde vorm: timestamp, error, statusCode, message (exception/ErrorResponse.java).",
            "**Rate limiting.** Een filter beperkt elk IP tot rate.limit.requests-per-minute verzoeken per minuut (standaard 20, in de lokale compose 600). "
            "Bij overschrijding volgt 429 met X-Rate-Limit-Retry-After-Millis. Daarnaast staat op de inlogendpoints een eigen limiet van 5 pogingen per minuut (utility/RateLimiter.java).",
            "**Versheid van de data.** De kaartendpoints en /api/snapshot sturen X-Data-As-Of mee (moment van de laatste geslaagde ingest). "
            "/api/snapshot ondersteunt ETag met If-None-Match (antwoord 304) en Cache-Control max-age=30.",
            "**Oude paden.** /api/Meetstation (hoofdletter) werkt nog als alias van /api/meetstation, evenals /stationsMetMeasurements, /Claim en /Availibility. "
            "De aliassen staan niet in de specificatie (StationController.java:46 tot 51, 100, 184, 197).",
        ]),
        Heading("Alle endpoints"),
        Para("Codes zijn de statuscodes uit de specificatie. De kolom Parameters toont query-, pad- en headerparameters en het type van de requestbody."),
    ]
    for g in groepen:
        b += [Heading(g, 2), tabel(g)]
    b += [
        Heading("Voorbeeld: /api/snapshot"),
        Para("Het antwoord is in werkelijkheid circa 108 kB (43 stations, 59 wijken met een reeks van 24 uur). Hieronder staat een ingekort antwoord "
             "van de lokale draaiende backend: van elke lijst alleen de eerste twee items. De stations bevatten geen persoonsgegevens."),
        Code(SNAP),
        Para("De velden status en reason bij een station betekenen: status ok (er is een actuele waarde) of no_current_value, met als reden "
             "uitval (geen meting), sensorfout (recente meting zonder temperatuur en PM2.5) of late_meting (laatste meting ouder dan recencyMinutes). "
             "Bron: snapshot/OverviewCalculator.java:178 tot 193."),
        Heading("Afwijkingen tussen specificatie en code"),
        Bullets([
            "POST /api/meetstation/add vereist in SecurityConfiguration de rol ADMIN of SUPER_ADMIN, maar de specificatie noemt alleen 401 en 500 (geen 403).",
            "De specificatie kent geen rollen: elk beveiligd endpoint heeft alleen bearerAuth. De kolom Toegang hierboven vult dat aan uit de code.",
            "OpenAPI is standaard uit (springdoc.api-docs.enabled=false in application.properties) en staat alleen aan in de profielen dev en test. "
            "In productie bestaat /v3/api-docs dus niet, tenzij de omgeving het aanzet.",
            "Het issue Software-BackEnd #196 (OpenAPI en Swagger UI) staat nog open, terwijl PR #197 de functie al heeft samengevoegd. Hetzelfde geldt voor #198 tot #201 en de PR's #202 tot #205.",
            "Het issue Software-Documents #103 (API-documentatie) staat op de bordstatus Not Planned; dit document vervangt de handgeschreven aanpak.",
        ]),
        Heading("Bronnen en controle"),
        Bullets([
            f"Backend: OntdekIT/Software-BackEnd, commit {E['backend_sha']} (origin/s3nj26_dev). Gelezen: docs/api/openapi.json, config/SecurityConfiguration.java, config/ratelimit/RateLimitingFilter.java, utility/RateLimiter.java, exception/ErrorResponse.java, features/station/endpoint/StationController.java, snapshot/OverviewCalculator.java, application*.properties.",
            f"Live: http://localhost:8082/v3/api-docs is {'identiek aan' if E['live_gelijk'] else 'afwijkend van'} docs/api/openapi.json; /api/snapshot en /api/status zijn van dezelfde backend op 2026-11-17.",
            "Diagrambron: api-kaart.dot, afgeleid uit docs/api/openapi.json; het voorbeeldantwoord is van de live backend.",
            "Datum van dit document: 2026-11-17.",
        ]),
        Para("**Onduidelijk gebleven:** de precieze requestbody-velden per endpoint staan in de schema's van de specificatie en zijn hier alleen bij naam genoemd. "
             "Of de productieomgeving /v3/api-docs aan heeft, is niet vast te stellen vanuit de repo."),
    ]
    return Document(meta=Meta("API-document", "De REST-API van ClimateChecker: endpoints, toegang en voorbeeld.",
                              [("Datum", "2026-11-17"), ("Bron", f"backend {SHA}")]),
                    blokken=b, voettekst="MB Ontdekt - ClimateChecker - API-document")
