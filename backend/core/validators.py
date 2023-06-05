from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from rest_framework import serializers


def not_me_username(value: str) -> str:
    """Метод запрещает использовать username 'me'."""
    if value.lower() == 'me':
        raise serializers.ValidationError('Имя пользователя "me"- не доступно')
    return value


UsernameValidator = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message='Имя пользователя содержит недопустимый символ',
)

HexValidator = RegexValidator(
    regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
    message='Проверьте правильность HEX-кода',
)

MinValidator = MinValueValidator(
    settings.MIN_VALUE,
    message='Значение меньше минимального',
)
