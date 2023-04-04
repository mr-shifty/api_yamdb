# from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User
from users.validators import username_me


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации.
       Следит за уникальностью полей email и username,
       валидирует username"""
    email = serializers.EmailField(
        max_length=254, required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'email',
            'username')

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                "Использовать слово 'me' для username нельзя."
            )
        return username


class UserSignUpSerializer(serializers.Serializer):
    """Сериалайзер для отправки письма пользователю."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        max_length=150,
    )
    email = serializers.EmailField()

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(
            username__iexact=username, email__iexact=email
        ).exists():
            return data
        return data


class UserSignUpValidationSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации пользователей."""

    class Meta:
        model = User
        fields = ('username', 'email',)
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ),
        ]

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя')
        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже зарегистрирован'
            )
        return username

    def validate_email(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже зарегистрирован'
            )
        return email

class TokenSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения токена.
       Проверяет наличие username и валидирует
       код подтверждения."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        max_length=150,
    )
    confirmation_code = serializers.CharField(
        required=True)   # CharField, функция из utils генерирует строку

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code')

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if not username and not confirmation_code:
            raise serializers.ValidationError(
                f"Пустые поля: {username}, {confirmation_code}"
            )
        return data

    def validate_username(self, username):
        if not username:
            raise serializers.ValidationError(
                'Поле username не должно быть пустым'
            )
        return username


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для кастомной модели пользователя"""

    username = serializers.RegexField(max_length=150,
                                      regex=r'^[\w.@+-]+\Z', required=True)

    class Meta:
        abstract = True
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует!')
        return username_me(value)


class UserEditSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения профиля автором"""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):

    """Сериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
