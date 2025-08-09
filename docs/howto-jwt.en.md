How‑to: JWT (login and refresh)

1) Obtain token

```bash
curl -X POST "http://localhost:8000/api/auth/token/" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>"}'
# => { "access": "...", "refresh": "..." }
```

2) Use token

```bash
ACCESS=<access>
curl -H "Authorization: Bearer $ACCESS" \
  "http://localhost:8000/api/v1/techniques/?page=1"
```

3) Refresh token

```bash
REFRESH=<refresh>
curl -X POST "http://localhost:8000/api/auth/token/refresh/" \
  -H "Content-Type: application/json" \
  -d "{\"refresh\":\"$REFRESH\"}"
# => { "access": "..." }
```

Client: store `access` short‑lived, `refresh` in secure storage; on 401 try refresh then retry request.

