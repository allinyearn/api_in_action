from rest_framework import serializers
from rest_framework.validators import UniqueValidator

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
