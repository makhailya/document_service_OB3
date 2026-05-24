from django.contrib.auth import get_user_model
from rest_framework import serializers

# Получаем нашу кастомную модель пользователя
User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации.
    Принимает: username, email, password, password2
    """
    # Поле для подтверждения пароля — только для записи, в ответ не возвращаем
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']

    def validate(self, attrs):
        """Проверяем что оба пароля совпадают"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Пароли не совпадают'})
        return attrs

    def create(self, validated_data):
        """Создаём пользователя с хешированным паролем"""
        # Убираем password2 — он нам больше не нужен
        validated_data.pop('password2')

        # create_user — метод Django, который хеширует пароль автоматически
        # Никогда не храни пароли в открытом виде!
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра и редактирования профиля
    """
    class Meta:
        model = User
        # Пароль не показываем никогда!
        fields = ['id', 'username', 'email', 'bio', 'date_joined']
        read_only_fields = ['id', 'date_joined']
        