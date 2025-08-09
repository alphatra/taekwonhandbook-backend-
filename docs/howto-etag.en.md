How‑to: ETag (If‑None‑Match)

Conditional GET for techniques list:

```bash
# 1) First fetch
curl -i "http://localhost:8000/api/v1/techniques/" \
  -H "Authorization: Bearer $ACCESS"

# Read ETag header from response, e.g. ETag: "\"abc123\""
ETAG=\"abc123\"

# 2) Conditional fetch (no changes → 304)
curl -i "http://localhost:8000/api/v1/techniques/" \
  -H "If-None-Match: $ETAG" \
  -H "Authorization: Bearer $ACCESS"
```

In an offline-first client: persist ETags per resource and use `If-None-Match`; on 304 keep cached data.

