# Clubs API (PL)

Endpointy (owner):
- GET /api/v1/billing/clubs — lista klubów właściciela
- POST /api/v1/billing/clubs — utwórz klub (name, plan, seats_total)
- POST /api/v1/billing/clubs/{id}/invite — zaproś członka (user_id)
- DELETE /api/v1/billing/clubs/{id}/members/{user_id} — usuń członka (nie owner)
- DELETE /api/v1/billing/clubs/{id} — usuń klub (gdy pusty)

Endpointy (member):
- POST /api/v1/billing/clubs/{id}/leave — opuść klub (nie owner)

Wymagania:
- JWT w nagłówku Authorization: Bearer <token>
- Limit miejsc: egzekwowany przez seats_max planu club

Zobacz także: howto-billing.pl.md oraz Swagger UI w sekcji API.

## Uprawnienia ról

| Operacja | Endpoint | owner | coach | member |
|---|---|---|---|---|
| Lista klubów | GET /api/v1/billing/clubs | ✓ | ✓ | ✗ |
| Utwórz klub | POST /api/v1/billing/clubs | ✓ | ✗ | ✗ |
| Lista członków | GET /api/v1/billing/clubs/{id}/members | ✓ | ✓ | ✗ |
| Zaproś członka | POST /api/v1/billing/clubs/{id}/invite | ✓ | ✓ | ✗ |
| Usuń członka | DELETE /api/v1/billing/clubs/{id}/members/{user_id} | ✓ | ✓ | ✗ |
| Zmień rolę | POST /api/v1/billing/clubs/{id}/members/{user_id}/role | ✓ | ✗ | ✗ |
| Usuń klub (pusty) | DELETE /api/v1/billing/clubs/{id} | ✓ | ✗ | ✗ |
| Opuść klub | POST /api/v1/billing/clubs/{id}/leave | ✗ | ✗ | ✓ |
