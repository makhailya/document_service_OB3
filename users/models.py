from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Расширенная модель пользователя.
    AbstractUser уже содержит: username, email, password, first_name, last_name.
    Мы добавляем своё поле.
    """
    bio = models.TextField(
        blank=True,         # Поле необязательное
        verbose_name='О себе'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
    