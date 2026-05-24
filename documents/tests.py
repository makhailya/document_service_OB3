import pytest
from django.urls import reverse
from documents.models import Document


# ============================
# Тесты загрузки документов
# ============================

class TestDocumentUpload:

    def test_upload_pdf_success(self, authenticated_client, user, pdf_file):
        """
        Успешная загрузка PDF файла.
        """
        url = reverse('document-list-create')
        data = {
            'title': 'Мой договор',
            'file': pdf_file,
            'description': 'Договор аренды',
        }

        response = authenticated_client.post(url, data, format='multipart')

        assert response.status_code == 201
        assert Document.objects.filter(owner=user).count() == 1

    def test_upload_image_success(self, authenticated_client, user, image_file):
        """
        Успешная загрузка изображения.
        """
        url = reverse('document-list-create')
        data = {
            'title': 'Скан паспорта',
            'file': image_file,
        }

        response = authenticated_client.post(url, data, format='multipart')

        assert response.status_code == 201

    def test_upload_too_large_file(self, authenticated_client, large_file):
        """
        Файл больше 10 МБ — должна быть ошибка 400.
        """
        url = reverse('document-list-create')
        data = {
            'title': 'Огромный файл',
            'file': large_file,
        }

        response = authenticated_client.post(url, data, format='multipart')

        assert response.status_code == 400
        assert 'file' in response.data

    def test_upload_invalid_extension(self, authenticated_client, invalid_file):
        """
        Недопустимое расширение — ошибка 400.
        """
        url = reverse('document-list-create')
        data = {
            'title': 'Подозрительный файл',
            'file': invalid_file,
        }

        response = authenticated_client.post(url, data, format='multipart')

        assert response.status_code == 400

    def test_upload_unauthenticated(self, api_client, pdf_file):
        """
        Неавторизованный пользователь не может загружать файлы.
        """
        url = reverse('document-list-create')
        data = {'title': 'Чужой файл', 'file': pdf_file}

        response = api_client.post(url, data, format='multipart')

        assert response.status_code == 401

    def test_file_type_detected_automatically(
        self, authenticated_client, user, pdf_file
    ):
        """
        Тип файла определяется автоматически по расширению.
        Пользователь не задаёт его вручную.
        """
        url = reverse('document-list-create')
        data = {'title': 'Договор', 'file': pdf_file}

        authenticated_client.post(url, data, format='multipart')

        doc = Document.objects.get(owner=user)
        assert doc.file_type == Document.FileType.PDF


# ============================
# Тесты изоляции данных (БЕЗОПАСНОСТЬ!)
# ============================

class TestDocumentIsolation:

    def test_user_sees_only_own_documents(
        self,
        authenticated_client,
        another_authenticated_client,
        user,
        another_user,
        pdf_file,
    ):
        """
        КЛЮЧЕВОЙ ТЕСТ БЕЗОПАСНОСТИ:
        Пользователь видит только свои документы,
        но не документы другого пользователя.
        """
        # Первый пользователь загружает файл
        url = reverse('document-list-create')
        authenticated_client.post(
            url,
            {'title': 'Мой документ', 'file': pdf_file},
            format='multipart'
        )

        # Второй пользователь запрашивает список — должен увидеть пустой список
        response = another_authenticated_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 0

    def test_user_cannot_delete_others_document(
        self,
        authenticated_client,
        another_authenticated_client,
        document,
    ):
        """
        Пользователь не может удалить чужой документ — 404.
        (Мы не говорим «нет прав», мы говорим «не найдено» —
        чтобы не раскрывать существование чужих файлов)
        """
        url = reverse('document-detail', kwargs={'pk': document.id})

        # Второй пользователь пытается удалить документ первого
        response = another_authenticated_client.delete(url)

        assert response.status_code == 404


# ============================
# Тесты просмотра и удаления
# ============================

class TestDocumentDetail:

    def test_get_document_detail(self, authenticated_client, document):
        """
        Просмотр своего документа — успешно.
        """
        url = reverse('document-detail', kwargs={'pk': document.id})
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert response.data['title'] == 'Тестовый документ'

    def test_update_document_title(self, authenticated_client, document):
        """
        Обновление названия документа через PATCH.
        """
        url = reverse('document-detail', kwargs={'pk': document.id})
        response = authenticated_client.patch(
            url,
            {'title': 'Новое название'},
        )

        assert response.status_code == 200
        document.refresh_from_db()
        assert document.title == 'Новое название'

    def test_delete_document(self, authenticated_client, user, document):
        """
        Удаление своего документа — 204 No Content.
        После удаления документ не существует в БД.
        """
        url = reverse('document-detail', kwargs={'pk': document.id})
        response = authenticated_client.delete(url)

        assert response.status_code == 204
        assert not Document.objects.filter(id=document.id).exists()

    def test_list_documents(self, authenticated_client, user, document):
        """
        Список документов содержит загруженный документ.
        """
        url = reverse('document-list-create')
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['title'] == 'Тестовый документ'
        