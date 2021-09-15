import datetime as dt

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Genre, Title, Comment, Review
from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор проверяет на уникальность имя пользователя и email"""

    username = serializers.CharField(
        required=True, validators=[UniqueValidator(
                queryset=User.objects.all(),
        )]
    )
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(
            queryset=User.objects.all(),
        )]
    )

    class Meta:
        fields = ('username', 'email',)
        model = User


class ConfirmCodeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )

    class Meta:
        fields = ('username', 'confirmation_code',)
        model = User


class UserAdminSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        required=True, validators=[UniqueValidator(
                queryset=User.objects.all(),
        )]
    )

    class Meta:
        fields = (
            'username', 'email', 'role',
            'bio', 'first_name', 'last_name',
        )
        model = User


class UserSerializer(UserAdminSerializer):
    role = serializers.CharField(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    reviews = serializers.SlugRelatedField(
        read_only=True,
        slug_field='text',
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'reviews')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'rating', 'genre', 'category'
        )

    def validate_year(self, value):
        year = dt.datetime.today().year
        if not value <= year:
            raise serializers.ValidationError('Произведение из будущего')
        return value


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=False
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        required=False,
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
