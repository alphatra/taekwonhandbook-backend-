How‑to: Pagination, ordering, and filtering

## Pagination (DRF PageNumberPagination)

```bash
curl "http://localhost:8000/api/v1/techniques/?page=2" \
  -H "Authorization: Bearer $ACCESS"
```

## Ordering (OrderingFilter)

```bash
# descending by updated_at then ascending by id
curl "http://localhost:8000/api/v1/techniques/?ordering=-updated_at,id" \
  -H "Authorization: Bearer $ACCESS"
```

## Filtering — Techniques

```bash
# category
curl "http://localhost:8000/api/v1/techniques/?category=hand" -H "Authorization: Bearer $ACCESS"

# minimum belt
curl "http://localhost:8000/api/v1/techniques/?min_belt=5" -H "Authorization: Bearer $ACCESS"

# has media
curl "http://localhost:8000/api/v1/techniques/?hasMedia=true" -H "Authorization: Bearer $ACCESS"
```

## Filtering — Tuls

```bash
curl "http://localhost:8000/api/v1/tuls/?belt=6" -H "Authorization: Bearer $ACCESS"
```

