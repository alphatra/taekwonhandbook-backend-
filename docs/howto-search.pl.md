# Wyszukiwanie i Reindeksacja (PL)

## Endpoint `/api/v1/search`
- Parametry:
  - q: fraza (opcjonalna)
  - type: technique | tul (domyślnie technique)
  - limit: 1–50 (domyślnie 20)
- Działanie: najpierw Meilisearch, w razie braku – fallback do bazy danych.

Przykład:
```bash
curl "http://localhost:8000/api/v1/search?q=Hwa&type=tul&limit=5"
```

## Reindeksacja Meilisearch
- Komenda:
```bash
rye run python backend/manage.py reindex_search --types techniques,tuls --batch-size 500 --drop
```
- Opcje:
  - --types: techniques,tuls (lista po przecinkach)
  - --batch-size: rozmiar partii (domyślnie 500)
  - --drop: usuń/odtwórz indeksy przed wgraniem danych
  - --dry-run: tylko policz rekordy, bez zapisu do Meilisearch

Wymagania:
- Zmienne środowiskowe: MEILISEARCH_URL, opcjonalnie MEILISEARCH_API_KEY
