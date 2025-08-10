# Billing i Kluby (PL)

Ten przewodnik pokazuje jak:
- pobrać plany (`GET /api/v1/billing/plans`),
- uzyskać token uprawnień (`GET /api/v1/billing/entitlements/token`),
- sprawdzić decyzję reklam (`GET /api/v1/ads/should-show`),
- utworzyć klub i zaprosić członka.

## JWT
Uzyskaj token:

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"member","password":"Member123!"}'
```

## Plany
```bash
curl http://localhost:8000/api/v1/billing/plans
```

## Token uprawnień
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/billing/entitlements/token
```
Odpowiedź zawiera `token` i `ttlSeconds`.

## Reklamy
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/ads/should-show
```

## Kluby
- Utwórz klub:
```bash
curl -X POST -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"Do jang A","plan":"club","seats_total":5}' \
  http://localhost:8000/api/v1/billing/clubs
```
- Zaproś członka:
```bash
curl -X POST -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"user_id":3}' \
  http://localhost:8000/api/v1/billing/clubs/1/invite
```
- Usuń członka:
```bash
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/billing/clubs/1/members/3
```

