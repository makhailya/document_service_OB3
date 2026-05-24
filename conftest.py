import io
import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


# ============================
# Фикстуры пользователей
# ============================

@pytest.fixture
def user(db):
    """
    Обычный тестовый пользователь.
    db — говорит pytest что тест работает с базой данных.
    """
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='strongpassword123',
    )


@pytest.fixture
def another_user(db):
    """Второй пользователь — для проверки изоляции данных"""
    return User.objects.create_user(
        username='anotheruser',
        email='another@example.com',
        password='strongpassword123',
    )


# ============================
# Фикстуры клиентов
# ============================

@pytest.fixture
def api_client():
    """
    Обычный неавторизованный клиент.
    Используется в тестах, где не нужна авторизация.
    """
    return APIClient()


@pytest.fixture
def authenticated_client(user):
    """
    Авторизованный клиент от имени первого пользователя.
    Создаёт свой собственный экземпляр APIClient,
    чтобы не конфликтовать с другими клиентами.
    """
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def another_authenticated_client(another_user):
    """
    Авторизованный клиент от имени второго пользователя.
    Тоже создаёт свой экземпляр APIClient.
    """
    client = APIClient()
    client.force_authenticate(user=another_user)
    return client


# ============================
# Фикстуры файлов
# ============================

@pytest.fixture
def pdf_file():
    """Имитация PDF файла для загрузки"""
    return SimpleUploadedFile(
        name='test_document.pdf',
        content=b'%PDF-1.4 test content',  # Минимальный PDF контент
        content_type='application/pdf'
    )


@pytest.fixture
def image_file():
    """Настоящее PNG изображение через Pillow"""
    img = Image.new('RGB', (100, 100), color='red')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return SimpleUploadedFile(
        name='test_image.png',
        content=buffer.read(),
        content_type='image/png'
    )


@pytest.fixture
def large_file():
    """Файл размером больше 10 МБ — для проверки валидации"""
    return SimpleUploadedFile(
        name='large_file.pdf',
        # 11 МБ нулей
        content=b'0' * (11 * 1024 * 1024),
        content_type='application/pdf'
    )


@pytest.fixture
def invalid_file():
    """Файл с недопустимым расширением"""
    return SimpleUploadedFile(
        name='virus.exe',
        content=b'MZ malicious content',
        content_type='application/octet-stream'
    )


@pytest.fixture
def document(db, user, pdf_file):
    """Готовый документ в базе данных для тестов"""
    from documents.models import Document
    return Document.objects.create(
        owner=user,
        title='Тестовый документ',
        file=pdf_file,
        description='Описание тестового документа'
    )
