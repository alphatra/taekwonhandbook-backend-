## Offline sync (delta + ETag)

Sekwencja (skrót):
- GET listy z If-None-Match → 304 przy zgodnym ETag
- POST progress w kolejce retry → 200/201

