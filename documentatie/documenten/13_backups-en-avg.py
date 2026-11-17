"""13 Backups en AVG (technische-verantwoording-recept)."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from docgen import Bullets, Document, Heading, Image, Meta, Note, Para, Table

D = Path(__file__).resolve().parents[1] / "diagrammen" / "architectuur" / "13_backups-en-avg"
BR = "(commit backend e104152, 2026-11-17)"


def document() -> Document:
    return Document(
        meta=Meta(titel="Backups en AVG", ondertitel="Welke gegevens MB Ontdekt bewaart, welke daarvan persoonsgegevens zijn, en wat er over backups vast te stellen is.",
                  kopregels=[("Systeem", "MB Ontdekt / ClimateChecker"), ("Datum", "2026-11-17"), ("Bron", "echt databaseschema en code")]),
        voettekst="MB Ontdekt · backups en AVG",
        blokken=[
            Note("De database bevat weinig persoonsgegevens: naam, e-mailadres en wachtwoordhash van gebruikers, de naam van een station en (gepseudonimiseerd) het IP-adres van vertrouwde apparaten, plus de locatie van meetstations. Over backups staat in de repo's alleen wat er hoort te gebeuren, niet wat er draait. Of er echt backups worden gemaakt en of ze herstelbaar zijn, is uit de repo's niet vast te stellen.", kop="Kort gezegd"),
            Heading("Het echte schema"),
            Para("Het ERD is afgeleid uit information_schema van de lokale database (alleen-lezen) en toont alle tabellen, kolommen en relaties. Gekleurde kolommen bevatten persoons- of locatiegegevens. Elke kolom is beoordeeld op persoons- of locatiegegevens. Vier tabellen (location, mail, sensor, sensor_type) hebben geen entiteit in de code en zijn leeg: restanten van het eerste schema. De rijtellingen zijn die van de lokale ontwikkeldatabase op 2026-11-17, niet van een echte omgeving."),
            Image(str(D / "erd.png"), onderschrift="Figuur 1. Databaseschema met persoons- en locatiegegevens gemarkeerd. Bron: information_schema van de lokale database, Flyway-migraties V1_0_0 tot V1_3_0, JPA-entiteiten " + BR, max_hoogte_mm=165),
            Heading("Welke persoons- en locatiegegevens"),
            Table(kop=["Gegeven", "Tabel en kolom", "Soort", "Opmerking"],
                  rijen=[["Voor- en achternaam", "user.first_name, last_name", "direct", "ingevuld bij registratie"],
                         ["E-mailadres", "user.email", "direct", "uniek; ook inlogsleutel en mailadres voor codes en uitvalmeldingen"],
                         ["Wachtwoord", "user.password", "geheim", "Argon2-hash, nooit het wachtwoord zelf"],
                         ["Rol, workshopcode", "user.role, workshop_code", "indirect", "koppelt een persoon aan een workshop"],
                         ["IP-adres van vertrouwde apparaten", "trusted_ip.ip_hash", "gepseudonimiseerd", "HMAC-SHA256 met een geheime pepper; het IP zelf staat niet in de database"],
                         ["Eenmalige code", "token.numeric_code", "geheim", "zes cijfers, vijf minuten geldig"],
                         ["Stationsnaam", "station.name", "mogelijk direct", "vrije tekst door de eigenaar; kan een naam of adres bevatten"],
                         ["Eigenaar van een station", "station.user_id", "indirect", "koppelt een persoon aan een locatie"],
                         ["Locatie van een station", "station.last_known_latitude, longitude; measurement.latitude, longitude", "locatie", "een station kan thuis bij een deelnemer staan; nauwkeurigheid niet onderzocht"]],
                  kolombreedtes=[3, 4, 2, 5]),
            Heading("Waar de gegevens heen gaan"),
            Image(str(D / "persoonsgegevens.png"), onderschrift="Figuur 2. Stroom van persoonsgegevens. Bron: UserAuthenticationController.java, TrustedIpService.java, EmailSenderService.java, SecurityConfiguration.java, StationDto.java, docs/api/openapi.json " + BR, max_hoogte_mm=95),
            Heading("Bewaren en verwijderen", 2),
            Bullets(["**Gebruikers**: een beheerder kan een gebruiker verwijderen (DELETE /api/users/{id}). Dan krijgen de stations van die gebruiker user_id leeg (ON DELETE SET NULL) en verdwijnen de vertrouwde IP's (ON DELETE CASCADE). De gebruiker zelf kan zijn account niet verwijderen of exporteren: /api/my-account kent alleen GET en PUT.",
                     "**Metingen** worden niet opgeruimd; er is geen verwijder- of bewaartermijncode voor de tabel measurement. Dat groeit onbeperkt (43.643 rijen lokaal over twee maanden).",
                     "**Tokens**: een gebruikte of oude code wordt verwijderd bij gebruik of bij een nieuwe code; de tabel heeft geen koppeling met user (geen foreign key) en geen opruimtaak voor codes van gebruikers die nooit meer inloggen.",
                     "**Vertrouwde IP's** hebben geen vervaldatum: eenmaal onthouden blijft het apparaat vertrouwd tot het account verdwijnt.",
                     "**Logs** noemen stationnummers en mailtypes, geen e-mailadressen (EmailSenderService logt het type mail). Bewaartermijn van logs: onduidelijk."]),
            Heading("Aandachtspunten voor de AVG", 2),
            Bullets(["**Publieke stations-endpoint** toont per station naam, coordinaten, userid en registrationCode zonder login (StationDto). Het veld is_public verbergt niets: lokaal kwamen alle 43 stations terug terwijl is_public bij allemaal false is. Lokaal zijn nog geen stations gekoppeld, maar met echte deelnemers is dit een lek van locatie en koppeling.",
                     "**SQL-dump met gebruikers in git**: ClimateChecker/res/dump-ontdekstation013-202506121529.sql staat in de repo en bevat een INSERT voor de tabel user met drie rijen (e-mailadressen in de geschiedenis van de repo). Verwijderen uit de huidige map haalt ze niet uit de geschiedenis.",
                     "**Persoonlijke e-mailadressen in de code**: EmailSenderService.java stelt Gmail-adressen als afzender in (setFrom, onder andere een persoonlijk adres). Dat zijn persoonsgegevens in de broncode.",
                     "**Mail via een derde partij**: de productiemailserver is niet gekozen (docs/email-self-hosting.md is een onderzoek). Zodra mail via een externe relay gaat, is die een verwerker; de repo noemt dat zelf bij Privacy (AVG) als punt om vast te leggen.",
                     "**Geen verwerkingsregister, bewaartermijnen of privacyverklaring** in de repo's gevonden. Er is hier niet naar een rechtsgrond of verwerkersovereenkomst gezocht buiten de repo's."]),
            Heading("Backups"),
            Para("Wat de repo's zeggen: docs/deployment.md schrijft voor om bij de database in Dokploy backups in te schakelen (naar B2-opslag) en een restore te testen voordat productie wordt gebruikt. In de overzichtstabel staat: test optioneel, acceptatie aan, productie aan met een geteste restore. docker-compose-prod.yml bewaart de database op een benoemd volume (db_data), zodat data een herstart overleeft, maar een volume is geen backup."),
            Table(kop=["Vraag", "Antwoord uit de repo's"],
                  rijen=[["Is een backup ingesteld?", "niet vast te stellen; alleen voorgeschreven in docs/deployment.md"],
                         ["Hoe vaak, hoe lang bewaard?", "niet beschreven"],
                         ["Is een restore getest?", "niet vast te stellen; docs/deployment.md eist het voor productie"],
                         ["Wat wordt geback-upt?", "alleen de database is in scope; de worker bouwt snapshots uit de database, dus die hoeven niet"],
                         ["Wat gaat verloren zonder backup?", "gebruikers, claims van stations en workshopcodes. De metingen zijn grotendeels terug te halen bij meetjestad.net, maar de ingest haalt maximaal 168 uur terug (ingest.max-catch-up-hours)"],
                         ["Bestaat een dump?", "ja, in de repo: dump-ontdekstation013-202506121529.sql, geen backupstrategie en met gebruikersgegevens"]],
                  kolombreedtes=[4, 7]),
            Para("Belangrijk onderscheid: de metingen zijn herleidbaar, de gebruikers en stationsclaims niet. Voor het risico is dus vooral de tabel user, station (user_id) en workshop van belang. Omdat Flyway het schema beheert, is het schema zelf reproduceerbaar; de gegevens niet."),
            Heading("Bronnen en controle"),
            Bullets(["OntdekIT/Software-BackEnd, commit e104152e572449be91d75b1d86a3bcecd6d4f5d0: Flyway-migraties, JPA-entiteiten, docs/deployment.md, docs/email-self-hosting.md, ClimateChecker/res/.",
                     "Echte database: information_schema en rijtellingen van de lokale container ontdekit-mariaDB-1 op 2026-11-17; geen inhoud gelezen of opgeslagen."]),
            Para("**Onduidelijk:** of backups in Dokploy daadwerkelijk draaien (de Dokploy-omgeving is niet bevraagd), de bewaartermijn van backups en logs, wie verwerkingsverantwoordelijke is, en of de locaties van stations bij particulieren staan."),
        ],
    )
