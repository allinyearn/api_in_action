from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import UserRoles


class AuthorOrReadOnly(BasePermission):
    """Это разрешение представляет права на получение объектов
    любым пользователям, добавления объекта аутентифицированным
    пользователям и редактиования объекта только авторам объекта,
    админу или модераторам
    """
    def has_permission(self, request, view):
        return (
                request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == UserRoles.ADMIN
            )

    # def has_object_permission(self, request, view, obj):
        # return (
        #         request.method in permissions.SAFE_METHODS or
        #         obj.author == request.user or 
        #         moderator == request.user or admin == request.user
        #     )
        # return (
        #         request.method in SAFE_METHODS
        #         or obj.author == request.user
        #     )


class IsAdmin(BasePermission):
    """Пермишн только для админа."""

    def has_permission(self, request, view):
        return (request.user.is_superuser
                or request.auth and request.user.is_admin
                )


class IsAdminOrReadOnly(BasePermission):
    """ Пермишен для админа на редактирование контента:
        категорий, жанров, произведений.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
            or request.user.is_superuser
        )
