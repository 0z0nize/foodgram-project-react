from django.db.models import Model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение на изменение только автора.
    Остальным только чтение объекта.
    """

    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(
        self, request: Request, view: ModelViewSet, obj: Model
    ) -> bool:
        """Метод проверяет соответсвие типа запроса и уровня доступа."""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
