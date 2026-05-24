from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, ProfileView, LoginView

urlpatterns = [
    # Регистрация
    path('register/', RegisterView.as_view(), name='register'),

    # Вход — получаем токены
    path('login/', LoginView.as_view(), name='login'),

    # Обновление access токена через refresh токен
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Профиль текущего пользователя
    path('profile/', ProfileView.as_view(), name='profile'),
]
