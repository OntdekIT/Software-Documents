"""09 Beveiliging van MB Ontdekt (technische-verantwoording-recept)."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from docgen import Bullets, Document, Heading, Image, Meta, Note, Para, Table

D = Path(__file__).resolve().parents[1] / "diagrammen" / "architectuur" / "09_beveiliging"
BR = "(commit backend e104152, frontend 13fc1e2, 2026-11-17)"


def document() -> Document:
    return Document(
        meta=Meta(titel="Beveiliging", ondertitel="Hoe MB Ontdekt gebruikers, tokens en endpoints beschermt, en welke risico's openstaan.",
                  kopregels=[("Systeem", "MB Ontdekt / ClimateChecker"), ("Datum", "2026-11-17"), ("Bron", "code en live aanroepen")]),
        voettekst="MB Ontdekt · beveiliging",
        blokken=[
            Para("Dit document beschrijft de beveiliging zoals die in de code staat, niet zoals ze bedoeld was. De toegangsregels zijn uit SecurityConfiguration.java gelezen en daarna met echte, anonieme aanroepen op de lokale backend gecontroleerd: voor alle 32 operaties buiten /api/authentication klopte de regel met het antwoord."),
            Heading("Lagen in de keten"),
            Para("Elk verzoek loopt eerst door de RateLimitingFilter (hoogste voorrang, dus ook een 401 draagt de header X-Rate-Limit-Limit, dat is lokaal vastgesteld), daarna CORS, de JwtAuthenticationFilter en de autorisatieregels. Fouten komen in een vaste JSON-vorm terug (zie het document over foutafhandeling)."),
            Image(str(D / "filterketen.png"), onderschrift="Figuur 1. De filterketen. Bron: RateLimitingFilter.java, CorsConfig.java, JwtAuthenticationFilter.java, SecurityConfiguration.java " + BR, max_hoogte_mm=60),
            Heading("Inloggen, 2FA-mail en vertrouwd IP"),
            Para("Een gebruiker logt in met e-mail en wachtwoord (Argon2-hash). Komt het verzoek van een IP-adres dat de gebruiker eerder via de mailcode heeft bevestigd, dan volgt direct een JWT. Anders mailt de backend een zescijferige code, die vijf minuten geldig is en na gebruik wordt verwijderd. Na een geslaagde verificatie onthoudt de backend het IP als HMAC-SHA256 met een geheime pepper, zodat een databaselek geen leesbare IP-adressen geeft. Een JWT is tien uur geldig (HS256). De React-app bewaart het token in localStorage en stuurt het als Authorization: Bearer mee."),
            Image(str(D / "sequentie-login.png"), onderschrift="Figuur 2. Inlogstroom. Bron: UserAuthenticationController.java, TrustedIpService.java, TokenService.java, JwtService.java, auth-provider.jsx " + BR, max_hoogte_mm=165),
            Heading("Wie mag wat"),
            Para("Er zijn drie rollen in UserRole: USER, ADMIN en SUPER_ADMIN. Het diagram deelt alle 37 operaties van de API in naar de eerste passende regel in SecurityConfiguration. Alles dat niet expliciet openstaat vereist een login (anyRequest().authenticated())."),
            Image(str(D / "toegang.png"), onderschrift="Figuur 3. Toegang per operatie. Bron: SecurityConfiguration.java toegepast op docs/api/openapi.json, gecontroleerd met anonieme aanroepen " + BR, max_hoogte_mm=140),
            Heading("Maatregelen in de code"),
            Table(kop=["Maatregel", "Waar", "Waarde"],
                  rijen=[["Rate limiting per IP", "RateLimitingFilter.java (Bucket4J)", "20 per minuut standaard, 600 in de lokale compose"],
                         ["Extra limiet inlogacties", "RateLimiter.java", "5 per minuut per actie, IP en e-mail"],
                         ["Geen standaardgeheimen buiten dev en test", "JwtSecretGuard.java, DefaultCredentialsGuard.java", "app start niet met bekende JWT-sleutel, pepper of wachtwoord"],
                         ["Vertrouwde proxies voor X-Forwarded-For", "ClientIpResolver.java", "alleen loopback en privereeksen, instelbaar via TRUSTED_PROXIES"],
                         ["CORS alleen eigen frontend", "CorsConfig.java", "cors.allowed-origins; een vreemde Origin kreeg lokaal 403"],
                         ["Wachtwoordsterkte", "PasswordRules.java", "8 tot 128 tekens, hoofdletter en cijfer"],
                         ["Zelfde antwoord bij vergeten wachtwoord", "UserAuthenticationController.java", "voorkomt dat bestaande accounts te raden zijn"],
                         ["Claim weigert eigen station van een ander", "StationService.java", "409 als het station al een eigenaar heeft"],
                         ["Alleen health in actuator", "application.properties", "management.endpoints.web.exposure.include=health; /actuator/env gaf 401"],
                         ["API-documentatie uit buiten dev en test", "application.properties", "springdoc standaard uit; lokaal (profiel dev) 302 op /swagger-ui.html"],
                         ["Container als niet-root gebruiker", "Dockerfile", "gebruiker app"],
                         ["Geheimen scannen in de frontend-CI", "security.yml (frontend)", "gitleaks en npm audit"]],
                  kolombreedtes=[3, 3, 4]),
            Heading("Beveiligingsissue 198 naast de code"),
            Para("Issue 198 (backend) staat nog open, maar de bijbehorende pull request #202 is gemerged. Elk acceptatiecriterium is in de code terug te vinden:"),
            Table(kop=["Criterium uit issue 198", "In de code"],
                  rijen=[["Claim weigert een al geclaimd station", "StationService.ClaimMeetstation: 409 bij bestaande eigenaar"],
                         ["POST /meetstation/add vereist rol en gebruikt een request-DTO", "SecurityConfiguration: hasAnyAuthority ADMIN of SUPER_ADMIN; AddStationRequest"],
                         ["forgot-password geeft altijd hetzelfde antwoord", "UserAuthenticationController: altijd 200, fouten alleen gelogd"],
                         ["register valideert wachtwoordsterkte", "PasswordRules.PATTERN in register"],
                         ["X-Forwarded-For alleen van bekende proxy", "ClientIpResolver"],
                         ["Geen standaardwachtwoorden of JWT-sleutel buiten dev en test", "JwtSecretGuard, DefaultCredentialsGuard"],
                         ["Hardcoded @CrossOrigin weg", "geen @CrossOrigin meer in de broncode (docs/deployment.md noemt hem nog: verouderd)"]],
                  kolombreedtes=[5, 5]),
            Para("Dat de issue open staat terwijl de code klaar is, is een administratieve afwijking. Of elk punt een eigen test heeft (het laatste criterium) is hier niet per punt nagelopen."),
            Heading("Openstaande risico's"),
            Para("Gerangschikt op ernst. Dit zijn bevindingen uit de code en live aanroepen, geen aannames."),
            Heading("Aanpakken", 2),
            Bullets(["**Publieke respons bevat registratiecode en eigenaar.** GET /api/meetstation/stations en /stations-met-measurements zijn publiek en StationDto bevat registrationCode en userid. Lokaal zijn alle 43 stations nog zonder code (0) en zonder eigenaar, dus daar is niets te lekken; in een omgeving met echte codes zou iedereen ze kunnen lezen. Oplossing: een aparte publieke DTO zonder deze velden.",
                     "**Gelekte MailSlurp-sleutel nog niet ingetrokken en per-omgeving geheimen** (issue 182 staat open; handmatig in het MailSlurp-dashboard).",
                     "**Persoonlijke Gmail-adressen hardcoded als afzender** in EmailSenderService.java (setFrom). Zet het afzenderadres in de configuratie."]),
            Heading("Wees ervan bewust", 2),
            Bullets(["**JWT in localStorage**: een XSS-lek zou het token kunnen lezen. Er is geen intrekken van een token voor het verlopen (tien uur) en geen refresh.",
                     "**Rate limiting in het geheugen per instantie**: bij meer dan een backend-instantie telt elke instantie apart. De code zegt dit zelf (RateLimiter.java). Buckets worden niet opgeruimd, wat bij veel unieke IP-adressen geheugen kost.",
                     "**Sessiecookie**: een anonieme aanroep kreeg lokaal een JSESSIONID-cookie (HttpOnly), terwijl de README zegt dat cookies niet worden gebruikt. De sessiebeleid is niet op stateless gezet.",
                     "**CSRF staat uit**: dat is bij bearer-tokens gangbaar, maar volgt alleen uit de keuze om geen cookies voor authenticatie te gebruiken.",
                     "**Dump met gebruikersgegevens in de repo**: ClimateChecker/res/dump-ontdekstation013-202506121529.sql bevat een INSERT voor de tabel user met drie rijen, waaronder e-mailadressen. Zie het document over backups en AVG."]),
            Heading("Bronnen en controle"),
            Bullets(["OntdekIT/Software-BackEnd, commit e104152e572449be91d75b1d86a3bcecd6d4f5d0; OntdekIT/Software-FrontEnd, commit 13fc1e2f086ea4c2c52c37188294b6e3921bfebd.",
                     "Issues en pull requests: Software-BackEnd #198, #182, #202; live aanroepen op de lokale stack (http://localhost:8082).",
                     "Datum: 2026-11-17."]),
            Para("**Onduidelijk:** de beveiligingsinstellingen van test, acceptatie en productie (HTTPS, headers van de proxy, de werkelijke waarden van TRUSTED_PROXIES en de limieten) zijn niet vast te stellen. Er is geen penetratietest uitgevoerd; dit document leest de code en test de lokale stack."),
        ],
    )
