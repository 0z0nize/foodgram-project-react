from core.filters import IngredientFilter, RecipeFilter
from core.pagination import CustomPagination
from core.permissions import IsAuthorOrReadOnly
from django.db.models import Model, QuerySet, Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import SerializerMetaclass
from users.models import Follow, User

from .serializers import (
    FavoriteSerializer,
    FollowListSerializer,
    FollowSerializer,
    IngredientSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    ShoppingCartSerializer,
    TagSerializer,
    UserSerializer,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с тэгами."""

    queryset = Tag.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = TagSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для работы с игридиентами."""

    queryset = Ingredient.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = IngredientSerializer
    pagination_class = None
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с рецептами."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self) -> SerializerMetaclass:
        """Метод определяет сериализатор в соответствии запросу."""
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @staticmethod
    def add_to(
        serializer_class: SerializerMetaclass, request: Request, pk: str
    ) -> Response:
        """Метод добавления объекта."""
        context = {'request': request}
        recipe = get_object_or_404(Recipe, id=pk)
        data = {'user': request.user.id, 'recipe': recipe.id}
        serializer = serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def del_from(model: Model, request: Request, pk: str) -> Response:
        """Метод удаления объекта соответствующей модели."""
        get_object_or_404(
            model, user=request.user, recipe=get_object_or_404(Recipe, id=pk)
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='favorite',
    )
    def favorites(self, request: Request, pk: str) -> Response:
        """Добавляет/удалет рецепт в `избранное`."""
        if request.method == 'POST':
            return self.add_to(FavoriteSerializer, request, pk)
        return self.del_from(Favorite, request, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='shopping_cart',
    )
    def shopping_cart(self, request: Request, pk: str) -> Response:
        """Добавляет/удаляет рецепт в `список покупок`."""
        if request.method == 'POST':
            return self.add_to(ShoppingCartSerializer, request, pk)
        return self.del_from(ShoppingCart, request, pk)

    @staticmethod
    def download_shopping_list(ingredients: QuerySet) -> HttpResponse:
        """Метод выгружает список покупок в формате txt."""
        shopping_list = 'Нужно купить:'
        for ingredient in ingredients:
            shopping_list += (
                f'\n{ingredient["ingredient__name"]} '
                f'({ingredient["ingredient__measurement_unit"]}) - '
                f'{ingredient["amount"]}'
            )
        filename = 'shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename = {filename}'
        return response

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='download_shopping_cart',
    )
    def make_shopping_list(self, request: Request) -> HttpResponse:
        """Метод формирует список покупок."""
        ingredients = (
            IngredientRecipe.objects.filter(
                recipe__shopping_cart__user=request.user
            )
            .order_by('ingredient__name')
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(amount=Sum('amount'))
        )
        return self.download_shopping_list(ingredients)


class UserViewSet(DjoserUserViewSet):
    """ViewSet для работы с пользователми."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['patch', 'get', 'post', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
        url_path='me',
    )
    def get_or_update_self(self, request: Request) -> Response:
        """Метод получение или изменения пользователя
        в зависимости от типа запроса.
        """
        if request.method != 'GET':
            serializer = self.get_serializer(
                instance=request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=serializer.instance.role)
            return Response(serializer.data)
        serializer = self.get_serializer(request.user, many=False)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='subscribe',
    )
    def follow(self, request: Request, id: int = None) -> Response:
        """Создаёт/удалет связь между пользователями."""
        author = get_object_or_404(User, id=id)
        follow_data = {'user': request.user.id, 'author': author.id}
        if request.method == 'POST':
            serializer = FollowSerializer(
                author, data=follow_data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data.get('user')
            author = serializer.validated_data.get('author')
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        get_object_or_404(Follow, user=request.user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='subscriptions',
    )
    def follow_list(self, request: Request) -> Response:
        """Список подписок пользоваетеля."""
        queryset = User.objects.filter(following__user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowListSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
