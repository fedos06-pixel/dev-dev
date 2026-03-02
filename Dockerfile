FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Делаем скрипт запуска исполняемым
RUN chmod +x entrypoint.sh

# Переменная окружения (без секретов)
ENV APP_ENV=production

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["serve"]
