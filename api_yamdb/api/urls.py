from django.urls import include, path
from rest_framework import routers
from .views import give_token, signup #UserViewSet
#
# router = routers.DefaultRouter()
# router.register(r'users', UsersViewSet, basename='users')

# свои эндпоинты к АПИ добавляем сюда
# или роутерами или прямым маршрутом по аналогии)

urlpatterns = [
    path('v1/auth/token/', give_token),
    path('v1/auth/signup/', signup),
    # path('v1/', include(router.urls)),
]