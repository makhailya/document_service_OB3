# Берём официальный образ Python
FROM python:3.14-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Создаём непривилегированного пользователя
# (убрали обратный слеш, теперь команда завершается)
RUN useradd --create-home appuser

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости без создания виртуального окружения
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --with dev

# Копируем весь проект
COPY . .

# Создаём папки для статики и медиа
RUN mkdir -p /app/static /app/media

# Копируем и делаем исполняемым entrypoint скрипт
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Меняем владельца всех файлов на appuser
RUN chown -R appuser:appuser /app /entrypoint.sh

# Переключаемся на непривилегированного пользователя
USER appuser

# Открываем порт
EXPOSE 8000

# Команда запуска
ENTRYPOINT ["/entrypoint.sh"]
