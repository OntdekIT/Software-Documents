"""De eisen, kwaliteitseisen en use cases van ClimateChecker, met bewijs per regel.

Dit bestand bevat de eisenlijst voor het Analysedocument en de diagrammen.
Statussen: gerealiseerd (in de code van origin/s3nj26_dev aangetroffen), deels, open, niet gepland.
Verwijzingen: BE = Software-BackEnd, FE = Software-FrontEnd, Doc = Software-Documents.
Een issue dat nog open staat terwijl de PR is samengevoegd, is zo vermeld.
"""
G, D, O, N = "gerealiseerd", "deels", "open", "niet gepland"

# (code, onderwerp, wens, bewijs, status)
FR = [
    ("FR-01", "Kaart en wijken", "Het systeem toont de kaart als hoofdscherm op /, met wijken gekleurd naar temperatuur of PM2.5 en stations als markers.", "FE #172, PR #179; main.jsx (route /, Kaart)", G),
    ("FR-02", "Kaart en wijken", "Het systeem toont per wijk een deelbare detailweergave (/wijk/:id) met temperatuur, PM2.5, tijd sinds de laatste meting en een grafiek van 24 uur.", "FE #173, PR #180; main.jsx (wijk/:id). De knop Meld mij (RegionDetails.jsx:157) wacht op meldingsvoorkeuren (FR-27)", D),
    ("FR-03", "Kaart en wijken", "Het systeem laat de afgelopen 24 uur op de kaart afspelen met een LIVE-markering bij het laatste beeld.", "FE #174, PR #181; BE endpoint /api/neighbourhood/history/timelapse; utils/timeline.js", G),
    ("FR-04", "Kaart en wijken", "Het systeem toont een heatmap van temperatuur of PM2.5 als doorlopend kleurvlak, los van wijkgrenzen (/heatmap).", "FE #184, PR #191; main.jsx (route /heatmap)", G),
    ("FR-05", "Kaart en wijken", "Het systeem toont alle wijken als rangschikking en laat er tot drie vergelijken met het stadsgemiddelde (/wijken).", "FE #185, PR #189; main.jsx (route /wijken)", G),
    ("FR-06", "Kaart en wijken", "Het systeem toont een dashboard met de gezondheid van het meetnet: actieve en uitgevallen stations, dekking van 24 uur en uitleg waarom data ontbreekt (/dashboard).", "FE #186, PR #190; main.jsx (route /dashboard); components/dashboard/", G),
    ("FR-07", "Kaart en wijken", "Het systeem toont bij een wijk zonder recente meting Geen recente data in grijs in plaats van een foutwaarde.", "FE #158, PR #169 (issue nog open); utils/region-status.js", G),
    ("FR-08", "Kaart en wijken", "Het systeem toont een samenvatting van kerncijfers (gemiddelde, warmste en koudste wijk, aantal actieve stations) en een legenda met eenheid.", "FE #161 PR #165, FE #160 PR #171 (issues nog open)", G),
    ("FR-09", "Meetstations", "Het systeem laat een ingelogde gebruiker een station claimen dat nog geen eigenaar heeft.", "BE #144; PUT /api/meetstation/claim; StationService.ClaimMeetstation weigert een al geclaimd station", G),
    ("FR-10", "Meetstations", "Het systeem laat de eigenaar of een beheerder een station overdragen aan een andere gebruiker op e-mailadres.", "BE #143, PR #135; StationController.transferMeetstation", G),
    ("FR-11", "Meetstations", "Het systeem laat de eigenaar of een beheerder de naam en zichtbaarheid van een station wijzigen.", "PUT /api/meetstation/edit/{id}; StationController.java:118 (geen apart issue gevonden)", G),
    ("FR-12", "Meetstations", "Het systeem toont een eigenaar zijn stations met status en laatste meting, en een uitleg bij een lege lijst.", "FE #162, PR #166 (issue nog open); route /my/stations", G),
    ("FR-13", "Meetstations", "Het systeem laat een beheerder een station handmatig toevoegen.", "POST /api/meetstation/add (ADMIN); FE #140; admin-route stations/toevoegen", G),
    ("FR-14", "Meetstations", "Het systeem levert de metingen van een station over een periode als PDF.", "GET /api/meetstation/measurements/{id}; StationController.java:156 (geen apart issue gevonden)", G),
    ("FR-15", "Meetstations", "Het systeem laat meetstations vergelijken met elkaar en met een wijk.", "FE #102 staat op Todo; de Wijken-pagina vergelijkt wijken (FR-05), geen stations", O),
    ("FR-16", "Data ophalen en kwaliteit", "Het systeem haalt elke 5 minuten nieuwe metingen op bij meetjestad.net en slaat ze idempotent op in de eigen database.", "BE #148, #149, PR #207; ingest/IngestWorker.java; ingest.interval-seconds=300", G),
    ("FR-17", "Data ophalen en kwaliteit", "Het systeem laat de databron instellen (demo, test, live) via configuratie.", "BE #146, #155, PR #133; meetjestad.base-url in application.properties", G),
    ("FR-18", "Data ophalen en kwaliteit", "Het systeem voegt dubbele metingen samen en verwerkt nagestuurde metingen door elk venster 10 minuten te laten overlappen.", "BE #175, PR #180; MeasurementDeduplicator; BE #177 (late metingen) staat nog open", D),
    ("FR-19", "Data ophalen en kwaliteit", "Het systeem verwerpt onrealistische waarden volgens instelbare grenzen (vocht 0 tot 100, PM 0 tot 1000).", "FE #98, BE PR #186; measurement.limits.* in application.properties", G),
    ("FR-20", "Data ophalen en kwaliteit", "Het systeem geeft een meting zonder geldige GPS-positie de laatst bekende positie van het station.", "BE #185, PR #194 (issue nog open); migratie V1_2_0; Measurement.locationInherited", G),
    ("FR-21", "Data ophalen en kwaliteit", "Het systeem importeert eenmalig historische meetdata.", "BE #176 staat op Todo, geen code aangetroffen", O),
    ("FR-22", "Uitval en storing", "Het systeem detecteert een station zonder meting in de laatste 24 uur en zet het op niet actief.", "BE #140, #142; StationMonitorService.handleInactiveStation; interval 300 s", G),
    ("FR-23", "Uitval en storing", "Het systeem mailt de eigenaar bij uitval en bij een wijziging van een storingsvlag, zonder herhaalde meldingen.", "BE #141, #139; StationMonitorService.updateErrorStatus (alleen bij wijziging); EmailSenderService.sendEmailStationDown", G),
    ("FR-24", "Uitval en storing", "Het systeem geeft per station de reden van een ontbrekende waarde: uitval, sensorfout of late meting.", "snapshot/OverviewCalculator.java:178; Overview.java:55", G),
    ("FR-25", "Uitval en storing", "Het systeem toont een beheerder de dekking van fijnstofdata per station en voor het hele netwerk.", "BE PR #181, FE PR #152; GET /api/measurement/coverage (ADMIN); drempels 80 en 50 procent nog niet bevestigd (Doc #98)", D),
    ("FR-26", "Uitval en storing", "Het systeem laat een gebruiker meldingsvoorkeuren instellen.", "FE #148 niet gepland; de pagina /meldingen zegt dat meldingen eraan komen", N),
    ("FR-27", "Accounts en beheer", "Het systeem laat iemand registreren met een geldige workshopcode en stationcode; het station wordt dan aan hem gekoppeld.", "POST /api/authentication/register (UserAuthenticationController.java:78)", G),
    ("FR-28", "Accounts en beheer", "Het systeem laat een gebruiker inloggen met wachtwoord en een code per e-mail, en slaat de mailstap over vanaf een vertrouwd IP.", "login en verify (UserAuthenticationController.java:114, 137); BE #158, PR #137; FE PR #139", G),
    ("FR-29", "Accounts en beheer", "Het systeem laat een gebruiker zijn wachtwoord herstellen via een e-mailcode.", "forgot-password en reset-password; route /auth/forgot-password", G),
    ("FR-30", "Accounts en beheer", "Het systeem laat een gebruiker zijn eigen naam, e-mail en wachtwoord wijzigen.", "GET en PUT /api/my-account; route /my/account", G),
    ("FR-31", "Accounts en beheer", "Het systeem laat een beheerder gebruikers zoeken, hun rol wijzigen en ze verwijderen, met rolregels voor superbeheerders.", "UserController.java:49 tot 89; admin-route users", G),
    ("FR-32", "Accounts en beheer", "Het systeem laat een beheerder workshopcodes aanmaken, filteren op verlopen, verwijderen en de gebruikers per code tonen.", "WorkshopController (4 endpoints); admin-route workshopcodes", G),
    ("FR-33", "Accounts en beheer", "Het systeem toont het beheer als een scherm met tabs en kerncijfers en waarschuwingen op het overzicht.", "FE #176 PR #178, FE #163 PR #167 (issue nog open); utils/admin-tabs.js, admin-summary.js", G),
]

# (code, onderwerp, eis, bewijs, status)
NFR = [
    ("NFR-01", "Snelheid", "De kaartendpoints antwoorden binnen 300 ms en hangen niet af van meetjestad.net.", "BE #206, PR #207. Eenmalig lokaal gemeten op 2026-11-17: /api/snapshot 17 ms, timelapse 6 ms. Productiecijfers onbekend", G),
    ("NFR-02", "Versheid", "Een meting telt 120 minuten als actueel; zonder geslaagde ingest in 30 minuten is de data verouderd en staat readiness op DEGRADED.", "snapshot.recency-minutes, ingest.stale-after-minutes; IngestHealthIndicator", G),
    ("NFR-03", "Eerlijk gebruik", "De backend belast meetjestad.net hooguit eens per 60 seconden en 30 keer per uur, met oplopende wachttijd (30 seconden tot 30 minuten) na fouten.", "ingest/RequestLimiter.java, BackoffPolicy.java, IngestProperties.java", G),
    ("NFR-04", "Beveiliging", "Wachtwoorden worden met Argon2 bewaard, de backend start buiten dev en test niet zonder eigen JWT_SECRET, IP-adressen worden als HMAC bewaard en actuator toont alleen health.", "ApplicationConfig.java; BE #123, #129, PR #187; TrustedIpService", G),
    ("NFR-05", "Beveiliging", "Inloggen en wachtwoord herstellen zijn begrensd tot 5 pogingen per minuut; alle verzoeken tot 20 per minuut per IP.", "utility/RateLimiter.java; RateLimitingFilter.java; BE #126", G),
    ("NFR-06", "Beveiliging", "Een wachtwoord is 8 tot 128 tekens met minstens een hoofdletter en een cijfer.", "features/user/PasswordRules.java", G),
    ("NFR-07", "Bruikbaarheid", "De app werkt op mobiel (responsive).", "FE #145, #141, PR #138", G),
    ("NFR-08", "Toegankelijkheid", "Contrast en kleurgebruik voldoen aan WCAG AA en het kleurenpalet is kleurenblind-vriendelijk.", "Acceptatiecriteria van FE #160, #164, #175; niet getoetst met een tool of meting", O),
    ("NFR-09", "Consistentie", "Kaart, heatmap, wijken en dashboard tonen dezelfde warmste en koudste plek.", "FE #193, PR #196", G),
    ("NFR-10", "Laadtijd", "De frontend wordt gecomprimeerd (gzip) en gecachet, zware grafieken worden lui geladen.", "FE #192, PR #195; nginx.conf (gzip on)", G),
    ("NFR-11", "Beschikbaarheid", "De backend heeft liveness- en readinessendpoints (database en ingest) voor monitoring.", "BE #169, PR #188; docs/monitoring.md", G),
    ("NFR-12", "Uitrol", "De backend draait als Docker-container met een niet-root gebruiker en healthcheck; een testomgeving en een acceptatie- en productieomgeving volgen.", "BE #174 PR #189, #178 PR #191 (Dockerfile). BE #172 open, #173 niet gepland", D),
    ("NFR-13", "Testbaarheid", "Tests draaien automatisch bij elke wijziging (backend Maven, frontend lint en e2e).", "BE #163, PR #162, #164; .github/workflows/ci.yml; FE PR #146, #147. Dekking meten: BE #183 open, jacoco in PR #195", D),
    ("NFR-14", "Tijd", "Tijden worden in UTC verwerkt en getoond als dd-MM-yyyy HH:mm:ss.", "application.timezone=UTC; FE #193 (measurement-time.js); BE #200 (issue open, PR #204)", G),
]

# (code, naam, actoren, omschrijving, FR-codes, bron)
UC = [
    ("UC-01", "Klimaat op de kaart bekijken", ["Bezoeker"], "Een bezoeker opent de kaart, kiest een wijk, speelt de laatste 24 uur af.", "FR-01, FR-02, FR-03, FR-07, FR-08", "routes / en /wijk/:id"),
    ("UC-02", "Wijken vergelijken", ["Bezoeker"], "Wijken rangschikken en tot drie naast elkaar leggen.", "FR-05", "route /wijken"),
    ("UC-03", "Heatmap bekijken", ["Bezoeker"], "Hotspots en koele plekken zien als kleurvlak.", "FR-04", "route /heatmap"),
    ("UC-04", "Gezondheid van het meetnet bekijken", ["Bezoeker", "Beheerder"], "Zien welke stations uitvallen en hoe volledig de data is.", "FR-06, FR-24", "route /dashboard"),
    ("UC-05", "Registreren", ["Stationeigenaar"], "Met workshopcode en stationcode een account maken; het station wordt gekoppeld.", "FR-27", "POST /api/authentication/register"),
    ("UC-06", "Inloggen", ["Stationeigenaar", "Beheerder"], "Wachtwoord en e-mailcode; vanaf een vertrouwd IP zonder mailstap.", "FR-28", "login en verify"),
    ("UC-07", "Wachtwoord herstellen", ["Stationeigenaar"], "Via een e-mailcode een nieuw wachtwoord instellen.", "FR-29", "forgot-password, reset-password"),
    ("UC-08", "Eigen stations beheren", ["Stationeigenaar"], "Stations bekijken, claimen, bewerken, overdragen en als PDF downloaden.", "FR-09, FR-10, FR-11, FR-12, FR-14", "route /my/stations; /api/meetstation"),
    ("UC-09", "Gebruikers en workshopcodes beheren", ["Beheerder"], "Gebruikers zoeken, rollen wijzigen, verwijderen; workshopcodes aanmaken en verwijderen.", "FR-31, FR-32, FR-33", "route /admin; /api/users, /api/workshops"),
    ("UC-10", "Station toevoegen", ["Beheerder"], "Handmatig een station aanmaken.", "FR-13", "POST /api/meetstation/add"),
    ("UC-11", "Datadekking bekijken", ["Beheerder"], "Dekking van fijnstofdata per station en netwerkgaten.", "FR-25", "route /admin/data-coverage"),
    ("UC-12", "Metingen ophalen en opslaan", ["Meet je stad", "Systeem"], "De ingest-worker haalt metingen op en bewaart ze.", "FR-16 tot FR-20", "ingest/IngestWorker.java"),
    ("UC-13", "Uitval signaleren", ["Systeem", "Stationeigenaar"], "De uitvalcontrole markeert een station als niet actief en mailt de eigenaar.", "FR-22, FR-23", "StationMonitorService"),
]
