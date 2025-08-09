## Szybki start (DEV)

1. `rye pin 3.12 && rye sync`
2. `docker compose up -d postgres redis meilisearch minio`
3. `rye run python backend/manage.py migrate`
4. `rye run python backend/manage.py runserver`

API: `/api/docs/` (Swagger/Redoc)
