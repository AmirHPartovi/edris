#!/usr/bin/env bash
set -euo pipefail

# اطمینان از در دسترس بودن Docker
command -v docker >/dev/null 2>&1 || { echo >&2 "Docker نصب نیست"; exit 1; }

# بیلد و بالا آوردن سرویس‌ها
docker compose up --build -d
