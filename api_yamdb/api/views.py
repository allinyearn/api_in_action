from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
# from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status # filters, mixins
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

# from reviews.models import Categories, Title, Genres, Review
from users.models import User
# from .permissions import IsAdmin
from .serializers import (
#     UserSerializer,
      ConfirmCodeSerializer,
      SignUpSerializer,
#     EmailSerializer,
#     UserForAdminSerializer,
#     CommentSerializer,
#     ReviewSerializer,
#     GenresSerializer,
#     CategoriesSerializer,
#     TitlesSerializer,
#     TitleSerializerCreateUpdate
)

ban_names = (
    'me',
    'Me',
    'Voldemort'
)

@api_view(['POST'])
def signup(request):
    serializer_data = SignUpSerializer(data=request.data)
    serializer_data.is_valid(raise_exception=True)
    email = serializer_data.data.get('email')
    username = serializer_data.data.get('username')
    if username in ban_names:
        return Response(
            'Выберите другое имя пользователя!',
            status=status.HTTP_400_BAD_REQUEST
        )
    new_user, create = User.objects.get_or_create(
        username=username,
        email=email,
    )
    confirmation_code = default_token_generator.make_token(new_user)
    send_mail(
        'Youre registration is Done',
        f'Ваш код подтверждения {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
    return Response({
        "email": email,
        "username": username
    })

@api_view(['POST'])
def give_token(request):
    serializer_data = ConfirmCodeSerializer(data=request.data)
    serializer_data.is_valid(raise_exception=True)
    confirmation_code = serializer_data.data.get('confirmation_code')
    username = serializer_data.data.get('username')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        user.is_active=True
        user.save()
        token = AccessToken.for_user(user)
        print(token)
        return Response({
            "token": f"{token}"
        }, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def youself(self, request):
        pass

