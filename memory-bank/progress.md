---
id: MB.PROGRESS.v1
title: Postęp prac, roadmapa i CI/CD
version: 1.0.0
status: draft
tags: [progress, roadmap, cicd]
updated: 2025-08-09
owner: delivery
---

## Roadmap (MVP → 8 tygodni)
- Tydz. 1–2: Szkielet Django/DRF + Auth JWT, modele Technique/Tul/Media, OpenAPI; Flutter skeleton, klient OpenAPI, IA ekrany.
- Tydz. 3–4: Upload/transkodowanie, listy/karty, offline cache, wyszukiwanie (Meilisearch).
- Tydz. 5–6: Quizy SRS (SM‑2), sylabus 9–6 kup, harmonogram, push.
- Tydz. 7–8: QA, lokalizacja KR/EN, CDN, analityka, przygotowanie do store.

## CI/CD
- Backend: lint, testy, makemigrations --check, build/push Docker, deploy (K8s/ECS). Migracje po deploy.
- Frontend: analyze/test, build IPA/AAB z fastlane, dystrybucja TestFlight/Play Internal.

## Metryki jakości
- Sentry error rate < 1%, pokrycie testami kluczowych modułów ≥ 60% (MVP), P95 dla list < 200 ms (cache + ETag).

## Ostatnie decyzje
- ADR‑001, ADR‑002, ADR‑003 (CSP), ADR‑004 (throttling), ADR‑005 (ExamSyllabus), ADR‑011 (monetyzacja Free/Pro/Club), ADR‑012 (anti‑scraping) — zob. `activeContext.md`.

## Co dalej (backend)
- Uzupełnić OpenAPI dla wszystkich APIViews (brak ostrzeżeń), gotowe `openapi.json` w repo root.
- Dodać request_id do logów Gunicorna i korelację z Nginx JSON.
- Przygotować profile prod (ENV: `CSRF_TRUSTED_ORIGINS`, `DJANGO_ALLOWED_HOSTS`, `CDN_ORIGIN`).
- Opcjonalnie: dodać integrację z Sentry (BE/FE) i PostHog/Amplitude.
- Billing: twarde webhooki (Stripe/RevenueCat) + idempotencja, TTL tokenu entitlements, Club API (create/invite/seats).

## Artefakty
- OpenAPI: `openapi.json` (aktualne po uruchomieniu `./scripts/export_openapi.sh`).
- Docs:
  - Public Pages (subset): `https://alphatra.github.io/taekwonhandbook-backend-/`
  - Private ZIP (Actions → Build & Deploy Docs → Artifacts): `private-docs`

## Release/Deploy checklist (prod)
- ENV: `DJANGO_DEBUG=0`, `DJANGO_ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DJANGO_SECRET_KEY`, `REDIS_URL`, `DB_*`, `S3_*`, `MEILISEARCH_*`, `CDN_ORIGIN`.
- Build: `docker compose -f docker-compose.prod.yml build` → uruchomienie `up -d`.
- Migracje: automatycznie w entrypoincie (`manage.py migrate --noinput`).
- Health: `/health/` powinno zwrócić `ok` dla `db/redis/meilisearch`.
- Logi: JSON (Nginx/Gunicorn/Django) z `X-Request-ID`; korelacja działa.
- Smoke: `/api/docs`, `/api/v1/techniques`, `/api/v1/media`, JWT token.

