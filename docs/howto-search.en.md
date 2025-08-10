# Search & Reindex (EN)

## Endpoint `/api/v1/search`
- Params:
  - q: query string (optional)
  - type: technique | tul (default technique)
  - limit: 1–50 (default 20)
- Behavior: Meilisearch first, then DB fallback.

Example:
```bash
curl "http://localhost:8000/api/v1/search?q=Hwa&type=tul&limit=5"
```

## Meilisearch Reindex
- Command:
```bash
rye run python backend/manage.py reindex_search --types techniques,tuls --batch-size 500 --drop
```
- Options:
  - --types: techniques,tuls (comma-separated)
  - --batch-size: batch size (default 500)
  - --drop: drop/recreate indices before ingest
  - --dry-run: count only, do not write to Meilisearch

Requirements:
- Env vars: MEILISEARCH_URL, optional MEILISEARCH_API_KEY
