## Offline sync (delta + ETag)

Sequence (short):
- GET list with If-None-Match → 304 on ETag match
- POST progress with retry queue → 200/201

