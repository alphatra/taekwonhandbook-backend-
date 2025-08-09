## Quick start (DEV)

1. `rye pin 3.12 && rye sync`
2. `docker compose up -d postgres redis meilisearch minio`
3. `rye run python backend/manage.py migrate`
4. `rye run python backend/manage.py runserver`

API: `/api/docs/` (Swagger/Redoc)

### Upload a video (cURL example)

1) Get presigned POST:

```bash
curl -X POST "http://localhost:8000/api/v1/media/upload" \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"filename":"demo.mp4"}'
```

2) Upload file directly to S3/MinIO:

```bash
curl -X POST "$URL_FROM_STEP1" \
  -F key="$KEY" \
  -F acl=private \
  -F AWSAccessKeyId="$ACCESS_KEY" \
  -F policy="$POLICY" \
  -F signature="$SIGNATURE" \
  -F file=@demo.mp4
```

3) Finalize:

```bash
curl -X POST "http://localhost:8000/api/v1/media/complete" \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"key":"uploads/<uid>/demo.mp4","kind":"video"}'
```

