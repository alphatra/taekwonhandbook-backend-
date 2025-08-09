---
id: MB.TECHCONTEXT.v1
title: Kontekst Techniczny — Architektura i Stack
version: 1.0.0
status: approved
tags: [architecture, backend, frontend, devops]
updated: 2025-08-08
owner: platform-arch
---

## Architektura
- Frontend: Flutter (iOS/Android/Web), Riverpod/Bloc, Isar/Hive, Background sync (WorkManager/BackgroundFetch), VideoPlayer + cache.
- Backend: Django + DRF (OpenAPI przez drf-spectacular), JWT (SimpleJWT) + OAuth Apple/Google, Channels (WebSocket), Celery + Redis.
- Wyszukiwanie: Meilisearch (MVP) / Elasticsearch (rozszerzenie), indeksy: techniques, tuls, glossary.
- CMS: lekkie modele + Django Admin (MVP), opcjonalnie Wagtail headless.
- Pliki: S3 (prod) / MinIO (dev), podpisane URL, CDN (CloudFront/Cloudflare).
- Baza: Postgres. Serwowanie: Nginx → Gunicorn/Uvicorn (ASGI).
 - Versioning: API pod `/api/v1/*`; docs pod `/api/docs`, schema pod `/api/schema`.
 - Observability: logi JSON (Nginx/Gunicorn/Django) z `X-Request-ID`; w DEV logi Rich.

## Kluczowe modele (skrót)
- Technique(id, names{pl,en,kr}, audio, category, minBelt, keyPoints[], commonMistakes[], videos{front,side,slow}, safety, tags[])
- Tul(id, name, belt, steps[], diagram, tempo[], videos{demo,slow,mirror}, meaning, judgeNotes)
- Exercise, Plan, QuizQuestion, ExamSyllabus, Progress, MediaAsset

## API (przykłady)
- GET /api/v1/techniques?category=kick&belt=7
- GET /api/v1/techniques/{id}
- GET /api/v1/tuls/{id}
- POST /api/v1/progress
- GET /api/v1/quizzes/start?mode=terms&belt=7
- POST /api/v1/quizzes/{sessionId}/answer
- GET /api/v1/exams/{belt}/syllabus
- POST /api/v1/media/upload → Celery transkodowanie
- GET /api/v1/media?techniques=<id>&tuls=<id>

## Asynchronicznie (Celery)
- Transkodowanie (ffmpeg), miniatury, indeksacja, SRS scheduler, powiadomienia.

## DevOps i jakość
- CI/CD: GitHub Actions; Backend: lint/test/migrations --check/build/push/deploy; Frontend: analyze/test/build IPA/AAB (fastlane).
- Monitoring: Sentry (FE/BE), Prometheus + Grafana, PostHog/Amplitude.
- Bezpieczeństwo: JWT rotacja, throttling, CORS, CSP, Signed URLs, dependency scans.

## Referencje
- Medium (Django↔Flutter): [Easy steps to connect Django and Flutter mobile apps](https://medium.com/django-unleashed/easy-steps-to-connect-django-and-flutter-mobile-apps-b80de633191a)
- Repo przykład: [pygraz/django-flutter-example](https://github.com/pygraz/django-flutter-example)
- Stream: [YouTube — Django + Flutter stream](https://www.youtube.com/watch?v=VnztChBw7Og)

