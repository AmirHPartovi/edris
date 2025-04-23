#!/usr/bin/env bash
set -euo pipefail

# 1) بارگذاری متغیرهای محیطی
if [ -f backend/.env ]; then
  export $(grep -v '^#' backend/.env | xargs)
fi

# 2) ساخت و فعال‌سازی venv
python3 -m venv .venv
source .venv/bin/activate

# 3) نصب وابستگی‌ها
pip install --upgrade pip
pip install -r backend/app/requirements.txt

# 4) ساخت دایرکتوری‌های دانش
mkdir -p backend/app/knowledge/{docs,vectorstore}

# 5) بررسی و راه‌اندازی Ollama
OLLAMA_API_URL="${OLLAMA_API_URL:-http://localhost:11434/api/generate}"
# می‌توان پورت را از URL استخراج کرد یا مستقیم URL را چک کرد:
if ! nc -z $(echo "$OLLAMA_API_URL" | sed -E 's|https?://([^:/]+):?([0-9]*).*|\1 \2|') ; then
  echo "Starting Ollama..."
  ollama serve --port "${OLLAMA_PORT:-11434}" &
  sleep 3
fi

# 6) اجرای Frontend
(
  cd frontend
  npm install
  npm run build
  npm start &
)

# 7) اجرای Backend
uvicorn backend.app.main:app --host 0.0.0.0 --port "${BACKEND_PORT:-8000}"
