#!/usr/bin/env bash
set -euo pipefail

# بالا بردن سرویس‌ها با Docker Compose
# مطمئن باش docker و docker-compose روی سیستم نصب هستند
docker-compose up --build
