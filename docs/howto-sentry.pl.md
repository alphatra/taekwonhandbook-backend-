# Sentry (PL)

## Konfiguracja
Ustaw zmienne środowiskowe:
- SENTRY_DSN: adres projektu w Sentry (włącza integrację)
- SENTRY_TRACES_SAMPLE_RATE (opcjonalnie, np. 0.1)
- SENTRY_PROFILES_SAMPLE_RATE (opcjonalnie)

Integracja inicjuje się automatycznie w core/__init__.py (Django + Celery). Dane osobowe nie są wysyłane (send_default_pii=False).

## Korelacja zdarzeń
Middleware dodaje do scope:
- request_id (tag) – zgodny z logami Nginx/Gunicorn/Django
- duration_ms (extra)

## Weryfikacja
Wywołaj błąd lokalnie, np. odwiedzając nieistniejący URL lub dodaj tymczasowo 1/0 w dowolnym widoku. Zdarzenie pojawi się w Sentry z tagiem request_id.
