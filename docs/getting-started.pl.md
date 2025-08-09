## Szybki start (DEV)

1. `rye pin 3.12 && rye sync`
2. `docker compose up -d postgres redis meilisearch minio`
3. `rye run python backend/manage.py migrate`
4. `rye run python backend/manage.py runserver`

API: `/api/docs/` (Swagger/Redoc)

### Upload wideo (przykład cURL)

1) Pobierz presigned POST:

```bash
curl -X POST "http://localhost:8000/api/v1/media/upload" \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"filename":"demo.mp4"}'
```

2) Wyślij plik bezpośrednio do S3/MinIO:

```bash
curl -X POST "$URL_Z_KROKU_1" \
  -F key="$KEY" \
  -F acl=private \
  -F AWSAccessKeyId="$ACCESS_KEY" \
  -F policy="$POLICY" \
  -F signature="$SIGNATURE" \
  -F file=@demo.mp4
```

3) Finalizacja:

```bash
curl -X POST "http://localhost:8000/api/v1/media/complete" \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"key":"uploads/<uid>/demo.mp4","kind":"video"}'
```
