from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserRegisterSerializer, UserProfileSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    POST /api/users/register/
    Регистрация нового пользователя.
    Доступна всем — даже без токена!
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]  # Открытый эндпоинт


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/users/profile/ — просмотр своего профиля
    PUT  /api/users/profile/ — полное обновление
    PATCH /api/users/profile/ — частичное обновление
    Только для авторизованных пользователей!
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Возвращаем только текущего пользователя
        # Пользователь не может смотреть чужой профиль
        return self.request.user


class LoginView(TokenObtainPairView):
    """
    POST /api/users/login/
    Принимает username + password
    Возвращает access и refresh токены
    Наследуем готовый класс из simplejwt
    """
    permission_classes = [permissions.AllowAny]
    