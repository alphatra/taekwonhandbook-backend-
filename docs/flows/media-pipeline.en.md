## Video pipeline (upload → transcode → thumbnails)

Steps:
1. FE: POST /api/v1/media/upload (filename)
2. API: returns presigned POST (url, fields)
3. FE: upload multipart to S3/MinIO
4. FE: POST /api/v1/media/complete (key, kind)
5. API: Celery transcode_media(asset_id) → renditions + thumbnails

