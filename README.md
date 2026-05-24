# 📄 Document Service

Сервис обработки загружаемых документов — REST API на Django + DRF.
Позволяет пользователям загружать, хранить и управлять документами
с полной изоляцией данных между пользователями.

## 🚀 Технологии

| Технология              | Назначение |
|-------------------------|---|
| Python 3.14             | Язык программирования |
| Django 6.x              | Веб-фреймворк |
| Django REST Framework   | REST API |
| PostgreSQL              | База данных |
| JWT (SimpleJWT)         | Авторизация |
| Docker + Docker-Compose | Контейнеризация |
| Nginx                   | Проксирование запросов |
| pytest                  | Тестирование |

## ⚙️ Запуск проекта

### 1. Клонируй репозиторий

```bash
git clone https://github.com/makhailya/document_service_OB3.git
cd document_service
```

### 2. Создай `.env` файл

```bash
cp .env.example .env
# Отредактируй .env под свои настройки
```

### 3. Запусти через Docker-Compose

```bash
docker-compose up --build
```

### 4. Создай суперпользователя (опционально)

```bash
docker-compose exec web python manage.py createsuperuser
```

## 📚 API Документация

После запуска доступна по адресу:

- **Swagger UI**: http://localhost:8000/api/docs/
- **Admin панель**: http://localhost:8000/admin/

## 🔑 Основные эндпоинты

### Пользователи
| Метод | URL | Описание |
|---|---|---|
| POST | `/api/users/register/` | Регистрация |
| POST | `/api/users/login/` | Вход (получение токенов) |
| POST | `/api/users/token/refresh/` | Обновление токена |
| GET/PATCH | `/api/users/profile/` | Профиль пользователя |

### Документы
| Метод | URL | Описание |
|---|---|---|
| GET | `/api/documents/` | Список своих документов |
| POST | `/api/documents/` | Загрузить документ |
| GET | `/api/documents/{id}/` | Просмотр документа |
| PATCH | `/api/documents/{id}/` | Обновить название/описание |
| DELETE | `/api/documents/{id}/` | Удалить документ |

## 📋 Ограничения

- Максимальный размер файла: **10 МБ**
- Разрешённые форматы: **PDF, DOCX, DOC, JPG, JPEG, PNG**
- Каждый пользователь видит **только свои** документы

## 🧪 Тестирование

```bash
# Запуск тестов с отчётом о покрытии
docker-compose exec web pytest --cov=. --cov-report=term-missing -v
```

## 🐳 Продакшен

```bash
docker-compose -f docker-compose.prod.yml up --build
```

## 📁 Структура проекта

```
document_service/
├── config/          # Настройки Django
├── users/           # Приложение пользователей
├── documents/       # Приложение документов
├── nginx.conf       # Конфигурация Nginx
├── Dockerfile
├── docker-compose.yml
└── docker-compose.prod.yml
```
