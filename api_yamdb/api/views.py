
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
# from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters #, mixins
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Comment, Review, Title, Category, Genre, Title
from users.models import User
from .permissions import AuthorOrReadOnly # , IsAdmin
from .serializers import (
#     UserSerializer,
      ConfirmCodeSerializer,
      SignUpSerializer,
#     EmailSerializer,
#     UserForAdminSerializer,
      CommentSerializer,
      ReviewSerializer,
      GenreSerializer,
      CategorySerializer,
      TitleSerializer,
#     TitleSerializerCreateUpdate
)

ban_names = (
    'me',
    'Me',
    'Voldemort'
)

@api_view(['POST'])
def signup(request):
    """Функция регистрации нового пользователя
    отправляет confirmation_code на указанный email
    Запрещает использовать имя пользователя из кортежа ban_names"""

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
        f'Ваш код подтверждения (confirmation_code) {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
    return Response({
        "email": email,
        "username": username
    })

@api_view(['POST'])
def give_token(request):
    """Выдает токен указаному пользователю, который прислал confirmation_code
    Вылсанный ранее на почту"""

    serializer_data = ConfirmCodeSerializer(data=request.data)
    serializer_data.is_valid(raise_exception=True)
    confirmation_code = serializer_data.data.get('confirmation_code')
    username = serializer_data.data.get('username')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        user.is_active=True
        user.save()
        token = AccessToken.for_user(user)
        return Response({
            "token": f"{token}"
        }, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Изменение данных пользователям им самим"""

    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def youself(self, request):
        pass


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для отзывов к произведению.

    Возваращает список всех отзывов, отзыв по id, 
    может добавить обновить и удалить отзыв по id
    """
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Получаем набор отзывов относящихся к определенному произведению"""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        queryset = title.rewiews.all()
        return queryset

    def perform_create(self, serializer):
        """При создании нового отзыва, автор = пользователь создающий отзыв"""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для комментов к отзыву.

    Возваращает список всех комментов к отзыву, коммент по id, 
    может добавить, обновить и удалить коммент по id
    """
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        """Получаем набор комментов относящихся к определенному отзыву"""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        """При создании нового коммента,
        автор = пользователь создающий коммент,
        отзыв = отзыв с необходимым id
        """
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=name', )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('category', 'genre', 'name', 'year')
