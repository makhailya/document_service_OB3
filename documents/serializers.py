from rest_framework import serializers
from .models import Document


# Максимальный размер файла — 10 МБ
MAX_FILE_SIZE = 10 * 1024 * 1024

# Разрешённые расширения
ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.doc', '.jpg', '.jpeg', '.png']


class DocumentUploadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для загрузки документа.
    Валидирует файл: размер и расширение.
    """
    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'description']

    def validate_file(self, file):
        """
        Проверяем файл перед сохранением.
        Это наш «фейсконтроль» для файлов 😄
        """
        import os

        # Проверка размера
        if file.size > MAX_FILE_SIZE:
            raise serializers.ValidationError(
                f'Файл слишком большой. Максимум: 10 МБ. '
                f'Размер вашего файла: {file.size // (1024 * 1024)} МБ'
            )

        # Проверка расширения
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise serializers.ValidationError(
                f'Недопустимый тип файла: {ext}. '
                f'Разрешены: {", ".join(ALLOWED_EXTENSIONS)}'
            )

        return file

    def create(self, validated_data):
        """
        При создании автоматически ставим владельца
        из текущего запроса — пользователь не может
        загрузить файл «от чужого имени»
        """
        # request передаётся через context из view
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class DocumentListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка документов.
    Показываем меньше полей — только нужное для списка.
    """
    # Добавляем читаемый размер файла
    file_size_kb = serializers.SerializerMethodField()
    owner_username = serializers.CharField(
        source='owner.username',
        read_only=True
    )

    class Meta:
        model = Document
        fields = [
            'id',
            'title',
            'file_type',
            'file_size_kb',
            'owner_username',
            'uploaded_at',
        ]

    def get_file_size_kb(self, obj):
        """Переводим байты в килобайты для удобства"""
        return round(obj.file_size / 1024, 2)


class DocumentDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детального просмотра документа.
    Показываем все поля включая ссылку на файл.
    """
    file_size_kb = serializers.SerializerMethodField()
    owner_username = serializers.CharField(
        source='owner.username',
        read_only=True
    )

    class Meta:
        model = Document
        fields = [
            'id',
            'title',
            'file',
            'file_type',
            'file_size_kb',
            'description',
            'owner_username',
            'uploaded_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'file_type', 'uploaded_at', 'updated_at']

    def get_file_size_kb(self, obj):
        return round(obj.file_size / 1024, 2)
    