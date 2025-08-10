# Media: upload → transcode → listing (EN)

## 1) Presigned upload (S3/MinIO)
```bash
curl -X POST http://localhost:8000/api/v1/media/upload   -H "Authorization: Bearer $TOKEN"   -H 'Content-Type: application/json'   -d '{"filename":"test.mp4"}'
```
The response contains `url` and `fields` for direct POST to the bucket.

## 2) Complete upload and start transcode
After successful POST to the bucket, call:
```bash
curl -X POST http://localhost:8000/api/v1/media/complete   -H "Authorization: Bearer $TOKEN"   -d "key=uploads/1/test.mp4" -d "kind=video"
```
In DEV Celery runs eager – the asset gets `status=ready`, `codec=h264`, `duration≈12.34`, `resolutions=[360p,480p]`, thumbnails.

## 3) List and filters
```bash
# all ready videos with h264 codec
curl "http://localhost:8000/api/v1/media/assets?status=ready&kind=video&codec=h264"

# duration range
curl "http://localhost:8000/api/v1/media/assets?duration_min=1&duration_max=30"

# by resolution (JSON contains)
curl "http://localhost:8000/api/v1/media/assets?resolution=480p"
