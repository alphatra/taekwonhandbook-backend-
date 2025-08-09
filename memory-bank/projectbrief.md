---
id: MB.PROJECTBRIEF.v1
title: ITF Taekwon‑Do Handbook — Project Brief
version: 1.0.0
status: approved
tags: [vision, scope, nfr, architecture]
updated: 2025-08-08
owner: core-arch
---

## Cel i wizja
ITF Taekwon‑Do Handbook to aplikacja mobilna i webowa dla uczniów i instruktorów ITF, łącząca leksykon technik i tul, szkolenia wideo (offline‑first), quizy SRS i ścieżki przygotowania do egzaminów. System jest projektowany jako skalowalna platforma treści, z synchronizacją postępów między urządzeniami i łagodną pracą w trybie offline.

## Użytkownicy i kluczowe wartości
- Uczeń: szybkie odnalezienie technik/tul, nauka krok po kroku, audio KR, materiały offline, quizy SRS.
- Instruktor: konspekty treningów, sylabusy, raport postępów, odtwarzanie wideo ze znacznikami kroków.
- Administrator/Redaktor: publikacja i wersjonowanie treści, transkodowanie wideo, indeksacja do wyszukiwarki.

## Zakres MVP
- Modele: Technique, Tul, MediaAsset, Plan/Exercise, QuizQuestion, ExamSyllabus, Progress.
- API: DRF REST + OpenAPI; listy i szczegóły, filtry, postęp, sesje quizów, uploady mediów (signed URLs).
- Klient Flutter: leksykon, tul, treningi, quizy, profil; offline cache (Isar/Hive), odtwarzacz wideo z markerami.
- DevOps: Docker Compose (dev), CI na GitHub Actions, S3/MinIO, Postgres, Redis, Meilisearch.

## Poza MVP (po 8 tyg.)
- Wagtail headless CMS (opcjonalnie), płatności subskrypcyjne, feature flags, analytics produktowe, web live‑feedback.

## NFR (kluczowe wymagania niefunkcjonalne)
- Wydajność: P95 < 200 ms dla listy 50 pozycji (z cache i ETag).
- Offline‑first: pełna nawigacja i przegląd treści przy braku sieci; kolejka zmian „push”.
- Multimedia: wideo z cache offline i limitami pamięci; transkodowanie wielorozdzielczościowo.
- Języki: PL/EN/KR; TTS i napisy; transliteracja.
- Bezpieczeństwo: JWT rotacja, signed URLs, rate limiting, CSP/CORS, brak PII w analytics.
- Skalowalność: stateless API, Celery workers, osobny search, S3/CDN, gotowość do K8s/ECS.

## Architektura (skrót)
- Frontend: Flutter (iOS/Android/Web), Riverpod/Bloc, Isar/Hive, Background sync.
- Backend: Django + DRF, SimpleJWT, OAuth (Apple/Google), Channels (WebSocket), Celery + Redis.
- Wyszukiwanie: Meilisearch (MVP) / Elasticsearch (rozszerzenie).
- Treści: lekkie modele + Django Admin (MVP), Wagtail headless (opcjonalnie).
- Pliki: S3 (prod) / MinIO (dev) + CDN.
- Baza: Postgres. Serwowanie: Nginx → Gunicorn/Uvicorn (ASGI).
 - Observability: Health, logi JSON (Nginx/Gunicorn/Django) z `X-Request-ID`, Rich w DEV, Swagger/OpenAPI, ETag.

## Sukces/Mierniki
- ≥ 1 000 aktywnych użytkowników miesięcznie, ≥ 70% zadowolenia UX.
- ≥ 95% pokrycia treścią sylabusu 9–6 kup (MVP) i ≥ 60% dla 6–8 tul.
- ≥ 80% dostarczonych list API z OpenAPI + wygenerowany klient Dart.
- ≥ 90% przypadków użycia działa offline; brak krytycznych crashy (Sentry error rate < 1%).

## Referencje
- Medium — łączenie Django i Flutter: [Easy steps to connect Django and Flutter mobile apps](https://medium.com/django-unleashed/easy-steps-to-connect-django-and-flutter-mobile-apps-b80de633191a)
- Przykład Django+Flutter: [pygraz/django-flutter-example](https://github.com/pygraz/django-flutter-example)
- Stream Django+Flutter: [YouTube — Django + Flutter stream](https://www.youtube.com/watch?v=VnztChBw7Og)

