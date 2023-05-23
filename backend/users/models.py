from django.conf import settings

# from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.validators import UsernameValidatorMixin


class User(AbstractUser, UsernameValidatorMixin):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=settings.DEFAULT_EMAIL_LENGTH,
        unique=True,
    )
    # username = models.CharField(verbose_name='Уникальный юзернейм',
    #                             max_length=settings.DEFAULT_FIELD_LENGTH,
    #                             validators=[
    #                                 RegexValidator(
    #                                     regex=r'^[\w.@+-]+$',
    #                                     message='Имя пользователя содержит '
    #                                             'недопустимый символ',
    #                                 )
    #                             ],
    #                             )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.DEFAULT_FIELD_LENGTH,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.DEFAULT_FIELD_LENGTH,
    )
    #         is_subscribed:
    #           type: boolean
    #           readOnly: true
    #           description: "Подписан ли текущий пользователь на этого"
    #           example: false
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

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
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user.username} подписался на {self.author.username}'


# Create your models here.
#  User:
#       description:  'Пользователь (В рецепте - автор рецепта)'
#       type: object
#       properties:
#         email:
#           type: string
#           format: email
#           maxLength: 254
#           description: "Адрес электронной почты"
#         id:
#           type: integer
#           readOnly: true
#         username:
#           type: string
#           description: "Уникальный юзернейм"
#           pattern: ^[\w.@+-]+\z
#           maxLength: 150
#         first_name:
#           type: string
#           maxLength: 150
#           description: "Имя"
#           example: "Вася"
#         last_name:
#           type: string
#           maxLength: 150
#           description: "Фамилия"
#           example: "Пупкин"
#         is_subscribed:
#           type: boolean
#           readOnly: true
#           description: "Подписан ли текущий пользователь на этого"
#           example: false
#       required:
#         - username
