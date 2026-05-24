import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# ============================
# Тесты регистрации
# ============================

class TestRegistration:

    def test_register_success(self, api_client, db):
        """
        Успешная регистрация нового пользователя.
        Проверяем: статус 201, пользователь создан в БД.
        """
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'strongpassword123',
            'password2': 'strongpassword123',
        }

        response = api_client.post(url, data)

        assert response.status_code == 201
        assert User.objects.filter(username='newuser').exists()

    def test_register_passwords_mismatch(self, api_client, db):
        """
        Пароли не совпадают — должна быть ошибка 400.
        """
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'strongpassword123',
            'password2': 'differentpassword',
        }

        response = api_client.post(url, data)

        assert response.status_code == 400
        assert 'password' in response.data

    def test_register_duplicate_username(self, api_client, user):
        """
        Нельзя зарегистрироваться с уже существующим username.
        """
        url = reverse('register')
        data = {
            'username': 'testuser',  # Этот пользователь уже есть (фикстура user)
            'email': 'other@example.com',
            'password': 'strongpassword123',
            'password2': 'strongpassword123',
        }

        response = api_client.post(url, data)

        assert response.status_code == 400

    def test_register_password_not_returned(self, api_client, db):
        """
        Пароль никогда не должен возвращаться в ответе!
        Это вопрос безопасности.
        """
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'strongpassword123',
            'password2': 'strongpassword123',
        }

        response = api_client.post(url, data)

        assert 'password' not in response.data


# ============================
# Тесты авторизации (JWT)
# ============================

class TestAuthentication:

    def test_login_success(self, api_client, user):
        """
        Успешный вход — получаем access и refresh токены.
        """
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'strongpassword123',
        }

        response = api_client.post(url, data)

        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_wrong_password(self, api_client, user):
        """
        Неверный пароль — доступ запрещён (401).
        """
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }

        response = api_client.post(url, data)

        assert response.status_code == 401

    def test_token_refresh(self, api_client, user):
        """
        Обновление access токена через refresh токен.
        """
        # Сначала логинимся
        login_url = reverse('login')
        login_response = api_client.post(login_url, {
            'username': 'testuser',
            'password': 'strongpassword123',
        })
        refresh_token = login_response.data['refresh']

        # Обновляем access токен
        refresh_url = reverse('token_refresh')
        response = api_client.post(refresh_url, {'refresh': refresh_token})

        assert response.status_code == 200
        assert 'access' in response.data


# ============================
# Тесты профиля
# ============================

class TestProfile:

    def test_get_profile_authenticated(self, authenticated_client, user):
        """
        Авторизованный пользователь получает свой профиль.
        """
        url = reverse('profile')
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert response.data['username'] == 'testuser'

    def test_get_profile_unauthenticated(self, api_client):
        """
        Неавторизованный пользователь не видит профиль (401).
        """
        url = reverse('profile')
        response = api_client.get(url)

        assert response.status_code == 401

    def test_update_profile(self, authenticated_client, user):
        """
        Пользователь может обновить поле bio.
        """
        url = reverse('profile')
        data = {'bio': 'Я люблю Python!'}

        response = authenticated_client.patch(url, data)

        assert response.status_code == 200
        user.refresh_from_db()
        assert user.bio == 'Я люблю Python!'
        