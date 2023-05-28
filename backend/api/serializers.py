from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Follow, User


class UserSerializer(DjoserUserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and obj.following.filter(user=request.user).exists()
        )


class FollowListSerializer(UserSerializer):
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


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=('user', 'author')
            )
        ]

    def validate(self, data):
        if self.context['request'].user == data['author']:
            raise serializers.ValidationError('Нельзя подписываться на себя')
        return data

    def to_representation(self, instance):
        return FollowListSerializer(instance).data
