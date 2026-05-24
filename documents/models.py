import os
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def user_directory_path(instance, filename):
    """
    Генерирует путь для сохранения файла.
    Каждый пользователь получает свою папку:
    media/documents/user_1/filename.pdf

    Это важно для безопасности — файлы разных
    пользователей физически разделены!
    """
    return f'documents/user_{instance.owner.id}/{filename}'


class Document(models.Model):
    """
    Модель документа.
    Каждый документ принадлежит конкретному пользователю.
    """

    # Типы разрешённых файлов
    class FileType(models.TextChoices):
        PDF = 'pdf', 'PDF'
        DOCX = 'docx', 'DOCX'
        IMAGE = 'image', 'Изображение'
        OTHER = 'other', 'Другое'

    # Владелец документа — связь с пользователем
    # on_delete=CASCADE означает: удалили пользователя → удалились все его документы
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='documents',  # user.documents.all() — все документы пользователя
        verbose_name='Владелец'
    )

    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )

    # Сам файл — сохраняется в папку по функции выше
    file = models.FileField(
        upload_to=user_directory_path,
        verbose_name='Файл'
    )

    file_type = models.CharField(
        max_length=10,
        choices=FileType.choices,
        default=FileType.OTHER,
        verbose_name='Тип файла'
    )

    file_size = models.PositiveIntegerField(
        default=0,
        verbose_name='Размер файла (байт)'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,  # Ставится автоматически при создании
        verbose_name='Дата загрузки'
    )

    updated_at = models.DateTimeField(
        auto_now=True,  # Обновляется автоматически при каждом сохранении
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        # Сортировка: сначала новые
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'{self.title} ({self.owner.username})'

    def get_file_type(self):
        """
        Определяем тип файла по расширению автоматически.
        Вызываем при сохранении.
        """
        ext = os.path.splitext(self.file.name)[1].lower()
        type_map = {
            '.pdf': self.FileType.PDF,
            '.docx': self.FileType.DOCX,
            '.doc': self.FileType.DOCX,
            '.jpg': self.FileType.IMAGE,
            '.jpeg': self.FileType.IMAGE,
            '.png': self.FileType.IMAGE,
        }
        return type_map.get(ext, self.FileType.OTHER)

    def save(self, *args, **kwargs):
        """
        Переопределяем save() чтобы автоматически
        заполнять file_type и file_size при сохранении
        """
        if self.file:
            self.file_type = self.get_file_type()
            self.file_size = self.file.size
        super().save(*args, **kwargs)
        