#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "Exporting OpenAPI schema to openapi.json..."
rye run python backend/manage.py export_openapi > openapi.json
echo "Saved to $(pwd)/openapi.json"

