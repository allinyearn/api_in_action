from rest_framework import permissions

class AuthorOrReadOnly(permissions.BasePermission):
    """Это разрешение представляет права на получение объектов
    любым пользователям, добавления объекта аутентифицированным
    пользователям и редактиования объекта только авторам объекта,
    админу или модераторам
    """
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        # return (
        #         request.method in permissions.SAFE_METHODS or
        #         obj.author == request.user or 
        #         moderator == request.user or admin == request.user
        #     )
        return (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
            )
