How‑to: Paginacja, sortowanie i filtrowanie

## Paginacja (DRF PageNumberPagination)

```bash
curl "http://localhost:8000/api/v1/techniques/?page=2" \
  -H "Authorization: Bearer $ACCESS"
```

## Sortowanie (OrderingFilter)

```bash
# malejąco po updated_at, potem rosnąco po id
curl "http://localhost:8000/api/v1/techniques/?ordering=-updated_at,id" \
  -H "Authorization: Bearer $ACCESS"
```

## Filtrowanie — Techniques

```bash
# kategoria
curl "http://localhost:8000/api/v1/techniques/?category=hand" -H "Authorization: Bearer $ACCESS"

# minimalny pas
curl "http://localhost:8000/api/v1/techniques/?min_belt=5" -H "Authorization: Bearer $ACCESS"

# czy ma media
curl "http://localhost:8000/api/v1/techniques/?hasMedia=true" -H "Authorization: Bearer $ACCESS"
```

## Filtrowanie — Tuls

```bash
curl "http://localhost:8000/api/v1/tuls/?belt=6" -H "Authorization: Bearer $ACCESS"
```

