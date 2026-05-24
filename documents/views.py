from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Document
from .serializers import (
    DocumentUploadSerializer,
    DocumentListSerializer,
    DocumentDetailSerializer,
)


class DocumentListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/documents/        — список своих документов
    POST /api/documents/        — загрузить новый документ
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        ВАЖНО: пользователь видит ТОЛЬКО свои документы!
        Это ключевое правило безопасности сервиса.
        """
        return Document.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        """
        Для GET возвращаем список (меньше полей),
        для POST принимаем файл (другой сериализатор).
        Один view — два разных сериализатора.
        """
        if self.request.method == 'POST':
            return DocumentUploadSerializer
        return DocumentListSerializer


class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/documents/{id}/ — просмотр документа
    PATCH  /api/documents/{id}/ — обновление названия/описания
    DELETE /api/documents/{id}/ — удаление документа
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentDetailSerializer

    def get_queryset(self):
        """Только свои документы"""
        return Document.objects.filter(owner=self.request.user)

    def perform_destroy(self, instance):
        """
        При удалении документа удаляем и сам файл с диска.
        Иначе файлы будут копиться в папке media/ вечно!
        """
        import os
        # Получаем путь к файлу
        file_path = instance.file.path

        # Удаляем запись из базы
        instance.delete()

        # Удаляем файл с диска если он существует
        if os.path.exists(file_path):
            os.remove(file_path)
            