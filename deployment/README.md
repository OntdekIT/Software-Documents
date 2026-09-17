# Deployment — volledige stack lokaal draaien

Deze map bevat de overkoepelende `docker-compose.yml` die **alle repos samen** opstart:
frontend, backend en database. Het project bestaat uit meerdere repositories,
dus deze compose hoort bij geen enkele repo afzonderlijk en staat daarom hier in
Software-Documents.

## Verwachte mappenstructuur

De build-contexts in de compose zijn **relatief** en gaan ervan uit dat de drie
repos naast elkaar in één map staan (bijv. `OntdekIT/`):

```
OntdekIT/
├── Software-BackEnd/
├── Software-FrontEnd/
├── Software-Documents/     ← deze repo (met deployment/docker-compose.yml)
└── docker-compose.yml      ← kopie hierheen om te draaien (zie hieronder)
```

## Draaien

De compose moet draaien vanuit de **parent-map** (`OntdekIT/`), want `context:`
verwijst naar `./Software-BackEnd/...` en `./Software-FrontEnd`.

```bash
# vanuit OntdekIT/ (de map die alle repos bevat):
cp Software-Documents/deployment/docker-compose.yml ./docker-compose.yml
docker compose up -d --build
```

> Tip: in plaats van kopiëren kun je een symlink gebruiken zodat updates
> automatisch meekomen:
> `ln -sf Software-Documents/deployment/docker-compose.yml ./docker-compose.yml`

## Services

| Service       | Poort (host) | Omschrijving                              |
|---------------|--------------|-------------------------------------------|
| `frontend`    | `3000`       | React app, productie-build via nginx      |
| `backend-api` | `8082`       | Spring Boot API                           |
| `mariaDB`     | `3307`       | MariaDB, database `ontdekstation013`      |
| `mailhog`     | `8025` (UI), `1025` (SMTP) | Lokale mailserver — vangt alle uitgaande mail op |

- Frontend: <http://localhost:3000>
- Backend:  <http://localhost:8082>
- **MailHog (mail lezen): <http://localhost:8025>**
- De frontend praat met de backend via `VITE_BACKEND_API_URL=http://localhost:8082/api`
  (ingebakken tijdens de build).

## Mail lokaal ontvangen (MailHog)

De backend verstuurt mail (o.a. de login-verificatiecode) naar de `mailhog`
service in plaats van een echte SMTP-server. Alles wat verstuurd wordt is te
lezen in de MailHog web-UI op <http://localhost:8025> — er gaat dus nooit echte
mail de deur uit. MailHog spreekt plain SMTP (poort 1025, geen TLS/auth); de
backend is daarop ingesteld via `MAILSERVER_RELAY_HOST=mailhog`,
`MAILSERVER_RELAY_PORT=1025` en `SPRING_MAIL_PROPERTIES_MAIL_SMTP_STARTTLS_ENABLE=false`.

Bij inloggen (email + wachtwoord) stuurt de app een verificatiecode; open
<http://localhost:8025>, pak de code uit de mail en vul die in om de login af te
ronden.

## Beheer

```bash
docker compose up -d --build     # bouwen + starten
docker compose ps                # status
docker compose logs -f backend-api
docker compose down              # stoppen (volume db_data blijft behouden)
docker compose down -v           # stoppen + database wissen
```

## Let op

- Dit is de **productie/nginx**-variant: code-wijzigingen zijn pas zichtbaar na
  `--build`. Voor actief ontwikkelen met hot-reload gebruik je de dev-compose in
  `Software-BackEnd/ClimateChecker/docker-compose-dev.yml` (frontend op :5173).
- De standaard admin-gebruiker (seed): `admin@example.com` / `Admin123!`.
- De DB-poort is bewust `3307` (host) om niet te botsen met een lokale MySQL/MariaDB
  op 3306.
