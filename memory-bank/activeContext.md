---
id: MB.ACTIVECONTEXT.v1
title: Aktywny Kontekst — decyzje, ADR, zmiany schematu
version: 1.0.0
status: draft
tags: [adr, checklist, changes]
updated: 2025-08-09
owner: core-arch
---

## ADR‑001: Meilisearch jako wyszukiwarka MVP
- Decyzja: Meilisearch (lekki, prosty deploy) na MVP; możliwość migracji do Elasticsearch.
- Uzasadnienie: czas dostarczenia i prostota.
- Koszt zmiany: średni (migracja indeksów i klienta).

## ADR‑002: SM‑2 jako domyślny algorytm SRS
- Decyzja: Start od SM‑2, możliwość migracji do FSRS.
- Uzasadnienie: prostota, sprawdzony algorytm.
- Koszt zmiany: niski/średni (mapowanie parametrów).

## Zmiany DB/API w toku
- ENT.TECHNIQUE.v1 — definicja modelu i endpointów (Django/DRF), i18n, signed URLs.
- ENT.TUL.v1 — kroki, tempo, mirror; wideo wielobitrate.
- ENT.MEDIA.v1 — pipeline upload→transcode→thumbnails.
 - ENT.BILLING.v1 — plany/subskrypcje/entitlements, reklamy z cappingiem, webhooki providerów.

## Checklisty wydania (MVP)
- OpenAPI wygenerowane i opublikowane; klient Dart wygenerowany.
- Sync offline: ETag + kolejka push dla `progress`, testy konfliktów.
- Sentry (FE/BE), health checks, alerty Celery/Redis.

## ADR‑003: Content‑Security‑Policy (django‑csp) w produkcji
- Decyzja: Włączyć `django-csp` z domyślnymi dyrektywami: `default-src 'self'`, `img-src 'self' data: blob:`, `media-src 'self' data: blob: {CDN_ORIGIN}`, `script-src 'self'` (opcjonalnie `'unsafe-inline'` via env), `style-src 'self' 'unsafe-inline'`.
- Uzasadnienie: ochrona przed XSS/clickjacking; łatwa konfiguracja per środowisko.
- Wpływ: Nginx/ASGI bez zmian; konieczne dopasowanie `CDN_ORIGIN` i wyjątków dla analytics jeśli włączone.
- Koszt zmiany: niski.

## ADR‑004: Throttling DRF (global + per‑endpoint)
- Decyzja: Włączyć DRF throttling: globalnie `anon=100/min`, `user=1000/min`, oraz zakresy per endpoint: `media=20/min`, `search=60/min`, `quizzes=60/min`, `progress=120/min` (konfigurowalne ENV).
- Uzasadnienie: ochrona API i zasobów (S3 presign, quizy), prewencja nadużyć.
- Wpływ: wymagane obsłużenie HTTP 429 po stronie klienta (retry/backoff).
- Koszt zmiany: niski.

## ADR‑005: ExamSyllabus — endpoint referencyjny
- Decyzja: Udostępnić `GET /api/exams/{belt}/syllabus` jako źródło prawdy dla sylabusów 9–6 kup (rozszerzalne).
- Uzasadnienie: jeden kontrakt dla klienta i panelu treści; łatwe wersjonowanie (`version`, `valid_from/to`).
- Wpływ: modele `ExamSyllabus`, integracja z treściami i IA egzaminów.
- Koszt zmiany: niski/średni (ew. migracja formatu przy rozbudowie teorii/testów siły).

## ADR‑006: Versioning API `v1`
- Decyzja: Wszystkie ścieżki biznesowe pod `api/v1/*` (auth/schema/docs poza prefixem).
- Uzasadnienie: stabilność kontraktu i możliwość wprowadzenia `v2` bez zrywania zgodności.
- Wpływ: aktualizacja testów i dokumentacji; aliasy w routerach.
- Koszt zmiany: niski.

## ADR‑007: ETag + Pagination + Ordering
- Decyzja: włączyć `ConditionalGetMiddleware` + `USE_ETAGS=True`; globalna paginacja DRF (PageNumber), `OrderingFilter`.
- Uzasadnienie: mniejsze payloady, szybsze listy, delta‑sync i powtarzalne sortowanie.
- Wpływ: odpowiedzi list zwracają strukturę paginowaną; klienci używają `?ordering=`.
- Koszt zmiany: niski.

## ADR‑008: Observability i korelacja logów
- Decyzja: JSON logi w prod (Django request + Nginx + Gunicorn) z `X-Request-ID`; w DEV czytelne logi Rich + mini‑tabela requestu.
- Uzasadnienie: szybka diagnoza w DEV, kompletna korelacja w prod.
- Wpływ: `RequestLogMiddleware`, `nginx.conf` JSON access, `gunicorn.conf.py` JSON access.
- Koszt zmiany: niski.

## ADR‑009: Admin UX dla pól JSON
- Decyzja: `django-json-widget` (tryb tree) we wszystkich `JSONField` (Technique/Tul/Media/ExamSyllabus częściowo).
- Uzasadnienie: brak ręcznego wklejania JSON; walidacja i wygodna edycja.
- Wpływ: szybsza praca redakcji.
- Koszt zmiany: niski.

## ADR‑010: Relacje M2M dla treści
- Decyzja: `ExamSyllabus.required_techniques/tuls` oraz `MediaAsset.techniques/tuls` jako ManyToMany; filtry w API (`hasMedia`, `?techniques=`/`?tuls=`).
- Uzasadnienie: relacyjne modelowanie; proste zapytania i panel admina bez JSON.
- Wpływ: migracje; aktualizacja serializerów i widoków; dodane filtry.
- Koszt zmiany: niski/średni (migracje i UI admina).

## ADR‑011: Model monetyzacji — Free + Pro + Club
- Decyzja: Wszystkie treści dostępne za darmo (Free) z rzadkimi fullscreen ads (cap session/daily, cooldown). Plan Pro wyłącza reklamy i daje komfort offline; Plan Club umożliwia funkcje zespołowe (quizy klubowe, seat’y, analityka).
- Wpływ (BE): nowa aplikacja `tkh_billing` (Plan, Subscription, Entitlement, Club, ClubMember, AdPolicy); endpointy: `GET /billing/plans`, `GET /billing/me`, `GET /ads/should-show`, `GET /billing/entitlements/token`, webhooki `POST /billing/webhooks/(stripe|revenuecat)`.
- Wpływ (FE): integracja z RevenueCat/Stripe, egzekwowanie `no_ads`, capy po stronie SDK + serwerowa decyzja.
- Koszt zmiany: średni (integracja providerów, płatne testy sandbox).

## ADR‑012: Anti‑scraping i polityka danych
- Decyzja: `DisallowScrapingMiddleware` (nagłówki: `nosniff`, `DENY`, `X‑Robots‑Tag: noindex`), `robots.txt` = `Disallow: /`, otwarty kod Apache‑2.0, treści/dane zastrzeżone (NOTICE/ToS).
- Uzasadnienie: maksymalnie otwarty kod przy ochronie treści; sygnały dla botów i wyszukiwarek.
- Wpływ: brak zmian funkcjonalnych; lepsza zgodność prawna i ograniczenie indeksacji.
- Koszt zmiany: niski.

## Docs: public/private portal
- Public: MkDocs Material i18n (PL/EN), How‑to (JWT, ETag, Filters, Upload), API (Swagger UI), Legal.
- Private ZIP (Actions Artifact): pełna dokumentacja łącznie z Reference (mkdocstrings).

## ADR‑014: Dokumentowanie przepływów funkcjonalnych (bez kodu)
- Decyzja: Wszystkie kluczowe pipelines opisujemy tekstowo (kroki) w memory‑bank i docs how‑to zamiast Mermaid (stabilność buildów). Każdy przepływ ma: wejścia, walidacje, decyzje, wyjścia, oraz linki do endpointów.
- Zakres przepływów: Media (upload→complete→transcode→list), Billing/Clubs (plans→webhook→entitlements→ads; clubs CRUD+roles), Search (Meili→fallback), Progress (upsert+ETag), Health (db/redis/meili status), Admin (dashboard wykresy + quick links).
- Koszt zmiany: niski.

## ADR‑013: Clubs API (owner‑centric)
- Decyzja: Minimalne API klubów dla planu `club`: list/create owner clubs; invite/remove członków; delete klubu tylko gdy pusty. Limit miejsc egzekwowany przez `seats_max` w planie.
- Endpointy: `GET/POST /billing/clubs`, `POST /billing/clubs/{id}/invite`, `DELETE /billing/clubs/{id}/members/{user_id}`, `DELETE /billing/clubs/{id}`.
- Uzasadnienie: potrzebny prosty model zespołowy (kluby/trenerzy) na MVP z bezpieczeństwem po stronie serwera.
- Koszt zmiany: niski/średni (rozszerzenia: role per uprawnienia, zaproszenia mail/link, seat management UI).

