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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date')


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('score', )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    rating = RatingSerializer(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'category', 'genre'
        )
