from collections import OrderedDict
from typing import List

from django.conf import settings
from djoser.serializers import UserSerializer as DjoserUserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import Follow, User


class UserSerializer(DjoserUserSerializer):
    """Сериализатор для использования с моделью User."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj: User) -> bool:
        """Проверка подписки пользователей."""
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and obj.following.filter(user=request.user).exists()
        )


class FollowListSerializer(UserSerializer):
    """Сериализатор вывода авторов на которых подписан текущий пользователь."""

    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')
        read_only_fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
        )

    def get_recipes(self, obj: User) -> OrderedDict:
        """Показывает рецепты в моей подписке."""
        request = self.context.get('request')
        if not request:
            return False
        limit = request.GET.get('recipes_limit')
        queryset = obj.recipes.all()
        if limit:
            queryset = queryset[: int(limit)]
        return RecipeShortSerializer(queryset, many=True).data

    def get_recipes_count(self, obj: User) -> int:
        """Показывает общее количество рецептов у каждого автора."""
        return obj.recipes.count()


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки на авторов."""

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=('user', 'author')
            )
        ]

    def validate(self, data: OrderedDict) -> OrderedDict:
        """Проверка подписки на себя."""
        if self.context['request'].user == data['author']:
            raise serializers.ValidationError('Нельзя подписываться на себя')
        return data

    def to_representation(self, instance: User) -> dict:
        """Отображает подписку."""
        return FollowListSerializer(instance).data


class TagSerializer(serializers.ModelSerializer):
    """Cериализатор отображение тэгов."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода ингридиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для отобоажения ингридиетов в рецепте."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit')


class IngredientRecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания ингридиентов."""

    id = serializers.SlugRelatedField(
        queryset=Ingredient.objects.all(), slug_field='id'
    )
    amount = serializers.IntegerField(write_only=True, min_value=1)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""

    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    image = Base64ImageField(max_length=None)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredients(self, obj: Recipe) -> OrderedDict:
        """Получает ингридиенты для рецепта."""
        ingredients = IngredientRecipe.objects.filter(recipe=obj).all()
        return IngredientRecipeReadSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj: Recipe) -> bool:
        """Проверяет рецепт в избранном."""
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and obj.favorites.filter(user=request.user).exists()
        )

    def get_is_in_shopping_cart(self, obj: Recipe) -> bool:
        """Проверяет рецепт в корзине покупок."""
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and obj.shopping_cart.filter(user=request.user).exists()
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Cериализатор создания рецепта."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = IngredientRecipeCreateSerializer(many=True)
    author = UserSerializer(read_only=True)
    image = Base64ImageField(max_length=None)
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate_tags(self, tags: List[Tag]) -> List[Tag]:
        """Проверка введёных данных тега."""
        tags_list = []
        if not tags:
            raise serializers.ValidationError(
                {'tags': 'Нужно выбрать хотя бы один тег'}
            )
        for tag in tags:
            if not Tag.objects.filter(id=tag.id).exists():
                raise serializers.ValidationError(
                    'Указанного тега не существует'
                )
            if tag.id in tags_list:
                raise serializers.ValidationError(
                    'Теги рецепта не могут повторяться'
                )
            tags_list.append(tag.id)
        return tags

    def validate_ingredients(self, ingredients: OrderedDict) -> OrderedDict:
        """Проверка введёных данных ингридиентов."""
        ingredients_list = []
        if not ingredients:
            raise serializers.ValidationError(
                'Нужно выбрать хотя бы один ингредиент'
            )
        for ingredient in ingredients:
            if ingredient in ingredients_list:
                raise serializers.ValidationError(
                    'Ингредиенты в рецепте не могут повторяться'
                )
            ingredients_list.append(ingredient)
            if int(ingredient.get('amount')) < settings.MIN_VALUE:
                raise serializers.ValidationError(
                    'Укажите верное кол-во ингредиента'
                )
        return ingredients

    def validate_cooking_time(self, cooking_time: int) -> int:
        """Проверка введёных данных времени приготовления."""
        if cooking_time < settings.MIN_VALUE:
            raise serializers.ValidationError(
                'Время приготовления должно отличаться от нуля'
            )
        return cooking_time

    @staticmethod
    def add_ingredients(recipe, ingredients: OrderedDict) -> None:
        """Добавляет новые инткредиенты."""
        IngredientRecipe.objects.bulk_create(
            [
                IngredientRecipe(
                    ingredient=ingredient.pop('id'),
                    recipe=recipe,
                    amount=ingredient.pop('amount'),
                )
                for ingredient in ingredients
            ]
        )

    def create(self, validated_data: dict) -> Recipe:
        """Создаёт рецепт."""
        request = self.context.get('request')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        self.add_ingredients(recipe=recipe, ingredients=ingredients)
        return recipe

    def update(self, instance: Recipe, validated_data: dict) -> Recipe:
        """Изменияет рецепт."""
        instance.tags.clear()
        IngredientRecipe.objects.filter(recipe=instance).delete()
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        ingredients = validated_data.pop('ingredients')
        self.add_ingredients(recipe=instance, ingredients=ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance: Recipe) -> dict:
        """Отображает рецепт после создания или измененния."""
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance, context=context).data


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сокращённый сериализатор рецептов для некоторых эндпоинтов."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранного."""

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data: OrderedDict) -> OrderedDict:
        """Проверка на наличие рецепта в избранном."""
        user = data['user']
        if user.favorites.filter(recipe=data['recipe']).exists():
            raise serializers.ValidationError('Рецепт уже в избранном')
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для списка покупок."""

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def validate(self, data: OrderedDict) -> OrderedDict:
        """Проверка рецепта на наличие в списке покупок."""
        user = data['user']
        if user.shopping_cart.filter(recipe=data['recipe']).exists():
            raise serializers.ValidationError('Рецепт уже в корзине')
        return data
