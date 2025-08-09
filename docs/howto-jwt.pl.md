How‑to: JWT (logowanie i odświeżanie)

1) Pobierz token (login)

```bash
curl -X POST "http://localhost:8000/api/auth/token/" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<hasło>"}'
# => { "access": "...", "refresh": "..." }
```

2) Użyj tokenu w zapytaniach API

```bash
ACCESS=<wstaw_access>
curl -H "Authorization: Bearer $ACCESS" \
  "http://localhost:8000/api/v1/techniques/?page=1"
```

3) Odśwież token

```bash
REFRESH=<wstaw_refresh>
curl -X POST "http://localhost:8000/api/auth/token/refresh/" \
  -H "Content-Type: application/json" \
  -d "{\"refresh\":\"$REFRESH\"}"
# => { "access": "..." }
```

W aplikacji klienckiej: przechowuj tylko `access` krótkoterminowo; `refresh` w bezpiecznym magazynie. Po 401 spróbuj odświeżenia i powtórz żądanie.

