# Deploy (prod) – Compose

## ENV
Ustaw zmienne:
- DJANGO_DEBUG=0
- DJANGO_ALLOWED_HOSTS=your.domain
- CSRF_TRUSTED_ORIGINS=https://your.domain
- DJANGO_SECRET_KEY=<secret>
- REDIS_URL=redis://redis:6379/0
- DB_* (jeśli zewnętrzny Postgres)
- S3_* (endpoint, bucket, keys)
- MEILISEARCH_URL=http://meilisearch:7700
- CSP_CONNECT_EXTRA=https://sentry.io (opcjonalnie)

## Uruchomienie
```bash
docker compose -f docker-compose.prod.yml up -d --build
```
Sprawdź:
- /health/ – powinno być OK dla db/redis/meilisearch
- /api/docs – Swagger

## Logi
- Nginx/Gunicorn/Django – JSON z X-Request-ID

## Aktualizacja
```bash
docker compose -f docker-compose.prod.yml pull &&   docker compose -f docker-compose.prod.yml up -d &&   docker image prune -f
```
