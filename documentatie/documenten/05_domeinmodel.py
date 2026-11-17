"""05 Domeinmodel: ERD, klassendiagram en domeinmodel, alles uit de echte bronnen."""
import json, os
from docgen import Document, Meta, Heading, Para, Bullets, Table, Note, Image, Spacer

HIER = os.path.dirname(os.path.abspath(__file__))
DG = os.path.join(HIER, "..", "diagrammen", "domeinmodel")
schema = json.load(open(os.path.join(DG, "schema.json")))
bron = json.load(open(os.path.join(DG, "bron.json")))
SHA = bron["backend_sha"][:7]
AANT = {k: v for k, v in schema["aantallen"]}
BR = f"backend {SHA} (origin/s3nj26_dev)"


def document():
    b = [
        Para("Dit document legt de structuur van de gegevens van ClimateChecker uit. Het bevat drie diagrammen "
             "die allemaal uit de echte bronnen zijn gemaakt: het databaseschema (ERD), de entiteiten uit de "
             "broncode (klassendiagram) en een domeinmodel in de taal van de gebruiker. Het domeinmodel "
             "(objecten en begrippen) en het databaseontwerp (tabellen) zijn verschillende modellen: ze lijken "
             "op elkaar, maar komen niet altijd overeen. Waar ze verschillen staat dat hieronder."),
        Para("Het ERD en het klassendiagram zijn afgeleid uit de draaiende database en uit de Java-broncode. De begrippen staan in het document "
             "Woordenlijst, de wensen in het Analysedocument."),
        Heading("Het domeinmodel in gewone taal"),
        Para("Het domein draait om meetstations die metingen leveren. Een station kan van een gebruiker zijn. "
             "Metingen worden aan een wijk toegerekend op basis van hun positie. Gebruikers kunnen via een "
             "workshopcode een station koppelen."),
        Image(os.path.join(DG, "domein.png"),
              "Domeinmodel. Bron: JPA-entities en NeighbourhoodService in " + BR + ", de bestanden staan in de tabel hieronder.",
              breedte_mm=165),
        Table(["Relatie", "Kardinaliteit", "Bron (bestand:regel)"], [
            ["Gebruiker en Workshop", "veel gebruikers hebben hooguit een workshop", "features/user/User.java:50 (ManyToOne, kolom workshop_code)"],
            ["Gebruiker en Meetstation", "een gebruiker heeft nul of meer stations", "features/user/User.java:47 en features/station/Station.java:63"],
            ["Meetstation en Meting", "een station heeft nul of meer metingen", "features/measurement/Measurement.java:32 (kolom stationid)"],
            ["Wijk en Wijkgrens", "een wijk heeft meerdere hoekpunten (tabel region_coords)", "features/neighbourhood/NeighbourhoodCoords.java:19"],
            ["Meting en Wijk", "berekend per verzoek, niet opgeslagen", "features/neighbourhood/NeighbourhoodService.java:161 (pointInPolygon)"],
            ["Gebruiker en Inlogcode", "geen foreign key; user_id is een gewoon veld", "features/user/authentication/Token.java:18"],
            ["Gebruiker en Vertrouwd IP", "FK in database; entity bewaart alleen het id", "db/migration/V1_1_0__trusted_ip.sql, TrustedIp.java"],
        ], kolombreedtes=[2.2, 3.2, 4.6]),
        Note("Een wijk heeft in de database geen koppeling met metingen. Welke meting bij welke wijk hoort wordt bij "
             "elke berekening bepaald met een point-in-polygon-test op de positie van de meting. "
             "In de code heet een wijk Neighbourhood en staat hij in de tabel region.", kop="Leesregel"),
        Heading("Het databaseschema (ERD)"),
        Para(f"Het ERD is uitgelezen uit de lokaal draaiende MariaDB ({schema['dbversie']}) op {schema['uitgelezen']}. "
             "Amber gekleurde tabellen hebben een entity in de code. Lichtgrijze, gestippelde tabellen hebben geen "
             "entity. Een vraagteken achter een kolomnaam betekent dat de kolom leeg mag zijn. De tabel "
             "flyway_schema_history (de administratie van Flyway) is weggelaten."),
        Image(os.path.join(DG, "erd.png"),
              "ERD. Bron: information_schema van de database ontdekstation013 (Flyway 1.0.0 tot 1.3.0), " + BR + ".",
              breedte_mm=165, max_hoogte_mm=215),
        Heading("De entiteiten in de code (klassendiagram)"),
        Para("Het klassendiagram is afgeleid uit de entities in de Java-broncode "
             "(klassen met @Entity). De naam tussen haakjes boven elke klasse is de databasetabel. Pijlen komen uit "
             "@ManyToOne en @OneToMany. De rol van een gebruiker wordt als getal (ORDINAL) opgeslagen, "
             "het type van een inlogcode als tekst."),
        Image(os.path.join(DG, "klassen.png"),
              "Klassendiagram. Bron: de @Entity-klassen onder ClimateChecker/src/main/java in " + BR + ".",
              breedte_mm=165),
        Heading("Rollen"),
        Table(["Waarde in de database", "Rol in de code", "Betekenis"], [
            ["0", "USER", "gewone gebruiker"],
            ["1", "SUPER_ADMIN", "superbeheerder"],
            ["2", "ADMIN", "beheerder"],
        ], kolombreedtes=[2, 2, 3]),
        Para("De waarde in de database volgt de volgorde van de enum UserRole.java (EnumType.ORDINAL). Wie de volgorde "
             "van de enum wijzigt, verandert dus de rechten van bestaande gebruikers."),
        Heading("Wat de gegevens nu bevatten"),
        Table(["Tabel", "Aantal rijen in de lokale database"], [
            ["station", AANT["station"]],
            ["measurement", AANT["measurement"]],
            ["region (wijken)", AANT["region"]],
            ["region_coords (hoekpunten)", AANT["region_coords"]],
        ], kolombreedtes=[3, 3], uitlijning=["links", "rechts"]),
        Para(f"Dit zijn tellingen van de lokale ontwikkeldatabase op {schema['uitgelezen']}, geen productiecijfers."),
        Heading("Verschillen tussen code en database"),
        Bullets([
            "**Vier tabellen zonder entity.** location, sensor, sensor_type en mail komen uit het oude schema "
            "(V1_0_0__inti.sql) en worden door de code niet gebruikt. De tabellen zijn leeg. station.location_locationid "
            "verwijst nog wel naar location, terwijl de positie van een station nu uit de metingen en uit "
            "last_known_latitude en last_known_longitude komt (migratie V1_2_0).",
            "**Dubbele foreign keys.** station.user_id en user.workshop_code hebben elk twee constraints "
            "(een door Hibernate gegenereerde en een eigen met ON DELETE SET NULL), zie V1_0_0__inti.sql.",
            "**Workshop.** De entity markeert verloopdatum en aanmaakdatum als verplicht (@NotNull), "
            "de databasekolommen staan als leeg toegestaan.",
            "**Token.** De entity Token heeft geen @Table en geen koppeling met User. Hibernate valideert het schema "
            "(ddl-auto=validate), maar er is geen foreign key van token.user_id naar user.",
            "**Wijk en meting.** De entity Measurement heeft geen veld voor de wijk; dat is een bewuste keuze (de wijk "
            "wordt uit de positie berekend), maar het betekent dat een wijkgrenswijziging terugwerkt op oude metingen.",
        ]),
        Heading("Bronnen en controle"),
        Bullets([
            f"Backend: OntdekIT/Software-BackEnd, commit {bron['backend_sha']} (origin/s3nj26_dev). Gelezen: de entities onder features/, db/migration/V1_0_0 tot V1_3_0, NeighbourhoodService.",
            f"Database: container ontdekit-mariaDB-1, MariaDB {schema['dbversie']}, schema ontdekstation013, uitgelezen {schema['uitgelezen']} (alleen SELECT op information_schema). Flyway-geschiedenis: " + ", ".join(v for v, _ in schema["flyway"]) + " (gelijk aan de vier migratiebestanden in de repo).",
            "Diagrambronnen: erd.dot, klassen.puml en domein.dot, gebaseerd op de database-uitlezing en de entities hierboven.",
            "Datum van dit document: 2026-11-17.",
        ]),
        Para("**Onduidelijk gebleven:** het EER-diagram uit het oude Analysedocument iteratie 4 (s3nj24) is een afbeelding in een "
             "Word-bestand en is niet vergeleken met het huidige schema. Of de oude tabellen location, sensor, sensor_type en "
             "mail in de productiedatabase nog gevuld zijn, is niet vast te stellen vanuit de lokale database."),
    ]
    return Document(meta=Meta("Domeinmodel", "De gegevens van ClimateChecker: database, code en begrippen.",
                              [("Datum", "2026-11-17"), ("Bron", f"backend {SHA}")]),
                    blokken=b, voettekst="MB Ontdekt - ClimateChecker - domeinmodel")
