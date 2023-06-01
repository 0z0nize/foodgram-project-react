from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from rest_framework import serializers


def not_me_username(value: str) -> str:
    """Метод запрещает использовать uername 'me'."""
    if value.lower() == 'me':
        raise serializers.ValidationError('Имя пользователя "me"- не доступно')
    return value


UsernameValidator = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message='Имя пользователя содержит недопустимый символ',
)

HEX_Validator = RegexValidator(
    regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
    message='Проверьте правильность HEX-кода',
)

MIN_VALUE_Validator = MinValueValidator(
    settings.MIN_VALUE,
    message='Значение меньше минимального',
)
