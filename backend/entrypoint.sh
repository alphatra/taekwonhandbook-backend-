#!/usr/bin/env sh
set -e

python manage.py migrate --noinput

exec gunicorn core.asgi:application \
  --bind 0.0.0.0:8000 \
  --worker-class uvicorn.workers.UvicornWorker \
  --workers ${WEB_CONCURRENCY:-2} \
  --timeout 60 \
  -c /app/backend/gunicorn.conf.py

