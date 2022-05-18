from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer модели Post.
    Поля:
    id - идентификационный номер поста (Создается автоматически).
    author - поле связанное по полю username с моделью User (создается
    автоматически).
    text - текст поста.
    pub_date - дата публикации поста (Создается автоматически).
    image - изображение, прикрепленное к посту, если таковое имеется.
    group - Группа к которой прикреплен пост (указывается только id Группы).
    """

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True, many=False
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        model = Post
        read_only_fields = ('id', 'author', 'pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer для модели Comment.
    Поля:
    id - идентификационный номер комментария (создается автоматически).
    author - id пользователя, который оставил комментарий(создается
    автоматичеки).
    text - текст комментария.
    created - дата публикации комментария (создается автоматически).
    post - id объекта класса Post к которому относится комментарий(создается
    автоматически, информация о посте берется из пути).
    """

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username', many=False
    )

    class Meta:
        fields = ('id', 'author', 'text', 'created', 'post')
        model = Comment
        read_only_fields = ('id', 'created', 'author', 'post')


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer для модели Group.
    Доступен только для получения информации о группе(группах).
    Поля:
    id - идентификационный номер группы.
    title - заголовок группы.
    slug - slug группы.
    description - описание группы.
    """

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')
        read_only_fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    """
    Serializer для регистрации подписок на пользователей.
    Поля:
    following - username пользователя на которого хочет подписаться человек.
    user - username пользователя, отправившего запрос. Создается автоматически.
    """

    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        many=False,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate_following(self, obj):
        """Проверка на дурака (нельзя подписываться на самого себя)."""

        if self.context.get('request').user != obj:
            return obj
        raise ValidationError(
            'Нельзя подписываться на самого себя!'
        )
