from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User model."""
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    ROLE = [
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор"),
        (USER, "Пользователь"),
    ]

    username = models.CharField(
        max_length=150, unique=True, verbose_name="Имя пользователя"
    )
    email = models.EmailField(
        max_length=254, unique=True, verbose_name="Электронная почта"
    )
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name="Фамилия"
    )
    bio = models.CharField(
        max_length=100, blank=True, verbose_name="Биография"
    )
    role = models.CharField(
        max_length=100, choices=ROLE, default=USER, verbose_name="Роль"
    )

    def __str__(self):
        return self.username
