# Берём официальный образ Python
FROM python:3.14-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости без создания виртуального окружения
# (в Docker оно не нужно — контейнер сам изолирован)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --with dev

# Копируем весь проект
COPY . .

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
