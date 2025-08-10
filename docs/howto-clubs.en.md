# Clubs API (EN)

Owner endpoints:
- GET /api/v1/billing/clubs — list owner's clubs
- POST /api/v1/billing/clubs — create club (name, plan, seats_total)
- POST /api/v1/billing/clubs/{id}/invite — invite member (user_id)
- DELETE /api/v1/billing/clubs/{id}/members/{user_id} — remove member (not owner)
- DELETE /api/v1/billing/clubs/{id} — delete club (when empty)

Member endpoints:
- POST /api/v1/billing/clubs/{id}/leave — leave club (not owner)

Requirements:
- JWT header Authorization: Bearer <token>
- Seat limit enforced by plan's seats_max

See also: howto-billing.en.md and Swagger UI under API.
