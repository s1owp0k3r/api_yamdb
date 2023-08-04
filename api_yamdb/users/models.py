from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    """User's roles enum"""

    USER = "user", "User"
    MODERATOR = "moderator", "Moderator"
    ADMIN = "admin", "Administrator"


class User(AbstractUser):
    """User model"""

    username = models.CharField(
        max_length=150, unique=True, verbose_name="Username"
    )
    email = models.EmailField(
        max_length=254, unique=True, verbose_name="Email"
    )
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name="First name"
    )
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name="Last name"
    )
    bio = models.TextField(blank=True, verbose_name="Biography")
    role = models.CharField(
        max_length=max([len(role.value) for role in Role]),
        choices=Role.choices,
        default=Role.USER,
        verbose_name="Role",
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "user"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def is_admin(self):
        return self.role == Role.ADMIN or self.is_superuser

    def is_moderator(self):
        return self.role in (Role.MODERATOR, Role.ADMIN) or self.is_superuser
