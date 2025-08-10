# Billing and Clubs (EN)

This guide shows how to:
- fetch plans (`GET /api/v1/billing/plans`)
- obtain an entitlements token (`GET /api/v1/billing/entitlements/token`)
- check ad decision (`GET /api/v1/ads/should-show`)
- create a club and invite/remove members, delete a club

## JWT
Obtain a token:

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"member","password":"Member123!"}'
```

## Plans
```bash
curl http://localhost:8000/api/v1/billing/plans
```

## Entitlements token
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/billing/entitlements/token
```
Response contains `token` (signed) and `ttlSeconds` (default 300).

## Ads decision
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/ads/should-show
```
If user has `no_ads` entitlement, response is `{ "shouldShow": false, "reason": "no_ads" }`.

## Clubs
- Create a club (owner):
```bash
curl -X POST -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"Do jang A","plan":"club","seats_total":5}' \
  http://localhost:8000/api/v1/billing/clubs
```
- Invite a member (owner):
```bash
curl -X POST -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"user_id":3}' \
  http://localhost:8000/api/v1/billing/clubs/1/invite
```
- Remove a member (owner):
```bash
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/billing/clubs/1/members/3
```
- Delete an empty club (owner only):
```bash
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/billing/clubs/1
```
