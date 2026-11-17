# Backend API-documentatie (ClimateChecker)

Naslagwerk voor ontwikkelaars over alle HTTP-endpoints van de ClimateChecker-backend (Spring Boot).

Bron van waarheid: de code in `OntdekIT/Software-BackEnd`, branch `s3nj26_dev` (commit `e8c567b`). Alles in dit document is afgeleid uit de controllers, DTO's, services en de securityconfiguratie. Waar het gedrag uit de code niet eenduidig te halen is, staat **onduidelijk** vermeld in plaats van een aanname.

> **OpenAPI:** de backend publiceert ook een door de code gegenereerde specificatie (`/v3/api-docs`) met Swagger UI (`/swagger-ui.html`), beschikbaar met het dev- of test-profiel (Software-BackEnd #196, PR #197). Dit document is het handgeschreven naslagwerk en kan achterlopen op de code; bij verschil geldt de OpenAPI-spec.

## Inhoudsopgave

- [1. Overzicht](#1-overzicht)
  - [1.1 Basis-URL en poort](#11-basis-url-en-poort)
  - [1.2 Authenticatie en autorisatie](#12-authenticatie-en-autorisatie)
  - [1.3 Foutformaat](#13-foutformaat)
  - [1.4 Rate limiting](#14-rate-limiting)
  - [1.5 CORS](#15-cors)
  - [1.6 Datum- en tijdformaten](#16-datum--en-tijdformaten)
  - [1.7 Overzichtstabel van alle endpoints](#17-overzichtstabel-van-alle-endpoints)
- [2. Authenticatie (`/api/authentication`)](#2-authenticatie-apiauthentication)
- [3. Mijn account (`/api/my-account`)](#3-mijn-account-apimy-account)
- [4. Gebruikers (`/api/users`)](#4-gebruikers-apiusers)
- [5. Workshops (`/api/workshops`)](#5-workshops-apiworkshops)
- [6. Meetstations (`/api/Meetstation`)](#6-meetstations-apimeetstation)
- [7. Metingen (`/api/measurement`)](#7-metingen-apimeasurement)
- [8. Wijken (`/api/neighbourhood`)](#8-wijken-apineighbourhood)
- [9. Health (`/actuator/health`)](#9-health-actuatorhealth)
- [10. E2E-testendpoints (`/api/e2e`)](#10-e2e-testendpoints-apie2e)
- [11. Gedeelde responsemodellen](#11-gedeelde-responsemodellen)
- [12. Bekende onduidelijkheden en valkuilen](#12-bekende-onduidelijkheden-en-valkuilen)

---

## 1. Overzicht

### 1.1 Basis-URL en poort

| Omgeving | Basis-URL |
|---|---|
| Lokaal | `http://localhost:8082` |
| Andere omgevingen | onduidelijk (niet in de code vastgelegd, hangt af van de deployment) |

De poort komt uit `server.port=8082` in `application.properties`. Alle applicatie-endpoints beginnen met `/api/`. Er is geen versieprefix (zoals `/v1`).

Requests met een body gebruiken `Content-Type: application/json`.

### 1.2 Authenticatie en autorisatie

De API gebruikt **JWT (Bearer token)**. Sessies en cookies worden niet gebruikt; CSRF staat uit.

**Token meesturen:**

```
Authorization: Bearer <jwt>
```

**JWT-eigenschappen** (`JwtService`):

- Ondertekend met HS256, geheime sleutel uit de omgevingsvariabele `JWT_SECRET` (Base64, minimaal 256 bit).
- `sub` (subject) is het **gebruikers-id** (`userId`) als tekst.
- Geldigheid: **10 uur** na uitgifte. Een refreshmechanisme bestaat niet.
- Een ongeldig, verlopen of ontbrekend token leidt niet tot een eigen foutmelding van de filter: de request wordt dan als anoniem behandeld en geweigerd op beveiligde routes.

**Loginflow (twee stappen, tenzij het IP vertrouwd is):**

1. `POST /api/authentication/login` met e-mail en wachtwoord.
   - Is het IP-adres van de client al vertrouwd voor deze gebruiker: antwoord `{"verificationRequired": false, "token": "<jwt>"}`. Klaar.
   - Anders: er wordt een 6-cijferige code per e-mail verstuurd en het antwoord is `{"verificationRequired": true, "token": null}`.
2. `POST /api/authentication/verify` met e-mail en de 6-cijferige code. Antwoord `{"token": "<jwt>"}`. Het IP-adres wordt daarbij onthouden als vertrouwd, zodat een volgende login vanaf dat IP stap 2 overslaat.

De code is **5 minuten** geldig en kan maar een keer gebruikt worden. Per gebruiker en codetype bestaat steeds maar een actieve code (een nieuwe code vervangt de vorige).

**Registratie:** `POST /api/authentication/register` maakt het account aan en mailt een verificatiecode. Daarna volgt `verify` (stap 2 hierboven) om een token te krijgen.

**Rollen** (`UserRole`): `USER`, `ADMIN`, `SUPER_ADMIN`. Standaardrol bij registratie is `USER`. Het JWT bevat de rol niet; de rol wordt bij elke request uit de database geladen.

**Toegangsregels** (`SecurityConfiguration`, van boven naar beneden geevalueerd):

| Route | Toegang |
|---|---|
| `/actuator/health`, `/actuator/health/**` | Publiek |
| `/api/authentication/**` | Publiek |
| `/api/users/**` | `ADMIN` of `SUPER_ADMIN` |
| `/api/workshops/**` | `ADMIN` of `SUPER_ADMIN` |
| `PUT /api/Meetstation/edit/**` | Ingelogd |
| `PUT /api/Meetstation/transfer/**` | Ingelogd |
| `PUT /api/Meetstation/Claim` | Ingelogd |
| `POST /api/Meetstation/add` | Ingelogd |
| overige `/api/Meetstation/**` | Publiek |
| `/api/measurement/coverage` | `ADMIN` of `SUPER_ADMIN` |
| overige `/api/measurement/**` | Publiek |
| `/api/neighbourhood/**` | Publiek |
| `/api/e2e/**` | Publiek (maar het endpoint bestaat alleen met Spring-profiel `e2e`) |
| `/api/my-account/**` | Ingelogd |
| al het overige | Ingelogd |

Een request zonder (geldig) token op een beveiligde route, of met een te lage rol, geeft in de praktijk **403 Forbidden**. Er is geen eigen `AuthenticationEntryPoint` geconfigureerd, dus een aparte 401 komt niet uit de eigen code; de exacte body van deze afwijzing (door Spring Security, niet door `GlobalExceptionHandler`) is **onduidelijk**.

### 1.3 Foutformaat

Fouten die via de `GlobalExceptionHandler` lopen hebben dit JSON-formaat:

```json
{
  "timestamp": "2026-05-10T14:00:00.123Z",
  "error": "BAD_REQUEST",
  "statusCode": 400,
  "message": "Timestamp must be in ISO 8601 format"
}
```

| Veld | Type | Betekenis |
|---|---|---|
| `timestamp` | string | Tijdstip van de fout, ISO 8601 in UTC |
| `error` | string | Naam van de HTTP-status (`BAD_REQUEST`, `NOT_FOUND`, `CONFLICT`, `FORBIDDEN`, ...) |
| `statusCode` | number | Numerieke HTTP-status |
| `message` | string | Foutbeschrijving (taal wisselt: deels Engels, deels Nederlands) |

Mapping van exceptions naar statuscodes in de `GlobalExceptionHandler`:

| Exception | Status | Bericht |
|---|---|---|
| `NoSuchElementException` | 404 | `Resource not found` (of het bericht van de exception) |
| `NotFoundException` | 404 | Bericht van de exception, anders `Resource not found` |
| `ExistingUniqueIdentifierException` | 409 | Bericht van de exception, anders `Resource already exists` |
| `IllegalArgumentException` | 400 | Bericht van de exception, anders `Invalid argument` |
| `InvalidArgumentException` | 400 | Bericht van de exception, anders `Invalid argument` |
| `MethodArgumentNotValidException` (Bean Validation op `@Valid` body) | 400 | `<veld> <melding>`, meerdere gescheiden door `, ` |
| `ConstraintViolationException` | 400 | Bericht van de exception |
| `AccessDeniedException` | 403 | Bericht van de exception, anders `Access denied` |

**Let op, afwijkend gedrag:** veel controllers (alle in `/api/authentication`, `/api/my-account`, `/api/users`, `StationController`) vangen exceptions zelf op en geven een **platte tekst-body** terug in plaats van het JSON-formaat hierboven. Per endpoint staat hieronder wat er echt gebeurt. Exceptions die nergens worden afgehandeld (bijvoorbeeld `DateTimeParseException`) leiden tot een standaard Spring-500 met een body die niet onder onze controle valt (**onduidelijk**).

### 1.4 Rate limiting

Er zijn twee onafhankelijke limieten.

**Globaal (alle endpoints, `RateLimitingFilter`):**

- Standaard 20 requests per minuut per client (configureerbaar: `rate.limit.enabled`, `rate.limit.requests-per-minute`).
- Client = eerste IP in `X-Forwarded-For`, anders het remote adres.
- Elk antwoord bevat de headers `X-Rate-Limit-Limit` en (bij toegestane requests) `X-Rate-Limit-Remaining`.
- Bij overschrijding: status **429** met headers `X-Rate-Limit-Remaining: 0` en `X-Rate-Limit-Retry-After-Millis`, en JSON-body:

```json
{
  "timestamp": "2026-05-10T14:00:00Z",
  "error": "TOO_MANY_REQUESTS",
  "statusCode": 429,
  "message": "Rate limit exceeded. Try again in 12345 milliseconds."
}
```

**Extra op authenticatie-endpoints** (`login`, `verify`, `reset-password`, `forgot-password`): maximaal **5 pogingen per minuut** per combinatie van actie, IP en e-mailadres. Bij overschrijding: status **429** met platte tekst-body `Te veel pogingen. Probeer het over een minuut opnieuw.`. `register` heeft deze extra limiet niet.

Beide limieten zijn in-memory en gelden per applicatie-instantie.

### 1.5 CORS

Toegestane origins komen uit `cors.allowed-origins` (omgevingsvariabele `CORS_ALLOWED_ORIGINS`, standaard `http://localhost:5173,http://localhost:3000`). Toegestane methoden: `GET, POST, PUT, DELETE, PATCH, OPTIONS`. Alle headers zijn toegestaan en credentials zijn toegestaan.

### 1.6 Datum- en tijdformaten

Er worden twee formaten gebruikt, afhankelijk van het endpoint:

| Formaat | Voorbeeld | Waar |
|---|---|---|
| ISO 8601 UTC-instant | `2026-05-10T14:00:00Z` | `timestamp`, `from`, `to` queryparameters. Moet precies dit formaat zijn (met `Z`), anders 400. |
| `dd-MM-yyyy HH:mm` | `10-05-2026 14:00` | `startDate`, `endDate` queryparameters |

Het formaat `dd-MM-yyyy HH:mm` wordt geinterpreteerd in de **standaardtijdzone van de server** (`ZoneId.systemDefault()`). Welke tijdzone dat is hangt van de deployment af (**onduidelijk**; `application.timezone=UTC` staat wel in de properties, maar de controllers gebruiken `systemDefault()`).

### 1.7 Overzichtstabel van alle endpoints

| Methode | Pad | Toegang | Sectie |
|---|---|---|---|
| POST | `/api/authentication/register` | Publiek | [2.1](#21-post-apiauthenticationregister) |
| POST | `/api/authentication/login` | Publiek | [2.2](#22-post-apiauthenticationlogin) |
| POST | `/api/authentication/verify` | Publiek | [2.3](#23-post-apiauthenticationverify) |
| POST | `/api/authentication/forgot-password` | Publiek | [2.4](#24-post-apiauthenticationforgot-password) |
| POST | `/api/authentication/reset-password` | Publiek | [2.5](#25-post-apiauthenticationreset-password) |
| GET | `/api/my-account` | Ingelogd | [3.1](#31-get-apimy-account) |
| PUT | `/api/my-account` | Ingelogd | [3.2](#32-put-apimy-account) |
| GET | `/api/users` | Admin | [4.1](#41-get-apiusers) |
| GET | `/api/users/{id}` | Admin | [4.2](#42-get-apiusersid) |
| PUT | `/api/users/{id}` | Admin | [4.3](#43-put-apiusersid) |
| DELETE | `/api/users/{id}` | Admin | [4.4](#44-delete-apiusersid) |
| POST | `/api/workshops` | Admin | [5.1](#51-post-apiworkshops) |
| GET | `/api/workshops` | Admin | [5.2](#52-get-apiworkshops) |
| GET | `/api/workshops/{code}/users` | Admin | [5.3](#53-get-apiworkshopscodeusers) |
| DELETE | `/api/workshops/{code}` | Admin | [5.4](#54-delete-apiworkshopscode) |
| GET | `/api/Meetstation/{id}` | Publiek | [6.1](#61-get-apimeetstationid) |
| GET | `/api/Meetstation/stations` | Publiek | [6.2](#62-get-apimeetstationstations) |
| GET | `/api/Meetstation/stationsMetMeasurements` | Publiek | [6.3](#63-get-apimeetstationstationsmetmeasurements) |
| PUT | `/api/Meetstation/edit/{id}` | Ingelogd (eigenaar of admin) | [6.4](#64-put-apimeetstationeditid) |
| PUT | `/api/Meetstation/transfer/{id}` | Ingelogd (eigenaar of admin) | [6.5](#65-put-apimeetstationtransferid) |
| GET | `/api/Meetstation/measurements/{id}` | Publiek | [6.6](#66-get-apimeetstationmeasurementsid) |
| GET | `/api/Meetstation/Availibility/{stationId}/{workshopCode}` | Publiek | [6.7](#67-get-apimeetstationavailibilitystationidworkshopcode) |
| PUT | `/api/Meetstation/Claim` | Ingelogd | [6.8](#68-put-apimeetstationclaim) |
| POST | `/api/Meetstation/add` | Ingelogd | [6.9](#69-post-apimeetstationadd) |
| GET | `/api/measurement/history` | Publiek | [7.1](#71-get-apimeasurementhistory) |
| GET | `/api/measurement/history/average/{id}` | Publiek | [7.2](#72-get-apimeasurementhistoryaverageid) |
| GET | `/api/measurement/history/network` | Publiek | [7.3](#73-get-apimeasurementhistorynetwork) |
| GET | `/api/measurement/history/average/region/{regionId}` | Publiek | [7.4](#74-get-apimeasurementhistoryaverageregionregionid) |
| GET | `/api/measurement/history/hourly/{id}` | Publiek | [7.5](#75-get-apimeasurementhistoryhourlyid) |
| GET | `/api/measurement/history/half-hourly/{id}` | Publiek | [7.6](#76-get-apimeasurementhistoryhalf-hourlyid) |
| GET | `/api/measurement/coverage` | Admin | [7.7](#77-get-apimeasurementcoverage) |
| GET | `/api/neighbourhood/history` | Publiek | [8.1](#81-get-apineighbourhoodhistory) |
| GET | `/api/neighbourhood/history/timelapse` | Publiek | [8.2](#82-get-apineighbourhoodhistorytimelapse) |
| GET | `/api/neighbourhood/history/average/{id}` | Publiek | [8.3](#83-get-apineighbourhoodhistoryaverageid) |
| GET | `/api/neighbourhood/{id}` | Publiek | [8.4](#84-get-apineighbourhoodid) |
| GET | `/actuator/health` (+ `/liveness`, `/readiness`) | Publiek | [9](#9-health-actuatorhealth) |
| POST | `/api/e2e/reset` | Alleen profiel `e2e` | [10.1](#101-post-apie2ereset) |
| GET | `/api/e2e/users/{email}/auth-token` | Alleen profiel `e2e` | [10.2](#102-get-apie2eusersemailauth-token) |

Admin = rol `ADMIN` of `SUPER_ADMIN`.

---

## 2. Authenticatie (`/api/authentication`)

Alle endpoints in deze sectie zijn publiek. Fouten komen als platte tekst terug (zie [1.3](#13-foutformaat)). Algemeen: een onverwachte fout geeft **500** met body `Er is een onverwachte fout opgetreden.`

### 2.1 `POST /api/authentication/register`

Maakt een gebruiker aan, koppelt het station met de opgegeven stationcode aan die gebruiker en mailt een verificatiecode.

**Request body** (`RegisterUserRequest`):

| Veld | Type | Verplicht | Validatie |
|---|---|---|---|
| `firstName` | string | ja | Geen validatie in de controller (de uitkomst van `UserValidator` wordt niet gebruikt). Leeg of ontbrekend: **onduidelijk** |
| `lastName` | string | ja | Idem |
| `email` | string | ja | Moet uniek zijn. Formaatvalidatie: **onduidelijk** |
| `password` | string | ja | Geen wachtwoordeisen bij registratie (de regel "8 tekens, hoofdletter en cijfer" geldt alleen bij reset en account-update) |
| `stationCode` | number (Long) | ja | Registratiecode van een bestaand station dat nog geen eigenaar heeft |
| `workshopCode` | number (Long) | ja | Code van een niet-verlopen workshop |

**Response 201** (`UserResponse`, zonder stations):

```json
{
  "id": 12,
  "firstName": "Jan",
  "lastName": "Jansen",
  "email": "jan@example.com",
  "role": "USER",
  "stations": []
}
```

**Foutcodes:**

| Status | Body (tekst) | Oorzaak |
|---|---|---|
| 400 | `Ongeldige workshopcode` | Workshopcode onbekend of verlopen |
| 400 | `Ongeldige stationcode` | Geen station met deze registratiecode |
| 400 | `Station is al geclaimd` | Station heeft al een eigenaar |
| 400 | `Email already exists` | E-mailadres bestaat al (de catch voor `Email is al in gebruik` is een tweede pad bij een databaseconstraint) |
| 500 | `Er is een onverwachte fout opgetreden.` | Overige fouten, bijvoorbeeld mailverzending |

Bijwerking: een `VERIFY_AUTH`-code (6 cijfers) wordt gemaild. Om in te loggen moet daarna [2.3](#23-post-apiauthenticationverify) worden aangeroepen.

### 2.2 `POST /api/authentication/login`

**Request body** (`LoginRequest`):

| Veld | Type | Verplicht |
|---|---|---|
| `email` | string | ja |
| `password` | string | ja |

**Response 200** (`LoginResponse`):

| Veld | Type | Betekenis |
|---|---|---|
| `verificationRequired` | boolean | `true`: code gemaild, ga naar `verify`. `false`: direct ingelogd |
| `token` | string of null | JWT als `verificationRequired` `false` is, anders `null` |

```json
{ "verificationRequired": true, "token": null }
```

**Foutcodes:**

| Status | Body (tekst) | Oorzaak |
|---|---|---|
| 400 | `Invalid email and/or password` | Onbekend e-mailadres of fout wachtwoord |
| 429 | `Te veel pogingen. Probeer het over een minuut opnieuw.` | Meer dan 5 pogingen per minuut |
| 500 | `Er is een onverwachte fout opgetreden.` | Overige fouten |

### 2.3 `POST /api/authentication/verify`

Wisselt de gemailde code in voor een JWT en onthoudt het IP als vertrouwd.

**Request body** (`VerifyLoginRequest`):

| Veld | Type | Verplicht |
|---|---|---|
| `email` | string | ja |
| `code` | string | ja (6 cijfers, 5 minuten geldig) |

**Response 200** (`AuthenticationResponse`):

```json
{ "token": "<jwt>" }
```

**Foutcodes:**

| Status | Body | Oorzaak |
|---|---|---|
| 400 | leeg | Onbekende gebruiker, foute of verlopen code |
| 429 | `Te veel pogingen. Probeer het over een minuut opnieuw.` | Meer dan 5 pogingen per minuut |
| 500 | `Er is een onverwachte fout opgetreden.` | Overige fouten |

Een gebruikte code wordt direct verwijderd, ook als hij verlopen bleek.

### 2.4 `POST /api/authentication/forgot-password`

Stuurt een 6-cijferige resetcode per e-mail (`PASSWORD_RESET`, 5 minuten geldig).

**Request body** (`ForgotPasswordRequest`):

| Veld | Type | Verplicht |
|---|---|---|
| `email` | string | ja |

**Response 200:** lege body.

**Foutcodes:**

| Status | Body (tekst) | Oorzaak |
|---|---|---|
| 400 | `Invalid email` | Onbekend e-mailadres (let op: dit maakt het mogelijk om te achterhalen welke adressen een account hebben) |
| 429 | `Te veel pogingen. Probeer het over een minuut opnieuw.` | Meer dan 5 pogingen per minuut |
| 500 | `Er is een onverwachte fout opgetreden.` | Overige fouten |

### 2.5 `POST /api/authentication/reset-password`

Zet een nieuw wachtwoord met de code uit [2.4](#24-post-apiauthenticationforgot-password).

**Request body** (`ResetPasswordRequest`, met `@Valid`):

| Veld | Type | Verplicht | Validatie |
|---|---|---|---|
| `email` | string | ja | Niet leeg (`@NotBlank`) |
| `password` | string | ja | Niet leeg; regex `^(?=.*[A-Z])(?=.*\d).{8,}$`: minimaal 8 tekens, minstens een hoofdletter en een cijfer |
| `token` | string | ja | Niet leeg; de gemailde code |

**Response 200:** lege body.

**Foutcodes:**

| Status | Body | Oorzaak |
|---|---|---|
| 400 | JSON-foutobject (`password must be at least 8 characters long, ...`) | Bean Validation mislukt (via `GlobalExceptionHandler`) |
| 400 | `Invalid email and/or token` (tekst) | Onbekende gebruiker, foute of verlopen code |
| 429 | `Te veel pogingen. Probeer het over een minuut opnieuw.` | Meer dan 5 pogingen per minuut |
| 500 | `Er is een onverwachte fout opgetreden.` | Overige fouten |

---

## 3. Mijn account (`/api/my-account`)

Toegang: ingelogd. De gebruiker wordt bepaald uit het `sub` van het JWT.

### 3.1 `GET /api/my-account`

**Queryparameters:**

| Naam | Type | Verplicht | Standaard | Betekenis |
|---|---|---|---|---|
| `includeStations` | boolean | nee | `false` | Neem de stations van de gebruiker op in de response |

**Response 200:** `UserResponse` (zie [11.3](#113-userresponse)).

**Foutcodes:** 400 (tekst, `InvalidArgumentException`), 500 `Er is een onverwachte fout opgetreden.`. Zonder geldig token: 403.

### 3.2 `PUT /api/my-account`

Werkt voornaam, achternaam, e-mail en optioneel het wachtwoord van de ingelogde gebruiker bij. De rol kan hier niet gewijzigd worden.

**Request body** (`UpdateMyAccountRequest`, met `@Valid`):

| Veld | Type | Verplicht | Validatie |
|---|---|---|---|
| `firstName` | string | ja | Niet leeg |
| `lastName` | string | ja | Niet leeg |
| `email` | string | ja | Niet leeg (formaat en uniekheid: **onduidelijk**) |
| `password` | string | nee | Weglaten of `null` laat het wachtwoord ongewijzigd. Anders regex `^(?=.*[A-Z])(?=.*\d).{8,}$` (een lege string faalt dus op de regex) |

**Response 200:** lege body.

**Foutcodes:**

| Status | Body | Oorzaak |
|---|---|---|
| 400 | JSON-foutobject | Bean Validation mislukt |
| 400 | tekst | `InvalidArgumentException` |
| 500 | `Er is een onverwachte fout opgetreden.` | Overige fouten. Een e-mailadres dat al bij een ander account hoort leidt waarschijnlijk hiertoe (databaseconstraint), maar dat is **onduidelijk** |

---

## 4. Gebruikers (`/api/users`)

Toegang: rol `ADMIN` of `SUPER_ADMIN` voor alle endpoints. Alle fouten in deze controller zijn platte tekst: `InvalidArgumentException` geeft 400, **elke andere exception geeft 500** met `Er is een onverwachte fout opgetreden.` (ook "niet gevonden" en de rolchecks hieronder).

### 4.1 `GET /api/users`

Gepagineerde lijst van gebruikers, optioneel gefilterd.

**Queryparameters** (`GetAllUsersRequest`):

| Naam | Type | Verplicht | Standaard | Betekenis |
|---|---|---|---|---|
| `page` | integer | nee | `0` | Paginanummer, 0-gebaseerd. Negatief geeft 500 |
| `pageSize` | integer | nee | `20` | Paginagrootte, afgekapt op maximaal `100` |
| `firstName` | string | nee | - | Filter op voornaam |
| `lastName` | string | nee | - | Filter op achternaam |
| `email` | string | nee | - | Filter op e-mail |
| `role` | enum | nee | - | `USER`, `ADMIN` of `SUPER_ADMIN` |

Hoe de filters matchen (exact of gedeeltelijk) staat in de repositoryquery en is hier **onduidelijk**.

**Response 200:** Spring Data `Page<UserResponse>`. De stations in elk item zijn altijd een lege lijst. Velden van de pagina (standaard Spring-serialisatie): `content`, `pageable`, `totalElements`, `totalPages`, `size`, `number`, `first`, `last`, `numberOfElements`, `empty`, `sort`. De exacte JSON-vorm is niet in de code vastgelegd en hangt van de Spring Data-versie af.

### 4.2 `GET /api/users/{id}`

| Parameter | Waar | Type | Betekenis |
|---|---|---|---|
| `id` | pad | long | Gebruikers-id |
| `includeStations` | query | boolean, standaard `false` | Stations meesturen |

**Response 200:** `UserResponse`.

**Foutcodes:** onbekend id geeft **500** (de `NotFoundException` wordt door de eigen `catch` omgezet), niet 404. Ongeldige `id` (geen getal) geeft een standaard Spring 400 (body onduidelijk).

### 4.3 `PUT /api/users/{id}`

Wijzigt de rol van een gebruiker.

**Request body** (`UpdateUserRequest`):

| Veld | Type | Verplicht | Betekenis |
|---|---|---|---|
| `role` | enum | ja | `USER`, `ADMIN` of `SUPER_ADMIN`. Ontbrekend of ongeldig: **onduidelijk** |

**Regels:**

- Alleen een `SUPER_ADMIN` mag de rol `SUPER_ADMIN` toekennen.
- Alleen een `SUPER_ADMIN` mag de rol van een `SUPER_ADMIN` wijzigen.
- Alleen een `SUPER_ADMIN` mag een gebruiker met een speciale rol terugzetten naar `USER`.

**Response 200:** lege body.

**Foutcodes:** een overtreding van bovenstaande regels geeft **500** met `Er is een onverwachte fout opgetreden.` (de `IllegalArgumentException` wordt door de eigen `catch` opgevangen). Onbekend id: ook 500.

### 4.4 `DELETE /api/users/{id}`

Verwijdert een gebruiker.

| Parameter | Waar | Type |
|---|---|---|
| `id` | pad | long |

**Regel:** alleen een `SUPER_ADMIN` mag gebruikers met een andere rol dan `USER` verwijderen. Een `ADMIN` mag dus alleen gewone gebruikers verwijderen.

**Response 200:** lege body.

**Foutcodes:** regelovertreding of onbekend id geeft **500** met `Er is een onverwachte fout opgetreden.`. Wat er met de stations en tokens van de verwijderde gebruiker gebeurt, is **onduidelijk** (hangt af van databaseconstraints).

---

## 5. Workshops (`/api/workshops`)

Toegang: rol `ADMIN` of `SUPER_ADMIN`. Een workshop is een tijdelijke code waarmee deelnemers zich kunnen registreren. Deze controller vangt zelf geen exceptions op, dus fouten die door de `GlobalExceptionHandler` worden afgehandeld hebben het JSON-formaat uit [1.3](#13-foutformaat).

### 5.1 `POST /api/workshops`

Maakt een workshop aan met een willekeurige, unieke 6-cijferige code (tussen 100000 en 999998).

**Request body** (`WorkshopRequest`):

| Veld | Type | Verplicht | Validatie |
|---|---|---|---|
| `expirationDate` | string | ja | ISO 8601 datum-tijd (`DateTimeFormatter.ISO_DATE_TIME`), bijvoorbeeld `2026-12-01T10:00:00`. Een offset of `Z` wordt geaccepteerd maar genegeerd |

**Response 201** (`WorkshopResponse`):

```json
{
  "code": 483920,
  "expirationDate": "2026-12-01T10:00:00Z",
  "creationDate": "2026-11-17T09:15:30.123456Z"
}
```

| Veld | Type | Betekenis |
|---|---|---|
| `code` | number | Workshopcode |
| `expirationDate` | string | Verloopmoment, ISO 8601 met offset `Z` (de opgeslagen lokale tijd wordt als UTC gelabeld) |
| `creationDate` | string of null | Aanmaakmoment, ISO 8601 met offset `Z` |

**Foutcodes:** een niet te parsen `expirationDate` geeft een niet-afgehandelde `DateTimeParseException`, dus een standaard Spring **500** (geen 400).

### 5.2 `GET /api/workshops`

**Queryparameters:**

| Naam | Type | Verplicht | Standaard | Betekenis |
|---|---|---|---|---|
| `isExpired` | boolean | nee | `false` | `false`: alleen actieve (nog niet verlopen) workshops. `true`: alleen verlopen workshops |

**Response 200:** array van `WorkshopResponse`.

### 5.3 `GET /api/workshops/{code}/users`

Geeft de gebruikers die zich met deze workshopcode hebben geregistreerd.

| Parameter | Waar | Type |
|---|---|---|
| `code` | pad | long |

**Response 200:** array van `UserResponse` (zonder stations). Gedrag bij een onbekende code: **onduidelijk** (de service zoekt dan met `null` als workshop).

### 5.4 `DELETE /api/workshops/{code}`

| Parameter | Waar | Type |
|---|---|---|
| `code` | pad | long |

**Response 204:** lege body.

**Foutcodes:** onbekende code leidt tot een `delete(null)` op de repository. Dat geeft waarschijnlijk een `IllegalArgumentException` en dus 400 via de `GlobalExceptionHandler`, maar het bericht is **onduidelijk**. Wat er gebeurt met gebruikers die aan deze workshop gekoppeld zijn, is ook **onduidelijk**.

---

## 6. Meetstations (`/api/Meetstation`)

Let op de hoofdletter `M` in het pad en de scheiding tussen `Meetstation` (pad) en `station` (model). Deze controller heeft `@CrossOrigin` voor `http://localhost:5173` naast de algemene CORS-configuratie.

Foutafhandeling is per endpoint verschillend; zie de tabellen hieronder.

### 6.1 `GET /api/Meetstation/{id}`

Toegang: publiek.

| Parameter | Waar | Type |
|---|---|---|
| `id` | pad | long |

**Response 200:** `StationDto` (zie [11.1](#111-stationdto)), zonder `measurements`, `latitude` en `longitude` (die zijn `null` respectievelijk `0`).

**Foutcodes:** 404 met lege body bij `id` gelijk aan `0`, onbekend station, of een interne fout.

### 6.2 `GET /api/Meetstation/stations`

Toegang: publiek. Lijst van stations met optionele filters.

**Queryparameters** (`GetAllStationsRequest`):

| Naam | Type | Verplicht | Standaard | Werkt echt |
|---|---|---|---|---|
| `page` | integer | nee | `0` | Nee: wordt geaccepteerd maar niet gebruikt, er is geen paginering |
| `pageSize` | integer | nee | `20` | Nee: idem |
| `name` | string | nee | - | Ja |
| `database_tag` | string | nee | - | Ja |
| `isPublic` | boolean | nee | - | Ja |
| `registrationCode` | long | nee | - | Ja |
| `userid` | long | nee | - | Nee: wordt niet doorgegeven aan het filter |
| `username` | string | nee | - | Ja: zoekt gebruikers op volledige naam en filtert op hun stations. Geen gebruikers gevonden geeft een lege lijst |
| `isActive` | boolean | nee | - | Ja |

Hoe tekstfilters matchen (exact of deels) staat in de repositoryquery: **onduidelijk**.

**Response 200:** array van `StationDto` (zonder metingen en coordinaten).

**Foutcodes:** 400 met tekstbericht (`InvalidArgumentException`), 500 met `Er is een onverwachte fout opgetreden.`

### 6.3 `GET /api/Meetstation/stationsMetMeasurements`

Toegang: publiek. Alle stations uit de database, aangevuld met de metingen rond het gegeven tijdstip. Stations die wel in de meetdata voorkomen maar niet in de database worden toegevoegd met `database_tag` `Unknown`.

| Naam | Waar | Type | Verplicht | Betekenis |
|---|---|---|---|---|
| `timestamp` | query | string | ja | ISO 8601 UTC, bijvoorbeeld `2026-05-10T14:00:00Z` |

**Response 200:** array van `StationDto`, met `measurements` (array van `MeasurementDto`, zie [11.2](#112-measurementdto)) en `latitude`/`longitude` gevuld.

**Foutcodes:** 400 met lege body bij een ongeldige `timestamp`; 500 met lege body als het asynchroon ophalen faalt.

### 6.4 `PUT /api/Meetstation/edit/{id}`

Toegang: ingelogd, en de gebruiker moet eigenaar van het station zijn of `ADMIN`/`SUPER_ADMIN`.

| Parameter | Waar | Type |
|---|---|---|
| `id` | pad | long |

**Request body** (`UpdateStationRequest`):

| Veld | Type | Verplicht | Gedrag |
|---|---|---|---|
| `name` | string | nee | Alleen toegepast als het niet `null` en niet leeg is. De annotatie `@NotBlank` wordt niet afgedwongen omdat `@Valid` ontbreekt |
| `is_public` | boolean | ja (in de praktijk) | Wordt altijd overgenomen; bij weglaten is het resultaat **onduidelijk** (`null` wordt doorgezet) |

**Response 200:** body is de tekst `OK`.

**Foutcodes** (JSON-foutobject via `GlobalExceptionHandler`):

| Status | Oorzaak |
|---|---|
| 403 | `You are not allowed to edit this station` (niet eigenaar en geen admin) |
| 404 | Station bestaat niet (bericht is `User not found`, een misleidende tekst in de code) |
| 403 | Geen of ongeldig token |

### 6.5 `PUT /api/Meetstation/transfer/{id}`

Toegang: ingelogd, eigenaar van het station of `ADMIN`/`SUPER_ADMIN`. Draagt het station over aan een andere gebruiker; de meethistorie blijft behouden.

| Parameter | Waar | Type |
|---|---|---|
| `id` | pad | long |

**Request body** (`TransferStationRequest`, met `@Valid`):

| Veld | Type | Verplicht | Validatie |
|---|---|---|---|
| `newOwnerEmail` | string | ja | Niet leeg en geldig e-mailadres |

**Response 200:** body is de tekst `OK`.

**Foutcodes** (JSON-foutobject):

| Status | Oorzaak |
|---|---|
| 400 | Validatie mislukt |
| 403 | `You are not allowed to transfer this station` |
| 404 | Station niet gevonden (`User not found`), of `Gebruiker met dit e-mailadres bestaat niet` |

### 6.6 `GET /api/Meetstation/measurements/{id}`

Toegang: publiek. Geeft de metingen van een station in een periode als **PDF-download**.

| Naam | Waar | Type | Verplicht | Betekenis |
|---|---|---|---|---|
| `id` | pad | integer | ja | Station-id |
| `startDate` | query | string | ja | `dd-MM-yyyy HH:mm` |
| `endDate` | query | string | ja | `dd-MM-yyyy HH:mm` |

**Response 200:** binaire PDF. Headers: `Content-Type: application/pdf`, `Content-Disposition: form-data; name="attachment"; filename="measurements.pdf"`, `Content-Length`.

**Foutcodes:**

| Status | Oorzaak |
|---|---|
| 400 (JSON-foutobject) | `Start date is after end date` |
| 500 | Ongeldig datumformaat (niet-afgehandelde `DateTimeParseException`, body onduidelijk) |

### 6.7 `GET /api/Meetstation/Availibility/{stationId}/{workshopCode}`

Toegang: publiek. Controleert of een station geclaimd kan worden met een workshopcode. Let op de schrijfwijze `Availibility` in het pad.

| Parameter | Waar | Type |
|---|---|---|
| `stationId` | pad | long |
| `workshopCode` | pad | long |

**Response:** altijd HTTP 200 met als body een **getal** dat de uitkomst aangeeft:

| Body | Betekenis |
|---|---|
| `200` | Station is vrij en de workshopcode is geldig |
| `402` | Station bestaat niet of is al geclaimd |
| `403` | Station is vrij maar de workshopcode is ongeldig of verlopen |

**Foutcodes:** 400 met lege body bij een onverwachte fout.

### 6.8 `PUT /api/Meetstation/Claim`

Toegang: ingelogd. Claimt een station voor de ingelogde gebruiker. Het `userid` uit de body wordt genegeerd en vervangen door de ingelogde gebruiker.

**Request body:** `StationDto` (zie [11.1](#111-stationdto)). Relevante velden:

| Veld | Type | Gedrag |
|---|---|---|
| `stationid` | number | Verplicht: het station dat geclaimd wordt |
| `name` | string | Wordt op het station gezet |
| `database_tag` | string | Wordt op het station gezet |
| `is_public` | boolean | Wordt op het station gezet |
| `userid` | number | Genegeerd, wordt de ingelogde gebruiker |

Alle overige velden worden genegeerd. De service zet daarnaast `registrationCode` van het station op de waarde van `stationid` (zie [12](#12-bekende-onduidelijkheden-en-valkuilen)).

**Response 200:** lege body.

**Foutcodes:** 400 met tekstbericht van de exception (bij een onbekend `stationid` is de melding mogelijk leeg, **onduidelijk**). Er wordt niet gecontroleerd of het station al een eigenaar heeft: een ingelogde gebruiker kan dus een al geclaimd station overnemen (zie [12](#12-bekende-onduidelijkheden-en-valkuilen)).

### 6.9 `POST /api/Meetstation/add`

Toegang: ingelogd (elke rol). Voegt een station toe met `database_tag` `MJS`, `is_public` `false` en `isActive` `false`.

**Request body:** `Station`-entiteit; gebruikte velden:

| Veld | Type | Betekenis |
|---|---|---|
| `name` | string | Naam |
| `registrationCode` | number | Unieke registratiecode |
| `location_locationid` | number | Verwijzing naar een locatie |

Andere velden worden genegeerd. Het `stationid` wordt niet door de controller gezet; hoe het gegenereerd wordt, is **onduidelijk**.

**Response 201:** het opgeslagen `Station` (JSON-vorm van de entiteit: `stationid`, `name`, `database_tag`, `is_public`, `registrationCode`, `location_locationid`, `userid`, `isActive`, `tempError`, `humError`, `stofError`, `locError`, `user`, `measurementList`; de exacte serialisatie is **onduidelijk**).

**Foutcodes:**

| Status | Body (tekst) | Oorzaak |
|---|---|---|
| 400 | `Registratiecode is al in gebruik!` | Databaseconstraint op `registrationCode` |
| 500 | `Er is een fout opgetreden bij het toevoegen van het meetstation.` | Overige fouten |

---

## 7. Metingen (`/api/measurement`)

Toegang: publiek, behalve `coverage` (admin). Bevat alleen stations in de gemeente Tilburg. Fouten van type `InvalidArgumentException` hebben het JSON-formaat uit [1.3](#13-foutformaat).

### 7.1 `GET /api/measurement/history`

Per station de meting die het dichtst bij het gegeven tijdstip ligt. Alleen metingen binnen een aantal minuten (`MeetJeStadService.getMinuteLimit()`, waarde **onduidelijk**) komen mee.

| Naam | Waar | Type | Verplicht | Betekenis |
|---|---|---|---|---|
| `timestamp` | query | string | ja | ISO 8601 UTC, bijvoorbeeld `2026-05-10T14:00:00Z` |

**Response 200:** array van `MeasurementDto` (zie [11.2](#112-measurementdto)). `is_public` en `userId` worden aangevuld uit het station; voor onbekende stations is `is_public` `true`.

**Foutcodes:** 400 `Timestamp must be in ISO 8601 format`.

### 7.2 `GET /api/measurement/history/average/{id}`

Per dag de gemiddelde, minimale en maximale waarden van een station.

| Naam | Waar | Type | Verplicht | Betekenis |
|---|---|---|---|---|
| `id` | pad | integer | ja | Station-id |
| `startDate` | query | string | ja | `dd-MM-yyyy HH:mm` |
| `endDate` | query | string | ja | `dd-MM-yyyy HH:mm` |

**Response 200:** array van `DayMeasurementResponse` (zie [11.4](#114-daymeasurementresponse)), chronologisch.

**Foutcodes:** 400 `Start date is after end date`. Een ongeldig datumformaat wordt doorgegooid als niet-afgehandelde `DateTimeParseException`: standaard Spring **500** (geen 400).

### 7.3 `GET /api/measurement/history/network`

Per dag de netwerkbrede temperatuurstatistiek over alle stations samen. Gebruikt dezelfde dagbuckets als [7.2](#72-get-apimeasurementhistoryaverageid).

| Naam | Waar | Type | Verplicht | Betekenis |
|---|---|---|---|---|
| `startDate` | query | string | ja | `dd-MM-yyyy HH:mm` |
| `endDate` | query | string | ja | `dd-MM-yyyy HH:mm` |

**Response 200:** array van `NetworkMeasurementResponse`:

| Veld | Type | Betekenis |
|---|---|---|
| `timestamp` | string | Dag, formaat `dd-MM` |
| `minTemp` | number of null | Laagste gemeten temperatuur in het netwerk |
| `maxTemp` | number of null | Hoogste gemeten temperatuur |
| `medianTemp` | number of null | Mediaan over alle metingen (niet over stationsgemiddelden) |
| `avgTemp` | number of null | Gemiddelde over alle metingen |
| `stationCount` | integer | Aantal unieke stations in deze bucket |
| `measurementCount` | integer | Aantal metingen waarop de statistiek is gebaseerd |

**Foutcodes:** 400 `Dates must be in dd-MM-yyyy HH:mm format`, 400 `Start date is after end date`.

### 7.4 `GET /api/measurement/history/average/region/{regionId}`

Geaggregeerde temperatuur (min/max/gemiddelde/mediaan) en fijnstof van alle stations binnen een wijk, per tijdsbucket.

| Naam | Waar | Type | Verplicht | Standaard | Betekenis |
|---|---|---|---|---|---|
| `regionId` | pad | long | ja | - | Wijk-id (zie [8](#8-wijken-apineighbourhood)) |
| `from` | query | string | nee | 24 uur voor `to` | ISO 8601 UTC |
| `to` | query | string | nee | nu | ISO 8601 UTC |
| `granularity` | query | string | nee | `hour` | `half-hour`, `hour` of `day` (hoofdletterongevoelig). Een andere waarde valt stilzwijgend terug op `hour` |

**Response 200:** array van `RegionAverageBucketResponse`:

| Veld | Type | Betekenis |
|---|---|---|
| `timestamp` | string | Start van de bucket, formaat `yyyy-MM-dd'T'HH:mm:ss` (zonder tijdzone, in de servertijdzone) |
| `min` | number | Minimale temperatuur |
| `max` | number | Maximale temperatuur |
| `avg` | number | Gemiddelde temperatuur |
| `median` | number of null | Mediaan temperatuur |
| `pm25` | number of null | Fijnstof PM2.5 (aggregatie: **onduidelijk**, vermoedelijk gemiddelde) |
| `pm10` | number of null | Fijnstof PM10 (idem) |

Is er geen enkel station in de wijk of geen data, dan is het antwoord een lege array.

**Foutcodes:** 400 `Date must be in ISO 8601 format (e.g. 2025-05-10T14:00:00Z)`, 400 `'from' must not be after 'to'`, 404 `Region not found: <id>`.

### 7.5 `GET /api/measurement/history/hourly/{id}`

Uurgemiddelden (temperatuur en PM2.5) van een station voor de huidige dag, van 00:00 tot nu.

| Naam | Waar | Type |
|---|---|---|
| `id` | pad | integer (station-id) |

**Response 200:** array van `HourMeasurementResponse`:

| Veld | Type | Betekenis |
|---|---|---|
| `timestamp` | string | Uur, formaat `HH:mm` |
| `avgTemp` | number | Gemiddelde temperatuur |
| `avgPm25` | number | Gemiddelde PM2.5 |

Dag en tijd zijn in de standaardtijdzone van de server.

### 7.6 `GET /api/measurement/history/half-hourly/{id}`

Zelfde als [7.5](#75-get-apimeasurementhistoryhourlyid), maar per half uur.

**Response 200:** array van `HalfHourMeasurementResponse` met dezelfde velden als hierboven (`timestamp` `HH:mm`, `avgTemp`, `avgPm25`), bucketgrens op `:00` en `:30`.

### 7.7 `GET /api/measurement/coverage`

Toegang: `ADMIN` of `SUPER_ADMIN`. Laat per station en voor het hele netwerk zien hoe compleet de fijnstofdata is, zodat ontbrekende of onregelmatige data opvalt. Resultaten worden 15 minuten gecachet (maximaal 16 combinaties).

| Naam | Waar | Type | Verplicht | Standaard | Betekenis |
|---|---|---|---|---|---|
| `from` | query | string | nee | 7 dagen voor `to` | ISO 8601 UTC |
| `to` | query | string | nee | begin van het huidige uur | ISO 8601 UTC, exclusief |
| `granularity` | query | string | nee | `hour` | `hour` of `day` (hoofdletterongevoelig) |

**Beperkingen:** `from` moet voor `to` liggen en de periode (na uitlijnen van `from` op de bucketgrens) mag maximaal 31 dagen zijn. Buckets worden uitgelijnd in de tijdzone `Europe/Amsterdam`.

**Response 200:** `DataCoverageResponse` (zie [11.5](#115-datacoverageresponse)).

**Foutcodes:** 400 `Granularity must be 'hour' or 'day'`, 400 `'from' must be before 'to'`, 400 `The period can be at most 31 days`, 400 `Date must be in ISO 8601 format (e.g. 2025-05-10T14:00:00Z)`, 403 zonder adminrol.

---

## 8. Wijken (`/api/neighbourhood`)

Toegang: publiek. Alleen wijken in de gemeente Tilburg.

### 8.1 `GET /api/neighbourhood/history`

Alle wijken met hun gemiddelde temperatuur en PM2.5 rond een tijdstip.

| Naam | Waar | Type | Verplicht | Betekenis |
|---|---|---|---|---|
| `timestamp` | query | string | ja | ISO 8601 UTC |

**Response 200:** array van `NeighbourhoodDto`:

| Veld | Type | Betekenis |
|---|---|---|
| `id` | number | Wijk-id |
| `name` | string | Wijknaam |
| `coordinates` | array van `[latitude, longitude]` | Polygoon van de wijkgrens, `float[y][x]` |
| `avgTemp` | number | Gemiddelde temperatuur |
| `avgPm25` | number of null | Gemiddelde PM2.5 |

**Foutcodes:** 400 `Timestamp must be in ISO 8601 format`.

### 8.2 `GET /api/neighbourhood/history/timelapse`

Een tijdreeks voor het afspelen van de heatmap: per tijdstap de gemiddelde temperatuur en PM2.5 per wijk, in een antwoord. De wijkgrenzen staan eenmalig in het antwoord.

| Naam | Waar | Type | Verplicht | Standaard | Betekenis |
|---|---|---|---|---|---|
| `from` | query | string | nee | 24 uur voor `to` | ISO 8601 UTC, tijdstip van de eerste stap |
| `to` | query | string | nee | nu | ISO 8601 UTC, tijdstip van de laatste stap |
| `steps` | query | integer | nee | `24` | Aantal stappen inclusief begin en eind, tussen `2` en `48` |

**Response 200** (`NeighbourhoodTimelapseResponse`):

```json
{
  "neighbourhoods": [
    { "id": 1, "name": "Centrum", "coordinates": [[51.55, 5.08], [51.56, 5.09]] }
  ],
  "frames": [
    {
      "timestamp": "2026-05-10T14:00:00Z",
      "stationCount": 14,
      "values": [ { "id": 1, "avgTemp": 17.4, "avgPm25": 6.1 } ]
    }
  ]
}
```

| Veld | Type | Betekenis |
|---|---|---|
| `neighbourhoods[].id` / `name` / `coordinates` | zie 8.1 | Wijken met grenzen, eenmalig |
| `frames[].timestamp` | string | Tijdstip van de stap (ISO 8601; exacte notatie **onduidelijk**) |
| `frames[].stationCount` | integer | Aantal stations met een bruikbare meting in deze stap |
| `frames[].values[].id` | number | Wijk-id |
| `frames[].values[].avgTemp` | number of null | `null` als de wijk in deze stap geen meting had |
| `frames[].values[].avgPm25` | number of null | Idem |

**Foutcodes:** 400 `steps must be between 2 and 48`, 400 `'from' must be before 'to'`, 400 `Date must be in ISO 8601 format (e.g. 2026-05-10T14:00:00Z)`.

### 8.3 `GET /api/neighbourhood/history/average/{id}`

Per dag de gemiddelde, minimale en maximale waarden voor een wijk.

| Naam | Waar | Type | Verplicht | Betekenis |
|---|---|---|---|---|
| `id` | pad | long | ja | Wijk-id |
| `startDate` | query | string | ja | `dd-MM-yyyy HH:mm` |
| `endDate` | query | string | ja | `dd-MM-yyyy HH:mm` |

**Response 200:** array van `DayMeasurementResponse` (zie [11.4](#114-daymeasurementresponse)). Een onbekende wijk, of een wijk zonder stations in de periode, geeft een **lege array** (geen 404). Er wordt niet gecontroleerd of `startDate` voor `endDate` ligt.

**Foutcodes:** 400 `Date must be in format dd-MM-yyyy HH:mm`.

### 8.4 `GET /api/neighbourhood/{id}`

Een wijk met grenzen (zonder meetwaarden).

| Parameter | Waar | Type |
|---|---|---|
| `id` | pad | long |

**Response 200:** `NeighbourhoodDto` (zie 8.1). In dit endpoint is `avgTemp` altijd de waarde `NaN`, en `avgPm25` is `null`. Hoe `NaN` in JSON verschijnt (standaard Jackson schrijft dit als de string `"NaN"`) is niet expliciet geconfigureerd.

**Foutcodes:** 404 `Neighbourhood not found`.

---

## 9. Health (`/actuator/health`)

Publiek, geen authenticatie. Alleen het health-endpoint van Spring Actuator is beschikbaar (`management.endpoints.web.exposure.include=health`). Details en componenten worden nooit getoond.

| Pad | Betekenis |
|---|---|
| `GET /actuator/health` | Algemene status, bijvoorbeeld `{"status":"UP"}` |
| `GET /actuator/health/liveness` | Het proces leeft (zonder database) |
| `GET /actuator/health/readiness` | Klaar voor verkeer (inclusief database) |

---

## 10. E2E-testendpoints (`/api/e2e`)

Deze controller bestaat **alleen** wanneer het Spring-profiel `e2e` actief is. De route is in de securityconfiguratie publiek. Gebruik dit nooit in productie.

### 10.1 `POST /api/e2e/reset`

Bedoeld om de database te resetten. **Niet geimplementeerd:** gooit `UnsupportedOperationException("Not implemented yet")`, wat een standaard Spring 500 geeft.

### 10.2 `GET /api/e2e/users/{email}/auth-token`

Geeft de actieve verificatiecode (`VERIFY_AUTH`) voor een gebruiker, zodat E2E-tests kunnen inloggen zonder e-mail. Maakt een code aan als er nog geen geldige is.

| Parameter | Waar | Type |
|---|---|---|
| `email` | pad | string |

**Response 200:** een `Token`-entiteit:

| Veld | Type | Betekenis |
|---|---|---|
| `id` | number | Gelijk aan `userId` |
| `userId` | number | Gebruikers-id |
| `tokenType` | string | `VERIFY_AUTH` |
| `numericCode` | string | De 6-cijferige code om in te leveren bij `verify` |
| `creationTime` | string | Aanmaakmoment (formaat **onduidelijk**) |

**Foutcodes:** een onbekend e-mailadres geeft waarschijnlijk een `NullPointerException` (de service geeft `null` terug) en dus een standaard Spring 500. Dat is **onduidelijk**.

---

## 11. Gedeelde responsemodellen

### 11.1 `StationDto`

| Veld | Type | Betekenis |
|---|---|---|
| `stationid` | number | Station-id |
| `name` | string of null | Naam |
| `database_tag` | string | Databron, bijvoorbeeld `MJS` (Meet je Stad) |
| `is_public` | boolean | Is het station openbaar |
| `registrationCode` | number | Registratiecode |
| `location_locationid` | number | Verwijzing naar locatie |
| `latitude` | number | Breedtegraad (alleen gevuld bij `stationsMetMeasurements`, anders `0`) |
| `longitude` | number | Lengtegraad (idem) |
| `userid` | number of null | Eigenaar |
| `isActive` | boolean | Status van het station |
| `measurements` | array van `MeasurementDto` of null | Alleen gevuld bij `stationsMetMeasurements` |
| `tempError` | boolean of null | Fout in temperatuursensor |
| `humError` | boolean of null | Fout in luchtvochtigheidssensor |
| `stofError` | boolean of null | Fout in fijnstofsensor |
| `locError` | boolean of null | Fout in locatiegegevens |

### 11.2 `MeasurementDto`

| Veld | Type | Betekenis |
|---|---|---|
| `measurementId` | number of null | Intern meting-id (geen `@JsonProperty`, standaardnaam) |
| `id` | integer | Station-id |
| `timestamp` | string | Tijdstip van de meting (exacte notatie **onduidelijk**) |
| `latitude` | number | Breedtegraad |
| `longitude` | number | Lengtegraad |
| `temperature` | number of null | Graden Celsius |
| `humidity` | number of null | Luchtvochtigheid in procenten |
| `pm2.5` | number of null | Fijnstof PM2.5 (let op de punt in de veldnaam) |
| `pm10` | number of null | Fijnstof PM10 |
| `is_public` | boolean of null | Is het station openbaar (aangevuld door `/api/measurement/history`) |
| `userId` | number of null | Eigenaar van het station (idem) |

Meetwaarden buiten plausibele grenzen worden door de server op `null` gezet (standaard: luchtvochtigheid 0 tot 100, PM2.5 en PM10 0 tot 1000; instelbaar via `MEASUREMENT_*`-omgevingsvariabelen).

### 11.3 `UserResponse`

| Veld | Type | Betekenis |
|---|---|---|
| `id` | number | Gebruikers-id |
| `firstName` | string | Voornaam |
| `lastName` | string | Achternaam |
| `email` | string | E-mailadres |
| `role` | string | `USER`, `ADMIN` of `SUPER_ADMIN` |
| `stations` | array van `StationDto` | Leeg tenzij `includeStations=true` is meegegeven (waar ondersteund) |

Het wachtwoord zit nooit in een response.

### 11.4 `DayMeasurementResponse`

| Veld | Type | Betekenis |
|---|---|---|
| `timestamp` | string | Dag, formaat `dd-MM` |
| `avgTemp` | number | Gemiddelde temperatuur |
| `minTemp` | number | Minimale temperatuur |
| `maxTemp` | number | Maximale temperatuur |
| `avgHum` | number | Gemiddelde luchtvochtigheid |
| `minHum` | number | Minimale luchtvochtigheid |
| `maxHum` | number | Maximale luchtvochtigheid |
| `avgStof` | number | Gemiddelde fijnstof (welke grootheid, PM2.5 of PM10: **onduidelijk**) |

### 11.5 `DataCoverageResponse`

| Veld | Type | Betekenis |
|---|---|---|
| `from` | string | ISO 8601, begin van de eerste bucket |
| `to` | string | ISO 8601, exclusief |
| `granularity` | string | `hour` of `day` |
| `okThreshold` | number | Drempel voor status `OK`: `0.8` |
| `networkGapThreshold` | number | Drempel voor een netwerkgat: `0.5` |
| `buckets` | array van string | ISO 8601 begin van elke bucket |
| `stationCount` | integer | Aantal stations |
| `pmCapableStationCount` | integer | Aantal stations dat fijnstof kan meten |
| `networkPmCoverage` | number of null | 0 tot 1; `null` als geen enkel station fijnstofdata stuurde |
| `networkTimeline` | array van number | Per bucket het aandeel fijnstofstations dat data leverde |
| `networkGaps` | array van object | Perioden waarin de meeste stations tegelijk data misten |
| `networkGaps[].start` | string | ISO 8601 |
| `networkGaps[].end` | string | ISO 8601, exclusief |
| `networkGaps[].bucketCount` | integer | Aantal buckets in het gat |
| `networkGaps[].lowestShare` | number | Laagste aandeel dat data leverde binnen het gat |
| `stations` | array van object | Dekking per station |
| `stations[].stationId` | number | Station-id |
| `stations[].name` | string | Naam |
| `stations[].active` | boolean | Actief |
| `stations[].stofError` | boolean | Fijnstoffout |
| `stations[].totalReadings` | integer | Aantal metingen |
| `stations[].pmReadings` | integer | Aantal metingen met fijnstof |
| `stations[].bucketsWithData` | integer | Buckets met een meting |
| `stations[].bucketsWithPm` | integer | Buckets met een fijnstofmeting |
| `stations[].dataCoverage` | number | 0 tot 1, elke meting |
| `stations[].pmCoverage` | number | 0 tot 1, metingen met PM2.5 of PM10 |
| `stations[].longestPmGapBuckets` | integer | Langste reeks buckets zonder fijnstof |
| `stations[].medianPmIntervalMinutes` | number of null | Mediaan interval tussen fijnstofmetingen in minuten |
| `stations[].status` | string | `OK`, `IRREGULAR`, `NO_PM` of `NO_DATA` |
| `stations[].pmTimeline` | array van integer | Aantal fijnstofmetingen per bucket |

---

## 12. Bekende onduidelijkheden en valkuilen

Gedrag dat bij het uitschrijven van deze documentatie opviel en dat ontwikkelaars moeten weten. Dit zijn waarnemingen over de code zoals die nu is, geen wijzigingsvoorstellen die al zijn doorgevoerd.

**Foutafhandeling**

- Veel controllers geven tekst in plaats van het JSON-foutobject (zie [1.3](#13-foutformaat)); de frontend moet beide vormen aankunnen.
- In `/api/users` geeft "niet gevonden" en een geweigerde rolwijziging beide **500** in plaats van 404 of 403, doordat een brede `catch (Exception)` de exceptions opvangt.
- Een ongeldig datumformaat in `startDate`/`endDate` geeft bij `/api/measurement/history/average/{id}`, `/api/Meetstation/measurements/{id}` en `POST /api/workshops` een standaard 500 in plaats van 400.
- Een afgewezen request door Spring Security (geen token, te lage rol) geeft 403; een 401 bestaat niet.

**Beveiliging en datakwaliteit**

- `PUT /api/Meetstation/Claim` controleert niet of het station al een eigenaar heeft en zet `registrationCode` gelijk aan `stationid`. Een ingelogde gebruiker kan zo een geclaimd station overnemen en de registratiecode overschrijven.
- `POST /api/Meetstation/add` is voor elke ingelogde gebruiker toegankelijk, niet alleen voor admins.
- `POST /api/authentication/forgot-password` geeft 400 `Invalid email` bij een onbekend adres, waardoor bestaande accounts te achterhalen zijn.
- `POST /api/authentication/register` valideert het wachtwoord niet, terwijl reset en account-update dat wel doen.
- `X-Forwarded-For` wordt blind vertrouwd voor zowel de rate limiting als het "vertrouwde IP"-mechanisme. Zonder een reverse proxy die deze header overschrijft kan een client zijn IP vervalsen.
- De rate limiters zijn in-memory en dus per instantie; bij meerdere instanties zijn de limieten ruimer dan ingesteld.
- Productie vereist `JWT_SECRET` en `TRUSTED_IP_PEPPER`; de standaardwaarden in `application.properties` zijn alleen voor lokaal gebruik.

**Inconsistenties**

- Padschrijfwijze: `/api/Meetstation/...` (hoofdletter) naast `/api/measurement/...` en `/api/neighbourhood/...` (kleine letters), en `Availibility` (typfout).
- `page`, `pageSize` en `userid` bij `GET /api/Meetstation/stations` worden geaccepteerd maar hebben geen effect.
- `GET /api/neighbourhood/{id}` geeft `avgTemp` altijd als `NaN`.
- Tijdzones zijn gemengd: de `dd-MM-yyyy HH:mm`-endpoints en `hourly`/`half-hourly` gebruiken de servertijdzone, `coverage` gebruikt `Europe/Amsterdam`, `timestamp`/`from`/`to` zijn UTC.
- De Postman-map in de backendrepo bevat alleen een lege "New Collection" en dekt geen endpoints; deze documentatie is daarom uit de code afgeleid.
