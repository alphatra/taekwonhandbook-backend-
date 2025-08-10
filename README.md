# ITF Taekwon‑Do Handbook — Backend Dev

## Szybki start (dev)
1. Zainstaluj zależności: `rye sync`
2. Skonfiguruj środowisko: skopiuj `.env.example` → `.env` i dostosuj.
3. Uruchom usługi: `docker compose up -d` (Postgres, Redis, MinIO, Meilisearch)
4. Migracje: `rye run python backend/manage.py migrate`
5. Uruchom serwer: `rye run python backend/manage.py runserver`
6. API docs: `http://127.0.0.1:8000/api/docs` (Swagger), schema: `/api/schema`
   
Public Docs (Pages): https://alphatra.github.io/taekwonhandbook-backend-/
Prywatny ZIP (Actions → Build & Deploy Docs → Artifacts): `private-docs`

## Usługi
- Postgres: `localhost:5432` (u: tkh, p: tkhpass, db: taekwonhandbook)
- Redis: `localhost:6379`
- MinIO: `http://localhost:9000` (console: `http://localhost:9001`)
- Meilisearch: `http://localhost:7700`

## Moduły backendu
- Auth (JWT), Lexicon (`techniques`), Patterns (`tuls`), Progress, Media (upload/complete), Search, Quizzes.

## Produkcja (ENV + uruchomienie)
- Kluczowe ENV (prod):
  - Django: `DJANGO_DEBUG=0`, `DJANGO_ALLOWED_HOSTS=api.example.com`, `CSRF_TRUSTED_ORIGINS=https://api.example.com`, `DJANGO_SECRET_KEY=<strong-secret>`
  - Security: `SECURE_SSL_REDIRECT=1`, `SECURE_HSTS_SECONDS=31536000`, `CDN_ORIGIN=https://cdn.example.com`
  - DB: `DB_ENGINE=django.db.backends.postgresql`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
  - Redis: `REDIS_URL=redis://redis:6379/0`
  - Storage: `S3_ENDPOINT_URL`, `S3_BUCKET`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`
  - Search: `MEILISEARCH_URL`, `MEILISEARCH_API_KEY`
  - Sentry: `SENTRY_DSN` (opcjonalnie), `SENTRY_TRACES_SAMPLE_RATE`, `SENTRY_PROFILES_SAMPLE_RATE`
  - CSP: `CSP_CONNECT_EXTRA` (np. `https://sentry.io`)

- Build + run:
  - `docker compose -f docker-compose.prod.yml build`
  - `docker compose -f docker-compose.prod.yml up -d`
  - Logs: `docker compose -f docker-compose.prod.yml logs -f nginx` (JSON access), `... logs -f web`

- OpenAPI eksport: `./scripts/export_openapi.sh` → plik `openapi.json`

## Rate limits (DRF)
- DEV (domyślne): `anon=200/min`, `user=2000/min`, media=30/min, search=90/min, quizzes=90/min, progress=180/min, billing=90/min, ads=90/min
- PROD (domyślne): `anon=60/min`, `user=600/min`, media=10/min, search=30/min, quizzes=30/min, progress=60/min, billing=30/min, ads=30/min
- Nadpisywanie: przez zmienne `DRF_THROTTLE_*`

## Admin dashboard
- Wykresy: Media (statusy), Content (techniques/tuls), Billing (plany/subskrypcje), Uploads 30d, Subscriptions 30d
- Szybkie linki: Media (failed/processing), Techniques/Tuls, Subscriptions (active), Plans, Clubs

## Health i Celery (dev)
- Health endpoint: `GET /health/` zwraca `{"status":"ok|degraded","db":...,"redis":...,"meilisearch":...}`
- Usługi pomocnicze (dev):
  - `docker compose up -d postgres redis minio meilisearch celery-beat celery-worker`
  - logi: `docker compose logs -f redis`, `docker compose logs -f meilisearch`, `docker compose logs -f celery-beat`, `docker compose logs -f celery-worker`
- Uruchom backend lokalnie: `rye run python backend/manage.py runserver`
- Szybki seed: `rye run python backend/manage.py seed_demo`

# taekwonhandbook

Describe your project here.

## License & Content Policy

- Code: Apache-2.0 (see `LICENSE`).
- Content/Data: NOT covered by the open-source license. Any datasets, media,
  texts, syllabus materials, and database exports are proprietary and may not be
  copied, redistributed or published without explicit permission. See `NOTICE`.

Planned monetization: subscription features are compatible with Apache-2.0; the
license allows SaaS use while keeping proprietary content closed.
