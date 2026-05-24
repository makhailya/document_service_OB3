from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Добавляем поле bio в отображение
    list_display = ['username', 'email', 'is_staff', 'date_joined']
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('bio',)}),
    )
    