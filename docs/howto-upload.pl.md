How‑to: Upload wideo (presigned POST)

1) Pobierz presigned POST

```bash
curl -X POST "http://localhost:8000/api/v1/media/upload" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"filename":"demo.mp4"}'
# => { url, fields{ key, acl, AWSAccessKeyId, policy, signature } }
```

2) Wyślij plik do S3/MinIO (multipart)

```bash
curl -X POST "$URL" \
  -F key="$KEY" -F acl=private -F AWSAccessKeyId="$AK" \
  -F policy="$POLICY" -F signature="$SIG" \
  -F file=@demo.mp4
```

3) Finalizacja uploadu

```bash
curl -X POST "http://localhost:8000/api/v1/media/complete" \
  -H "Authorization: Bearer $ACCESS" \
  -H "Content-Type: application/json" \
  -d '{"key":"uploads/<uid>/demo.mp4","kind":"video"}'
```

