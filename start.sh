#!/usr/bin/env bash
set -euo pipefail

command -v docker >/dev/null 2>&1 || { echo >&2 "Docker Not Installed "; exit 1; }

# پاکسازی و بیلد مجدد
docker compose down --volumes
docker compose up --build -d

echo "Waiting for backend to be healthy..."
sleep 5
docker logs --tail 50 edris-backend
