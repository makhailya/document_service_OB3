#!/bin/sh

echo "Ожидаем запуска базы данных..."

# Ждём пока PostgreSQL не будет готов принимать соединения
while ! python -c "
import os, psycopg2
try:
    psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT', '5432'),
    )
    print('БД готова!')
except Exception as e:
    exit(1)
" 2>/dev/null; do
    echo "БД ещё не готова — ждём 1 секунду..."
    sleep 1
done

echo "Применяем миграции..."
python manage.py migrate --noinput

echo "Собираем статику..."
python manage.py collectstatic --noinput

echo "Запускаем сервер..."
exec "$@"
