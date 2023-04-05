from django.contrib.auth.models import AbstractUser
from django.db import models


class RoleChoices(models.TextChoices):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'


class User(AbstractUser):

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    role = models.CharField(
        'роль',
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
        blank=True
    )
    confirmation_code = models.CharField(
        max_length=5, null=True,
        verbose_name='Код подтверждения'
    )

    @property
    def is_user(self):
        return self.role == RoleChoices.USER

    @property
    def is_admin(self):
        return self.role == (
            RoleChoices.ADMIN or self.is_staff or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == RoleChoices.MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='uq_username_email'
            ),
        ]

    def __str__(self):
        return self.username
