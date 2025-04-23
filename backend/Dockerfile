# پایه: پایتون 3.9
FROM python:3.9-slim

# تنظیم متغیر محیطی برای جلوگیری از buffer stdout/stderr
ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

# ایجاد پوشه‌ی کاری
WORKDIR /app

# نصب وابستگی‌های سیستمی
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# کپی فایل‌های پروژه
COPY backend/pyproject.toml backend/poetry.lock /app/
# (یا اگر از requirements.txt استفاده می‌کنی)
# COPY backend/requirements.txt /app/

# نصب وابستگی‌ها
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry install --no-dev --no-interaction --no-ansi

# کپی بقیه‌ی کد
COPY backend/app /app/app
COPY config.yaml /app/config.yaml
COPY backend/.env /app/.env

# اکسپورت پورت
EXPOSE 8000

# فرمان اجرا
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
