from core.validators import UsernameValidator, not_me_username
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Настроенная под приложение `Foodgram` кастомная модель пользователя."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')
    username = models.CharField(
        max_length=settings.DEFAULT_FIELD_LENGTH,
        verbose_name='Имя пользователя',
        unique=True,
        null=True,
        validators=[UsernameValidator],
    )

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=settings.DEFAULT_EMAIL_LENGTH,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.DEFAULT_FIELD_LENGTH,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.DEFAULT_FIELD_LENGTH,
    )

    def validate_username(self, value: str) -> str:
        """Проверка валидности username"""
        return not_me_username(value)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username


class Follow(models.Model):
    """Модель подписки пользователей друг на друга."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'author'], name='uniq_follow'
            ),
        )
        verbose_name = 'Подписка'
        verbose_name_plural = "Подписки"

    def __str__(self) -> str:
        return f'{self.user.username} подписался на {self.author.username}'
