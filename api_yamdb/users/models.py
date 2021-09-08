from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoles:
    """ Клас определяющий роли пользователей. ПО ТЗ 4 роли. Суперпользователя
будем вынимать из БД. """

    GUEST = 'guest'  # роль гостя скорее всего не пригодится, пока оставлю
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    choices = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )


class User(AbstractUser):
    """Расширяем модель полями биография и роль"""

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.TextField(
        'Роль',
        max_length=24,
        choices=UserRoles.choices,
        default=UserRoles.GUEST,  # пока роль гостя по дефолту
    )
