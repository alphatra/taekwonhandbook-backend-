How‑to: ETag (If‑None‑Match)

Lista technik z warunkowym GET:

```bash
# 1) Pierwsze pobranie
curl -i "http://localhost:8000/api/v1/techniques/" \
  -H "Authorization: Bearer $ACCESS"

# Sprawdź nagłówek ETag w odpowiedzi, np. ETag: "\"abc123\""
ETAG=\"abc123\"

# 2) Warunkowe pobranie (brak zmian → 304)
curl -i "http://localhost:8000/api/v1/techniques/" \
  -H "If-None-Match: $ETAG" \
  -H "Authorization: Bearer $ACCESS"
```

W kliencie offline-first: zapisuj ETag per zasób i używaj `If-None-Match`; przy 304 pozostaw cache bez zmian.

