---
id: MB.SYSTEMPATTERNS.v1
title: Wzorce Systemowe — Offline‑first, Wideo, SRS, Wyszukiwanie, Sync
version: 1.0.0
status: approved
tags: [patterns, offline, srs, video, search, syncing]
updated: 2025-08-08
owner: platform-arch
---

## Offline‑first (Delta Sync)
- Pull: ETag per kolekcja (techniques, tuls, glossary, plans). Algorytm: If‑None‑Match → 304 (brak zmian) lub 200 z delta window (since=lastSyncAt) i listą zmian (upserts/deletes) z `valid_from/valid_to`.
- Push: Kolejka zmian (progress, quiz answers). Retry z backoff, idempotentne endpointy (upsert przez naturalny klucz user+itemType+itemId). Konflikty: merge heurystyki (np. progress.score = max). 
- Konflikty czasowe: last‑write‑wins dla pól niekumulatywnych.

## Media i wideo
- Upload: pre‑signed POST do S3/MinIO; po zakończeniu POST /api/media/complete → Celery job: ffmpeg transkodowanie (HLS/DASH lub MP4 multi‑bitrate), generacja miniatur, VTT/SRT.
- Odtwarzanie: VideoPlayer z markerami kroków/tempa; LRU cache offline z limitami MB.
- Signed URLs TTL: 10–60 min, odświeżane transparentnie.

### Powiązania i filtrowanie
- `MediaAsset` posiada relacje M2M do `Technique` i `Tul`; API oferuje listę `/api/v1/media/` z filtrami `?techniques=<id>&tuls=<id>&kind=&status=`.
- `Technique` i `Tul` mają filtr `?hasMedia=true|false` (JOIN do relacji z mediami).

## SRS (SM‑2 → FSRS)
- Start: SM‑2 z polami easeFactor, interval, repetitions, nextReviewAt; zapisywane w `quizzes` + `progress`.
- Migracja: flagą `algo=sm2|fsrs` + migracja parametrów. Zadanie Celery generuje harmonogram przypomnień.

## Wyszukiwanie
- Meilisearch: indeksy `techniques`, `tuls`, `glossary`; pola boost: tags, belt, category. Indeksacja async po publikacji/aktualizacji treści.

## Wersjonowanie treści
- Pola: `version`, `valid_from`, `valid_to`, `is_draft`. Soft‑rollout kontrolowany feature flagami (ConfigCat/LaunchDarkly). Flutter przechowuje wiele wersji rekordów, aktywną wybiera po `now ∈ [valid_from, valid_to)`.

## Bezpieczeństwo i prywatność
- JWT rotacja/refresh, throttling per IP/user, CORS/CSP. Brak PII w eventach produktowych. Signed URLs, minimal scope.

## Schematy API (zarysy)
- GET /api/v1/techniques?etag=... → 200 { count, next, previous, results:[...] } + ETag / 304
- POST /api/v1/progress { userItem:{itemType,itemId}, status, score, occurredAt } → 200 upsert
- POST /api/v1/media/upload { filename, size, mime } → 200 { url, fields } (S3 form)
- GET /api/v1/media?techniques=<id>&tuls=<id>&kind=video&status=ready → lista powiązanych mediów

