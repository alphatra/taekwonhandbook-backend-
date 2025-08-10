# Media: upload → transkodowanie → listy (PL)

## 1) Presigned upload (S3/MinIO)
```bash
curl -X POST http://localhost:8000/api/v1/media/upload   -H "Authorization: Bearer $TOKEN"   -H 'Content-Type: application/json'   -d '{"filename":"test.mp4"}'
```
Odpowiedź zawiera `url` i `fields` do formularza POST bezpośrednio do bucketa.

## 2) Zakończenie uploadu i start transkodowania
Po udanym POST do bucketa, wywołaj:
```bash
curl -X POST http://localhost:8000/api/v1/media/complete   -H "Authorization: Bearer $TOKEN"   -d "key=uploads/1/test.mp4" -d "kind=video"
```
W DEV Celery działa eager – zasób dostanie `status=ready`, `codec=h264`, `duration≈12.34`, `resolutions=[360p,480p]`, miniatury.

## 3) Lista i filtry
```bash
# wszystkie gotowe wideo z kodekiem h264
curl "http://localhost:8000/api/v1/media/assets?status=ready&kind=video&codec=h264"

# zakres czasu trwania
curl "http://localhost:8000/api/v1/media/assets?duration_min=1&duration_max=30"

# po rozdzielczości (JSON contains)
curl "http://localhost:8000/api/v1/media/assets?resolution=480p"
