from core.validators import UsernameValidatorMixin
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser, UsernameValidatorMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')
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

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
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

    def __str__(self):
        return f'{self.user.username} подписался на {self.author.username}'
