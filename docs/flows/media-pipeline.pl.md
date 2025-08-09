## Pipeline wideo (upload → transcode → thumbnails)

Lista kroków:
1. FE: POST /api/v1/media/upload (filename)
2. API: zwraca presigned POST (url, fields)
3. FE: upload multipart do S3/MinIO
4. FE: POST /api/v1/media/complete (key, kind)
5. API: Celery transcode_media(asset_id) → rendery + miniatury

