---
id: MB.PRODUCTCONTEXT.v1
title: Kontekst Produktu i UX — ITF Taekwon‑Do Handbook
version: 1.0.0
status: approved
tags: [product, ux, ia, stakeholders]
updated: 2025-08-08
owner: product-lead
---

## Persony i główne scenariusze
- Uczeń (9–6 kup): nauka podstawowych technik i 6–8 tul, szybkie „jak to się robi” z wideo i audio KR; quizy terminów i teorii.
- Instruktor: planowanie treningu, demonstrowanie kroków (markery, tempo, „mirror”), checklisty egzaminów.
- Administrator/Redaktor: zarządzanie treściami (wersje), publikacja i aktualizacje multimediów, kontrola jakości.

## Mapa informacji (IA)
- Start: szybkie wejście do trybów Nauka/Trening/Quizy.
- Leksykon: Technique (karta z multimediami, key points, mistakes, safety, tagi).
- Tul: kroki, diagram, tempo, wideo demo/slow/mirror, znaczenie.
- Trening: plany i bloki Exercise, timery, sygnały dźwiękowe, markery.
- Quizy: tryby (terms, techniques, tul, theory), SRS z historią postępów.
- Profil: pas/klub, statystyki, pobrane, ustawienia offline/i18n.

## Zasady UX
- „Quick to learn”: jedna karta = cała technika; zawsze dostępny offline opis + niskiej rozdziałki wideo.
- „No dead ends”: zawsze linki kontekstowe (z Technique do Quizów, z Tul do Ćwiczeń).
- „Clear progress”: procenty, streaks, checklisty; konflikty offline rozwiązywane jako merge (max postępu).

## Lokalizacja i dostępność
- i18n: PL/EN/KR; transliteracja KR; TTS i napisy do wideo (VTT/SRT).
- A11y: wysokie kontrasty, rozmiar czcionki, napisy i audio guides.

## Ryzyka produktowe
- Zbyt „ciężkie” multimedia offline — mitigacja: limit pamięci, wielorozdzielczości, LRU cache, preferencje jakości.
- Złożoność SRS — mitigacja: zacząć od SM‑2, telemetry dla skuteczności; możliwość migracji do FSRS.
- Jakość treści i wersjonowanie — procedury review i soft‑rollout z feature flags.

## KPI
- DAU/WAU, czas nauki/dzień, liczba wykonanych quizów, retencja 4/8 tygodni, CR do subskrypcji Pro (po MVP).

## Runbook (operacje szybkie)
- Uruchomienie lokalne (bez Dockera): `rye sync` → `manage.py migrate` → `manage.py seed_demo` → `manage.py runserver`.
- Admin: `manage.py createsuperuser` → `/admin/` (JSON pola w trybie tree; M2M dla sylabusów i mediów).
- JWT: `POST /api/auth/token/` (demo/demo123) → `Authorization: Bearer <access>`.
- Health: `/health/` (db/redis/meili; bez Dockera możliwe `status=degraded`).
- OpenAPI: `/api/docs` (UI), `/api/schema` (JSON), `./scripts/export_openapi.sh` (plik).
- Media: `POST /api/v1/media/upload` (presign) → `POST /api/v1/media/complete` (tworzy `MediaAsset`, w DEBUG od razu `ready`).
- Wyszukiwanie: `GET /api/v1/search?q=&type=technique|tul`; z Meili lub fallback do DB.
- Filtry relacyjne: `GET /api/v1/media?techniques=<id>&tuls=<id>`; `GET /api/v1/techniques?hasMedia=true`.
- Logi:
  - DEV: kolorowe Rich + mini‑tabela requestów; PROD: JSON z `X-Request-ID` (Nginx/Gunicorn/Django).
- CI: `backend.yml` (ruff, check, migrations --check, pytest).

