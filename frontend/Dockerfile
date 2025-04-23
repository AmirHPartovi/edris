# پایه: Node.js 16
FROM node:16-alpine AS builder

WORKDIR /app

# کپی و نصب وابستگی‌ها
COPY frontend/package*.json ./
RUN npm install

# کپی و بیلد
COPY frontend/ ./
RUN npm run build

# مرحله نهایی با Nginx
FROM nginx:stable-alpine

# حذف تنظیمات پیش‌فرض
RUN rm /etc/nginx/conf.d/default.conf

# کپی فایل کانفیگ Nginx
COPY docker/nginx.conf /etc/nginx/conf.d

# کپی خروجی بیلد
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
