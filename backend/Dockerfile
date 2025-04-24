# --------------------------------------------------
# Backend/Dockerfile  (روش 2.2: تنظیم PYTHONPATH)
# --------------------------------------------------

# 1) پایه: Python 3.11 slim
FROM python:3.11-slim

# Update and upgrade system packages
RUN apt-get update && apt-get upgrade -y && apt-get clean

# 2) جلوگیری از buffering لاگ‌ها
ENV PYTHONUNBUFFERED=1

# 3) اضافه کردن مسیر کد به PYTHONPATH
#    این باعث می‌شود که پوشه /app/app
#    در sys.path قرار بگیرد و import experts.* کار کند.
# ENV PYTHONPATH="/app/app"

# 4) پوشه کاری
WORKDIR /app

# 5) نصب بسته‌های سیستمی
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      curl \
      netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

# 6) نصب وابستگی‌های Python
COPY backend/app/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r /app/requirements.txt

# 7) کپی کد و کانفیگ
COPY backend/app /app/app
COPY config.yaml /app/config.yaml
COPY backend/.env /app/.env

# 8) پورت
EXPOSE 8000

# 9) فرمان اجرا
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
